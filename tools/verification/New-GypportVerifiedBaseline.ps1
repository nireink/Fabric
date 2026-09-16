<#
.SYNOPSIS
    Generates the Verified Baseline document of an Owner-accepted, locally committed GYPPORT STEP and registers it
    once in the canonical Reglas.md.

.DESCRIPTION
    GYPPORT-VERIFIED-BASELINE-AUTOMATION-01, specified in
    Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_VERIFIED_BASELINE_AUTOMATION.md.
    A documentation and evidence generator, never an approval engine.

    Its input is a small evidence JSON taken from the controlled commit gate report. The generator:
      1. requires status OWNER_ACCEPTED_COMMITTED_LOCAL and validates every evidence field;
      2. checks with read-only git commands that each accepted commit exists locally, and reads its parents and
         its changed files, whose total must equal verifiedFiles;
      3. renders the baseline Markdown (UTF-8 without BOM, LF) into verification-baselines/. An existing document
         is never overwritten: identical content is left as it is, different content is refused;
      4. appends one compact registration to the canonical Reglas.md, unless the line BASELINE_ID=<id> is already
         there. The append is byte-level: the existing bytes stay an exact prefix, and the file's own line ending
         is used. A compatibility pointer that only redirects to the canonical log is refused.

    Everything is validated before anything is written, so a refused run writes nothing.

    It writes only inside Fabric: the baseline document and, by appending, the canonical rules log
    Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md. It never modifies implementation repositories, never executes
    tests, never approves a baseline, never starts the next STEP, never commits and never pushes. GENERATE_ONLY is
    the default and only mode.

.PARAMETER EvidenceFile
    The evidence JSON file.

.PARAMETER Mode
    GENERATE_ONLY, the default and only accepted value.

.PARAMETER FabricRoot
    The Fabric repository root. Default: two levels above this script.

.PARAMETER OutputDirectory
    The directory that receives the baseline document. Default:
    <FabricRoot>\Knowledge\00-GYPPORT-UNIVERSE\verification-baselines. It must be named verification-baselines;
    disposable validation passes a temporary directory with that name.

.PARAMETER ReglasPath
    The canonical, append-only rules log. Default: <FabricRoot>\Knowledge\00-GYPPORT-UNIVERSE\Reglas.md. It must be
    named Reglas.md, and a compatibility pointer (a file that starts with a "# MOVED" heading) is refused;
    disposable validation passes a temporary copy.

.PARAMETER WorkspaceRoot
    The GYPPORT workspace root, which contains Gystigo, Fabric and Modules. Default: the parent of FabricRoot. A
    repository is found at <WorkspaceRoot>\<name> or <WorkspaceRoot>\Modules\<name>, unless its evidence entry
    gives a path.

.EXAMPLE
    .\Fabric\tools\verification\New-GypportVerifiedBaseline.ps1 -EvidenceFile .\Fabric\.verification\evidence\pkg2c.json -Mode GENERATE_ONLY
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$EvidenceFile,

    [ValidateSet('GENERATE_ONLY')]
    [string]$Mode = 'GENERATE_ONLY',

    [string]$FabricRoot = '',

    [string]$OutputDirectory = '',

    [Alias('RulesFile')]
    [string]$ReglasPath = '',

    [string]$WorkspaceRoot = ''
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'
$Mode = 'GENERATE_ONLY'

# This file stays ASCII: Windows PowerShell 5.1 reads a script without a byte order mark in the ANSI code page.
# The non-ASCII characters of the output are therefore built from their code points.
$EmDash = [string][char]0x2014
$RegisteredSign = [string][char]0x00AE
$SmallUAcute = [string][char]0x00FA

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$Utf8Strict = New-Object System.Text.UTF8Encoding($false, $true)

$AcceptedStatus = 'OWNER_ACCEPTED_COMMITTED_LOCAL'
$CanonicalDirectory = 'Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines'
$ReusePolicyPath = $CanonicalDirectory + '/VERIFIED_BASELINE_REUSE.md'
$GeneratorPath = 'Fabric/tools/verification/New-GypportVerifiedBaseline.ps1'
$RequiredFields = @('baselineId', 'step', 'phase', 'date', 'migrationHead', 'repositories', 'verifiedFiles', 'status')
$OptionalFields = @('verification', 'invariants', 'knownDebts', 'invalidationTriggers', 'supersedes')
$RepositoryFields = @('name', 'commit', 'path')
$BaselineIdPattern = '^GYPPORT-(?<subject>[A-Z0-9]+(?:-[A-Z0-9]+)*)-VERIFIED-BASELINE-(?<date>[0-9]{4}-[0-9]{2}-[0-9]{2})$'

function Stop-Generator([string]$Reason) {
    throw (New-Object System.InvalidOperationException($Reason))
}

function Resolve-FullPath([string]$Path) {
    $unresolved = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
    return [System.IO.Path]::GetFullPath($unresolved)
}

function Get-Sha256([byte[]]$Bytes) {
    $algorithm = [System.Security.Cryptography.SHA256]::Create()
    try { return [System.BitConverter]::ToString($algorithm.ComputeHash($Bytes)).Replace('-', '') }
    finally { $algorithm.Dispose() }
}

function Test-Scalar($Value) {
    return ($Value -is [string] -or $Value -is [int] -or $Value -is [long] -or $Value -is [double] -or
        $Value -is [decimal] -or $Value -is [bool])
}

function Assert-Line($Text, [string]$What) {
    if (-not ($Text -is [string]) -or [string]::IsNullOrWhiteSpace($Text)) {
        Stop-Generator ($What + ' must be a non-empty string.')
    }
    if ($Text -match '[\r\n]') { Stop-Generator ($What + ' must be a single line.') }
    if ($Text.Contains('```')) { Stop-Generator ($What + ' must not contain a Markdown code fence.') }
}

function Assert-Format($Text, [string]$Pattern, [string]$What) {
    Assert-Line $Text $What
    if ($Text -cnotmatch $Pattern) { Stop-Generator ($What + ' has an invalid format: ' + $Text) }
}

# An evidence object of KEY: value pairs, rendered as KEY=value lines. An array value gives one line per item.
function Get-KeyValueLines($Object, [string]$What) {
    $lines = New-Object System.Collections.Generic.List[string]
    if ($null -eq $Object) { return , $lines }
    if (-not ($Object -is [System.Management.Automation.PSCustomObject])) { Stop-Generator ($What + ' must be a JSON object.') }
    foreach ($property in $Object.PSObject.Properties) {
        $key = $property.Name
        if ($key -cnotmatch '^[A-Za-z0-9_./-]+$') { Stop-Generator ($What + ' has an invalid key: ' + $key) }
        $value = $property.Value
        if ($null -eq $value) { Stop-Generator ($What + '.' + $key + ' must not be null.') }
        $items = @($value)
        if ($items.Count -eq 0) { Stop-Generator ($What + '.' + $key + ' must not be empty.') }
        foreach ($item in $items) {
            if (-not (Test-Scalar $item)) { Stop-Generator ($What + '.' + $key + ' must hold text, numbers or booleans.') }
            $text = [string]$item
            Assert-Line $text ($What + '.' + $key)
            $lines.Add($key + '=' + $text)
        }
    }
    return , $lines
}

function Get-TextItems($Value, [string]$What) {
    $items = New-Object System.Collections.Generic.List[string]
    if ($null -eq $Value) { return , $items }
    if (-not ($Value -is [System.Array])) { Stop-Generator ($What + ' must be a JSON array of strings.') }
    foreach ($item in $Value) {
        Assert-Line $item ($What + ' item')
        $items.Add($item)
    }
    return , $items
}

# Read-only git: cat-file, rev-list, diff-tree and merge-base never write to a repository.
function Invoke-GitRead([string]$Repository, [string[]]$Arguments) {
    $ErrorActionPreference = 'Continue'
    $output = @(& git -C $Repository -c core.quotepath=off @Arguments 2>$null)
    return [pscustomobject]@{ ExitCode = $LASTEXITCODE; Lines = $output }
}

function Add-Fence($Target, $Lines) {
    $Target.Add('```text')
    foreach ($line in $Lines) { $Target.Add([string]$line) }
    $Target.Add('```')
}

$report = New-Object System.Collections.Generic.List[string]
$documentState = 'NOT_WRITTEN'
$registrationState = 'NOT_APPENDED'
$exitCode = 0
$previousOutputEncoding = $null

try {
    try {
        $previousOutputEncoding = [Console]::OutputEncoding
        [Console]::OutputEncoding = $Utf8NoBom
    }
    catch {
        $previousOutputEncoding = $null
    }

    # --- Paths and write targets ----------------------------------------------------------------------------------
    if ([string]::IsNullOrWhiteSpace($FabricRoot)) { $FabricRoot = Join-Path $PSScriptRoot '..\..' }
    $FabricRoot = Resolve-FullPath $FabricRoot
    if (-not (Test-Path -LiteralPath $FabricRoot -PathType Container)) { Stop-Generator ('Fabric root not found: ' + $FabricRoot) }
    if ([string]::IsNullOrWhiteSpace($WorkspaceRoot)) { $WorkspaceRoot = Split-Path -Parent $FabricRoot }
    $WorkspaceRoot = Resolve-FullPath $WorkspaceRoot
    $canonicalOutput = Resolve-FullPath (Join-Path $FabricRoot 'Knowledge\00-GYPPORT-UNIVERSE\verification-baselines')
    if ([string]::IsNullOrWhiteSpace($OutputDirectory)) { $OutputDirectory = $canonicalOutput }
    $OutputDirectory = (Resolve-FullPath $OutputDirectory).TrimEnd('\', '/')
    $canonicalReglas = Resolve-FullPath (Join-Path $FabricRoot 'Knowledge\00-GYPPORT-UNIVERSE\Reglas.md')
    if ([string]::IsNullOrWhiteSpace($ReglasPath)) { $ReglasPath = $canonicalReglas }
    $ReglasPath = Resolve-FullPath $ReglasPath
    $EvidenceFile = Resolve-FullPath $EvidenceFile

    if (-not (Test-Path -LiteralPath $EvidenceFile -PathType Leaf)) { Stop-Generator ('Evidence file not found: ' + $EvidenceFile) }
    if ([System.IO.Path]::GetFileName($OutputDirectory) -ne 'verification-baselines') {
        Stop-Generator ('The output directory must be named verification-baselines: ' + $OutputDirectory)
    }
    if (-not (Test-Path -LiteralPath $OutputDirectory -PathType Container)) { Stop-Generator ('Output directory not found: ' + $OutputDirectory) }
    if ([System.IO.Path]::GetFileName($ReglasPath) -ne 'Reglas.md') {
        Stop-Generator ('The registration target must be a file named Reglas.md: ' + $ReglasPath)
    }
    if (-not (Test-Path -LiteralPath $ReglasPath -PathType Leaf)) { Stop-Generator ('Reglas.md not found: ' + $ReglasPath) }
    if ($null -eq (Get-Command git -CommandType Application -ErrorAction SilentlyContinue)) {
        Stop-Generator 'git was not found, so the accepted commits cannot be verified.'
    }

    # --- Evidence ------------------------------------------------------------------------------------------------
    $raw = Get-Content -LiteralPath $EvidenceFile -Raw -Encoding UTF8
    $evidence = $null
    try { $evidence = $raw | ConvertFrom-Json }
    catch { Stop-Generator ('The evidence file is not valid JSON: ' + $_.Exception.Message) }
    if (-not ($evidence -is [System.Management.Automation.PSCustomObject])) { Stop-Generator 'The evidence must be a JSON object.' }

    $fields = @{}
    foreach ($property in $evidence.PSObject.Properties) {
        if (($RequiredFields + $OptionalFields) -notcontains $property.Name) { Stop-Generator ('Unknown evidence field: ' + $property.Name) }
        $fields[$property.Name] = $property.Value
    }
    foreach ($field in $RequiredFields) {
        if (-not $fields.ContainsKey($field) -or $null -eq $fields[$field]) { Stop-Generator ('Missing required evidence field: ' + $field) }
    }

    $status = $fields['status']
    if (-not ($status -is [string]) -or $status -cne $AcceptedStatus) {
        Stop-Generator ('The evidence status must be ' + $AcceptedStatus + '. Actual: ' + [string]$status)
    }

    $baselineId = $fields['baselineId']
    Assert-Format $baselineId $BaselineIdPattern 'baselineId'
    $idMatch = [regex]::Match($baselineId, $BaselineIdPattern)
    $subject = $idMatch.Groups['subject'].Value
    $idDate = $idMatch.Groups['date'].Value

    $date = $fields['date']
    Assert-Format $date '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' 'date'
    $parsedDate = [datetime]::MinValue
    if (-not [datetime]::TryParseExact($date, 'yyyy-MM-dd', [System.Globalization.CultureInfo]::InvariantCulture,
            [System.Globalization.DateTimeStyles]::None, [ref]$parsedDate)) {
        Stop-Generator ('date is not a calendar date: ' + $date)
    }
    if ($idDate -cne $date) { Stop-Generator ('The date in baselineId (' + $idDate + ') differs from date (' + $date + ').') }

    $step = $fields['step']
    Assert-Format $step '^[A-Za-z0-9_.-]+$' 'step'
    $phase = $fields['phase']
    Assert-Format $phase '^[A-Za-z0-9_.-]+$' 'phase'
    $migrationHead = $fields['migrationHead']
    Assert-Format $migrationHead '^V[0-9]+(?:[._][0-9]+)*$' 'migrationHead'

    $verifiedFiles = $fields['verifiedFiles']
    if (-not ($verifiedFiles -is [int] -or $verifiedFiles -is [long]) -or $verifiedFiles -lt 1) {
        Stop-Generator ('verifiedFiles must be a positive integer. Actual: ' + [string]$verifiedFiles)
    }

    $supersedes = ''
    if ($null -ne $fields['supersedes']) {
        $supersedes = $fields['supersedes']
        Assert-Format $supersedes $BaselineIdPattern 'supersedes'
        if ($supersedes -ceq $baselineId) { Stop-Generator 'A baseline cannot supersede itself.' }
    }

    $verificationLines = Get-KeyValueLines $fields['verification'] 'verification'
    $invariantLines = Get-KeyValueLines $fields['invariants'] 'invariants'
    $knownDebts = Get-TextItems $fields['knownDebts'] 'knownDebts'
    $knownDebtsRecorded = $null -ne $fields['knownDebts']
    $triggers = Get-TextItems $fields['invalidationTriggers'] 'invalidationTriggers'

    # --- Accepted commits, checked read-only in the local repositories -------------------------------------------
    $repositoriesValue = $fields['repositories']
    if (-not ($repositoriesValue -is [System.Array]) -or $repositoriesValue.Count -eq 0) {
        Stop-Generator 'repositories must be a non-empty JSON array.'
    }
    $repositories = New-Object System.Collections.Generic.List[object]
    $seen = @{}
    foreach ($entry in $repositoriesValue) {
        if (-not ($entry -is [System.Management.Automation.PSCustomObject])) { Stop-Generator 'Each repositories entry must be a JSON object.' }
        $entryFields = @{}
        foreach ($property in $entry.PSObject.Properties) {
            if ($RepositoryFields -notcontains $property.Name) { Stop-Generator ('Unknown repositories field: ' + $property.Name) }
            $entryFields[$property.Name] = $property.Value
        }
        $name = $entryFields['name']
        Assert-Format $name '^[A-Za-z0-9_.-]+$' 'repositories.name'
        $commit = $entryFields['commit']
        Assert-Format $commit '^[0-9a-fA-F]{40}$' ('repositories.commit of ' + $name)
        $commit = $commit.ToLowerInvariant()
        $key = $name + '@' + $commit
        if ($seen.ContainsKey($key)) { Stop-Generator ('Duplicate repositories entry: ' + $key) }
        $seen[$key] = $true

        $candidates = New-Object System.Collections.Generic.List[string]
        $explicitPath = $entryFields['path']
        if ($null -ne $explicitPath) {
            Assert-Line $explicitPath ('repositories.path of ' + $name)
            if ([System.IO.Path]::IsPathRooted($explicitPath)) { $candidates.Add($explicitPath) }
            else { $candidates.Add((Join-Path $WorkspaceRoot $explicitPath)) }
        }
        else {
            $candidates.Add((Join-Path $WorkspaceRoot $name))
            $candidates.Add((Join-Path (Join-Path $WorkspaceRoot 'Modules') $name))
        }
        $repositoryPath = $null
        foreach ($candidate in $candidates) {
            $full = Resolve-FullPath $candidate
            if (Test-Path -LiteralPath (Join-Path $full '.git')) { $repositoryPath = $full; break }
        }
        if ($null -eq $repositoryPath) {
            Stop-Generator ('Repository ' + $name + ' was not found locally (' + ($candidates -join ', ') + '). Give its path in the evidence entry.')
        }

        $exists = Invoke-GitRead $repositoryPath @('cat-file', '-e', ('{0}^{{commit}}' -f $commit))
        if ($exists.ExitCode -ne 0) { Stop-Generator ('Commit ' + $commit + ' of ' + $name + ' does not exist in ' + $repositoryPath + '.') }
        $revList = Invoke-GitRead $repositoryPath @('rev-list', '--parents', '-n', '1', $commit)
        if ($revList.ExitCode -ne 0 -or $revList.Lines.Count -lt 1) { Stop-Generator ('Cannot read the parents of ' + $commit + ' in ' + $name + '.') }
        $parents = @(([string]$revList.Lines[0]).Trim().Split(' ') | Select-Object -Skip 1)
        $diffTree = Invoke-GitRead $repositoryPath @('diff-tree', '--no-commit-id', '-r', '--root', '--abbrev=12', $commit)
        if ($diffTree.ExitCode -ne 0) { Stop-Generator ('Cannot read the files of ' + $commit + ' in ' + $name + '.') }
        $files = New-Object System.Collections.Generic.List[string]
        foreach ($line in $diffTree.Lines) {
            $text = [string]$line
            if ([string]::IsNullOrWhiteSpace($text)) { continue }
            $tab = $text.IndexOf("`t")
            if (-not $text.StartsWith(':') -or $tab -lt 1) { Stop-Generator ('Unexpected git diff-tree output in ' + $name + ': ' + $text) }
            $meta = $text.Substring(1, $tab - 1).Split(' ')
            if ($meta.Count -lt 5) { Stop-Generator ('Unexpected git diff-tree output in ' + $name + ': ' + $text) }
            $files.Add($meta[4] + ' ' + $meta[3] + ' ' + $text.Substring($tab + 1))
        }
        $ancestorCheck = Invoke-GitRead $repositoryPath @('merge-base', '--is-ancestor', $commit, 'HEAD')
        $ancestor = 'UNKNOWN'
        if ($ancestorCheck.ExitCode -eq 0) { $ancestor = 'YES' }
        elseif ($ancestorCheck.ExitCode -eq 1) { $ancestor = 'NO' }

        $repositories.Add([pscustomobject]@{
                Name = $name; Commit = $commit; Path = $repositoryPath; Parents = $parents; Files = $files; Ancestor = $ancestor
            })
    }

    $totalFiles = 0
    foreach ($repository in $repositories) { $totalFiles += $repository.Files.Count }
    if ($totalFiles -ne $verifiedFiles) {
        Stop-Generator ('verifiedFiles is ' + $verifiedFiles + ' but the accepted commits change ' + $totalFiles + ' files.')
    }

    $fileName = 'GYPPORT_' + $subject.Replace('-', '_') + '_VERIFIED_BASELINE_' + $date + '.md'
    $outFile = Join-Path $OutputDirectory $fileName
    $baselinePath = $CanonicalDirectory + '/' + $fileName
    $acceptedCommits = @($repositories | ForEach-Object { $_.Name + '=' + $_.Commit })

    # --- Baseline document ---------------------------------------------------------------------------------------
    $md = New-Object System.Collections.Generic.List[string]
    $md.Add('# GYPPORT ' + $EmDash + ' ' + $subject + ' Verified Baseline')
    $md.Add('')
    $md.Add('**Baseline ID:** `' + $baselineId + '`  ')
    $md.Add('**Status:** `' + $AcceptedStatus + '`  ')
    $md.Add('**Date:** ' + $date + '  ')
    $md.Add('**Step:** `' + $step + '`  ')
    $md.Add('**Phase:** `' + $phase + '`')
    $md.Add('')
    $md.Add('## Purpose')
    $md.Add('')
    $md.Add('This is the canonical reusable verification baseline of an Owner-accepted, locally committed STEP.')
    $md.Add('')
    $md.Add('Future STEPs MUST NOT rerun its complete historical regression while this baseline remains valid. They first')
    $md.Add('classify it as REUSE, PARTIAL_INVALIDATION or FULL_INVALIDATION under the policy:')
    $md.Add('')
    Add-Fence $md @($ReusePolicyPath)
    $md.Add('')
    $md.Add('## Baseline record')
    $md.Add('')
    $record = New-Object System.Collections.Generic.List[string]
    $record.Add('BASELINE_ID=' + $baselineId)
    $record.Add('STATUS=' + $AcceptedStatus)
    $record.Add('STEP=' + $step)
    $record.Add('PHASE=' + $phase)
    $record.Add('DATE=' + $date)
    $record.Add('MIGRATION_HEAD=' + $migrationHead)
    $record.Add('VERIFIED_FILE_COUNT=' + $verifiedFiles)
    $record.Add('BASELINE_REUSE_ALLOWED=YES')
    if ($supersedes) { $record.Add('SUPERSEDES_BASELINE_ID=' + $supersedes) }
    Add-Fence $md $record
    $md.Add('')
    $md.Add('## Accepted commits')
    $md.Add('')
    Add-Fence $md $acceptedCommits
    $md.Add('')
    $md.Add('Parent commits:')
    $md.Add('')
    $parentLines = New-Object System.Collections.Generic.List[string]
    foreach ($repository in $repositories) {
        if ($repository.Parents.Count -gt 0) { $parentLines.Add($repository.Name + '=' + ($repository.Parents -join ' ')) }
        else { $parentLines.Add($repository.Name + '=NONE') }
    }
    Add-Fence $md $parentLines
    $md.Add('')
    $md.Add('## Accepted commit manifest')
    $md.Add('')
    $md.Add('Secondary evidence read from the accepted commits, one line per file: `<status> <abbreviated blob id> <path>`,')
    $md.Add('with paths relative to the repository.')
    foreach ($repository in $repositories) {
        $md.Add('')
        $block = New-Object System.Collections.Generic.List[string]
        $block.Add($repository.Name + ' ' + $repository.Commit + ' files=' + $repository.Files.Count)
        foreach ($file in $repository.Files) { $block.Add($file) }
        Add-Fence $md $block
    }
    if ($verificationLines.Count -gt 0) {
        $md.Add('')
        $md.Add('## Verification evidence')
        $md.Add('')
        Add-Fence $md $verificationLines
    }
    if ($invariantLines.Count -gt 0) {
        $md.Add('')
        $md.Add('## Architecture invariants')
        $md.Add('')
        Add-Fence $md $invariantLines
    }
    $md.Add('')
    $md.Add('## Known pre-existing debts')
    $md.Add('')
    $debtBlock = New-Object System.Collections.Generic.List[string]
    if ($knownDebtsRecorded) {
        $debtBlock.Add('KNOWN_PREEXISTING_FAILURES=' + $knownDebts.Count)
        for ($i = 0; $i -lt $knownDebts.Count; $i++) { $debtBlock.Add([string]($i + 1) + '. ' + $knownDebts[$i]) }
    }
    else {
        $debtBlock.Add('KNOWN_PREEXISTING_FAILURES=NOT_RECORDED')
    }
    Add-Fence $md $debtBlock
    if ($knownDebts.Count -gt 0) {
        $md.Add('')
        $md.Add('These are not regressions of this STEP. Future STEPs do not fix them unless they are explicitly in scope.')
    }
    $md.Add('')
    $md.Add('## Reuse contract')
    $md.Add('')
    Add-Fence $md @('BASELINE_FOUND=YES', ('BASELINE_ID=' + $baselineId),
        'BASELINE_REUSE_DECISION=REUSE|PARTIAL_INVALIDATION|FULL_INVALIDATION',
        'BASELINE_REUSE_REASON=<short evidence-based reason>')
    $md.Add('')
    $md.Add('REUSE means `FULL_HISTORICAL_REGRESSION_RERUN=NO`: the new STEP runs only its own tests, impact-selected tests')
    $md.Add('and the required integration smoke. The decision is proven from repository ancestry, path and contract impact,')
    $md.Add('migration semantics and current Owner decisions. A complete historical regression is never selected merely')
    $md.Add('"to be safe".')
    if ($triggers.Count -gt 0) {
        $md.Add('')
        $md.Add('## Baseline invalidation triggers')
        $md.Add('')
        foreach ($trigger in $triggers) { $md.Add('- ' + $trigger) }
        $md.Add('')
        $md.Add('An invalidation does not by itself require a full rerun: impact analysis selects the smallest sufficient')
        $md.Add('verification scope.')
    }
    $md.Add('')
    $md.Add('## Closeout')
    $md.Add('')
    Add-Fence $md @(('STATUS=' + $AcceptedStatus), ('GENERATED_BY=' + $GeneratorPath), 'GENERATOR_MODE=GENERATE_ONLY',
        'GENERATOR_APPROVAL=NONE', 'OWNER_REVIEW_REQUIRED=YES', 'AUTO_START_NEXT_STEP=NO',
        'COMMIT_PERFORMED_BY_GENERATOR=NO', 'PUSH_PERFORMED=NO')
    $markdownBytes = $Utf8NoBom.GetBytes(($md -join "`n") + "`n")

    # --- Registration entry, in the style of the Reglas.md log ---------------------------------------------------
    $entry = New-Object System.Collections.Generic.List[string]
    $entry.Add($date + ' ' + $EmDash + ' GYPPORT' + $RegisteredSign + ' Universe / Registro de Verified Baseline ' + $subject)
    $entry.Add('')
    $entry.Add('Verified Baseline de un STEP aceptado por el Owner y committed localmente.')
    $entry.Add('Se reutiliza seg' + $SmallUAcute + 'n VERIFIED_BASELINE_REUSE.')
    $entry.Add('')
    $registrationBlock = New-Object System.Collections.Generic.List[string]
    $registrationBlock.Add('BASELINE_ID=' + $baselineId)
    $registrationBlock.Add('BASELINE_PATH=' + $baselinePath)
    $registrationBlock.Add('STEP=' + $step)
    $registrationBlock.Add('PHASE=' + $phase)
    $registrationBlock.Add('STATUS=' + $AcceptedStatus)
    $registrationBlock.Add('ACCEPTED_COMMITS=' + ($acceptedCommits -join '; '))
    $registrationBlock.Add('MIGRATION_HEAD=' + $migrationHead)
    $registrationBlock.Add('VERIFIED_FILE_COUNT=' + $verifiedFiles)
    $registrationBlock.Add('BASELINE_REUSE_ALLOWED=YES')
    if ($supersedes) { $registrationBlock.Add('SUPERSEDES_BASELINE_ID=' + $supersedes) }
    Add-Fence $entry $registrationBlock

    # --- Reglas.md: read, strict UTF-8, pointer refusal, duplicate check, its own line ending --------------------
    $reglasBytes = [System.IO.File]::ReadAllBytes($ReglasPath)
    $reglasText = $null
    try { $reglasText = $Utf8Strict.GetString($reglasBytes) }
    catch { Stop-Generator ('Reglas.md is not valid UTF-8: ' + $ReglasPath) }
    # A compatibility pointer only redirects to the canonical log and never receives a registration.
    if ($reglasText.TrimStart([char]0xFEFF).TrimStart().StartsWith('# MOVED', [System.StringComparison]::Ordinal)) {
        Stop-Generator ('This Reglas.md is a compatibility pointer, not the rules log; register in the canonical log instead: ' + $ReglasPath)
    }
    $alreadyRegistered = [regex]::IsMatch($reglasText, '(?m)^BASELINE_ID=' + [regex]::Escape($baselineId) + '\r?$')

    $crlfCount = [regex]::Matches($reglasText, "`r`n").Count
    $lfCount = [regex]::Matches($reglasText, "`n").Count
    $eol = "`n"
    if ($crlfCount -gt 0 -and $crlfCount * 2 -ge $lfCount) { $eol = "`r`n" }
    # Entries are separated by two blank lines; count the line ends after the last visible character.
    $trailingLineEnds = 0
    $index = $reglasText.Length - 1
    while ($index -ge 0) {
        $character = $reglasText[$index]
        if ($character -eq "`n") { $trailingLineEnds++ }
        elseif ($character -ne "`r" -and $character -ne ' ' -and $character -ne "`t") { break }
        $index--
    }
    $separator = ''
    if ($index -ge 0) {
        for ($i = $trailingLineEnds; $i -lt 3; $i++) { $separator += $eol }
    }
    $registrationBytes = $Utf8NoBom.GetBytes($separator + ($entry -join $eol) + $eol + $eol)

    # --- Baseline document: never overwrite a different existing document ----------------------------------------
    $documentExists = Test-Path -LiteralPath $outFile -PathType Leaf
    if ($documentExists) {
        $existingDocument = [System.IO.File]::ReadAllBytes($outFile)
        if ((Get-Sha256 $existingDocument) -ne (Get-Sha256 $markdownBytes)) {
            Stop-Generator ('A different baseline document already exists and is never overwritten: ' + $outFile +
                '. A superseding baseline needs its own baselineId.')
        }
    }

    # --- Writes: everything above is validated ------------------------------------------------------------------
    if ($documentExists) {
        $documentState = 'UNCHANGED_ALREADY_PRESENT'
    }
    else {
        $stream = New-Object System.IO.FileStream($outFile, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write,
            [System.IO.FileShare]::None)
        try { $stream.Write($markdownBytes, 0, $markdownBytes.Length) }
        finally { $stream.Dispose() }
        $documentState = 'WRITTEN'
    }

    $appendedBytes = 0
    if ($alreadyRegistered) {
        $registrationState = 'ALREADY_PRESENT_SKIPPED'
    }
    else {
        $stream = New-Object System.IO.FileStream($ReglasPath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite,
            [System.IO.FileShare]::Read)
        try {
            $current = New-Object byte[] ([int]$stream.Length)
            $offset = 0
            while ($offset -lt $current.Length) {
                $count = $stream.Read($current, $offset, $current.Length - $offset)
                if ($count -le 0) { break }
                $offset += $count
            }
            if ($offset -ne $current.Length -or (Get-Sha256 $current) -ne (Get-Sha256 $reglasBytes)) {
                Stop-Generator ('Reglas.md changed while the generator was running; nothing was appended: ' + $ReglasPath)
            }
            [void]$stream.Seek(0, [System.IO.SeekOrigin]::End)
            $stream.Write($registrationBytes, 0, $registrationBytes.Length)
            $stream.Flush()
        }
        finally { $stream.Dispose() }

        $expected = New-Object byte[] ($reglasBytes.Length + $registrationBytes.Length)
        [System.Array]::Copy($reglasBytes, 0, $expected, 0, $reglasBytes.Length)
        [System.Array]::Copy($registrationBytes, 0, $expected, $reglasBytes.Length, $registrationBytes.Length)
        if ((Get-Sha256 ([System.IO.File]::ReadAllBytes($ReglasPath))) -ne (Get-Sha256 $expected)) {
            $registrationState = 'APPEND_VERIFICATION_FAILED'
            Stop-Generator ('Reglas.md is not its previous bytes plus the registration after the append: ' + $ReglasPath)
        }
        $registrationState = 'APPENDED'
        $appendedBytes = $registrationBytes.Length
    }

    $report.Add('GENERATOR=New-GypportVerifiedBaseline')
    $report.Add('MODE=' + $Mode)
    $report.Add('BASELINE_ID=' + $baselineId)
    $report.Add('BASELINE_FILE=' + $outFile)
    $report.Add('BASELINE_PATH=' + $baselinePath)
    $report.Add('OUTPUT_DIRECTORY_IS_CANONICAL=' + $(if ($OutputDirectory -eq $canonicalOutput) { 'YES' } else { 'NO' }))
    $report.Add('BASELINE_DOCUMENT=' + $documentState)
    $report.Add('REGLAS_FILE=' + $ReglasPath)
    $report.Add('REGLAS_IS_CANONICAL=' + $(if ($ReglasPath -eq $canonicalReglas) { 'YES' } else { 'NO' }))
    $report.Add('REGLAS_REGISTRATION=' + $registrationState)
    $report.Add('REGLAS_APPENDED_BYTES=' + $appendedBytes)
    foreach ($repository in $repositories) {
        $report.Add('REPOSITORY=' + $repository.Name + ' COMMIT=' + $repository.Commit + ' EXISTS_LOCALLY=YES ANCESTOR_OF_HEAD=' +
            $repository.Ancestor + ' FILES=' + $repository.Files.Count + ' PATH=' + $repository.Path)
    }
    $report.Add('COMMITS_VERIFIED_LOCALLY=' + $repositories.Count + '/' + $repositories.Count)
    $report.Add('COMMIT_FILES_TOTAL=' + $totalFiles)
    $report.Add('TESTS_EXECUTED=NO')
    $report.Add('COMMIT_PERFORMED=NO')
    $report.Add('PUSH_PERFORMED=NO')
    $report.Add('NEXT_STEP_STARTED=NO')
    $report.Add('OWNER_REVIEW_REQUIRED=YES')
    $report.Add('STATUS=VERIFIED_BASELINE_GENERATED_PENDING_OWNER_REVIEW')
}
catch {
    $exitCode = 1
    $report.Clear()
    $report.Add('GENERATOR=New-GypportVerifiedBaseline')
    $report.Add('MODE=' + $Mode)
    $report.Add('STATUS=REFUSED')
    $report.Add('REASON=' + $_.Exception.Message)
    $report.Add('BASELINE_DOCUMENT=' + $documentState)
    $report.Add('REGLAS_REGISTRATION=' + $registrationState)
    $report.Add('TESTS_EXECUTED=NO')
    $report.Add('COMMIT_PERFORMED=NO')
    $report.Add('PUSH_PERFORMED=NO')
}
finally {
    if ($null -ne $previousOutputEncoding) {
        try { [Console]::OutputEncoding = $previousOutputEncoding } catch { }
    }
}

foreach ($line in $report) { Write-Output $line }
exit $exitCode

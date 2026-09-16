<#
    Set-GypportCurrentStep.ps1

    Validates and materializes the single global GYPPORT CURRENT_STEP continuity pointer.

    It is a closeout helper, not an executor. It never approves a STEP, never modifies application
    code, never executes the prompt source, never runs tests, never commits and never pushes. A
    freshly prepared CURRENT_STEP always defaults to OWNER_EXECUTION_AUTHORIZED=NO.

    Mode:
        GENERATE_ONLY   the only accepted value

    Canonical schema:
        The canonical CURRENT_STEP representation is the contract. Two of its fields are
        step-specific, so they are explicit inputs instead of hard-coded prose:
        -RegressionRerunKey  the regression reuse key name, for example
                             FULL_PKG2C_REGRESSION_RERUN when a STEP reuses an accepted PKG-2C
                             baseline. Default: FULL_HISTORICAL_REGRESSION_RERUN.
        -RegressionRerun     its value, YES or NO. Default: NO.
        -NextAction          the explicit next action, one array entry per output line. Omitted,
                             a neutral next action is written.
        -OwnerExecutionAuthorized  YES only when the Owner has authorized this STEP in the
                             current instruction. The default is NO, and NO is what a closeout
                             prepares; the tool still never authorizes anything by itself.
        Given the canonical inputs of a STEP, the generated file is byte-identical to the
        canonical CURRENT_STEP.md. The tool is reconciled with the canonical file, never the
        other way round.

    Validation before writing:
        - the prompt source exists under the workspace root;
        - every required baseline id is registered in verification-baselines;
        - the track, step id and phase are non-empty;
        - the regression key is an uppercase KEY name and its value is YES or NO;
        - every next action entry is a single line without a Markdown code fence;
        - the output file is named CURRENT_STEP.md.

    Output: KEY=VALUE lines. A successful run ends with
    STATUS=CURRENT_STEP_PREPARED_PENDING_OWNER_REVIEW and exit code 0.
    A refused run prints STATUS=REFUSED and REASON=, and exits with code 1.

    Windows PowerShell 5.1 compatible. ASCII only: PowerShell 5.1 reads a BOM-less script as ANSI.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Track,
    [Parameter(Mandatory = $true)][string]$StepId,
    [string]$Phase = '',
    [string]$StepMode = 'AUDIT_ONLY_FIRST',
    [string]$Status = 'READY_TO_START',
    [Parameter(Mandatory = $true)][string]$PromptSource,
    [string[]]$RequiredBaselines = @(),
    [string]$RegressionRerunKey = 'FULL_HISTORICAL_REGRESSION_RERUN',
    [string]$RegressionRerun = 'NO',
    [string[]]$NextAction = @(),
    [ValidateSet('YES', 'NO')][string]$OwnerExecutionAuthorized = 'NO',
    [string]$Mode = 'GENERATE_ONLY',
    [string]$FabricRoot = '',
    [string]$WorkspaceRoot = '',
    [string]$OutputPath = ''
)

$ErrorActionPreference = 'Stop'

function Stop-Tool([string]$reason) {
    Write-Output 'STATUS=REFUSED'
    Write-Output ('REASON=' + $reason)
    exit 1
}

if ($Mode -ne 'GENERATE_ONLY') {
    Stop-Tool ('the only accepted mode is GENERATE_ONLY: ' + $Mode)
}

if ([string]::IsNullOrWhiteSpace($FabricRoot)) {
    $FabricRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
}
if (-not (Test-Path -LiteralPath $FabricRoot -PathType Container)) {
    Stop-Tool ('Fabric root not found: ' + $FabricRoot)
}
if ([string]::IsNullOrWhiteSpace($WorkspaceRoot)) {
    $WorkspaceRoot = Split-Path -Parent $FabricRoot
}
if (-not (Test-Path -LiteralPath $WorkspaceRoot -PathType Container)) {
    Stop-Tool ('workspace root not found: ' + $WorkspaceRoot)
}

$universe = Join-Path $FabricRoot 'Knowledge\00-GYPPORT-UNIVERSE'
$baselineDir = Join-Path $universe 'verification-baselines'
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $universe 'active-work\CURRENT_STEP.md'
}
if ([System.IO.Path]::GetFileName($OutputPath) -ne 'CURRENT_STEP.md') {
    Stop-Tool ('the output file must be named CURRENT_STEP.md: ' + $OutputPath)
}

foreach ($pair in @(@('Track', $Track), @('StepId', $StepId), @('Status', $Status), @('StepMode', $StepMode))) {
    if ([string]::IsNullOrWhiteSpace($pair[1])) {
        Stop-Tool ($pair[0] + ' must not be empty')
    }
}
if ([string]::IsNullOrWhiteSpace($Phase)) { $Phase = $StepId }

if ($RegressionRerunKey -notmatch '^[A-Z][A-Z0-9_]*$') {
    Stop-Tool ('RegressionRerunKey must be an uppercase KEY name: ' + $RegressionRerunKey)
}
if ($RegressionRerun -notmatch '^(YES|NO)$') {
    Stop-Tool ('RegressionRerun must be YES or NO: ' + $RegressionRerun)
}
foreach ($entry in $NextAction) {
    if ($null -eq $entry) { Stop-Tool 'a NextAction entry must not be null' }
    if ($entry -match '[
]') { Stop-Tool 'each NextAction entry must be a single line' }
    if ($entry.Contains('```')) { Stop-Tool 'NextAction must not contain a Markdown code fence' }
}

# --- the prompt source must exist, resolved from the workspace root ------------------------------
$promptFull = $PromptSource
if (-not [System.IO.Path]::IsPathRooted($promptFull)) {
    $promptFull = Join-Path $WorkspaceRoot ($PromptSource -replace '/', '\')
}
if (-not (Test-Path -LiteralPath $promptFull -PathType Leaf)) {
    Stop-Tool ('PROMPT_SOURCE does not resolve to a file: ' + $PromptSource)
}

# --- every required baseline id must be registered ------------------------------------------------
$known = @{}
if (Test-Path -LiteralPath $baselineDir -PathType Container) {
    $policyDocs = @('VERIFIED_BASELINE_REUSE.md', 'GYPPORT_VERIFIED_BASELINE_AUTOMATION.md')
    foreach ($doc in Get-ChildItem -LiteralPath $baselineDir -Filter '*.md' -File) {
        $isPolicy = $policyDocs -contains $doc.Name
        foreach ($line in (Get-Content -LiteralPath $doc.FullName)) {
            if ($line -match '^\s*BASELINE_ID\s*=\s*(\S+)\s*$') {
                $id = $Matches[1]
                if ($id -like '*<*') { continue }
                if ((-not $known.ContainsKey($id)) -or (-not $isPolicy)) {
                    if ((-not $known.ContainsKey($id)) -or $isPolicy -eq $false) { $known[$id] = $doc.Name }
                }
            }
        }
    }
}
$resolved = @()
foreach ($id in $RequiredBaselines) {
    if ([string]::IsNullOrWhiteSpace($id)) { continue }
    if (-not $known.ContainsKey($id)) {
        Stop-Tool ('required baseline is not registered in verification-baselines: ' + $id)
    }
    $resolved += ($id + ' -> ' + $known[$id])
}

# --- deterministic content ------------------------------------------------------------------------
$baselineValue = ''
if ($RequiredBaselines.Count -gt 0) { $baselineValue = ($RequiredBaselines -join ',') }
$reuseRequired = 'NO'
if ($RequiredBaselines.Count -gt 0) { $reuseRequired = 'YES' }

$nextActionLines = $NextAction
if ($nextActionLines.Count -eq 0) {
    $nextActionLines = @(
        'Wait for explicit Owner authorization. Once authorized, read `PROMPT_SOURCE` completely and execute',
        'this STEP in its declared mode, reusing the required verified baselines instead of rerunning',
        'accepted verification.')
}

$nl = "`n"
$sb = New-Object System.Text.StringBuilder
[void]$sb.Append('# CURRENT STEP' + $nl + $nl)
[void]$sb.Append('The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not' + $nl)
[void]$sb.Append('canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,' + $nl)
[void]$sb.Append('not an Owner approval and not an execution trigger.' + $nl + $nl)
[void]$sb.Append('```text' + $nl)
[void]$sb.Append('CURRENT_TRACK=' + $Track + $nl)
[void]$sb.Append('CURRENT_STEP_ID=' + $StepId + $nl)
[void]$sb.Append('CURRENT_PHASE=' + $Phase + $nl)
[void]$sb.Append('MODE=' + $StepMode + $nl)
[void]$sb.Append('STATUS=' + $Status + $nl + $nl)
[void]$sb.Append('PROMPT_SOURCE=' + $PromptSource + $nl)
[void]$sb.Append('REQUIRED_BASELINES=' + $baselineValue + $nl)
[void]$sb.Append('BASELINE_REUSE_REQUIRED=' + $reuseRequired + $nl)
[void]$sb.Append($RegressionRerunKey + '=' + $RegressionRerun + $nl + $nl)
[void]$sb.Append('OWNER_EXECUTION_AUTHORIZED=' + $OwnerExecutionAuthorized + $nl)
[void]$sb.Append('AUTO_IMPLEMENT_NEXT_STEP=NO' + $nl)
[void]$sb.Append('AUTO_PUSH=NO' + $nl)
[void]$sb.Append('```' + $nl + $nl)
[void]$sb.Append('## Next action' + $nl + $nl)
foreach ($entry in $nextActionLines) { [void]$sb.Append($entry + $nl) }
[void]$sb.Append($nl)
[void]$sb.Append('## How to use this file' + $nl + $nl)
[void]$sb.Append('- Every agent reads this file at startup, before deciding what to work on.' + $nl)
[void]$sb.Append('- `PROMPT_SOURCE` resolves from the GYPPORT workspace root and must be read in full before acting.' + $nl)
[void]$sb.Append('- `REQUIRED_BASELINES` resolves by BASELINE_ID against' + $nl)
[void]$sb.Append('  `Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/`; apply `VERIFIED_BASELINE_REUSE.md`' + $nl)
[void]$sb.Append('  before running any historical regression.' + $nl)
[void]$sb.Append('- `STATUS=READY_TO_START` is not permission. Execution requires `OWNER_EXECUTION_AUTHORIZED=YES` or a' + $nl)
[void]$sb.Append('  current explicit Owner instruction authorizing this STEP.' + $nl)
[void]$sb.Append('- Repository and schema evidence outrank this file. If they disagree, stop and report; never guess.' + $nl)
[void]$sb.Append('- One global CURRENT_STEP exists for the MVP period. Do not create per-module variants without an' + $nl)
[void]$sb.Append('  explicit Owner decision.' + $nl)
[void]$sb.Append('- This file is prepared by the closeout workflow (`Fabric/tools/continuity/`), which never approves,' + $nl)
[void]$sb.Append('  never executes and never commits.' + $nl)

$outDir = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $outDir -PathType Container)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}
$bytes = [System.Text.Encoding]::UTF8.GetBytes($sb.ToString())
[System.IO.File]::WriteAllBytes($OutputPath, $bytes)

Write-Output ('MODE=' + $Mode)
Write-Output ('CURRENT_STEP_PATH=' + $OutputPath)
Write-Output ('CURRENT_TRACK=' + $Track)
Write-Output ('CURRENT_STEP_ID=' + $StepId)
Write-Output ('REGRESSION_RERUN_KEY=' + $RegressionRerunKey)
Write-Output ('REGRESSION_RERUN=' + $RegressionRerun)
Write-Output ('NEXT_ACTION_SOURCE=' + $(if ($NextAction.Count -gt 0) { 'EXPLICIT' } else { 'DEFAULT' }))
Write-Output ('PROMPT_SOURCE_RESOLVED=' + $promptFull)
foreach ($r in $resolved) { Write-Output ('REQUIRED_BASELINE_RESOLVED=' + $r) }
Write-Output ('OWNER_EXECUTION_AUTHORIZED=' + $OwnerExecutionAuthorized)
Write-Output 'AUTO_IMPLEMENT_NEXT_STEP=NO'
Write-Output 'AUTO_PUSH=NO'
Write-Output 'COMMITS=NONE'
Write-Output ('BYTES_WRITTEN=' + $bytes.Length)
Write-Output 'STATUS=CURRENT_STEP_PREPARED_PENDING_OWNER_REVIEW'
exit 0

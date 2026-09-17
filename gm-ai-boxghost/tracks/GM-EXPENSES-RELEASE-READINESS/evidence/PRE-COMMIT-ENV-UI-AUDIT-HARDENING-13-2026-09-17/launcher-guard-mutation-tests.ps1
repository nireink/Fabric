# GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13 - mutation tests of the local launcher's mandatory Shared DEV guard.
# Each mutant is a scratch copy of the hardened launcher with ONE Shared DEV marker injected and with Java start replaced by
# a throw, so no mutant can ever start a backend. Nothing here touches Shared DEV or the running local backend.
param([ValidateSet('Mutants', 'Control')][string]$Phase = 'Mutants')
$ErrorActionPreference = 'Stop'
$launcher = 'D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo\platform_os\server\target\runtime-local\start-runtime-local.ps1'
$jar = (Get-ChildItem -LiteralPath (Join-Path (Split-Path $launcher) 'app') -Filter 'gystigo-host-runtime-*.jar' |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
$workDir = Join-Path $PSScriptRoot 's13-guard-mutants'
New-Item -ItemType Directory -Path $workDir -Force | Out-Null
$refusal = 'Local runtime refused to start because the datasource points to Shared DEV.'
$source = Get-Content -LiteralPath $launcher -Raw
$javaStart = '$process = Start-Process -FilePath $java'
if (([regex]::Matches($source, [regex]::Escape($javaStart))).Count -ne 1) { throw 'Java start line not found exactly once.' }
$neutralized = $source.Replace($javaStart, "throw 'MUTANT_REACHED_JAVA_START'`r`n" + $javaStart)

function New-Mutant([string]$name, [string]$old, [string]$new) {
    $text = $neutralized
    if ($old) {
        $count = ([regex]::Matches($text, [regex]::Escape($old))).Count
        if ($count -ne 1) { throw "Mutation anchor for $name found $count times." }
        $text = $text.Replace($old, $new)
    }
    $path = Join-Path $workDir "$name.ps1"
    [IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($true)))
    return $path
}

function Invoke-Mutant([string]$name, [string]$path, [hashtable]$extraEnv = @{}) {
    $javaBefore = @(Get-CimInstance Win32_Process -Filter "Name='java.exe'" | ForEach-Object ProcessId)
    $saved = @{}
    foreach ($key in $extraEnv.Keys) { $saved[$key] = [Environment]::GetEnvironmentVariable($key, 'Process'); [Environment]::SetEnvironmentVariable($key, $extraEnv[$key], 'Process') }
    try {
        $previous = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
        $output = (& powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $path -Jar $jar 2>&1 | Out-String)
        $exit = $LASTEXITCODE
        $ErrorActionPreference = $previous
    } finally {
        foreach ($key in $saved.Keys) { [Environment]::SetEnvironmentVariable($key, $saved[$key], 'Process') }
    }
    $javaAfter = @(Get-CimInstance Win32_Process -Filter "Name='java.exe'" | ForEach-Object ProcessId)
    $newJava = @($javaAfter | Where-Object { $_ -notin $javaBefore }).Count
    $displayed = @('ENV=', 'DB_HOST=', 'DB_PORT=', 'DB_NAME=' | Where-Object { $output -match "(?m)^$([regex]::Escape($_))" })
    [pscustomobject]@{
        Name = $name; ExitCode = $exit; Refused = $output.Contains($refusal); ReachedJavaStart = $output.Contains('MUTANT_REACHED_JAVA_START')
        DisplayLines = ($displayed -join ','); NewJavaProcesses = $newJava
        FirstError = (($output -split "`r?`n" | Where-Object { $_ -match 'refused|MUTANT_REACHED|already in use|binding|expected|No runtime jar' } | Select-Object -First 1) -replace '^\s+', '')
    }
}

if ($Phase -eq 'Mutants') {
    $results = @(
        Invoke-Mutant 'M1_PORT_3308' (New-Mutant 'M1_PORT_3308' '$dbPort = 3310' '$dbPort = 3308')
        Invoke-Mutant 'M2_HOST_GYPPORT_MYSQL_DEV' (New-Mutant 'M2_HOST_GYPPORT_MYSQL_DEV' "`$dbHost = '127.0.0.1'" "`$dbHost = 'gypport-mysql-dev'")
        Invoke-Mutant 'M3_DATABASE_CORE_BUSINESS_DEV' (New-Mutant 'M3_DATABASE_CORE_BUSINESS_DEV' "`$dbName = 'gypport_runtime_local'" "`$dbName = 'core_business_dev'")
        Invoke-Mutant 'M4_URL_LOCALHOST_3308' (New-Mutant 'M4_URL_LOCALHOST_3308' '$url = "jdbc:mysql://${dbHost}:${dbPort}/${dbName}?allowPublicKeyRetrieval=true&useSSL=false"' '$url = "jdbc:mysql://localhost:3308/core_business_dev?allowPublicKeyRetrieval=true&useSSL=false"')
        Invoke-Mutant 'M5_JAVA_TOOL_OPTIONS_SHARED_DEV' (New-Mutant 'M5_JAVA_TOOL_OPTIONS_SHARED_DEV' '' '') @{ JAVA_TOOL_OPTIONS = '-Dspring.datasource.url=jdbc:mysql://127.0.0.1:3308/core_business_dev' }
    )
    $results | Format-Table -AutoSize | Out-String -Width 400
    $ok = @($results | Where-Object { $_.ExitCode -ne 0 -and $_.Refused -and -not $_.ReachedJavaStart -and -not $_.DisplayLines -and $_.NewJavaProcesses -eq 0 }).Count
    "GUARD_MUTANTS_REFUSED=$ok/$($results.Count)"
} else {
    # Control: the unmodified guard with the real configuration passes every check and displays only the four lines.
    $result = Invoke-Mutant 'CONTROL_REAL_CONFIGURATION' (New-Mutant 'CONTROL_REAL_CONFIGURATION' '' '')
    $result | Format-List | Out-String -Width 400
    $control = Join-Path $workDir 'CONTROL_REAL_CONFIGURATION.ps1'
    $previous = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    $lines = (& powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $control -Jar $jar 2>&1 | Out-String) -split "`r?`n" | Where-Object { $_ -match '^[A-Z_]+=' }
    $ErrorActionPreference = $previous
    "CONTROL_OUTPUT_BEFORE_JAVA=[$($lines -join ' | ')]"
    "CONTROL_OK=$($result.ReachedJavaStart -and -not $result.Refused -and $result.DisplayLines -eq 'ENV=,DB_HOST=,DB_PORT=,DB_NAME=' -and $result.NewJavaProcesses -eq 0)"
}

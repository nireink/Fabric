<#
.SYNOPSIS
    Starts the working-tree Host on 127.0.0.1:8080 against the isolated runtime database (127.0.0.1:3310).
.DESCRIPTION
    GYPPORT_LOCAL_RUNTIME_ALIGNMENT_FIX_01, hardened by GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13.
    Local, disposable runtime only - never Shared DEV (port 3308, container gypport-mysql-dev, database core_business_dev).
    - The configuration is explicit and process-local (ENV, DB_HOST, DB_PORT, DB_NAME below). No Windows User or Machine
      environment variable supplies the datasource; inherited SPRING_* variables are removed from this process.
    - The database password is read from the gypport-runtime-local-mysql container at launch; nothing secret is stored in
      this file or printed. Before Java starts, only ENV, DB_HOST, DB_PORT and DB_NAME are displayed.
    - Mandatory guard: a resolved datasource that points to Shared DEV refuses startup with
      "Local runtime refused to start because the datasource points to Shared DEV."
    Windows PowerShell 5.1 compatible. Build output lives in ../ (target/), which `mvn clean` deletes:
    stop this backend before cleaning.
#>
[CmdletBinding()]
param(
    [string]$Jar = ''
)

$ErrorActionPreference = 'Stop'
$runtimeDir = $PSScriptRoot

# Explicit, process-local configuration of the local runtime.
$envName = 'LOCAL_EDUARDO'
$dbHost = '127.0.0.1'
$dbPort = 3310
$dbName = 'gypport_runtime_local'
$dbUser = 'gypport_runtime_local'
$runtimeContainer = 'gypport-runtime-local-mysql'
$url = "jdbc:mysql://${dbHost}:${dbPort}/${dbName}?allowPublicKeyRetrieval=true&useSSL=false"

# Mandatory Shared DEV guard (port 3308, container gypport-mysql-dev, database core_business_dev).
$sharedDevRefusal = 'Local runtime refused to start because the datasource points to Shared DEV.'
function Assert-NotSharedDev([string[]]$Values) {
    foreach ($value in $Values) {
        if ([string]::IsNullOrEmpty($value)) { continue }
        if ($value -match ':3308(\D|$)' -or $value -match '(?i)gypport-mysql-dev' -or $value -match '(?i)core_business_dev') {
            throw $sharedDevRefusal
        }
    }
}
if ($dbPort -eq 3308) { throw $sharedDevRefusal }
Assert-NotSharedDev @($url, "${dbHost}:${dbPort}", $dbHost, $dbName, $dbUser, $runtimeContainer)
# JVM option variables are not removed by name, so they must not carry a Shared DEV datasource either.
Assert-NotSharedDev @($env:JAVA_TOOL_OPTIONS, $env:JDK_JAVA_OPTIONS, $env:_JAVA_OPTIONS)
if ($url -notmatch '^jdbc:mysql://127\.0\.0\.1:3310/gypport_runtime_local\?') {
    throw "Local runtime refused to start: datasource '$url' is not the isolated runtime database."
}

if (-not $Jar) {
    $Jar = (Get-ChildItem -LiteralPath (Join-Path $runtimeDir 'app') -Filter 'gystigo-host-runtime-*.jar' |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
}
if (-not $Jar -or -not (Test-Path -LiteralPath $Jar)) { throw 'No runtime jar found under app/.' }

# The isolated database must be the published runtime container, hosting the runtime database - never Shared DEV.
$binding = [string](docker port $runtimeContainer 3306/tcp)
if ($LASTEXITCODE -ne 0 -or $binding.Trim() -ne "${dbHost}:${dbPort}") { throw "Runtime MySQL binding is '$binding', expected ${dbHost}:${dbPort}." }
$previousPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue' # Windows PowerShell 5.1 turns redirected native stderr into errors.
try { $sharedDevBinding = [string](docker port gypport-mysql-dev 3306/tcp 2>$null) } finally { $ErrorActionPreference = $previousPreference }
if ($sharedDevBinding.Trim() -eq "${dbHost}:${dbPort}") { throw $sharedDevRefusal }
$envList = (docker inspect $runtimeContainer | ConvertFrom-Json)[0].Config.Env
$databaseEntry = $envList | Where-Object { $_ -like 'MYSQL_DATABASE=*' } | Select-Object -First 1
$containerDatabase = if ($databaseEntry) { $databaseEntry.Substring('MYSQL_DATABASE='.Length) } else { '' }
Assert-NotSharedDev @($containerDatabase)
if ($containerDatabase -ne $dbName) { throw "Runtime MySQL database is '$containerDatabase', expected $dbName." }
$passwordEntry = $envList | Where-Object { $_ -like 'MYSQL_PASSWORD=*' } | Select-Object -First 1
if (-not $passwordEntry) { throw 'Runtime MySQL password not found in its container configuration.' }
$dbPassword = $passwordEntry.Substring('MYSQL_PASSWORD='.Length)

if (Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue) { throw 'Port 8080 is already in use.' }

# Nothing inherited may point this process at Shared DEV.
foreach ($name in @(Get-ChildItem Env: | Where-Object { $_.Name -like 'SPRING_*' } | ForEach-Object Name)) {
    Remove-Item -LiteralPath "Env:$name"
}
$env:SPRING_DATASOURCE_URL = $url
$env:SPRING_DATASOURCE_USERNAME = $dbUser
$env:SPRING_DATASOURCE_PASSWORD = $dbPassword
$env:SPRING_FLYWAY_ENABLED = 'true'

$java = Join-Path $env:JAVA_HOME 'bin\java.exe'
if (-not (Test-Path -LiteralPath $java)) { $java = 'C:\Program Files\Java\jdk-25.0.4\bin\java.exe' }
$stamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
$documents = Join-Path $runtimeDir 'documents\expense-documents'
$accessLogs = Join-Path $runtimeDir 'access-logs'
$arguments = @(
    '-Duser.timezone=UTC', '-Dfile.encoding=UTF-8',
    '-jar', "`"$Jar`"",
    '--server.address=127.0.0.1', '--server.port=8080',
    "`"--spring.datasource.url=$url`"", "--spring.datasource.username=$dbUser",
    '--spring.flyway.enabled=true',
    '--gypport.email.delivery.mode=smtp', '--gypport.email.smtp.host=127.0.0.1', '--gypport.email.smtp.port=1026',
    "`"--gypport.expenses.document-storage-path=$documents`"",
    '--server.tomcat.accesslog.enabled=true', "`"--server.tomcat.accesslog.directory=$accessLogs`"",
    '--server.tomcat.accesslog.pattern=common'
)
# Last look at exactly what Java receives (the password travels only in this process's environment).
Assert-NotSharedDev (@($env:SPRING_DATASOURCE_URL, $env:SPRING_DATASOURCE_USERNAME) + $arguments)

Write-Output "ENV=$envName"
Write-Output "DB_HOST=$dbHost"
Write-Output "DB_PORT=$dbPort"
Write-Output "DB_NAME=$dbName"

$process = Start-Process -FilePath $java -ArgumentList $arguments -WorkingDirectory $runtimeDir -NoNewWindow -PassThru `
    -RedirectStandardOutput (Join-Path $runtimeDir "logs\backend-$stamp.out.log") `
    -RedirectStandardError (Join-Path $runtimeDir "logs\backend-$stamp.err.log")
Set-Content -LiteralPath (Join-Path $runtimeDir 'backend.pid') -Value $process.Id -Encoding ascii
Write-Output "BACKEND_PID=$($process.Id)"
Write-Output "BACKEND_LOG=$(Join-Path $runtimeDir "logs\backend-$stamp.out.log")"
Write-Output "RUNTIME_JAR=$(Split-Path -Leaf $Jar)"

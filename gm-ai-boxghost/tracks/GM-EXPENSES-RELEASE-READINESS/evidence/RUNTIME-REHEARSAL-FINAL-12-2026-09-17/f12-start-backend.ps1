# GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 - the freshly packaged working-tree Host against the disposable Shared DEV copy
# (127.0.0.1:3314/gypport_rehearsal_final12), served on 127.0.0.1:18084. Never 3308 (Shared DEV), never 3310 (Owner runtime copy).
# It connects as the copy's root, exactly as the official DEV backend connects to Shared DEV (root, default server flags).
$ErrorActionPreference = 'Stop'
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\6bd391c2-9dd7-4c98-8f41-546e5a9baea1\scratchpad'
$work = Join-Path $scratch 'f12-backend'
New-Item -ItemType Directory -Force -Path (Join-Path $work 'documents'), (Join-Path $work 'access-logs') | Out-Null
$status = Join-Path $work 'start-status.txt'
Set-Content -LiteralPath $status -Value 'STARTING' -Encoding ascii
try {
    $name = (Get-Content -LiteralPath "$scratch\f12-container-name.txt").Trim()
    if ($name -notlike 'gypport-rehearsal-final12-*') { throw 'Not the rehearsal container.' }
    $jar = 'D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo\platform_os\server\target\gystigo-host-runtime-0.1.0-SNAPSHOT.jar'
    if (-not (Get-FileHash -Algorithm SHA256 -LiteralPath $jar).Hash.StartsWith('F4A5509405EA')) { throw 'Unexpected Host jar.' }
    $binding = [string](docker port $name 3306/tcp)
    if ($binding.Trim() -ne '127.0.0.1:3314') { throw "Rehearsal binding is '$binding', expected 127.0.0.1:3314." }
    $envList = (docker inspect $name | ConvertFrom-Json)[0].Config.Env
    $rootPassword = ($envList | Where-Object { $_ -like 'MYSQL_ROOT_PASSWORD=*' } | Select-Object -First 1).Substring('MYSQL_ROOT_PASSWORD='.Length)
    $url = 'jdbc:mysql://127.0.0.1:3314/gypport_rehearsal_final12?allowPublicKeyRetrieval=true&useSSL=false'
    if ($url -match ':3308|:3310|core_business_dev') { throw "STOP: '$url' is not the disposable rehearsal copy." }
    if (Get-NetTCPConnection -LocalPort 18084 -State Listen -ErrorAction SilentlyContinue) { throw 'Port 18084 is already in use.' }
    foreach ($variable in @(Get-ChildItem Env: | Where-Object { $_.Name -like 'SPRING_*' } | ForEach-Object Name)) {
        [Environment]::SetEnvironmentVariable($variable, $null, 'Process')
    }
    [Environment]::SetEnvironmentVariable('SPRING_DATASOURCE_URL', $url, 'Process')
    [Environment]::SetEnvironmentVariable('SPRING_DATASOURCE_USERNAME', 'root', 'Process')
    [Environment]::SetEnvironmentVariable('SPRING_DATASOURCE_PASSWORD', $rootPassword, 'Process')
    [Environment]::SetEnvironmentVariable('SPRING_FLYWAY_ENABLED', 'true', 'Process')
    $java = if ($env:JAVA_HOME) { Join-Path $env:JAVA_HOME 'bin\java.exe' } else { '' }
    if (-not $java -or -not (Test-Path -LiteralPath $java)) { $java = 'C:\Program Files\Java\jdk-25.0.4\bin\java.exe' }
    $arguments = @('-Duser.timezone=UTC', '-Dfile.encoding=UTF-8', '-jar', "`"$jar`"",
        '--server.address=127.0.0.1', '--server.port=18084',
        "`"--spring.datasource.url=$url`"", '--spring.datasource.username=root', '--spring.flyway.enabled=true',
        '--gypport.email.delivery.mode=smtp', '--gypport.email.smtp.host=127.0.0.1', '--gypport.email.smtp.port=1026',
        "`"--gypport.expenses.document-storage-path=$work\documents`"",
        '--server.tomcat.accesslog.enabled=true', "`"--server.tomcat.accesslog.directory=$work\access-logs`"",
        '--server.tomcat.accesslog.pattern=common')
    $process = Start-Process -FilePath $java -ArgumentList $arguments -WorkingDirectory $work -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput "$work\backend.out.log" -RedirectStandardError "$work\backend.err.log"
    Set-Content -LiteralPath "$work\backend.pid" -Value $process.Id -Encoding ascii
    Set-Content -LiteralPath $status -Value "STARTED PID=$($process.Id)" -Encoding ascii
}
catch {
    Set-Content -LiteralPath $status -Value ("FAILED " + $_.Exception.Message) -Encoding ascii
}

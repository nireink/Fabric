# GM_EXPENSES_RUNTIME_REHEARSAL_03 - the freshly packaged working-tree Host against the disposable Shared DEV copy
# (127.0.0.1:3312/gypport_rehearsal03), served on 127.0.0.1:18082. Never 3308 (Shared DEV), never 3310 (runtime copy).
$ErrorActionPreference = 'Stop'
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\4bbfc1ff-e737-4ade-bbb8-169c21a07560\scratchpad'
$name = (Get-Content "$scratch\r03-container-name.txt").Trim()
if ($name -notlike 'gypport-rehearsal03-*') { throw 'Not the rehearsal container.' }
$jar = 'D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo\platform_os\server\target\gystigo-host-runtime-0.1.0-SNAPSHOT.jar'
if (-not (Get-FileHash -Algorithm SHA256 -LiteralPath $jar).Hash.StartsWith('CC028B886C4D')) { throw 'Unexpected Host jar.' }
$binding = [string](docker port $name 3306/tcp)
if ($binding.Trim() -ne '127.0.0.1:3312') { throw "Rehearsal binding is '$binding', expected 127.0.0.1:3312." }
$envList = (docker inspect $name | ConvertFrom-Json)[0].Config.Env
$dbPassword = ($envList | Where-Object { $_ -like 'MYSQL_PASSWORD=*' } | Select-Object -First 1).Substring('MYSQL_PASSWORD='.Length)
$url = 'jdbc:mysql://127.0.0.1:3312/gypport_rehearsal03?allowPublicKeyRetrieval=true&useSSL=false'
if ($url -match ':3308|:3310|core_business_dev') { throw "STOP: '$url' is not the disposable rehearsal copy." }
if (Get-NetTCPConnection -LocalPort 18082 -State Listen -ErrorAction SilentlyContinue) { throw 'Port 18082 is already in use.' }
foreach ($variable in @(Get-ChildItem Env: | Where-Object { $_.Name -like 'SPRING_*' } | ForEach-Object Name)) { Remove-Item -LiteralPath "Env:$variable" }
$env:SPRING_DATASOURCE_URL = $url
$env:SPRING_DATASOURCE_USERNAME = 'gypport_rehearsal'
$env:SPRING_DATASOURCE_PASSWORD = $dbPassword
$env:SPRING_FLYWAY_ENABLED = 'true'
$work = Join-Path $scratch 'r03-backend'
New-Item -ItemType Directory -Force -Path (Join-Path $work 'documents'), (Join-Path $work 'access-logs') | Out-Null
$java = Join-Path $env:JAVA_HOME 'bin\java.exe'
if (-not (Test-Path -LiteralPath $java)) { $java = 'C:\Program Files\Java\jdk-25.0.4\bin\java.exe' }
$arguments = @('-Duser.timezone=UTC', '-Dfile.encoding=UTF-8', '-jar', "`"$jar`"",
    '--server.address=127.0.0.1', '--server.port=18082',
    "`"--spring.datasource.url=$url`"", '--spring.datasource.username=gypport_rehearsal', '--spring.flyway.enabled=true',
    '--gypport.email.delivery.mode=smtp', '--gypport.email.smtp.host=127.0.0.1', '--gypport.email.smtp.port=1026',
    "`"--gypport.expenses.document-storage-path=$work\documents`"",
    '--server.tomcat.accesslog.enabled=true', "`"--server.tomcat.accesslog.directory=$work\access-logs`"",
    '--server.tomcat.accesslog.pattern=common')
$started = Get-Date
$process = Start-Process -FilePath $java -ArgumentList $arguments -WorkingDirectory $work -NoNewWindow -PassThru `
    -RedirectStandardOutput "$work\backend.out.log" -RedirectStandardError "$work\backend.err.log"
Set-Content -LiteralPath "$work\backend.pid" -Value $process.Id -Encoding ascii
"REHEARSAL_BACKEND_PID=$($process.Id)"
for ($i = 0; $i -lt 120; $i++) {
    if (Get-NetTCPConnection -LocalPort 18082 -State Listen -ErrorAction SilentlyContinue) { "LISTENING_AFTER=$([int]((Get-Date) - $started).TotalSeconds)s"; break }
    if ($process.HasExited) { "BACKEND_EXITED=$($process.ExitCode)"; break }
    Start-Sleep -Seconds 2
}
Select-String -Path "$work\backend.out.log" -Pattern 'Current version of schema|Migrating schema|Successfully applied|Started ServerApplication|APPLICATION FAILED|FlywayValidateException|SQLException' |
    ForEach-Object { $_.Line.Substring([Math]::Min(60, [Math]::Max(0, $_.Line.Length - 1))) }

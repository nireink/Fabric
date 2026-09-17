# GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13 - what a plain, freshly created process inherits.
# Launched through WMI (Win32_Process.Create), so its environment is built from the registry (Machine + User), not from
# any running shell. Writes PRESENT/ABSENT only; never a username or password value.
param([Parameter(Mandatory = $true)][string]$Out)
$lines = @("PROBE_UTC=$((Get-Date).ToUniversalTime().ToString('o'))", "PROBE_PID=$PID", "PROBE_PARENT=WMI")
foreach ($name in 'SPRING_DATASOURCE_URL', 'SPRING_DATASOURCE_USERNAME', 'SPRING_DATASOURCE_PASSWORD', 'SPRING_APPLICATION_JSON',
    'JAVA_TOOL_OPTIONS', 'JDK_JAVA_OPTIONS', '_JAVA_OPTIONS') {
    $value = [Environment]::GetEnvironmentVariable($name, 'Process')
    $lines += "$name=$(if ($value) { 'PRESENT' } else { 'ABSENT' })"
}
$url = [Environment]::GetEnvironmentVariable('SPRING_DATASOURCE_URL', 'Process')
$lines += "PLAIN_SHELL_INHERITS_SHARED_DEV=$(if ($url -match ':3308|core_business_dev|gypport-mysql-dev') { 'YES' } else { 'NO' })"
Set-Content -LiteralPath $Out -Value $lines -Encoding ascii

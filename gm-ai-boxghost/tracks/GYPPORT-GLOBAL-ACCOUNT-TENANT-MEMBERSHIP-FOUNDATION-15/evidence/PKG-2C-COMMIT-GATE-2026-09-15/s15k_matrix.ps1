# STEP 15 PKG-2C FINAL coherent matrix (Owner OPTION_A resume, 2026-09-15): the entries of s15j_matrix.ps1, run
# from entry 1 to entry 39, with a quick drift check after every entry (first change = stop).
# Origin, s15j_matrix.ps1 -- STEP 15 PKG-2C full disposable runtime matrix: the 34 entries of the PKG-2B matrix plus the five PKG-2C suites
# (contextual Party read, V57, V57 STOP, V58, V58 global actor), now at the V58 schema. Disposable
# MySQL/Mailpit containers only (canonical runner); never the shared DEV database or inbox.
param([string[]]$Only = @(), [string]$Tag = 'matrix')
$ErrorActionPreference = 'Continue'
# powershell.exe -File passes "a,b" as one string; accept comma-separated lists either way.
$Only = @($Only | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\8142c294-1815-45b4-90ee-94d1198faa7d\scratchpad'
$gystigo = 'D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo'
$platform = Join-Path $gystigo 'platform_os'
$runner = Join-Path $platform 'server\scripts\run-host-isolated-db-tests.ps1'
$summary = Join-Path $scratch ('s15k_' + $Tag + '_summary.txt')
Set-Content -LiteralPath $summary -Value ('START=' + (Get-Date -Format o)) -Encoding utf8

function Wait-PortFree([int]$Port) {
    for ($i = 0; $i -lt 180; $i++) {
        if (-not (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue)) { return $true }
        Start-Sleep -Seconds 10
    }
    return $false
}

function Add-Result([string]$Name, [int]$Code, [string]$Log) {
    $line = '{0}={1}' -f $Name, $Code
    $hit = Select-String -LiteralPath $Log -Pattern 'HOST_ISOLATED_DB_RESULT=(.+)$' | Select-Object -Last 1
    if ($hit -and (Test-Path -LiteralPath $hit.Matches[0].Groups[1].Value.Trim())) {
        $j = Get-Content -LiteralPath $hit.Matches[0].Groups[1].Value.Trim() -Raw | ConvertFrom-Json
        $line += ' tests={0} failures={1} errors={2} skipped={3} flyway={4} db={5} port={6} disposed={7} mailpitDisposed={8}' -f `
            $j.testsRun, $j.failures, $j.errors, $j.skipped, $j.flywayMax, $j.database, $j.port, $j.containerDisposed, $j.mailpitDisposed
    } else {
        $totals = Select-String -LiteralPath $Log -Pattern 'Tests run: [0-9]+, Failures: [0-9]+, Errors: [0-9]+, Skipped: [0-9]+$' | Select-Object -Last 1
        if ($totals) { $line += ' ' + $totals.Line.Trim() }
    }
    Add-Content -LiteralPath $summary -Value $line
}

Set-Location -LiteralPath $gystigo
$groupATests = 'GmEntitiesHostIntegrationTest,CorsConfigurationSecurityTest,OnboardingHostIntegrationTest,' +
    'GmHumanResourcesRealDatabaseAcceptanceTest,GystigoAuthenticatedTenantBoundaryHttpTest,MyProfileHostIntegrationTest,' +
    'MailpitEmailVerificationAcceptanceTest,MailpitPasswordRecoveryAcceptanceTest'
$groupAFlags = 'GYPPORT_E2_REAL_DB_TESTS,GYPPORT_CORS_REAL_DB_TESTS,GYPPORT_ONBOARDING_REAL_DB_TESTS,' +
    'GYPPORT_GM_HUMAN_RESOURCES_REAL_DB_TESTS,GYPPORT_AUTH_BOUNDARY_REAL_DB_TESTS,GYPPORT_PROFILE_REAL_DB_TESTS,' +
    'GYPPORT_MAILPIT_REAL_SMTP_TESTS'
$fuelTests = 'GmFuelStationsHttpApiTest,GmFuelStationsTransportTankConcurrencyHttpApiTest,' +
    'GmFuelStationsDischargeMeterHttpApiTest,GmFuelStationsDischargeMeterConcurrencyHttpApiTest'
$membership = 'GYPPORT_TENANT_MEMBERSHIP_REAL_DB_TESTS'
$runs = @(
    @{ Name = 'm_contextual_party'; Args = @('-Tests', 'ContextualPartyReadRealDatabaseAcceptanceTest',
        '-Database', 'gypport_contextual_party_read_test', '-EnableFlags', $membership) },
    @{ Name = 'm_v57'; Args = @('-Tests', 'TenantAccessSubjectMembershipFkMigrationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_access_subject_fk_migration_test', '-EnableFlags', $membership) },
    @{ Name = 'm_v57_stop'; Args = @('-Tests', 'TenantAccessSubjectMembershipFkMigrationStopRealDatabaseAcceptanceTest',
        '-Database', 'gypport_access_subject_fk_stop_test', '-EnableFlags', $membership) },
    @{ Name = 'm_v58'; Args = @('-Tests', 'GlobalUserAccountActorFkMigrationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_global_actor_fk_migration_test', '-EnableFlags', $membership) },
    @{ Name = 'm_v58_actor'; Args = @('-Tests', 'GlobalUserAccountActorRealDatabaseAcceptanceTest',
        '-Database', 'gypport_global_actor_test', '-EnableFlags', $membership) },
    @{ Name = 'm_context_all'; Args = @('-Tests', '*', '-Database', 'gypport_host_context_test') },
    @{ Name = 'm_group_a'; Args = @('-WithMailpit', '-Tests', $groupATests, '-Database', 'gypport_host_test', '-EnableFlags', $groupAFlags) },
    @{ Name = 'm_pending_acceptance'; Args = @('-Tests', 'PendingAccountIdentityRealDatabaseAcceptanceTest',
        '-Database', 'gypport_pending_account_acceptance', '-EnableFlags', 'GYPPORT_PENDING_ACCOUNT_IDENTITY_REAL_DB_TESTS') },
    @{ Name = 'm_pending_migration'; Args = @('-Tests', 'PendingAccountIdentityMigrationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_pending_account_migration_test', '-EnableFlags', 'GYPPORT_PENDING_ACCOUNT_IDENTITY_REAL_DB_TESTS') },
    @{ Name = 'm_pending_migration_stop'; Args = @('-Tests', 'PendingAccountIdentityMigrationStopRealDatabaseAcceptanceTest',
        '-Database', 'gypport_pending_account_stop_test', '-EnableFlags', 'GYPPORT_PENDING_ACCOUNT_IDENTITY_REAL_DB_TESTS') },
    @{ Name = 'm_membership_v53_v54'; Args = @('-Tests', 'UserTenantMembershipMigrationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tenant_membership_migration_test', '-EnableFlags', $membership) },
    @{ Name = 'm_membership_v53_stop'; Args = @('-Tests', 'UserTenantMembershipMigrationStopRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tenant_membership_stop_test', '-EnableFlags', $membership) },
    @{ Name = 'm_membership_v54_stop'; Args = @('-Tests', 'OneActiveAccountPerGoldenRecordMigrationStopRealDatabaseAcceptanceTest',
        '-Database', 'gypport_one_account_stop_test', '-EnableFlags', $membership) },
    @{ Name = 'm_membership_v55'; Args = @('-Tests', 'UserTenantMembershipCatchUpMigrationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tenant_membership_catch_up_test', '-EnableFlags', $membership) },
    @{ Name = 'm_membership_v55_stop'; Args = @('-Tests', 'UserTenantMembershipCatchUpMigrationStopRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tenant_membership_catch_up_stop_test', '-EnableFlags', $membership) },
    @{ Name = 'm_membership_runtime'; Args = @('-Tests', 'UserTenantMembershipRuntimeWriterRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tenant_membership_runtime_test', '-EnableFlags', $membership) },
    @{ Name = 'm_membership_v56'; Args = @('-Tests', 'TenantlessPlatformSessionMigrationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tenantless_session_migration_test', '-EnableFlags', $membership) },
    @{ Name = 'm_signin_gate'; Args = @('-Tests', 'SignInMembershipGateRealDatabaseAcceptanceTest',
        '-Database', 'gypport_signin_membership_gate_test', '-EnableFlags', $membership) },
    @{ Name = 'm_platform_session'; Args = @('-Tests', 'PlatformSessionRealDatabaseAcceptanceTest',
        '-Database', 'gypport_platform_session_test', '-EnableFlags', $membership) },
    @{ Name = 'm_route_boundary'; Args = @('-Tests', 'SessionRouteBoundaryRealDatabaseAcceptanceTest',
        '-Database', 'gypport_session_route_boundary_test', '-EnableFlags', $membership) },
    @{ Name = 'm_team_access'; Args = @('-WithMailpit', '-Tests', 'EmployeeAccessGrantRealDatabaseAcceptanceTest',
        '-Database', 'gypport_team_access_acceptance', '-PortVariables', 'GYPPORT_GM_TEAM_ACCESS_TEST_DB_PORT',
        '-EnableFlags', 'GYPPORT_GM_TEAM_ACCESS_REAL_DB_TESTS') },
    @{ Name = 'm_team'; Args = @('-Tests', 'TeamEmployeeRealDatabaseAcceptanceTest', '-Database', 'gypport_team_acceptance',
        '-PortVariables', 'GYPPORT_GM_TEAM_TEST_DB_PORT', '-EnableFlags', 'GYPPORT_GM_TEAM_REAL_DB_TESTS') },
    @{ Name = 'm_team_employment'; Args = @('-Tests', 'EmployeeEmploymentUpdateRealDatabaseAcceptanceTest',
        '-Database', 'gypport_team_employment_acceptance', '-PortVariables', 'GYPPORT_GM_TEAM_EMPLOYMENT_TEST_DB_PORT',
        '-EnableFlags', 'GYPPORT_GM_TEAM_EMPLOYMENT_REAL_DB_TESTS') },
    @{ Name = 'm_team_revocation'; Args = @('-Tests', 'EmployeeAccessRevocationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_team_revocation_acceptance', '-PortVariables', 'GYPPORT_GM_TEAM_REVOCATION_TEST_DB_PORT',
        '-EnableFlags', 'GYPPORT_GM_TEAM_REVOCATION_REAL_DB_TESTS') },
    @{ Name = 'm_rbac_scope'; Args = @('-Tests', 'TeamEmployeeControllerScopeBoundaryRealDatabaseAcceptanceTest',
        '-Database', 'gypport_rbac_scope_boundary_acceptance', '-PortVariables', 'GYPPORT_RBAC_SCOPE_BOUNDARY_TEST_DB_PORT',
        '-EnableFlags', 'GYPPORT_RBAC_SCOPE_BOUNDARY_REAL_DB_TESTS') },
    @{ Name = 'm_organization_rbac'; Args = @('-Tests', 'OrganizationRoleAdministrationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_organization_rbac_acceptance', '-PortVariables', 'GYPPORT_ORGANIZATION_RBAC_TEST_DB_PORT',
        '-EnableFlags', 'GYPPORT_ORGANIZATION_RBAC_REAL_DB_TESTS') },
    @{ Name = 'm_organization_control'; Args = @('-Tests', 'OrganizationControlActivationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_organization_control_acceptance', '-PortVariables', 'GYPPORT_ORGANIZATION_CONTROL_TEST_DB_PORT',
        '-EnableFlags', 'GYPPORT_ORGANIZATION_CONTROL_REAL_DB_TESTS') },
    @{ Name = 'm_gm_organizations'; Args = @('-Tests', 'GmOrganizationsRealDatabaseAcceptanceTest',
        '-Database', 'gypport_organization_acceptance', '-PortVariables', 'GYPPORT_GM_ORGANIZATIONS_TEST_DB_PORT',
        '-EnableFlags', 'GYPPORT_GM_ORGANIZATIONS_REAL_DB_TESTS') },
    @{ Name = 'm_platform_admin'; Args = @('-Tests', 'PlatformAdminRealDatabaseAcceptanceTest',
        '-Database', 'gypport_platform_admin_acceptance', '-PortVariables', 'GYPPORT_PLATFORM_ADMIN_TEST_DB_PORT',
        '-EnableFlags', 'GYPPORT_PLATFORM_ADMIN_REAL_DB_TESTS') },
    @{ Name = 'm_tenant_safe_fk'; Args = @('-Tests', 'TenantSafeReferenceIntegrityRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tenant_safe_fk_test', '-EnableFlags', 'GYPPORT_TENANT_SAFE_FK_REAL_DB_TESTS') },
    @{ Name = 'm_tenant_safe_stop'; Args = @('-Tests', 'TenantSafeProductScopeMigrationStopRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tenant_safe_stop_test', '-EnableFlags', 'GYPPORT_TENANT_SAFE_FK_REAL_DB_TESTS') },
    @{ Name = 'm_tax_subject'; Args = @('-Tests', 'TaxSubjectFoundationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_tax_subject_test', '-EnableFlags', 'GYPPORT_TAX_SUBJECT_REAL_DB_TESTS') },
    @{ Name = 'm_establishment_stop'; Args = @('-Tests', 'UserEstablishmentAccessMigrationStopRealDatabaseAcceptanceTest',
        '-Database', 'gypport_establishment_stop_test', '-EnableFlags', 'GYPPORT_TAX_SUBJECT_REAL_DB_TESTS') },
    @{ Name = 'm_collation'; Args = @('-Tests', 'IdentityCollationReconciliationRealDatabaseAcceptanceTest',
        '-Database', 'gypport_identity_collation_test', '-EnableFlags', 'GYPPORT_IDENTITY_COLLATION_REAL_DB_TESTS') },
    @{ Name = 'm_collation_stop'; Args = @('-Tests', 'IdentityCollationMigrationStopRealDatabaseAcceptanceTest',
        '-Database', 'gypport_identity_collation_stop_test', '-EnableFlags', 'GYPPORT_IDENTITY_COLLATION_REAL_DB_TESTS') },
    @{ Name = 'm_identity_intake'; Args = @('-Tests', 'UniversalIdentityIntakeRealDatabaseAcceptanceTest',
        '-Database', 'gypport_identity_intake_test', '-EnableFlags', 'GYPPORT_IDENTITY_INTAKE_REAL_DB_TESTS') },
    @{ Name = 'm_identity_reconciliation'; Port = 3310; Args = @('-Tests', 'PersonIdentityReconciliationHttpTest',
        '-Database', 'core_business_fleets_test', '-HostPort', '3310', '-EnableFlags', 'GYPPORT_IDENTITY_REAL_DB_TESTS') },
    @{ Name = 'm_fleets'; Port = 3310; Args = @('-Tests', 'GmFleetsHttpApiTest', '-Database', 'core_business_fleets_test',
        '-HostPort', '3310', '-EnableFlags', 'GYPPORT_FLEETS_REAL_DB_TESTS') },
    @{ Name = 'm_fuel_stations'; Port = 3311; Args = @('-Tests', $fuelTests, '-Database', 'core_business_fuel_stations_test',
        '-HostPort', '3311', '-EnableFlags', 'GYPPORT_FUEL_STATIONS_REAL_DB_TESTS') })
# Quick drift detector: any change of any uncommitted file (status, size or last-write time) in any GYPPORT repository.
$workspace = Split-Path -Parent $gystigo
$quickRepos = @($gystigo, (Join-Path $workspace 'Fabric')) + @(Get-ChildItem -Directory -LiteralPath (Join-Path $workspace 'Modules') |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName '.git') } | ForEach-Object { $_.FullName })
function Get-QuickState {
    $text = New-Object System.Text.StringBuilder
    foreach ($repo in $quickRepos) {
        foreach ($line in @(& git -C $repo status --porcelain -uall 2>$null | Where-Object { $_ })) {
            [void]$text.Append($repo).Append('|').Append($line)
            $full = Join-Path $repo ($line.Substring(3).Trim('"'))
            if (Test-Path -LiteralPath $full -PathType Leaf) {
                $item = Get-Item -LiteralPath $full
                [void]$text.Append('|').Append($item.Length).Append('|').Append($item.LastWriteTimeUtc.Ticks)
            }
            [void]$text.AppendLine()
        }
    }
    $sha = [System.Security.Cryptography.SHA256]::Create()
    return [BitConverter]::ToString($sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($text.ToString()))).Replace('-', '')
}
$initialState = Get-QuickState
Add-Content -LiteralPath $summary -Value ('QUICK_STATE_START=' + $initialState)
Add-Content -LiteralPath $summary -Value ('MATRIX_ENTRIES=' + $runs.Count)
foreach ($run in $runs) {
    if ($Only.Count -gt 0 -and $Only -notcontains $run.Name) { continue }
    if ($run.Port -and -not (Wait-PortFree $run.Port)) { Add-Content -LiteralPath $summary -Value "$($run.Name)=PORT_BUSY"; continue }
    $log = Join-Path $scratch ('s15k_' + $Tag + '_' + $run.Name + '.log')
    $arguments = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $runner) + $run.Args
    & powershell.exe @arguments *> $log
    Add-Result $run.Name $LASTEXITCODE $log
    if ((Get-QuickState) -ne $initialState) {
        Add-Content -LiteralPath $summary -Value ('EXTERNAL_DRIFT_DETECTED_AFTER=' + $run.Name)
        break
    }
}

$leftovers = @(& docker ps -a --filter 'label=gypport.host.test-run' --format '{{.Names}}') +
    @(& docker ps -a --filter 'label=gypport.expenses.test-run' --format '{{.Names}}') | Where-Object { $_ }
Add-Content -LiteralPath $summary -Value ('LEFTOVER_TEST_CONTAINERS=' + @($leftovers).Count)
Add-Content -LiteralPath $summary -Value ('END=' + (Get-Date -Format o))

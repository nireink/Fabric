# STEP 15 PKG-2C controlled commit gate: post-commit verification (offline Maven; no database; no DEV).
#   -Stage modules : gm-entities and gm-security clean install with their full suites, only from a clean committed HEAD
#   -Stage host    : Host test-compile against the installed artifacts, then the PKG-2C Host unit tests
param([Parameter(Mandatory = $true)][ValidateSet('modules', 'host')][string]$Stage)
$ErrorActionPreference = 'Continue'
$root = 'D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT'
$mvnw = Join-Path $root 'Gystigo\platform_os\mvnw.cmd'
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\8142c294-1815-45b4-90ee-94d1198faa7d\scratchpad'
$summary = Join-Path $scratch ('s15k_post_commit_' + $Stage + '_summary.txt')
Set-Content -LiteralPath $summary -Value ('START=' + (Get-Date -Format o)) -Encoding utf8

function Run-Maven([string]$Name, [string[]]$Arguments) {
    $log = Join-Path $scratch ('s15k_post_commit_' + $Name + '.log')
    & $mvnw @Arguments *> $log
    $code = $LASTEXITCODE
    $tests = Select-String -LiteralPath $log -Pattern 'Tests run: [0-9]+, Failures: [0-9]+, Errors: [0-9]+, Skipped: [0-9]+$' | Select-Object -Last 1
    $build = Select-String -LiteralPath $log -Pattern '^\[INFO\] BUILD (SUCCESS|FAILURE)' | Select-Object -Last 1
    $line = '{0}={1}' -f $Name, $code
    if ($tests) { $line += ' ' + $tests.Line.Trim() }
    if ($build) { $line += ' ' + $build.Line.Trim() }
    Add-Content -LiteralPath $summary -Value $line
    return $code
}

if ($Stage -eq 'modules') {
    foreach ($module in 'gm-entities', 'gm-security') {
        $dir = Join-Path $root ('Modules\' + $module)
        $dirty = @(& git -C $dir status --porcelain -uall | Where-Object { $_ })
        $head = "$(& git -C $dir rev-parse HEAD)".Trim()
        Add-Content -LiteralPath $summary -Value ('{0}_HEAD={1} WORKTREE_DIRTY_ENTRIES={2}' -f $module, $head, $dirty.Count)
        if ($dirty.Count -ne 0) {
            Add-Content -LiteralPath $summary -Value ($module + '_INSTALL=SKIPPED_NOT_CLEAN_HEAD')
            continue
        }
        [void](Run-Maven ($module + '_install') @('-o', '-B', '-f', (Join-Path $dir 'pom.xml'), 'clean', 'install'))
    }
} else {
    $pom = Join-Path $root 'Gystigo\platform_os\server\pom.xml'
    $compile = Run-Maven 'host_test_compile' @('-o', '-B', '-f', $pom, 'test-compile')
    if ($compile -eq 0) {
        $units = 'ConfirmOrganizationControlUseCaseTest,ClaimOrganizationControlUseCaseTest,ReviewOrganizationControlUseCaseTest,' +
            'RegisterPersonAccountUseCaseTest,MyProfileServiceTest,ProfileIdentityServiceTest,EmployeeAccessGrantServiceTest,' +
            'SessionServiceTest,PlatformAdminControllerTest'
        [void](Run-Maven 'host_units' @('-o', '-B', '-f', $pom, "-Dtest=$units", '-Dsurefire.failIfNoSpecifiedTests=false', 'test'))
    }
}
Add-Content -LiteralPath $summary -Value ('END=' + (Get-Date -Format o))
Get-Content -LiteralPath $summary

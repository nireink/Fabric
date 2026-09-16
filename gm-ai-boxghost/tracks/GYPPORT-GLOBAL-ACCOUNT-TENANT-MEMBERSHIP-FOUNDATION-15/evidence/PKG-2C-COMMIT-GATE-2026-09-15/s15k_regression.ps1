# STEP 15 PKG-2C FINAL coherent regression (Owner decision OPTION_A, resume of the same STEP; evidence only, no
# implementation change). ONE stable snapshot: every uncommitted file of every GYPPORT repository is fingerprinted
# (SHA-256) first, and after every stage the fingerprint is compared with it; ANY change stops the run as
# EXTERNAL_DRIFT_DETECTED_AT_<stage>, and no reconciliation is chosen. Stages, in order:
#   0 snapshot + PKG-2C byte proof against the reviewed state (s15j_fingerprint_after_regression.txt, 52 paths)
#   1 gm-entities and gm-security clean install with their full suites, from the unchanged reviewed sources
#   2 Host test-compile
#   3 gm-expenses canonical real-DB runner
#   4 Studio contracts, then the Studio build (never concurrently); no Studio source is changed by PKG-2C
#   5 normal Host suite
#   6 the full 39-entry disposable matrix, entry 1 to entry 39 (s15k_matrix.ps1; quick drift check after every entry)
#   7 final fingerprint + PKG-2C byte proof
# Disposable MySQL/Mailpit only; never the shared DEV database or inbox. Nothing is staged, committed or pushed.
$ErrorActionPreference = 'Continue'
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\8142c294-1815-45b4-90ee-94d1198faa7d\scratchpad'
$root = 'D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT'
$gystigo = Join-Path $root 'Gystigo'
$platform = Join-Path $gystigo 'platform_os'
$mvn = Join-Path $platform 'mvnw.cmd'
$pom = Join-Path $platform 'server\pom.xml'
$entitiesPom = Join-Path $root 'Modules\gm-entities\pom.xml'
$securityPom = Join-Path $root 'Modules\gm-security\pom.xml'
$expensesRunner = Join-Path $platform 'server\scripts\run-expenses-real-db-tests.ps1'
$matrix = Join-Path $scratch 's15k_matrix.ps1'
$fingerprint = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\9df81ea4-65a4-4345-b872-06e0b99a4ebc\scratchpad\s15g_fingerprint.ps1'
$reviewed = Join-Path $scratch 's15j_fingerprint_after_regression.txt'
$pkg2cProof = Join-Path $scratch 's15k_pkg2c_hashes.py'
$snapshot = Join-Path $scratch 's15k_fingerprint_snapshot.txt'
$summary = Join-Path $scratch 's15k_regression_summary.txt'
Set-Content -LiteralPath $summary -Value ('START=' + (Get-Date -Format o)) -Encoding utf8

function Add-Line([string]$Text) { Add-Content -LiteralPath $summary -Value $Text }

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
        $build = Select-String -LiteralPath $Log -Pattern '^\[INFO\] BUILD (SUCCESS|FAILURE)' | Select-Object -Last 1
        if ($build) { $line += ' ' + $build.Line.Trim() }
    }
    Add-Line $line
}

function Stop-Run([string]$Reason) {
    Add-Line ('STOPPED=' + $Reason)
    $left = @(& docker ps -a --filter 'label=gypport.host.test-run' --format '{{.Names}}') +
        @(& docker ps -a --filter 'label=gypport.expenses.test-run' --format '{{.Names}}') | Where-Object { $_ }
    Add-Line ('LEFTOVER_TEST_CONTAINERS=' + @($left).Count)
    Add-Line ('END=' + (Get-Date -Format o))
    exit 1
}

function Invoke-Maven([string]$Name, [string[]]$MavenArgs) {
    $log = Join-Path $scratch ('s15k_r_' + $Name + '.log')
    & $mvn @MavenArgs *> $log
    $code = $LASTEXITCODE
    Add-Result $Name $code $log
    return $code
}

function Invoke-Npm([string]$Name, [string]$NpmArgs) {
    $log = Join-Path $scratch ('s15k_r_' + $Name + '.log')
    cmd /c "npm $NpmArgs > `"$log`" 2>&1"
    $code = $LASTEXITCODE
    $files = "$((Select-String -LiteralPath $log -Pattern 'Test Files\s+.+$' | Select-Object -Last 1).Line)".Trim()
    $tests = "$((Select-String -LiteralPath $log -Pattern '^\s+Tests\s+.+$' | Select-Object -Last 1).Line)".Trim()
    $built = "$((Select-String -LiteralPath $log -Pattern 'built in' | Select-Object -Last 1).Line)".Trim()
    Add-Line ('{0}={1} {2} {3} {4}' -f $Name, $code, $files, $tests, $built)
    return $code
}

function Test-Drift([string]$Stage) {
    $out = Join-Path $scratch ('s15k_fingerprint_' + $Stage + '.txt')
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fingerprint -Out $out -CompareTo $snapshot *> $null
    $line = "$((Select-String -LiteralPath $out -Pattern '^DRIFT_TOTAL=' | Select-Object -Last 1).Line)"
    Add-Line ('drift_{0}={1}' -f $Stage, $line)
    if ($line -notmatch '^DRIFT_TOTAL=0 ') {
        foreach ($d in @(Select-String -LiteralPath $out -Pattern '^DRIFT\|' | ForEach-Object { $_.Line })) { Add-Line ('  ' + $d) }
        Stop-Run ('EXTERNAL_DRIFT_DETECTED_AT_' + $Stage)
    }
}

function Test-Pkg2c([string]$Stage) {
    $out = Join-Path $scratch ('s15k_pkg2c_' + $Stage + '.txt')
    $line = "$(& python $pkg2cProof $reviewed $out | Select-Object -Last 1)"
    Add-Line ('pkg2c_{0}={1}' -f $Stage, $line)
    if ($line -notmatch 'MATCH=52 MISMATCH=0 MISSING_NOW=0 NOT_IN_BASELINE=0') { Stop-Run ('PKG2C_DRIFT_AT_' + $Stage) }
}

Set-Location -LiteralPath $gystigo

# 0. The snapshot of this run, and PKG-2C against the reviewed state.
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fingerprint -Out $snapshot *> $null
foreach ($l in @(Select-String -LiteralPath $snapshot -Pattern '^(COUNT|HEAD)\|' | ForEach-Object { $_.Line })) { Add-Line ('snapshot ' + $l) }
Test-Pkg2c 'start'

# 1. PKG-2C's own modules, rebuilt and installed from the unchanged reviewed sources (their full suites run).
$entities = Invoke-Maven 'r01_gm_entities_install' @('-o', '-B', '-f', $entitiesPom, 'clean', 'install')
$security = Invoke-Maven 'r02_gm_security_install' @('-o', '-B', '-f', $securityPom, 'clean', 'install')
if ($entities -ne 0 -or $security -ne 0) { Stop-Run 'MODULE_INSTALL_FAILED' }
Test-Drift 'modules'

# 2. Host compile against the installed artifacts (gm-expenses included, installed by its owning session).
$compile = Invoke-Maven 'r03_host_test_compile' @('-o', '-B', '-f', $pom, 'test-compile')
if ($compile -ne 0) { Stop-Run 'HOST_COMPILE_FAILED' }

# 3. gm-expenses canonical real-DB runner (its own disposable MySQL).
$log = Join-Path $scratch 's15k_r_r04_gm_expenses.log'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $expensesRunner -MavenCommand $mvn *> $log
Add-Result 'r04_gm_expenses' $LASTEXITCODE $log
Test-Drift 'expenses'

# 4. Studio contracts, then the build.
[void](Invoke-Npm 'r05_studio_contracts' 'run contracts --workspace=@gypport/platform-os-browser-shell')
[void](Invoke-Npm 'r06_studio_build' 'run build --workspace=@gypport/platform-os-browser-shell')
Test-Drift 'studio'

# 5. Normal Host suite.
[void](Invoke-Maven 'r07_host_normal' @('-o', '-B', '-f', $pom, 'test'))
Test-Drift 'host_normal'

# 6. Full disposable matrix, entry 1 to entry 39.
$log = Join-Path $scratch 's15k_r_r08_matrix_driver.log'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $matrix -Tag 'matrix' *> $log
Add-Line ('r08_matrix_driver=' + $LASTEXITCODE + ' summary=s15k_matrix_summary.txt')
$aborted = Select-String -LiteralPath (Join-Path $scratch 's15k_matrix_summary.txt') -Pattern '^EXTERNAL_DRIFT_DETECTED_AFTER=' | Select-Object -First 1
Test-Drift 'after_matrix'
if ($aborted) { Stop-Run ('EXTERNAL_DRIFT_DETECTED_DURING_MATRIX ' + $aborted.Line) }

# 7. PKG-2C still byte-identical to the reviewed state.
Test-Pkg2c 'end'
$left = @(& docker ps -a --filter 'label=gypport.host.test-run' --format '{{.Names}}') +
    @(& docker ps -a --filter 'label=gypport.expenses.test-run' --format '{{.Names}}') | Where-Object { $_ }
Add-Line ('LEFTOVER_TEST_CONTAINERS=' + @($left).Count)
Add-Line ('END=' + (Get-Date -Format o))
Get-Content -LiteralPath $summary

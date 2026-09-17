# GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 - what the freshly built working-tree jars contain.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$root = 'D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT'
$moduleJar = Join-Path $root 'Modules\gm-expenses\target\gm-expenses-0.1.0-SNAPSHOT.jar'
$m2Jar = Join-Path $env:USERPROFILE '.m2\repository\com\gypport\gm-expenses\0.1.0-SNAPSHOT\gm-expenses-0.1.0-SNAPSHOT.jar'
$hostJar = Join-Path $root 'Gystigo\platform_os\server\target\gystigo-host-runtime-0.1.0-SNAPSHOT.jar'
$rehearsal03Jar = Join-Path $root 'Gystigo\platform_os\server\target\runtime-local\app\gystigo-host-runtime-cc028b886c4d.jar'
$step11Jar = Join-Path $root 'Gystigo\platform_os\server\target\runtime-local\app\gystigo-host-runtime-ecd17c12f8af.jar'

function Sha([string]$path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash }
function Entries([string]$jar) {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($jar); $map = @{}
    foreach ($e in $zip.Entries) { $s = $e.Open(); $ms = New-Object System.IO.MemoryStream; $s.CopyTo($ms); $s.Dispose(); $map[$e.FullName] = $ms.ToArray() }
    $zip.Dispose(); return $map
}
function Contains([byte[]]$bytes, [string]$text) {
    $needle = [System.Text.Encoding]::UTF8.GetBytes($text)
    $hay = [System.Text.Encoding]::GetEncoding(28591).GetString($bytes)
    return $hay.Contains([System.Text.Encoding]::GetEncoding(28591).GetString($needle))
}
$sha256 = [System.Security.Cryptography.SHA256]::Create()
function BytesSha([byte[]]$bytes) { [BitConverter]::ToString($sha256.ComputeHash($bytes)).Replace('-', '') }

"GM_EXPENSES_JAR_SHA256=$(Sha $moduleJar)"
"GM_EXPENSES_JAR_BUILT_UTC=$((Get-Item -LiteralPath $moduleJar).LastWriteTimeUtc.ToString('o'))"
"GM_EXPENSES_M2_EQUALS_TARGET=$((Sha $m2Jar) -eq (Sha $moduleJar))"
"HOST_JAR_SHA256=$(Sha $hostJar)"
"HOST_JAR_BUILT_UTC=$((Get-Item -LiteralPath $hostJar).LastWriteTimeUtc.ToString('o'))"
"HOST_JAR_EQUALS_STEP11_DEPLOYED_JAR=$((Sha $hostJar) -eq (Sha $step11Jar))"

$hostEntries = Entries $hostJar
$nestedName = @($hostEntries.Keys | Where-Object { $_ -like 'BOOT-INF/lib/gm-expenses-*.jar' })[0]
"NESTED_GM_EXPENSES=$nestedName SHA256=$(BytesSha $hostEntries[$nestedName]) EQUALS_MODULE_JAR=$((BytesSha $hostEntries[$nestedName]) -eq (Sha $moduleJar))"

$migrations = @($hostEntries.Keys | Where-Object { $_ -match '^BOOT-INF/classes/db/migration/V(\d+)__.*\.sql$' })
$versions = @($migrations | ForEach-Object { [int]([regex]::Match($_, 'V(\d+)__').Groups[1].Value) } | Sort-Object)
"PACKAGED_MIGRATIONS=$($migrations.Count) HIGHEST=V$($versions[-1]) V62=$([bool]($migrations -match 'V62__')) V63=$([bool]($migrations -match 'V63__')) BEYOND_V63=$(@($versions | Where-Object { $_ -gt 63 }).Count)"
$r03Entries = Entries $rehearsal03Jar
$sqlNames = @(@($hostEntries.Keys) + @($r03Entries.Keys) | Where-Object { $_ -match '\.sql$' } | Sort-Object -Unique)
$sqlDiff = @($sqlNames | Where-Object { -not $hostEntries.ContainsKey($_) -or -not $r03Entries.ContainsKey($_) -or (BytesSha $hostEntries[$_]) -ne (BytesSha $r03Entries[$_]) })
"SQL_ENTRIES=$(@($sqlNames | Where-Object { $hostEntries.ContainsKey($_) }).Count) IDENTICAL_TO_REHEARSAL03_JAR=$($sqlDiff.Count -eq 0) DIFFERENT=[$($sqlDiff -join ', ')]"
$v63 = [System.Text.Encoding]::UTF8.GetString($hostEntries[@($migrations | Where-Object { $_ -match 'V63__' })[0]])
$v62 = [System.Text.Encoding]::UTF8.GetString($hostEntries[@($migrations | Where-Object { $_ -match 'V62__' })[0]])
"V62_PLANNED_DELIVERY_COLUMNS=$($v62.Contains('planned_delivery_method_code') -and $v62.Contains('planned_rendition_days'))"
"V63_UNIFIED_EQUATION=$($v63.Contains('chk_settlement_reconciled_equation'))"

$tmp = Join-Path $env:TEMP ("f12-nested-" + [guid]::NewGuid().ToString('N') + '.jar')
[IO.File]::WriteAllBytes($tmp, $hostEntries[$nestedName])
$module = Entries $tmp
[IO.File]::Delete($tmp)
$classes = @($module.Keys | Where-Object { $_ -like '*.class' })
$base = 'com/gypport/business/expenses/'
"CLASS CaseRenditionService=$($module.ContainsKey($base + 'casefile/application/CaseRenditionService.class'))"
"CLASS CaseRenditionLedger=$($module.ContainsKey($base + 'casefile/application/CaseRenditionLedger.class'))"
"CLASS CaseJustifiedTotalAllocation(FIFO)=$(@($classes | Where-Object { $_ -like '*CaseJustifiedTotalAllocation*' }).Count)"
"CLASS OneActiveAdvancePerCaseCurrency=$(@($classes | Where-Object { $_ -like '*OneActiveAdvance*' }).Count)"
"CLASS AdvanceDeliveryPlan(V62)=$($module.ContainsKey($base + 'advance/domain/AdvanceDeliveryPlan.class'))"
"CLASS SettlementBalance(V63)=$($module.ContainsKey($base + 'settlement/domain/SettlementBalance.class'))"
$fifoHits = @($classes | Where-Object { (Contains $module[$_] 'CaseJustifiedTotalAllocation') -or (Contains $module[$_] 'FIFO') -or (Contains $module[$_] 'closed_justified') -or (Contains $module[$_] 'DELIVERED_CASE_ADVANCES') })
"FIFO_REFERENCES_IN_MODULE_CLASSES=$($fifoHits.Count) [$($fifoHits -join ', ')]"
$service = $module[$base + 'casefile/application/ExpenseCaseService.class']
$rendition = $module[$base + 'casefile/application/CaseRenditionService.class']
"CASE_CLOSE_COPY drafts=$((Contains $service 'Hay 1 anticipo en borrador por ') -and (Contains $service 'anticipos en borrador por un total de ')) unbalanced=$(Contains $service 'La rendición del expediente tiene saldo pendiente') not_reconciled=$(Contains $service 'Concilia la rendición del expediente antes de cerrarlo.')"
"CASE_RENDITION_COPY managed_by_case=$(Contains $rendition 'La rendición de este anticipo se gestiona desde su expediente.') balanced_only=$(Contains $rendition 'por justificar o devolver.')"
$delivery = $module[$base + 'casefile/application/CaseAdvanceDeliveryService.class']
"V62_PLAN_IS_FIXED_COPY=$(Contains $delivery 'El método de entrega y los días para rendir se definieron al registrar el anticipo.')"
"ONE_ACTIVE_ADVANCE_REFUSAL_COPY=$(@($classes | Where-Object { (Contains $module[$_] 'anticipo activo') }).Count)"

$controller = $hostEntries['BOOT-INF/classes/com/gypport/server/module/expenses/ExpenseCaseController.class']
"ENDPOINT returns=$(Contains $controller '/{reference}/rendition/returns') reimbursements=$(Contains $controller '/{reference}/rendition/reimbursements') reconcile=$(Contains $controller '/{reference}/rendition/reconcile') close=$(Contains $controller '/{reference}/close') per_advance_rendition=$(Contains $controller '/advances/{advanceId}/rendition')"
$settlementController = $hostEntries['BOOT-INF/classes/com/gypport/server/module/expenses/AdvanceSettlementController.class']
"LEGACY_SETTLEMENT_API_GUARDED=$(Contains $settlementController 'requireOutsideCase')"
$advanceController = $hostEntries['BOOT-INF/classes/com/gypport/server/module/expenses/ExpenseAdvanceController.class']
"ADVANCE_DETAIL renditionManagedByCase=$(Contains $advanceController 'renditionManagedByCase')"

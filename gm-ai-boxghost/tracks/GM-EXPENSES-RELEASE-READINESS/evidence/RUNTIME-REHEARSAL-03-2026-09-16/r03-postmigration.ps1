# GM_EXPENSES_RUNTIME_REHEARSAL_03 - post-migration verification of the disposable copy (V63) against read-only Shared DEV (V43).
$ErrorActionPreference = 'Stop'
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\4bbfc1ff-e737-4ade-bbb8-169c21a07560\scratchpad'
$name = (Get-Content "$scratch\r03-container-name.txt").Trim()
if ($name -notlike 'gypport-rehearsal03-*') { throw 'Not the rehearsal container.' }
function Copy-Sql([string]$sql) {
    $out = $sql | docker exec -i $name sh -c 'MYSQL_PWD=$MYSQL_PASSWORD exec mysql -u$MYSQL_USER --batch --skip-column-names $MYSQL_DATABASE'
    if ($LASTEXITCODE -ne 0) { throw 'Rehearsal copy query failed.' }
    return $out
}
[Environment]::SetEnvironmentVariable('MYSQL_PWD', [Environment]::GetEnvironmentVariable('SPRING_DATASOURCE_PASSWORD', 'User'), 'Process')
$devUser = [Environment]::GetEnvironmentVariable('SPRING_DATASOURCE_USERNAME', 'User')
function Dev-Sql([string]$sql) {
    $out = ("SET SESSION TRANSACTION READ ONLY;`nSTART TRANSACTION READ ONLY;`n" + $sql + "`nROLLBACK;") |
        docker exec -i -e MYSQL_PWD gypport-mysql-dev mysql "-u$devUser" --batch --skip-column-names core_business_dev
    if ($LASTEXITCODE -ne 0) { throw 'Shared DEV read-only query failed.' }
    return $out
}
try {
    "## flyway"
    Copy-Sql "SELECT CONCAT('max=', MAX(CAST(version AS UNSIGNED)), ' rows=', COUNT(*), ' failed=', SUM(success = 0), ' applied_44_63=', SUM(CAST(version AS UNSIGNED) BETWEEN 44 AND 63 AND success = 1)) FROM flyway_schema_history WHERE version IS NOT NULL;"

    "## row counts: every table present before (Shared DEV V43) vs after (copy V63)"
    $before = @{}; foreach ($line in (Get-Content "$scratch\r03-copy-counts-before.txt")) { $t, $n = $line.Split("`t"); $before[$t] = [long]$n }
    $tables = Copy-Sql "SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE() AND table_type = 'BASE TABLE' ORDER BY table_name;"
    $countSql = "SELECT t, n FROM (" + (($tables | ForEach-Object { "SELECT '$_' AS t, COUNT(*) AS n FROM ``$_``" }) -join " UNION ALL ") + ") x ORDER BY t;"
    $after = @{}; foreach ($line in (Copy-Sql $countSql)) { $t, $n = $line.Split("`t"); $after[$t] = [long]$n }
    $changed = @(); $missing = @(); $added = @()
    foreach ($t in $before.Keys) { if (-not $after.ContainsKey($t)) { $missing += $t } elseif ($after[$t] -ne $before[$t]) { $changed += "$t $($before[$t])->$($after[$t])" } }
    foreach ($t in $after.Keys) { if (-not $before.ContainsKey($t)) { $added += "$t($($after[$t]))" } }
    "tables_before=$($before.Count) tables_after=$($after.Count) rows_before=$(($before.Values | Measure-Object -Sum).Sum) rows_after=$(($after.Values | Measure-Object -Sum).Sum)"
    "tables_missing_after=[$($missing -join ', ')]"
    "tables_with_changed_counts=[$($changed -join '; ')]"
    "tables_added_by_migrations=[$($added -join ', ')]"

    "## content of every gm-expenses table: CRC over all columns shared by Shared DEV (V43) and the copy (V63)"
    $expensesTables = @('responsible_reference','vehicle_reference','expense_category','expense_advance','expense','advance_settlement',
        'expense_advance_assignment_event','expense_review_event','expense_revision_event','settlement_adjustment_event',
        'settlement_balance_event','expense_adjustment','expense_document','expense_command_receipt','expense_allocation',
        'expense_document_review_event','expense_advance_participant_event','expense_case','expense_case_resource')
    $mismatch = 0
    foreach ($table in $expensesTables) {
        $devColumns = Dev-Sql "SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = '$table' ORDER BY ordinal_position;"
        $copyColumns = Copy-Sql "SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = '$table' ORDER BY ordinal_position;"
        $shared = @($devColumns | Where-Object { $copyColumns -contains $_ })
        $onlyCopy = @($copyColumns | Where-Object { $devColumns -notcontains $_ })
        $expression = "COALESCE(SUM(CRC32(CONCAT_WS('|', " + (($shared | ForEach-Object { "``$_``" }) -join ', ') + "))), 0)"
        $devHash = (Dev-Sql "SELECT CONCAT(COUNT(*), ':', $expression) FROM ``$table``;") | Select-Object -First 1
        $copyHash = (Copy-Sql "SELECT CONCAT(COUNT(*), ':', $expression) FROM ``$table``;") | Select-Object -First 1
        $same = $devHash -eq $copyHash
        if (-not $same) { $mismatch++ }
        "{0,-36} rows:crc dev={1} copy={2} same={3} shared_columns={4} columns_added={5}" -f $table, $devHash, $copyHash, $same, $shared.Count, ($(if ($onlyCopy.Count) { $onlyCopy -join ',' } else { '-' }))
    }
    "EXPENSES_CONTENT_MISMATCHES=$mismatch"

    "## protections, catalog, V61, V62, V63"
    $guards = @('trg_responsible_reference_no_delete:responsible_reference','trg_vehicle_reference_no_delete:vehicle_reference',
        'trg_expense_category_no_delete:expense_category','trg_expense_advance_no_delete:expense_advance','trg_expense_no_delete:expense',
        'trg_advance_settlement_no_delete:advance_settlement','trg_assign_event_no_delete:expense_advance_assignment_event',
        'trg_review_event_no_delete:expense_review_event','trg_revision_event_no_delete:expense_revision_event',
        'trg_set_adj_event_no_delete:settlement_adjustment_event','trg_exp_adjustment_no_delete:expense_adjustment',
        'trg_exp_document_no_delete:expense_document','trg_set_balance_event_no_delete:settlement_balance_event',
        'trg_command_receipt_no_delete:expense_command_receipt','trg_expense_allocation_no_delete:expense_allocation',
        'trg_exp_doc_review_event_no_delete:expense_document_review_event','trg_advance_participant_event_no_delete:expense_advance_participant_event')
    $pairs = ($guards | ForEach-Object { $n, $t = $_ -split ':'; "('$n','$t')" }) -join ','
    Copy-Sql "SELECT CONCAT('expenses_delete_guards=', COUNT(*)) FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = DATABASE() AND ACTION_TIMING = 'BEFORE' AND EVENT_MANIPULATION = 'DELETE' AND (TRIGGER_NAME, EVENT_OBJECT_TABLE) IN ($pairs);"
    Copy-Sql "SELECT CONCAT('canonical_categories=', COUNT(*)) FROM expense_category WHERE tenant_id IS NULL AND active = 1 AND category_code IN ('ALIMENTACION','COMBUSTIBLE','PEAJE','PARQUEADERO','MANTENIMIENTO','HOSPEDAJE','COMISIONES','OTRO');"
    Copy-Sql @"
SELECT CONCAT('V61 origin_columns=', (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND column_name IN ('origin_tenant_id','origin_party_id')),
  ' old_columns=', (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND column_name IN ('tenant_id','party_id')),
  ' origin_fks=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND constraint_type = 'FOREIGN KEY' AND constraint_name IN ('fk_user_accounts_origin_tenant','fk_user_accounts_origin_party','fk_user_accounts_origin_tenant_party')),
  ' old_fks=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND constraint_name IN ('fk_user_tenant','fk_user_party','fk_user_accounts_tenant_party')),
  ' identity_pair_check=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND constraint_name = 'ck_user_account_identity_pair'),
  ' retired_unique_key=', (SELECT COUNT(*) FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND index_name = 'uk_user_accounts_tenant_user'),
  ' accounts=', (SELECT COUNT(*) FROM user_accounts),
  ' accounts_without_membership=', (SELECT COUNT(*) FROM user_accounts u WHERE NOT EXISTS (SELECT 1 FROM user_tenant_memberships m WHERE m.user_account_id = u.user_account_id)));
"@
    Copy-Sql @"
SELECT CONCAT('V62 planned_columns=', (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'expense_advance' AND column_name IN ('planned_delivery_method_code','planned_rendition_days')),
  ' planned_checks=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'expense_advance' AND constraint_name IN ('chk_advance_planned_delivery_method_code','chk_advance_planned_rendition_days','chk_advance_planned_delivery_pair')),
  ' existing_rows_with_plan=', (SELECT COUNT(*) FROM expense_advance WHERE planned_delivery_method_code IS NOT NULL OR planned_rendition_days IS NOT NULL));
"@
    Copy-Sql @"
SELECT CONCAT('V63 return_reimburse_check=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'advance_settlement' AND constraint_name = 'chk_settlement_return_reimburse'),
  ' reconciled_equation_check=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'advance_settlement' AND constraint_name = 'chk_settlement_reconciled_equation'),
  ' adjustment_shortfall_check=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'advance_settlement' AND constraint_name = 'chk_settlement_adjustment_shortfall_only'),
  ' settlement_checks=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'advance_settlement' AND constraint_type = 'CHECK'),
  ' unified_clause=', (SELECT check_clause LIKE '%advance_amount_snapshot% + %reimbursement_amount%' FROM information_schema.check_constraints WHERE constraint_schema = DATABASE() AND constraint_name = 'chk_settlement_reconciled_equation'));
"@
    "## legacy link ambiguity (expense_case.advance_id pointing at an advance attached to another Case)"
    Copy-Sql "SELECT CONCAT('ambiguous_legacy_links=', COUNT(*)) FROM expense_case c JOIN expense_advance a ON a.advance_id = c.advance_id AND a.tenant_id = c.tenant_id WHERE a.expense_case_id IS NOT NULL AND a.expense_case_id <> c.expense_case_id;"
    "## Shared DEV untouched"
    Dev-Sql "SELECT CONCAT('shared_dev_flyway_max=', MAX(CAST(version AS UNSIGNED)), ' history_rows=', COUNT(*)) FROM flyway_schema_history WHERE version IS NOT NULL;"
}
finally {
    [Environment]::SetEnvironmentVariable('MYSQL_PWD', $null, 'Process')
}

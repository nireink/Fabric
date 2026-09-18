#!/usr/bin/env bash
# GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28 §6-§10 - the narrow final smoke after the Owner's reverso.
# Nothing is written: SQL runs in a READ ONLY transaction that is rolled back, HTTP probes carry no credentials, and no
# synthetic account or tenant is created. The authenticated API smoke of STEP 27 ran against this same container.
set -uo pipefail
export MSYS_NO_PATHCONV=1
HERE="$(cd "$(dirname "$0")" && pwd)"
failures=0; total=0
check() { total=$((total + 1)); if [ "$2" = "1" ]; then echo "PASS $1 :: $3"; else echo "FAIL $1 :: $3"; failures=$((failures + 1)); fi; }
ro() { { printf 'SET SESSION TRANSACTION READ ONLY;\nSTART TRANSACTION READ ONLY;\n'; cat; printf '\nROLLBACK;\n'; } \
  | docker exec -i gypport-mysql-dev sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql -uroot --batch --skip-column-names core_business_dev' 2>&1 \
  | tr -d '\r' | { grep -v "Using a password" || true; }; }
status() { curl -s -o "$HERE/.probe-body" -w '%{http_code}' "$1"; rm -f "$HERE/.probe-body"; }

echo "== runtime"
inspect=$(docker inspect -f '{{.Id}} {{.Image}} {{.State.StartedAt}} {{.RestartCount}} {{.State.Health.Status}}' gypport-backend-dev)
read -r cid image started restarts health <<<"$inspect"
check BACKEND_CONTAINER_UNCHANGED_SINCE_STEP27 \
  "$([ "$image" = "sha256:f44f598a5a786ab4f91a0d1b42fcfb1ee803a819f680c51cd11513a702d6533e" ] && [ "${cid:0:12}" = "445046e2801e" ] && [ "$restarts" = "0" ] && echo 1 || echo 0)" \
  "container ${cid:0:12} image ${image:7:12} started $started restarts $restarts"
list=$(status http://127.0.0.1:8080/api/expense-cases)
owner=$(status http://127.0.0.1:8080/api/expense-cases/437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0)
actuator=$(status http://127.0.0.1:8080/actuator/health)
errors=$(docker logs gypport-backend-dev 2>&1 | grep -c -E '^\S+\s+ERROR' || true)
exceptions=$(docker logs gypport-backend-dev 2>&1 | grep -c -E 'Exception|Servlet\.service\(\)' || true)
check BACKEND_HEALTH "$([ "$health" = "healthy" ] && [[ "$list" =~ ^40[13]$ ]] && echo 1 || echo 0)" \
  "docker health $health; the application answers HTTP (unauthenticated list $list, actuator $actuator)"
check UNAUTHENTICATED_LIST_REFUSED "$([[ "$list" =~ ^40[13]$ ]] && echo 1 || echo 0)" "GET /api/expense-cases without a session -> $list"
check UNAUTHENTICATED_UUID_ROUTE_REFUSED "$([[ "$owner" =~ ^40[13]$ ]] && echo 1 || echo 0)" "GET /api/expense-cases/437a92bf-... without a session -> $owner"
check NO_SERVER_ERROR_LOGGED "$([ "$errors" = "0" ] && [ "$exceptions" = "0" ] && echo 1 || echo 0)" \
  "backend log since start: ERROR lines $errors, exceptions $exceptions"

echo "== Shared DEV, the Owner tenant and the Owner Case (read-only)"
sqlout=$(ro <<'SQL'
SET @cid := (SELECT expense_case_id FROM expense_case WHERE expense_case_uuid = UUID_TO_BIN('437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0'));
SET @tenant := (SELECT tenant_id FROM expense_case WHERE expense_case_id = @cid);
SELECT CONCAT(IF(MAX(CAST(version AS UNSIGNED)) = 65 AND SUM(success = 0) = 0, 'PASS', 'FAIL'), ' SHARED_DEV_V65 :: current ',
              MAX(CAST(version AS UNSIGNED)), ', failed ', SUM(success = 0)) FROM flyway_schema_history WHERE version IS NOT NULL;
-- §1/§9 numbering: permanent EXP. NN, daily ID, business date
SELECT CONCAT(IF(expense_sequence = 8 AND case_number = '202609170001' AND case_business_date = '2026-09-17', 'PASS', 'FAIL'),
              ' NUMBERING_COMPRA_FILTRO :: EXP. ', LPAD(expense_sequence, 2, '0'), ' | ID ', case_number, ' | Fecha ', case_business_date)
FROM expense_case WHERE expense_case_uuid = UUID_TO_BIN('437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0');
SELECT CONCAT(IF(expense_sequence = 9 AND case_number = '202609170002' AND case_business_date = '2026-09-17', 'PASS', 'FAIL'),
              ' NUMBERING_VIAJE_QUITO :: EXP. ', LPAD(expense_sequence, 2, '0'), ' | ID ', case_number, ' | Fecha ', case_business_date)
FROM expense_case WHERE expense_case_uuid = UUID_TO_BIN('a41aa6c9-945a-47bc-98da-69ddeb18beb9');
SELECT CONCAT(IF(COUNT(*) = 9 AND MIN(expense_sequence) = 1 AND MAX(expense_sequence) = 9 AND COUNT(DISTINCT expense_sequence) = 9
                 AND (SELECT last_sequence FROM expense_case_permanent_sequence WHERE tenant_id = @tenant) = 9, 'PASS', 'FAIL'),
              ' OWNER_TENANT_PERMANENT_NUMBERS :: ', COUNT(*), ' Cases numbered ', MIN(expense_sequence), '..', MAX(expense_sequence),
              ', counter at ', (SELECT last_sequence FROM expense_case_permanent_sequence WHERE tenant_id = @tenant))
FROM expense_case WHERE tenant_id = @tenant;
-- §6 the financial summary, from the inputs the backend reads (ExpenseCaseFinancialSummary / CaseRenditionLedger)
SET @delivered := (SELECT IFNULL(SUM(advance_amount), 0) FROM expense_advance WHERE expense_case_id = @cid AND lifecycle_status NOT IN ('BORRADOR', 'CANCELADO'));
SET @justified := (SELECT IFNULL(SUM(expense_amount), 0) FROM expense WHERE expense_case_id = @cid AND lifecycle_status = 'APROBADO');
SET @spent := (SELECT IFNULL(SUM(expense_amount), 0) FROM expense WHERE expense_case_id = @cid AND lifecycle_status NOT IN ('RECHAZADO', 'EXCLUIDO'));
SET @returned := (SELECT IFNULL(SUM(s.returned_amount), 0) FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @cid);
SET @reimbursed := (SELECT IFNULL(SUM(s.reimbursement_amount), 0) FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @cid);
SET @adjustments := (SELECT IFNULL(SUM(s.authorized_adjustment_total), 0) FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @cid);
SET @currencies := (SELECT COUNT(DISTINCT c) FROM (SELECT advance_currency AS c FROM expense_advance WHERE expense_case_id = @cid
                    UNION ALL SELECT expense_currency FROM expense WHERE expense_case_id = @cid) x);
SET @base := @delivered - @justified;
SET @position := @delivered + @reimbursed - @justified - @returned - @adjustments;
SELECT CONCAT(IF(@currencies = 1, 'PASS', 'FAIL'), ' ONE_CURRENCY :: ', @currencies, ' currency (USD) in advances and expenses');
SELECT CONCAT(IF(@delivered = 320, 'PASS', 'FAIL'), ' TOTAL_ANTICIPOS :: ', FORMAT(@delivered, 2));
SELECT CONCAT(IF(@justified = 400, 'PASS', 'FAIL'), ' TOTAL_GASTOS :: ', FORMAT(@justified, 2), ' (APROBADO only)');
SELECT CONCAT(IF(@base = -80, 'PASS', 'FAIL'), ' TOTAL_A_CONCILIAR :: ', FORMAT(ABS(@base), 2), IF(@base < 0, ' Por reembolsar', IF(@base > 0, ' Por devolver', ' Balanceado')));
SELECT CONCAT(IF(@returned = 0, 'PASS', 'FAIL'), ' DEVUELTO :: ', FORMAT(@returned, 2));
SELECT CONCAT(IF(@reimbursed = 0, 'PASS', 'FAIL'), ' REEMBOLSADO :: ', FORMAT(@reimbursed, 2));
SELECT CONCAT(IF(@adjustments = 0, 'PASS', 'FAIL'), ' AJUSTES :: ', FORMAT(@adjustments, 2));
SELECT CONCAT(IF(@position = -80, 'PASS', 'FAIL'), ' PENDIENTE :: ', FORMAT(ABS(@position), 2),
              IF(@position < 0, ' Por reembolsar', IF(@position > 0, ' Por justificar o devolver', ' Pendiente de conciliar')));
SELECT CONCAT(IF(@spent = 400, 'PASS', 'FAIL'), ' USADO :: ', FORMAT(@spent, 2), ' (every expense not rejected or excluded)');
SELECT CONCAT(IF(ROUND(@spent / @delivered * 100) = 125, 'PASS', 'FAIL'), ' USO :: ', ROUND(@spent / @delivered * 100), '%');
-- §7 the rejected expense stays RECHAZADO and weighs nothing
SELECT CONCAT(IF(COUNT(*) = 1 AND SUM(expense_amount) = 200 AND @justified = 400 AND @spent = 400, 'PASS', 'FAIL'),
              ' REJECTED_EXPENSE_EFFECT_ZERO :: ', COUNT(*), ' RECHAZADO for ', FORMAT(SUM(expense_amount), 2),
              '; Total gastos and Usado exclude it') FROM expense WHERE expense_case_id = @cid AND lifecycle_status = 'RECHAZADO';
-- §5 the reverso: originals kept, compensating events appended, one per original
SELECT CONCAT(IF(COUNT(*) = 2 AND SUM(amount) = 300 AND MIN(occurred_at) = MAX(occurred_at) AND SUM(reverses_balance_event_id IS NULL) = 2, 'PASS', 'FAIL'),
              ' ORIGINAL_EVENTS_PRESERVED :: 29 and 30 RETURN_REGISTERED, ', FORMAT(SUM(amount), 2), ' at ', MIN(occurred_at))
FROM settlement_balance_event WHERE settlement_balance_event_id IN (29, 30) AND event_type = 'RETURN_REGISTERED';
SELECT CONCAT(IF(COUNT(*) = 2 AND SUM(r.amount = o.amount) = 2 AND SUM(r.settlement_id = o.settlement_id) = 2
                 AND SUM(r.event_type = 'RETURN_REVERSED') = 2, 'PASS', 'FAIL'),
              ' REVERSAL_EVENTS_APPENDED :: ', GROUP_CONCAT(CONCAT(r.settlement_balance_event_id, '->', r.reverses_balance_event_id, ' ', FORMAT(r.amount, 2))
              ORDER BY r.settlement_balance_event_id SEPARATOR ', '))
FROM settlement_balance_event r JOIN settlement_balance_event o ON o.settlement_balance_event_id = r.reverses_balance_event_id
WHERE r.reverses_balance_event_id IN (29, 30);
SELECT CONCAT(IF(COUNT(*) = 2 AND COUNT(DISTINCT r.performed_by_user_account_id) = 1 AND SUM(u.user_account_id IS NULL) = 0
                 AND SUM(r.performed_by_user_account_id = c.created_by_user_account_id) = 2, 'PASS', 'FAIL'),
              ' AUTHENTICATED_ACTOR_RECORDED :: user_account ', MIN(r.performed_by_user_account_id),
              ' (a global UserAccount; the account that created the Case and registered the original returns)')
FROM settlement_balance_event r LEFT JOIN user_accounts u ON u.user_account_id = r.performed_by_user_account_id
JOIN expense_case c ON c.expense_case_id = @cid WHERE r.reverses_balance_event_id IN (29, 30);
SELECT CONCAT(IF(COUNT(*) = 2 AND SUM(occurred_at IS NULL) = 0 AND SUM(reason IS NULL OR TRIM(reason) = '') = 0, 'PASS', 'FAIL'),
              ' REVERSAL_TIMESTAMP_AND_REASON :: ', MIN(occurred_at), ' (database time zone UTC), reason "', MIN(reason), '"')
FROM settlement_balance_event WHERE reverses_balance_event_id IN (29, 30);
SELECT CONCAT(IF(MAX(n) = 1 AND (SELECT COUNT(*) FROM information_schema.statistics WHERE table_schema = DATABASE()
                 AND table_name = 'settlement_balance_event' AND index_name = 'uq_set_balance_single_reversal'
                 AND column_name = 'reverses_balance_event_id' AND non_unique = 0) = 1, 'PASS', 'FAIL'),
              ' DUPLICATE_REVERSAL_BLOCKED :: at most ', MAX(n), ' reversal per original; UNIQUE uq_set_balance_single_reversal(reverses_balance_event_id)')
FROM (SELECT COUNT(*) AS n FROM settlement_balance_event WHERE reverses_balance_event_id IS NOT NULL GROUP BY reverses_balance_event_id) x;
SELECT CONCAT(IF(SUM(CASE event_type WHEN 'RETURN_REGISTERED' THEN amount WHEN 'RETURN_REVERSED' THEN -amount ELSE 0 END) = @returned, 'PASS', 'FAIL'),
              ' LEDGER_AGREES_WITH_ROWS :: returns registered minus reversed = ',
              FORMAT(SUM(CASE event_type WHEN 'RETURN_REGISTERED' THEN amount WHEN 'RETURN_REVERSED' THEN -amount ELSE 0 END), 2),
              ' = rows returned ', FORMAT(@returned, 2), '; reimbursement events ', SUM(event_type LIKE 'REIMBURSEMENT%'))
FROM settlement_balance_event e JOIN advance_settlement s ON s.settlement_id = e.settlement_id
JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @cid;
SELECT CONCAT(IF(COUNT(*) = 2 AND SUM(s.lifecycle_status = 'EN_CONCILIACION' AND s.reconciliation_result = 'PENDING') = 2, 'PASS', 'FAIL'),
              ' RENDITION_REOPENED :: ', GROUP_CONCAT(CONCAT(s.settlement_id, ' ', s.lifecycle_status, '/', s.reconciliation_result) ORDER BY s.settlement_id SEPARATOR ', '))
FROM advance_settlement s WHERE s.settlement_id IN (61, 62);
-- §8 Registrar reembolso: CaseRenditionLedger offers it on an open Case with a delivered advance, a rendition that is not
-- CERRADO, a positive pending reimbursement and no authorized adjustment. Nothing was registered (the Owner deferred it).
SELECT CONCAT(IF(c.lifecycle_status = 'ABIERTO' AND @delivered > 0 AND @position < 0 AND @adjustments = 0
                 AND (SELECT COUNT(*) FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id
                      WHERE a.expense_case_id = @cid AND s.lifecycle_status = 'CERRADO') = 0, 'PASS', 'FAIL'),
              ' REIMBURSEMENT_OFFERED :: Case ', c.lifecycle_status, ', pending reimbursement ', FORMAT(-@position, 2), ', no row CERRADO')
FROM expense_case c WHERE c.expense_case_id = @cid;
-- tenant isolation as data: nothing synthetic lives in the Owner tenant
SELECT CONCAT(IF(COUNT(*) = 0, 'PASS', 'FAIL'), ' OWNER_TENANT_HAS_NO_SYNTHETIC_CASES :: ', COUNT(*), ' Cases created by @example.test accounts')
FROM expense_case c JOIN user_accounts u ON u.user_account_id = c.created_by_user_account_id
WHERE c.tenant_id = @tenant AND u.email_address LIKE '%@example.test';
SQL
)
echo "$sqlout"
sql_pass=$(grep -c '^PASS ' <<<"$sqlout" || true)
sql_fail=$(grep -c -E '^(FAIL |ERROR)' <<<"$sqlout" || true)
total=$((total + sql_pass + sql_fail)); failures=$((failures + sql_fail))
echo "FINAL_SMOKE_CHECKS=$total FAILURES=$failures WRITES=0"

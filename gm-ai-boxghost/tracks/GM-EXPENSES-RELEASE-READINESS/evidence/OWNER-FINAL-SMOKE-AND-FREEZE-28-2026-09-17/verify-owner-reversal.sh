#!/usr/bin/env bash
# GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28 §5-§9 - read-only proof of the Owner's authenticated reversal of the
# "Devolucion USD 300.00" movement of Case 437a92bf (Compra Filtro). Nothing is written to Shared DEV.
set -uo pipefail
export MSYS_NO_PATHCONV=1
ro() { { printf 'SET SESSION TRANSACTION READ ONLY;\nSTART TRANSACTION READ ONLY;\n'; cat; printf '\nROLLBACK;\n'; } \
  | docker exec -i gypport-mysql-dev sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql -uroot --batch --skip-column-names core_business_dev' 2>&1 \
  | tr -d '\r' | { grep -v "Using a password" || true; }; }

ro <<'SQL'
SET @cid := (SELECT expense_case_id FROM expense_case WHERE expense_case_uuid = UUID_TO_BIN('437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0'));
SELECT CONCAT('CASE ', name, ' | status=', lifecycle_status, ' | EXP. ', LPAD(expense_sequence, 2, '0'), ' | ID ', case_number, ' | Fecha ', case_business_date) FROM expense_case WHERE expense_case_id = @cid;
-- §5 the originals are unchanged, and each reversal points at its original with actor, instant and reason
SELECT CONCAT('EVENT ', e.settlement_balance_event_id, ' ', e.event_type, ' ', e.amount, ' | reverses=',
              IFNULL(CAST(e.reverses_balance_event_id AS CHAR), 'NULL'), ' | actor=', e.performed_by_user_account_id,
              ' | at=', e.occurred_at, ' | reason=', IFNULL(e.reason, ''))
FROM settlement_balance_event e JOIN advance_settlement s ON s.settlement_id = e.settlement_id
JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @cid ORDER BY e.settlement_balance_event_id;
SELECT CONCAT('ORIGINALS_UNCHANGED=', IF(COUNT(*) = 2 AND SUM(amount) = 300 AND MIN(occurred_at) = '2026-09-17 16:40:29.559'
              AND MAX(occurred_at) = '2026-09-17 16:40:29.559' AND SUM(reverses_balance_event_id IS NULL) = 2, 'YES', 'NO'))
FROM settlement_balance_event WHERE settlement_balance_event_id IN (29, 30) AND event_type = 'RETURN_REGISTERED';
SELECT CONCAT('REVERSALS=', COUNT(*), ' | total=', IFNULL(SUM(r.amount), 0),
              ' | each_matches_its_original=', IF(COUNT(*) = 2 AND SUM(r.amount = o.amount) = 2, 'YES', 'NO'),
              ' | actor_populated=', IF(COUNT(*) > 0 AND SUM(r.performed_by_user_account_id IS NULL) = 0, 'YES', 'NO'),
              ' | timestamp_populated=', IF(COUNT(*) > 0 AND SUM(r.occurred_at IS NULL) = 0, 'YES', 'NO'),
              ' | reason_populated=', IF(COUNT(*) > 0 AND SUM(r.reason IS NULL OR r.reason = '') = 0, 'YES', 'NO'))
FROM settlement_balance_event r JOIN settlement_balance_event o ON o.settlement_balance_event_id = r.reverses_balance_event_id
WHERE r.reverses_balance_event_id IN (29, 30);
-- the actor is a global UserAccount, never a membership
SELECT CONCAT('REVERSAL_ACTOR user_account_id=', r.performed_by_user_account_id, ' exists=', IF(u.user_account_id IS NULL, 'NO', 'YES'))
FROM settlement_balance_event r LEFT JOIN user_accounts u ON u.user_account_id = r.performed_by_user_account_id
WHERE r.reverses_balance_event_id IN (29, 30) LIMIT 1;
-- duplicate reversal is refused by the database itself, not only by the service
SELECT CONCAT('SINGLE_REVERSAL_KEY=', COUNT(*)) FROM information_schema.statistics
WHERE table_schema = DATABASE() AND table_name = 'settlement_balance_event' AND index_name = 'uq_set_balance_single_reversal';
-- §6 the rendition rows after the reverso
SELECT CONCAT('SETTLEMENT ', s.settlement_id, ' status=', s.lifecycle_status, ' result=', s.reconciliation_result,
              ' returned=', s.returned_amount, ' reimbursed=', s.reimbursement_amount)
FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @cid;
-- §6/§7 the inputs of the financial summary; the rejected expense weighs nothing
SELECT CONCAT('INPUTS delivered=', (SELECT SUM(advance_amount) FROM expense_advance WHERE expense_case_id = @cid AND lifecycle_status NOT IN ('BORRADOR', 'CANCELADO')),
              ' approved=', (SELECT SUM(expense_amount) FROM expense WHERE expense_case_id = @cid AND lifecycle_status = 'APROBADO'),
              ' rejected=', (SELECT IFNULL(SUM(expense_amount), 0) FROM expense WHERE expense_case_id = @cid AND lifecycle_status = 'RECHAZADO'),
              ' returned=', (SELECT SUM(s.returned_amount) FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @cid),
              ' reimbursed=', (SELECT SUM(s.reimbursement_amount) FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @cid));
SELECT CONCAT('REJECTED_EXPENSE status=', lifecycle_status, ' amount=', expense_amount) FROM expense WHERE expense_case_id = @cid AND lifecycle_status = 'RECHAZADO';
SQL

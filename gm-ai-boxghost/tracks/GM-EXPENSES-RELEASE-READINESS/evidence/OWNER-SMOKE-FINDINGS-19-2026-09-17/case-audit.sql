-- GM_EXPENSES_OWNER_SMOKE_FINDINGS_19 - read-only audit of ExpenseCase 437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0 (SELECT only).
SET @case_uuid = UUID_TO_BIN('437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0');
SELECT '## case' AS section;
SELECT c.expense_case_id, BIN_TO_UUID(c.expense_case_uuid) AS case_uuid, c.tenant_id, c.organization_scope, c.name, c.lifecycle_status, c.version,
       c.created_at, c.created_by_user_account_id, c.closed_at, c.closed_by_user_account_id, c.advance_id AS legacy_advance_link,
       c.responsible_snapshot_name, c.reviewer_snapshot_name
FROM expense_case c WHERE c.expense_case_uuid = @case_uuid;
SET @case_id = (SELECT expense_case_id FROM expense_case WHERE expense_case_uuid = @case_uuid);
SET @tenant_id = (SELECT tenant_id FROM expense_case WHERE expense_case_uuid = @case_uuid);

SELECT '## advances' AS section;
SELECT a.advance_id, BIN_TO_UUID(a.advance_uuid) AS advance_uuid, a.advance_amount, a.advance_currency, a.lifecycle_status, a.version,
       a.activity_type, a.activity_description, a.planned_delivery_method_code, a.planned_rendition_days, a.delivery_method_code,
       a.created_at, a.created_by_user_account_id, a.delivered_at, a.delivered_by_user_account_id, a.rendition_due_at, a.updated_at
FROM expense_advance a WHERE a.tenant_id = @tenant_id AND (a.expense_case_id = @case_id OR a.advance_id = (SELECT advance_id FROM expense_case WHERE expense_case_id = @case_id))
ORDER BY a.created_at;

SELECT '## expenses' AS section;
SELECT e.expense_id, BIN_TO_UUID(e.expense_uuid) AS expense_uuid, e.expense_amount, e.expense_currency, e.expense_date, e.lifecycle_status, e.version,
       e.advance_id, e.expense_category_id, LEFT(IFNULL(e.description, ''), 60) AS description, e.created_at, e.created_by_user_account_id, e.updated_at
FROM expense e WHERE e.tenant_id = @tenant_id AND e.expense_case_id = @case_id ORDER BY e.created_at;

SELECT '## expense review events' AS section;
SELECT r.expense_review_event_id, r.expense_id, r.event_type, r.reason, LEFT(IFNULL(r.notes, ''), 60) AS notes, r.performed_by_user_account_id, r.occurred_at
FROM expense_review_event r JOIN expense e ON e.expense_id = r.expense_id WHERE e.tenant_id = @tenant_id AND e.expense_case_id = @case_id ORDER BY r.occurred_at, r.expense_review_event_id;

SELECT '## expense revision events' AS section;
SELECT v.expense_revision_event_id, v.expense_id, v.revision_type, v.revision_number, v.performed_by_user_account_id, v.occurred_at
FROM expense_revision_event v JOIN expense e ON e.expense_id = v.expense_id WHERE e.tenant_id = @tenant_id AND e.expense_case_id = @case_id ORDER BY v.occurred_at;

SELECT '## expense adjustments' AS section;
SELECT x.expense_adjustment_id, x.original_expense_id, x.adjustment_type, x.adjustment_amount, x.voids_adjustment_id, x.created_by_user_account_id, x.created_at
FROM expense_adjustment x JOIN expense e ON e.expense_id = x.original_expense_id WHERE e.tenant_id = @tenant_id AND e.expense_case_id = @case_id;

SELECT '## rendition rows (advance_settlement, technical carriers)' AS section;
SELECT s.settlement_id, BIN_TO_UUID(s.settlement_uuid) AS settlement_uuid, s.advance_id, s.currency_code, s.advance_amount_snapshot, s.justified_expense_total,
       s.returned_amount, s.reimbursement_amount, s.authorized_adjustment_total, s.reconciliation_result, s.lifecycle_status, s.version, s.created_at, s.updated_at,
       s.closed_at, s.closed_by_user_account_id
FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id AND a.tenant_id = s.tenant_id
WHERE a.tenant_id = @tenant_id AND a.expense_case_id = @case_id ORDER BY s.created_at;

SELECT '## settlement balance events (returns / reimbursements)' AS section;
SELECT b.settlement_balance_event_id, BIN_TO_UUID(b.settlement_balance_event_uuid) AS event_uuid, b.settlement_id, b.currency_code, b.event_type, b.amount,
       b.reverses_balance_event_id, LEFT(IFNULL(b.reason, ''), 80) AS reason, b.performed_by_user_account_id, b.occurred_at
FROM settlement_balance_event b JOIN advance_settlement s ON s.settlement_id = b.settlement_id AND s.tenant_id = b.tenant_id
JOIN expense_advance a ON a.advance_id = s.advance_id AND a.tenant_id = s.tenant_id
WHERE a.tenant_id = @tenant_id AND a.expense_case_id = @case_id ORDER BY b.occurred_at, b.settlement_balance_event_id;

SELECT '## settlement adjustment events' AS section;
SELECT j.settlement_adjustment_event_id, j.settlement_id, j.event_type, j.amount, j.reverses_adjustment_event_id, LEFT(j.reason, 80) AS reason, j.performed_by_user_account_id, j.occurred_at
FROM settlement_adjustment_event j JOIN advance_settlement s ON s.settlement_id = j.settlement_id AND s.tenant_id = j.tenant_id
JOIN expense_advance a ON a.advance_id = s.advance_id AND a.tenant_id = s.tenant_id
WHERE a.tenant_id = @tenant_id AND a.expense_case_id = @case_id ORDER BY j.occurred_at;

SELECT '## command receipts for the case, its advances, expenses and rendition rows' AS section;
SELECT k.command_receipt_id, k.command_type, k.target_type, BIN_TO_UUID(k.target_public_uuid) AS target_uuid, k.committed_version, k.executed_by_user_account_id, k.executed_at,
       LEFT(CAST(k.result_snapshot AS CHAR), 220) AS result_snapshot
FROM expense_command_receipt k
WHERE k.tenant_id = @tenant_id AND (
      k.target_public_uuid = @case_uuid
   OR k.target_public_uuid IN (SELECT advance_uuid FROM expense_advance WHERE tenant_id = @tenant_id AND expense_case_id = @case_id)
   OR k.target_public_uuid IN (SELECT expense_uuid FROM expense WHERE tenant_id = @tenant_id AND expense_case_id = @case_id)
   OR k.target_public_uuid IN (SELECT s.settlement_uuid FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id AND a.tenant_id = s.tenant_id WHERE a.tenant_id = @tenant_id AND a.expense_case_id = @case_id))
ORDER BY k.executed_at, k.command_receipt_id;

SELECT '## actors' AS section;
SELECT u.user_account_id, CONCAT(LEFT(u.username, 3), '***@', SUBSTRING_INDEX(u.username, '@', -1)) AS username_masked
FROM user_accounts u WHERE u.user_account_id IN (
  SELECT created_by_user_account_id FROM expense_case WHERE expense_case_id = @case_id
  UNION SELECT performed_by_user_account_id FROM settlement_balance_event b JOIN advance_settlement s ON s.settlement_id = b.settlement_id JOIN expense_advance a ON a.advance_id = s.advance_id WHERE a.expense_case_id = @case_id
  UNION SELECT delivered_by_user_account_id FROM expense_advance WHERE expense_case_id = @case_id
  UNION SELECT performed_by_user_account_id FROM expense_review_event r JOIN expense e ON e.expense_id = r.expense_id WHERE e.expense_case_id = @case_id);

SELECT '## other cases of the tenant created today (for the business id design)' AS section;
SELECT c.expense_case_id, BIN_TO_UUID(c.expense_case_uuid) AS case_uuid, c.name, c.lifecycle_status, c.created_at FROM expense_case c WHERE c.tenant_id = @tenant_id ORDER BY c.created_at;

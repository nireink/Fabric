SET SESSION TRANSACTION READ ONLY;
START TRANSACTION READ ONLY;
SELECT '## flyway' AS section;
SELECT MAX(CAST(version AS UNSIGNED)) AS flyway_max, COUNT(*) AS history_rows, SUM(success = 0) AS failed FROM flyway_schema_history WHERE version IS NOT NULL;
SELECT '## legacy OBSERVADO without OBSERVED event' AS section;
SELECT HEX(e.expense_uuid) AS expense, e.tenant_id, e.expense_case_id, e.created_at
FROM expense e
WHERE e.lifecycle_status = 'OBSERVADO'
  AND NOT EXISTS (SELECT 1 FROM expense_review_event r WHERE r.expense_id = e.expense_id AND r.event_type = 'OBSERVED');
SELECT '## CERRADO settlements whose advance is not RENDIDO/CERRADO' AS section;
SELECT HEX(s.settlement_uuid) AS settlement, HEX(a.advance_uuid) AS advance, a.lifecycle_status AS advance_status, a.tenant_id,
       HEX(c.expense_case_uuid) AS expense_case, c.lifecycle_status AS case_status
FROM advance_settlement s
JOIN expense_advance a ON a.advance_id = s.advance_id AND a.tenant_id = s.tenant_id
LEFT JOIN expense_case c ON c.expense_case_id = a.expense_case_id
WHERE s.lifecycle_status = 'CERRADO' AND a.lifecycle_status NOT IN ('RENDIDO', 'CERRADO');
SELECT '## BORRADOR advances' AS section;
SELECT a.tenant_id, (a.expense_case_id IS NOT NULL) AS in_case, COUNT(*) AS drafts,
       GROUP_CONCAT(DISTINCT HEX(c.expense_case_uuid)) AS cases
FROM expense_advance a LEFT JOIN expense_case c ON c.expense_case_id = a.expense_case_id
WHERE a.lifecycle_status = 'BORRADOR' GROUP BY a.tenant_id, (a.expense_case_id IS NOT NULL) ORDER BY a.tenant_id;
SELECT '## advance states and delivery method codes' AS section;
SELECT a.lifecycle_status, COALESCE(a.delivery_method_code, '(null)') AS delivery_method_code, COUNT(*) AS advances
FROM expense_advance a GROUP BY a.lifecycle_status, COALESCE(a.delivery_method_code, '(null)') ORDER BY 1, 2;
SELECT '## settlements by status' AS section;
SELECT s.lifecycle_status, s.reconciliation_result, COUNT(*) AS settlements, SUM(s.returned_amount > 0) AS with_return,
       SUM(s.reimbursement_amount > 0) AS with_reimbursement, SUM(s.authorized_adjustment_total > 0) AS with_adjustment
FROM advance_settlement s GROUP BY s.lifecycle_status, s.reconciliation_result ORDER BY 1, 2;
SELECT '## Case+currency groups with more than one financially active advance (S06 legacy)' AS section;
SELECT a.tenant_id, HEX(c.expense_case_uuid) AS expense_case, c.lifecycle_status AS case_status, a.advance_currency,
       COUNT(*) AS active_advances, GROUP_CONCAT(a.lifecycle_status ORDER BY a.created_at) AS statuses
FROM expense_advance a JOIN expense_case c ON c.expense_case_id = a.expense_case_id
WHERE a.lifecycle_status NOT IN ('CANCELADO', 'CERRADO')
GROUP BY a.tenant_id, c.expense_case_uuid, c.lifecycle_status, a.advance_currency HAVING COUNT(*) > 1;
SELECT '## other legacy shapes' AS section;
SELECT (SELECT COUNT(*) FROM expense_advance WHERE expense_case_id IS NULL) AS advances_without_case,
       (SELECT COUNT(*) FROM expense_case WHERE advance_id IS NOT NULL) AS cases_with_legacy_advance_link,
       (SELECT COUNT(*) FROM expense WHERE expense_case_id IS NULL) AS expenses_without_case,
       (SELECT COUNT(*) FROM expense_case WHERE lifecycle_status = 'ABIERTO') AS open_cases,
       (SELECT COUNT(*) FROM expense_case WHERE lifecycle_status = 'CERRADO') AS closed_cases;
SELECT '## tenants holding expenses data, with synthetic-account share' AS section;
SELECT t.tenant_id,
       (SELECT COUNT(*) FROM user_accounts u WHERE u.tenant_id = t.tenant_id) AS accounts,
       (SELECT COUNT(*) FROM user_accounts u WHERE u.tenant_id = t.tenant_id AND u.email_address LIKE '%@example.test') AS example_test_accounts,
       (SELECT COUNT(*) FROM expense_case c WHERE c.tenant_id = t.tenant_id) AS cases,
       (SELECT COUNT(*) FROM expense_advance a WHERE a.tenant_id = t.tenant_id) AS advances,
       (SELECT COUNT(*) FROM expense e WHERE e.tenant_id = t.tenant_id) AS expenses
FROM tenants t
WHERE EXISTS (SELECT 1 FROM expense_case c WHERE c.tenant_id = t.tenant_id)
   OR EXISTS (SELECT 1 FROM expense_advance a WHERE a.tenant_id = t.tenant_id)
   OR EXISTS (SELECT 1 FROM expense e WHERE e.tenant_id = t.tenant_id)
ORDER BY t.tenant_id;
ROLLBACK;

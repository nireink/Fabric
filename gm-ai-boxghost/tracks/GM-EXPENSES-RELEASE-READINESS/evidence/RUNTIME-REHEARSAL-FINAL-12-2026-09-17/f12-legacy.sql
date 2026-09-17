SELECT '## flyway' AS section;
SELECT MAX(CAST(version AS UNSIGNED)) AS flyway_max, COUNT(*) AS history_rows, SUM(success = 0) AS failed FROM flyway_schema_history WHERE version IS NOT NULL;
SELECT '## INCONSISTENT: OBSERVADO expense without an OBSERVED review event' AS section;
SELECT HEX(e.expense_uuid) AS expense, e.tenant_id, e.expense_case_id, e.created_at
FROM expense e
WHERE e.lifecycle_status = 'OBSERVADO'
  AND NOT EXISTS (SELECT 1 FROM expense_review_event r WHERE r.expense_id = e.expense_id AND r.event_type = 'OBSERVED');
SELECT '## INCONSISTENT: CERRADO settlement whose advance is not RENDIDO/CERRADO (blocks closing its Case)' AS section;
SELECT HEX(s.settlement_uuid) AS settlement, HEX(a.advance_uuid) AS advance, a.lifecycle_status AS advance_status, a.tenant_id,
       HEX(c.expense_case_uuid) AS expense_case, c.lifecycle_status AS case_status
FROM advance_settlement s
JOIN expense_advance a ON a.advance_id = s.advance_id AND a.tenant_id = s.tenant_id
LEFT JOIN expense_case c ON c.expense_case_id = a.expense_case_id
WHERE s.lifecycle_status = 'CERRADO' AND a.lifecycle_status NOT IN ('RENDIDO', 'CERRADO');
SELECT '## OPEN WORK (not a defect): BORRADOR advances by tenant' AS section;
SELECT a.tenant_id, (a.expense_case_id IS NOT NULL) AS in_case, COUNT(*) AS drafts, MIN(a.created_at) AS oldest, MAX(a.created_at) AS newest
FROM expense_advance a WHERE a.lifecycle_status = 'BORRADOR' GROUP BY a.tenant_id, (a.expense_case_id IS NOT NULL) ORDER BY a.tenant_id;
SELECT '## LEGACY SHAPE: advances outside any Case (direct or legacy link)' AS section;
SELECT a.tenant_id, a.lifecycle_status, COUNT(*) AS advances
FROM expense_advance a
WHERE a.expense_case_id IS NULL AND NOT EXISTS (SELECT 1 FROM expense_case c WHERE c.advance_id = a.advance_id AND c.tenant_id = a.tenant_id)
GROUP BY a.tenant_id, a.lifecycle_status ORDER BY a.tenant_id, a.lifecycle_status;
SELECT '## LEGACY SHAPE: advances attached only through the legacy expense_case.advance_id link' AS section;
SELECT COUNT(*) AS legacy_linked_advances FROM expense_advance a
WHERE a.expense_case_id IS NULL AND EXISTS (SELECT 1 FROM expense_case c WHERE c.advance_id = a.advance_id AND c.tenant_id = a.tenant_id);
SELECT '## LEGACY SHAPE: expenses without a Case' AS section;
SELECT e.tenant_id, e.lifecycle_status, (e.advance_id IS NOT NULL) AS linked_to_advance, COUNT(*) AS expenses
FROM expense e WHERE e.expense_case_id IS NULL GROUP BY e.tenant_id, e.lifecycle_status, (e.advance_id IS NOT NULL) ORDER BY 1, 2;
SELECT '## VALID (not a defect): Cases with more than one advance in one currency' AS section;
SELECT a.tenant_id, HEX(c.expense_case_uuid) AS expense_case, c.lifecycle_status AS case_status, a.advance_currency,
       COUNT(*) AS advances, GROUP_CONCAT(a.lifecycle_status ORDER BY a.created_at) AS statuses
FROM expense_advance a JOIN expense_case c ON c.expense_case_id = a.expense_case_id AND c.tenant_id = a.tenant_id
GROUP BY a.tenant_id, c.expense_case_uuid, c.lifecycle_status, a.advance_currency HAVING COUNT(*) > 1 ORDER BY 1, 2;
SELECT '## rendition rows by status' AS section;
SELECT s.lifecycle_status, s.reconciliation_result, COUNT(*) AS settlements, SUM(s.justified_expense_total > 0) AS with_justified_total,
       SUM(s.returned_amount > 0) AS with_return, SUM(s.reimbursement_amount > 0) AS with_reimbursement, SUM(s.authorized_adjustment_total > 0) AS with_adjustment
FROM advance_settlement s GROUP BY s.lifecycle_status, s.reconciliation_result ORDER BY 1, 2;
SELECT '## TECHNICAL CARRIERS (not business truth): open rendition rows of Case advances that still hold a per-advance justified total' AS section;
SELECT a.tenant_id, s.lifecycle_status, COUNT(*) AS rows_with_justified_total
FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id AND a.tenant_id = s.tenant_id
WHERE s.lifecycle_status <> 'CERRADO' AND s.justified_expense_total > 0
  AND (a.expense_case_id IS NOT NULL OR EXISTS (SELECT 1 FROM expense_case c WHERE c.advance_id = a.advance_id AND c.tenant_id = a.tenant_id))
GROUP BY a.tenant_id, s.lifecycle_status;
SELECT '## Case-level impact: approved expenses linked to an advance outside that advance''s Case' AS section;
SELECT COUNT(*) AS advance_linked_expenses_outside_their_advance_case FROM expense e
JOIN expense_advance a ON a.advance_id = e.advance_id AND a.tenant_id = e.tenant_id
LEFT JOIN expense_case legacy ON legacy.advance_id = a.advance_id AND legacy.tenant_id = a.tenant_id
WHERE COALESCE(a.expense_case_id, legacy.expense_case_id) IS NOT NULL
  AND (e.expense_case_id IS NULL OR e.expense_case_id <> COALESCE(a.expense_case_id, legacy.expense_case_id));
SELECT '## Case-level impact: Cases whose delivered advances are all closed but whose approved total differs from the frozen rows' AS section;
SELECT COUNT(*) AS closed_cases_with_changed_justified FROM (
  SELECT c.expense_case_id, a.advance_currency, SUM(s.lifecycle_status = 'CERRADO') AS closed_rows, COUNT(*) AS delivered_count,
         COALESCE(SUM(CASE WHEN s.lifecycle_status = 'CERRADO' THEN s.justified_expense_total END), 0) AS closed_justified,
         (SELECT COALESCE(SUM(e.expense_amount), 0) FROM expense e WHERE e.expense_case_id = c.expense_case_id
            AND e.expense_currency = a.advance_currency AND e.lifecycle_status = 'APROBADO') AS approved
  FROM expense_case c
  JOIN expense_advance a ON a.tenant_id = c.tenant_id AND a.organization_scope = c.organization_scope
    AND (a.expense_case_id = c.expense_case_id OR (a.expense_case_id IS NULL AND c.advance_id = a.advance_id))
  LEFT JOIN advance_settlement s ON s.advance_id = a.advance_id AND s.tenant_id = a.tenant_id
  WHERE a.delivered_at IS NOT NULL AND a.lifecycle_status NOT IN ('BORRADOR', 'CANCELADO')
  GROUP BY c.expense_case_id, a.advance_currency
  HAVING closed_rows = delivered_count AND closed_justified <> approved) diffs;
SELECT '## Case-level positions of open Cases with delivered money (read only, per Case and currency)' AS section;
SELECT c.tenant_id, HEX(c.expense_case_uuid) AS expense_case, a.advance_currency AS currency,
       SUM(a.advance_amount) AS delivered,
       (SELECT COALESCE(SUM(e.expense_amount), 0) FROM expense e WHERE e.expense_case_id = c.expense_case_id
          AND e.expense_currency = a.advance_currency AND e.lifecycle_status = 'APROBADO') AS justified,
       COALESCE(SUM(s.returned_amount), 0) AS returned, COALESCE(SUM(s.reimbursement_amount), 0) AS reimbursed,
       COUNT(s.settlement_id) AS rows_opened, SUM(s.lifecycle_status = 'CERRADO') AS rows_closed
FROM expense_case c
JOIN expense_advance a ON a.tenant_id = c.tenant_id AND a.expense_case_id = c.expense_case_id
LEFT JOIN advance_settlement s ON s.advance_id = a.advance_id AND s.tenant_id = a.tenant_id
WHERE c.lifecycle_status = 'ABIERTO' AND a.delivered_at IS NOT NULL AND a.lifecycle_status NOT IN ('BORRADOR', 'CANCELADO')
GROUP BY c.tenant_id, c.expense_case_id, c.expense_case_uuid, a.advance_currency ORDER BY 1, 2;
SELECT '## totals' AS section;
SELECT (SELECT COUNT(*) FROM expense_case WHERE lifecycle_status = 'ABIERTO') AS open_cases,
       (SELECT COUNT(*) FROM expense_case WHERE lifecycle_status = 'CERRADO') AS closed_cases,
       (SELECT COUNT(*) FROM expense_advance) AS advances, (SELECT COUNT(*) FROM expense) AS expenses,
       (SELECT COUNT(*) FROM advance_settlement) AS settlements;

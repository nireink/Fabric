SELECT 'cases_with_delivered_advances' AS metric, COUNT(DISTINCT c.expense_case_id) AS value
FROM expense_case c
JOIN expense_advance a ON a.tenant_id = c.tenant_id AND a.organization_scope = c.organization_scope
  AND (a.expense_case_id = c.expense_case_id OR (a.expense_case_id IS NULL AND c.advance_id = a.advance_id))
WHERE a.delivered_at IS NOT NULL AND a.lifecycle_status NOT IN ('BORRADOR','CANCELADO')
UNION ALL
SELECT 'cases_all_delivered_rows_closed_justified_differs', COUNT(*) FROM (
  SELECT c.expense_case_id, a.advance_currency,
         SUM(s.lifecycle_status = 'CERRADO') AS closed_rows, COUNT(*) AS delivered_count,
         COALESCE(SUM(CASE WHEN s.lifecycle_status = 'CERRADO' THEN s.justified_expense_total END), 0) AS closed_justified,
         (SELECT COALESCE(SUM(e.expense_amount), 0) FROM expense e WHERE e.expense_case_id = c.expense_case_id
            AND e.expense_currency = a.advance_currency AND e.lifecycle_status = 'APROBADO') AS approved
  FROM expense_case c
  JOIN expense_advance a ON a.tenant_id = c.tenant_id AND a.organization_scope = c.organization_scope
    AND (a.expense_case_id = c.expense_case_id OR (a.expense_case_id IS NULL AND c.advance_id = a.advance_id))
  LEFT JOIN advance_settlement s ON s.advance_id = a.advance_id AND s.tenant_id = a.tenant_id
  WHERE a.delivered_at IS NOT NULL AND a.lifecycle_status NOT IN ('BORRADOR','CANCELADO')
  GROUP BY c.expense_case_id, a.advance_currency
  HAVING closed_rows = delivered_count AND closed_justified <> approved) diffs
UNION ALL
SELECT 'case_expenses_linked_to_an_advance', COUNT(*) FROM expense e WHERE e.expense_case_id IS NOT NULL AND e.advance_id IS NOT NULL
UNION ALL
SELECT 'open_case_rows_with_justified_total', COUNT(*) FROM advance_settlement s
JOIN expense_advance a ON a.advance_id = s.advance_id
WHERE s.lifecycle_status <> 'CERRADO' AND s.justified_expense_total > 0
  AND (a.expense_case_id IS NOT NULL OR EXISTS (SELECT 1 FROM expense_case c WHERE c.advance_id = a.advance_id));

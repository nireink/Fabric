SELECT 'case_expenses_with_advance_link' AS metric, COUNT(*) AS value FROM expense e WHERE e.expense_case_id IS NOT NULL AND e.advance_id IS NOT NULL
UNION ALL
SELECT 'case_expenses_with_advance_link_approved', COUNT(*) FROM expense e WHERE e.expense_case_id IS NOT NULL AND e.advance_id IS NOT NULL AND e.lifecycle_status = 'APROBADO'
UNION ALL
SELECT 'advance_linked_expenses_outside_their_advance_case', COUNT(*) FROM expense e
JOIN expense_advance a ON a.advance_id = e.advance_id
LEFT JOIN expense_case legacy ON legacy.advance_id = a.advance_id
WHERE COALESCE(a.expense_case_id, legacy.expense_case_id) IS NOT NULL
  AND (e.expense_case_id IS NULL OR e.expense_case_id <> COALESCE(a.expense_case_id, legacy.expense_case_id));

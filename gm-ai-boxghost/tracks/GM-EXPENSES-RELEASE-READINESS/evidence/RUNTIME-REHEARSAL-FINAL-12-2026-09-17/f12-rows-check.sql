SET SESSION TRANSACTION READ ONLY;
START TRANSACTION READ ONLY;
SELECT 'construccion' AS scope, COUNT(*) AS rows_count, SUM(s.lifecycle_status = 'CERRADO') AS closed_rows, SUM(s.justified_expense_total) AS justified, SUM(s.returned_amount) AS returned,
       SUM(s.advance_amount_snapshot + s.reimbursement_amount <> s.justified_expense_total + s.returned_amount + s.authorized_adjustment_total) AS unbalanced_rows,
       (SELECT COUNT(*) FROM settlement_balance_event b JOIN advance_settlement s2 ON s2.settlement_id = b.settlement_id JOIN expense_advance a2 ON a2.advance_id = s2.advance_id JOIN expense_case c2 ON c2.expense_case_id = a2.expense_case_id WHERE c2.expense_case_uuid = UUID_TO_BIN('c387f1c5-bfc0-4969-b00f-73303f0da2ed')) AS balance_events
FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id JOIN expense_case c ON c.expense_case_id = a.expense_case_id
WHERE c.expense_case_uuid = UUID_TO_BIN('c387f1c5-bfc0-4969-b00f-73303f0da2ed');
SELECT 'tramo_adicional' AS scope, COUNT(*) AS rows_count FROM advance_settlement s JOIN expense_advance a ON a.advance_id = s.advance_id JOIN expense_case c ON c.expense_case_id = a.expense_case_id WHERE c.expense_case_uuid = UUID_TO_BIN('c696a28b-cc59-4f72-bba4-1002b3ba9ccf');
SELECT 'all_reconciled_rows_violating_v63' AS scope, COUNT(*) AS n FROM advance_settlement WHERE reconciliation_result = 'RECONCILED' AND advance_amount_snapshot + reimbursement_amount <> justified_expense_total + returned_amount + authorized_adjustment_total;
SELECT 'flyway' AS scope, MAX(CAST(version AS UNSIGNED)) AS max_version, SUM(success = 0) AS failed FROM flyway_schema_history WHERE version IS NOT NULL;
ROLLBACK;

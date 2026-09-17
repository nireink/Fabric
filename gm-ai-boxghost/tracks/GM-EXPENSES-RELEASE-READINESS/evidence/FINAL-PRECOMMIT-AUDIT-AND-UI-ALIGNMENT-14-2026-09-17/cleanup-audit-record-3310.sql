-- GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14 §5 - audit of the STEP 13 DEV test-data cleanup through the EXISTING
-- global audit table audit_logs (V1 core baseline; actor key re-pointed to global user_accounts by V58).
-- Target: ONLY the isolated local runtime database gypport_runtime_local (127.0.0.1:3310). Never Shared DEV.
--
-- Facts used (PRE-COMMIT-ENV-UI-AUDIT-HARDENING-13-2026-09-17/known-test-expense-cleanup-3310-output.txt):
--   expense 5E63494AA2564C1E847CD54A6ED67A51, tenant 1, organization_scope 0
--   before OBSERVADO v2 (updated_at 2026-08-30 21:08:29.952, 0 review events); after RECHAZADO v3 (updated_at
--   2026-09-17 12:55:25.122, 0 review events); cleanup_at_utc 2026-09-17 12:55:25.123; ROWS_CHANGED=1.
-- Actor: the cleanup had no authenticated GYPPORT UserAccount. user_account_id stays NULL, the canonical system-event
--   semantics of audit_logs (GYPPORT_FINAL_CANONICAL_FOUNDATION_REGISTER_v1.0 §6.4). No actor is fabricated.
-- Time: created_at is the table default (the real time this audit record is written). The real cleanup time is carried in
--   new_values.regularization.performed_at_utc; nothing is backdated.
-- Action: audit_action_types was empty (no canonical code existed). The Owner-specified code
--   LEGACY_DEV_TEST_DATA_REGULARIZATION is registered once, as catalog data (no schema change, no migration).

SELECT CONCAT('TARGET database=', DATABASE(), ' now_utc=', UTC_TIMESTAMP(3)) AS target;
START TRANSACTION;

INSERT INTO audit_action_types (audit_action_code, audit_action_name, description, is_active)
SELECT 'LEGACY_DEV_TEST_DATA_REGULARIZATION', 'Regularización de dato de prueba heredado (DEV)',
       'Operación administrativa controlada sobre datos de prueba de DEV. No es un flujo del producto.', 1
FROM DUAL
WHERE DATABASE() = 'gypport_runtime_local'
  AND NOT EXISTS (SELECT 1 FROM audit_action_types WHERE audit_action_code = 'LEGACY_DEV_TEST_DATA_REGULARIZATION');
SELECT CONCAT('ACTION_TYPES_INSERTED=', ROW_COUNT()) AS action_type;

INSERT INTO audit_logs (audit_log_uuid, tenant_id, user_account_id, audit_action_type_id, entity_name, entity_id, entity_uuid,
                        entity_version, request_id, correlation_id, old_values, new_values, ip_address, user_agent)
SELECT UUID_TO_BIN('c24094e6-60c2-480a-88d8-c6cadbdeaba4'), e.tenant_id, NULL, t.audit_action_type_id, 'Expense', e.expense_id, e.expense_uuid,
       e.version, NULL, 'GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13',
       JSON_OBJECT('lifecycle_status', 'OBSERVADO', 'version', 2, 'updated_at', '2026-08-30 21:08:29.952', 'review_events', 0),
       JSON_OBJECT('lifecycle_status', 'RECHAZADO', 'version', 3, 'updated_at', '2026-09-17 12:55:25.122', 'review_events', 0,
           'regularization', JSON_OBJECT(
               'action', 'LEGACY_DEV_TEST_DATA_REGULARIZATION',
               'reason', 'Test record created before canonical review-history persistence.',
               'classification', 'LEGACY_DEV_TEST_DATA',
               'performed_at_utc', '2026-09-17T12:55:25.123Z',
               'performed_in', 'local isolated runtime database gypport_runtime_local (127.0.0.1:3310) only; Shared DEV unchanged',
               'execution_context', 'Guarded SQL known-test-expense-cleanup-3310.sql run through docker exec as MySQL user gypport_runtime_local by the Claude agent under the Owner-authorized STEP GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13 (section 17). No authenticated GYPPORT UserAccount took part: system event, empty actor.',
               'review_event_written', FALSE,
               'evidence', 'Fabric/gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/PRE-COMMIT-ENV-UI-AUDIT-HARDENING-13-2026-09-17/',
               'audit_recorded_by_step', 'GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14',
               'audit_recorded_after_the_operation', TRUE)),
       NULL, 'mysql client via docker exec gypport-runtime-local-mysql'
FROM expense e
JOIN audit_action_types t ON t.audit_action_code = 'LEGACY_DEV_TEST_DATA_REGULARIZATION'
WHERE DATABASE() = 'gypport_runtime_local'
  AND e.tenant_id = 1 AND e.organization_scope = 0
  AND e.expense_uuid = UNHEX('5E63494AA2564C1E847CD54A6ED67A51')
  AND e.lifecycle_status = 'RECHAZADO' AND e.version = 3
  AND NOT EXISTS (SELECT 1 FROM audit_logs a WHERE a.entity_uuid = e.expense_uuid AND a.audit_action_type_id = t.audit_action_type_id);
SELECT CONCAT('AUDIT_ROWS_INSERTED=', ROW_COUNT()) AS audit_row;

COMMIT;

SELECT CONCAT('AUDIT_LOG uuid=', BIN_TO_UUID(a.audit_log_uuid), ' tenant=', a.tenant_id, ' actor=', IFNULL(a.user_account_id, 'NULL'),
              ' action=', t.audit_action_code, ' entity=', a.entity_name, '#', a.entity_id, ' entity_uuid=', HEX(a.entity_uuid),
              ' entity_version=', a.entity_version, ' correlation=', a.correlation_id, ' created_at=', a.created_at,
              ' old_status=', JSON_UNQUOTE(JSON_EXTRACT(a.old_values, '$.lifecycle_status')), ' old_version=', JSON_EXTRACT(a.old_values, '$.version'),
              ' new_status=', JSON_UNQUOTE(JSON_EXTRACT(a.new_values, '$.lifecycle_status')), ' new_version=', JSON_EXTRACT(a.new_values, '$.version'),
              ' performed_at_utc=', JSON_UNQUOTE(JSON_EXTRACT(a.new_values, '$.regularization.performed_at_utc')),
              ' reason=', JSON_UNQUOTE(JSON_EXTRACT(a.new_values, '$.regularization.reason'))) AS audit_record
FROM audit_logs a JOIN audit_action_types t ON t.audit_action_type_id = a.audit_action_type_id
WHERE a.entity_uuid = UNHEX('5E63494AA2564C1E847CD54A6ED67A51');
SELECT CONCAT('TOTALS audit_logs=', (SELECT COUNT(*) FROM audit_logs), ' audit_action_types=', (SELECT COUNT(*) FROM audit_action_types),
              ' expense_review_event_for_row=', (SELECT COUNT(*) FROM expense_review_event r JOIN expense e ON e.tenant_id = r.tenant_id
                  AND e.organization_scope = r.organization_scope AND e.expense_id = r.expense_id
                  WHERE e.expense_uuid = UNHEX('5E63494AA2564C1E847CD54A6ED67A51'))) AS totals;

-- GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13 §12, §17, §18 - controlled DEV test-data cleanup.
-- Target: ONLY the isolated local runtime database gypport_runtime_local (container gypport-runtime-local-mysql,
-- published on 127.0.0.1:3310). Never Shared DEV (127.0.0.1:3308, core_business_dev).
--
-- Record: expense 5E63494AA2564C1E847CD54A6ED67A51 (tenant 1, PERSONAL, no Case), OBSERVADO without any review event.
-- Classification: LEGACY_DEV_TEST_DATA, observed by pre-history code (before gm-expenses 6f1b43f, 2026-09-03) that changed
-- the status without writing review history. Owner decision: final state RECHAZADO.
--
-- Why not the product path: Expense.rejectReview requires PENDIENTE_REVISION, and CorrectObservedExpenseUseCase refuses an
-- OBSERVADO expense without its OBSERVED event (MISSING_OBSERVATION_HISTORY). No canonical OBSERVADO -> RECHAZADO exists,
-- and none is added for this row.
--
-- What this does NOT do: it writes no expense_review_event row, fabricates no reviewer, no rejection date and no motive.
-- It is not business history; who, when and why are recorded in this STEP's BoxGhost evidence.
-- Guards: exact tenant/scope/uuid, expected status OBSERVADO and version 2, zero review events, and the database name.

SELECT CONCAT('TARGET database=', DATABASE(), ' server_now_utc=', UTC_TIMESTAMP(3)) AS target;

START TRANSACTION;

SELECT CONCAT('BEFORE expense=', HEX(e.expense_uuid), ' tenant=', e.tenant_id, ' organization_scope=', e.organization_scope,
              ' scope=', e.expense_scope, ' case_id=', IFNULL(e.expense_case_id, 'NULL'), ' advance_id=', IFNULL(e.advance_id, 'NULL'),
              ' status=', e.lifecycle_status, ' version=', e.version, ' amount=', e.expense_amount, ' ', e.expense_currency,
              ' expense_date=', e.expense_date, ' created_by=', e.created_by_user_account_id, ' created_at=', e.created_at,
              ' updated_at=', e.updated_at,
              ' review_events=', (SELECT COUNT(*) FROM expense_review_event r WHERE r.tenant_id = e.tenant_id
                                   AND r.organization_scope = e.organization_scope AND r.expense_id = e.expense_id),
              ' command_receipts=', (SELECT COUNT(*) FROM expense_command_receipt c WHERE c.tenant_id = e.tenant_id
                                   AND c.target_public_uuid = e.expense_uuid)) AS before_state
FROM expense e
WHERE e.tenant_id = 1 AND e.organization_scope = 0 AND e.expense_uuid = UNHEX('5E63494AA2564C1E847CD54A6ED67A51')
FOR UPDATE;

UPDATE expense e
SET e.lifecycle_status = 'RECHAZADO', e.version = e.version + 1
WHERE DATABASE() = 'gypport_runtime_local'
  AND e.tenant_id = 1 AND e.organization_scope = 0
  AND e.expense_uuid = UNHEX('5E63494AA2564C1E847CD54A6ED67A51')
  AND e.lifecycle_status = 'OBSERVADO' AND e.version = 2
  AND NOT EXISTS (SELECT 1 FROM expense_review_event r WHERE r.tenant_id = e.tenant_id
                  AND r.organization_scope = e.organization_scope AND r.expense_id = e.expense_id);

SELECT CONCAT('ROWS_CHANGED=', ROW_COUNT(), ' cleanup_at_utc=', UTC_TIMESTAMP(3)) AS changed;

SELECT CONCAT('AFTER expense=', HEX(e.expense_uuid), ' tenant=', e.tenant_id, ' status=', e.lifecycle_status, ' version=', e.version,
              ' amount=', e.expense_amount, ' ', e.expense_currency, ' updated_at=', e.updated_at,
              ' review_events=', (SELECT COUNT(*) FROM expense_review_event r WHERE r.tenant_id = e.tenant_id
                                   AND r.organization_scope = e.organization_scope AND r.expense_id = e.expense_id)) AS after_state
FROM expense e
WHERE e.tenant_id = 1 AND e.organization_scope = 0 AND e.expense_uuid = UNHEX('5E63494AA2564C1E847CD54A6ED67A51');

COMMIT;

SELECT CONCAT('OBSERVADO_WITHOUT_OBSERVED_EVENT_REMAINING=', COUNT(*)) AS remaining
FROM expense e
WHERE e.lifecycle_status = 'OBSERVADO'
  AND NOT EXISTS (SELECT 1 FROM expense_review_event r WHERE r.tenant_id = e.tenant_id
                  AND r.organization_scope = e.organization_scope AND r.expense_id = e.expense_id AND r.event_type = 'OBSERVED');

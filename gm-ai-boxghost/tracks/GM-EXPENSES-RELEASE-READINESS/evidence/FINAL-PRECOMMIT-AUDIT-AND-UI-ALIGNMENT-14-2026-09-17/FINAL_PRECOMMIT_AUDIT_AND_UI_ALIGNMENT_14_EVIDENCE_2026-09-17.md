# GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14 — evidence (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14
MODE=AUDIT_EXISTING_ARCHITECTURE_THEN_TARGETED_FINALIZATION
OWNER_AUTHORIZED=YES
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14.md
EXECUTED_BY=Claude (Opus 5) in the Claude desktop app, on the Owner's instruction
STATUS=READY_FOR_OWNER_FINAL_PRECOMMIT_REVIEW
```

Repository heads, unchanged: Gystigo d9f3dde, Modules/gm-expenses ab74610, Fabric 70fd250. Nothing was staged, committed or pushed, and Shared DEV was not modified (still V43).

## Part A — existing audit architecture

### What exists (`audit-architecture-verification.txt`)

- **`ExpenseAuditTrailPort`:** not found. There are no files in Gystigo, Modules or Fabric/Knowledge with that name (only this STEP's stored prompt), and it appears in no commit of gm-expenses, Gystigo or Fabric. It is not a current or past implementation.
- **Global / transversal audit table:** `audit_logs`, with its action catalog `audit_action_types`.
  - **Origin:** created by `Gystigo/database/core/migration/V1__core_business_baseline.sql` (also in the B17 baseline). V3 added the composite `fk_audit_logs_tenant_user`; V58 dropped it and kept `fk_audit_log_user` → `user_accounts(user_account_id)`, the global account.
  - **Columns:** `audit_log_id`, `audit_log_uuid` (UNIQUE), `tenant_id` (nullable, FK tenants), `user_account_id` (nullable, FK global accounts), `audit_action_type_id` (NOT NULL, FK catalog), `entity_name`, `entity_id`, `entity_uuid`, `entity_version`, `request_id`, `correlation_id`, `old_values` JSON, `new_values` JSON, `ip_address`, `user_agent`, and `created_at` (NOT NULL, database clock default).
  - **Catalog:** `audit_action_code` is UNIQUE, plus name, description and `is_active`.
  - **Actor semantics:** GYPPORT_FINAL_CANONICAL_FOUNDATION_REGISTER_v1.0 §6.4 says nullable `tenant_id` and nullable actor support system/global events, and that a NULL component preserves legitimate system-event semantics. The Universe data-domain context §13 defines the granularity to keep: actor + context + entity + before/after + request trace + technical evidence + time.
  - **Design:** ADR-0010 (Audit Log Architecture) is PROPOSED.
  - **Writers:** no application port, service, adapter or Host code writes `audit_logs`, and no trigger writes it.
  - **Protection:** the table has no append-only triggers.
  - **Rows before this STEP:** 0, and the catalog was also empty. That holds in both local 3310 and Shared DEV.
- **Domain histories (gm-expenses):** `expense_review_event`, `expense_revision_event`, `expense_advance_assignment_event`, `settlement_adjustment_event`, `settlement_balance_event`, `expense_document_review_event`, `expense_advance_participant_event` and `expense_command_receipt`. All exist, and every one has BEFORE UPDATE and BEFORE DELETE refusal triggers.
- **Review history model:** described in the domain baseline §4, "Review history integrity" (STEP 13).
- **Revision history model:**
  - The domain returns `ExpenseRevisionChange(previous, newDetails)` from `editRegistered` and `correctObserved`.
  - `EditRegisteredExpenseUseCase` writes `EDITED_BEFORE_REVIEW`. `CorrectObservedExpenseUseCase` writes `CORRECTION_SUBMITTED` and `CORRECTED_AFTER_OBSERVATION`. Both are `@Transactional` and idempotency-guarded.
  - `expense_revision_event` keeps `revision_number`, `revision_type`, `reason`, `previous_snapshot` / `new_snapshot` JSON, `triggering_review_event_id`, `resulting_review_event_id`, `performed_by_user_account_id` and `occurred_at`.
  - The only expense writers are Register, Submit, Accept, Observe, Reject, EditRegistered and CorrectObserved. `Expense.linkAdvance`, `unlinkAdvance`, `reassignAdvance`, `freezeAdvanceReference` and `reopenApproved` have no production caller, so no mutation path lacks history.
- **Actor source for all histories:** `AuthenticatedPrincipal.userAccountId` from the validated session, then `AuthenticatedRequestContext.actorUserAccountId`, then `CommandContext.actorUserId`. Time: `Instant.now()` in the Host bridge (server clock). No business participant is ever the audit actor.

### Split preserved

Business history stays in the semantic tables, and administrative/system operations use `audit_logs`. No domain event is copied into `audit_logs`: the new real-DB test checks that the count is unchanged after an edit, submit, observe and correct flow. No new audit architecture, table, column or V64 was created.

**Audit gaps:** none blocks the MVP. Every business question (who, when, what, why, before/after for material changes) is answered by the domain histories and the command receipts. Non-blocking observations:
- `audit_logs` has no application writer yet (ADR-0010 PROPOSED).
- `audit_logs` has no append-only triggers.
- The catalog has only the one local code created below.

### Audit of the STEP 13 DEV cleanup (local 3310 only)

- **Facts used:** `PRE-COMMIT-ENV-UI-AUDIT-HARDENING-13-2026-09-17/known-test-expense-cleanup-3310-output.txt`.
  - Expense 5E63494AA2564C1E847CD54A6ED67A51, tenant 1.
  - Before: OBSERVADO v2, updated_at 2026-08-30 21:08:29.952, 0 review events.
  - After: RECHAZADO v3, updated_at 2026-09-17 12:55:25.122.
  - `cleanup_at_utc` 2026-09-17 12:55:25.123; one row changed.
  - The cleanup ran as guarded SQL through docker exec, as MySQL user `gypport_runtime_local`, by the Claude agent under the Owner-authorized STEP 13. No authenticated GYPPORT UserAccount was involved.
- **Action code:** the catalog was empty, so no canonical code existed. The Owner-specified code `LEGACY_DEV_TEST_DATA_REGULARIZATION` ("Regularización de dato de prueba heredado (DEV)") was registered once in `audit_action_types`, as catalog data only: no schema change, no migration.
- **Record** (`cleanup-audit-record-3310.sql`, `-output.txt`):
  - `audit_log_uuid` c24094e6-60c2-480a-88d8-c6cadbdeaba4, `tenant_id` 1.
  - `user_account_id` NULL: the system-event semantics of §6.4. No actor was fabricated.
  - Action `LEGACY_DEV_TEST_DATA_REGULARIZATION`; entity `Expense` #2 (uuid 5E63494A…, version 3); `correlation_id` GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13.
  - `old_values` {lifecycle_status OBSERVADO, version 2, updated_at, review_events 0}.
  - `new_values` {lifecycle_status RECHAZADO, version 3, updated_at, review_events 0, regularization: action, reason "Test record created before canonical review-history persistence.", classification LEGACY_DEV_TEST_DATA, performed_at_utc 2026-09-17T12:55:25.123Z, performed_in, execution_context, review_event_written false, evidence path, audit recorded by STEP 14 after the operation}.
  - `user_agent` "mysql client via docker exec gypport-runtime-local-mysql".
  - `created_at` 2026-09-17 13:36:19: the real time the audit record was written. The operation time is carried in the payload, and nothing is backdated.
- **After:** `audit_logs`=1, `audit_action_types`=1, and still 0 review events for the row (none invented). Shared DEV is unchanged (`audit_logs`=0, catalog 0, V43).
- **Not added:** no `LEGACY_OBSERVED_REGULARIZED` workflow event and no UI flow.

### Frozen behavior (new and kept tests)

`ExpenseReviewHistoryIntegrityHttpApiTest` has 4 tests, still in the real-DB runner:
- A–C: observe → OBSERVADO with its OBSERVED event; actor = account; time inside the request window.
- D: a MySQL failure on the OBSERVED insert rolls the whole transaction back; E and F follow.
- G: tenant isolation.
- New (§2/§8): edit and correction write `expense_revision_event` rows 1 and 2.
  - Row 1 is `EDITED_BEFORE_REVIEW`, 40 → 42.
  - Row 2 is `CORRECTED_AFTER_OBSERVATION`, 42 → 45, reason kept, triggering OBSERVED and resulting CORRECTION_SUBMITTED.
  - The actor is the account on both rows.
  - The database refuses UPDATE and DELETE on both history tables, and `audit_logs` is unchanged by business flows.

**Results:** Host real-DB 103/103 (`host-realdb-result.json`, `host-realdb-surefire-summary.txt`; Flyway 63, 17 delete guards, 8 categories, container and evidence disposed). The gm-expenses module is unchanged in this STEP (748/748 in STEP 13, reused).

## Part B — tracked safe local launcher (`tracked-launcher-verification.txt`)

- **Canonical home:** `Gystigo/platform_os/server/scripts/`, the existing tracked scripts folder of the Host module.
  - It now holds `start-runtime-local.ps1` (SHA-256 20f37f0e…) and `stop-runtime-local.ps1` (c13bb248…).
  - The old copies in `target/runtime-local` were deleted, so one launcher remains.
  - Runtime state stays in `target/runtime-local`.
- **Contract:** ENV=LOCAL_EDUARDO, DB_HOST=127.0.0.1, DB_PORT=3310, DB_NAME=gypport_runtime_local.
  - The password is read from the `gypport-runtime-local-mysql` container at launch; no secret sits in the tracked file, and no Windows variable is used.
  - Only the four lines are displayed before Java.
  - The same mandatory guard and message apply.
- **Guard:** 5/5 Shared DEV mutants refused with no Java start. The control passed and displayed only the four lines.
- **Switch-over:** the tracked stop script stopped PID 47236, and the tracked launcher started PID 2460 through WMI.
  - Connections: 10 to 3310, 0 to 3308.
  - Schema 63, up to date, 0 errors.
  - `/auth/me` 401, `POST /auth/login {}` 401.
  - Local V63, Shared DEV V43.
- **Clean survival:** the real Maven wrapper ran offline against a disposable replica of the module. `mvn clean` deleted `target/`, including the fake runtime state, and both scripts survived byte-identical. The scripts are not git-ignored.

## Part C — Case card semantic layout (`studio-case-card-layout-verification.txt`)

- **Conciliado:** a Case-lifecycle indicator, one per Case (`caseReconciled(open, rows)`: closed and every currency settled). It sits in the card header under the Abierto / Cerrado status, above the Finanzas divider, and reads 100% on a full bar or Pendiente on an empty bar.
- **Uso:** a Finanzas metric, one per currency (`caseUsage(row)`), with its own bar in Finanzas column 4 next to Entregado · Usado · Justificado. The text keeps the real value and the fill is clamped.
- **Never combined:** HARDENING_13's indicator column (`expense-case-card__indicators` / `__currency`) is removed.
- **Owner examples:**
  - Compra Teléfono (Cerrado, Conciliado 100%; Uso 87%).
  - Viaje Loja (Cerrado, Conciliado 100%; Uso 29%).
  - Open overuse (Abierto, Conciliado Pendiente; Uso 110%, bar full).
- **Tests:** Studio 630/630, ESLint clean.
- **Browser, at 1280, 768, 375 and 320 px:** document overflow 0, 0 cards overflowing, 20 Conciliado and 21 Uso indicators, 0 misplaced, 0 hidden. Conciliado always sits above the divider, under the status and right-aligned with it; Uso always sits inside Finanzas.

## Part D — frozen review integrity

- `ObserveExpenseReviewUseCase` is unchanged: expense → OBSERVADO and the OBSERVED insert happen in one transaction; the actor is the authenticated global UserAccount and the time is the server clock.
- The real-DB rollback test is kept and passes.

## Canonical documentation

- **`Reglas.md`:** three entries appended (d8d00c92 → 93bbca67, existing text byte-identical).
  1. Reuse of the existing audit (Universe);
  2. canonical tracked local launcher (Universe, complementing the STEP 13 environment rule);
  3. placement of Conciliado and Uso (gm-expenses), which explicitly supersedes HARDENING_13's placement.
  - The STEP 13 rules on atomic OBSERVADO + OBSERVED and on the local environment were not duplicated.
- **gm-expenses domain baseline:** §4 "Expense revision history"; §5 card indicators and their placement (earlier text kept as superseded).
- **gm-expenses persistence baseline:** §10.1, the two complementary audit layers.
- **`Gystigo/docker/README.md`:** the canonical launcher path, and what `mvn clean` removes.

## Files changed by this STEP

- **Gystigo** (uncommitted):
  - Studio: `ExpenseCaseCard.jsx`, `caseRules.js`, `ExpenseCases.css`, `fixtures/ExpenseCaseCardsFixture.jsx` (comment), `ExpenseCaseCard.contract.mjs`, `ExpenseCases.contract.mjs`.
  - Server: `scripts/start-runtime-local.ps1` (new), `scripts/stop-runtime-local.ps1` (new), `ExpenseReviewHistoryIntegrityHttpApiTest.java` (4th test).
  - Docs: `docker/README.md`.
- **Fabric** (uncommitted): the step prompt, `Reglas.md`, `CURRENT_STEP.md`, the gm-expenses domain and persistence baselines, and this evidence folder.
- **Not versioned:**
  - `target/runtime-local` (old launcher copies deleted).
  - Local DB 3310: one `audit_action_types` row and one `audit_logs` row.
- **gm-expenses:** no change. Backend main code: no change. Migrations: none.

## Observations and Owner decisions (non-blocking)

- **Local expense documents:** they live in `target/runtime-local/documents`, which `mvn clean` would delete: the 11 DEV evidence files copied in FIX_01, 3.2 MB. Moving them, for example to the gitignored `Gystigo/.gypport/`, is an Owner decision that was not taken here.
- **`audit_logs`:** writing it from the application (an audit port) and adding append-only triggers are future Owner decisions. Neither is needed for the MVP.
- **Action code scope:** `LEGACY_DEV_TEST_DATA_REGULARIZATION` exists only in the local 3310 catalog. When the audit catalog is seeded canonically, decide whether this code belongs to it.

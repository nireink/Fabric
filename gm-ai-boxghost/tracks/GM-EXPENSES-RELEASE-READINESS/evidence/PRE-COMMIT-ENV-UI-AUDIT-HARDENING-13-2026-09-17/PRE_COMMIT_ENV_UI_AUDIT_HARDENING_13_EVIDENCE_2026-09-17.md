# GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13 — evidence (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13
MODE=AUDIT_FIRST_THEN_TARGETED_IMPLEMENTATION
OWNER_AUTHORIZED=YES
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13.md
EXECUTED_BY=Claude (Opus 5) in the Claude desktop app, on the Owner's instruction
STATUS=READY_FOR_OWNER_PRE_COMMIT_HARDENING_REVIEW
```

Repository heads, unchanged: Gystigo d9f3dde, Modules/gm-expenses ab74610, Fabric 70fd250. Nothing was staged, committed or pushed, and Shared DEV was not modified.

## Part A — local environment safety

### Audit (read only; secrets reported only as PRESENT / ABSENT / equality)

| Scope | SPRING_DATASOURCE_URL | USERNAME | PASSWORD |
|---|---|---|---|
| Process (this app) | `jdbc:mysql://127.0.0.1:3308/core_business_dev` | PRESENT | PRESENT |
| User (HKCU\Environment) | `jdbc:mysql://127.0.0.1:3308/core_business_dev` | PRESENT (= DEV backend container user, = `root`) | PRESENT (= DEV MySQL root password, = DEV backend container password) |
| Machine (HKLM) | ABSENT | ABSENT | ABSENT |

- **Ownership:** clearly Shared-DEV-specific. The URL is Shared DEV, and the username and password are Shared DEV's root credentials. The same values stay in the gitignored `Gystigo/docker/.env`, which DEV compose interpolation falls back to, and in the DEV containers. Removing them loses nothing.
- **Other scopes:** no Machine value, no `JAVA_TOOL_OPTIONS` / `JDK_JAVA_OPTIONS` / `_JAVA_OPTIONS`, no `SPRING_APPLICATION_JSON`. No shell profile, `~/.m2/settings.xml` or JetBrains/VS Code settings reference Shared DEV. VS Code's local-history caches mention the strings, but they are not configuration.
- **Project references:**
  - `Gystigo/docker/compose.yaml` and `.env`: DEV-scoped, legitimate for the official DEV stack. The container URL is `mysql:3306/core_business_dev`.
  - `application.yaml`: `${SPRING_DATASOURCE_*}` without defaults, so an unset environment fails fast.
  - `server/pom.xml`: Surefire excludes the variables.
  - Test runners and guards (`run-host-isolated-db-tests.ps1`, `run-expenses-real-db-tests.ps1`, `IsolatedTestDatabaseGuard*`, `ExpensesTestDatabaseGuard*`): refuse or strip Shared DEV.
  - Docs:
    - `Gystigo/docker/README.md` instructed setting the three variables for the Windows backend with `localhost:3308`, which is how the global variables came to exist. It was updated.
    - `docs/testing/TEST_DATABASE_ISOLATION.md` described the global variables. It was updated.
  - No IDE launch configurations exist (`.claude/launch.json` files contain no datasource).
- Evidence: `env-scope-audit-before-removal.txt`, `plain-process-env-probe-before-removal.txt`.

### Correction

- **2026-09-17T12:50:28Z:** removed `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME` and `SPRING_DATASOURCE_PASSWORD` from the Windows User scope (registry value deleted, WM_SETTINGCHANGE broadcast) and cleared them from the executing process. Machine scope was not touched and had nothing.
- **Plain process proof:** a process created through WMI gets its environment from the registry. Before the removal it showed `PLAIN_SHELL_INHERITS_SHARED_DEV=YES`; after, `NO`.
  - Already-running processes keep their old environment until restarted. That includes the Claude desktop app and its tool shells, terminals, IDEs and the Studio Vite server.
- **Hardened launcher** `Gystigo/platform_os/server/target/runtime-local/start-runtime-local.ps1` (copy: `start-runtime-local.hardened.ps1`):
  - Explicit, process-local configuration: `ENV=LOCAL_EDUARDO`, `DB_HOST=127.0.0.1`, `DB_PORT=3310`, `DB_NAME=gypport_runtime_local`.
  - The password is still read from the `gypport-runtime-local-mysql` container at launch (the existing safe mechanism) and is never printed or placed on the command line.
  - Before Java starts, it displays only ENV, DB_HOST, DB_PORT and DB_NAME.
  - The mandatory guard throws `Local runtime refused to start because the datasource points to Shared DEV.` when the resolved datasource or the values Java receives contain `:3308`, `gypport-mysql-dev` or `core_business_dev`. It checks:
    - the configuration itself;
    - the JVM option variables;
    - the database name inside the runtime container;
    - whether `gypport-mysql-dev` is the container published on 127.0.0.1:3310;
    - a final look at the exact environment and arguments handed to Java.
  - Inherited `SPRING_*` variables are still removed from the launcher process.
- **Guard mutation tests** (`launcher-guard-mutation-tests.txt`, `.ps1`):
  - 5/5 refused with the exact message: port 3308, host `gypport-mysql-dev`, database `core_business_dev`, a `localhost:3308` URL, and a Shared DEV `JAVA_TOOL_OPTIONS`.
  - None displayed configuration lines, and no Java process started.
  - The control run with the real configuration passed every guard and displayed only the four lines.

### Verification (`local-runtime-verification-2026-09-17T1253Z.txt`)

- **Restart:** the backend was restarted with the hardened launcher through WMI (fresh environment). PID 47236 listens on 127.0.0.1:8080 with jar `gystigo-host-runtime-ecd17c12f8af.jar`; backend main code is unchanged.
- **Connections:** 10 established to 3310, 0 to 3308.
- **Log:**
  - Flyway `jdbc:mysql://127.0.0.1:3310/gypport_runtime_local`, schema 63, up to date, no migration.
  - 0 ERROR lines, and 0 lines mentioning Shared DEV.
- **HTTP:** `GET /auth/me` → 401; `POST /auth/login {}` → 401 (reachable); CORS preflight from 5173 → 200.
- **Databases:** local V63 (47 rows, 0 failed). Shared DEV V43 (27 rows, 0 failed, last installed 2026-09-10), unchanged. `gypport-backend-dev` is still stopped.

## Part B — two independent Case card indicators (Studio only)

- **Rule** (`caseRules.caseCardIndicators`): `reconciled = closed && nothing pending`, and `usage = round(used / delivered × 100)`, or 0 without a delivered amount.
- **Card** (`ExpenseCaseCard.jsx`): per currency, the amounts are followed by a column holding the two indicators, Conciliado above Uso, each with its own compact track.
  - Conciliado reads `100%` on a full track, or `Pendiente` on an empty track.
  - Uso reads its real percentage, and the fill is clamped at 100%.
  - The layout is the same for open and closed Cases. FIX_10's single bar, its plain "Uso" figure and the dashed inactive capsule were removed.
- **CSS** (`ExpenseCases.css`):
  - Desktop: an amounts grid of 3 columns plus an indicator column.
  - At ≤ 600 px: amounts in 2 columns, the position row full width, and the indicators side by side.
- **Owner examples:**
  - A: Compra Teléfono, closed. Conciliado 100% (full) and Uso 87% (87%).
  - B: Viaje Loja, closed. Conciliado 100% and Uso 29%, on two bars.
  - C: open 1000/1100. Conciliado Pendiente (empty) and Uso 110% (full track, text kept).
  - D: no delivered advance. Uso 0% (empty), and open cards read Conciliado Pendiente.
- **Contracts:** `ExpenseCaseCard.contract.mjs` and `ExpenseCases.contract.mjs` were updated. The Studio suite passes 629/629 and ESLint is clean. The fixture's scenario A is renamed "Compra Teléfono".
- **Responsive** (`studio-dual-indicators-verification.txt`): at 1280, 768, 375 and 320 px, document overflow is 0 px, 0 cards overflow, and all 42 indicators are visible with correct fills.

## Part C — OBSERVADO review-history integrity

### Root cause and current code

- **Production paths into OBSERVADO:** exactly one, `ObserveExpenseReviewUseCase` (`Expense.observeReview`, PENDIENTE_REVISION → OBSERVADO).
  - `Expense.reopenApproved` (APROBADO → OBSERVADO) has no production caller.
  - No migration or other SQL writer sets OBSERVADO: `JdbcExpenseCaseRepository.linkExpense` only sets `expense_case_id`.
- **Trace:**
  1. `POST /api/expenses/{id}/observe` (`ExpenseController.observe`, permission `expenses.expense.review`).
  2. `ExpensesRequestContextBridge.toCommandContext`: the actor is `AuthenticatedRequestContext.actorUserAccountId`, which is `AuthenticatedPrincipal.userAccountId` from the validated session (global UserAccount). The time is `Instant.now()` (server system clock).
  3. The `@Transactional ObserveExpenseReviewUseCase.execute`, a CGLIB-proxied Spring bean from `GmExpensesConfig`, runs under Boot's DataSourceTransactionManager.
  4. Inside it: `IdempotencyGuard.execute`, which catches nothing, then `expense.observeReview(reason)`, then `JdbcExpenseRepository.save` (UPDATE with version check, `NamedParameterJdbcOperations`), then `JdbcExpenseReviewEventRepository.save` (INSERT OBSERVED, same template and transaction; a failure becomes the runtime `RepositoryAccessException`), then the receipt.
  5. The exception leaves the proxy, so everything rolls back. The controller then maps it to 500 outside the transaction.
- **Result:** `CURRENT_CODE_CAN_CREATE_OBSERVED_WITHOUT_HISTORY=NO`. This is proven by test D below.
- **Known row** `5E63494AA2564C1E847CD54A6ED67A51` (tenant 1, PERSONAL, no Case, USD 20.00):
  - It has 0 review events of any kind.
  - Its command receipts show RegisterExpense v0 at 21:08:18, SubmitExpenseForReview v1 at 21:08:21 and ObserveExpenseReview v2 at 21:08:29 on 2026-08-30, all by account 1 (`known-test-expense-command-receipts-3310.txt`).
  - Review events were first written by gm-expenses `6f1b43f` on 2026-09-03. Before it, `ObserveExpenseReviewUseCase` saved the status only (`git show 6f1b43f^`).
  - The first review event in the database is dated 2026-09-03 11:57.
  - **Classification: LEGACY_DEV_TEST_DATA.** No legacy product workflow was added.

### Audit fields (`review-history-schema-audit-3310.txt`)

- **expense:**
  - `tenant_id` NOT NULL; `organization_id` with generated `organization_scope`.
  - `created_by_user_account_id` NOT NULL; `created_at` datetime(3) DB default.
  - `updated_at` datetime(3) ON UPDATE (DB-maintained); `version`.
  - No `updated_by`.
- **expense_review_event:**
  - `expense_review_event_id`, `tenant_id` NOT NULL, `organization_id`/`organization_scope`.
  - `expense_id` NOT NULL, with a composite tenant-safe FK to `expense`.
  - `event_type` NOT NULL, CHECK-listed.
  - `performed_by_user_account_id` NOT NULL (actor).
  - `occurred_at` datetime(3) NOT NULL (server clock).
  - `reason` varchar(500) (catalog code; CHECK requires it for OBSERVED/REJECTED).
  - `notes` varchar(1000) (detail).
  - `settlement_id` and `amends_review_event_id` for settlement-scoped events.
  - Append-only triggers `trg_review_event_no_update` / `trg_review_event_no_delete`.
  - No separate `created_at`/`source` column.
- **Genuine gaps, reported only; no columns were added and none is a release blocker:**
  1. No DB-recorded insertion time next to the application's `occurred_at`. That time comes from the server clock, never the client.
  2. No `updated_by` on `expense`. Every business change carries its actor in its own append-only event table (review, revision, allocation, assignment, participant, document review), and the command receipt keeps `executed_by_user_account_id` and `executed_at`.
  - Not a gap: actor columns have no FK to `user_accounts`. That is the accepted gm-expenses MVP design (no cross-module FKs; ADR-0014 keeps it with no retrofit).
  - `audit_logs` exists but has no writer in current code, so it was not used.

### Modern tests (synthetic @example.test accounts, fresh isolated MySQL)

- **New class** `Gystigo/platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseReviewHistoryIntegrityHttpApiTest.java`:
  - It is deliberately non-transactional, so each request commits or rolls back on its own. It was added to `run-expenses-real-db-tests.ps1` and `docs/testing/GM_EXPENSES_REAL_DB_TESTS.md`.
  - **A–C:** submit → observe gives OBSERVADO with events [SUBMITTED, OBSERVED]. `performed_by_user_account_id` equals the session's account, `occurred_at` falls inside the request window, and the reason/notes are stored as sent.
  - **D:** a test-only MySQL trigger refuses the OBSERVED insert (SQLSTATE 45000, seen in the log).
    - The response is 500 and the expense stays PENDIENTE_REVISION at the same version.
    - Events stay [SUBMITTED], and no idempotency receipt is written.
    - After the trigger is dropped, the same operationId succeeds.
  - **E:** the correction then works. **F:** a rejection is final (observe and correct refused), with history [SUBMITTED, OBSERVED, CORRECTION_SUBMITTED, REJECTED].
  - **G:** another tenant gets 404 on observe and on read, and nothing is written.
- **Existing coverage:** E and F are also covered by `ExpenseCaseHttpApiTest` (`observedExpenseIsCorrectedAndApprovedKeepingItsWholeReviewHistory`, `rejectedExpenseIsFinalAndKeepsItsDecisionOnRecord`), and pre-history refusal by `preHistoryObservedExpenseIsRefusedCleanlyNeverWithAServerError`.
- **Results:**
  - Host real-DB 102/102 (`host-realdb-result.json`, `host-realdb-surefire-summary.txt`; Flyway 63, 17 delete guards, 8 categories, container and evidence disposed).
  - gm-expenses module 748/748 (`gm-expenses-module-tests-summary.txt`).

### Known test expense regularization (local 3310 only) — DEV cleanup evidence, not product history

- **Canonical path:** it does not allow OBSERVADO → RECHAZADO. `rejectReview` requires PENDIENTE_REVISION, and `CorrectObservedExpenseUseCase` refuses an OBSERVADO expense without its OBSERVED event. No transition was added.
- **Mechanism:** `known-test-expense-cleanup-3310.sql`, one guarded UPDATE in a transaction.
  - Guards: exact tenant, scope and uuid; status OBSERVADO; version 2; zero review events; `DATABASE() = 'gypport_runtime_local'`.
  - It ran through `docker exec gypport-runtime-local-mysql`, after the binding was checked as 127.0.0.1:3310.
- **Before:** OBSERVADO v2, updated_at 2026-08-30 21:08:29.952, 0 review events, 3 command receipts.
- **After:** RECHAZADO v3, updated_at 2026-09-17 12:55:25.122 (DB time of the action), 0 review events. `OBSERVADO_WITHOUT_OBSERVED_EVENT_REMAINING=0` (`known-test-expense-cleanup-3310-output.txt`).
- **Who:** Claude (Opus 5), executing this STEP's §17 on the Owner's explicit authorization. It was not an authenticated product action, so nothing in the product history names an actor for it.
- **When:** 2026-09-17T12:55:25.123Z.
- **Why:** Owner decision. It is a pre-history test row that is no longer useful as an unresolved OBSERVADO blocker; preferred final state RECHAZADO.
- **Not done:** no review event, no fabricated reviewer, rejection motive or historical date, no Shared DEV change.
  - Shared DEV still holds the row as OBSERVADO v2.
  - Its cleanup belongs to a separate, explicit DEV cleanup STEP after the release migration.
- **Side effect** (expected, local copy only): tenant 1's August 2026 period reports stop counting this USD 20.00 as used, because a rejected expense is never spent money. The row has no Case, so no Case card changes.

## Canonical documentation

- **`Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md`:** three entries appended. The existing content is byte-identical, SHA-256 prefix c369f581 → d8d00c92.
  1. environment safety rule;
  2. independent Conciliado/Uso indicators, which explicitly supersedes FIX_10's single bar;
  3. review-history integrity, with the cleanup recorded as DEV evidence.
- **`Fabric/Knowledge/gm-expenses/01-domain/GYPPORT_GM_EXPENSES_DOMAIN_BASELINE_v1.0.md`:** §4 "Review history integrity"; §5 card indicators (FIX_10 text kept as superseded).
- **Gystigo docs:** `docker/README.md` (never global variables; local runtime; Shared DEV only process-scoped), `docs/testing/TEST_DATABASE_ISOLATION.md`, `docs/testing/GM_EXPENSES_REAL_DB_TESTS.md`.

## Files changed by this STEP

- **Gystigo** (uncommitted):
  - Studio: `ExpenseCaseCard.jsx`, `caseRules.js`, `ExpenseCases.css`, `fixtures/ExpenseCaseCardsFixture.jsx`, `ExpenseCaseCard.contract.mjs`, `ExpenseCases.contract.mjs`.
  - Server: `ExpenseReviewHistoryIntegrityHttpApiTest.java` (new), `scripts/run-expenses-real-db-tests.ps1`.
  - Docs: `docker/README.md`, `docs/testing/GM_EXPENSES_REAL_DB_TESTS.md`, `docs/testing/TEST_DATABASE_ISOLATION.md`.
- **Fabric** (uncommitted): the step prompt, `Reglas.md`, `active-work/CURRENT_STEP.md`, the gm-expenses domain baseline, and this evidence folder.
- **Not versioned:**
  - `start-runtime-local.ps1` lives in the gitignored `target/runtime-local`, so `mvn clean` would delete it. The copy kept here can restore it.
  - Windows User environment (three variables removed).
  - Local DB 3310 (one test row regularized).
- **gm-expenses:** no change. Backend main code: no change. Migrations: none.

## Pre-existing debt and observations

- The local runtime launcher and its runtime folder live under the gitignored `target/`.
- Running applications still hold the removed variables until restarted. That includes the Claude desktop app, terminals, IDEs and the Studio Vite server. New processes do not inherit them.
- The card fixture shell logs one 401 resource error (no backend session), unrelated to the card.

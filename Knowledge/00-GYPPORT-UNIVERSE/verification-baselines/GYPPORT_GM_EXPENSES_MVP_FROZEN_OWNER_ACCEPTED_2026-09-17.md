# GYPPORT — GM-EXPENSES MVP FROZEN OWNER-ACCEPTED Baseline

**Baseline ID:** `GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17`  
**Status:** `FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL`  
**Date:** 2026-09-17  
**Step:** `GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28`  
**Phase:** `MVP_FREEZE`  
**Supersedes:** `GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17`

## Purpose

This is the frozen, Owner-accepted state of the gm-expenses MVP: the committed source, the Shared DEV schema it runs
on, the numbering model and the financial semantics the Owner accepted in the real application. From this baseline on,
an MVP architecture or UI change needs a new explicit track; new ideas go to the backlog, post-MVP or the next release
(Reglas.md, 2026-09-17, "MVP de gm-expenses congelado").

Future STEPs classify their impact on it as REUSE, PARTIAL_INVALIDATION or FULL_INVALIDATION under:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/VERIFIED_BASELINE_REUSE.md
```

It supersedes the MVP-RELEASE baseline as a PARTIAL_INVALIDATION: the four source commits after that baseline change
the 46 files listed below, which were verified again; every other file of the MVP-RELEASE manifest is untouched and
keeps its evidence.

This document follows the generator's template but was written by hand: the Owner fixed its id, and
`Fabric/tools/verification/New-GypportVerifiedBaseline.ps1` accepts only ids of the form
`GYPPORT-<SUBJECT>-VERIFIED-BASELINE-<date>`.

## Baseline record

```text
BASELINE_ID=GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
STATUS=FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL
STEP=GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28
PHASE=MVP_FREEZE
DATE=2026-09-17
MIGRATION_HEAD=V65
SHARED_DEV_FLYWAY=65
VERIFIED_FILE_COUNT=46
SUPERSEDES_BASELINE_ID=GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
BASELINE_REUSE_ALLOWED=YES
GM_EXPENSES_MVP_STATUS=FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL
PUSH_PERFORMED=NO
```

## Accepted commits

```text
GM_EXPENSES_HEAD=39a2adf4dfff0196208a1f80719be1c12c047ac2
GYSTIGO_HEAD=5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc
FABRIC_HEAD=the local Fabric closure commit that adds this document
```

Parent commits and branches:

```text
gm-expenses=874a3e5071e46b179444730089d34afa5fe0e742 (master)
Gystigo=0293ff45e94b2ebbec67e792fea28e7b80bc8901 (feature/gm-fleets-minimum-vehicle-master-01)
Fabric=1f5bed831c54d01efe74444f02ee2b2d947df549 (main)
```

The commits since the superseded baseline:

```text
gm-expenses 874a3e5 feat(expenses): case business number and reconciliation semantics
gm-expenses 39a2adf feat(expenses): permanent expediente sequence per tenant
Gystigo     0293ff4 feat(expenses): expense case business number in the API, V64 and Studio
Gystigo     5eed5d6 feat(expenses): permanent expediente numbering in V65, the API and Studio
Fabric      018ea84 docs(expenses): record the gm-expenses MVP closure and commit gate
Fabric      1f5bed8 docs(expenses): record the V64 deployment and the permanent expediente numbering
Fabric      the closure commit that adds this document (STEP 27 and STEP 28 evidence, this baseline, Reglas, CURRENT_STEP)
```

The Fabric closure commit is found with:

```text
git -C Fabric log --diff-filter=A --format=%H -- Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_GM_EXPENSES_MVP_FROZEN_OWNER_ACCEPTED_2026-09-17.md
```

## Accepted commit manifest

Secondary evidence read from git, one line per file changed since the superseded baseline:
`<status> <abbreviated blob id at the frozen head> <path>`, paths relative to the repository.

```text
gm-expenses 545eae0..39a2adf4dfff0196208a1f80719be1c12c047ac2 files=22
A 3633af2d1a11 src/main/java/com/gypport/business/expenses/casefile/application/BusinessDatePort.java
A 02c76532bdeb src/main/java/com/gypport/business/expenses/casefile/application/CaseNumberSequencePort.java
M e97a3381157f src/main/java/com/gypport/business/expenses/casefile/application/CaseRenditionLedger.java
M b8f53816a7a2 src/main/java/com/gypport/business/expenses/casefile/application/CaseRenditionService.java
M 926194295953 src/main/java/com/gypport/business/expenses/casefile/application/ExpenseCaseService.java
A 6336ab74e931 src/main/java/com/gypport/business/expenses/casefile/application/ExpenseSequencePort.java
A d9551899a014 src/main/java/com/gypport/business/expenses/casefile/domain/CaseNumber.java
M 8f311ab5a7e9 src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseCase.java
M acd80a71b9da src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseCaseFinancialSummary.java
A e7375f6300d9 src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseSequence.java
A e00fe7a8a066 src/main/java/com/gypport/business/expenses/casefile/infrastructure/persistence/jdbc/JdbcCaseNumberSequenceRepository.java
M effe5366024a src/main/java/com/gypport/business/expenses/casefile/infrastructure/persistence/jdbc/JdbcExpenseCaseRepository.java
A ad8a3275e581 src/main/java/com/gypport/business/expenses/casefile/infrastructure/persistence/jdbc/JdbcExpenseSequenceRepository.java
M 703e0dc05217 src/main/java/com/gypport/business/expenses/settlement/application/SettlementBalanceEventRepository.java
M fb562e92fc5a src/main/java/com/gypport/business/expenses/settlement/domain/AdvanceSettlement.java
M 5650e54fed0f src/main/java/com/gypport/business/expenses/settlement/domain/SettlementBalanceChange.java
A 40b9afd0e296 src/main/java/com/gypport/business/expenses/settlement/domain/SettlementBalanceEvent.java
M 296952cd35ff src/main/java/com/gypport/business/expenses/settlement/infrastructure/persistence/jdbc/JdbcSettlementBalanceEventRepository.java
M 07fcaea9d9b6 src/test/java/com/gypport/business/expenses/casefile/application/CaseRenditionServiceTest.java
A 38719cf92a2b src/test/java/com/gypport/business/expenses/casefile/domain/CaseNumberTest.java
A fe1764159e9d src/test/java/com/gypport/business/expenses/casefile/domain/ExpenseSequenceTest.java
M a101a48a2527 src/test/java/com/gypport/business/expenses/settlement/domain/AdvanceSettlementTest.java

Gystigo bcb9591..5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc files=24
A a5b33da98479 database/modules/gm-expenses/migration/V64__gm_expenses_case_business_number.sql
A 80bbf42af4ca database/modules/gm-expenses/migration/V65__gm_expenses_case_permanent_sequence.sql
M c42bf0370219 platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseCaseController.java
M 83abd1f19ebb platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensesResponseFormatting.java
A 1eea4dde6760 platform_os/server/src/main/java/com/gypport/server/module/expenses/TenantBusinessDateResolver.java
M e793e2436b95 platform_os/server/src/main/java/com/gypport/server/shared/config/ExpenseCaseConfig.java
M cdbcf0925880 platform_os/server/src/main/resources/application.yaml
M 7736089e9b92 platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseCaseHttpApiTest.java
M 89405a4eb236 platform_os/studio/channel/browser/shell/fixtures/ExpenseCaseCardsFixture.jsx
A 080afac08390 platform_os/studio/channel/browser/shell/fixtures/ExpenseCaseDetailFixture.jsx
A c7f1a5b45a1b platform_os/studio/channel/browser/shell/fixtures/expense-case-detail.html
M d0cce12165a0 platform_os/studio/channel/browser/shell/src/application/expenses/cases/ChooseCaseForAdvancePage.jsx
M 735103c5e02c platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseCard.jsx
M f475b3a584c8 platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseDetailPage.jsx
M 63192d0d7f64 platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseListPage.jsx
M b00fd7858a46 platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCases.css
M 7fd2c03eff3b platform_os/studio/channel/browser/shell/src/application/expenses/cases/caseRules.js
M 70a9cb3b79a7 platform_os/studio/channel/browser/shell/src/application/expenses/cases/renditionRules.js
M 09a164784642 platform_os/studio/channel/browser/shell/src/application/expenses/expenseService.js
M 2183b7103fba platform_os/studio/verification/contracts/browser/AdvanceRenditionFlow.contract.mjs
M 58ffd940de88 platform_os/studio/verification/contracts/browser/ExpenseCaseCard.contract.mjs
M c327b58761e0 platform_os/studio/verification/contracts/browser/ExpenseCaseListNumbering.contract.mjs
M ab2303b9fc1d platform_os/studio/verification/contracts/browser/ExpenseCases.contract.mjs
M 3610cc3c93da platform_os/studio/verification/contracts/browser/ExpenseOperationIdBoundary.contract.mjs
```

## Verification evidence

```text
OWNER_ACCEPTANCE=GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28, in the real application at http://localhost:5173
OWNER_NUMBERING_VISUAL_ACCEPTED=YES
OWNER_LAYOUT_VISUAL_ACCEPTED=YES
REVERSAL_EXECUTED_BY_OWNER=YES   REVERSAL_RESULT=SUCCESS
REIMBURSEMENT_TEST=DEFERRED   SYNTHETIC_DEV_DATA_DECISION=KEEP
FULL_HISTORICAL_REGRESSION_RERUN=NO
MVP_RELEASE_BASELINE_IMPACT=PARTIAL_INVALIDATION
MVP_RELEASE_BASELINE_IMPACT_REASON=the four source commits after it change 46 files (V64, V65, the case business number, the permanent EXP. NN, Total a conciliar and the reverso), verified again by the suites below; the rest of its manifest is untouched
GM_EXPENSES_MODULE_SUITE=780/780 (STEP 25; reused at the STEP 26 gate, the newest source older than the green run)
HOST_REAL_DB_EXPENSES_SUITE=107/107 at Flyway 65, 0 failures, 0 errors, 0 skipped (STEP 25, disposable real database; the tested module jar is class-identical to the build from 39a2adf, 261 of 261 classes)
STUDIO_CONTRACTS=652/652 with ESLint clean (STEP 25A; reused at the STEP 26 gate)
V64_SHA256=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21
V65_SHA256=8ed3c20b1b45af4f832623992882612f4fe78d8327b31d8cb3a90a245e1962b4
V65_REHEARSAL=PASS (V64 -> V65 through the Host's own Flyway on a copy of Shared DEV, plus the eight-racer permanent-sequence test)
SHARED_DEV_DEPLOYMENTS=V43 -> V63 (STEP 18), V63 -> V64 (STEP 24), V64 -> V65 (STEP 27); each by the application's own Flyway from an image built from git-archive exports of the committed heads, with the official backend stopped first; 0 failed
BACKUP_PRE_V64=core_business_dev-pre-v64-20260917T200210.sql sha256 0f5fbd0ee6c2e7815d57a95c4a1947e7d06ce0bce41977a13aeb95bdab2505b1 (restore-validated)
BACKUP_PRE_V65=core_business_dev-pre-v65-20260917T222529.sql sha256 ffd4abb7674f5a4f268bad0198016cdfc62bd7ea7151326d84c7796e3263482e (restore-validated)
BACKUP_LOCATION=%LOCALAPPDATA%\Temp\gypport\shared-dev-backups, outside every repository; both files hashed again at the freeze and unchanged
DEPLOYED_IMAGE=gystigo-backend:4.1.0-java25-gm-expenses-v65-5eed5d6 sha256:f44f598a5a786ab4f91a0d1b42fcfb1ee803a819f680c51cd11513a702d6533e
DEPLOYED_ARTIFACT_SHA256=8c438d5da7de3f84329810ed1d9481f597fbc178229f859305381915f207baf8 (66 packaged migrations, highest V65)
DEPLOYED_CONTAINER=gypport-backend-dev 445046e2801e, started 2026-09-18T03:31:46Z, 0 restarts at the freeze
V65_MIGRATION_RESULT=35/35 Cases numbered, 0 duplicates, 0 order mismatches, 11 tenants with 11 counter rows, financial checksums identical
STEP27_SMOKE=27/27, 0 HTTP 5xx; STEP27_REVERSAL_CAPABILITY=12/12 (synthetic tenants, the same container)
OWNER_CASE_REVERSAL=RETURN_REVERSED 35 -> 29 (USD 200.00) and 36 -> 30 (USD 100.00); user_account 1; 2026-09-18 04:04:03.129 UTC; reason "Actulizacion"; originals kept
OWNER_CASE_POSITION=Total anticipos 320.00 | Total gastos 400.00 | Total a conciliar 80.00 Por reembolsar | Devuelto 0.00 | Reembolsado 0.00 | Pendiente 80.00 Por reembolsar | Usado 400.00 | Uso 125%
FINAL_SMOKE=29/29, 0 failures, 0 writes (STEP 28, read-only, after the Owner's reverso)
EVIDENCE=Fabric/gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/ SHARED-DEV-V64-DEPLOYMENT-24-2026-09-17, PERMANENT-EXPEDIENTE-SEQUENCE-V65-25-2026-09-17, V65-EXP-DISPLAY-CORRECTION-25A-2026-09-17, V65-CONTROLLED-COMMIT-GATE-26-2026-09-17, V65-SHARED-DEV-DEPLOYMENT-27-2026-09-17, OWNER-FINAL-SMOKE-AND-FREEZE-28-2026-09-17
```

## Final numbering model

```text
UUID=technical resource identifier and the API route (/api/expense-cases/{uuid}); a business number is not a route (400)
EXP_NN=expense_sequence: permanent per tenant, in real creation order, never reset, immutable (trigger), UNIQUE (tenant_id, expense_sequence), allocated by the server from expense_case_permanent_sequence inside the creating transaction
EXP_DISPLAY=EXP. NN with at least two digits, never truncated (1 -> EXP. 01, 100 -> EXP. 100)
ID=case_number YYYYMMDD####, a stored generated column from case_business_date and case_sequence
CASE_SEQUENCE=daily per TENANT + BUSINESS_DATE; it composes the ID only and never decides EXP
BUSINESS_DATE=persisted at creation from the tenant time zone, else gypport.business.default-zone (America/Guayaquil)
REAL_DATA=EXP. 08: Compra Filtro, ID 202609170001; EXP. 09: VIAJE QUITO, ID 202609170002 (the Owner tenant numbers its nine Cases 01..09)
```

## Final financial semantics

```text
TOTAL_ANTICIPOS=delivered advances: every advance that is not BORRADOR or CANCELADO
TOTAL_GASTOS=APROBADO expenses of the Case
TOTAL_A_CONCILIAR=Total anticipos - Total gastos, a positive amount with its direction: Por devolver / Por reembolsar / Balanceado
DEVUELTO / REEMBOLSADO=real cash movements, net of their reversos
PENDIENTE=delivered + reimbursed - justified - returned - authorized adjustments (RN-001), a positive amount with its direction: Por justificar o devolver / Por reembolsar / Pendiente de conciliar
USADO=every expense that is not RECHAZADO or EXCLUIDO; an operational metric that never decides a direction
USO=Usado / Total anticipos, the real percentage, on the card
RECHAZADO=final, weighs zero in every total
MOVEMENT_CORRECTION=an authenticated reverso appends RETURN_REVERSED or REIMBURSEMENT_REVERSED naming the original event; never an edit, a delete or SQL
MOVEMENT_DISPLAY=the events of one command (same type, instant, actor and reason) are one movement; a reversed movement stays listed, marked Reversado
CARD_AND_DETAIL=the same server financialSummary: the list builds every card with the same service.detail and format as the detail
```

## Architecture invariants

```text
EXPENSE_CASE=center of funding and rendition
ADVANCES_PER_CASE=MULTIPLE_VALID
RENDITION=CASE_LEVEL, one per currency
RECONCILE_REQUIRES_CASE_BALANCE_ZERO=YES
CLOSE_CASE_CLOSES=every reconciled rendition row and every advance of the Case, in the same transaction
RETURN_AND_REIMBURSEMENT_COEXIST=YES (V63 unified equation)
BALANCE_EVENTS=append-only ledger settlement_balance_event: the audit record of every movement and reverso (actor, instant, reason, reverses_balance_event_id)
ONE_REVERSO_PER_ORIGINAL=YES (UNIQUE uq_set_balance_single_reversal on reverses_balance_event_id, and the service refuses a second one)
REVERSO_ON_CERRADO=refused; a reverso reopens the rendition (EN_CONCILIACION / PENDING) and the Case is reconciled again
REGISTRAR_REEMBOLSO_OFFERED=open Case, a delivered advance, a rendition not CERRADO, a positive pending reimbursement and no authorized adjustment
EXPENSES_HISTORY=append-only (BEFORE UPDATE or DELETE guards)
GLOBAL_AUDIT_LOGS_WRITER=NOT_IMPLEMENTED (ADR-0010 PROPOSED); no parallel audit architecture
CARD_CONCILIADO=one per Case in the header; CARD_USO=one per currency in Finanzas
FINAL_MIGRATION_HEAD=V65
```

## Unrelated WIP exclusions

Never staged by this track and preserved as they are:

```text
Gystigo (5): README.md deletion; studio AuthPage.css; onboarding/ShortRegisterPage.jsx; fixtures/HeaderBrandingFixture.jsx and fixtures/header-branding.html
Fabric (10): Knowledge/AI/; Knowledge/Architecture/GYPPORT_REGLAS_CANONICAS_ARQUITECTURA_DOMINIO_UIX.md; Knowledge/Derived/; Knowledge/Security/; Knowledge/UIX/; Knowledge/gm-accounting/; Knowledge/gm-expenses/03-application/, 04-integration/, 05-implementation/ and README.md
gm-expenses: none (clean worktree)
```

## Known pre-existing debts

```text
KNOWN_PREEXISTING_FAILURES=0
KNOWN_NON_BLOCKING_DEBT=ERROR_DISPATCH_404_MASKED_AS_401 for unmapped routes; expenses endpoints return their own 404
KNOWN_NON_BLOCKING_DEBT=audit_logs has no application writer (ADR-0010 PROPOSED); expense movements are audited in their own append-only ledger
KNOWN_NON_BLOCKING_DEBT=Spring's UserDetailsServiceAutoConfiguration still prints a generated development password at every Host start; promoted logs carry the notice without the password line (0 tokens in the STEP 24 and 27 migration logs)
KNOWN_NON_BLOCKING_DEBT=Shared DEV keeps 19 synthetic @example.test accounts in 18 isolated tenants from the smokes of STEPs 18/24/27 and earlier QA; the Owner decided KEEP
KNOWN_NON_BLOCKING_DEBT=the Shared DEV backups live under %LOCALAPPDATA%\Temp, outside every repository; moving them to GYPPORT_STORAGE (Restricted) awaits an Owner decision
KNOWN_NON_BLOCKING_DEBT=STEP 18 (Shared DEV V43 -> V63) has no stored prompt or evidence folder in Fabric; its facts survive in the STEP 19 prompt and the 20A and 22B records
KNOWN_NON_BLOCKING_DEBT=reports keep Entregado / Usado / Justificado until the Owner decides whether they follow the card vocabulary (Reglas.md, 2026-09-17)
KNOWN_NON_BLOCKING_DEBT=Shared DEV legacy data not regularized (1 OBSERVADO expense without its event, 3 CERRADO settlements on EN_RENDICION advances, drafts and orphans), a separate Owner STEP
KNOWN_NON_BLOCKING_DEBT=the Case and settlement API still return the raw closedBy account id; Studio never displays it
KNOWN_NON_BLOCKING_DEBT=Studio shell topbar reaches 336px at a 320px viewport (shell layout)
KNOWN_NON_BLOCKING_DEBT=PersonIdentityReconciliationHttpTest and GmFleetsHttpApiTest pin 127.0.0.1:3310, the local runtime database port
KNOWN_NON_BLOCKING_DEBT=gm-operational-resources and gm-banking integrations are later foundations
KNOWN_NON_BLOCKING_DEBT=BoxGhost evidence folders and stored prompts are missing for the early track STEPs (reconciliation 01 to STEP 06); their decisions live in Reglas.md
RESOLVED_SINCE_MVP_RELEASE=the stale official DEV backend image: rebuilt from committed exports in STEPs 18, 24 and 27
```

## Reuse contract

```text
BASELINE_FOUND=YES
BASELINE_ID=GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
BASELINE_REUSE_DECISION=REUSE|PARTIAL_INVALIDATION|FULL_INVALIDATION
BASELINE_REUSE_REASON=<short evidence-based reason>
```

REUSE means `FULL_HISTORICAL_REGRESSION_RERUN=NO`: the new STEP runs only its own tests, impact-selected tests and the
required integration smoke. A complete historical regression is never selected merely "to be safe".

## Baseline invalidation triggers

- any change to the MVP's architecture or UI - which the freeze admits only through a new explicit track
- a migration after V65 that touches expense_case numbering (expense_sequence, case_number, case_sequence,
  case_business_date, their counters or triggers) or the expense, advance, settlement or balance-event tables
- EXP. NN read from anything but expense_sequence, a daily sequence shown as EXP, or a permanent number that resets
- a change to Total a conciliar, Pendiente and its direction, Usado, Uso, or the zero weight of RECHAZADO
- a movement that can be edited or deleted, more than one reverso per original, or a reverso on a CERRADO rendition
- the card and the detail reading different financial sources
- Cerrar expediente no longer closing the reconciled rows and advances in one transaction, or Conciliar accepting a
  non-zero Case balance
- a Shared DEV schema that differs from Flyway 65 as deployed in STEP 27

An invalidation does not by itself require a full rerun: impact analysis selects the smallest sufficient
verification scope.

## Closeout

```text
STATUS=FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL
WRITTEN_BY=hand, in the generator's template (the Owner-fixed id is outside the generator's id pattern)
OWNER_ACCEPTANCE=recorded in STEP 28: numbering and layout on screen, the authenticated reverso, reimbursement deferred, synthetic data kept
AUTO_START_NEXT_STEP=NO
PUSH_PERFORMED=NO
NEXT_ACTION=the Owner authorizes the push of gm-expenses, Gystigo and Fabric when desired
```

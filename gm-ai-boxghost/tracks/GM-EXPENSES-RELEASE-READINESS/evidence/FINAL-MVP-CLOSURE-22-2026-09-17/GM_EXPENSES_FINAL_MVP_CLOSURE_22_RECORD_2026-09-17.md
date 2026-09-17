# GM_EXPENSES_FINAL_MVP_CLOSURE_22 — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_FINAL_MVP_CLOSURE_22
MODE=AUDIT_CURRENT_WIP -> IMPLEMENT_FINAL_REQUIREMENTS -> VERIFY -> V64_REHEARSAL -> PREPARE_CONTROLLED_COMMIT_GATE
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_FINAL_MVP_CLOSURE_22.md
STATUS=READY_FOR_OWNER_FINAL_REVIEW
SHARED_DEV_MODIFIED=NO   OWNER_CASE_MODIFIED=NO   V64_CREATED=YES (working tree only)   DEV_MIGRATION_HEAD=V63
FILES_STAGED=0  COMMITS_CREATED=0  PUSH_PERFORMED=NO
```

## 1. §39 — dirty worktree audit

Full path-by-path table: `dirty-worktree-classification.md` (same folder).

```text
TOTAL_DIRTY_PATHS=65   UNKNOWN=0   FILES_STAGED=0
STEP_22 (ID Gasto)=14
STEP_20/20A/21 (financial semantics, movement UX, reverso, card and detail)=24
STEP_19/20/21/22 (Fabric canonical records and evidence)=12
PRE_EXISTING_WIP (other tracks, excluded on purpose, untouched)=15
```

The excluded WIP is Gystigo's deleted `README.md` (last commit 54bdacd, 2026-07-28), the onboarding `AuthPage.css` and
`ShortRegisterPage.jsx` (2026-08-29), the branding fixture (2026-08-30) and ten untracked Fabric knowledge paths
(2026-08-07 to 2026-09-10). Every one of them predates this STEP series and none was opened, read into, moved or
cleaned by it.

## 2. The financial model (carried from STEPs 20, 20A and 21, re-verified here)

```text
TOTAL_ADVANCES=SUM(delivered advances)            a delivered advance keeps counting in every later state
TOTAL_EXPENSES=SUM(APROBADO)                      never approved - rejected
REJECTED_EXPENSE_FINANCIAL_EFFECT=ZERO            RECHAZADO and EXCLUIDO also stay out of Usado
BASE_RECONCILIATION_BALANCE=TOTAL_ADVANCES - TOTAL_EXPENSES    shown as "Total a conciliar"
REAL_RETURN / REAL_REIMBURSEMENT=only from an explicit registered movement
PENDIENTE=delivered + reimbursed - justified - returned - adjustments (RN-001), with its direction as a caption
```

The Owner's own Case, as the Owner's business facts describe it (320 delivered, 400 approved, one 200 rejected that
weighs nothing, no real cash movement): Total anticipos USD 320.00 · Total gastos USD 400.00 · Total a conciliar
USD 80.00 Por reembolsar · Devuelto USD 0.00 · Reembolsado USD 0.00 · Pendiente USD 80.00 Por reembolsar · Usado
USD 400.00. Both surfaces of the acceptance fixtures show exactly that.

## 3. ID Gasto — implemented (B, previously blocked)

```text
SEQUENCE_SCOPE=TENANT + BUSINESS_DATE            (Owner supersession; establishment NOT required)
FORMAT=YYYYMMDD####  (0001..9999)                 example 202609170001
UNIQUENESS=(tenant_id, case_number) and (tenant_id, case_business_date, case_sequence)
BUSINESS_DATE=persisted at creation; tenant time_zone, else gypport.business.default-zone (Host property)
ECUADOR_HARDCODED_IN_GM_EXPENSES=NO               the module only receives a business date through BusinessDatePort
GENERATION=persistent counter row, advanced inside the creating transaction; no MAX()+1, no memory counter,
           no UI, no UUID transformation, no SRI document_sequences
IMMUTABLE=case_business_date, case_sequence, case_number (database trigger)
UUID_ROUTE=unchanged; GET /api/expense-cases/{caseNumber} is refused
FULL_REFERENCE=RUC-ESTABLISHMENT-CASE_NUMBER, derived and optional; never on the card
```

Where it is proved:

```text
DOMAIN   CaseNumberTest (format, 0001..9999 refusal above and below, equality)
DOMAIN   ExpenseCaseServiceTest: everyCaseTakesTheNextNumberOfItsTenantAndBusinessDate, theNumberNeedsNothingFiscal
HOST     everyCaseIsBornWithItsBusinessNumberAndKeepsItsUuidRoute - 0001 then 0002, Fecha and number read the same day,
         list item == detail for the same Case, the number is not a route, another tenant counts its own day
HOST     theNumberSequenceSurvivesAConcurrentRaceAndWhatItAssignedIsImmutable - 8 threads on their own connections run
         the very statement the creation transaction runs: 8 distinct allocations 1..8, counter = 8, and the database
         refuses to move an assigned number
STUDIO   ExpenseCaseCard.contract §27 (identity group) and §38 (no ID Gasto invented when the API sends none),
         AdvanceRenditionFlow.contract §32 (detail shows it, and CARD_CASE_NUMBER == DETAIL_CASE_NUMBER)
```

## 4. V64 rehearsal on a disposable copy of the current Shared DEV

Full log: `v64-rehearsal-result.txt` (same folder). Shared DEV itself was only read (`mysqldump --single-transaction`).

```text
COPY=current Shared DEV bytes at V63, restored into a throwaway MySQL 8.4.10 container, deleted afterwards
V64_APPLIED=YES
FINANCIAL_TABLES_UNCHANGED=YES  (CHECKSUM TABLE identical before and after for expense, expense_advance,
                                 advance_settlement, settlement_balance_event, expense_review_event,
                                 expense_command_receipt)
BACKFILLED_CASES=30   CASES_WITHOUT_NUMBER=0   DUPLICATE_NUMBERS=0   DUPLICATE_SEQUENCES=0
DATE_MATCHES_CREATED_UTC=30 of 30   NUMBER_MATCHES_PARTS=30 of 30
COUNTER_ROWS=13   MAX_GAP=0
OWNER_CASE=202609170001 (Compra Filtro), fecha 2026-09-17
DUPLICATE_NUMBER_REFUSED=YES   NUMBER_IMMUTABLE=YES   COUNTER_ALLOCATES=1 then 2   OVERFLOW_REFUSED=YES
TRIGGERS=32 -> 34   TABLES=107 -> 108
```

## 5. Header hierarchy and the two surfaces

```text
GROUP_1_IDENTITY=EXP. NN: nombre / Fecha / ID Gasto
GROUP_2_ASSIGNMENT=Responsable / Supervisor / Recurso asignado, with Conciliado on its right rail
GROUP_3_FINANCE=Total anticipos · Total gastos · Total a conciliar · Uso, then Devuelto · Reembolsado · Pendiente,
                then Usado
SEPARATORS=spacing and a subtle rule; no nested cards
CARD_HEADER_NUDGED=NO (the STEP 15 alignment is untouched: the identity row carries the gap, a ::before draws the rule)
UUID_ON_THE_CARD=NO   FULL_REFERENCE_ON_THE_CARD=NO
```

Verified in the browser on the acceptance fixtures (`fixtures/expense-case-cards.html` and the new
`fixtures/expense-case-detail.html`, both synthetic, no backend):

```text
WIDTH  CARD                                   DETAIL
1280   ID Gasto: 202609170001, overflow 0     Fecha + ID Gasto on the identity line, overflow 0
768    ID Gasto: 202609170001, overflow 0     overflow 0
375    ID Gasto: 202609170001, overflow 0     overflow 0
320    ID Gasto: 202609170001, overflow 0     overflow 0
```

## 6. Verification

```text
GM_EXPENSES_MODULE=773 tests, 0 failures, 0 errors, 0 skipped (85 classes)
STUDIO_CONTRACTS=644 tests in 53 files, 0 failures; ESLint clean
HOST_EXPENSES_REAL_DB=106 tests, 0 failures, 0 errors, 0 skipped; flywayMax=64; container and evidence disposed
   result.json: host-expenses-realdb-result.json (same folder)
```

## 7. Runtime reality

```text
WORKING_TREE_API_SUPPORTS_CASE_NUMBER=YES
RUNNING_DEV_API_SUPPORTS_CASE_NUMBER=NO
   deployed image gystigo-backend:4.1.0-java25-gm-expenses-mvp-bcb9591, built from commits that predate this work
   Shared DEV read-only check: FLYWAY_MAX=63, case_business_date/case_sequence/case_number columns=0,
   expense_case_number_sequence table=0, cases=30, balance events=14
```

The Owner's live Case therefore still shows the old values in DEV; nothing about it was corrected, hidden or deleted,
and the USD 300 stored return remains exactly as STEP 21 audited it. The Owner corrects it after deployment through the
reverso, so the real actor and instant are recorded.

## 8. Still open for the Owner

```text
OWNER_DECISION_REQUIRED=controlled commit gate (three repositories, nothing staged yet)
OWNER_DECISION_REQUIRED=Shared DEV migration to V64 and the rebuild of the DEV backend from the new commits
OWNER_DECISION_REQUIRED=the correction of the live Case's USD 300 return through the reverso, after deployment
PRE_EXISTING_DEBT=the full business reference (RUC-ESTABLISHMENT-CASE_NUMBER) stays unavailable while Shared DEV holds
                  0 RUC identifiers, 0 tax subjects and 0 establishments; the ID Gasto does not depend on it
NEW_REGRESSION=none observed
```

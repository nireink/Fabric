# GM_EXPENSES_FINAL_CASE_CARD_NUMBERING_ALIGNMENT_22A — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_FINAL_CASE_CARD_NUMBERING_ALIGNMENT_22A
MODE=AUDIT_CURRENT_IMPLEMENTATION -> APPLY_OWNER_NUMBERING_RULE -> VERIFY
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_FINAL_CASE_CARD_NUMBERING_ALIGNMENT_22A.md
STATUS=READY_FOR_OWNER_FINAL_VISUAL_ACCEPTANCE
SHARED_DEV_MODIFIED=NO   OWNER_CASE_MODIFIED=NO   NEW_MIGRATION=NO   V64_MODIFIED=NO   DEV_MIGRATION_HEAD=V63
FILES_STAGED=0  COMMITS_CREATED=0  PUSH_PERFORMED=NO
```

## 1. Audit before touching anything (§5)

```text
API_HAS_CASE_NUMBER=YES      (list and detail, since STEP 22)
API_HAS_BUSINESS_DATE=YES    (list and detail, since STEP 22)
API_HAS_CASE_SEQUENCE=NO  -> added here, from the persisted CaseNumber.sequence(); no new column, no new migration
STUDIO_EXP_SOURCE_BEFORE=list position (page * pageSize + index + 1), in caseListSequence()
STUDIO_EXP_SOURCE_AFTER=the Case's own caseSequence, in caseSequenceOf()
```

One `format(...)` builds both the list item and the detail, so the new field reaches both surfaces at once.

## 2. What changed

```text
HOST     ExpenseCaseController.format(): json caseSequence beside caseNumber and businessDate
STUDIO   caseRules.js: caseListSequence() removed; caseSequenceOf(), caseTitle() and caseIdentityConsistent() added
STUDIO   ExpenseCaseCard.jsx: takes the Case only - no sequence prop; label "ID:" instead of "ID Gasto:"
STUDIO   ExpenseCaseListPage.jsx: renders Cases, numbers nothing
STUDIO   ChooseCaseForAdvancePage.jsx: each option reads the Case's own heading
STUDIO   ExpenseCaseDetailPage.jsx: label "ID:"
FIXTURES both acceptance fixtures carry caseSequence beside caseNumber
DOCS     CaseNumber javadoc, expenseService and ChooseCase comments, domain baseline, Reglas.md (append-only)
```

The compatibility path (§6): when a deployed API sends `caseNumber` without `caseSequence`, the last four digits are
read as the sequence. It is never the canonical source - the backend's own field wins whenever it is present - and a
Case with neither field shows no EXP and no ID at all.

## 3. Single source, proved

```text
STUDIO §1  SINGLE_SEQUENCE_SOURCE: EXP reads caseSequence, ID reads caseNumber, the list position feeds neither
STUDIO §4  minimum two digits, never truncated: 1 -> EXP. 01, 9 -> EXP. 09, 27 -> EXP. 27, 100 -> EXP. 100
STUDIO §23 sorting and filtering do not renumber: [A1, B2, C3] re-sorted to [C, A, B] still reads 03, 01, 02, and
           filtering down to B alone still reads EXP. 02
STUDIO §24 daily reset: 2026-09-17 #1 and 2026-09-18 #1 both read EXP. 01 and keep ID 202609170001 / 202609180001
STUDIO §25 consistency invariant: sequence 1 vs 202609170001 is consistent, sequence 2 vs 202609170007 is not, and
           Studio prints both values as they arrived instead of quietly repairing them
STUDIO     list contract rewritten: page 2 shows Cases 3, 2 and 1 of their day as EXP. 03, 02, 01 - never 21, 22, 23
HOST       caseSequence is 1 then 2 for the day, the list item carries the same sequence as the detail, and the
           number ends with that same sequence
STUDIO §32 detail and card show one identity: EXP. 01, Fecha 2026-09-17 and ID 202609170001 on both
```

## 4. Card and detail, verified in the browser

Acceptance fixtures (synthetic, no backend): `fixtures/expense-case-cards.html`, `fixtures/expense-case-detail.html`.

```text
CARD    EXP. 01: Compra Filtro | Fecha: 2026-09-17 | ID: 202609170001 | divider | Responsable / Supervisor /
        Recurso asignado with Conciliado on its rail | divider | Finanzas
CARDS   the fixture's other Cases read their own day's sequence, so EXP. 01 recurs across days by design
        (202609170001, 202609130001, 202609160002, 202609160001, 202609120001, 202609110001)
DETAIL  Compra Filtro | Fecha: 2026-09-17 | ID: 202609170001, same financial block as the card
WIDTHS  1280 / 768 / 375 / 320 - no horizontal overflow on either surface; EXP and ID readable at every width
FINANCE 320.00 | 400.00 | 80.00 Por reembolsar | Uso 125% | 0.00 | 0.00 | 80.00 Por reembolsar | Usado 400.00
```

## 5. Verification

```text
GM_EXPENSES=773/773 (rerun; a javadoc changed in the module)
STUDIO=648/648 in 53 files (rerun; 644 before, +5 new numbering tests, -1 superseded page-numbering test)
ESLINT=PASS (rerun)
HOST_EXPENSES_REAL_DB=106/106, flywayMax=64 (rerun; the Host payload changed)
V64_REHEARSAL=PASS, reused from STEP 22 - no migration, schema or backfill byte changed in this STEP
CONCURRENT_SEQUENCE_TEST=PASS, part of the 106 rerun
```

## 6. Frozen on purpose

```text
V64=untouched (case_business_date, case_sequence, case_number; scope TENANT + BUSINESS_DATE)
FINANCIAL_FORMULAS=untouched (advances = delivered, expenses = APROBADO, rejected = zero, base = advances - expenses)
OWNER_FIXTURE=320 / 400 / 80 Por reembolsar / 0 / 0 / 80 Por reembolsar / 400 / 125%
CARD_HEADER_LAYOUT=the STEP 14/15 alignment: Responsable, Supervisor, Recurso asignado and Conciliado unmoved,
                   Uso one visual unit in Finanzas with its clamped bar
SHARED_DEV=V63, untouched; the Owner's live Case untouched
```

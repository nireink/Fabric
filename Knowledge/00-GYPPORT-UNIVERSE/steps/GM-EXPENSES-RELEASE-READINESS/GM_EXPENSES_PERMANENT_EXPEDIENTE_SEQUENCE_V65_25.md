# GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25
MODE=AUDIT_V64_THEN_IMPLEMENT_V65_THEN_VERIFY_THEN_REHEARSE
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner usability rule after GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24: EXP. NN permanent per tenant
ACCEPTED_BASELINE=gm-expenses 874a3e5, Gystigo 0293ff4, Fabric 018ea84, Shared DEV V64
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES PERMANENT EXPEDIENTE SEQUENCE

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25

MODE=
AUDIT_CURRENT_V64_MODEL
→ IMPLEMENT_V65
→ VERIFY
→ DISPOSABLE_REHEARSAL
→ OWNER_REVIEW

OWNER_AUTHORIZED=YES

PUSH_AUTHORIZED=NO
SHARED_DEV_DEPLOYMENT_AUTHORIZED=NO


======================================================================
0. PURPOSE
======================================================================

gm-expenses is functionally near MVP closure.

V64 is already deployed successfully and introduced:

    case_business_date
    case_sequence
    case_number

with:

    case_number = YYYYMMDD####

and sequence scope:

    TENANT + BUSINESS_DATE


The Owner has now clarified one final usability requirement:

    EXP. NN

must NOT reuse the daily case_sequence.

EXP. NN must be a permanent, monotonically increasing ExpenseCase number
inside the tenant, independent of business date.

Therefore:

    EXP. NN
    and
    ID: YYYYMMDD####

are TWO different business representations with TWO different purposes.

This STEP must implement that separation cleanly.

Do NOT change the existing ID semantics.

Do NOT modify V64.

Do NOT modify financial semantics.

Do NOT modify the Owner Case movements.

Do NOT push.

Do NOT deploy Shared DEV in this STEP.


======================================================================
1. OWNER FINAL CANONICAL MODEL
======================================================================

There are now FOUR distinct identifiers/concepts.


A. TECHNICAL RESOURCE ID

    UUID

Example:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0

Purpose:

    technical identity
    API routing
    persistence relationships


B. PERMANENT EXPEDIENTE SEQUENCE

New concept:

    expense_sequence

Example:

    1
    2
    3
    4
    ...


Scope:

    TENANT


It NEVER resets because of the business date.


Visual representation:

    EXP. 01
    EXP. 02
    EXP. 03
    ...
    EXP. 99
    EXP. 100


C. DAILY CASE SEQUENCE

Existing V64 concept:

    case_sequence


Example:

    1
    2
    3


Scope:

    TENANT + BUSINESS_DATE


It exists to compose the business ID.


D. BUSINESS CASE NUMBER

Existing V64 concept:

    case_number


Format:

    YYYYMMDD####


Example:

    202609170001


Composition:

    case_business_date
    +
    zero-padded case_sequence


======================================================================
2. FINAL EXAMPLE
======================================================================

Correct model:

    EXP. 01: Viaje Loja
    Fecha: 2026-09-13
    ID: 202609130001


    EXP. 02: Compra Filtro
    Fecha: 2026-09-17
    ID: 202609170001


    EXP. 03: Mantenimiento B34
    Fecha: 2026-09-17
    ID: 202609170002


Important:

The exact historical EXP. 01 / EXP. 02 assignment MUST follow real creation
order.

Do NOT assume that business date equals creation order.

If Compra Filtro was actually created before Viaje Loja:

    Compra Filtro may correctly become EXP. 01
    Viaje Loja may correctly become EXP. 02

Backfill must use actual creation chronology, not the displayed business date.


======================================================================
3. WHY THE TWO SEQUENCES ARE DIFFERENT
======================================================================

expense_sequence answers:

    "Which ExpenseCase number is this for this tenant?"


case_sequence answers:

    "Which Case number was generated on this business date?"


Therefore:

    expense_sequence

does NOT participate in:

    case_number


and:

    case_sequence

does NOT determine:

    EXP. NN


Do NOT force one sequence to serve both purposes.


======================================================================
4. PERMANENT EXP NUMBER RULE
======================================================================

Canonical:

    expense_sequence scope =
    TENANT


Examples for Tenant A:

    Case 1  → EXP. 01
    Case 2  → EXP. 02
    Case 3  → EXP. 03
    ...
    Case 99 → EXP. 99
    Case 100 → EXP. 100


Changing date MUST NOT reset it.


Example:

2026-09-17:

    EXP. 28
    ID: 202609170004


2026-09-18:

    EXP. 29
    ID: 202609180001


The new day resets only:

    case_sequence

NOT:

    expense_sequence


======================================================================
5. RETROACTIVE BUSINESS DATE
======================================================================

Creation order is authoritative for EXP numbering.


Example:

The tenant already has:

    EXP. 30


Then a new Case is created today but with:

    businessDate = 2026-09-10


It must become:

    EXP. 31


Its ID may be:

    202609100003


Therefore:

    EXP sequence depends on creation

while:

    ID depends on business date.


Never renumber EXP because businessDate changes.


======================================================================
6. EXP DISPLAY FORMAT
======================================================================

Visual formatting:

    1   → EXP. 01
    2   → EXP. 02
    9   → EXP. 09
    10  → EXP. 10
    99  → EXP. 99
    100 → EXP. 100
    101 → EXP. 101


Rule:

    minimum 2 digits

NOT:

    exactly 2 digits


Do not truncate numbers above 99.


======================================================================
7. FINAL CARD IDENTIFICATION
======================================================================

Required card:

    EXP. 02: Compra Filtro

    Fecha: 2026-09-17
    ID: 202609170001


The title uses:

    expense_sequence


The ID line uses:

    case_number


Do NOT use:

    case_sequence

for EXP anymore.


======================================================================
8. AUDIT CURRENT V64 IMPLEMENTATION FIRST
======================================================================

Before modifying anything, audit:

- ExpenseCase aggregate/domain representation;
- V64 fields;
- current sequence allocation ports;
- current counter table;
- Case creation transaction;
- JDBC repository;
- Host payload;
- Studio card/detail;
- tests;
- current Shared DEV V64 schema.


Determine exact existing names.

Do NOT guess schema names.

Return internally:

    EXISTING_CASE_SEQUENCE_FIELD=
    EXISTING_CASE_NUMBER_FIELD=
    EXISTING_BUSINESS_DATE_FIELD=
    EXISTING_DAILY_COUNTER_TABLE=
    CASE_CREATION_TRANSACTION_BOUNDARY=


Confirm:

    V64 remains byte-identical and untouched.


======================================================================
9. V64 MUST REMAIN IMMUTABLE
======================================================================

V64 is already deployed.

STRICT RULE:

    DO NOT EDIT V64.


No correction-in-place.

No migration rewriting.

No checksum drift.


This change must be:

    V65


Require:

    V64_BEFORE_SHA256=
    V64_AFTER_SHA256=

and:

    identical = YES


======================================================================
10. V65 SCOPE
======================================================================

V65 must be SMALL and bounded.


Expected schema addition:

    expense_sequence


to the existing ExpenseCase persistence model.


Also add only the minimum persistence required for concurrency-safe
per-tenant allocation.


Expected concepts:

    expense_sequence
    permanent per-tenant counter


Do NOT change:

    case_business_date
    case_sequence
    case_number


Do NOT change:

    financial tables
    advances
    expenses
    settlement events
    reviews
    Return/Reimbursement history


======================================================================
11. EXPENSE SEQUENCE UNIQUENESS
======================================================================

Enforce:

    UNIQUE (
        tenant_id,
        expense_sequence
    )


expense_sequence must be:

    NOT NULL

after deterministic backfill.


There must be no duplicate EXP number inside the same tenant.


Different tenants may independently have:

    EXP. 01


That is correct.


======================================================================
12. HISTORICAL BACKFILL
======================================================================

Current Shared DEV contains existing ExpenseCases.

Backfill expense_sequence independently for EACH tenant.


Ordering rule:

    ORDER BY
        created_at ASC,
        stable technical id ASC


The stable technical id is used only as a deterministic tie-breaker.


DO NOT order by:

    businessDate
    caseNumber
    current list order
    title
    responsible
    UUID lexical order alone if created_at differs


Do NOT change:

    created_at
    businessDate
    caseSequence
    caseNumber


Only assign:

    expense_sequence


======================================================================
13. HISTORICAL EXAMPLE
======================================================================

Suppose real creation chronology is:

    A created_at 10:00
    B created_at 11:00
    C created_at 12:00


Regardless of their business dates:

    A → expense_sequence 1
    B → expense_sequence 2
    C → expense_sequence 3


Even if:

    A businessDate = 2026-09-17
    B businessDate = 2026-09-13
    C businessDate = 2026-09-17


EXP remains creation chronology.


======================================================================
14. NEW CASE ALLOCATION
======================================================================

For a new ExpenseCase:

allocate:

    expense_sequence

server-side.


Scope:

    tenant_id


The allocation must happen as part of the authoritative Case creation flow.


Do NOT generate it in Studio.


Do NOT derive it from:

    number of Cases
    current list
    MAX(expense_sequence) + 1 without concurrency protection
    UUID
    business date
    case_sequence


======================================================================
15. CONCURRENCY
======================================================================

expense_sequence allocation must be:

- persistent;
- transactional;
- concurrency-safe;
- tenant-scoped.


Two concurrent ExpenseCase creations for the same tenant must receive
different permanent sequences.


Example:

Existing:

    latest expense_sequence = 30


Two concurrent requests:

    Request A → 31
    Request B → 32


Never:

    both 31


Add a REAL DB concurrency test.


======================================================================
16. COUNTER ARCHITECTURE
======================================================================

Audit whether the V64 daily sequence counter abstraction can be safely reused
as an implementation pattern.

Do NOT reuse the SAME daily counter key.


The two counters are logically different:

A.

    daily Case-number counter

keyed by:

    tenant + businessDate


B.

    permanent Expense sequence counter

keyed by:

    tenant


Reuse code/pattern where appropriate.

Do not conflate state.


Do not duplicate infrastructure unnecessarily if a generic sequence allocator
already exists.


======================================================================
17. TRANSACTION SEMANTICS
======================================================================

Prefer permanent EXP allocation within the same database transaction as Case
creation.


A failed Case creation must not produce:

- duplicate sequence;
- partially-created Case;
- inconsistent counter state.


Document whether transaction rollback may reuse an uncommitted number.


Once an ExpenseCase is committed:

    expense_sequence is immutable

and must NEVER be assigned to another committed Case.


======================================================================
18. IMMUTABILITY
======================================================================

Once assigned:

    expense_sequence

must never change.


Not because of:

- date correction;
- title correction;
- responsible change;
- resource change;
- Case lifecycle;
- sorting;
- filtering;
- migration;
- tenant timezone change.


Add protection consistent with existing project conventions.


======================================================================
19. DOMAIN MODEL
======================================================================

Introduce the minimum domain concept required.


Preferred semantic name:

    ExpenseSequence

or equivalent consistent with current naming.


Do not misuse:

    CaseNumber

because CaseNumber already represents:

    YYYYMMDD####


The domain should make the semantic difference explicit.


======================================================================
20. API
======================================================================

Expose the permanent number in Case list/detail.


Preferred payload concept:

    expenseSequence


Preserve:

    caseSequence
    caseNumber
    businessDate
    UUID


Required conceptual payload:

    id: UUID
    expenseSequence: 2
    businessDate: 2026-09-17
    caseSequence: 1
    caseNumber: 202609170001


Do not remove existing fields.


======================================================================
21. STUDIO — TITLE
======================================================================

Replace the current title source.


OLD:

    EXP derived from caseSequence


NEW:

    EXP derived from expenseSequence


Example:

    expenseSequence = 2

renders:

    EXP. 02: Compra Filtro


ID remains:

    ID: 202609170001


No other presentation change is required.


======================================================================
22. STUDIO — NO LIST POSITION FALLBACK
======================================================================

Do NOT bring back list-position numbering.


EXP must not depend on:

- array index;
- page number;
- sort order;
- filters.


If API returns:

    expenseSequence = 27

then display:

    EXP. 27

regardless of its position on screen.


======================================================================
23. STUDIO — OLD API COMPATIBILITY
======================================================================

Do NOT invent an EXP number from:

    caseSequence

once V65 semantics are active.


If a temporary old backend does not expose expenseSequence:

prefer:

    no EXP prefix / transitional unavailable state

over displaying a semantically incorrect daily sequence as permanent EXP.


However the final deployed V65 runtime MUST always provide expenseSequence.


Do not create a long-lived compatibility ambiguity.


======================================================================
24. DETAIL PAGE
======================================================================

If the Detail surface displays the EXP number, it must use:

    expenseSequence


Require:

    CARD_EXPENSE_SEQUENCE
    ==
    DETAIL_EXPENSE_SEQUENCE
    ==
    API_EXPENSE_SEQUENCE


The ID remains:

    CARD_CASE_NUMBER
    ==
    DETAIL_CASE_NUMBER
    ==
    API_CASE_NUMBER


======================================================================
25. FINAL VISUAL EXAMPLE
======================================================================

Target:

    EXP. 02: Compra Filtro                         Abierto

    Fecha: 2026-09-17
    ID: 202609170001

    --------------------------------------------------

    Responsable:       Eduardo Burgasí             Conciliado
    Supervisor:        Sofia Salinas               Pendiente
    Recurso asignado:  Vehículo · LBC9835 ...

    --------------------------------------------------

    Finanzas


No visual redesign beyond changing the EXP source is requested.


======================================================================
26. FINANCIAL MODEL — FREEZE
======================================================================

DO NOT modify any financial behavior.


Freeze:

    Total anticipos
    Total gastos
    Total a conciliar
    Devuelto
    Reembolsado
    Pendiente
    Usado
    Uso


Canonical Owner fixture remains:

    advances = 320
    approved expenses = 400
    rejected expense = financial effect zero
    base = 80 Por reembolsar


The live historical stored Return USD 300 remains separate.


======================================================================
27. OWNER CASE — DO NOT TOUCH MOVEMENTS
======================================================================

Target Case:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0


It still has:

    raw Return events = USD 300


DO NOT reverse them in this STEP.


V65 must not change:

    settlement_balance_event
    Return history
    final pending balance


The authenticated reversal remains a later Owner action.


======================================================================
28. REQUIRED BACKFILL TESTS
======================================================================

Test deterministic historical ordering.


Example same tenant:

Case A:
    created_at 10:00

Case B:
    created_at 11:00

Case C:
    created_at 12:00


Expected:

    A expenseSequence = 1
    B expenseSequence = 2
    C expenseSequence = 3


Even if their businessDates are out of chronological order.


Also test tie:

Case A/B same created_at.

Stable technical-id ordering must produce deterministic assignment.


======================================================================
29. REQUIRED NEW-CREATION TESTS
======================================================================

Same tenant:

Existing:

    EXP. 01
    EXP. 02


Next creation:

    EXP. 03


New business date:

    still EXP. 04


Retroactive business date:

    still next EXP number


Another tenant:

    may begin independently at EXP. 01


======================================================================
30. REQUIRED CONCURRENCY TEST
======================================================================

Use real MySQL / existing real-DB test pattern.


Race at least:

    8 concurrent allocations

for the same tenant.


Require:

- 8 distinct expenseSequence values;
- no duplicate;
- contiguous committed values if the chosen transaction architecture provides
  that guarantee;
- otherwise document valid gap behavior.


Do not weaken the test due to outer test transaction/snapshot issues.

Use the proven STEP 22 real-connection pattern where appropriate.


======================================================================
31. REQUIRED IMMUTABILITY TEST
======================================================================

After creation attempt to alter:

    expense_sequence


Require refusal/protection at the appropriate layer.


Existing Case remains:

    EXP. NN

forever.


======================================================================
32. REQUIRED LIST TEST
======================================================================

Fixture:

    A expenseSequence=1
    B expenseSequence=2
    C expenseSequence=3


Sort:

    C
    A
    B


Must render:

    C → EXP. 03
    A → EXP. 01
    B → EXP. 02


Filter to B only:

    B → EXP. 02


No renumbering.


======================================================================
33. REQUIRED DATE-INDEPENDENCE TEST
======================================================================

Fixture:

Case A:

    expenseSequence = 7
    businessDate = 2026-09-17
    caseSequence = 3
    caseNumber = 202609170003


Case B:

    expenseSequence = 8
    businessDate = 2026-09-18
    caseSequence = 1
    caseNumber = 202609180001


Expected:

    A → EXP. 07 / ID 202609170003
    B → EXP. 08 / ID 202609180001


This proves EXP does not reset with date.


======================================================================
34. V65 DISPOSABLE REHEARSAL
======================================================================

Before touching Shared DEV:

create a disposable copy of CURRENT Shared DEV V64.


Apply V65.


Verify:

    migration 64 → 65 PASS
    failed migrations = 0


Record:

    total ExpenseCases
    cases with expense_sequence
    NULL expense_sequence
    duplicate tenant+expense_sequence


Require:

    NULL=0
    DUPLICATES=0


Verify exact backfill order for every tenant.


======================================================================
35. MIGRATION FINANCIAL INTEGRITY
======================================================================

Before/after V65 compare accepted financial tables.


Require V65 changes ZERO bytes/business values in:

- advances;
- expenses;
- expense review history;
- settlement/rendition;
- settlement_balance_event;
- Return/Reimbursement history.


V65 is numbering only.


Return:

    FINANCIAL_HISTORY_CHANGED_BY_V65=NO


======================================================================
36. V64 PROVENANCE
======================================================================

Prove:

    V64 remains unchanged.


Return:

    V64_SHA256_BEFORE=
    V64_SHA256_AFTER=
    V64_UNCHANGED=YES


Migration chain becomes:

    ...
    V63
    V64
    V65


Never:

    edited V64


======================================================================
37. CURRENT SOURCE BASELINE
======================================================================

Current committed baseline after STEP 23:

gm-expenses:

    874a3e5071e46b179444730089d34afa5fe0e742


Gystigo:

    0293ff45e94b2ebbec67e792fea28e7b80bc8901


Fabric:

    018ea843b6bbb86f4e47c3ad43edb42ac7f7ffe5


Current Shared DEV:

    V64


Current official backend:

    STEP 24 image built from those committed code heads.


Before editing verify exact repository HEADs.


Important:

Fabric contains STEP 24 deployment evidence that may currently be uncommitted.

Preserve/classify it.

Do NOT lose it.


======================================================================
38. WORKTREE AUDIT
======================================================================

Before editing:

audit current dirty paths in:

    gm-expenses
    Gystigo
    Fabric


Classify:

A.
STEP 24 deployment evidence

B.
V65 accepted work

C.
unrelated pre-existing WIP

D.
generated/runtime

E.
unknown


Require:

    UNKNOWN=0


Do not stage anything in this STEP.


======================================================================
39. TEST STRATEGY
======================================================================

Run affected tests only, plus required migration/concurrency proof.


gm-expenses:

    affected + full module suite


Host:

    targeted Case API
    real-DB expenses suite


Studio:

    affected contracts
    full contract suite
    ESLint


Migration:

    disposable V64 → V65 rehearsal


Concurrency:

    real DB tenant permanent-sequence race


Responsive:

Only rerun the relevant card/detail contracts if Studio markup changes.

No broad platform regressions unless shared bytes invalidate baseline.


======================================================================
40. DOCUMENTATION
======================================================================

Append final Owner rule to canonical documentation.


Record:

    EXP. NN =
    permanent tenant-scoped ExpenseCase sequence


    ID =
    YYYYMMDD#### business identifier


    UUID =
    technical identifier


Explicitly SUPERSEDE the previous rule:

    EXP. NN derives from case_sequence


New canonical rule:

    EXP. NN derives from expense_sequence


Existing canonical rule remains:

    case_number derives from
    case_business_date + daily case_sequence


Document:

    expense_sequence scope = tenant
    case_sequence scope = tenant + business date


Append-only:

    Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md


Store STEP prompt/evidence.

Refresh CURRENT_STEP.


======================================================================
41. NO COMMIT YET
======================================================================

This is implementation + verification only.


Do NOT:

- stage;
- commit;
- push;
- deploy V65 to Shared DEV;
- rebuild official backend;
- mutate Owner financial data.


Stop for Owner review after all evidence is green.


======================================================================
42. OWNER ACCEPTANCE CRITERIA
======================================================================

This STEP is ready only when all are true:

    V65 created

    V64 unchanged

    historical ExpenseCases have deterministic expense_sequence

    no tenant duplicates

    new Cases auto-increment permanent EXP number

    new day does NOT reset EXP

    ID daily sequence still works unchanged

    concurrent creation cannot duplicate EXP

    Card uses expenseSequence

    Detail uses expenseSequence

    ID still uses caseNumber

    financial data unchanged

    all affected tests green


======================================================================
43. REQUIRED FINAL REPORT
======================================================================

Return:


STEP=
GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25


STATUS=
READY_FOR_OWNER_REVIEW
or
BLOCKED


--------------------------------------------------
BASELINE
--------------------------------------------------

GM_EXPENSES_HEAD=

GYSTIGO_HEAD=

FABRIC_HEAD=

SHARED_DEV_VERSION=
64


--------------------------------------------------
MODEL
--------------------------------------------------

PERMANENT_EXP_FIELD=
expense_sequence

PERMANENT_EXP_SCOPE=
TENANT

DAILY_SEQUENCE_FIELD=
case_sequence

DAILY_SEQUENCE_SCOPE=
TENANT + BUSINESS_DATE

BUSINESS_ID_FIELD=
case_number

TECHNICAL_ID=
UUID


--------------------------------------------------
EXAMPLES
--------------------------------------------------

EXP_SEQUENCE_1_DISPLAY=
EXP. 01

EXP_SEQUENCE_2_DISPLAY=
EXP. 02

EXP_SEQUENCE_100_DISPLAY=
EXP. 100

BUSINESS_ID_EXAMPLE=
202609170001


--------------------------------------------------
V65
--------------------------------------------------

V65_CREATED=
YES/NO

V64_UNCHANGED=
YES/NO

V64_SHA256_BEFORE=

V64_SHA256_AFTER=

V65_SCOPE=
PERMANENT EXPEDIENTE NUMBERING ONLY


--------------------------------------------------
BACKFILL
--------------------------------------------------

TOTAL_EXISTING_CASES=

CASES_BACKFILLED=

NULL_EXPENSE_SEQUENCE=

DUPLICATE_TENANT_EXPENSE_SEQUENCE=

BACKFILL_ORDER=
created_at + stable technical id

BACKFILL_DETERMINISTIC=
YES/NO


--------------------------------------------------
OWNER CASE
--------------------------------------------------

OWNER_CASE_UUID=
437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0

OWNER_CASE_EXPENSE_SEQUENCE=

OWNER_CASE_EXP_DISPLAY=

OWNER_CASE_BUSINESS_DATE=
2026-09-17

OWNER_CASE_DAILY_SEQUENCE=
1

OWNER_CASE_ID=
202609170001


--------------------------------------------------
DATE INDEPENDENCE
--------------------------------------------------

EXP_RESETS_DAILY=
NO

ID_DAILY_SEQUENCE_RESETS=
YES

RETROACTIVE_DATE_CHANGES_EXP_SEQUENCE=
NO


--------------------------------------------------
CONCURRENCY
--------------------------------------------------

PERMANENT_SEQUENCE_ALLOCATOR=
TRANSACTIONAL / OTHER

REAL_DB_CONCURRENT_THREADS=

DISTINCT_ALLOCATIONS=

DUPLICATES=

CONCURRENT_SEQUENCE_TEST=
PASS/FAIL


--------------------------------------------------
API
--------------------------------------------------

LIST_HAS_EXPENSE_SEQUENCE=
YES/NO

DETAIL_HAS_EXPENSE_SEQUENCE=
YES/NO

CASE_SEQUENCE_PRESERVED=
YES/NO

CASE_NUMBER_PRESERVED=
YES/NO

UUID_ROUTES_PRESERVED=
YES/NO


--------------------------------------------------
STUDIO
--------------------------------------------------

CARD_EXP_SOURCE=
expenseSequence

DETAIL_EXP_SOURCE=
expenseSequence

CARD_ID_SOURCE=
caseNumber

DETAIL_ID_SOURCE=
caseNumber

LIST_SORT_DOES_NOT_RENUMBER=
PASS/FAIL

LIST_FILTER_DOES_NOT_RENUMBER=
PASS/FAIL

DATE_CHANGE_DOES_NOT_RESET_EXP=
PASS/FAIL


--------------------------------------------------
FINANCIAL
--------------------------------------------------

FINANCIAL_MODEL_CHANGED=
NO

FINANCIAL_HISTORY_CHANGED_BY_V65=
NO

OWNER_CASE_RETURN_HISTORY_CHANGED=
NO


--------------------------------------------------
TESTS
--------------------------------------------------

GM_EXPENSES=

HOST_REAL_DB=

HOST_TARGETED=

STUDIO=

ESLINT=

V64_TO_V65_REHEARSAL=

PERMANENT_SEQUENCE_CONCURRENCY=


--------------------------------------------------
SOURCE CONTROL
--------------------------------------------------

CURRENT_DIRTY_PATHS=

UNKNOWN_PATHS=
0

FILES_STAGED=
0

COMMITS_CREATED=
0

PUSH_PERFORMED=
NO

SHARED_DEV_MODIFIED=
NO

DEPLOYMENT_PERFORMED=
NO


READY_FOR_CONTROLLED_COMMIT_GATE=
YES/NO


NEXT_STEP_IF_GREEN=

    GM_EXPENSES_V65_CONTROLLED_COMMIT_AND_DEPLOYMENT


STOP_FOR_OWNER_REVIEW=
YES

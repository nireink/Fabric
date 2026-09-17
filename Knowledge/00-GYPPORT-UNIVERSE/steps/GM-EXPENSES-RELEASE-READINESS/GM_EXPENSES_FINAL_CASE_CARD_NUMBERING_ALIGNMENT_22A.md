# GM_EXPENSES_FINAL_CASE_CARD_NUMBERING_ALIGNMENT_22A — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_FINAL_CASE_CARD_NUMBERING_ALIGNMENT_22A
MODE=AUDIT_CURRENT_IMPLEMENTATION_THEN_APPLY_THEN_VERIFY
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner final presentation rule after GM_EXPENSES_FINAL_MVP_CLOSURE_22
ACCEPTED_BASELINE=gm-expenses 545eae0, Gystigo bcb9591, Fabric bbdd66a, Shared DEV V63
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES FINAL CASE CARD
VISUAL ALIGNMENT + SINGLE EXPEDIENTE NUMBERING SOURCE

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_FINAL_CASE_CARD_NUMBERING_ALIGNMENT_22A

MODE=
AUDIT_CURRENT_IMPLEMENTATION
→ APPLY FINAL OWNER VISUAL/NUMBERING RULE
→ VERIFY

OWNER_AUTHORIZED=YES


======================================================================
0. PURPOSE
======================================================================

STEP 22 already implemented the persistent ExpenseCase business numbering:

    case_business_date
    case_sequence
    case_number

This STEP applies the Owner's FINAL presentation rule:

    EXP. 01

and:

    ID: 202609170001

represent the SAME ExpenseCase numbering system.

There must NOT be two independent counters.

The visual card must also match the Owner's final layout.

No new migration.

Do NOT change V64.

Do NOT modify financial formulas.

Do NOT modify Shared DEV.

Do NOT stage.

Do NOT commit.

Do NOT push.


======================================================================
1. OWNER FINAL NUMBERING DECISION
======================================================================

There is ONE canonical ExpenseCase sequence source:

    case_sequence

There is ONE canonical complete business number:

    case_number


Example persisted data:

    case_business_date = 2026-09-17
    case_sequence      = 1
    case_number        = 202609170001


Both UI representations derive from this SAME data.


Short representation:

    EXP. 01


Complete representation:

    ID: 202609170001


DO NOT maintain:

    exp_number counter
    +
    case_number counter

There is no separate EXP counter.


Canonical:

    SINGLE_SEQUENCE_SOURCE = case_sequence


======================================================================
2. RELATION BETWEEN EXP AND ID
======================================================================

caseNumber composition:

    YYYYMMDD + caseSequence padded to 4 digits


Example:

    businessDate = 2026-09-17
    caseSequence = 1

    caseNumber =
    20260917 + 0001
    =
    202609170001


UI title:

    EXP. 01: VIAJE QUITO


UI identifier:

    ID: 202609170001


Therefore:

    EXP. 01

is the short human-friendly representation of:

    case_sequence = 1


and:

    ID: 202609170001

is the complete business number built from:

    businessDate + the SAME case_sequence.


======================================================================
3. NO LIST-POSITION NUMBERING
======================================================================

The current historical implementation may derive:

    EXP. NN

from list position/index.

That behavior is now SUPERSEDED.


EXP. NN MUST NOT depend on:

- array index;
- pagination;
- sorting;
- filtering;
- current screen order;
- number of Cases returned.


Example:

If the Case has:

    case_sequence = 1

it remains:

    EXP. 01

even if it appears third in a filtered list.


If:

    case_sequence = 27

it displays:

    EXP. 27


If:

    case_sequence = 100

it displays:

    EXP. 100


Do not truncate sequences above 99.


======================================================================
4. EXP DISPLAY FORMAT
======================================================================

For presentation:

    1  → 01
    2  → 02
    9  → 09
    10 → 10
    99 → 99
    100 → 100


Conceptually:

    minimum 2 digits

not:

    fixed exactly 2 digits.


Title format:

    EXP. {formatted caseSequence}: {Case title}


Examples:

    EXP. 01: VIAJE QUITO
    EXP. 02: Compra Filtro
    EXP. 27: Mantenimiento Bodega
    EXP. 100: Proyecto Especial


======================================================================
5. API AUDIT FIRST
======================================================================

Before editing Studio, inspect the current STEP 22 API payload.

Determine whether Case list/detail already expose:

    caseSequence
    caseNumber
    businessDate


Return internally:

    API_HAS_CASE_SEQUENCE=YES/NO
    API_HAS_CASE_NUMBER=YES/NO
    API_HAS_BUSINESS_DATE=YES/NO


If caseSequence already exists:

    reuse it directly.


If caseSequence is NOT exposed:

add the smallest correct API/Host mapping necessary to expose the persisted:

    caseSequence


Do NOT create a second calculation in Studio.

Do NOT derive EXP. NN from list position.


Do NOT create another database field.


======================================================================
6. DO NOT PARSE CASE NUMBER AS PRIMARY DESIGN
======================================================================

Preferred:

    EXP display ← caseSequence

not:

    EXP display ← last digits of caseNumber


caseNumber parsing may be used only as a temporary compatibility fallback if
an old deployed API lacks caseSequence.

It must NOT become the canonical source.


When the current API supports caseSequence:

    backend value wins.


======================================================================
7. SINGLE SOURCE INVARIANTS
======================================================================

Require:

    caseSequence = 1

therefore:

    EXP display = 01


and:

    caseNumber = 202609170001


Require consistency:

    caseNumber suffix 0001
    corresponds to
    caseSequence 1


For normal persisted Cases these values must never contradict each other.


Add a contract/invariant proving this relationship.


======================================================================
8. DAILY SEQUENCE BEHAVIOR
======================================================================

The sequence scope established by STEP 22 remains:

    TENANT + BUSINESS_DATE


Example:

2026-09-17:

    sequence 1
    EXP. 01
    ID: 202609170001

    sequence 2
    EXP. 02
    ID: 202609170002


2026-09-18:

    sequence 1
    EXP. 01
    ID: 202609180001


Therefore:

    EXP. 01

may legitimately appear again on a different business date.


The complete ID remains tenant-business-date specific.


======================================================================
9. TECHNICAL ID REMAINS SEPARATE
======================================================================

Technical API/resource identity remains:

    UUID


Example:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0


Do NOT replace UUID routing.


Concepts:

    UUID
        = technical resource id

    caseSequence
        = daily short ExpenseCase sequence

    caseNumber
        = complete visible business number


======================================================================
10. FULL BUSINESS REFERENCE REMAINS SEPARATE
======================================================================

Future/full Ecuador traceability may compose:

    RUC-ESTABLISHMENT_NUMBER-CASE_NUMBER


Example:

    1191771814001-001-202609170001


This does NOT alter:

    caseSequence
    caseNumber


Establishment is not required for:

    EXP. 01
    ID: 202609170001


Do NOT fabricate establishment data.


======================================================================
11. OWNER FINAL CARD VISUAL TARGET
======================================================================

The card must visually follow this structure:


┌──────────────────────────────────────────────────────────────────────┐
│ EXP. 01: VIAJE QUITO                                      Cerrado   │
│ Fecha: 2026-09-17                                                   │
│ ID: 202609170001                                                    │
│ ------------------------------------------------------------------  │
│                                                                      │
│ Responsable:       Eduardo Burgasí                    Conciliado     │
│ Supervisor:        Eduardo Burgasí                    100%   │BAR│  │
│ Recurso asignado:  Sin recurso                                     │
│                                                                      │
│ ------------------------------------------------------------------  │
│ Finanzas                                                             │
│                                                                      │
│ Total anticipos   Total gastos   Total a conciliar        Uso        │
│ USD 200.00        USD 200.00     USD 0.00                 100% │BAR││
│                                  Balanceado                          │
│                                                                      │
│ Devuelto          Reembolsado    Pendiente                           │
│ USD 0.00          USD 0.00       USD 0.00                            │
│                                  Pendiente de conciliar              │
│                                                                      │
│ Usado                                                                │
│ USD 200.00                                                           │
└──────────────────────────────────────────────────────────────────────┘


======================================================================
12. NO EXTRA SECTION TITLES
======================================================================

Do NOT add visible headings such as:

    Expediente
    Identidad
    Asignación


The visual hierarchy must come from:

- spacing;
- two subtle horizontal dividers;
- existing Finanzas heading.


The result should remain:

    clean
    quiet
    professional
    Executive Technology


======================================================================
13. FIRST REGION — CASE IDENTITY
======================================================================

Top-left:

    EXP. 01: VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170001


Top-right:

    Cerrado / Abierto


The ID label is:

    ID:


NOT:

    ID Gasto:


Use the complete persisted:

    caseNumber


Do NOT display only:

    20260917


Correct:

    ID: 202609170001


======================================================================
14. FIRST DIVIDER
======================================================================

Immediately after the identity information:

    one subtle hairline divider


It separates:

    Case identity

from:

    Assignment


Do not make a nested card.


======================================================================
15. ASSIGNMENT REGION
======================================================================

Below the first divider:

    Responsable:       Eduardo Burgasí
    Supervisor:        Eduardo Burgasí
    Recurso asignado:  Sin recurso


Preserve the accepted label/value layout.


Do NOT:

- shrink label width;
- break label/value into separate desktop rows;
- reduce font size;
- compress line-height;
- truncate names unnecessarily;
- distort resource text.


======================================================================
16. CONCILIADO
======================================================================

Conciliado belongs to the Assignment region.


Target:

    Responsable:       Eduardo Burgasí             Conciliado
    Supervisor:        Eduardo Burgasí             100% │BAR│
    Recurso asignado:  Sin recurso


Keep Conciliado approximately aligned with the Responsable row.


Preserve STEP 15 structural alignment.


Do NOT use arbitrary margin hacks.


Do NOT place Conciliado alongside:

    Fecha
    ID


======================================================================
17. SECOND DIVIDER
======================================================================

After the Assignment region:

    subtle hairline divider


Then:

    Finanzas


Thus the visual model becomes:

    Identity
    ----------------
    Assignment
    ----------------
    Finance


without displaying those words as section headings.


======================================================================
18. FINANCE GRID — FREEZE
======================================================================

Preserve the accepted desktop hierarchy.


ROW 1:

    Total anticipos
    USD 200.00


    Total gastos
    USD 200.00


    Total a conciliar
    USD 0.00
    Balanceado


    Uso
    100%
    │BAR│


ROW 2:

    Devuelto
    USD 0.00


    Reembolsado
    USD 0.00


    Pendiente
    USD 0.00
    Pendiente de conciliar


ROW 3:

    Usado
    USD 200.00


======================================================================
19. USO VISUAL UNIT
======================================================================

Uso must remain one visual unit:

    Uso
    100%
    │BAR│


Do NOT separate the percentage from the bar.


Do NOT allow:

    Usado

to push Uso into another row.


For >100%:

    text = real %
    visual bar = clamp 100%


Example:

    Uso 125%
    full bar


======================================================================
20. FINANCIAL SEMANTICS — DO NOT CHANGE
======================================================================

Freeze STEP 22 financial rules.


TOTAL_ADVANCES =

    SUM(ACTUALLY DELIVERED ADVANCES)


TOTAL_EXPENSES =

    SUM(APROBADO Expenses)


REJECTED Expense:

    financial effect = ZERO


Base:

    TOTAL_ADVANCES - TOTAL_EXPENSES


Do not modify formulas in this visual/numbering STEP.


======================================================================
21. OWNER FINANCIAL FIXTURE
======================================================================

Regression fixture remains:

Advances:

    200
    100
     20

Total:

    320


Approved Expenses:

    200
     80
     90
     30

Total:

    400


Rejected:

    200

Financial effect:

    0


Canonical fixture after net Return correction:

    Total anticipos = 320
    Total gastos = 400
    Total a conciliar = 80 Por reembolsar
    Devuelto = 0
    Reembolsado = 0
    Pendiente = 80 Por reembolsar
    Usado = 400
    Uso = 125%


Do not change this fixture.


======================================================================
22. DETAIL PAGE
======================================================================

The Detail page must use the same canonical identifier data.


If Detail displays an EXP number:

    derive it from caseSequence.


Display:

    Fecha: <businessDate>
    ID: <caseNumber>


Require:

    CARD_CASE_SEQUENCE == DETAIL_CASE_SEQUENCE == API_CASE_SEQUENCE

and:

    CARD_CASE_NUMBER == DETAIL_CASE_NUMBER == API_CASE_NUMBER


Do not redesign the entire Detail page.


======================================================================
23. SORTING / FILTERING REGRESSION
======================================================================

Add a Studio contract proving:

Cases:

    A sequence=1
    B sequence=2
    C sequence=3


If list order becomes:

    C
    A
    B


display remains:

    C → EXP. 03
    A → EXP. 01
    B → EXP. 02


Do NOT renumber them:

    01
    02
    03

based on current array position.


Also verify filtering:

If only B remains visible:

    B still shows EXP. 02


not:

    EXP. 01


======================================================================
24. BUSINESS DATE RESET CONTRACT
======================================================================

Require:

Case A:

    businessDate = 2026-09-17
    sequence = 1
    caseNumber = 202609170001

renders:

    EXP. 01


Case B:

    businessDate = 2026-09-18
    sequence = 1
    caseNumber = 202609180001

also renders:

    EXP. 01


This is correct.


======================================================================
25. CASE NUMBER CONSISTENCY CONTRACT
======================================================================

For:

    caseSequence = 1
    caseNumber = 202609170001


assert:

    short EXP = 01


For:

    caseSequence = 27
    caseNumber = 202609170027


assert:

    short EXP = 27


If API provides inconsistent values:

    do NOT silently repair them in Studio.

Fail the contract / surface the data inconsistency in tests.


======================================================================
26. RESPONSIVE
======================================================================

Verify:

    1280
    768
    375
    320


At desktop/tablet:

    Case identity
    divider
    Assignment + Conciliado
    divider
    Finance


At mobile:

stack naturally but preserve the same semantic order.


No horizontal overflow.

No overlap.

ID must remain readable.

EXP title must remain readable.

No text deformation.


======================================================================
27. TEST SCOPE
======================================================================

Start by auditing whether Host already exposes:

    caseSequence


If NO and Host mapping changes:

run:

- affected Host API tests;
- ID Gasto targeted Host tests;
- relevant real-DB test only if required by changed integration bytes.


If only Studio changes:

reuse:

    GM_EXPENSES=773/773
    HOST_REAL_DB=106/106
    V64 rehearsal=PASS
    concurrency test=PASS


Run:

- ExpenseCase card contracts;
- list ordering/filtering contract;
- Detail identifier contract;
- full Studio contracts;
- ESLint;
- responsive fixtures 1280/768/375/320.


Do not rerun unaffected large suites without invalidation.


======================================================================
28. V64 — FREEZE
======================================================================

Do NOT modify V64 unless audit proves STEP 22 accidentally implemented a
different numbering model.


Expected persisted concepts remain:

    case_business_date
    case_sequence
    case_number


Expected sequence scope remains:

    TENANT + BUSINESS_DATE


No new migration is expected.


======================================================================
29. DOCUMENTATION
======================================================================

Append the final Owner numbering clarification to canonical documentation.


Record:

    EXP. NN is NOT a separate numbering system.

    EXP. NN derives from case_sequence.

    ID derives from case_number.

    case_number derives from:
        business_date + same case_sequence.

    separate EXP counter = NO.

    separate ID counter = NO.


Also record:

    EXP display uses minimum 2-digit formatting.


Examples:

    sequence 1   → EXP. 01
    sequence 27  → EXP. 27
    sequence 100 → EXP. 100


Append-only Reglas.md if this is a new Owner rule.


Store this STEP prompt/evidence.

Refresh CURRENT_STEP.


======================================================================
30. CURRENT WIP
======================================================================

Preserve all accepted accumulated changes from:

    STEP 19
    STEP 20
    STEP 20A
    STEP 21
    STEP 22
    this STEP 22A


Preserve unrelated WIP exclusions.


Before final report:

inventory dirty paths again.


Require:

    UNKNOWN=0


Do NOT stage.


======================================================================
31. HARD SAFETY
======================================================================

Do NOT:

- modify Shared DEV;
- deploy V64;
- deploy backend;
- alter financial history;
- mutate Owner Case;
- create another sequence;
- create another case-number column;
- derive EXP from array index;
- push;
- commit;
- stage.


======================================================================
32. REQUIRED FINAL REPORT
======================================================================

Return:

STEP=
GM_EXPENSES_FINAL_CASE_CARD_NUMBERING_ALIGNMENT_22A


STATUS=
READY_FOR_OWNER_FINAL_VISUAL_ACCEPTANCE
or
BLOCKED


NUMBERING:

SINGLE_SEQUENCE_SOURCE=
case_sequence

SEPARATE_EXP_COUNTER=
NO

SEPARATE_ID_COUNTER=
NO

EXP_DERIVED_FROM=
case_sequence

ID_DERIVED_FROM=
case_number

CASE_NUMBER_COMPOSITION=
businessDate + zero-padded caseSequence

SEQUENCE_SCOPE=
TENANT + BUSINESS_DATE


EXAMPLES:

CASE_SEQUENCE_1=
EXP. 01

CASE_NUMBER_1=
202609170001

CASE_SEQUENCE_27=
EXP. 27

CASE_NUMBER_27=
202609170027


API:

API_HAS_CASE_SEQUENCE=
YES/NO

API_HAS_CASE_NUMBER=
YES/NO

API_HAS_BUSINESS_DATE=
YES/NO

HOST_CHANGED=
YES/NO


CARD:

TITLE_EXAMPLE=
EXP. 01: VIAJE QUITO

ID_LABEL=
ID

ID_EXAMPLE=
202609170001

IDENTITY_SECTION=
PASS/FAIL

FIRST_DIVIDER=
PASS/FAIL

ASSIGNMENT_SECTION=
PASS/FAIL

CONCILIADO_POSITION=
PASS/FAIL

SECOND_DIVIDER=
PASS/FAIL

FINANCE_SECTION=
PASS/FAIL

USAGE_BAR=
PASS/FAIL


DETAIL:

DETAIL_CASE_SEQUENCE_SOURCE=
case_sequence

DETAIL_CASE_NUMBER_SOURCE=
case_number

CARD_DETAIL_SEQUENCE_CONSISTENCY=
YES/NO

CARD_DETAIL_CASE_NUMBER_CONSISTENCY=
YES/NO


LIST BEHAVIOR:

SORTING_DOES_NOT_RENUMBER_EXP=
PASS/FAIL

FILTERING_DOES_NOT_RENUMBER_EXP=
PASS/FAIL

DAILY_SEQUENCE_RESET_DISPLAY=
PASS/FAIL


RESPONSIVE:

1280=
768=
375=
320=


TESTS:

HOST_TARGETED=
STUDIO=
ESLINT=


UNCHANGED_BASELINES:

GM_EXPENSES=
773/773 REUSED / RERUN

HOST_REAL_DB=
106/106 REUSED / RERUN

V64_REHEARSAL=
PASS REUSED / RERUN

CONCURRENT_SEQUENCE_TEST=
PASS REUSED / RERUN


RUNTIME:

SHARED_DEV_VERSION=
V63

SHARED_DEV_MODIFIED=
NO


SOURCE_CONTROL:

UNKNOWN_DIRTY_PATHS=
0

FILES_STAGED=
0

COMMITS_CREATED=
0

PUSH_PERFORMED=
NO

READY_FOR_CONTROLLED_COMMIT_GATE=
YES/NO


STOP_FOR_OWNER_REVIEW=
YES

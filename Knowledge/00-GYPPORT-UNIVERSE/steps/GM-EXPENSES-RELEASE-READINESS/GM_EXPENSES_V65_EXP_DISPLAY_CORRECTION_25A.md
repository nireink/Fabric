# GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A
MODE=TARGETED_FIX_AND_VERIFY
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner correction after STEP 25: the EXP display must show on V65 fixtures, contract and runtime
ACCEPTED_BASELINE=gm-expenses 874a3e5, Gystigo 0293ff4, Fabric 018ea84, Shared DEV V64
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES V65 EXP DISPLAY CORRECTION

STEP=
GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A

MODE=
TARGETED_FIX_AND_VERIFY

OWNER_AUTHORIZED=YES

============================================================
0. PROBLEM
============================================================

The current real/fixture card renders:

    VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170002

The Owner-approved EXP display disappeared.

This is NOT the desired result.

The final card MUST render:

    EXP. 01: VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170002

Do NOT change the V65 numbering architecture.

============================================================
1. CANONICAL EXP DISPLAY
============================================================

EXP is derived exclusively from:

    expenseSequence

Required formatting:

    expenseSequence = 1
        → EXP. 01

    expenseSequence = 2
        → EXP. 02

    expenseSequence = 9
        → EXP. 09

    expenseSequence = 10
        → EXP. 10

    expenseSequence = 99
        → EXP. 99

    expenseSequence = 100
        → EXP. 100

Rule:

    minimum 2 digits

NOT:

    exactly 2 digits.

============================================================
2. TITLE
============================================================

Canonical title:

    EXP. {formatted expenseSequence}: {case title}

Examples:

    EXP. 01: VIAJE QUITO
    EXP. 02: Compra Filtro
    EXP. 03: Mantenimiento B34
    EXP. 100: Proyecto Especial

Do NOT render only:

    VIAJE QUITO

once expenseSequence exists.

============================================================
3. ID REMAINS INDEPENDENT
============================================================

Do NOT change:

    ID: {caseNumber}

Example:

    EXP. 01: VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170002

This is valid.

The two numbers serve different purposes:

    expenseSequence
        = permanent tenant-wide expediente sequence

    caseNumber
        = business-date identifier YYYYMMDD####

Do NOT force their numeric suffixes to match.

============================================================
4. DO NOT FALL BACK TO DAILY SEQUENCE
============================================================

Do NOT derive EXP from:

    caseSequence
    caseNumber suffix
    list index
    sort position
    pagination position

Canonical:

    EXP_SOURCE = expenseSequence

If an OLD V64 backend does not yet emit expenseSequence:

do NOT invent a permanent EXP number.

A transitional old-runtime screen may lack the EXP number until V65 is
deployed.

But:

the V65 fixture,
the V65 API contract,
and the final V65 deployed runtime

MUST always show EXP from expenseSequence.

============================================================
5. V65 ACCEPTANCE FIXTURES
============================================================

Update/verify fixtures explicitly.

Fixture A:

    title = VIAJE QUITO
    expenseSequence = 1
    businessDate = 2026-09-17
    caseSequence = 2
    caseNumber = 202609170002

Expected:

    EXP. 01: VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170002


Fixture B:

    title = Compra Filtro
    expenseSequence = 2
    businessDate = 2026-09-17
    caseSequence = 1
    caseNumber = 202609170001

Expected:

    EXP. 02: Compra Filtro
    Fecha: 2026-09-17
    ID: 202609170001


This explicitly proves:

    EXP numbering
    and
    ID numbering

are independent.

============================================================
6. REQUIRED CONTRACTS
============================================================

Require:

EXP_SEQUENCE_1_DISPLAY=
EXP. 01

EXP_SEQUENCE_2_DISPLAY=
EXP. 02

EXP_SEQUENCE_9_DISPLAY=
EXP. 09

EXP_SEQUENCE_10_DISPLAY=
EXP. 10

EXP_SEQUENCE_100_DISPLAY=
EXP. 100


Also prove:

SORTING_DOES_NOT_RENUMBER_EXP=
PASS

FILTERING_DOES_NOT_RENUMBER_EXP=
PASS

BUSINESS_DATE_CHANGE_DOES_NOT_RENUMBER_EXP=
PASS

CASE_SEQUENCE_DOES_NOT_CONTROL_EXP=
PASS

CASE_NUMBER_DOES_NOT_CONTROL_EXP=
PASS

============================================================
7. CARD + DETAIL
============================================================

Card:

    EXP. {expenseSequence}: {title}

Detail:

if the EXP title is displayed there:

    EXP. {expenseSequence}: {title}

Require:

    CARD_EXPENSE_SEQUENCE
    ==
    DETAIL_EXPENSE_SEQUENCE
    ==
    API_EXPENSE_SEQUENCE

============================================================
8. DO NOT CHANGE OTHER WORK
============================================================

Do NOT modify:

- V64;
- V65 schema unless a real defect is found;
- expense_sequence allocation;
- daily case_sequence;
- case_number;
- financial model;
- Return/Reimbursement;
- Owner Case movements;
- header grouping;
- Finance layout.

This correction is about EXP rendering/contracts only.

============================================================
9. TESTS
============================================================

Run:

- affected Studio contracts;
- full Studio contract suite;
- ESLint;
- card/detail fixtures;
- responsive 1280 / 768 / 375 / 320.

If backend source does not change:

reuse backend/domain tests.

If backend payload already exposes expenseSequence:

do not modify backend merely to fix presentation.

============================================================
10. SOURCE CONTROL
============================================================

Do NOT stage.
Do NOT commit.
Do NOT push.
Do NOT deploy V65 yet.

============================================================
11. REQUIRED REPORT
============================================================

Return:

STEP=
GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A

STATUS=
READY_FOR_OWNER_REVIEW

EXP_SOURCE=
expenseSequence

EXP_SEQUENCE_1_DISPLAY=
EXP. 01

EXP_SEQUENCE_2_DISPLAY=
EXP. 02

EXP_SEQUENCE_100_DISPLAY=
EXP. 100

CARD_TITLE_EXAMPLE=
EXP. 01: VIAJE QUITO

CARD_ID_EXAMPLE=
ID: 202609170002

EXP_AND_ID_INDEPENDENT=
YES

EXP_USES_CASE_SEQUENCE=
NO

EXP_USES_LIST_POSITION=
NO

CARD_EXP_VISIBLE=
YES

DETAIL_EXP_VISIBLE=
YES

STUDIO_TESTS=

ESLINT=

BACKEND_CHANGED=
YES/NO

V65_CHANGED=
YES/NO

FILES_STAGED=
0

COMMITS_CREATED=
0

PUSH_PERFORMED=
NO

STOP_FOR_OWNER_REVIEW=
YES

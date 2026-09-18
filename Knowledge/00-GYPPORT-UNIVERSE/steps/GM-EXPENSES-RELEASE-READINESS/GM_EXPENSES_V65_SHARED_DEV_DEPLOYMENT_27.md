# GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27
MODE=PREDEPLOYMENT_PROOF_BACKUP_V65_MIGRATION_BUILD_DEPLOY_VERIFY
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner activation of the committed V65 permanent expediente number on Shared DEV
ACCEPTED_BASELINE=gm-expenses 39a2adf, Gystigo 5eed5d6, Fabric 1f5bed8, Shared DEV V64 before this STEP
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES V65 SHARED DEV DEPLOYMENT
PERMANENT EXPEDIENTE NUMBER ACTIVATION

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27

MODE=
PREDEPLOYMENT_PROOF
→ BACKUP
→ V65_MIGRATION
→ BUILD_FROM_COMMITTED_HEADS
→ DEPLOY
→ RUNTIME_PROVENANCE
→ REAL_OWNER_UI_SMOKE

OWNER_AUTHORIZED=YES

PUSH_AUTHORIZED=NO


======================================================================
0. PURPOSE
======================================================================

V65 and STEP 25A are already implemented, verified and committed.

Current committed heads:

GM_EXPENSES=
39a2adf4dfff0196208a1f80719be1c12c047ac2

GYSTIGO=
5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc

FABRIC=
1f5bed831c54d01efe74444f02ee2b2d947df549


Current runtime is intentionally still:

    Shared DEV = V64

Therefore the real Studio currently shows:

    VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170002

without:

    EXP. NN:


This STEP must deploy the already-committed V65 implementation.

DO NOT MODIFY SOURCE CODE.

DO NOT redesign EXP.

DO NOT change Studio.

DO NOT change numbering semantics.

DO NOT push.


======================================================================
1. FINAL NUMBERING MODEL — FROZEN
======================================================================

UUID
    = technical resource identifier


expense_sequence
    = permanent tenant-scoped ExpenseCase sequence
    = source of EXP. NN
    = never resets by date


case_sequence
    = daily sequence
    = scope TENANT + BUSINESS_DATE
    = used only to compose case_number


case_number
    = YYYYMMDD####
    = source of ID


Examples:

    expenseSequence=1
        → EXP. 01

    expenseSequence=2
        → EXP. 02

    expenseSequence=100
        → EXP. 100


Valid independent values:

    EXP. 09: VIAJE QUITO
    ID: 202609170002


Do NOT require EXP suffix to match ID suffix.


======================================================================
2. STRICT SOURCE BASELINE
======================================================================

Before deployment verify exact repository heads:

GM_EXPENSES:

    branch = master

    HEAD =
    39a2adf4dfff0196208a1f80719be1c12c047ac2


GYSTIGO:

    branch =
    feature/gm-fleets-minimum-vehicle-master-01

    HEAD =
    5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc


FABRIC:

    branch = main

    HEAD =
    1f5bed831c54d01efe74444f02ee2b2d947df549


If any expected HEAD differs:

    STOP.


Unrelated WIP may remain dirty.

Do not touch it.


======================================================================
3. NO SOURCE EDITING
======================================================================

This is deployment only.

Do NOT edit:

- Java
- JSX
- CSS
- migrations
- tests
- application configuration
- documentation
- Fabric canonical rules


If deployment exposes a real defect:

    STOP
    report exact blocker

Do not repair source inside this STEP.


======================================================================
4. ACCEPTED EVIDENCE
======================================================================

Reuse committed evidence if bytes still match:

GM_EXPENSES=
780/780 PASS

HOST_REAL_DB=
107/107 PASS

STUDIO=
652/652 PASS

ESLINT=
PASS

V64_TO_V65_REHEARSAL=
PASS

PERMANENT_SEQUENCE_CONCURRENCY=
PASS

RESPONSIVE=
1280 PASS
768 PASS
375 PASS
320 PASS


Require:

    COMMITTED_BYTES_MATCH_ACCEPTED_EVIDENCE=YES


Do not rerun full suites merely because deployment is starting.


======================================================================
5. PRE-DEPLOY RUNTIME STATE
======================================================================

Record current runtime before any change.

Expected:

    Shared DEV Flyway = 64

    official backend =
    V64 image from STEP 24

    V65 column absent:
    expense_sequence


Read-only verify:

    expense_case count

    Owner Case:
    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0


Owner Case financial history must remain unchanged:

    Return 200
    Return 100
    no reversals


Do NOT correct those movements in this STEP.


======================================================================
6. FRESH SHARED DEV BACKUP
======================================================================

Before V65:

create a NEW backup of current Shared DEV V64.


Verify:

- file exists
- non-empty
- SHA256 recorded
- disposable restore succeeds


Return:

    BACKUP_PATH
    BACKUP_SIZE
    BACKUP_SHA256
    RESTORE_VALIDATION


If restore validation fails:

    STOP.

Do not migrate.


======================================================================
7. V64 PROVENANCE
======================================================================

V64 is already deployed and must remain unchanged.

Verify committed V64 SHA256 against the previously accepted value.

Require:

    V64_UNCHANGED=YES


Do NOT rewrite V64.


Migration chain must become:

    V64 → V65


======================================================================
8. V65 PROVENANCE
======================================================================

Verify V65 comes from committed Gystigo HEAD:

    5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc


V65 must contain only permanent ExpenseCase numbering.

Expected:

- expense_sequence column
- deterministic backfill
- unique tenant + expense_sequence
- permanent sequence counter/infrastructure
- immutability protection


V65 must NOT alter:

- case_business_date
- case_sequence
- case_number
- Advances
- Expenses
- Reviews
- Settlement
- Return/Reimbursement history
- fiscal identity data


Require:

    V65_COMMITTED_BYTE_VERIFIED=YES


======================================================================
9. APPLY V65 TO SHARED DEV
======================================================================

Use the canonical Flyway deployment path.

Apply:

    V64 → V65


Do NOT execute migration fragments manually.


Verify:

    Flyway current = 65
    migration success = YES
    failed migrations = 0


Require:

    SHARED_DEV_VERSION=V65


======================================================================
10. VERIFY HISTORICAL BACKFILL
======================================================================

After V65 verify every existing ExpenseCase has:

    expense_sequence


Return:

    TOTAL_EXPENSE_CASES
    CASES_WITH_EXPENSE_SEQUENCE
    NULL_EXPENSE_SEQUENCE
    DUPLICATE_TENANT_EXPENSE_SEQUENCE


Expected:

    NULL_EXPENSE_SEQUENCE=0
    DUPLICATE_TENANT_EXPENSE_SEQUENCE=0


Backfill order must match:

    tenant
    ORDER BY created_at, stable technical id


Do NOT renumber by business date.


======================================================================
11. VERIFY REAL OWNER CASE NUMBERS
======================================================================

Read actual migrated values.

For:

    Compra Filtro

report:

    UUID
    expenseSequence
    EXP display
    businessDate
    caseSequence
    caseNumber


For:

    Viaje Quito

report the same.


Expected from rehearsal, if current creation chronology is unchanged:

    Compra Filtro:
        expenseSequence = 8
        EXP. 08
        ID = 202609170001

    Viaje Quito:
        expenseSequence = 9
        EXP. 09
        ID = 202609170002


But do NOT force those expected values.

Database backfill result is authority.


======================================================================
12. EXP / ID INDEPENDENCE PROOF
======================================================================

Prove with real migrated data:

    EXP comes from expense_sequence

    ID comes from case_number


Example real result may be:

    EXP. 09: VIAJE QUITO
    ID: 202609170002


This is correct.


Require:

    EXP_USES_CASE_SEQUENCE=NO
    EXP_USES_CASE_NUMBER=NO
    EXP_USES_LIST_POSITION=NO


======================================================================
13. FINANCIAL INTEGRITY
======================================================================

Compare pre/post V65 financial tables.

Require zero business-value change in:

- advances
- expenses
- expense review history
- settlement/rendition
- settlement_balance_event
- Return/Reimbursement history


Return:

    FINANCIAL_HISTORY_CHANGED_BY_V65=NO


Owner Case must still contain:

    Return 200
    Return 100


This STEP does NOT reverse them.


======================================================================
14. BUILD GM-EXPENSES FROM COMMITTED HEAD
======================================================================

Build/install gm-expenses from:

    39a2adf4dfff0196208a1f80719be1c12c047ac2


Use committed bytes only.


Record:

    jar path
    jar SHA256


Require:

    GM_EXPENSES_BUILD=PASS


======================================================================
15. BUILD BACKEND FROM COMMITTED GYSTIGO
======================================================================

Build official backend from:

    5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc


Use the committed gm-expenses artifact.


Create an explicit image tag.

Example:

    gystigo-backend:4.1.0-java25-gm-expenses-v65-5eed5d6


Add/verify provenance labels:

    gypport.source.gystigo=
    5eed5d6...

    gypport.source.gm-expenses=
    39a2adf...

    gypport.step=
    GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27


Record:

    IMAGE_TAG
    IMAGE_ID


======================================================================
16. DEPLOY OFFICIAL BACKEND
======================================================================

Replace the official Shared DEV backend at:

    localhost:8080


Use the new committed V65 image.


Database:

    Shared DEV V65


Do NOT start a parallel unofficial backend as the final runtime.


After start verify:

    backend healthy
    DB connection healthy
    Flyway current 65


======================================================================
17. RUNTIME PROVENANCE
======================================================================

After deployment prove:

FRONTEND:

    localhost:5173
    current Gystigo Studio working tree


BACKEND:

    localhost:8080
    V65 committed image


DATABASE:

    Shared DEV V65


Return:

    FRONTEND_RUNTIME_SOURCE=
    BACKEND_RUNTIME_SOURCE=
    GM_EXPENSES_RUNTIME_SOURCE=
    DATABASE_FLYWAY_VERSION=65


======================================================================
18. API PROOF
======================================================================

Using existing authenticated test tooling, verify real deployed API emits:

    expenseSequence
    caseSequence
    caseNumber
    businessDate


For list:

    LIST_HAS_EXPENSE_SEQUENCE=YES
    LIST_HAS_CASE_SEQUENCE=YES
    LIST_HAS_CASE_NUMBER=YES
    LIST_HAS_BUSINESS_DATE=YES


For detail:

    DETAIL_HAS_EXPENSE_SEQUENCE=YES
    DETAIL_HAS_CASE_SEQUENCE=YES
    DETAIL_HAS_CASE_NUMBER=YES
    DETAIL_HAS_BUSINESS_DATE=YES


Do not ask for Owner credentials.


======================================================================
19. REAL STUDIO UI — PRIMARY ACCEPTANCE
======================================================================

Primary proof must use:

    http://localhost:5173


NOT synthetic fixture 5189.


Verify actual Case cards now render:

    EXP. {expenseSequence}: {title}

    Fecha: {businessDate}

    ID: {caseNumber}


For example, if migrated values are 8 and 9:

    EXP. 08: Compra Filtro
    Fecha: 2026-09-17
    ID: 202609170001


    EXP. 09: VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170002


The exact EXP values must come from real migration data.


======================================================================
20. DETAIL PAGE
======================================================================

Verify real Detail page uses the same permanent number.


Require:

    CARD_EXPENSE_SEQUENCE
    ==
    DETAIL_EXPENSE_SEQUENCE
    ==
    API_EXPENSE_SEQUENCE


and:

    CARD_CASE_NUMBER
    ==
    DETAIL_CASE_NUMBER
    ==
    API_CASE_NUMBER


======================================================================
21. VISUAL LAYOUT
======================================================================

Preserve accepted UI:

    EXP. NN: TITLE
    Fecha
    ID

    divider

    Responsable
    Supervisor
    Recurso asignado        Conciliado

    divider

    Finanzas


Do NOT alter:

- Finance grid
- Conciliado alignment
- Uso rail
- responsive layout


Verify real app visually at minimum desktop.

Existing responsive fixture evidence may be reused if source bytes are unchanged.


======================================================================
22. OWNER CASE FINANCIAL STATE
======================================================================

After V65 deployment, before Owner reversal, financial values must remain:

    Total anticipos = 320
    Total gastos = 400

    Total a conciliar =
    80 Por reembolsar

    Devuelto = 300

    Reembolsado = 0

    Pendiente =
    380 Por reembolsar

    Usado = 400

    Uso = 125%


This remains expected until the Owner performs authenticated reversals.


Do NOT treat 300/380 as V65 failure.


======================================================================
23. REVERSAL READINESS
======================================================================

Verify deployed runtime still supports reversing:

    Return 200
    Return 100


Require:

- reason mandatory
- authenticated actor
- original immutable
- append-only reversal
- one reversal per original
- net Return becomes zero after both


Do NOT execute the Owner reversals automatically.


======================================================================
24. SMOKE TEST
======================================================================

Run narrow Shared DEV smoke.

Must include:

- backend health
- auth through test tooling
- tenant isolation
- ExpenseCase list
- ExpenseCase detail
- expenseSequence
- caseSequence
- caseNumber
- businessDate
- UUID route
- financial summary
- no 5xx


Return:

    SMOKE_CHECKS
    SMOKE_FAILURES
    HTTP_5XX_COUNT
    TENANT_ISOLATION


======================================================================
25. NO SOURCE COMMIT
======================================================================

Deployment must not create source changes.


Expected:

    NEW_SOURCE_COMMITS_CREATED=0


If Fabric deployment evidence is written and uncommitted:

report it.

Do not silently commit without authorization.


======================================================================
26. NO PUSH
======================================================================

Do not push any repository.

Expected:

    PUSH_PERFORMED=NO


======================================================================
27. REQUIRED REPORT
======================================================================

Return:

STEP=
GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27

STATUS=
DEPLOYED_READY_FOR_OWNER_FINAL_SMOKE
or
BLOCKED


SOURCE:

GM_EXPENSES_HEAD=
39a2adf4dfff0196208a1f80719be1c12c047ac2

GYSTIGO_HEAD=
5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc

FABRIC_HEAD=
1f5bed831c54d01efe74444f02ee2b2d947df549

COMMITTED_BYTES_MATCH_ACCEPTED_EVIDENCE=
YES/NO


BACKUP:

BACKUP_CREATED=
YES/NO

BACKUP_PATH=

BACKUP_SHA256=

RESTORE_VALIDATION=
PASS/FAIL


MIGRATION:

PREVIOUS_SHARED_DEV_VERSION=
64

CURRENT_SHARED_DEV_VERSION=
65

V65_RESULT=
PASS/FAIL

TOTAL_EXPENSE_CASES=

CASES_WITH_EXPENSE_SEQUENCE=

NULL_EXPENSE_SEQUENCE=

DUPLICATE_TENANT_EXPENSE_SEQUENCE=


REAL_NUMBERING:

COMPRA_FILTRO_EXPENSE_SEQUENCE=

COMPRA_FILTRO_EXP_DISPLAY=

COMPRA_FILTRO_ID=

VIAJE_QUITO_EXPENSE_SEQUENCE=

VIAJE_QUITO_EXP_DISPLAY=

VIAJE_QUITO_ID=


NUMBERING_RULES:

EXP_SOURCE=
expenseSequence

EXP_RESETS_DAILY=
NO

ID_SOURCE=
caseNumber

ID_FORMAT=
YYYYMMDD####

EXP_USES_CASE_SEQUENCE=
NO

EXP_USES_LIST_POSITION=
NO


FINANCIAL_INTEGRITY:

FINANCIAL_HISTORY_CHANGED_BY_V65=
NO

OWNER_CASE_RETURN_HISTORY_PRESERVED=
YES/NO


BUILD:

GM_EXPENSES_BUILD=
PASS/FAIL

GM_EXPENSES_JAR_SHA256=

BACKEND_BUILD=
PASS/FAIL

BACKEND_IMAGE_TAG=

BACKEND_IMAGE_ID=


RUNTIME:

FRONTEND_RUNTIME_SOURCE=

BACKEND_RUNTIME_SOURCE=

GM_EXPENSES_RUNTIME_SOURCE=

DATABASE_FLYWAY_VERSION=
65

BACKEND_HEALTH=
PASS/FAIL


API:

LIST_HAS_EXPENSE_SEQUENCE=
YES/NO

DETAIL_HAS_EXPENSE_SEQUENCE=
YES/NO

LIST_HAS_CASE_NUMBER=
YES/NO

DETAIL_HAS_CASE_NUMBER=
YES/NO


REAL_UI:

REAL_APP_URL=
http://localhost:5173

COMPRA_FILTRO_CARD_TITLE=

COMPRA_FILTRO_CARD_ID=

VIAJE_QUITO_CARD_TITLE=

VIAJE_QUITO_CARD_ID=

CARD_DETAIL_EXP_CONSISTENCY=
YES/NO

CARD_DETAIL_ID_CONSISTENCY=
YES/NO


FINANCIAL_DISPLAY_BEFORE_REVERSAL:

TOTAL_ADVANCES=

TOTAL_EXPENSES=

TOTAL_TO_RECONCILE=

RETURNED=

REIMBURSED=

PENDING=

USED=

USAGE=


REVERSAL:

RETURN_200_REVERSIBLE=
YES/NO

RETURN_100_REVERSIBLE=
YES/NO

OWNER_REVERSALS_EXECUTED=
NO


SMOKE:

SMOKE_CHECKS=

SMOKE_FAILURES=

HTTP_5XX_COUNT=

TENANT_ISOLATION=

UUID_ROUTES_PRESERVED=


SOURCE_CONTROL:

NEW_SOURCE_COMMITS_CREATED=
0

PUSH_PERFORMED=
NO

UNRELATED_WIP_PRESERVED=
YES/NO


NEXT_ACTION=

Owner visually confirms real EXP numbers at localhost:5173.

Then Owner performs authenticated reversal of Return USD 200 and USD 100.

After both reversals expected:

    Devuelto = 0
    Pendiente = 80 Por reembolsar


STOP_FOR_OWNER_FINAL_SMOKE=
YES

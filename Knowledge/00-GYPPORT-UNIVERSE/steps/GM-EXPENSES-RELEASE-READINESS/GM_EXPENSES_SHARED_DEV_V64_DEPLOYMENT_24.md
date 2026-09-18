# GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24
MODE=PREDEPLOYMENT_PROOF_BACKUP_MIGRATION_BUILD_DEPLOY_VERIFY
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner runtime activation after GM_EXPENSES_CONTROLLED_COMMIT_GATE_23
ACCEPTED_BASELINE=gm-expenses 874a3e5, Gystigo 0293ff4, Fabric 018ea84, Shared DEV V63 before this STEP
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES SHARED DEV V64 DEPLOYMENT
FINAL OWNER RUNTIME ACTIVATION

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24

MODE=
PREDEPLOYMENT_PROOF
→ BACKUP
→ V64 MIGRATION
→ BUILD_FROM_COMMITTED_BYTES
→ DEPLOY
→ RUNTIME_PROVENANCE
→ OWNER-SMOKE VERIFICATION

OWNER_AUTHORIZED=YES

PUSH_AUTHORIZED=NO


======================================================================
0. PURPOSE
======================================================================

STEP 23 successfully created the three controlled LOCAL commits.

The source is now frozen and accepted for deployment.

Current committed heads:

gm-expenses:
    874a3e5071e46b179444730089d34afa5fe0e742

Gystigo:
    0293ff45e94b2ebbec67e792fea28e7b80bc8901

Fabric:
    018ea843b6bbb86f4e47c3ad43edb42ac7f7ffe5


Current runtime is intentionally still old:

    Shared DEV = V63

    backend source =
    STEP 18 / Gystigo bcb9591

    gm-expenses runtime source =
    545eae0


This explains why the Owner still sees:

    VIAJE QUITO
    Fecha: 2026-09-17

instead of:

    EXP. 01: VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170001


This STEP must deploy the committed STEP 22/22A implementation.

Do NOT modify source code.

Do NOT create new functional changes.

Do NOT push.


======================================================================
1. STRICT SOURCE BASELINE
======================================================================

Before deployment prove exact commits.

GM_EXPENSES:

    branch = master
    HEAD =
    874a3e5071e46b179444730089d34afa5fe0e742


GYSTIGO:

    branch =
    feature/gm-fleets-minimum-vehicle-master-01

    HEAD =
    0293ff45e94b2ebbec67e792fea28e7b80bc8901


FABRIC:

    branch = main

    HEAD =
    018ea843b6bbb86f4e47c3ad43edb42ac7f7ffe5


If any expected HEAD differs:

    STOP.


Unrelated WIP may remain in Gystigo/Fabric.

Do NOT touch it.


======================================================================
2. NO SOURCE EDITING
======================================================================

This is deployment only.

Do NOT edit:

- Java;
- JSX;
- CSS;
- migrations;
- tests;
- application configuration tracked in git;
- Fabric canonical rules.

If deployment exposes a functional defect:

    STOP
    report it

instead of repairing source inside this STEP.


======================================================================
3. RECONFIRM ACCEPTED EVIDENCE
======================================================================

Accepted evidence tied to committed bytes:

gm-expenses:
    773/773 PASS

Host real DB:
    106/106 PASS

Studio:
    648/648 PASS

ESLint:
    PASS

V64 rehearsal:
    PASS

Concurrent sequence test:
    PASS

Responsive:
    1280 PASS
    768 PASS
    375 PASS
    320 PASS


Prove current committed production/test/V64 bytes still correspond to that
evidence.

Do not rerun all suites unless committed bytes differ.

Require:

    COMMITTED_BYTES_MATCH_ACCEPTED_EVIDENCE=YES


======================================================================
4. PRE-DEPLOY SHARED DEV STATE
======================================================================

Before modifying Shared DEV, record:

    database name
    Flyway version
    migration history latest row
    ExpenseCase count
    settlement event count
    expense count
    advance count


Current expected:

    Flyway = V63


Also read-only verify the Owner Case:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0


Expected before deployment:

    stored Return events = 2
    net Return = USD 300.00


Do NOT correct the Owner Case yet.


======================================================================
5. FRESH BACKUP — REQUIRED
======================================================================

Before V64:

create a NEW Shared DEV database backup.

Do not rely solely on STEP 18 backup.


Verify:

- backup command succeeded;
- output exists;
- output non-empty;
- restore validation on disposable schema/database succeeds.


Record:

    BACKUP_PATH
    BACKUP_SIZE
    BACKUP_SHA256
    RESTORE_VALIDATION


If restore validation fails:

    STOP.

Do not migrate.


======================================================================
6. V64 MIGRATION PROVENANCE
======================================================================

V64 must come from committed Gystigo HEAD:

    0293ff45e94b2ebbec67e792fea28e7b80bc8901


Verify migration hash against the file committed in STEP 23.

Expected V64 purpose:

- case_business_date
- case_sequence
- case_number
- sequence/counter persistence
- deterministic historical backfill
- uniqueness
- immutability protection


It must NOT:

- fabricate Establishments;
- fabricate RUC;
- alter settlement balance history;
- rewrite Expense approvals;
- change Advances;
- reuse SRI document sequences.


Require:

    V64_COMMITTED_BYTE_VERIFIED=YES


======================================================================
7. APPLY V64 TO SHARED DEV
======================================================================

Apply the normal canonical Flyway migration path to:

    Shared DEV


Expected:

    V63 → V64


Do not manually execute pieces of V64 out of band.


After migration verify:

    Flyway current = 64
    migration success = YES
    failed migrations = 0


Require:

    SHARED_DEV_VERSION=V64


======================================================================
8. VERIFY V64 DATA RESULT
======================================================================

After migration verify every ExpenseCase has the expected business-number
fields according to V64 rules.


Return:

    EXPENSE_CASE_COUNT
    CASES_WITH_BUSINESS_DATE
    CASES_WITH_CASE_SEQUENCE
    CASES_WITH_CASE_NUMBER
    NULL_CASE_NUMBERS
    DUPLICATE_TENANT_CASE_NUMBERS


Expected:

    NULL_CASE_NUMBERS=0
    DUPLICATE_TENANT_CASE_NUMBERS=0


For the Owner target Case verify:

    UUID =
    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0


Expected:

    businessDate = 2026-09-17
    caseSequence = 1
    caseNumber = 202609170001


Do NOT infer.

Read the actual migrated result.


======================================================================
9. VERIFY EXP / ID SINGLE SOURCE
======================================================================

Canonical relationship:

    caseSequence = 1
        ↓
    EXP. 01

and:

    businessDate = 2026-09-17
    caseSequence = 1
        ↓
    caseNumber = 202609170001


No second EXP counter exists.

No list-position numbering exists.


Confirm migration/runtime data supports:

    SINGLE_SEQUENCE_SOURCE=case_sequence


======================================================================
10. VERIFY FINANCIAL DATA WAS NOT ALTERED BY V64
======================================================================

Compare pre/post migration counts/checksums or equivalent accepted proof for
financial tables.

Require no business financial mutation caused by V64.


At minimum verify unchanged:

- Advances;
- Expenses;
- Expense review history;
- settlement/rendition records;
- settlement_balance_event;
- Return/Reimbursement history.


The Owner Case must STILL contain its original stored Return events after V64.

Expected immediately after migration:

    raw stored Return = USD 300.00


This is correct until the authenticated reversal is performed later.


======================================================================
11. BUILD GM-EXPENSES FROM COMMITTED HEAD
======================================================================

Build/install gm-expenses from:

    874a3e5071e46b179444730089d34afa5fe0e742


Do not build from stale target output.

Prefer clean build if necessary to prove provenance.


Record:

    jar path
    jar sha256
    source HEAD


Require:

    GM_EXPENSES_BUILD=PASS


======================================================================
12. BUILD BACKEND FROM COMMITTED GYSTIGO HEAD
======================================================================

Build official backend from:

    Gystigo
    0293ff45e94b2ebbec67e792fea28e7b80bc8901


using the committed gm-expenses artifact.


Create a new explicit DEV image tag.

Example intent:

    gystigo-backend:4.1.0-java25-gm-expenses-v64-0293ff4


Do NOT overwrite provenance silently.


Add/verify image labels where current project process supports them:

    gypport.source.gystigo=
    0293ff45...

    gypport.source.gm-expenses=
    874a3e5...

    gypport.step=
    GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24


Record final:

    IMAGE_TAG
    IMAGE_ID


======================================================================
13. DEPLOY OFFICIAL BACKEND
======================================================================

Replace only the official Shared DEV backend runtime.

Target:

    localhost:8080


Database remains:

    Shared DEV V64


Preserve the existing infrastructure architecture.


Do NOT:

- start a second unofficial backend on another port as the final solution;
- point Studio at the personal 3310 database;
- mutate frontend source.


After start verify:

    container/process healthy
    backend ready
    database connected
    Flyway sees V64


======================================================================
14. RUNTIME PROVENANCE — MANDATORY
======================================================================

After deployment prove:

Studio:

    localhost:5173
    current Gystigo Studio working tree


Backend:

    localhost:8080
    new STEP 24 image


Database:

    Shared DEV V64


Return:

    FRONTEND_RUNTIME_SOURCE=
    BACKEND_RUNTIME_SOURCE=
    GM_EXPENSES_RUNTIME_SOURCE=
    DATABASE_FLYWAY_VERSION=


Expected:

    BACKEND_RUNTIME_SOURCE=
    0293ff45...

    GM_EXPENSES_RUNTIME_SOURCE=
    874a3e50...

    DATABASE_FLYWAY_VERSION=
    64


======================================================================
15. API FIELD VERIFICATION
======================================================================

Verify the running deployed backend now supports:

    caseSequence
    caseNumber
    businessDate


Use an authorized test/session path available in the existing test tooling.

Do not ask for or expose Owner credentials.


For a controlled authenticated test fixture prove:

    LIST_HAS_CASE_SEQUENCE=YES
    LIST_HAS_CASE_NUMBER=YES
    LIST_HAS_BUSINESS_DATE=YES

    DETAIL_HAS_CASE_SEQUENCE=YES
    DETAIL_HAS_CASE_NUMBER=YES
    DETAIL_HAS_BUSINESS_DATE=YES


If safe authenticated inspection of the real Owner Case is available through
existing session/tooling, verify actual values.

Otherwise use database read-only proof + automated API test evidence and
report the limitation accurately.


======================================================================
16. REAL STUDIO RUNTIME — OWNER SCREEN
======================================================================

Now verify the REAL application:

    http://localhost:5173


Do NOT use the 5189 synthetic fixture as the primary proof.


Target migrated Case should render:

    EXP. 01: VIAJE QUITO

    Fecha: 2026-09-17

    ID: 202609170001


Then divider.


Then:

    Responsable:       Eduardo Burgasí
    Supervisor:        Eduardo Burgasí
    Recurso asignado:  Sin recurso


With:

    Conciliado

on the right of the Assignment section.


Then divider.


Then:

    Finanzas


======================================================================
17. IMPORTANT — CURRENT FINANCE MAY STILL SHOW 300 / 380
======================================================================

After deployment, before reversing the historical mistaken Return, the REAL
Owner Case is expected to continue showing:

    Total anticipos = 320
    Total gastos = 400
    Total a conciliar = 80 Por reembolsar

but also:

    Devuelto = 300
    Pendiente = 380 Por reembolsar


That is EXPECTED because the historical incorrect Return events still exist.


Do NOT misdiagnose this as deployment failure.


The important deployment proof is:

- correct backend fields;
- correct ID Gasto;
- correct EXP numbering;
- correct base reconciliation;
- reversal action available.


======================================================================
18. RETURN REVERSAL UI AVAILABILITY
======================================================================

After deployment verify the authenticated product supports reversing the two
stored Return events.

Originals:

    USD 200
    USD 100


Verify UI/API capability exists to reverse each one with:

- explicit target movement;
- required reason;
- confirmation;
- authenticated actor;
- append-only reversal;
- immutable original.


Do NOT execute the reversals automatically.


The Owner must perform them through the product after deployment.


======================================================================
19. EXPECTED POST-REVERSAL RESULT
======================================================================

After the Owner later reverses both movements:

    original Return 200
    reversal 200

    original Return 100
    reversal 100


net:

    Devuelto = USD 0.00


Then expected financial state:

    Total anticipos
    USD 320.00

    Total gastos
    USD 400.00

    Total a conciliar
    USD 80.00
    Por reembolsar

    Devuelto
    USD 0.00

    Reembolsado
    USD 0.00

    Pendiente
    USD 80.00
    Por reembolsar

    Usado
    USD 400.00

    Uso
    125%


Do not perform this Owner action inside this automated deployment STEP.


======================================================================
20. SMOKE TEST
======================================================================

Run the narrow Shared DEV smoke appropriate to this deployment.


Must prove at least:

- backend health;
- authentication path still works using test tooling;
- tenant isolation;
- Case list;
- Case detail;
- caseSequence present;
- caseNumber present;
- businessDate present;
- Expense financial summary;
- Advance list;
- no 5xx;
- UUID route preserved.


Do not rerun unrelated platform regression matrices.


======================================================================
21. NO PUSH
======================================================================

Do not push any repository.

Expected:

    PUSH_PERFORMED=NO


This deployment is from local committed HEADs.


======================================================================
22. DO NOT COMMIT DEPLOYMENT NOISE
======================================================================

Deployment runtime files/logs must not create source commits.

No additional source commit is authorized by this STEP.


If Fabric deployment evidence must be recorded and this project requires a
new local evidence commit, STOP and report that need rather than silently
creating a fourth commit without authorization.


======================================================================
23. REQUIRED FINAL REPORT
======================================================================

Return:


STEP=
GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24


STATUS=
DEPLOYED_READY_FOR_OWNER_SMOKE
or
BLOCKED


--------------------------------------------------
SOURCE
--------------------------------------------------

GM_EXPENSES_HEAD=
874a3e5071e46b179444730089d34afa5fe0e742

GYSTIGO_HEAD=
0293ff45e94b2ebbec67e792fea28e7b80bc8901

FABRIC_HEAD=
018ea843b6bbb86f4e47c3ad43edb42ac7f7ffe5

COMMITTED_BYTES_MATCH_ACCEPTED_EVIDENCE=
YES/NO


--------------------------------------------------
BACKUP
--------------------------------------------------

BACKUP_CREATED=
YES/NO

BACKUP_PATH=

BACKUP_SIZE=

BACKUP_SHA256=

RESTORE_VALIDATION=
PASS/FAIL


--------------------------------------------------
MIGRATION
--------------------------------------------------

PREVIOUS_SHARED_DEV_VERSION=
63

CURRENT_SHARED_DEV_VERSION=
64

V64_RESULT=
PASS/FAIL

EXPENSE_CASE_COUNT=

CASES_WITH_CASE_NUMBER=

NULL_CASE_NUMBERS=

DUPLICATE_TENANT_CASE_NUMBERS=


OWNER_CASE_BUSINESS_DATE=

OWNER_CASE_SEQUENCE=

OWNER_CASE_NUMBER=


EXPECTED_OWNER_CASE_NUMBER=
202609170001


--------------------------------------------------
FINANCIAL DATA INTEGRITY
--------------------------------------------------

FINANCIAL_HISTORY_CHANGED_BY_V64=
NO/YES

OWNER_CASE_RETURN_EVENTS_PRESERVED=
YES/NO

OWNER_CASE_RAW_RETURN_BEFORE_REVERSAL=
USD 300.00


--------------------------------------------------
BUILD
--------------------------------------------------

GM_EXPENSES_BUILD=
PASS/FAIL

GM_EXPENSES_JAR_SHA256=

BACKEND_BUILD=
PASS/FAIL

BACKEND_IMAGE_TAG=

BACKEND_IMAGE_ID=


--------------------------------------------------
RUNTIME
--------------------------------------------------

FRONTEND_RUNTIME_SOURCE=

BACKEND_RUNTIME_SOURCE=

GM_EXPENSES_RUNTIME_SOURCE=

DATABASE_FLYWAY_VERSION=

BACKEND_HEALTH=
PASS/FAIL


--------------------------------------------------
API
--------------------------------------------------

LIST_HAS_CASE_SEQUENCE=
YES/NO

LIST_HAS_CASE_NUMBER=
YES/NO

LIST_HAS_BUSINESS_DATE=
YES/NO

DETAIL_HAS_CASE_SEQUENCE=
YES/NO

DETAIL_HAS_CASE_NUMBER=
YES/NO

DETAIL_HAS_BUSINESS_DATE=
YES/NO


--------------------------------------------------
REAL OWNER UI
--------------------------------------------------

REAL_APP_URL=
http://localhost:5173

OWNER_CARD_EXP_DISPLAY=
EXP. 01 / actual value

OWNER_CARD_DATE=

OWNER_CARD_ID=

EXPECTED_OWNER_CARD_ID=
202609170001

ID_VISIBLE_ON_REAL_APP=
YES/NO

EXP_USES_CASE_SEQUENCE=
YES/NO

IDENTITY_DIVIDER_VISIBLE=
YES/NO

ASSIGNMENT_LAYOUT=
PASS/FAIL

CONCILIADO_ALIGNMENT=
PASS/FAIL

FINANCE_LAYOUT=
PASS/FAIL


--------------------------------------------------
CURRENT FINANCIAL DISPLAY BEFORE REVERSAL
--------------------------------------------------

TOTAL_ADVANCES=

TOTAL_EXPENSES=

TOTAL_TO_RECONCILE=

RETURNED=

REIMBURSED=

PENDING=


EXPECTED_BEFORE_OWNER_REVERSAL=

    320
    400
    80 POR_REEMBOLSAR
    300 RETURNED
    0 REIMBURSED
    380 POR_REEMBOLSAR


--------------------------------------------------
REVERSAL READINESS
--------------------------------------------------

RETURN_200_REVERSIBLE=
YES/NO

RETURN_100_REVERSIBLE=
YES/NO

REVERSAL_REQUIRES_REASON=
YES/NO

REVERSAL_USES_AUTHENTICATED_ACTOR=
YES/NO

OWNER_REVERSALS_EXECUTED=
NO


--------------------------------------------------
SMOKE
--------------------------------------------------

SMOKE_TESTS=

HTTP_5XX_COUNT=

TENANT_ISOLATION=

UUID_ROUTES_PRESERVED=


--------------------------------------------------
SOURCE CONTROL
--------------------------------------------------

NEW_SOURCE_COMMITS_CREATED=
0

PUSH_PERFORMED=
NO

UNRELATED_WIP_PRESERVED=
YES/NO


NEXT_ACTION=

    OWNER verifies:
        EXP. 01
        Fecha
        ID: 202609170001

    then Owner performs authenticated reversal:
        USD 200
        USD 100

    then final financial smoke expects:
        Devuelto 0
        Pendiente 80 Por reembolsar


STOP_FOR_OWNER_SMOKE=
YES

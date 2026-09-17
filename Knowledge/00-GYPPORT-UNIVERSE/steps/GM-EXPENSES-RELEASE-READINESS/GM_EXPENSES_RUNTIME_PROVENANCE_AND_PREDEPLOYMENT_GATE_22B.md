# GM_EXPENSES_RUNTIME_PROVENANCE_AND_PREDEPLOYMENT_GATE_22B — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_RUNTIME_PROVENANCE_AND_PREDEPLOYMENT_GATE_22B
MODE=READ_ONLY_RUNTIME_AUDIT
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner runtime provenance gate after the Owner saw the old values at localhost:5173
ACCEPTED_BASELINE=gm-expenses 545eae0, Gystigo bcb9591, Fabric bbdd66a, Shared DEV V63
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES RUNTIME PROVENANCE GATE

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_RUNTIME_PROVENANCE_AND_PREDEPLOYMENT_GATE_22B

MODE=
READ_ONLY_RUNTIME_AUDIT

OWNER_AUTHORIZED=YES

============================================================
0. PURPOSE
============================================================

STOP implementation.

The Owner is viewing the real application at localhost:5173 and still sees:

    VIAJE QUITO
    Fecha: 2026-09-17

but NOT:

    EXP. 01: VIAJE QUITO
    ID: 202609170001

Do not make another UI change until we prove which frontend and backend are
actually serving the Owner browser.

This STEP is READ-ONLY.

DO NOT:

- edit source;
- stage;
- commit;
- push;
- migrate Shared DEV;
- modify the Owner Case;
- restart into another source tree without first proving current provenance.

============================================================
1. FRONTEND RUNTIME PROVENANCE
============================================================

Identify the exact process listening on:

    localhost:5173

Report:

    PID
    executable
    command line
    current working directory
    Vite root
    repository root
    git branch
    git HEAD

Then prove whether that process is serving the exact current Gystigo Studio
working tree containing STEP 22 / 22A.

Do not infer from filenames.

Prove it from:

- process working directory;
- source paths;
- current bytes/hashes;
- served module if necessary.

Return:

    PORT_5173_PID=
    PORT_5173_CWD=
    PORT_5173_REPO=
    PORT_5173_BRANCH=
    PORT_5173_HEAD=
    PORT_5173_SERVES_CURRENT_WORKTREE=YES/NO

============================================================
2. VERIFY THE ACTUAL CARD SOURCE
============================================================

Locate the exact ExpenseCase card component currently used by the route the
Owner is viewing.

Verify that its current source contains the STEP 22A logic:

    EXP. {caseSequence}
    ID: {caseNumber}

and NOT the old list-position implementation.

Report exact file path.

Return:

    REAL_CARD_COMPONENT=
    CURRENT_SOURCE_HAS_EXP_FROM_CASE_SEQUENCE=YES/NO
    CURRENT_SOURCE_HAS_ID_FROM_CASE_NUMBER=YES/NO

============================================================
3. BACKEND RUNTIME PROVENANCE
============================================================

Identify the API used by the Studio process on 5173.

Report:

    base URL
    backend port
    PID/container
    image if Docker
    git/source commit if known
    Flyway/schema version

Prove whether this is still the STEP 18 backend:

    Gystigo bcb9591...
    Shared DEV V63

or the STEP 22 working-tree backend.

Return:

    STUDIO_API_BASE_URL=
    BACKEND_RUNTIME=
    BACKEND_SOURCE_VERSION=
    DATABASE_TARGET=
    DATABASE_FLYWAY_VERSION=

============================================================
4. INSPECT REAL API PAYLOAD
============================================================

Using the normal authenticated development path, inspect one real Case list
response and the target Case detail response.

Target Case:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0

Do not mutate anything.

Report whether the real running API currently returns:

    caseSequence
    caseNumber
    businessDate

Return the field presence and values only.

Expected from old STEP 18 runtime:

    caseSequence = absent
    caseNumber   = absent
    businessDate = absent

Expected from STEP 22 implementation:

    caseSequence = 1
    caseNumber   = 202609170001
    businessDate = 2026-09-17

Do NOT fabricate values.

============================================================
5. EXPLAIN THE OWNER SCREEN
============================================================

Determine which of these is true:

A.
NEW_STUDIO + OLD_BACKEND

B.
OLD_STUDIO + OLD_BACKEND

C.
WRONG_FRONTEND_WORKTREE

D.
WRONG_BACKEND

E.
BROWSER_CACHE/HMR_STALE

F.
OTHER — prove exactly what

The screenshot already appears to contain some of the new visual grouping,
so explicitly determine whether:

    the frontend visual changes ARE loaded

while:

    the identifier fields are absent because the old API does not provide them.

Return one proven root cause.

============================================================
6. FIXTURE PROVENANCE
============================================================

The previous report referenced:

    localhost:5189/fixtures/expense-case-cards.html
    localhost:5189/fixtures/expense-case-detail.html

Identify exactly what serves 5189.

Make explicit that fixture success does NOT prove the real app at 5173 is
receiving STEP 22 API fields.

Return:

    PORT_5189_PURPOSE=
    PORT_5189_SOURCE=
    FIXTURE_IS_REAL_BACKEND_RUNTIME=YES/NO

============================================================
7. NO NEW IMPLEMENTATION
============================================================

If source code is already correct and the only problem is runtime version
mismatch:

    DO NOT EDIT THE CARD AGAIN.

Report:

    SOURCE_IMPLEMENTATION_CORRECT=YES
    DEPLOYMENT_REQUIRED=YES

If the actual 5173 process is pointing at a different checkout:

    STOP and report exact wrong path.

Do not copy files between repositories.

Do not "fix" by duplicating code.

============================================================
8. SOURCE CONTROL AUDIT
============================================================

Reconfirm exact dirty state in:

    gm-expenses
    Gystigo
    Fabric

Report:

    staged paths
    unstaged paths
    untracked paths
    branch
    HEAD

Confirm whether:

    COMMITS_CREATED_SINCE_STEP_22A=0
    PUSH_PERFORMED=NO

The Owner suspects work may be occurring in another repository/path.

Prove whether that suspicion is true or false.

Search only the relevant known GYPPORT workspace/checkouts.

Return:

    ALTERNATE_WORKTREE_FOUND_WITH_STEP22_CHANGES=YES/NO

If YES:
    exact path
    branch
    HEAD
    reason

If NO:
    state clearly that the implementation exists only in the expected
    working tree.

============================================================
9. DO NOT TOUCH THE 300 RETURN
============================================================

The real Owner Case still has stored Return USD 300.

This audit must NOT change it.

That correction remains after deployment through authenticated reversal.

Return:

    OWNER_CASE_MODIFIED=NO

============================================================
10. REQUIRED FINAL REPORT
============================================================

Return:

STEP=
GM_EXPENSES_RUNTIME_PROVENANCE_AND_PREDEPLOYMENT_GATE_22B

STATUS=
PROVEN


FRONTEND:

PORT_5173_PID=
PORT_5173_CWD=
PORT_5173_REPO=
PORT_5173_BRANCH=
PORT_5173_HEAD=

PORT_5173_SERVES_CURRENT_WORKTREE=
YES/NO

REAL_CARD_COMPONENT=

CURRENT_SOURCE_HAS_EXP_FROM_CASE_SEQUENCE=
YES/NO

CURRENT_SOURCE_HAS_ID_FROM_CASE_NUMBER=
YES/NO


BACKEND:

STUDIO_API_BASE_URL=

BACKEND_RUNTIME=

BACKEND_SOURCE_VERSION=

DATABASE_TARGET=

DATABASE_FLYWAY_VERSION=


REAL_API:

LIST_HAS_CASE_SEQUENCE=
YES/NO

LIST_CASE_SEQUENCE=

LIST_HAS_CASE_NUMBER=
YES/NO

LIST_CASE_NUMBER=

LIST_HAS_BUSINESS_DATE=
YES/NO

LIST_BUSINESS_DATE=

DETAIL_HAS_CASE_SEQUENCE=
YES/NO

DETAIL_CASE_SEQUENCE=

DETAIL_HAS_CASE_NUMBER=
YES/NO

DETAIL_CASE_NUMBER=

DETAIL_HAS_BUSINESS_DATE=
YES/NO

DETAIL_BUSINESS_DATE=


ROOT_CAUSE=

RUNTIME_COMBINATION=
NEW_STUDIO_OLD_BACKEND /
OLD_STUDIO_OLD_BACKEND /
WRONG_WORKTREE /
WRONG_BACKEND /
CACHE /
OTHER


FIXTURE:

PORT_5189_PURPOSE=

FIXTURE_IS_REAL_BACKEND_RUNTIME=
YES/NO


SOURCE_CONTROL:

GM_EXPENSES_BRANCH=
GM_EXPENSES_HEAD=

GYSTIGO_BRANCH=
GYSTIGO_HEAD=

FABRIC_BRANCH=
FABRIC_HEAD=

FILES_STAGED=

COMMITS_CREATED_SINCE_STEP22A=
0

PUSH_PERFORMED=
NO

ALTERNATE_WORKTREE_FOUND_WITH_STEP22_CHANGES=
YES/NO


SOURCE_IMPLEMENTATION_CORRECT=
YES/NO

DEPLOYMENT_REQUIRED=
YES/NO

OWNER_CASE_MODIFIED=
NO


NEXT_ACTION=

STOP_FOR_OWNER_REVIEW=
YES

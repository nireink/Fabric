# GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26
MODE=CONTINUE_FROM_CURRENT_STEP_THEN_CONTROLLED_COMMIT
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner controlled commit gate for the V65 and 25A work, stopping before deployment
ACCEPTED_BASELINE=gm-expenses 874a3e5, Gystigo 0293ff4, Fabric 018ea84, Shared DEV V64
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — CONTINUE GM-EXPENSES V65 FROM CURRENT CHECKPOINT

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26

MODE=
CONTINUE_FROM_CURRENT_STEP
→ VERIFY_EXISTING_V65_WORK
→ CONTROLLED_COMMIT
→ STOP_BEFORE_DEPLOYMENT

OWNER_AUTHORIZED=YES

PUSH_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO


============================================================
0. CONTINUITY — DO NOT RESTART
============================================================

Continue from the existing workspace and CURRENT_STEP.

DO NOT recreate STEP 25.

DO NOT recreate STEP 25A.

DO NOT redesign EXP numbering.

DO NOT change Studio unless a byte/evidence mismatch proves a real defect.

The Owner's real screen currently shows:

    VIAJE QUITO
    Fecha: 2026-09-17
    ID: 202609170002

without:

    EXP. NN:

This is EXPECTED because the real backend on localhost:8080 is still the
deployed V64 runtime and does not emit expenseSequence.

STEP 25A already proved:

    EXP_SOURCE=expenseSequence
    CARD_EXP_VISIBLE=YES in V65 fixture
    DETAIL_EXP_VISIBLE=YES in V65 fixture
    STUDIO_TESTS=652/652
    ESLINT=PASS

Therefore:

    DO NOT FIX THE CARD AGAIN.

The missing EXP prefix in the real application is a DEPLOYMENT STATE issue.


============================================================
1. FINAL CANONICAL NUMBERING — FROZEN
============================================================

These rules are FINAL and MUST NOT be reinterpreted:

UUID
    = technical resource identifier

expense_sequence
    = permanent tenant-scoped expediente sequence
    = NEVER resets by date
    = source of EXP. NN

case_sequence
    = tenant + business-date daily sequence
    = used only for case_number
    = NOT source of EXP

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


Valid independent identifiers:

    EXP. 01: VIAJE QUITO
    ID: 202609170002

    EXP. 02: Compra Filtro
    ID: 202609170001


The real Shared DEV historical backfill may result in:

    Compra Filtro → EXP. 08
    Viaje Quito   → EXP. 09

if that is their actual creation chronology.

Do NOT force fixture values into real data.


============================================================
2. AUDIT CURRENT CHECKPOINT FIRST
============================================================

Read:

    Fabric/active-work/CURRENT_STEP.md

and the latest STEP 25 / STEP 25A evidence.

Then verify exact current state of:

    gm-expenses
    Gystigo
    Fabric


Report:

    branch
    HEAD
    dirty paths
    staged paths


Expected committed baseline before V65:

gm-expenses:
    874a3e5071e46b179444730089d34afa5fe0e742

Gystigo:
    0293ff45e94b2ebbec67e792fea28e7b80bc8901

Fabric:
    018ea843b6bbb86f4e47c3ad43edb42ac7f7ffe5


Do NOT assume counts from an older report.

Use the actual workspace.


============================================================
3. CONFIRM EXISTING V65 WORK IS PRESENT
============================================================

Prove the current uncommitted V65 implementation already contains:

- permanent expense_sequence;
- tenant-scoped permanent sequence allocator;
- V65 migration;
- deterministic historical backfill;
- UNIQUE tenant + expense_sequence;
- immutable expense_sequence;
- real-DB concurrency protection;
- Host/API expenseSequence;
- Card EXP source = expenseSequence;
- Detail EXP source = expenseSequence;
- EXP formatting minimum 2 digits;
- ID source = caseNumber.


Require:

    EXISTING_V65_IMPLEMENTATION_PRESENT=YES

If YES:

    DO NOT REIMPLEMENT.

If NO:

    STOP and report exact missing bytes.


============================================================
4. V64 MUST REMAIN UNCHANGED
============================================================

V64 is already deployed.

Prove:

    V64 byte/hash unchanged.

Do NOT edit V64.

V65 must be the only new migration for permanent EXP numbering.


============================================================
5. REUSE GREEN EVIDENCE WHEN BYTES MATCH
============================================================

Existing accepted evidence includes:

STEP 25A:

    STUDIO=652/652 PASS
    ESLINT=PASS
    responsive 1280/768/375/320 PASS


STEP 25 V65 implementation:

    V64→V65 rehearsal PASS
    permanent-sequence concurrency PASS
    financial integrity unchanged
    affected domain/Host tests green


If current tested bytes are identical:

    REUSE evidence.

Do NOT rerun suites merely because Claude restarted or the previous agent
session ended.

Only rerun tests invalidated by changed bytes.


============================================================
6. WORKTREE CLASSIFICATION
============================================================

Classify every current dirty path as:

A.
V65 accepted implementation

B.
STEP 25A accepted Studio correction

C.
STEP 24 deployment evidence

D.
STEP 25 / 25A documentation/evidence

E.
unrelated pre-existing WIP

F.
generated/runtime

G.
unknown


Require:

    UNKNOWN=0


Preserve all unrelated WIP untouched.


============================================================
7. CONTROLLED COMMIT — GM-EXPENSES FIRST
============================================================

Stage ONLY explicit accepted gm-expenses V65 paths.

STRICTLY FORBIDDEN:

    git add .
    git add -A
    git add -u


Prove:

    git diff --cached --name-status
    git diff --cached --check


No unrelated path may be staged.


Commit intent:

    gm-expenses: add permanent expediente sequence


Record:

    new HEAD


Then build/install from the committed HEAD.

Require:

    build PASS


============================================================
8. CONTROLLED COMMIT — GYSTIGO SECOND
============================================================

Stage ONLY accepted Gystigo V65/25A paths:

- V65 migration;
- sequence persistence/wiring;
- Host/API expenseSequence;
- tests;
- Card EXP rendering;
- Detail EXP rendering;
- fixtures/contracts.


Do NOT stage unrelated Gystigo WIP.


Prove staged paths exactly.

Commit intent:

    gystigo: use permanent expediente numbering


Record:

    new HEAD


============================================================
9. CONTROLLED COMMIT — FABRIC THIRD
============================================================

Stage only accepted Fabric paths for:

- STEP 24 deployment evidence;
- STEP 25 prompt/evidence;
- STEP 25A prompt/evidence;
- canonical numbering decision;
- append-only Reglas.md;
- CURRENT_STEP;
- release-readiness evidence.


Do NOT stage unrelated Fabric Knowledge WIP.


Commit intent:

    fabric: record permanent expediente numbering


Record:

    new HEAD


============================================================
10. POST-COMMIT PROOF
============================================================

After all three commits require:

    ACCEPTED_UNCOMMITTED_PATHS=0
    UNKNOWN_PATHS=0

Unrelated WIP may remain dirty.


Verify from COMMITTED source:

    EXP source = expenseSequence

    ID source = caseNumber

    EXP resets daily = NO

    ID daily sequence resets = YES


Examples must still pass:

    1 → EXP. 01
    2 → EXP. 02
    100 → EXP. 100


============================================================
11. DO NOT DEPLOY YET
============================================================

This STEP ends after the controlled local commits.

DO NOT:

- migrate Shared DEV V64→V65;
- rebuild official backend;
- restart localhost:8080;
- modify Owner Case;
- reverse the USD 300;
- push.


The real browser may therefore STILL show:

    VIAJE QUITO

without EXP.

That remains expected until the NEXT STEP.


============================================================
12. CURRENT_STEP
============================================================

After successful commits, set continuity to:

    NEXT_STEP=
    GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27


Current actual runtime must still be recorded as:

    Shared DEV V64
    V65_DEPLOYED=NO


============================================================
13. REQUIRED REPORT
============================================================

Return:

STEP=
GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26

STATUS=
OWNER_REVIEW_REQUIRED
or
BLOCKED


CONTINUITY:

PREVIOUS_STEP_25_FOUND=
YES/NO

PREVIOUS_STEP_25A_FOUND=
YES/NO

EXISTING_V65_IMPLEMENTATION_PRESENT=
YES/NO

REIMPLEMENTED_FROM_SCRATCH=
NO


NUMBERING:

EXP_SOURCE=
expenseSequence

EXP_SCOPE=
TENANT

EXP_RESETS_DAILY=
NO

EXP_SEQUENCE_1_DISPLAY=
EXP. 01

EXP_SEQUENCE_2_DISPLAY=
EXP. 02

EXP_SEQUENCE_100_DISPLAY=
EXP. 100

ID_SOURCE=
caseNumber

ID_FORMAT=
YYYYMMDD####


PRE_COMMIT:

GM_EXPENSES_OLD_HEAD=
GYSTIGO_OLD_HEAD=
FABRIC_OLD_HEAD=

CURRENT_DIRTY_PATHS=
ACCEPTED_PATHS=
UNRELATED_WIP_PATHS=
UNKNOWN_PATHS=

V64_UNCHANGED=
YES/NO

TESTED_BYTES_UNCHANGED=
YES/NO


COMMITS:

GM_EXPENSES_COMMITTED=
YES/NO

GM_EXPENSES_NEW_HEAD=

GYSTIGO_COMMITTED=
YES/NO

GYSTIGO_NEW_HEAD=

FABRIC_COMMITTED=
YES/NO

FABRIC_NEW_HEAD=


EVIDENCE:

GM_EXPENSES_TESTS=

HOST_REAL_DB=

STUDIO=
652/652 PASS REUSED/RERUN

ESLINT=
PASS REUSED/RERUN

V64_TO_V65_REHEARSAL=
PASS REUSED/RERUN

PERMANENT_SEQUENCE_CONCURRENCY=
PASS REUSED/RERUN


POST_COMMIT:

ACCEPTED_UNCOMMITTED_PATHS=
0

UNKNOWN_POST_COMMIT_PATHS=
0

UNRELATED_WIP_PRESERVED=
YES/NO


RUNTIME:

SHARED_DEV_VERSION=
64

V65_DEPLOYED=
NO

REAL_APP_EXPECTED_TO_SHOW_EXP_BEFORE_DEPLOYMENT=
NO

OWNER_CASE_MODIFIED=
NO


OPERATIONS:

FILES_STAGED_AFTER_GATE=
0

PUSH_PERFORMED=
NO

DEPLOYMENT_PERFORMED=
NO


NEXT_STEP=
GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27

READY_FOR_V65_DEPLOYMENT=
YES/NO

STOP_FOR_OWNER_REVIEW=
YES

# GM_EXPENSES_CONTROLLED_COMMIT_GATE_23 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_CONTROLLED_COMMIT_GATE_23
MODE=READ_ONLY_PRECOMMIT_AUDIT_THEN_EXPLICIT_STAGING_THEN_COMMIT
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner controlled commit gate after GM_EXPENSES_RUNTIME_PROVENANCE_AND_PREDEPLOYMENT_GATE_22B
ACCEPTED_BASELINE=gm-expenses 545eae0, Gystigo bcb9591, Fabric bbdd66a, Shared DEV V63
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES CONTROLLED COMMIT GATE
FINAL MVP CLOSURE SOURCE FREEZE

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_CONTROLLED_COMMIT_GATE_23

MODE=
READ_ONLY_PRECOMMIT_AUDIT
→ EXPLICIT_PATH_STAGING
→ COMMIT
→ POST_COMMIT_PROOF

OWNER_AUTHORIZED=YES

PUSH_AUTHORIZED=NO
SHARED_DEV_DEPLOYMENT_AUTHORIZED=NO


======================================================================
0. PURPOSE
======================================================================

STEP 22B proved:

    SOURCE_IMPLEMENTATION_CORRECT=YES
    DEPLOYMENT_REQUIRED=YES

The real runtime mismatch is:

    NEW_STUDIO + OLD_BACKEND

There is no alternate worktree.

Do NOT make any further functional or visual implementation change.

This STEP exists only to:

1. audit the accumulated accepted working-tree changes;
2. distinguish accepted work from unrelated pre-existing WIP;
3. stage ONLY accepted explicit paths;
4. prove staged bytes are exactly the verified bytes;
5. create controlled local commits in:
       gm-expenses
       Gystigo
       Fabric
6. prove the resulting commits;
7. stop before deployment.

No push.
No Shared DEV migration.
No Owner Case mutation.


======================================================================
1. VERIFIED PRE-COMMIT BASELINE
======================================================================

Expected pre-commit repository state:

GM_EXPENSES:

    repo:
    Modules/gm-expenses

    branch:
    master

    HEAD:
    545eae0fb287f8e04f7f1b4ac73780304ec53f22


GYSTIGO:

    repo:
    Gystigo

    branch:
    feature/gm-fleets-minimum-vehicle-master-01

    HEAD:
    bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f


FABRIC:

    repo:
    Fabric

    branch:
    main

    HEAD:
    bbdd66a0c5a1c9cbb21293beb74c3e5e61cc5de0


If any branch or HEAD differs:

    STOP.

Do not stage.
Do not commit.

Report exact drift.


======================================================================
2. ACCEPTED IMPLEMENTATION CHAIN
======================================================================

The commit gate must preserve the accepted work from:

    STEP 19
    STEP 20
    STEP 20A
    STEP 21
    STEP 21 addendum
    STEP 22
    STEP 22A
    STEP 22B evidence/continuity

Relevant accepted capabilities include:

- final Expense financial semantics;
- rejected Expense financial effect = ZERO;
- delivered Advance counting;
- base reconciliation;
- Return/Reimbursement movement model;
- append-only movement reversal capability;
- Card financial hierarchy;
- Detail financial hierarchy;
- Card/Detail consistency contracts;
- header Identity / Assignment / Finance hierarchy;
- V64 ExpenseCase business numbering;
- case_business_date;
- case_sequence;
- case_number;
- tenant + business-date sequence;
- concurrency-safe sequence allocator;
- historical backfill;
- caseNumber immutability;
- API caseSequence/caseNumber/businessDate;
- Studio ID display;
- EXP derived from case_sequence;
- no list-position EXP numbering;
- detail/card identifier consistency;
- responsive proofs;
- canonical documentation/evidence;
- CURRENT_STEP continuity.

Do NOT reinterpret these decisions during the commit gate.


======================================================================
3. CURRENT RUNTIME FACT — DO NOT "FIX"
======================================================================

Current real runtime is intentionally still:

Studio:

    localhost:5173
    current working tree

Backend:

    localhost:8080
    STEP 18 image

Database:

    Shared DEV V63


Therefore the real Owner screen currently does NOT show:

    EXP. 01
    ID: 202609170001

because the deployed backend does not emit those fields.

This is expected.

Do NOT edit source to compensate.

Do NOT add a fake Studio-generated ID.

Do NOT deploy in this STEP.


======================================================================
4. MANDATORY DIRTY-WORKTREE RE-AUDIT
======================================================================

Before staging anything, obtain exact:

    git branch
    git rev-parse HEAD
    git status --short
    git diff --name-status
    git diff --stat

for:

    gm-expenses
    Gystigo
    Fabric


Reconcile every dirty path against the latest accepted classification.

Classify each as:

A.
GM_EXPENSES_ACCEPTED

B.
GYSTIGO_ACCEPTED

C.
FABRIC_ACCEPTED

D.
UNRELATED_PREEXISTING_WIP

E.
GENERATED_RUNTIME

F.
UNKNOWN


Require:

    UNKNOWN=0


Do NOT trust an old count blindly.

The exact current count may differ from earlier reports because STEP 22A/22B
added evidence or source paths.

Use the current filesystem as authority while preserving the prior
classification decisions.


======================================================================
5. UNRELATED WIP MUST REMAIN UNTOUCHED
======================================================================

Prior audits identified unrelated WIP including, among others:

Gystigo:

- README deletion;
- onboarding/AuthPage.css;
- ShortRegisterPage.jsx;
- unrelated branding fixtures;

Fabric:

- unrelated historical/untracked Knowledge paths from earlier work.


Reconfirm exact paths.

Do NOT:

- stage them;
- delete them;
- restore them;
- modify them;
- normalize them;
- move them.

The final post-commit worktree may remain dirty because these unrelated paths
must survive untouched.


======================================================================
6. NO BROAD STAGING COMMANDS
======================================================================

STRICTLY FORBIDDEN:

    git add .
    git add -A
    git add -u
    git add --all


Stage ONLY explicit accepted paths.

Prefer a generated reviewed path list and then explicit path-scoped staging.


Before each commit prove:

    git diff --cached --name-status

contains exactly the intended accepted files for that repository.


======================================================================
7. PRE-COMMIT BYTE PROOF
======================================================================

For every accepted path that was previously tested/verified:

prove the current working-tree byte is the same byte represented by the
latest accepted STEP evidence.

Where evidence contains hashes:

    compare hashes.

Where no explicit hash exists:

    compare current diff against the accepted STEP scope/evidence.


If any accepted production/test/migration file changed after its final passing
test:

    STOP.

Do not commit stale evidence.

Report:

    INVALIDATED_TEST_EVIDENCE=YES

and exact files.


======================================================================
8. V64 PRE-COMMIT PROOF
======================================================================

Verify:

    migration head before commit = V64 in source working tree

V64 must contain ONLY the accepted ExpenseCase numbering work.

Prove V64 still implements:

    case_business_date
    case_sequence
    case_number
    tenant + business-date numbering
    deterministic backfill
    uniqueness
    immutability
    required sequence/counter persistence


Prove V64 does NOT:

- fabricate establishment;
- introduce RUC;
- rewrite financial events;
- touch Return/Reimbursement history;
- reuse SRI document sequences.


The previously passed disposable rehearsal may be reused if the V64 bytes are
identical.


Return:

    V64_BYTES_UNCHANGED_SINCE_REHEARSAL=YES/NO


======================================================================
9. TEST-EVIDENCE VALIDITY
======================================================================

Latest accepted evidence:

GM_EXPENSES:

    773/773 PASS


HOST REAL DB:

    106/106 PASS


STUDIO:

    648/648 PASS


ESLINT:

    PASS


V64 REHEARSAL:

    PASS


CONCURRENT SEQUENCE:

    PASS


RESPONSIVE:

    1280 PASS
    768 PASS
    375 PASS
    320 PASS


Do NOT rerun these merely because a commit will be created.

Before committing, determine whether any tested byte has changed since these
results.

If:

    TESTED_BYTES_UNCHANGED=YES

reuse the baseline.

If:

    TESTED_BYTES_UNCHANGED=NO

run ONLY the invalidated affected verification before committing.


======================================================================
10. SECRET / SENSITIVE DATA GATE
======================================================================

Before staging/commit, scan accepted diff for accidental:

- passwords;
- tokens;
- API keys;
- database credentials;
- personal secrets;
- private certificates;
- `.p12`;
- `.pfx`;
- environment secrets;
- real credential dumps.


Do not treat normal test identifiers or documented non-secret configuration
names as secrets.


Require:

    SECRET_SCAN=PASS


If a real secret is found:

    STOP.


======================================================================
11. GM-EXPENSES COMMIT — FIRST
======================================================================

After all pre-commit gates pass:

stage ONLY accepted gm-expenses paths.


Prove:

    git diff --cached --name-status
    git diff --cached --check


Require:

    staged unrelated paths = 0


Then commit.


Suggested commit intent:

    gm-expenses: finalize MVP reconciliation and case numbering


Do not force that exact wording if project convention requires another form.


After commit record:

    new HEAD
    commit tree
    committed path list


Then prove:

    no accepted gm-expenses changes remain unstaged/uncommitted.


Unrelated WIP, if any exists in that repository, must remain untouched.


======================================================================
12. REINSTALL COMMITTED GM-EXPENSES
======================================================================

After gm-expenses commit:

build/install the module from the COMMITTED HEAD into the local Maven
repository needed by Gystigo.

Do not use stale pre-commit build output as proof.


Use the minimal command required to produce the dependency from committed
bytes.


Verify:

    build PASS

If Maven reuses stale output ambiguously:

    perform the necessary clean module build.


Do NOT alter source.


======================================================================
13. GYSTIGO COMMIT — SECOND
======================================================================

Now stage ONLY accepted Gystigo paths.

These include the accepted Host/API/Studio/V64/runtime configuration/test
changes belonging to the Expense MVP closure.

Exclude every unrelated Gystigo WIP path.


Prove:

    git diff --cached --name-status
    git diff --cached --check


Require:

    staged unrelated paths = 0


Also prove the committed Gystigo dependency expectation corresponds to the
new committed gm-expenses bytes.


Then commit.


Suggested intent:

    gystigo: finalize expenses MVP API, numbering and Studio


After commit record:

    new HEAD
    commit tree
    committed path list


The unrelated Gystigo WIP paths must remain dirty and untouched after commit.


======================================================================
14. FABRIC COMMIT — THIRD
======================================================================

Stage ONLY the accepted Fabric paths related to:

- STEP evidence;
- canonical gm-expenses documentation;
- append-only Reglas.md additions;
- CURRENT_STEP / continuity;
- release-readiness records;
- V64 evidence;
- runtime provenance evidence;
- final Owner decisions.


Do NOT stage unrelated Fabric Knowledge WIP.


Prove:

    git diff --cached --name-status
    git diff --cached --check


Require:

    staged unrelated paths = 0


Then commit.


Suggested intent:

    fabric: record gm-expenses MVP closure evidence


After commit record:

    new HEAD
    commit tree
    committed path list


======================================================================
15. POST-COMMIT SOURCE PROOF
======================================================================

After all three commits:

record:

GM_EXPENSES_NEW_HEAD=

GYSTIGO_NEW_HEAD=

FABRIC_NEW_HEAD=


For each commit prove:

    git show --stat --oneline HEAD
    git diff HEAD^ HEAD --name-status


Confirm:

    expected accepted paths only.


No unrelated path may appear in any of the three commits.


======================================================================
16. POST-COMMIT WORKTREE STATE
======================================================================

Run final:

    git status --short

in all three repos.


Expected:

gm-expenses:
    clean, unless a previously classified unrelated path exists

Gystigo:
    may still contain unrelated pre-existing WIP

Fabric:
    may still contain unrelated pre-existing WIP


Require:

    ACCEPTED_UNCOMMITTED_PATHS=0
    UNKNOWN_PATHS=0


Do NOT clean unrelated WIP merely to obtain a clean repository.


======================================================================
17. VERIFY CURRENT_STEP CONTINUITY
======================================================================

Fabric CURRENT_STEP after commit must point to the NEXT authorized operation:

    Shared DEV V64 + backend deployment

but it must NOT claim that deployment has already occurred.


Expected conceptual next state:

    NEXT_STEP=
    GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24


Current actual runtime remains:

    Shared DEV V63
    STEP 18 backend


Do not falsely record:

    V64 deployed

before it happens.


======================================================================
18. OWNER CASE MUST REMAIN UNTOUCHED
======================================================================

The live Owner Case currently still contains:

    RETURN_REGISTERED 200
    RETURN_REGISTERED 100

net stored Return:

    USD 300


Do NOT reverse them now.

Do NOT mutate the Case.


The reversal belongs after deployment so the authenticated Owner/user and
real server timestamp are recorded through the actual product workflow.


Require:

    OWNER_CASE_MODIFIED=NO


======================================================================
19. NO DEPLOYMENT
======================================================================

Do NOT:

- migrate Shared DEV V63 → V64;
- rebuild official backend container;
- replace the STEP 18 image;
- restart official backend for the new commits;
- mutate Shared DEV;
- reverse the USD 300;
- push any repository.


This STEP ends after LOCAL controlled commits and proofs.


======================================================================
20. NO PUSH
======================================================================

Explicit:

    PUSH_PERFORMED=NO


Do not push:

    gm-expenses
    Gystigo
    Fabric


Owner will authorize push separately.


======================================================================
21. REQUIRED FINAL REPORT
======================================================================

Return exactly enough evidence to authorize deployment:


STEP=
GM_EXPENSES_CONTROLLED_COMMIT_GATE_23


STATUS=
OWNER_REVIEW_REQUIRED
or
BLOCKED


--------------------------------------------------
PRE-COMMIT
--------------------------------------------------

GM_EXPENSES_BRANCH=
GM_EXPENSES_OLD_HEAD=

GYSTIGO_BRANCH=
GYSTIGO_OLD_HEAD=

FABRIC_BRANCH=
FABRIC_OLD_HEAD=


CURRENT_DIRTY_PATHS_TOTAL=

ACCEPTED_PATHS_TOTAL=

UNRELATED_WIP_PATHS_TOTAL=

UNKNOWN_PATHS=


TESTED_BYTES_UNCHANGED=
YES/NO

V64_BYTES_UNCHANGED_SINCE_REHEARSAL=
YES/NO

SECRET_SCAN=
PASS/FAIL


--------------------------------------------------
GM-EXPENSES COMMIT
--------------------------------------------------

GM_EXPENSES_COMMITTED=
YES/NO

GM_EXPENSES_NEW_HEAD=

GM_EXPENSES_COMMITTED_PATHS=

GM_EXPENSES_UNRELATED_PATHS_STAGED=
0

GM_EXPENSES_POST_COMMIT_BUILD=
PASS/FAIL


--------------------------------------------------
GYSTIGO COMMIT
--------------------------------------------------

GYSTIGO_COMMITTED=
YES/NO

GYSTIGO_NEW_HEAD=

GYSTIGO_COMMITTED_PATHS=

GYSTIGO_UNRELATED_PATHS_STAGED=
0


--------------------------------------------------
FABRIC COMMIT
--------------------------------------------------

FABRIC_COMMITTED=
YES/NO

FABRIC_NEW_HEAD=

FABRIC_COMMITTED_PATHS=

FABRIC_UNRELATED_PATHS_STAGED=
0


--------------------------------------------------
BASELINE EVIDENCE
--------------------------------------------------

GM_EXPENSES_TESTS=
773/773 PASS REUSED/RERUN

HOST_REAL_DB=
106/106 PASS REUSED/RERUN

STUDIO=
648/648 PASS REUSED/RERUN

ESLINT=
PASS REUSED/RERUN

V64_REHEARSAL=
PASS REUSED/RERUN

CONCURRENT_SEQUENCE_TEST=
PASS REUSED/RERUN


--------------------------------------------------
POST-COMMIT
--------------------------------------------------

ACCEPTED_UNCOMMITTED_PATHS=
0

UNKNOWN_POST_COMMIT_PATHS=
0

UNRELATED_WIP_PRESERVED=
YES/NO


GM_EXPENSES_POST_COMMIT_STATUS=

GYSTIGO_POST_COMMIT_STATUS=

FABRIC_POST_COMMIT_STATUS=


--------------------------------------------------
RUNTIME — MUST STILL BE OLD
--------------------------------------------------

SHARED_DEV_VERSION=
V63

OFFICIAL_BACKEND_SOURCE=
STEP 18 / bcb9591

WORKING_COMMITTED_SOURCE_SUPPORTS_CASE_NUMBER=
YES

RUNNING_BACKEND_SUPPORTS_CASE_NUMBER=
NO

OWNER_CASE_MODIFIED=
NO


--------------------------------------------------
OPERATIONS
--------------------------------------------------

FILES_STAGED_AFTER_GATE=
0

PUSH_PERFORMED=
NO

SHARED_DEV_MODIFIED=
NO

DEPLOYMENT_PERFORMED=
NO


NEXT_STEP=
GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24


READY_FOR_DEPLOYMENT_STEP=
YES/NO


STOP_FOR_OWNER_REVIEW=
YES

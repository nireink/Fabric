# GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17
MODE=FINAL_PRECOMMIT_PROOF_AND_CONTROLLED_COMMITS
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ACCEPTS=GM_EXPENSES_FINAL_DEBT_AND_COMMIT_READINESS_AUDIT_16 (manifest of 236 paths)
OWNER_DECISION=normal Git LF normalization is accepted; the Verified Baseline uses committed or staged blob hashes; the Gystigo branch is not changed during the gate; the initial-development gm-expenses docs stay excluded
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES MVP CONTROLLED COMMIT GATE

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17

MODE=
FINAL_PRECOMMIT_PROOF_AND_CONTROLLED_COMMITS

OWNER_AUTHORIZED=YES

SCOPE BOUNDARY:

This STEP is ONLY for the gm-expenses MVP release track.

Inspect or commit Gystigo, Fabric and shared files ONLY when they directly
belong to the accepted gm-expenses release manifest established by STEP 16.

Do NOT perform a general GYPPORT platform commit.

============================================================
0. ACCEPTED OWNER BASELINE
============================================================

Owner accepts:

GM_EXPENSES_FINAL_DEBT_AND_COMMIT_READINESS_AUDIT_16

Final audit result:

    READY_FOR_CONTROLLED_COMMIT_GATE=YES
    TECHNICAL_DEBT_BLOCKERS=0
    UNKNOWN_FILES=0
    ACCEPTED_FILES_MISSING=0
    DRIFTED_ACCEPTED_FILES=0

Accepted manifest:

    236 paths

    gm-expenses:
        64 paths

    Gystigo:
        68 paths

    Fabric:
        104 paths

Final migration head:

    V63

Accepted evidence:

    gm-expenses module       748/748
    Host real DB             103/103
    Studio                   631/631
    Runtime smoke            33/33
    V43 → V63                PASS
    Tenant isolation         PASS
    5xx                      0

Use VERIFIED_BASELINE_REUSE.

============================================================
1. CRITICAL ENVIRONMENT PRECONDITION
============================================================

STEP 16 found that the previous Claude/Desktop parent process still inherited
obsolete:

    SPRING_DATASOURCE_*

values pointing to Shared DEV.

Windows User and Machine scopes are already clean.

BEFORE any build/test:

inspect the CURRENT process environment.

Require:

    current process does NOT inherit Shared DEV datasource

Specifically reject:

    :3308
    gypport-mysql-dev
    core_business_dev

If the current process still inherits any Shared DEV datasource:

    STOP IMMEDIATELY.

Return:

    RESTART_REQUIRED=YES

Do not build.
Do not test.
Do not stage.

Do not rely on the local launcher to mask an unsafe parent process during the
commit gate.

============================================================
2. REGENERATE STEP 16 MANIFESTS
============================================================

The STEP 16 per-file TSV manifests existed only in temporary scratchpad s16/.

Regenerate from current working trees:

    classification.tsv
    commit-1-gm-expenses.tsv
    commit-2-gystigo.tsv
    commit-3-fabric.tsv
    excluded-unrelated-wip.tsv

Compare against the STEP 16 report.

Require:

    accepted paths = same semantic set
    unknown = 0
    missing = 0

If the accepted manifest differs unexpectedly:

    STOP.

Do not stage.

============================================================
3. REPOSITORY STATE
============================================================

Verify exact expected starting state.

Modules/gm-expenses:

    branch = master
    baseline HEAD = ab74610

Gystigo:

    current branch =
        feature/gm-fleets-minimum-vehicle-master-01

    baseline HEAD =
        d9f3dde

Fabric:

    branch = main
    baseline HEAD = 70fd250

Do NOT switch branch.

Do NOT rename branch.

Do NOT create worktree.

Do NOT stash.

Do NOT reset.

The current branch name in Gystigo is acknowledged as historical/misleading
but changing branch with the accepted WIP still uncommitted introduces
unnecessary risk.

Commit the accepted bytes first.

Branch integration/normalization happens after a clean accepted commit if
needed.

============================================================
4. VERIFY UNRELATED WIP EXCLUSION
============================================================

Explicitly preserve the STEP 16 excluded files.

Gystigo excluded:

    README.md deletion
    AuthPage.css
    onboarding/ShortRegisterPage.jsx
    fixtures/HeaderBrandingFixture.jsx
    fixtures/header-branding.html

Fabric excluded:

    Knowledge/AI
    Knowledge/Architecture
    Knowledge/Derived
    Knowledge/Security
    Knowledge/UIX
    Knowledge/gm-accounting

    Knowledge/gm-expenses/README.md
    Knowledge/gm-expenses/03-application
    Knowledge/gm-expenses/04-integration
    Knowledge/gm-expenses/05-implementation

Do NOT stage them.

Do NOT modify them.

Do NOT stage:

    .

Do NOT use:

    git add -A
    git add -u

Use explicit accepted paths only.

============================================================
5. OPTIONAL RECOMMENDED TARGETED VERIFICATION — NOW REQUIRED BY OWNER
============================================================

STEP 16 found no mandatory invalidated tests.

Owner chooses to run only the small recommended safeguards:

A.
PersonIdentityReconciliationHttpTest

because its Expenses delivery request changed and its last recorded execution
predates V62 / STEP 11.

B.
Host non-real-DB Expenses unit tests identified by STEP 16 as having old/no
run records.

Do NOT rerun:

    gm-expenses 748
    Host real-DB 103
    Studio 631
    FINAL_12 33/33
    V43→V63 rehearsal
    PKG-2D

unless one of the targeted tests identifies a real regression.

Record exact results.

============================================================
6. MIGRATION BYTE PROOF
============================================================

Before staging Gystigo, verify:

    V62
    V63

are still byte-identical to FINAL_12 accepted migration bytes.

Require:

    no V64
    no duplicate migration version
    no historical migration mutation

If mismatch:

    STOP.

============================================================
7. LINE ENDING POLICY — OWNER DECISION
============================================================

OWNER_DECISION:

Accept normal Git LF conversion.

Do NOT add a special:

    -text

policy merely to preserve old working-tree CRLF hashes.

For every accepted file whose working-tree bytes differ from the staged Git
blob only because of normalization:

record:

    PRE_STAGE_WORKTREE_SHA256
    STAGED_BLOB_SHA256
    NORMALIZATION=CRLF_TO_LF

The final VERIFIED BASELINE must use:

    COMMITTED / STAGED BLOB HASHES

not obsolete pre-commit working-tree hashes.

Historical evidence hashes remain valid as pre-normalization evidence.

Do not rewrite old evidence merely to hide the conversion.

============================================================
8. UTF-16 EVIDENCE FILE
============================================================

STEP 16 found one accepted evidence file that Git treats as binary.

Do not automatically re-encode it.

Before staging:

verify:

- file identity;
- evidence purpose;
- no secrets;
- byte integrity.

If it is accepted evidence:

commit its existing bytes.

Record:

    BINARY_EVIDENCE_FILE=<path>

============================================================
9. FABRIC CLOSEOUT BEFORE STAGING
============================================================

STEP 16 intentionally did not edit Fabric.

Before commit 3 only, perform the required governance closeout:

A.
Store the exact STEP 16 prompt in the existing:

    Knowledge/00-GYPPORT-UNIVERSE/steps/
    GM-EXPENSES-RELEASE-READINESS/

structure.

B.
Store this STEP 17 prompt using the same canonical naming convention.

C.
Update:

    active-work/CURRENT_STEP.md

through the existing continuity mechanism.

D.
Prepare/register the final gm-expenses VERIFIED BASELINE document containing:

- final commits when available;
- V63;
- committed blob hashes;
- accepted test evidence;
- FINAL_12;
- known non-blocking debts;
- Shared DEV still V43 pending migration.

Do NOT modify historical evidence.

Do NOT rewrite Reglas.md unless this gate creates a genuinely new Owner rule.

============================================================
10. COMMIT 1 — MODULES/GM-EXPENSES
============================================================

Use the regenerated STEP 16 accepted manifest.

Expected:

    64 paths
    41 modified
    4 deleted
    19 new

Stage ONLY those exact paths.

Before commit run:

    git diff --cached --name-status
    git diff --cached --check

Require:

    staged accepted paths = expected manifest
    unrelated staged paths = 0

Generate:

    final committed/staged blob SHA-256 manifest

Commit purpose:

    gm-expenses MVP case-level rendition and review workflow

Use a concise project-conventional commit message.

After commit verify:

    commit hash
    exact paths
    clean accepted scope
    unrelated WIP untouched

Record:

    GM_EXPENSES_COMMIT=<sha>

============================================================
11. COMMIT 2 — GYSTIGO
============================================================

Depends on Commit 1.

Expected accepted scope:

    68 paths

including:

- Host API;
- V62/V63;
- Studio Expenses;
- contracts/fixtures;
- tracked local launcher;
- Expenses integrity tests;
- accepted shared dependency paths.

Stage explicit paths only.

Exclude the 5 unrelated Gystigo files.

Before commit:

    git diff --cached --name-status
    git diff --cached --check

Require:

    unrelated staged = 0

Generate:

    staged/committed blob hash manifest.

Commit from current branch:

    feature/gm-fleets-minimum-vehicle-master-01

Do NOT change branch during this gate.

Record:

    GYSTIGO_COMMIT=<sha>

After commit prove unrelated WIP remains untouched.

============================================================
12. COMMIT 3 — FABRIC
============================================================

Only after commits 1 and 2 exist.

Update the final gm-expenses VERIFIED BASELINE with:

    GM_EXPENSES_COMMIT
    GYSTIGO_COMMIT

and final committed blob hash manifests.

Stage ONLY accepted release-readiness Fabric paths plus:

- STEP 16 prompt;
- STEP 17 prompt;
- refreshed CURRENT_STEP;
- final gm-expenses VERIFIED BASELINE.

Keep old initial-development docs excluded:

    README
    03-application
    04-integration
    05-implementation

Do not mix them into this release commit.

Before commit:

    git diff --cached --name-status
    git diff --cached --check

Require:

    unrelated staged = 0

Record:

    FABRIC_COMMIT=<sha>

============================================================
13. FINAL VERIFIED BASELINE
============================================================

The gm-expenses Verified Baseline must include at minimum:

    baseline id
    date

    gm-expenses commit
    Gystigo commit
    Fabric commit

    final migration head = V63

    migration hashes

    final accepted source/blob hash manifests

    tests:
        module 748/748
        Host real-DB 103/103
        Studio 631/631
        runtime smoke 33/33
        migration V43→V63 PASS
        tenant isolation PASS
        targeted pre-gate tests PASS

    known non-blocking debt

    Shared DEV:
        V43
        not yet migrated

    official stale DEV backend:
        not yet rebuilt

Status:

    COMMITTED_LOCAL
    READY_FOR_SHARED_DEV_MIGRATION

Do NOT claim Shared DEV validated yet.

============================================================
14. POST-COMMIT SOURCE PROOF
============================================================

After all commits:

prove accepted source exists in commits.

Confirm:

    ORPHANED_ACCEPTED_WORK=NONE

Confirm no accepted implementation exists only in:

    target/
    ~/.m2
    runtime jar
    scratchpad

Re-run no large suites unless committed blobs differ unexpectedly from the
tested blobs.

============================================================
15. DOCUMENTS / RUNTIME OUTPUT
============================================================

Do NOT commit:

    target/runtime-local/documents
    runtime jars
    logs
    access logs
    backend.pid
    dumps
    .env
    generated passwords

The 11 runtime documents have originals in the Docker volume and are not part
of source control.

Record as operational Docker/environment debt for the upcoming environment
track.

============================================================
16. SECURITY FINAL CHECK
============================================================

After commit, secret-scan the exact committed file sets.

Require:

    SECRET_SCAN=CLEAN

Never print secret values.

Confirm tracked launchers contain no credentials.

============================================================
17. SHARED DEV
============================================================

ABSOLUTELY DO NOT:

- migrate 3308;
- modify Shared DEV;
- start stale gypport-backend-dev;
- rebuild official DEV image;
- clean legacy DEV data.

Shared DEV remains:

    V43

The next STEP after Owner acceptance is:

    fresh backup
    → migrate V43→V63
    → rebuild backend from accepted commit
    → Owner real-login smoke

============================================================
18. PUSH
============================================================

Do NOT push in this STEP.

Commits remain local until Owner review.

============================================================
19. REQUIRED REPORT
============================================================

Return:

STATUS=
GM_EXPENSES_MVP_COMMITTED_LOCAL_READY_FOR_SHARED_DEV

STEP=
GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17

ENV_PRECONDITION=
PASS/FAIL

TARGETED_TEST_RESULTS=

GM_EXPENSES_COMMIT=
GYSTIGO_COMMIT=
FABRIC_COMMIT=

GM_EXPENSES_COMMITTED_PATHS=
GYSTIGO_COMMITTED_PATHS=
FABRIC_COMMITTED_PATHS=

UNRELATED_WIP_PRESERVED=

FINAL_MIGRATION_HEAD=V63
MIGRATION_BYTES_MATCH_FINAL12=

LINE_ENDING_NORMALIZATIONS=
BINARY_EVIDENCE_FILE=

FINAL_HASH_MANIFEST_STATUS=

VERIFIED_BASELINE_ID=
VERIFIED_BASELINE_STATUS=

ORPHANED_ACCEPTED_WORK=

SECRET_SCAN=

TECHNICAL_DEBT_BLOCKERS=0

SHARED_DEV_VERSION=V43
SHARED_DEV_MODIFIED=NO

OFFICIAL_DEV_BACKEND_REBUILT=NO

FILES_STAGED_AFTER_COMMIT=0

PUSH_PERFORMED=NO

READY_FOR_SHARED_DEV_MIGRATION=YES/NO

STOP_FOR_OWNER_REVIEW=YES

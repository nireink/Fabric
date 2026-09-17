# GM_EXPENSES_FINAL_DEBT_AND_COMMIT_READINESS_AUDIT_16 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_FINAL_DEBT_AND_COMMIT_READINESS_AUDIT_16
MODE=READ_ONLY_FINAL_CLOSURE_AUDIT
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ACCEPTS=GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15 (frozen baseline)
RESULT=READY_FOR_CONTROLLED_COMMIT_GATE=YES, Owner-accepted in GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17
STORED_BY=GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17 (the audit itself was read-only and did not write Fabric)
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES FINAL DEBT + COMMIT READINESS AUDIT

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_FINAL_DEBT_AND_COMMIT_READINESS_AUDIT_16

MODE=
READ_ONLY_FINAL_CLOSURE_AUDIT

OWNER_AUTHORIZED=YES

IMPORTANT:

This is NOT an implementation STEP.

Do NOT modify source code.
Do NOT modify documentation.
Do NOT modify databases.
Do NOT stage.
Do NOT commit.
Do NOT push.

The purpose is to establish the exact final closure state before controlled
commits.

============================================================
0. OWNER-ACCEPTED BASELINE
============================================================

Treat the following as accepted and frozen:

- V62 planned Advance delivery
- V63 unified financial reconciliation
- ExpenseCase-centered rendition
- multiple Advances per ExpenseCase
- same-currency multiple Advances
- FIFO removed as financial policy
- Return + Reimbursement coexistence
- Case-level reconciliation/closure
- final financial card semantics
- dual Conciliado / Uso indicators
- Conciliado aligned with Responsable
- OBSERVADO history atomicity
- local datasource safety hardening
- tracked local launcher
- FINAL_12 runtime rehearsal

Latest Studio verification:

    631/631

Latest Host real-DB accepted verification:

    103/103

gm-expenses accepted module verification:

    748/748

Final migration head:

    V63

Shared DEV:

    V43
    untouched

============================================================
1. REPOSITORY INVENTORY
============================================================

Audit all repositories relevant to this release:

- Modules/gm-expenses
- Gystigo
- Fabric

Also inspect any repository referenced by dirty files before classifying them.

For each:

record:

    branch
    HEAD
    status
    staged
    unstaged
    untracked
    ahead/behind if safely available

Do NOT change anything.

============================================================
2. CLASSIFY EVERY DIRTY FILE
============================================================

Every dirty/untracked/deleted path must be classified as exactly one:

A. GM_EXPENSES_MVP_ACCEPTED
B. SHARED_ACCEPTED_DEPENDENCY
C. UNRELATED_PREEXISTING_WIP
D. EVIDENCE / DOCUMENTATION
E. GENERATED / RUNTIME / SHOULD_NOT_COMMIT
F. UNKNOWN

There must be ZERO UNKNOWN files before recommending commit.

If UNKNOWN > 0:

    READY_FOR_CONTROLLED_COMMIT_GATE=NO

and report exact paths.

============================================================
3. RECONSTRUCT FINAL ACCEPTED FILE MANIFEST
============================================================

Reconstruct the complete final file manifest from:

- accepted STEP evidence;
- BoxGhost evidence;
- Fabric CURRENT_STEP;
- current git diff;
- previous manifests/fingerprints.

Do not rely only on current git status.

Prove no accepted file disappeared during the long WIP sequence.

Return:

    ACCEPTED_FILE_COUNT
    ACCEPTED_FILES_PRESENT
    ACCEPTED_FILES_MISSING

============================================================
4. HASH / BYTE INTEGRITY
============================================================

Verify the final accepted production bytes.

At minimum fingerprint:

gm-expenses:
    src/main
    relevant src/test

Gystigo Host:
    gm-expenses Host integration
    migrations V62/V63
    runtime/config touched by Expenses

Studio:
    all accepted Expenses source
    contracts
    fixture

Environment:
    tracked start-runtime-local.ps1
    stop-runtime-local.ps1

Fabric:
    canonical baselines
    Reglas.md
    CURRENT_STEP
    BoxGhost final evidence

Compare with accepted evidence wherever hashes already exist.

Do NOT call a hash "lost" merely because no prior comparison exists.

Classify:

    MATCHED_ACCEPTED_HASH
    NEW_FINAL_HASH_TO_REGISTER
    DRIFTED

DRIFTED production bytes require investigation before commit.

============================================================
5. FINAL MIGRATION AUDIT
============================================================

Verify repository migration chain ends exactly at:

    V63

Confirm:

- V62 present;
- V63 present;
- hashes match accepted/rehearsed migration bytes;
- no V64 exists;
- no duplicate version;
- no modified historical migration;
- no migration gap.

FINAL_12 V43→V63 evidence remains valid only if migration bytes match.

============================================================
6. FINAL TEST-EVIDENCE CROSSCHECK
============================================================

Build a matrix:

AREA                         ACCEPTED EVIDENCE
gm-expenses module           748/748
Host real DB                 103/103
Studio                       631/631
FINAL runtime smoke          33/33
Migration V43→V63            PASS
Tenant isolation             PASS
Server 5xx                   0

For each evidence set record:

- source STEP;
- relevant file/hash scope;
- whether later changes invalidated it.

Use VERIFIED_BASELINE_REUSE.

Do NOT rerun tests.

This audit is read-only.

If evidence is invalidated:

report exactly which suite must be rerun before commit.

============================================================
7. TECHNICAL DEBT INVENTORY
============================================================

Reconstruct ALL known debts and findings from the release track.

Classify each as:

BLOCKER
NON_BLOCKING_MVP
RESOLVED
SUPERSEDED
SEPARATE_FOUNDATION

At minimum verify status of:

- missing-route 404 masked as 401;
- audit_logs global writer not implemented;
- audit_logs append-only protection not implemented;
- ADR-0010 still PROPOSED;
- legacy OBSERVADO row;
- 3 closed settlements / EN_RENDICION Advance inconsistency;
- Shared DEV legacy drafts/standalone records;
- local runtime documents under target/runtime-local/documents;
- 320px global topbar width issue;
- any closedBy/raw actor-id display debt still present;
- gm-operational-resources later integration;
- gm-banking later integration;
- Shared DEV still V43;
- stale official DEV backend image.

Do NOT assume an old debt still exists.

Verify its current state from source/evidence.

============================================================
8. SECURITY CLOSURE
============================================================

Verify accepted security safeguards:

- Windows User-level Shared DEV datasource removed;
- Machine-level Shared DEV datasource absent;
- tracked LOCAL launcher exists;
- LOCAL launcher targets 3310;
- fail-closed guard refuses Shared DEV;
- secrets not committed;
- no passwords/tokens inside tracked scripts;
- current local backend has no intended dependency on global datasource vars.

Secret-scan the FINAL ACCEPTED FILE SET.

Do not print secrets.

Return only:

    CLEAN
    FINDING
    AMBIGUOUS

============================================================
9. AUDIT ARCHITECTURE STATUS
============================================================

Record factual final status:

GLOBAL TABLE:
    audit_logs

CATALOG:
    audit_action_types

GLOBAL WRITER:
    not implemented

ADR-0010:
    PROPOSED

gm-expenses histories:
    append-only and active

Confirm whether this is:

    NON_BLOCKING_MVP

Do NOT create implementation work.

Do NOT change ADR.

============================================================
10. LEGACY DATA STATUS
============================================================

Separate code debt from DEV data debt.

Report current known Shared DEV inconsistent test records.

Do NOT modify them.

Explicitly state:

    MIGRATION != LEGACY CLEANUP

Multiple Advances are NOT a defect.

Known local-only regularization must not be mistaken for Shared DEV cleanup.

============================================================
11. GENERATED / RUNTIME FILES
============================================================

Audit generated/runtime paths.

Especially:

    target/runtime-local/documents
    logs
    pid files
    jars
    temporary dumps
    screenshots
    local env files

Classify whether each should:

    remain ignored
    be preserved outside target
    be committed
    be archived as evidence

Do NOT move them.

Flag any user/business document that could be accidentally deleted by:

    mvn clean

as a separate operational finding.

============================================================
12. FABRIC / GOVERNANCE CONSISTENCY
============================================================

Verify:

- canonical gm-expenses domain baseline current;
- persistence baseline current;
- Reglas.md append-only integrity preserved;
- CURRENT_STEP reflects STEP 16 during audit;
- BoxGhost evidence chain complete;
- no duplicate conflicting canonical rule;
- superseded "one active Advance per Case" rule clearly superseded;
- FIFO clearly non-canonical;
- multiple Advances clearly canonical.

Do NOT edit.

Report inconsistencies only.

============================================================
13. COMMIT BOUNDARY PROPOSAL
============================================================

Without staging anything, propose exact commit groups.

Preferred dependency order:

1. gm-expenses
2. Gystigo
3. Fabric

For each proposed commit return:

    repository
    exact paths
    purpose
    evidence supporting those paths
    unrelated files excluded

If a file mixes accepted Expenses changes and unrelated WIP:

    classify as MIXED_FILE

Do NOT silently include it.

Report whether surgical staging is safe.

============================================================
14. LOST / ORPHANED WORK CHECK
============================================================

Search for evidence of accepted work that is:

- present in BoxGhost/Fabric but absent from source;
- source present but absent from final manifest;
- only in target/;
- only in ~/.m2;
- only in a generated jar;
- only in an old worktree/branch if referenced by current evidence.

Do not broadly search unrelated repositories.

Return:

    ORPHANED_ACCEPTED_WORK=YES/NO

If YES:
    exact item and recovery recommendation.

============================================================
15. FINAL RELEASE BLOCKER DECISION
============================================================

Return exactly one:

A.
READY_FOR_CONTROLLED_COMMIT_GATE

B.
NOT_READY_FOR_CONTROLLED_COMMIT_GATE

If B:

list ONLY true blockers.

Do not elevate known non-blocking debt into release blockers.

============================================================
16. REQUIRED FINAL REPORT
============================================================

Return:

STATUS=
READY_FOR_CONTROLLED_COMMIT_GATE
or
NOT_READY_FOR_CONTROLLED_COMMIT_GATE

STEP=
GM_EXPENSES_FINAL_DEBT_AND_COMMIT_READINESS_AUDIT_16

REPOSITORIES=
GM_EXPENSES_HEAD=
GYSTIGO_HEAD=
FABRIC_HEAD=

ACCEPTED_FILE_COUNT=
UNKNOWN_FILES=

ACCEPTED_FILES_MISSING=

HASH_STATUS=
DRIFTED_ACCEPTED_FILES=

FINAL_MIGRATION_HEAD=V63
MIGRATION_BYTES_MATCH_FINAL12=

TEST_EVIDENCE_VALID=
TESTS_REQUIRING_RERUN=

TECHNICAL_DEBT=
- BLOCKERS:
- NON_BLOCKING:
- RESOLVED:
- SUPERSEDED:
- SEPARATE_FOUNDATION:

SECURITY_FINAL_STATUS=

SECRET_SCAN=

GLOBAL_AUDIT_WRITER_STATUS=
GM_EXPENSES_DOMAIN_AUDIT_STATUS=

LEGACY_SHARED_DEV_DATA_STATUS=

GENERATED_RUNTIME_FINDINGS=

FABRIC_CANONICAL_CONSISTENCY=

ORPHANED_ACCEPTED_WORK=

MIXED_FILES=

PROPOSED_COMMIT_1=
PROPOSED_COMMIT_2=
PROPOSED_COMMIT_3=

SHARED_DEV_VERSION=V43
SHARED_DEV_MODIFIED=NO

FILES_CHANGED=0
FILES_STAGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

READY_FOR_CONTROLLED_COMMIT_GATE=YES/NO

STOP_FOR_OWNER_REVIEW=YES

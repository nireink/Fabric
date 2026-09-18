# GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 — Owner prompt (recovered)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
RECOVERY=EXACT - the Owner's message extracted programmatically from the session transcript; never retyped
STORED_BY=GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31 (2026-09-18); the prompt was not stored when the STEP ran
SOURCE=local Claude Code session transcript 6bd391c2-9dd7-4c98-8f41-546e5a9baea1.jsonl, line 4181
SOURCE_MESSAGE_UUID=ce148ba5-47b7-49b3-8e1d-ca958c1c7467
SOURCE_MESSAGE_TIMESTAMP=2026-09-17T16:08:11.892Z
PROMPT_TEXT_SHA256=c8f4d30179cc9ba0f6962597a9ab5962233381cd0bafd8d2999087b948924766
PROMPT_TEXT_CHARS=11499
```

The Owner's prompt follows verbatim. PROMPT_TEXT_SHA256 is computed over the UTF-8 text below the line.

---

GYPPORT® — GM-EXPENSES SHARED DEV V43→V63 MIGRATION + OFFICIAL DEV REBUILD

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18

MODE=
CONTROLLED_SHARED_DEV_MIGRATION_AND_DEPLOYMENT

OWNER_AUTHORIZED=YES

============================================================
0. ACCEPTED IMMUTABLE BASELINE
============================================================

Owner accepts:

GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17

Exact commits:

GM_EXPENSES_COMMIT=
545eae0fb287f8e04f7f1b4ac73780304ec53f22

GYSTIGO_COMMIT=
bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f

FABRIC_COMMIT=
bbdd66a0c5a1c9cbb21293beb74c3e5e61cc5de0

VERIFIED_BASELINE=
GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17

Current Shared DEV:

    MySQL = 127.0.0.1:3308
    Flyway = V43
    official backend image = stale
    stale backend container = expected stopped

Target:

    Shared DEV DB = V63
    official DEV backend = exact accepted commits
    Studio/API contract = accepted MVP
    no legacy-data cleanup mixed into migration

============================================================
1. HARD SCOPE
============================================================

This STEP may:

- inspect Shared DEV;
- make a fresh backup;
- fingerprint Shared DEV;
- migrate V43 → V63;
- build the official DEV backend from exact committed bytes;
- start the rebuilt DEV backend;
- execute deployment smoke tests.

This STEP must NOT:

- modify gm-expenses source;
- modify Gystigo source;
- modify Fabric;
- create V64;
- change business rules;
- regularize legacy data;
- fix old OBSERVADO records;
- repair the 3 old settlement/advance inconsistencies;
- stage;
- commit;
- push.

If source modification appears necessary:

    STOP.

============================================================
2. CRITICAL — BUILD FROM COMMITS, NOT CURRENT WORKTREES
============================================================

The current Gystigo working tree intentionally still contains unrelated WIP.

DO NOT build the official DEV backend from the current dirty working tree.

Build from clean exported bytes corresponding exactly to:

    gm-expenses 545eae0...
    Gystigo     bcb9591...

Use a disposable clean export/clone/archive/build directory.

Do not create a persistent development worktree.

The disposable build environment must be removable after verification.

Prove:

    build source commit ids
    source tree clean
    unrelated WIP absent

============================================================
3. PRE-MIGRATION ENVIRONMENT SAFETY
============================================================

Before touching Shared DEV verify:

LOCAL personal runtime:
    3310

Shared DEV:
    3308

Reject accidental ambiguity.

Confirm:

- no global SPRING_DATASOURCE_* variables;
- no personal backend connected to 3308;
- stale official DEV backend stopped;
- identify every current connection to Shared DEV;
- no active application writer during migration.

If an unknown writer is active:

    STOP_FOR_OWNER_REVIEW=YES

Do not migrate while write activity is unexplained.

============================================================
4. FRESH SHARED DEV BACKUP
============================================================

Do NOT rely only on the old FINAL_12 dump.

Create a fresh backup immediately before migration.

Backup requirements:

- Shared DEV V43;
- schema + data;
- Flyway history;
- routines/triggers as applicable;
- stored in restricted backup location;
- never Git;
- never Fabric;
- never print credentials.

Record:

    BACKUP_FILE
    BACKUP_SHA256
    BACKUP_CREATED_AT
    SOURCE_DB
    SOURCE_FLYWAY_VERSION

Verify backup completion before continuing.

If backup fails:

    STOP.

============================================================
5. PRE-MIGRATION FINGERPRINT
============================================================

Generate a read-only fingerprint immediately before migration.

Compare to FINAL_12 where applicable:

- Flyway version/history;
- failed migrations;
- table counts;
- gm-expenses relevant row counts;
- triggers;
- routines;
- relevant schema metadata;
- known legacy rows.

Do NOT require the live DB to be byte-identical to FINAL_12 if legitimate
Shared DEV usage occurred after FINAL_12.

Instead distinguish:

    EXPECTED_DATA_CHANGE
    SCHEMA_DRIFT
    UNKNOWN_DRIFT

Any unexpected SCHEMA_DRIFT:

    STOP.

============================================================
6. MIGRATION BYTE PROOF
============================================================

Before applying Flyway:

verify the migration bytes used by this deployment are exactly the accepted
committed migration bytes.

Require:

    final migration = V63
    V62 hash matches baseline
    V63 hash matches baseline
    no V64
    no historical migration modification

If not exact:

    STOP.

============================================================
7. APPLY SHARED DEV V43 → V63
============================================================

Use the accepted migration path only.

Expected:

    20 migrations
    V43 → V63

Do not execute manual schema modifications.

Do not execute legacy cleanup SQL.

Do not alter business data except as migrations explicitly require.

Capture:

    start version
    end version
    migrations applied
    duration
    failed migrations

Require:

    FINAL_FLYWAY_VERSION=V63
    FAILED_MIGRATIONS=0

============================================================
8. POST-MIGRATION DATA INTEGRITY
============================================================

Compare pre/post fingerprints.

Verify:

- expected schema additions;
- expected migration effects;
- no unexplained table loss;
- no unexplained business-row loss;
- gm-expenses legacy rows remain legacy unless migration explicitly transforms them;
- multiple Advances remain valid;
- no automatic OBSERVADO cleanup;
- no automatic settlement legacy repair.

Explicitly preserve:

    MIGRATION != LEGACY CLEANUP

If unexplained destructive change occurs:

    STOP.

Keep the fresh V43 backup for recovery.

============================================================
9. BUILD EXACT GM-EXPENSES MODULE
============================================================

From the clean exported commit:

    545eae0...

build gm-expenses.

Prefer an isolated Maven local repository for this deployment build so that a
different local SNAPSHOT cannot be consumed accidentally.

Record:

    module source commit
    module jar SHA256
    test/build result

Do not use an arbitrary existing ~/.m2 SNAPSHOT as proof of exact deployment.

============================================================
10. BUILD EXACT GYSTIGO BACKEND
============================================================

From clean exported:

    bcb9591...

build Gystigo using the exact gm-expenses artifact from section 9.

Record:

    source commit
    backend artifact SHA256

Prove that:

- accepted V62/V63 bytes are inside the artifact;
- unrelated Gystigo WIP is absent;
- compiled gm-expenses classes correspond to 545eae0.

============================================================
11. OFFICIAL DEV DOCKER IMAGE
============================================================

Rebuild the official DEV backend image from the exact accepted artifacts.

Do NOT reuse the stale 2026-09-09 backend image.

Do NOT use `latest` as deployment identity.

Record:

    IMAGE_TAG
    IMAGE_ID
    IMAGE_DIGEST if available
    BUILD_SOURCE_GYSTIGO_COMMIT
    BUILD_SOURCE_GM_EXPENSES_COMMIT

The image must target:

    Shared DEV 3308

through explicit DEV configuration.

Do not introduce Shared DEV as a machine/user global datasource.

============================================================
12. START OFFICIAL DEV BACKEND
============================================================

Start only after:

    Shared DEV = V63
    image exact = verified

Verify:

- application starts;
- Flyway validates V63;
- health endpoint healthy;
- connection target = Shared DEV 3308;
- no connection to personal 3310;
- no startup 5xx/error loop.

============================================================
13. AUTOMATED DEPLOYMENT SMOKE
============================================================

Use safe non-destructive or controlled test data.

At minimum verify:

- authentication path reachable;
- tenant context;
- Expenses list/read APIs;
- Case APIs;
- Advance APIs;
- Expense APIs;
- review-history API;
- reports;
- tenant isolation.

Do not perform legacy cleanup.

If creating smoke records:

use clearly identifiable test records and record them.

============================================================
14. OWNER REAL-LOGIN PREPARATION
============================================================

After automated smoke is green:

DO NOT claim final product validation yet.

Return the exact URL/environment and the Owner smoke checklist.

Owner smoke should cover:

    login
    → Gastos
    → crear expediente
    → varios anticipos
    → confirmar entrega
    → registrar gasto
    → editar REGISTRADO
    → enviar revisión
    → observar
    → corregir
    → aprobar
    → devolución/reembolso as applicable
    → conciliar
    → cerrar Case
    → reportes
    → visual Conciliado/Uso

The Owner performs this final product smoke.

============================================================
15. LEGACY DATA — ABSOLUTELY SEPARATE
============================================================

Do NOT fix during this STEP:

- Shared DEV legacy OBSERVADO row;
- 3 CERRADO settlements with Advances EN_RENDICION;
- old draft/standalone records.

Report them unchanged.

A future explicit DEV DATA REGULARIZATION STEP may handle them.

============================================================
16. ROLLBACK READINESS
============================================================

Before declaring success record rollback inputs:

    V43 backup path/hash
    previous image identity
    new image identity

If deployment fails:

do not improvise destructive reverse migrations.

Stop and report exact failure state.

============================================================
17. PUSH
============================================================

Do NOT push source commits during this STEP.

Deployment validation and repository push remain separate Owner decisions.

============================================================
18. REQUIRED REPORT
============================================================

Return:

STEP=
GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18

STATUS=
READY_FOR_OWNER_REAL_LOGIN_SMOKE
or
DEPLOYMENT_BLOCKED

SOURCE:
GM_EXPENSES_COMMIT=
GYSTIGO_COMMIT=
FABRIC_BASELINE_COMMIT=

PRECHECK:
UNKNOWN_SHARED_DEV_WRITERS=
GLOBAL_DATASOURCE_ENV_CLEAN=

BACKUP:
BACKUP_FILE=
BACKUP_SHA256=
BACKUP_VERIFIED=

MIGRATION:
START_VERSION=V43
END_VERSION=
MIGRATIONS_APPLIED=
FAILED_MIGRATIONS=
MIGRATION_BYTES_MATCH_BASELINE=

DATA_INTEGRITY=
LEGACY_DATA_AUTOMATICALLY_CLEANED=NO

BUILD:
GM_EXPENSES_JAR_SHA256=
GYSTIGO_ARTIFACT_SHA256=
BUILD_FROM_CLEAN_COMMITTED_BYTES=

DOCKER:
OLD_IMAGE=
NEW_IMAGE=
IMAGE_ID=
IMAGE_DIGEST=
OFFICIAL_DEV_BACKEND_REBUILT=

RUNTIME:
CONNECTED_DB=
FLYWAY_VERSION=
HEALTH=
SERVER_5XX=

AUTOMATED_SMOKE=
TENANT_ISOLATION=

LEGACY_OBSERVED_ROW_STATUS=
LEGACY_SETTLEMENT_INCONSISTENCIES=

SHARED_DEV_MODIFIED=
YES_ONLY_BY_ACCEPTED_MIGRATIONS_AND_CONTROLLED_SMOKE

SOURCE_FILES_MODIFIED=0
FILES_STAGED=0
COMMITS_CREATED=0
PUSH_PERFORMED=NO

READY_FOR_OWNER_REAL_LOGIN_SMOKE=YES/NO

OWNER_SMOKE_URL=

STOP_FOR_OWNER_REVIEW=YES

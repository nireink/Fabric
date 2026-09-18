# GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30
MODE=READ_ONLY_INVENTORY_THEN_HASH_VERIFY_THEN_SECURE_ARCHIVE_COPY_THEN_RESTORE_VALIDATION_THEN_TEMP_CLEANUP_THEN_EVIDENCE
OWNER_AUTHORIZATION=YES
DATE=2026-09-18
ORIGIN=Owner follow-up named in GM_EXPENSES_FINAL_PUSH_GATE_29: archive the Shared DEV backups from Temp to GYPPORT_STORAGE/Restricted
ACCEPTED_BASELINE=gm-expenses 39a2adf, Gystigo master 5eed5d6, Fabric 59ae14e, Shared DEV V65
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — SHARED DEV RESTRICTED BACKUP ARCHIVAL

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30

MODE=
READ_ONLY_INVENTORY
→ HASH_VERIFY
→ SECURE_ARCHIVE_COPY
→ RESTORE_VALIDATION
→ OWNER_SAFE_TEMP_CLEANUP
→ EVIDENCE

OWNER_AUTHORIZED=YES

SOURCE_CODE_CHANGES_AUTHORIZED=NO
DATABASE_CHANGES_AUTHORIZED=NO
RUNTIME_CHANGES_AUTHORIZED=NO


======================================================================
0. PURPOSE
======================================================================

gm-expenses MVP is already frozen and pushed.

DO NOT reopen the MVP.

Current frozen source:

GM_EXPENSES=
39a2adf4dfff0196208a1f80719be1c12c047ac2

GYSTIGO=
5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc

FABRIC=
59ae14e0520039bee41eef16c41509173b220677

SHARED_DEV=
Flyway V65


Previous deployment STEPs created Shared DEV database backups under:

    %LOCALAPPDATA%\Temp\gypport\shared-dev-backups

Those SQL dumps contain account/business/personal data.

Temporary storage is not their intended long-term location.

This STEP archives them under the restricted GYPPORT storage area with
verified provenance.

No application source or database state may change.


======================================================================
1. INVENTORY EXISTING BACKUPS
======================================================================

Inspect:

    %LOCALAPPDATA%\Temp\gypport\shared-dev-backups


Do NOT move/delete anything yet.


For every file report:

    filename
    full path
    size
    created timestamp
    modified timestamp
    SHA256


Identify known deployment backups including, where present:

STEP 24 / pre-V64

    core_business_dev-pre-v64-20260917T200210.sql

expected recorded SHA256:

    0f5fbd0ee6c2e7815d57a95c4a1947e7d06ce0bce41977a13aeb95bdab2505b1


STEP 27 / pre-V65

    core_business_dev-pre-v65-20260917T222529.sql

expected recorded SHA256:

    ffd4abb7674f5a4f268bad0198016cdfc62bd7ea7151326d84c7796e3263482e


Do NOT assume these are the only files.

Inventory all actual dumps.


======================================================================
2. VERIFY AGAINST RECORDED EVIDENCE
======================================================================

For each backup with existing Fabric deployment evidence:

compare:

    filename
    size if recorded
    SHA256


Require:

    HASH_MATCH=YES


If any previously recorded backup hash differs:

    STOP.

Do not archive a mutated backup as authentic evidence.


======================================================================
3. DETERMINE RESTRICTED DESTINATION
======================================================================

Inspect the existing structure under:

    GYPPORT-Storage


Locate the canonical restricted/sensitive archive area.

Expected concept:

    GYPPORT-Storage/Restricted


Do NOT invent an unrelated new storage hierarchy if an established one
already exists.


Create a bounded archive structure for Shared DEV backups, for example:

    GYPPORT-Storage/
      Restricted/
        Database-Backups/
          Shared-DEV/
            gm-expenses-release-readiness/


Use the actual storage conventions found in GYPPORT-Storage.


======================================================================
4. SENSITIVE DATA HANDLING
======================================================================

Treat every SQL dump as sensitive.

Do NOT:

- open it in an editor unnecessarily;
- print account/customer/personal rows;
- copy its contents into Fabric evidence;
- commit SQL dumps to Git;
- upload them to GitHub;
- move them into BoxGhost;
- expose credentials;
- expose personal data.


Evidence may record:

    filename
    size
    SHA256
    timestamps
    source path
    restricted destination

but NOT database row contents.


======================================================================
5. COPY FIRST — NEVER MOVE FIRST
======================================================================

For each validated source backup:

COPY to the restricted destination.

Preserve original filename.

Where practical preserve:

    modification timestamp


After copy verify:

    destination exists
    destination size == source size
    destination SHA256 == source SHA256


Require:

    COPY_HASH_MISMATCHES=0


Do not delete the Temp source yet.


======================================================================
6. RESTORE VALIDATION FROM RESTRICTED COPY
======================================================================

Using a disposable database environment only:

perform a restore validation from EACH restricted archive copy.


Do NOT restore over Shared DEV.


At minimum verify:

    SQL dump readable
    restore completes
    expected schema exists
    Flyway version matches dump era where determinable


For known backups:

pre-V64:
    expected pre-migration state around V63

pre-V65:
    expected Flyway V64


Use the original deployment evidence as authority for exact expectations.


Require:

    RESTRICTED_COPY_RESTORE_VALIDATION=PASS


If restore fails:

    preserve Temp source
    STOP cleanup.


======================================================================
7. CREATE ARCHIVE MANIFEST
======================================================================

Create an archive manifest in the restricted storage area.

Example:

    ARCHIVE_MANIFEST_SHARED_DEV_BACKUPS_STEP30.md


Record only metadata:

    STEP
    source path
    destination path
    filename
    SHA256
    size
    original deployment STEP
    backup purpose
    restore validation result
    archival date


Do NOT include SQL contents.


======================================================================
8. TEMP SOURCE CLEANUP GATE
======================================================================

Only after ALL of the following are true:

    source hash verified
    restricted copy exists
    destination hash matches
    restore validation passes
    archive manifest written

may Temp cleanup be considered.


Before deleting anything report:

    TEMP_BACKUPS_SAFE_TO_REMOVE=YES/NO


If YES and this prompt's Owner authorization permits cleanup:

delete only the successfully archived source backup files from:

    %LOCALAPPDATA%\Temp\gypport\shared-dev-backups


Do NOT delete the parent directory if unrelated files remain.


If there is any uncertainty:

    keep the Temp source
    report CLEANUP_DEFERRED=YES


======================================================================
9. POST-CLEANUP VERIFICATION
======================================================================

For every archived backup require:

    restricted copy exists
    restricted SHA256 correct
    Temp source absent only if cleanup succeeded


Return:

    ARCHIVED_COUNT
    TEMP_REMOVED_COUNT
    TEMP_RETAINED_COUNT


======================================================================
10. FABRIC EVIDENCE
======================================================================

Record STEP 30 evidence in Fabric.

Do NOT include SQL dumps.


Include:

- prompt
- archive metadata
- source/destination hashes
- restore-validation result
- cleanup result


Update ONLY the existing:

    Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md


Do NOT create another CURRENT_STEP.md.


======================================================================
11. FABRIC COMMIT
======================================================================

Audit current Fabric state first.

Expected intentional remaining WIP:

    2 untracked Owner files


Do NOT stage them.


Stage only explicit STEP 30 evidence/current-step paths.


Forbidden:

    git add .
    git add -A
    git add -u


Commit using Fabric convention.

Suggested:

    docs(expenses): archive Shared DEV backups securely


Then normal fast-forward push if origin/main has no divergence.


======================================================================
12. FROZEN MVP PROOF
======================================================================

Verify read-only:

GM_EXPENSES_HEAD=
39a2adf4dfff0196208a1f80719be1c12c047ac2

GYSTIGO_HEAD=
5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc

SHARED_DEV_VERSION=
65


Require:

    SOURCE_CODE_CHANGED=NO
    SHARED_DEV_MODIFIED=NO
    OWNER_CASE_MODIFIED=NO


======================================================================
13. REQUIRED REPORT
======================================================================

Return:

STEP=
GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30

STATUS=
ARCHIVED_AND_VERIFIED
or
BLOCKED


INVENTORY:

BACKUPS_FOUND=

KNOWN_BACKUPS_MATCH_RECORDED_HASHES=
YES/NO


ARCHIVE:

RESTRICTED_DESTINATION=

ARCHIVED_COUNT=

COPY_HASH_MISMATCHES=
0

RESTORE_VALIDATION=
PASS/FAIL

ARCHIVE_MANIFEST=


PRE_V64:

FOUND=
YES/NO

SOURCE_SHA256=

DESTINATION_SHA256=

HASH_MATCH=
YES/NO

RESTORE_VALIDATION=
PASS/FAIL


PRE_V65:

FOUND=
YES/NO

SOURCE_SHA256=

DESTINATION_SHA256=

HASH_MATCH=
YES/NO

RESTORE_VALIDATION=
PASS/FAIL


TEMP:

TEMP_BACKUPS_SAFE_TO_REMOVE=
YES/NO

TEMP_REMOVED_COUNT=

TEMP_RETAINED_COUNT=

CLEANUP_DEFERRED=
YES/NO


FABRIC:

FABRIC_NEW_HEAD=

EVIDENCE_COMMITTED=
YES/NO

PUSHED=
YES/NO

LOCAL_REMOTE_MATCH=
YES/NO

OWNER_WIP_STAGED=
NO


FROZEN_MVP:

GM_EXPENSES_HEAD=
39a2adf4dfff0196208a1f80719be1c12c047ac2

GYSTIGO_HEAD=
5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc

SHARED_DEV_VERSION=
65

SOURCE_CODE_CHANGED=
NO

SHARED_DEV_MODIFIED=
NO

OWNER_CASE_MODIFIED=
NO


NEXT_OPTIONAL_STEP=
GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31

PRE_PRODUCTION_SECURITY_DEBT=
SPRING_GENERATED_PASSWORD_STARTUP_LOG

STOP_FOR_OWNER_REVIEW=
YES

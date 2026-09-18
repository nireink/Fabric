# CURRENT STEP

The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not
canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,
not an Owner approval and not an execution trigger.

```text
CURRENT_TRACK=GM_EXPENSES_RELEASE_READINESS
CURRENT_STEP_ID=GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30
CURRENT_PHASE=SHARED_DEV_BACKUPS_ARCHIVED
MODE=READ_ONLY_INVENTORY_HASH_VERIFY_SECURE_ARCHIVE_COPY_RESTORE_VALIDATION_TEMP_CLEANUP_EVIDENCE
STATUS=ARCHIVED_AND_VERIFIED

PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30.md
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
BASELINE_REUSE_REQUIRED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO

OWNER_EXECUTION_AUTHORIZED=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

## Next action

STOP: GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30 is complete; Fabric = the commit that records this STEP. No source, database or runtime changed; no SQL content is in Fabric.
- ARCHIVED: the STEP 24 pre-V64 and STEP 27 pre-V65 Shared DEV dumps, with their companion records, in GYPPORT_STORAGE/Restricted/Gystigo/shared-dev-deployment-24-2026-09-17 and shared-dev-deployment-27-2026-09-17 (manifest ARCHIVE_MANIFEST_SHARED_DEV_BACKUPS_STEP30.md)
- VERIFIED: hashes equal to the recorded evidence, COPY_HASH_MISMATCHES=0, restore validation PASS from the restricted copies (107/30/Flyway 63 and 108/35/Flyway 64, financial checksums 6/6)
- TEMP: both dumps removed after the gate; 9 non-sensitive companion and migration-copy files remain in the Temp folder
- GM_EXPENSES_MVP_STATUS=FROZEN_OWNER_ACCEPTED_PUSHED; SHARED_DEV=Flyway 65; FABRIC_UNTRACKED_OWNER_WIP=2 files (unchanged)
Next optional STEP: GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31 (its restricted folder already holds a STEP 18 evidence tree). Separate pre-production debt: SPRING_GENERATED_PASSWORD_STARTUP_LOG. No next STEP is selected.

## How to use this file

- Every agent reads this file at startup, before deciding what to work on.
- `PROMPT_SOURCE` resolves from the GYPPORT workspace root and must be read in full before acting.
- `REQUIRED_BASELINES` resolves by BASELINE_ID against
  `Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/`; apply `VERIFIED_BASELINE_REUSE.md`
  before running any historical regression.
- `STATUS=READY_TO_START` is not permission. Execution requires `OWNER_EXECUTION_AUTHORIZED=YES` or a
  current explicit Owner instruction authorizing this STEP.
- Repository and schema evidence outrank this file. If they disagree, stop and report; never guess.
- One global CURRENT_STEP exists for the MVP period. Do not create per-module variants without an
  explicit Owner decision.
- This file is prepared by the closeout workflow (`Fabric/tools/continuity/`), which never approves,
  never executes and never commits.

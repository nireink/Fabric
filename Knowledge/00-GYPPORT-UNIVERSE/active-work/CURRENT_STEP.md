# CURRENT STEP

The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not
canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,
not an Owner approval and not an execution trigger.

```text
CURRENT_TRACK=GM_EXPENSES_RELEASE_READINESS
CURRENT_STEP_ID=GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31
CURRENT_PHASE=HISTORICAL_EVIDENCE_RECOVERED_TRACK_CLOSED
MODE=READ_ONLY_DISCOVERY_EXACT_SOURCE_RECOVERY_HASH_AND_PROVENANCE_VERIFY_BOXGHOST_EVIDENCE_RECONCILIATION_CONTINUITY_CLOSEOUT_CONTROLLED_FABRIC_COMMIT_PUSH
STATUS=EVIDENCE_RECOVERED_AND_TRACK_CLOSED

PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31.md
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
BASELINE_REUSE_REQUIRED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO

OWNER_EXECUTION_AUTHORIZED=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

## Next action

STOP: GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31 is complete; Fabric = the commit that records this STEP. No source, database or runtime changed; no SQL content is in Fabric.
- GM_EXPENSES_RELEASE_READINESS=COMPLETE
- GM_EXPENSES_MVP_STATUS=FROZEN_OWNER_ACCEPTED_PUSHED (gm-expenses 39a2adf, Gystigo master 5eed5d6, Shared DEV Flyway 65)
- BACKUP_ARCHIVAL_30=COMPLETE
- HISTORICAL_EVIDENCE_RECOVERY_31=COMPLETE: STEP 18 evidence recovered byte-exact into BoxGhost (96 files, 0 hash mismatches; the V43 dump stays restricted); the prompts of STEPs 18, 29 and 29C stored EXACT from the session transcript
- AI_GOVERNANCE_REFERENCE_WIRING=ALREADY_RESOLVED; NEW_AGENTS_EDIT_REQUIRED=NO; REGLAS_CHANGED=NO; FABRIC_UNTRACKED_OWNER_WIP=2 files (unchanged)
Remaining independent pre-production debt: SPRING_GENERATED_PASSWORD_STARTUP_LOG. NEXT_GM_EXPENSES_STEP=NONE. No next STEP is selected.

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

# CURRENT STEP

The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not
canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,
not an Owner approval and not an execution trigger.

```text
CURRENT_TRACK=GM_EXPENSES_RELEASE_READINESS
CURRENT_STEP_ID=GYPPORT_FABRIC_UNTRACKED_KNOWLEDGE_RECONCILIATION_29D
CURRENT_PHASE=FABRIC_UNTRACKED_RECONCILED
MODE=VERIFY_COMPARE_CANONICALIZE_ARCHIVE_COMMIT_PUSH
STATUS=FABRIC_UNTRACKED_RECONCILIATION_COMPLETED

PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GYPPORT_FABRIC_UNTRACKED_KNOWLEDGE_RECONCILIATION_29D.md
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
BASELINE_REUSE_REQUIRED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO

OWNER_EXECUTION_AUTHORIZED=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

## Next action

STOP: GYPPORT_FABRIC_UNTRACKED_KNOWLEDGE_RECONCILIATION_29D is complete; Fabric = the commit that records this STEP. No source, runtime, Shared DEV or other repository changed.
- FABRIC_UNTRACKED_RECONCILIATION=COMPLETED
- COMMITTED: the 3 AI governance policies, ADR-01 (still active), the Security and the 2 UIX baselines, gm-expenses 03/04/05 as historical initial-development baselines, and the gm-expenses README as a knowledge index
- RELOCATED: the 3 STEP 02 audit files to BoxGhost imports; the superseded proposed ADR-01 and the 14 reference-template files to GYPPORT_STORAGE (ARCHIVE_HASH_MISMATCHES=0)
- REMAINING_INTENTIONAL_OWNER_WIP=2 files: Knowledge/Architecture/GYPPORT_REGLAS_CANONICAS_ARQUITECTURA_DOMINIO_UIX.md and Knowledge/gm-accounting/01-conceptual-model/GYPPORT_GM_ACCOUNTING_GENERAL_MODULE_MODEL_EXECUTION_PROMPT_v1.2.md
- GM_EXPENSES_MVP_STATUS=FROZEN_OWNER_ACCEPTED_PUSHED; GYSTIGO_ACTIVE_BRANCH=master (5eed5d6); SHARED_DEV=Flyway 65
Open Owner decisions: whether AGENTS.md references the AI policies; audits of the other dirty repositories; GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30; GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31; pre-production debt SPRING_GENERATED_PASSWORD_STARTUP_LOG. No next STEP is selected.

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

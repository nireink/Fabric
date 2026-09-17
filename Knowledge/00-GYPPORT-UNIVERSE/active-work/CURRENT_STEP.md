# CURRENT STEP

The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not
canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,
not an Owner approval and not an execution trigger.

```text
CURRENT_TRACK=GM_EXPENSES_RELEASE_READINESS
CURRENT_STEP_ID=GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17
CURRENT_PHASE=FINAL_PRECOMMIT_PROOF_AND_CONTROLLED_COMMITS
MODE=FINAL_PRECOMMIT_PROOF_AND_CONTROLLED_COMMITS
STATUS=GM_EXPENSES_MVP_COMMITTED_LOCAL_READY_FOR_SHARED_DEV

PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17.md
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
BASELINE_REUSE_REQUIRED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO

OWNER_EXECUTION_AUTHORIZED=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

## Next action

STOP: GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17 committed the accepted gm-expenses MVP locally and waits for Owner review; nothing was pushed.
Commits: gm-expenses 545eae0 (master), Gystigo bcb9591 (feature/gm-fleets-minimum-vehicle-master-01), Fabric = the commit that adds this file; migration head V63.
Verified baseline: GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17 (release COMMITTED_LOCAL, READY_FOR_SHARED_DEV_MIGRATION). Shared DEV is still V43 and the official DEV backend is not rebuilt.
Next gate, only after Owner acceptance: fresh Shared DEV backup, migrate V43 to V63 per gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/handoffs/SHARED_DEV_MIGRATION_V43_V63_PLAN_2026-09-16.md, rebuild the DEV backend from the accepted commits, Owner real-login smoke.
Not authorized now: push, Shared DEV migration, official DEV backend rebuild or restart, Shared DEV legacy data cleanup, Gystigo branch normalization.

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

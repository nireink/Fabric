# CURRENT STEP

The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not
canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,
not an Owner approval and not an execution trigger.

```text
CURRENT_TRACK=GM_EXPENSES_RELEASE_READINESS
CURRENT_STEP_ID=GM_EXPENSES_CONTROLLED_COMMIT_GATE_23
CURRENT_PHASE=PRECOMMIT_AUDIT_THEN_EXPLICIT_STAGING_THEN_COMMIT
MODE=READ_ONLY_PRECOMMIT_AUDIT_THEN_EXPLICIT_STAGING_THEN_COMMIT
STATUS=COMMITTED_LOCALLY_WAITING_OWNER_REVIEW

PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_CONTROLLED_COMMIT_GATE_23.md
REQUIRED_BASELINES=GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
BASELINE_REUSE_REQUIRED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO

OWNER_EXECUTION_AUTHORIZED=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

## Next action

STOP: the gm-expenses MVP closure is committed locally and nothing is pushed. gm-expenses 874a3e5, Gystigo 0293ff4, Fabric on this commit; 57 accepted paths, 0 unrelated paths staged, 15 unrelated WIP paths preserved untouched.
Runtime is deliberately unchanged: Shared DEV is still V63 and 8080 still serves the STEP 18 image, so the Owner screen keeps showing no EXP and no ID until deployment.
NEXT_STEP=GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24 - migrate Shared DEV V63 to V64 with a verified backup, rebuild the official DEV backend from gm-expenses 874a3e5 and Gystigo 0293ff4, and smoke it. Not performed yet.
After deployment, and only then, the Owner corrects the live USD 300 return of Case 437a92bf through the authenticated reverso, so the real actor and instant are recorded.
Push of the three repositories remains a separate Owner authorization.

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

# CURRENT STEP

The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not
canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,
not an Owner approval and not an execution trigger.

```text
CURRENT_TRACK=GM_EXPENSES_RELEASE_READINESS
CURRENT_STEP_ID=GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26
CURRENT_PHASE=VERIFY_EXISTING_V65_THEN_CONTROLLED_COMMIT
MODE=CONTINUE_FROM_CURRENT_STEP_THEN_CONTROLLED_COMMIT
STATUS=COMMITTED_LOCALLY_WAITING_OWNER_REVIEW

PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26.md
REQUIRED_BASELINES=GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
BASELINE_REUSE_REQUIRED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO

OWNER_EXECUTION_AUTHORIZED=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

## Next action

STOP for Owner review: the V65 permanent expediente numbering and the 25A display correction are committed locally - gm-expenses 39a2adf, Gystigo 5eed5d6, Fabric on this commit. Nothing is pushed.
Runtime is unchanged on purpose: Shared DEV is V64, V65_DEPLOYED=NO, and 8080 serves gystigo-backend:4.1.0-java25-gm-expenses-v64-0293ff4, which sends no expenseSequence, so the real screen still shows no EXP prefix.
NEXT_STEP=GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27 - back up Shared DEV, migrate V64 to V65 through the Host Flyway, rebuild the official backend from gm-expenses 39a2adf and Gystigo 5eed5d6, smoke it. Not performed; it needs its own Owner authorization.
After deployment the real tenant reads Compra Filtro EXP. 08 (ID 202609170001) and VIAJE QUITO EXP. 09 (ID 202609170002), the real creation order; the Owner Case USD 300 return still awaits the Owner reverso.

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

# CURRENT STEP

The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not
canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,
not an Owner approval and not an execution trigger.

```text
CURRENT_TRACK=GM_EXPENSES_RELEASE_READINESS
CURRENT_STEP_ID=GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28
CURRENT_PHASE=MVP_FREEZE
MODE=OWNER_RUNTIME_VERIFICATION_THEN_AUTHENTICATED_CORRECTION_THEN_FREEZE
STATUS=FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL

PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28.md
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
BASELINE_REUSE_REQUIRED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO

OWNER_EXECUTION_AUTHORIZED=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

## Next action

STOP: GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28 is complete. The gm-expenses MVP is FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL: gm-expenses 39a2adf, Gystigo 5eed5d6, Shared DEV Flyway 65, Fabric = the commit that adds this file. Nothing was pushed.
The Owner accepted EXP. 08: Compra Filtro (ID 202609170001), EXP. 09: VIAJE QUITO (ID 202609170002) and the card layout in the real app, and reversed the USD 300.00 return through the product (events 35 and 36 reverse 29 and 30). Final smoke 29/29, read-only.
The Case reads Pendiente 80.00 Por reembolsar, its real position; the reimbursement test is deferred and the synthetic DEV data is kept, both by Owner decision.
Frozen baseline: GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17. No MVP architecture or UI change without a new explicit track; new ideas go to backlog, post-MVP or the next release.
Pending Owner decisions: the push of gm-expenses, Gystigo and Fabric; moving the Shared DEV backups from %LOCALAPPDATA%\Temp to GYPPORT_STORAGE (Restricted); promoting the missing STEP 18 evidence. No next STEP is selected.

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

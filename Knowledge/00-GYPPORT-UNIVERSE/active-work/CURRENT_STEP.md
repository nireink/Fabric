# CURRENT STEP

The single global pointer to the GYPPORT work that is active now. It is a continuity pointer: not
canonical knowledge, not a copy of the prompt, not a transcript, not a replacement for BoxGhost,
not an Owner approval and not an execution trigger.

```text
CURRENT_TRACK=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
CURRENT_STEP_ID=PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
CURRENT_PHASE=PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
MODE=AUDIT_ONLY_FIRST
STATUS=READY_TO_START

PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/PKG-2D/PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md
REQUIRED_BASELINES=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15
BASELINE_REUSE_REQUIRED=YES
FULL_PKG2C_REGRESSION_RERUN=NO

OWNER_EXECUTION_AUTHORIZED=NO
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

## Next action

Wait for explicit Owner authorization. Once authorized, read `PROMPT_SOURCE` completely and execute
PKG-2D in `AUDIT_ONLY_FIRST` mode, reusing the required verified baseline instead of rerunning the
accepted PKG-2C verification.

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

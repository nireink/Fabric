# GYPPORT — CANONICAL-MEMORY-FOUNDATION-CLOSEOUT Verified Baseline

**Baseline ID:** `GYPPORT-CANONICAL-MEMORY-FOUNDATION-CLOSEOUT-VERIFIED-BASELINE-2026-09-15`  
**Status:** `OWNER_ACCEPTED_COMMITTED_LOCAL`  
**Date:** 2026-09-15  
**Step:** `GYPPORT_CANONICAL_MEMORY_FOUNDATION_01`  
**Phase:** `FINAL_CANONICAL_MEMORY_FOUNDATION_CLOSEOUT_CORRECTION`

## Purpose

This is the canonical reusable verification baseline of an Owner-accepted, locally committed STEP.

Future STEPs MUST NOT rerun its complete historical regression while this baseline remains valid. They first
classify it as REUSE, PARTIAL_INVALIDATION or FULL_INVALIDATION under the policy:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/VERIFIED_BASELINE_REUSE.md
```

## Baseline record

```text
BASELINE_ID=GYPPORT-CANONICAL-MEMORY-FOUNDATION-CLOSEOUT-VERIFIED-BASELINE-2026-09-15
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
STEP=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01
PHASE=FINAL_CANONICAL_MEMORY_FOUNDATION_CLOSEOUT_CORRECTION
DATE=2026-09-15
MIGRATION_HEAD=V58
VERIFIED_FILE_COUNT=2
BASELINE_REUSE_ALLOWED=YES
SUPERSEDES_BASELINE_ID=GYPPORT-CANONICAL-MEMORY-FOUNDATION-VERIFIED-BASELINE-2026-09-15
```

## Accepted commits

```text
Fabric=80e7035052492372f99e36e509a3298eab07f784
gypport-engineering-template=74ff60cd6a789083db30488f5ac0f46dbf1cf86b
```

Parent commits:

```text
Fabric=3bddf2443e36ebada8fdbf8762b6373fdc7e0219
gypport-engineering-template=9084081fee80651cb450ad5878557cccb11dcf9d
```

## Accepted commit manifest

Secondary evidence read from the accepted commits, one line per file: `<status> <abbreviated blob id> <path>`,
with paths relative to the repository.

```text
Fabric 80e7035052492372f99e36e509a3298eab07f784 files=1
M b5a627b3e782 tools/continuity/Set-GypportCurrentStep.ps1
```

```text
gypport-engineering-template 74ff60cd6a789083db30488f5ac0f46dbf1cf86b files=1
A ccbac55de564 docs/governance/architecture/EXTERNAL_REFERENCES.md
```

## Verification evidence

```text
BASELINE_REUSE_DECISION=PARTIAL_INVALIDATION
BASELINE_REUSE_REASON=one verified file of the superseded baseline changed, Fabric/tools/continuity/Set-GypportCurrentStep.ps1; the other 433 verified files and every architecture invariant are unchanged
AFFECTED_VERIFICATION_SLICE=CURRENT_STEP continuity tooling only
SLICE_RERUN=YES
TOOL_PARSE_POWERSHELL_5_1=PASS
CURRENT_STEP_MATERIALIZER_IDEMPOTENCE=PASS_BYTE_IDENTICAL (2002 bytes, sha256 c1955a45f2c11ae6...)
MATERIALIZER_DETERMINISM=PASS
MATERIALIZER_REFUSAL_GUARDS=8/8 REFUSED (wrong mode, missing prompt source, unregistered baseline, wrong output name, bad regression key, bad regression value, next action with a code fence, empty track)
MATERIALIZER_DEFAULTS_UNAUTHORIZED=PASS
MATERIALIZER_COMMITS=NONE
CURRENT_STEP_CHANGED=NO
CURRENT_STEP_STATUS=READY_TO_START
CURRENT_STEP_OWNER_EXECUTION_AUTHORIZED=NO
ENGINEERING_EXTERNAL_REFERENCES_CLASSIFICATION=ACTIVE_UNIQUE_REGISTER_IN_A_REAL_REPOSITORY, previously untracked
ENGINEERING_EXTERNAL_REFERENCES_COPIES_IN_WORKSPACE=1
INTENDED_FOUNDATION_CHANGE_LEFT_UNCOMMITTED=0
STAGED_SCOPE_EXACT=YES (1 file per commit)
UNRELATED_FILES_STAGED=0
WHITESPACE_CHECK=PASS in both correction commits
PKG2C_FILES_UNCHANGED=52/52
GM_EXPENSES_WIP_PRESERVED=YES
OTHER_OWNER_WIP_PRESERVED=YES
APPLICATION_TESTS_RERUN=NO
DATABASE_WRITES=NONE
PKG2D_EXECUTED=NO
PUSH_PERFORMED=NO
```

## Architecture invariants

```text
FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT=YES
CANONICAL_REGLAS_COUNT=1
SECOND_ACTIVE_MEMORY_ROOT=0
CURRENT_STEP_GLOBAL=YES
CURRENT_STEP_IS_THE_CONTRACT=YES, the materializer is reconciled with the canonical file and never the other way round
AGENT_AUTO_DISCOVERY_ENABLED=YES
GYPPORT_STORAGE_LOGICAL_ID=GYPPORT_STORAGE
STORAGE_LOCATION_SINGLE_SOURCE=YES
BOXGHOST_OPERATIONAL_HISTORY_COMPLETE=YES
OLD_GOVERNANCE_ACTIVE_AUTHORITY=NO
GYPPORT_BRAIN_IMPLEMENTED=NO
PKG2D_EXECUTED=NO
```

## Known pre-existing debts

```text
KNOWN_PREEXISTING_FAILURES=4
1. The engineering template repository carries 14 modified tracked files and the untracked .dockerignore and sibling architecture documents; that is pre-existing Owner work and was deliberately left untouched.
2. A stale, empty .git/index.lock dated 2026-08-07 blocked the engineering template repository; it was preserved as evidence and removed, which is git's own documented remedy for a crashed process.
3. git diff --cached --check still reports whitespace in the migrated history committed by the superseded baseline; that content is byte-exact and must not be reformatted.
4. The GYPPORT Brain is specified in GYPPORT_MEMORY_ARCHITECTURE.md but not implemented.
```

These are not regressions of this STEP. Future STEPs do not fix them unless they are explicitly in scope.

## Reuse contract

```text
BASELINE_FOUND=YES
BASELINE_ID=GYPPORT-CANONICAL-MEMORY-FOUNDATION-CLOSEOUT-VERIFIED-BASELINE-2026-09-15
BASELINE_REUSE_DECISION=REUSE|PARTIAL_INVALIDATION|FULL_INVALIDATION
BASELINE_REUSE_REASON=<short evidence-based reason>
```

REUSE means `FULL_HISTORICAL_REGRESSION_RERUN=NO`: the new STEP runs only its own tests, impact-selected tests
and the required integration smoke. The decision is proven from repository ancestry, path and contract impact,
migration semantics and current Owner decisions. A complete historical regression is never selected merely
"to be safe".

## Baseline invalidation triggers

- the canonical CURRENT_STEP representation changes without the materializer being able to reproduce it
- a second writable Reglas.md or a second active memory root appears
- GYPPORT_LOCATIONS.properties gains a second GYPPORT_STORAGE_ROOT, or the resolved root stops existing
- either Gystigo entrypoint gains governance text or a literal storage path
- the Fabric branch docs/gm-ai-workspace-canonical-unification-01 is merged, rebased or deleted

An invalidation does not by itself require a full rerun: impact analysis selects the smallest sufficient
verification scope.

## Closeout

```text
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
GENERATED_BY=Fabric/tools/verification/New-GypportVerifiedBaseline.ps1
GENERATOR_MODE=GENERATE_ONLY
GENERATOR_APPROVAL=NONE
OWNER_REVIEW_REQUIRED=YES
AUTO_START_NEXT_STEP=NO
COMMIT_PERFORMED_BY_GENERATOR=NO
PUSH_PERFORMED=NO
```

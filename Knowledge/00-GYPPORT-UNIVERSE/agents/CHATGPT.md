# CHATGPT.md — GYPPORT® ChatGPT Working Instructions

ChatGPT acts as architecture coordinator, STEP designer, reviewer and implementation assistant for GYPPORT.

## Shared Governance

`AGENTS.md` in this folder is mandatory for ChatGPT, and ChatGPT cannot discover it: it has no
filesystem access. Every GYPPORT ChatGPT project or conversation must receive both `AGENTS.md` and
`CHATGPT.md` from this folder; if `AGENTS.md` is not in the context, request it before any GYPPORT
work. `AGENTS.md` holds the Mandatory Knowledge Gate, Working Governance, Canonical Domain
Boundaries, UIX Baseline, Architecture Gate, Conflict Gate, Audit / Provenance protection and the
Continuity Packet. This file adds only the ChatGPT-specific rules.

## GYPPORT Memory Roots and Artifact Placement

Fabric is the single GYPPORT memory root. The full contract is
`Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md`.

```text
FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT=YES
CANONICAL_KNOWLEDGE_ROOT=Fabric/Knowledge
OPERATIONAL_MEMORY_ROOT=Fabric/gm-ai-boxghost
GYPPORT_STORAGE_ID=GYPPORT_STORAGE
GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties
ACTIVE_WORK_ROOT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work
PRODUCT_HOST_ROOT=Gystigo
MODULE_ROOT=Modules
GM_AI_WORKSPACE_ROOT=Modules/gm-ai-workspace
```

Paths are relative to the GYPPORT workspace root, the directory that contains `Gystigo/`,
`Fabric/` and `Modules/`. `GYPPORT_STORAGE` is a logical role, not a path: resolve its physical root through
the location registry above and never hardcode it.

Placement rules:

```text
DO_NOT_CREATE_CANONICAL_KNOWLEDGE_IN_TEMP
DO_NOT_CREATE_OPERATIONAL_HISTORY_IN_ARBITRARY_PRODUCT_DOCS
PROMOTE_VALUABLE_TEMP_ARTIFACTS_BEFORE_STEP_CLOSE
RAW_SOURCE_TO_GYPPORT_STORAGE
DERIVED_CANONICAL_KNOWLEDGE_TO_FABRIC_KNOWLEDGE
OPERATIONAL_EXECUTION_HISTORY_TO_BOXGHOST
```

- Create every new durable GYPPORT artifact directly in its canonical owner path.
- What GYPPORT knows, once it is canonical, belongs to `Fabric/Knowledge`.
- What happened — conversations, sessions, prompts, interventions, handoffs, decisions, approvals,
  evidence, audits and continuity — belongs to `Fabric/gm-ai-boxghost`; see its
  `BOXGHOST_STRUCTURE.md`.
- Raw, original and heavy sources belong to `GYPPORT_STORAGE`, resolved through the location
  registry. Nothing there is canonical knowledge or operational memory, whatever a file there is
  named. If the resolved root is missing, report `GYPPORT_STORAGE_AVAILABLE=NO` and stop: never
  create a replacement root, and never fall back to a temporary folder, the Desktop or Downloads.
- Scratchpads, `AppData\Local\Temp`, Codex temporary folders, provider caches, provider
  compaction, the Desktop and Downloads are never durable GYPPORT memory. Promote anything valuable
  before the STEP closes.
- Copies of governance files in git worktrees, `UI_Experiments/`, `GYPPORT_STORAGE` or the legacy
  `Governance/` repository are historical and never authoritative.

## Startup Discovery

Every GYPPORT agent starts here, in this order:

```text
1. CURRENT_STEP        Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md
2. RULES               Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md
3. AGENT GOVERNANCE    Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/ (AGENTS.md and this file)
4. LOCATIONS           Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties
                       when external raw storage is involved
5. PROMPT_SOURCE       resolve it from CURRENT_STEP and read it completely
6. REQUIRED_BASELINES  resolve the ids under verification-baselines/ and apply
                       VERIFIED_BASELINE_REUSE.md before any historical regression
7. ACT                 only on the current Owner-authorized action
```

- `STATUS=READY_TO_START` is not permission. Execution requires `OWNER_EXECUTION_AUTHORIZED=YES`
  in CURRENT_STEP, or a current explicit Owner instruction authorizing that STEP.
- Never restart an Owner-accepted completed STEP.
- Do not choose a full baseline invalidation to be safe; apply the reuse policy.
- Repository, schema and test evidence outrank a continuity file. If they disagree, stop and report
  the discrepancy; never guess.

## Artifact Routing

Classify a durable artifact before creating it, then route it:

```text
CANONICAL_KNOWLEDGE                  -> Fabric/Knowledge
  architecture, ADRs, rules, standards, verified baselines, Owner-approved derived knowledge,
  canonical agent and collaboration governance

OPERATIONAL_MEMORY                   -> Fabric/gm-ai-boxghost
  conversations, sessions, interventions, handoffs, execution reports, continuity, audit evidence,
  operational decisions, track and context history, Owner review evidence

RAW_HEAVY_ORIGINAL_SOURCE            -> resolve(GYPPORT_STORAGE)
  books, PDFs, datasets, database dumps, source archives, external reference collections, raw
  research, large exports, original binaries

PRODUCT_CODE_OR_PRODUCT_SPECIFIC_DOC -> the owning repository or module

TEMPORARY_DISPOSABLE_WORK            -> a scratchpad is allowed, but
                                        VALUABLE_TEMP_ONLY_ARTIFACTS_AT_STEP_CLOSE=0
```

If a temporary artifact turns out to be valuable, promote it before the STEP closes: knowledge to
`Fabric/Knowledge`, history and evidence to `Fabric/gm-ai-boxghost`, raw sources to
resolve(GYPPORT_STORAGE). The only durable copy of anything valuable never stays in a temporary
folder, a provider cache, the Desktop or Downloads.


## ChatGPT Coordination Rules

- Preserve continuity across STEPs instead of redesigning previously accepted foundations.
- Before proposing a replacement architecture, inspect the canonical Universe baseline and relevant project documentation.
- Distinguish clearly between:
  - current implementation;
  - desired target;
  - historical rationale;
  - Owner decision;
  - future possibility.
- Do not transform a future possibility into an implementation requirement without Owner approval.
- Prefer one clear next STEP over multiple parallel initiatives.
- When reviewing agent output, verify whether evidence actually proves the claimed ownership, schema safety, tests and Git state.
- Do not recommend deleting or normalizing an existing MDM/Party relationship merely because it looks redundant.
- Keep prompts bounded and explicit about protected modules, commit/push rules and verification gates.


## Prompt Design Rule

A GYPPORT implementation prompt should normally contain:

```text
STEP
OWNER DECISION / OBJECTIVE
READ-ONLY AUDIT FIRST
CANONICAL BOUNDARIES
PROTECTED AREAS
IMPLEMENTATION LIMITS
VERIFY
REPORT
STOP FOR OWNER REVIEW
```

Do not overload one STEP with unrelated cleanup.

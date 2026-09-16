# CODEX.md — GYPPORT® Codex Working Instructions

Codex is a coding and implementation agent for GYPPORT. Repository evidence and canonical documentation are authoritative over assumptions.

## Shared Governance

`AGENTS.md` in this folder is mandatory for Codex. Codex discovers `Gystigo/AGENTS.md`, which is a
technical entrypoint: it points here. Read `AGENTS.md` and this file in full before any work.
`AGENTS.md` holds the Mandatory Knowledge Gate, Working Governance, Canonical Domain Boundaries,
UIX Baseline, Architecture Gate, Conflict Gate, Audit / Provenance protection and the Continuity
Packet. This file adds only the Codex-specific rules.

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


## Codex Coding Rules

- Inspect the active checkout and Git status before modifying files.
- Work on the existing active line unless the Owner explicitly authorizes a branch/worktree.
- Search for existing domain types, ports, migrations and tests before creating new ones.
- Never introduce a parallel source of truth when an existing canonical identity or master already exists.
- Prefer module ports/contracts over direct cross-domain SQL access.
- Keep domain/application code free from Host/framework concerns where the established architecture requires it.
- Preserve shared-schema compatibility and current identifiers.
- Use additive Flyway migrations by default.
- Never drop/recreate a table or regenerate IDs as a cleanup shortcut.
- Avoid N+1 cross-module query patterns; prefer narrow batch query ports when composition is required.
- Do not silently expand the scope when tests expose unrelated debt; classify and report it.
- Use targeted safe tests. Do not run commands that may mutate shared DEV unless explicitly authorized.


## Controlled Commit Rule

When the Owner authorizes a commit:

- verify expected branch/HEAD;
- inspect `git status`;
- stage only explicit STEP paths;
- run `git diff --cached --check`;
- inspect cached name/status and stat;
- prove unrelated WIP is unstaged;
- commit locally;
- do not push unless separately authorized.

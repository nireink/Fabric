# GYPPORT Memory Architecture

```text
DOCUMENT=GYPPORT_MEMORY_ARCHITECTURE
STATUS=OWNER_DECISION_APPLIED
OWNER_DECISION_DATE=2026-09-15
TRACK=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01
SCOPE=WHERE_EVERY_DURABLE_GYPPORT_ARTIFACT_BELONGS
AUTHORITY=CANONICAL
```

This is the only document that defines the GYPPORT memory roots and their ownership. Every other
document that needs them references this one; none of them redefines them.

## 1. Roots

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
`Fabric/` and `Modules/`. `GYPPORT_STORAGE` is a logical role, never a hardcoded path: its physical
root is resolved through the location registry (section 2.3.1).

| Root | Holds | One sentence |
|---|---|---|
| `Fabric/Knowledge` | canonical knowledge | what GYPPORT knows |
| `Fabric/gm-ai-boxghost` | operational memory | everything that happened, kept reconstructable |
| `GYPPORT_STORAGE` (logical role) | raw, original and heavy sources | what GYPPORT was given or collected |
| `Modules/gm-ai-workspace` | software | the application that reads and orchestrates the memory |
| `Gystigo` | product | the Host and its own technical documentation |
| `active-work/CURRENT_STEP.md` | the active work pointer | what GYPPORT is working on now |

## 2. What belongs where

### 2.1 `Fabric/Knowledge` — canonical knowledge

Architecture, ADRs and domain ownership; rules; global agent governance; collaboration governance;
standards; verified baselines; Owner-approved derived knowledge; the memory architecture itself;
the GYPPORT Brain contract; STEP definitions that are canonical knowledge.

It does not hold raw conversations, nor temporary logs unless they have been distilled into
knowledge with their source recorded.

### 2.2 `Fabric/gm-ai-boxghost` — operational memory (BoxGhost)

Full conversations; sessions; durable prompts and responses; interventions; handoffs; execution
reports; Owner review packets; operational decisions; approvals; evidence; audits; continuity;
context history; generated operational artifacts; raw AI collaboration history; track state.

Raw operational memory is never replaced by a summary. Its structure is defined in
`Fabric/gm-ai-boxghost/BOXGHOST_STRUCTURE.md`.

### 2.3 `GYPPORT_STORAGE` — raw persistent storage (logical role)

Books, PDFs, collections, archives, datasets, dumps, research, originals, exports, binary evidence
and heavy data.

```text
GYPPORT_STORAGE_IS_CANONICAL_KNOWLEDGE=NO
GYPPORT_STORAGE_IS_OPERATIONAL_MEMORY=NO
GYPPORT_STORAGE_IS_A_SECOND_MEMORY_ROOT=NO
GYPPORT_STORAGE_DUPLICATE_CANONICAL_ROLE=NO
GYPPORT_STORAGE_GOOGLE_DRIVE_SYNC=DISABLED
GOOGLE_DRIVE_IS_GYPPORT_STORAGE_BACKEND=NO
GOOGLE_DRIVE_IS_GYPPORT_BACKUP=NO
GOOGLE_DRIVE_IS_PART_OF_GYPPORT_MEMORY_ARCHITECTURE=NO
```

Nothing in `GYPPORT_STORAGE` is canonical or authoritative, whatever a file there is named.
Canonical Fabric documents are not copied into it. Dated backups and superseded versions may be
archived there, and they are history, never the live document.

Its areas are `External/` (raw external collections), `Fabric/` and `Gystigo/` (raw sources, dated
backups, inventory and recovery packages), `IAs Agents/` (archived AI project bases) and
`Restricted/` (sensitive archives).

### 2.3.1 Physical location and availability

The logical role is permanent; the physical location is configuration. One registry holds it:

```text
GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties
KEY=GYPPORT_STORAGE_ROOT
STORAGE_LOCATION_SINGLE_SOURCE=YES
FUTURE_NAS_MOVE_REQUIRES_ARCHITECTURE_CHANGE=NO
```

Every agent and tool resolves the root before reading or writing raw material:

```text
resolve(GYPPORT_STORAGE) -> GYPPORT_LOCATIONS.properties -> GYPPORT_STORAGE_ROOT
```

If the resolved root does not exist or is unavailable:

```text
GYPPORT_STORAGE_AVAILABLE=NO
-> STOP and report STORAGE UNAVAILABLE
STORAGE_UNAVAILABLE_FALLBACK_CREATION=NO
```

It never creates a replacement storage root, never falls back to a temporary folder, the Desktop or
Downloads, and never edits the registry without Owner-approved intent.

Moving the library to a NAS is a configuration migration: update `GYPPORT_STORAGE_ROOT`, validate
the new root, continue. Prefer a stable UNC path over a machine-dependent mapped drive letter. No
governance, memory, BoxGhost, CURRENT_STEP or Brain document changes.

Storage and backup are separate concerns:

```text
PRIMARY_STORAGE_LOCATION != BACKUP_MECHANISM
```

Google Drive is outside this architecture: it is not the storage backend, not the backup, and not a
sync, availability or lock-management dependency. A future backup may use NAS snapshots, a second
NAS or an encrypted external copy without changing the information model.

### 2.3.2 Restricted source material

A raw source that carries credentials or other secrets is classified `SENSITIVE_ARCHIVE` and kept
under `Restricted/` inside the resolved root, never copied into canonical knowledge:

```text
RESTRICTED_SOURCE_AUTOMATIC_CONTEXT_INGESTION=NO
RESTRICTED_SOURCE_SECRET_QUOTING=NO
RESTRICTED_SOURCE_AUTOMATIC_EXTERNAL_SYNC=NO
RESTRICTED_SOURCE_AUTO_UPLOAD=NO
```

Only safe metadata is recorded: path, size, hash and classification. A future Brain may index the
fact that a restricted artifact exists; it must not read secret-bearing content into agent
context.

### 2.4 `Modules/gm-ai-workspace` — application

```text
GM_AI_WORKSPACE_ROLE=APPLICATION_AND_ORCHESTRATOR
GM_AI_WORKSPACE_IS_CANONICAL_MEMORY=NO
```

It reads BoxGhost through its configured root, validates structure, references and hashes, and
presents what it finds. It is software, it is versioned as a module, and it stores no memory of
its own.

### 2.5 `Gystigo` — product and Host

Product code, migrations, tests and the product's own technical documentation, plus the two local
agent entrypoints that a tool technically requires. It is not the owner of GYPPORT memory: it
holds no rules log, no global agent governance and no AI operational history.

## 3. Data flow

```text
resolve(GYPPORT_STORAGE)             raw, original and heavy sources
      |   (read; never canonical)
      v
work: STEPs, AI interventions, verification runs
      |
      +----------------------> Fabric/gm-ai-boxghost    what happened (permanent, raw, reconstructable)
      |                                 |
      +----------------------> Fabric/Knowledge         what became canonical (distilled, Owner-approved)
                                        |
                                        v
                              GYPPORT Brain (future)    recover, search, correlate, interpret,
                                        |               summarize, trace sources, select context
                                        v
                              context pack              derived and regenerable; never replaces its sources
                                        |
                                        v
                              Modules/gm-ai-workspace   application and orchestrator
                                        |
                                        v
                              AIs and human (Owner, agents)
```

## 4. Memory rules

```text
RAW_MEMORY_RETENTION=PERMANENT
RAW_OPERATIONAL_MEMORY_MUST_NOT_BE_REPLACED_BY_SUMMARY=YES
SUMMARIES_ARE_DERIVED=YES
SUMMARIES_MUST_REFERENCE_SOURCE=YES
CONTEXT_PACKS_ARE_DERIVED=YES
CONTEXT_PACKS_ARE_REGENERABLE=YES
PROVIDER_CACHE_IS_NOT_GYPPORT_MEMORY=YES
PROVIDER_COMPACTION_IS_NOT_GYPPORT_MEMORY=YES
AI_TEMP_STORAGE_IS_NOT_DURABLE_GYPPORT_MEMORY=YES
VERIFICATION_BASELINE_REUSE=YES
```

- A summary, a context pack or an index may be regenerated at any time; losing one loses nothing.
  Losing raw memory loses GYPPORT history, so raw memory is kept.
- A summary that cannot name its source is not usable as evidence.
- A provider's conversation memory, its cache and its compaction are the provider's, not GYPPORT's.
  What must survive is written into BoxGhost or Knowledge.
- Verified baselines are reused instead of rerunning accepted verification; the policy is
  `verification-baselines/VERIFIED_BASELINE_REUSE.md`.

## 5. Placement of new artifacts

```text
NEW_DURABLE_GYPPORT_ARTIFACTS_MUST_BE_CREATED_DIRECTLY_IN_THEIR_CANONICAL_OWNER_PATH=YES
PROMOTE_VALUABLE_TEMP_ARTIFACTS_BEFORE_STEP_CLOSE=YES
VALUABLE_TEMP_ONLY_ARTIFACTS_AT_STEP_CLOSE=0
```

The only durable copy of a valuable artifact must never remain in `AppData\Local\Temp`, a Claude
scratchpad, a Codex temporary folder, a provider cache, the Desktop, Downloads, an arbitrary
folder or arbitrary product documentation. Anything worth keeping is promoted to its canonical
owner path before the STEP closes; everything else is disposable by definition.

```text
RAW_SOURCE_TO_GYPPORT_STORAGE
DERIVED_CANONICAL_KNOWLEDGE_TO_FABRIC_KNOWLEDGE
OPERATIONAL_EXECUTION_HISTORY_TO_BOXGHOST
DO_NOT_CREATE_CANONICAL_KNOWLEDGE_IN_TEMP
DO_NOT_CREATE_OPERATIONAL_HISTORY_IN_ARBITRARY_PRODUCT_DOCS
```

## 5.1 CURRENT_STEP — the active work pointer

```text
ONE_GLOBAL_CURRENT_STEP=YES
CURRENT_STEP_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md
```

CURRENT_STEP names the track, the STEP, its mode, its status, the prompt source to read in full and
the verified baselines to reuse. It is a continuity pointer: not canonical knowledge, not a prompt
copy, not a transcript, not a replacement for BoxGhost, not an approval and not an execution
trigger. Execution requires `OWNER_EXECUTION_AUTHORIZED=YES` or a current explicit Owner
instruction. Repository and schema evidence outrank it; a disagreement is reported, never guessed.

For the MVP period there is exactly one global CURRENT_STEP. Per-module variants require an
explicit Owner decision.

## 5.2 Closeout lifecycle

```text
IMPLEMENT
-> VERIFY
-> OWNER REVIEW
-> CONTROLLED COMMIT
-> POST-COMMIT SMOKE
-> GENERATE VERIFIED BASELINE
-> REGISTER VERIFIED BASELINE
-> PREPARE/UPDATE CURRENT_STEP
-> OWNER REVIEW
-> NEXT STEP

AUTO_BASELINE_GENERATION=YES
AUTO_BASELINE_REGISTRATION=YES
AUTO_CURRENT_STEP_PREPARATION=YES

AUTO_OWNER_APPROVAL=NO
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

Automatic means the closing workflow materializes the canonical files, so the Owner never
reconstructs them by hand. It never means automatic execution: a freshly prepared CURRENT_STEP
defaults to `OWNER_EXECUTION_AUTHORIZED=NO`. The materializer lives in `Fabric/tools/continuity/`
and only validates and writes that file.

## 6. Canonical index

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/
├── Reglas.md                        the canonical, append-only rules log (only writable copy)
├── GYPPORT_MEMORY_ARCHITECTURE.md   this document
├── GYPPORT_LOCATIONS.properties     the physical location registry (GYPPORT_STORAGE_ROOT)
├── active-work/CURRENT_STEP.md      the single global pointer to the work that is active now
├── agents/                          AGENTS.md (shared) + CLAUDE.md, CHATGPT.md, CODEX.md
├── ai-collaboration/                the approved AI collaboration execution order and its entry point
├── verification-baselines/          the reuse policy, the automation contract and each baseline
├── steps/                           STEP definitions that are canonical knowledge
└── (Universe baseline, data domain context, MDM memory and the other canonical Universe documents)

Fabric/gm-ai-boxghost/BOXGHOST_STRUCTURE.md   the operational memory structure and ownership
Gystigo/AGENTS.md, Gystigo/CLAUDE.md          technical entrypoints only, no governance text
```

`Reglas.md` is append-only: entries are added at the end, never renumbered, rewritten, reordered or
consolidated, and a superseding rule states explicitly what it replaces.

## 7. Precedence

```text
1. MOST RECENT EXPLICIT OWNER DECISION
2. CURRENT CANONICAL FABRIC DOCUMENT / APPROVED ADR
3. OWNER-ACCEPTED COMMITTED STEP
4. HISTORICAL GOVERNANCE / Reglas history
5. CURRENT VERIFIED SCHEMA / CODE / TESTS
6. NEW PROPOSAL
```

Superseded history may remain as history. It must never act as active authority.

## 8. GYPPORT Brain — contract only

The Owner's definition, recorded in `Reglas.md`:

> GYPPORT Brain es la capa de inteligencia y orquestación de contexto que transforma la memoria
> completa e inmutable de GYPPORT en contextos pequeños, relevantes y verificables para cada IA,
> sin destruir ni sustituir la información original.

```text
GYPPORT_BRAIN_ROLE=INTELLIGENCE_AND_CONTEXT_ORCHESTRATION_LAYER
GYPPORT_BRAIN_IS_STORAGE=NO
GYPPORT_BRAIN_IS_FINAL_AUTHORITY=NO
GYPPORT_BRAIN_AUTONOMOUS_CANONICAL_WRITE=NO
GYPPORT_BRAIN_IMPLEMENTED=NO

CAPABILITIES=RECOVER, SEARCH, CORRELATE, INTERPRET, SUMMARIZE, TRACE_SOURCES, SELECT_CONTEXT, PREPARE_CONTEXT_PACKS

READS=Fabric/Knowledge, Fabric/gm-ai-boxghost, GYPPORT-Storage
AUTHORITY_OF_WHAT_IT_READS:
  Fabric/Knowledge        = canonical truth
  Fabric/gm-ai-boxghost   = evidence and history
  GYPPORT-Storage         = source
```

The Brain never becomes the place where memory lives, never decides what is canonical, and never
writes canonical knowledge on its own: a canonical change is an Owner decision recorded in
`Reglas.md` or in a canonical document. Its outputs are derived: a summary references its source,
and a context pack can be regenerated from Knowledge, BoxGhost and Storage.

This section is the contract. No Brain implementation, vector database, embedding, compression,
summarization pipeline, routing or provider integration is part of it.

## 9. Locations that are not GYPPORT memory

| Location | Status |
|---|---|
| `Governance/GYPPORT_Governance_Architecture` | legacy governance repository; historical, no active authority |
| `Governance/` (loose documents) | historical proposals superseded by current standards |
| `Intelligence/GYPPORT_AI_Knowledge_System` | legacy empty repository; knowledge lives in `Fabric/Knowledge` |
| `UI_Experiments/` | historical clones; their governance copies are snapshots |
| `Gystigo/.claude/worktrees/` | tool-managed checkouts of older commits |
| Fabric branch `docs/gm-ai-workspace-canonical-unification-01` | unmerged 2026-08-07 history, preserved in git |
| `Transfer/` | raw migration archive; contains credentials, kept local until sanitized |
| provider caches and sessions | `~/.claude/projects`, `~/.codex/sessions`: provider cache, not GYPPORT memory |
| Google Drive | not the storage backend, not the backup, not part of this architecture |
| Claude and Codex scratchpads | working files; disposable by definition |

## 10. Arrangements this decision supersedes

| Superseded | Replaced by |
|---|---|
| `Gystigo/Reglas.md` (rules log, later a compatibility pointer) | `Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md` |
| `Gystigo/CHATGPT.md`, `Gystigo/CODEX.md` | `Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/` |
| `Gystigo/AGENTS.md`, `Gystigo/CLAUDE.md` as governance documents | the same paths as technical entrypoints only |
| `Gystigo/docs/ai/**` as the AI operational area | `Fabric/gm-ai-boxghost` |
| `Gystigo/docs/architecture/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md` | `Fabric/Knowledge/00-GYPPORT-UNIVERSE/ai-collaboration/` |
| `Fabric/Governance/` as a second governance location | `Fabric/Knowledge` |
| `Fabric/Knowledge/{Sources,Processing,Corpus}` (2026-08-01 corpus protocol) | raw sources to `GYPPORT-Storage`, processing and registers to BoxGhost |
| `Fabric/.chatgpt/` memory files (2026-08-07, unmerged branch) | `Fabric/Knowledge` and `Fabric/gm-ai-boxghost` |
| `GYPPORT-Storage\Fabric\Knowledge\Standards` as "Master" of the standards | `Gystigo/docs/governance/standards/` |
| The taxonomy where Fabric was candidate knowledge and AIWS/GDA held memory | this document |

## 11. Changing this document

This document changes only by an Owner decision, recorded as a dated entry in `Reglas.md` that
states what it replaces. A document that needs the memory roots references this one instead of
restating them, so the roots are defined in exactly one place.

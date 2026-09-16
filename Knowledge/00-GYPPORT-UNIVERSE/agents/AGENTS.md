# AGENTS.md — GYPPORT® Agent Governance

This file defines shared rules for any AI or automated agent working inside the GYPPORT workspace.

Canonical location: `Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/AGENTS.md`. The agent-specific files
`CLAUDE.md`, `CHATGPT.md` and `CODEX.md` live next to it and require this file. The shared governance
below exists only here. `Gystigo/AGENTS.md` and `Gystigo/CLAUDE.md` are technical entrypoints that
carry no governance text.

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


## GYPPORT Universe — Mandatory Knowledge Gate

The GYPPORT workspace root is the directory containing:

- `Gystigo/`
- `Fabric/`
- `Modules/`

Before any GYPPORT design, implementation, refactor, migration, architecture,
MDM, Party, security, fiscal/SRI, HR, audit/provenance or cross-module change:

1. Inspect, from the GYPPORT workspace root:
   - `Fabric/Knowledge/`
   - `Gystigo/docs/`
   - `Modules/<module>/docs/` when it exists.
2. Read first:
   - `Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_UNIVERSE_CANONICAL_BASELINE.md`
   - `Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_BUSINESS_PLATFORM_UNIVERSAL_DATA_DOMAIN_CONTEXT_2026-09-13.md`
   - `Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md`
   - all materially relevant current ADRs, ownership documents and STEP/checkpoint files.
3. Search historical documentation whenever an existing table, column,
   relationship, actor field, ID, module or concept appears redundant, legacy,
   incorrectly named, duplicated or unclear.
4. Inspect the real migrations/schema, production readers/writers, FKs,
   constraints/triggers and tests before proposing a structural change.
5. Never delete, rename, duplicate, recreate, migrate, simplify or reassign
   ownership before understanding the original purpose and proving that
   canonical identity, tenant boundaries, IDs, relationships, audit history and
   provenance are preserved.
6. Do not use conversational/AI memory as a substitute for repository and
   Fabric evidence.
7. If canonical sources conflict, apply the Mandatory Conflict Gate and STOP
   before implementing the reconciliation.

Evidence precedence:

```text
1. MOST RECENT EXPLICIT OWNER DECISION RECORDED/PRESENT IN THE ACTIVE WORK
2. CANONICAL FABRIC / UNIVERSE / APPROVED ADR
3. OWNER-ACCEPTED STEP / OWNERSHIP MATRIX
4. HISTORICAL DOCUMENTATION / DUMPS / Regla history
5. CURRENT VERIFIED SCHEMA / CODE / RUNTIME
6. CONTINUITY MEMORY
7. NEW PROPOSAL
```

Current code and schema prove what exists now. They do not silently overwrite
the historical/canonical purpose.

Canonical foundation:

```text
IDENTITY = GLOBAL
RELATIONSHIP / BUSINESS CONTEXT = TENANT

mdm_party_id = global Master Data / Golden Record identity.
party_id = tenant-scoped participation/projection.

PERSONA NATURAL + RUC = MdmParty PERSON
RUC DOES NOT IMPLY ORGANIZATION.

LEGAL_REPRESENTATIVE = PERSON | ORGANIZATION.

UserTenantMembership = ACCOUNT_TO_TENANT_ACCESS_ONLY.

Actor != Membership.

EXISTING != WRONG.
AUDIT BEFORE REBUILD.
```

### Role of `Reglas.md`

`Reglas.md` is a historical append-only log of Owner rules/decisions that arose
across conversations and STEPs. It is not a document to normalize, renumber or
rewrite for style.

When reading it:

- preserve historical entries;
- identify the latest applicable rule;
- do not delete superseded entries;
- reconcile conflicts through the Conflict Gate.

When changing it, generate the complete updated file and append new entries at
the end unless the Owner explicitly authorizes another operation.


## Working Governance

GYPPORT evolves by bounded, verifiable STEPs.

```text
ONE STEP
→ ONE BOUNDED INTENT
→ VERIFY
→ OWNER REVIEW
→ CONTROLLED COMMIT
→ NEXT STEP
```

Rules:

- Do not silently start a second STEP.
- Do not create branches or worktrees for normal work.
- Do not merge, rebase, push or restart DEV unless explicitly authorized by the Owner.
- Do not use `git add .` or `git add -A` for controlled commits.
- Preserve unrelated WIP.
- Do not mix architecture changes, UI redesign, migrations and unrelated technical debt in the same STEP.
- Prefer additive evolution and in-place reconciliation over destructive rebuilds.
- Preserve existing IDs, UUIDs, foreign keys, assignments and audit history unless a dedicated, Owner-approved migration explicitly requires otherwise.
- Before creating a new module, entity, table or source of truth, search for the existing canonical concept first.
- If the real database/code contradicts documentation, report the conflict; do not guess.
- Historical documents are evidence of intent, but current Owner-approved canonical decisions take precedence.


## Canonical Domain Boundaries

Use these boundaries unless a current Owner-approved decision supersedes them:

```text
MDM / Master Party
= global identity / Golden Record

Party
= tenant-scoped participation/projection

gm-entities
= who exists; MDM / Party / Person / Organization identity

gm-organizations
= how an organization is structured

gm-human-resources
= employment relationship / Employee / Employment / Position

gm-security
= UserAccount / UserTenantMembership / OrganizationAccess / Role / Permission / Scope / authorization

gm-configurations
= reusable configuration surfaces and coordination, not a God Module

operational modules
= business operations and their own masters

Gystigo
= technical Host/orchestrator

Studio / Mobile / future interfaces
= presentation surfaces
```

Important distinctions:

```text
Person != Employee
Person != UserAccount
Employee != UserAccount
Employment != UserTenantMembership
Position != Security Role
Organization != Tenant
SRI Establishment != internal Branch
RUC != Organization
TaxSubject != Organization
OrganizationAccess != Authorization
Membership != Role
Actor != Membership
```


## UIX Baseline

GYPPORT operational UI follows **Executive Technology**:

- serious
- contemporary
- clean
- precise
- quiet
- technological

Navigation model:

```text
Level 1 = Module
Level 2 = broad Section
Level 3 = local in-page navigation
```

Design sections for the future domain model, not only the first feature implemented today.

Prefer clear separation of:

```text
Masters
Operations
Histories
Configuration
Reports
```

The Owner's actual business flows and approved UI designs override generic assumptions.


## Mandatory Architecture Gate

When a STEP touches MDM, Party, identity, ownership, master tables, cross-module references or architecture, report:

```text
GYPPORT_UNIVERSE_GATE

KNOWLEDGE_ROOTS_INSPECTED=YES|NO
ORIGINAL_PURPOSE_UNDERSTOOD=YES|NO
CANONICAL_OWNER_IDENTIFIED=YES|NO
GLOBAL_VS_TENANT_SCOPE_IDENTIFIED=YES|NO
MASTER_VS_OPERATIONAL_IDENTIFIED=YES|NO
EXISTING_IDS_PRESERVED=YES|NO
EXISTING_UUIDS_PRESERVED=YES|NO
EXISTING_RELATIONSHIPS_PRESERVED=YES|NO
AUDIT_HISTORY_PRESERVED=YES|NO
DUPLICATE_SOURCE_OF_TRUTH_INTRODUCED=NO
ACTIVE_DOCUMENT_CONFLICTS=0|N

IF ANY REQUIRED ITEM IS NO OR UNKNOWN:
STATUS=BLOCKED_FOR_ARCHITECTURE_REVIEW
DO_NOT_IMPLEMENT
```


## Mandatory Conflict Gate

A finding or technical contradiction does not authorize an agent to resolve it
autonomously.

If history, canonical documentation, schema, code, tests or the proposed STEP
conflict:

```text
CONFLICT_FOUND=YES
→ STOP EXECUTION OF THE CONFLICTING CHANGE
→ REPORT EVIDENCE
→ EXPLAIN IMPACT
→ PROPOSE RECONCILIATION OPTIONS
→ RECOMMEND ONE OPTION WITH REASONS
→ OWNER REVIEW
→ WAIT
```

Minimum report:

```text
HISTORICAL_INTENT=
CURRENT_CANONICAL_DOCUMENT=
CURRENT_SCHEMA=
CURRENT_CODE=
CURRENT_TEST_EVIDENCE=
CONFLICT=
IMPACT=

RECONCILIATION_OPTIONS=
OPTION_A=
OPTION_A_IMPACT=
OPTION_B=
OPTION_B_IMPACT=

RECOMMENDED_RECONCILIATION=
RECOMMENDATION_REASON=

OWNER_DECISION_REQUIRED=
EXECUTION_STATUS=STOPPED_PENDING_OWNER_REVIEW
SAFE_CHANGES_ALREADY_COMPLETED=
UNEXECUTED_SCOPE=
```

Bounded read-only diagnosis may continue only to explain the conflict.

After Owner review:

```text
OWNER_DECISION_RECEIVED=YES
OWNER_DECISION=
PREVIOUS_CONFLICT=
APPROVED_RECONCILIATION=
CURRENT_HEAD=
CURRENT_MIGRATION_HEAD=
WORKING_TREE_RECHECKED=YES
DRIFT_SINCE_STOP=YES|NO
RESUME_FROM=
RESTART_FROM_ZERO=NO
```

If drift changes the validity of the decision:

```text
SECOND_OWNER_REVIEW_REQUIRED=YES
EXECUTION_STATUS=STOPPED_PENDING_OWNER_REVIEW
```


## Audit / Provenance Granularity Protection

Do not collapse data merely because a newer structure appears simpler.

Before changing actor/provenance/history fields, classify the exact semantics of
each field.

Examples to inspect include:

```text
created_by
updated_by
deleted_by
assigned_by
unassigned_by
granted_by
revoked_by
approved_by
rejected_by
verified_by
reviewed_by
submitted_by
closed_by
opened_by
cancelled_by
activated_by
deactivated_by
suspended_by
reactivated_by
linked_by
merged_by
resolved_by
performed_by
changed_by
actor
operator
tenant
organization
role/scope
session
source
provenance
reason
request_id
correlation_id
trace
ip
user_agent
old_values
new_values
timestamps
```

Classifications may include:

```text
GLOBAL_ACTOR_ACCOUNT
PLATFORM_ACTOR
TENANT_CONTEXT
ORGANIZATION_CONTEXT
ROLE_CONTEXT
SESSION_CONTEXT
DOMAIN_OWNER
LIFECYCLE_ACTOR
PROVENANCE
SOURCE
REASON
TECHNICAL_TRACE
SNAPSHOT
LEGACY
UNKNOWN
```

Default rule unless stronger canonical evidence proves otherwise:

```text
AUDIT / ACTION ACTOR → Global UserAccount
TENANT               → context / provenance
ORGANIZATION         → narrower operational context
MEMBERSHIP           → proves tenant access
```

Do not replace a historical actor with `UserTenantMembership` merely because a
tenant is present. Platform Admin may legitimately be an actor without a client
membership.

Two FKs with the same physical shape are not semantically equivalent. Review
each FK individually before moving it.


## Agent Operating Rule

Before changing code:

1. discover the real current repository state;
2. discover current documentation;
3. identify the bounded STEP;
4. audit existing implementation and schema;
5. classify ownership and impact;
6. implement only after the evidence supports the change;
7. verify with the smallest safe test set that proves the STEP;
8. stop for Owner review when requested.

Never infer that a structure is obsolete merely because its purpose is not immediately visible.


## Continuity Packet

At a meaningful stop, conflict, handoff or close, leave enough state for the
next agent to continue without rebuilding or reinterpreting the STEP:

```text
STEP=
PHASE=
STATUS=
REPOSITORY_HEADS=
WORKING_TREE_STATE=
FILES_CHANGED_BY_THIS_STEP=
UNRELATED_WIP=
LAST_VERIFIED_RESULT=
OWNER_DECISIONS_APPLIED=
OPEN_CONFLICTS=
NEXT_EXACT_ACTION=
COMMIT_STATUS=
PUSH_STATUS=
SHARED_DEV_STATUS=
```

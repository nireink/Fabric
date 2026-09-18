# GYPPORT_FABRIC_UNTRACKED_KNOWLEDGE_RECONCILIATION_29D — record (2026-09-18)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GYPPORT_FABRIC_UNTRACKED_KNOWLEDGE_RECONCILIATION_29D
MODE=VERIFY -> COMPARE -> CANONICALIZE -> ARCHIVE -> COMMIT -> PUSH
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GYPPORT_FABRIC_UNTRACKED_KNOWLEDGE_RECONCILIATION_29D.md
STATUS=RECONCILED (committed with this record, then pushed as a normal fast-forward)
SOURCE_CODE_CHANGED=NO   RUNTIME_CHANGED=NO   SHARED_DEV_MODIFIED=NO   OTHER_REPOSITORIES_MODIFIED=NO
```

Raw evidence in this folder: `prestate-manifest.tsv` (the 31 files: size, SHA-256, modification time),
`relocation-results.tsv` (the 18 relocations and their validation) and `post-state-checks.txt`.

## 1. Pre-state (§2) and the classification it rests on

```text
FABRIC main = origin/main = 59f72904c7fd3b2f5aed17fcff0c6ba264a21c4a (ls-remote)
TRACKED_MODIFIED=0 TRACKED_DELETED=0 STAGED=0 UNTRACKED=31 UNKNOWN=0
UNTRACKED_SET_EQUALS_STEP_29C=YES (31 of 31 paths)
```

GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C, a read-only audit left unrecorded by its own instruction, established
that VS Code's 36 changes were Fabric 31 + Gystigo 5, and that the "10" of earlier reports and the 31 are the same
files: `git status --short` folds a wholly untracked folder into one entry (8 folders + 2 files = 10), VS Code lists
each file. All 31 were created 2026-08-13 to 2026-09-10 and none had ever been committed. This STEP acts on that
classification.

## 2. Group A — Owner-approved documents, committed with their bytes unchanged (§3 - §6)

### AI governance, documents 1 - 3

```text
GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES.md          STILL_VALID_SUPPORTING_KNOWLEDGE   committed
GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE.md   STILL_VALID_SUPPORTING_KNOWLEDGE   committed
GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY.md    STILL_VALID_SUPPORTING_KNOWLEDGE   committed
CONFLICTS_WITH_NEWER_OWNER_RULES=0
```

Each is OWNER_APPROVED_BASELINE (2026-09-08) and was required reading in the Owner's prompts of 2026-09-08 to 09-10.
Compared with the committed `agents/AGENTS.md`, `CLAUDE.md`, `CHATGPT.md`, `CODEX.md`, `ai-collaboration/`,
`Reglas.md` and later rules, nothing contradicts them: the stop gates restate and detail AGENTS.md's Conflict Gate,
its no-push and WIP-preservation rules and the data-domain context's `DO_NOT_PICK_OPTION_AUTONOMOUSLY=YES`; no later
rule changes their subagent, test, context or follow-up limits. They are supporting knowledge rather than the primary
authority because AGENTS.md is the mandatory governance and does not reference them yet - the documents themselves say
AGENTS.md, CLAUDE.md and CHATGPT.md "should reference" them. That wiring is an edit to canonical governance and is left
to the Owner.

### Data access ADR, document 4

```text
ADR01_CLASSIFICATION=B - still active canonical architecture
HANDLING=committed unchanged at Knowledge/Derived/owner-approved/GYPPORT-DATA-ACCESS-ARCHITECTURE-01.md; no banner
```

ADR-01 (Rev 4, OWNER_APPROVED_CANONICAL, OD_DA_01 and OD_DA_02 approved 2026-08-21) sets the application's data-access
rules, DA-RULE-001 to 017: hexagonal ports and adapters, per-aggregate repositories, query ports, tenant id on every
tenant-scoped port, use-case-owned transactions, Host-owned DataSource and TransactionManager, exception translation.
ADR-0014 (module-to-core FKs), ADR-0015 (RUC and tax homes), ADR-0016 (collation), ADR-0017 (tax subject) and
ADR-0018 (global account and membership) decide other questions; none mentions data access, repositories or ADR-01, so
none supersedes it. It is live: the committed `gm-entities/START_HERE.md` lists this exact path as required reading
and the gm-organizations design proposal cites it; the frozen gm-expenses code has its shape. Its path is kept so
those references hold.

### Security and UIX, documents 5 - 7

Current bytes against the pre-edit copies archived by the canonical-memory migration (OP154 - OP156); the full diff is
in `post-state-checks.txt`:

```text
DOCUMENT                                          ADDED  REMOVED  CHANGED
UIX/GYPPORT_MODULE_NAVIGATION_HIERARCHY.md          0      0      3 lines: Empleados gm-workforce -> gm-human-resources;
                                                                  Roles and Permisos Gystigo Security -> gm-security
UIX/GYPPORT_UIX_IMPLEMENTATION_AND_COMPLIANCE_GUIDE 0      0      the same 3 lines
Security/GYPPORT_ORGANIZATION_CONTROL_FOUNDATION.md 0      0      1 line: WORKFORCE -> HUMAN_RESOURCES
EDIT_CLASSIFICATION=OWNER_APPROVED_LATER_DECISION (all 7 changed lines)
UNSUPPORTED_CHANGES=0   RESTORATIONS_NEEDED=0
```

The edits only carry two Owner-accepted decisions of 2026-09-10 into the documents: Workforce canonicalized as Human
Resources (Gystigo ad9c78d, gm-human-resources 08f10c7) and the access domain extracted into gm-security (Gystigo
c37c17f, gm-security 97a5632). The committed `agents/AGENTS.md` (Canonical Domain Boundaries) and the Universe baseline
already name gm-human-resources and gm-security. No old name remains in the three files. All three committed as they
are.

## 3. Groups B, C, D — relocated out of canonical knowledge (§7 - §9, §13)

```text
STEP02_AUDIT_FILES -> gm-ai-boxghost/imports/GYPPORT-FABRIC-UNTRACKED-KNOWLEDGE-RECONCILIATION-29D/fabric/Knowledge/Derived/proposed/  (3)
                      index: gm-ai-boxghost/imports/GYPPORT-FABRIC-UNTRACKED-KNOWLEDGE-RECONCILIATION-29D/IMPORT_INDEX.md
SUPERSEDED_PROPOSED_ADR -> GYPPORT_STORAGE/Fabric/Knowledge/Derived/proposed/GYPPORT-DATA-ACCESS-ARCHITECTURE-01.md  (1)
REFERENCE_TEMPLATES     -> GYPPORT_STORAGE/Fabric/Knowledge/Derived/proposed/reference-templates/gm-entities-data-access/  (14)
STORAGE_MANIFEST=GYPPORT_STORAGE/Fabric/Knowledge/Derived/ARCHIVE_MANIFEST_29D.md
ITEMS=18   ARCHIVE_HASH_MISMATCHES=0   BYTES_PRESERVED=YES   MODIFICATION_TIMES_PRESERVED=YES
SOURCES_REMOVED_FROM_FABRIC=18, only after every destination was validated (exists, size, SHA-256) and validated again
```

The three STEP 02 audit files declare no track, so they sit under `imports/` with their original relative path, as
BOXGHOST_STRUCTURE.md section 4 requires, and the index ties them to ADR-01, which cites STEP 02 as its evidence base.
One of them states that Gystigo is a Node.js/TypeScript project; the index records that this is history - the Host
is Java/Spring - and the file keeps its words. The proposed ADR is superseded by document 4 and is not committed. The
reference templates were generated against that proposal; the Owner-approved ADR lists templates as a phase it does
not authorize, and the real gm-entities data access has existed since PKG-2C/2D.

GYPPORT_STORAGE was resolved through `GYPPORT_LOCATIONS.properties`. The template subtree left empty in Fabric was
pruned; `Knowledge/Derived/proposed/` stays, empty and invisible to git, beside its empty siblings `archive/`,
`conceptually-reviewed/` and `superseded/` of the 2026-07-30 lifecycle scaffold.

## 4. Group F — gm-expenses initial-development documents (§11, §12)

Against the frozen baseline, the three documents are accurate for their date and superseded in places:

```text
03-application   its package tree has no casefile (ExpenseCase, the centre of the frozen MVP); its "exhaustive"
                 command list is settlement-level and includes CorrectRejected, while the frozen MVP runs Return,
                 Reimbursement and Conciliar on the Expediente and RECHAZADO is final (CorrectRejected removed, 545eae0)
04-integration   no auth/tenant context contract, gm-fleet bootstrap-only, and "no cross-module physical database
                 foreign keys" - superseded by the authoritative sessions and ADR-0018, by gm-fleets, and by ADR-0014
05-implementation "No database foreign keys across modules" (ADR-0014 again) and "the five documents in this folder"
                 as the source of truth (now the frozen baseline)
CONSISTENT_STILL idempotency by operationId, optimistic locking, reconciliation invalidation, append-only history,
                 domain purity, Host-owned DataSource and TransactionManager
```

```text
HISTORICAL_BANNER_ADDED=YES (the Owner's text, as a text block under each title)
BODIES_CHANGED=NO (removing the banner restores each file's pre-state SHA-256)
README_ACTION=REWRITTEN_INDEX
```

The README is now "gm-expenses — Knowledge Index": the status block states FROZEN_OWNER_ACCEPTED_PUSHED and the current
authority, and the index separates the current authority (frozen baseline, the maintained domain and persistence
baselines, Reglas), the historical design documents and the operational evidence, with the module's locations. The
original Purpose and Provenance bodies are carried over byte-for-byte under headings that mark them as the WP_00
publication. The pre-rewrite README (never committed; its status table records 2026-08-28) was rebuilt byte-exact -
its SHA-256 equals the pre-state manifest - and archived as `GYPPORT_STORAGE/Fabric/Knowledge/gm-expenses/
README_BACKUP_20260828.md`.

## 5. Group E — Owner WIP (§10)

```text
Knowledge/Architecture/GYPPORT_REGLAS_CANONICAS_ARQUITECTURA_DOMINIO_UIX.md                          untracked, byte-identical
Knowledge/gm-accounting/01-conceptual-model/GYPPORT_GM_ACCOUNTING_GENERAL_MODULE_MODEL_EXECUTION_PROMPT_v1.2.md  untracked, byte-identical
```

## 6. What this commit carries

```text
Knowledge/AI/ (3)   Knowledge/Derived/owner-approved/ (1)   Knowledge/Security/ (1)   Knowledge/UIX/ (2)
Knowledge/gm-expenses/03-application, 04-integration, 05-implementation (banner) and README.md (index)
gm-ai-boxghost/imports/GYPPORT-FABRIC-UNTRACKED-KNOWLEDGE-RECONCILIATION-29D/ (3 audit files and the index)
the stored prompt, this folder, and the existing CURRENT_STEP.md
NOT_STAGED=the two Owner WIP files
```

No file needed line-ending normalization (0 CR bytes, no BOM): every staged blob equals its working-tree bytes.
`git diff --cached --check` flags trailing whitespace only inside files kept byte-exact on purpose - the header of the
Owner-approved UIX compliance guide (Markdown line breaks) and the three imported STEP 02 files, one of which also ends
with a blank line. The files written by this STEP are clean.

## 7. Not done

```text
AGENTS_MD_REFERENCES_TO_THE_AI_POLICIES=NOT_ADDED (canonical governance edit; Owner decision)
STEP29_AND_STEP29C_PROMPTS=NOT_STORED (29 forbade documentation edits, 29C was read-only; the 29B record and this one
                           summarize them)
OTHER_REPOSITORIES=UNTOUCHED (Engineering, its engineering template, gm-e-documents, gm-sales, gm-service-management,
                   gm-operational-resources, UI_Experiments/E-commerce-develop - separate audits)
FOLLOW_UPS=GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30, GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31,
           SPRING_GENERATED_PASSWORD_STARTUP_LOG (pre-production debt)
```

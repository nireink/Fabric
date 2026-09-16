# Validation results — canonical memory migration

```text
TRACK=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01
DATE=2026-09-15
SCOPE=FILESYSTEM_AND_DOCUMENTATION_ONLY
APPLICATION_TESTS_RERUN=NO
DATABASE_WRITES=NONE
SHARED_DEV_TOUCHED=NO
```

## 1. Required results

```text
CANONICAL_PATH_REFERENCES_VALID=YES
BROKEN_REFERENCES=0
CANONICAL_REGLAS_COUNT=1
DUPLICATE_WRITABLE_REGLAS=0
SECOND_ACTIVE_GOVERNANCE_ROOT=0
SECOND_ACTIVE_MEMORY_ROOT=0
DUPLICATE_GLOBAL_AGENT_GOVERNANCE=0
TRANSITIONAL_COMPATIBILITY_FILES=0
DEFERRED_PATH_CLEANUP=0
UNCLASSIFIED_RELEVANT_FILES=0
HISTORICAL_CONTENT_LOSS=0
MIGRATED_UNIQUE_CONTENT_LOSS=0
PKG2C_FILES_UNCHANGED=52/52
GM_EXPENSES_WIP_PRESERVED=74/74
OTHER_OWNER_WIP_PRESERVED=YES
FILES_STAGED=0
```

## 2. How each one was verified

| Check | Method | Result |
|---|---|---|
| References | every markdown link and backticked path in the 23 documents this STEP created or modified was resolved against the filesystem | 33 unresolved strings, all classified: 13 prose (`AppData\Local\Temp`, `~/.claude/projects`, folder-type names, a git branch name) and 20 deliberate historical mentions ("hasta 2026-09-15", "Origen:", supersession tables). `BROKEN_REFERENCES=0`; no reference was left pointing at a moved artifact |
| Rules log | every `Reglas.md` in the workspace and in GYPPORT-Storage | 1 active (`Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md`), 15 historical copies in worktrees, UI experiments, storage backups and the recovery bundle |
| Agent governance | every `AGENTS/CLAUDE/CHATGPT/CODEX.md` in active areas | canonical set of 4 in Fabric; 2 Gystigo entrypoints containing no governance section (checked for the Knowledge Gate, Working Governance, Domain Boundaries, Conflict Gate, Continuity Packet and evidence precedence headings) |
| Transitional files | first heading of every markdown file in the workspace and in storage | no `# MOVED` pointer anywhere |
| Retired locations | existence check | `Gystigo/docs/ai`, `Gystigo/docs/guide`, `Fabric/Governance`, `Gystigo/Reglas.md`, `Gystigo/CHATGPT.md`, `Gystigo/CODEX.md` and the GYPPORT-Storage standards "Master" copy are gone; `steps/PKG-2D/PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md` present with no `.md.md` duplicate |
| Byte preservation | every moved file re-hashed at its target and compared with the source hash recorded before the move | 235 of 238 byte-identical; the 3 exceptions are the documents whose action is `MOVE_WITH_MINIMAL_REFERENCE_UPDATE` (both collaboration documents and the retention policy), moved byte-exact and then edited only in their location/reference lines |
| Content loss | every non-empty line of the four pre-migration Gystigo agent files was searched in the canonical set; the removed MDM backup was proved to be a line-level subset of the current document; duplicates were proved byte-identical to a git-tracked twin before removal | 0 |
| PKG-2C | the 52 accepted PKG-2C paths re-hashed and compared with the commit-gate record `s15k_pkg2c_end.txt` | 52/52 unchanged, 0 changed, 0 missing |
| Unrelated WIP | working-tree fingerprint before and after (`cm02_fingerprint_premigration.txt` vs `cm31_fingerprint_after.txt`), per category | GM_EXPENSES_WIP 74/74 unchanged; PKG2B 0; OWNER_WIP 42 unchanged plus the 4 agent/rules files this STEP replaced or removed and 11 entries that moved to their canonical path; OTHER_UNRELATED_WIP 18 unchanged plus the 3 Fabric documents this STEP edited |
| Secrets | BoxGhost sensitivity categories (API key prefixes, cloud credentials, PEM private keys, JWTs, connection strings with password) over everything written into BoxGhost and GYPPORT-Storage | 232 files scanned, 0 findings |
| Staging | `git diff --cached` in Gystigo, Fabric, the legacy governance repository, Engineering and three modules | 0 staged files in every repository |

## 3. Known, deliberate exceptions

```text
EMPTY_DIRECTORIES_KEPT=5
```

Five directories that the migration emptied could not be removed: the Google Drive sync client
holds a handle on them (`WinError 5` on `rmdir`). They contain no files:
`GYPPORT-Storage/IAs Agents/gm-ai-workspace`, `GYPPORT-Storage/Fabric/Knowledge/Standards`,
`GYPPORT-Storage/IAs Agents/Claude/GYPPORT Corpus`, and `Claude/` and `Codex/` inside
`GYPPORT-Storage/IAs Agents/GYPPORT Lineamientos Desarrollo ERP`. They can be deleted by hand once
the sync client releases them; nothing depends on them.

## 4. Pre-existing facts recorded, not caused by this STEP

- `Gystigo/README.md` was already deleted in the working tree before the migration: the
  pre-migration fingerprint records `ENTRY|Gystigo|OWNER_WIP| D|README.md|NOT_A_FILE`.
- `Gystigo/docs/architecture/REPOSITORY_ADOPTION_PLAN.md` and the renumbering note in `ADR-0005`
  contain `gypport/...` paths that stopped resolving when the repository was restructured in July
  2026. They are historical statements and were left as they are.
- The BoxGhost sensitivity policy on `main` references sibling documents that live only on the
  unmerged Fabric branch `docs/gm-ai-workspace-canonical-unification-01` (d43b4fd).


## 5. Completion intervention (2026-09-15, final)

Everything below was verified after the migration, on the same worktree, with no application test
and no database access.

```text
CONTINUITY_GATE=PASS (HEADs, canonical roots and their hashes matched the verified migrated state)

AGENT_AUTO_DISCOVERY_ENABLED=YES
CURRENT_STEP_RESOLUTION_TEST=PASS
PROMPT_SOURCE_RESOLUTION_TEST=PASS
REQUIRED_BASELINE_RESOLUTION_TEST=PASS
VERIFIED_BASELINE_POLICY_RESOLUTION_TEST=PASS
GYPPORT_LOCATION_REGISTRY_RESOLUTION_TEST=PASS
GYPPORT_STORAGE_AVAILABLE=YES
STORAGE_LOCATION_SINGLE_SOURCE=YES
ENTRYPOINT_REFERENCES_RESOLVE=PASS (5 of 5)
CLAUDE_ENTRYPOINT_IMPORTS_CANONICAL=PASS
CANONICAL_CLAUDE_IMPORTS_AGENTS=PASS

HARDCODED_STORAGE_PATHS_IN_ACTIVE_AGENT_GOVERNANCE=0
OBSOLETE_ACTIVE_ARCHITECTURE_REFERENCES=0
BROKEN_REFERENCES=0

GOOGLE_DRIVE_LOCK_RESIDUE=0
RESIDUAL_FILES_IN_OLD_DRIVE_DIRECTORIES=0

UNMERGED_UNIQUE_BOXGHOST_MEMORY=0
BOXGHOST_OPERATIONAL_HISTORY_COMPLETE=YES

GYPPORT_STORAGE_SOURCE_MIGRATION_COMPLETE=YES
RAW_SOURCE_FILES_LOST=0
PERMANENT_DUPLICATE_SOURCE_TREES=0

PKG2C_FILES_UNCHANGED=52/52
GM_EXPENSES_WIP_PRESERVED=92/92
APPLICATION_TESTS_RERUN=NO
FILES_STAGED=0
```

### How each completion check was verified

| Check | Method | Result |
|---|---|---|
| Discovery chain | resolved every hop from the two Gystigo entrypoints: canonical agent governance, CURRENT_STEP, Reglas, PROMPT_SOURCE, REQUIRED_BASELINES, the reuse policy and the location registry | 11 of 11 PASS |
| Location indirection | the registry holds exactly one `GYPPORT_STORAGE_ROOT`; the resolved root exists; no active agent governance file contains a literal storage path | PASS |
| Drive residue | the five emptied directories carried the ReadOnly attribute set by the sync client; the attribute was cleared and they were removed. The hidden staging folder held 83 blobs: 78 distinct, every one byte-identical to a file already in the library (the last one a git packfile), so it was backed up and removed | 0 remaining |
| Branch recovery | read-only `git ls-tree` / `git show` against d43b4fd, restricted to `gm-ai-boxghost/**`; 78 unique files written byte-exact and re-hashed, 1 already identical, 0 conflicting. No merge, no cherry-pick, no branch switch, no deletion | 78 recovered, 2,496,556 bytes |
| Storage migration | pre-move manifest (path, size, mtime for 25,774 files; sha256 for 92 archives, dumps and files over 100 MB), same-volume renames, then every file re-verified against that manifest | VERIFIED_FILES=25,774 PROBLEMS=0 |
| Sensitive archive | classified from entry names only, never read or printed; moved to the restricted area of the library | SENSITIVE_ARCHIVE recorded with size and hash |
| Tooling | both PowerShell scripts tokenize under 5.1; the materializer refuses a wrong mode, a missing prompt source, an unregistered baseline and a wrong output name, and defaults to OWNER_EXECUTION_AUTHORIZED=NO; the generator ran against a disposable Fabric tree | PASS; the canonical CURRENT_STEP and Reglas were not touched by the tests |
| WIP preservation | fingerprint before and after this intervention, per category | 100 files added (all under Fabric), 11 content changes (all intended), 0 removed, 0 added outside Fabric |

# Agent file discovery evidence

```text
TRACK=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01
DATE=2026-09-15
QUESTION=which agent file must remain physically inside the Gystigo repository, and why
METHOD=tool documentation + local configuration + workspace-wide consumer search (read-only)
```

## 1. Per file

| FILE | LOCAL_DISCOVERY_REQUIRED | EVIDENCE | FINAL_ROLE |
|---|---|---|---|
| `Gystigo/AGENTS.md` | YES | (a) Codex reads `AGENTS.override.md` and `AGENTS.md` from the project root down to the working directory and reads no other filename unless `project_doc_fallback_filenames` is configured — it is not configured in `~/.codex/config.toml`; (b) the Gystigo Toolchain requires the file as its project-root marker: `developer_platform/toolchain/tool/core/path/ToolProjectRootResolver.mjs` lines 131-136 return a directory only when `AGENTS.md` exists next to `developer_platform/` and `platform_os/`, and it is used by `tool/core/index.mjs` and by three migration contract runners | PERMANENT_TECHNICAL_ENTRYPOINT (pointer + local technical notes, no governance text) |
| `Gystigo/CLAUDE.md` | YES | Claude Code loads `CLAUDE.md` (never `AGENTS.md`) from the working directory, its ancestors and, on demand, from subdirectories; it supports `@path` imports that resolve relative to the importing file, recursively up to four hops. Observed in this session: working inside `Gystigo/` loaded `Gystigo/CLAUDE.md` into the context automatically | PERMANENT_TECHNICAL_ENTRYPOINT (imports the canonical Fabric files) |
| `Gystigo/CHATGPT.md` | NO | No tool discovers it: ChatGPT has no filesystem access, and the workspace-wide search found no code or configuration consumer. The Owner supplies the file to a ChatGPT project manually | REMOVED — canonical content in `Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/CHATGPT.md`; pre-migration bytes archived as `GYPPORT-Storage/Gystigo/CHATGPT_Backup_20260915.md` |
| `Gystigo/CODEX.md` | NO | Codex reads only `AGENTS.md` / `AGENTS.override.md` plus configured fallback filenames; no fallback is configured, and the workspace-wide search found no consumer | REMOVED — canonical content in `Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/CODEX.md`; pre-migration bytes archived as `GYPPORT-Storage/Gystigo/CODEX_Backup_20260915.md` |
| `Gystigo/Reglas.md` | NO | The baseline generator defaults to, and only accepts, the canonical log, and refuses a file whose first heading is `# MOVED`. The only other mention in the workspace was an inert permission string in `Gystigo/.claude/settings.local.json` | REMOVED — the canonical log is `Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md` |

## 2. Sources

```text
CLAUDE_CODE_MEMORY_DOC=https://code.claude.com/docs/en/memory
CODEX_AGENTS_DOC=https://learn.chatgpt.com/docs/agent-configuration/agents-md
CODEX_LOCAL_CONFIG=~/.codex/config.toml (no project_doc_fallback_filenames; ~/.codex/AGENTS.md exists and is empty)
TOOLCHAIN_CONSUMER=Gystigo/developer_platform/toolchain/tool/core/path/ToolProjectRootResolver.mjs:131-136
TOOLCHAIN_CALLERS=tool/core/index.mjs, tool/framework/migration/contract/{MigrationContractRunner,MigrationDryRunOperationListContract,MigrationCompositeTransactionIntegrityContract}.mjs
WORKSPACE_SEARCH=cm04_refsearch_full.txt (this folder)
```

## 3. Consequence

Both entrypoints carry only a pointer, the memory roots and their local technical reason. The
validation confirms they contain no copied governance section, so global agent governance exists in
exactly one place: `Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/`.

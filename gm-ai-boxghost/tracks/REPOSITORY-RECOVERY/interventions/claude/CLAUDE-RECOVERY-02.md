# CLAUDE-RECOVERY-02

## GYPPORT® REPOSITORY RECOVERY

**Track:** Repository Recovery  
**Step:** RECOVERY-02 — Final Working Tree Classification and Commit Plan  
**Mode:** Read-Only Audit  
**Agent:** Claude  
**Status:** Ready for Execution  

---

# 1. PURPOSE

Classify every remaining uncommitted and untracked file into a clean, logical commit plan.

Do not modify files.

Do not stage.

Do not commit.

Do not push.

The audit must separate the remaining work into independent groups such as:

```text
Kernel Recovery
Core Runtime Recovery
Dashboard Validator
Contract Harness
Dashboard Contracts
Registry Contracts
AI Recovery Instructions
Investigations
Reglas.md
```

Do not merge unrelated concerns into one commit.

---

# 2. REQUIRED INITIAL COMMANDS

Run:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
git --no-pager diff --stat
git diff --cached --stat
```

Expected repository root:

```text
D:/NZXTG7/GYPPORT/GYPPORT Fabric/Gystigo
```

Expected branch:

```text
master
```

If root or branch differs, stop.

---

# 3. CURRENT FILES TO CLASSIFY

At minimum inspect:

```text
gypport/Reglas.md

gypport/platform_os/studio/channel/browser/shell/package.json
gypport/platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
gypport/platform_os/studio/channel/browser/shell/vite.alias.js
gypport/platform_os/studio/channel/browser/shell/vitest.config.js

gypport/platform_os/studio/engine/core/runtime/bootstrap/PlatformBootstrap.js
gypport/platform_os/studio/engine/core/runtime/environment/RuntimeState.js
gypport/platform_os/studio/engine/core/runtime/service/PlatformAuthorization.js
gypport/platform_os/studio/engine/core/runtime/service/PlatformNavigation.js
gypport/platform_os/studio/engine/core/runtime/service/PlatformNotifications.js

gypport/platform_os/studio/engine/core/ui/dashboard/DashboardValidator.js

gypport/platform_os/studio/engine/kernel/Kernel.js
gypport/platform_os/studio/engine/kernel/diagnostics/KernelDiagnostics.js
gypport/platform_os/studio/engine/kernel/diagnostics/KernelHealth.js
gypport/platform_os/studio/engine/kernel/lifecycle/KernelLifecycle.js

gypport/platform_os/studio/contracts/dashboard/**
gypport/platform_os/studio/contracts/registry/**

gypport/docs/ai/claude/CLAUDE-ROLLBACK-01.md
gypport/docs/ai/codex/CODEX-DOCS-01.md
gypport/docs/ai/codex/CODEX-ROLLBACK-01.md

gypport/docs/investigations/DASHBOARD_ENGINE_STABILIZATION_STEP_2B_3C1_AUDIT_TRAIL.md
gypport/docs/investigations/Especificacion de desarrollo de DASHBOARD.md
gypport/docs/investigations/Organizacion de repositorio.md
```

---

# 4. CLASSIFICATION CATEGORIES

Classify each path into exactly one:

```text
COMMIT — KERNEL RECOVERY
COMMIT — CORE RUNTIME RECOVERY
COMMIT — STUDIO BOOTSTRAP RECOVERY
COMMIT — CONTRACT HARNESS
COMMIT — DASHBOARD CONTRACTS
COMMIT — REGISTRY CONTRACTS
COMMIT — DASHBOARD VALIDATOR
COMMIT — GOVERNANCE RULES
COMMIT — AI RECOVERY RECORDS
COMMIT — INVESTIGATION RECORDS
DEFER — NEEDS SEPARATE AUDIT
PROTECT — UNRELATED
```

If one file contains multiple concerns, classify it as:

```text
MIXED — REQUIRES HUNK SPLIT
```

and explain exact hunks.

---

# 5. REQUIRED FILE AUDIT

For every modified tracked file:

1. Read the complete diff.
2. State the exact semantic change.
3. Confirm whether the change was already validated.
4. Identify its proper commit group.
5. State whether it can be committed as-is.

For every untracked file:

1. Read the file.
2. State its purpose.
3. Identify whether it belongs in source, contract, AI instruction or investigation.
4. State whether it should be committed now or deferred.

---

# 6. VALIDATION STATUS

Audit and report the known validation status of each proposed commit group.

At minimum:

```text
Contracts:
6 files / 42 tests / PASS

Build:
fails only on installedPlugins

Kernel path recovery:
validated

@kernel alias recovery:
validated

getAllWorkspaces correction:
validated

DashboardValidator guard:
validated
```

Do not rerun commands unless needed to verify current state.

If rerunning:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

Do not modify files.

---

# 7. COMMIT PLAN REQUIREMENTS

Produce an ordered commit plan.

Each commit must include:

```text
Commit number
Purpose
Exact files
Why these files belong together
Validation already available
Suggested commit message
Any prerequisites
```

Prefer small, coherent commits.

Do not create a commit combining:

```text
Kernel + Dashboard contracts
Runtime + investigations
AI instructions + production code
Reglas.md + unrelated source changes
```

---

# 8. REGLAS.MD DECISION

Audit `gypport/Reglas.md` separately.

Determine whether it is:

```text
ready for commit
partially duplicated by Foundation v3
requires a consistency audit
should remain uncommitted for now
```

Do not automatically include it in another commit.

---

# 9. DOCUMENTATION DECISION

Audit:

```text
docs/ai/**
docs/investigations/**
```

Distinguish:

```text
operational AI instruction
audit evidence
technical investigation
canonical architecture
```

None of these should be mixed with production-code commits.

---

# 10. REQUIRED OUTPUT

Return:

```text
1. Executive verdict

2. Repository root and branch

3. Current Git state

4. Complete file classification table

5. Mixed-file findings

6. Validation status by group

7. Ordered commit plan

8. Exact file list per commit

9. Suggested commit message per commit

10. Files to defer

11. Reglas.md decision

12. Documentation decision

13. Recommended first commit to execute

14. Final git status --short
```

---

# 11. STRICTLY PROHIBITED

Do not modify files.

Do not:

```text
git add
git commit
git push
git restore
git clean
git reset
git stash
```

Do not fix:

```text
installedPlugins
Theme
App composition
DashboardRuntime
WidgetRegistry resolution
```

This is classification only.

---

# 12. STOP CONDITION

Stop after the commit plan.

Do not generate or execute commit commands.

End with:

```text
git status --short
```

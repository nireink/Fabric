# CLAUDE-ROLLBACK-01

## GYPPORT® PLATFORM OS

**Track:** Repository Recovery  
**Step:** RECOVERY-01 — Unauthorized Boundary Expansion Audit  
**Mode:** Read-Only Audit  
**Agent:** Claude  
**Status:** Ready for Execution  

---

# 1. PURPOSE

Identify exactly which current uncommitted changes belong to the unauthorized expansion from:

```text
Dashboard Engine
```

into:

```text
Legacy UI Migration
Journey
Module UI
Channel restructuring
App composition
Theme restructuring
```

Do not modify files.

The goal is to prepare a precise rollback plan that preserves:

```text
Toolchain work
Dashboard Engine contracts
Dashboard Registry contracts
Dashboard Validator correction
Contract harness
validated Runtime recovery fixes
Foundation documentation already committed
investigation/audit knowledge
```

and removes only unauthorized implementation.

---

# 2. CLOSED AUTHORIZATION

Authorized tracks:

```text
Developer Platform / Toolchain
Dashboard Engine stabilization
```

Authorized Dashboard areas:

```text
platform_os/studio/engine/core/ui/dashboard/
platform_os/studio/engine/core/ui/widget/
platform_os/studio/engine/core/registry/ui/
platform_os/studio/contracts/dashboard/
platform_os/studio/contracts/registry/ui/
contract harness required to execute those contracts
minimal Runtime recovery already validated
```

Unauthorized expansion to remove:

```text
platform_os/studio/journey/
platform_os/studio/module/party/ui/
platform_os/studio/module/tax/
platform_os/studio/module/workforce/
Legacy UI physical migration
React/UI relocation outside Browser Shell
new Journey alias created for that migration
react-router-dom added only for migrated Legacy UI
authService created only for that migration
archive movement caused by that migration
```

---

# 3. REQUIRED INITIAL COMMANDS

Run:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
git log --oneline -10
```

Expected repository root:

```text
D:/NZXTG7/GYPPORT/GYPPORT Fabric/Gystigo/gypport
```

Expected branch:

```text
master
```

Do not modify, stage, commit, push, restore, clean, reset or stash.

---

# 4. CURRENT COMMIT TO PRESERVE

Preserve the committed Foundation documentation commit:

```text
0086845 docs(architecture): establish GYPPORT Foundation v3 governance
```

Do not revert that commit.

The two Legacy UI investigation documents committed under `docs/architecture/` are misclassified, but do not move them in this audit. Record them for a later documentation-only correction.

---

# 5. FILE-BY-FILE CLASSIFICATION

Classify every current modified, deleted and untracked path into exactly one:

```text
KEEP — TOOLCHAIN
KEEP — DASHBOARD ENGINE
KEEP — CONTRACT HARNESS
KEEP — VALIDATED RUNTIME RECOVERY
KEEP — KNOWLEDGE / INVESTIGATION
REMOVE — UNAUTHORIZED LEGACY UI MIGRATION
REMOVE — UNAUTHORIZED JOURNEY
REMOVE — UNAUTHORIZED MODULE UI
REMOVE — UNAUTHORIZED CHANNEL/UI SUPPORT CHANGE
REVIEW — MIXED FILE
UNRELATED — PROTECT
```

At minimum inspect:

```text
Reglas.md

platform_os/studio/channel/browser/shell/package.json
platform_os/studio/channel/browser/shell/package-lock.json
platform_os/studio/channel/browser/shell/vite.alias.js
platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
platform_os/studio/channel/browser/shell/vitest.config.js

platform_os/studio/channel/browser/shell/src/legacy/**

platform_os/studio/contracts/dashboard/**
platform_os/studio/contracts/registry/**

platform_os/studio/journey/**
platform_os/studio/module/party/ui/**
platform_os/studio/module/tax/**
platform_os/studio/module/workforce/**

platform_os/studio/engine/core/runtime/**
platform_os/studio/engine/core/ui/dashboard/DashboardValidator.js
platform_os/studio/engine/kernel/**

docs/archive/**
docs/investigations/**
```

---

# 6. MIXED FILE AUDIT

The following files may contain both valid and unauthorized changes:

```text
package.json
package-lock.json
vite.alias.js
StudioBootstrap.js
```

For each mixed file identify exact hunks:

```text
KEEP
REMOVE
```

Examples to verify:

```text
Vitest dependency/script
    likely KEEP — contract harness

react-router-dom dependency
    likely REMOVE — Legacy UI migration

@kernel alias
    KEEP — validated Runtime recovery

@journey alias
    REMOVE — unauthorized migration

getAllWorkspaces correction
    KEEP — validated Runtime recovery

installedPlugins remains unresolved
    no implementation authorized
```

Do not assume. Verify actual diffs and package-lock ownership.

---

# 7. LEGACY FILE RESTORATION PLAN

Determine whether the deleted files under:

```text
platform_os/studio/channel/browser/shell/src/legacy/
```

must be restored from `HEAD`.

Confirm that their new copies under:

```text
journey/
module/*/ui/
```

are untracked migration outputs.

Prepare exact rollback actions:

```text
restore original tracked Legacy files
delete unauthorized untracked migrated copies
remove directories only when empty
```

Do not execute.

---

# 8. KNOWLEDGE PRESERVATION

Preserve as evidence:

```text
docs/investigations/**
Dashboard audit trails
Legacy UI migration investigation
Organizacion de repositorio
Especificacion de desarrollo de DASHBOARD
```

Do not treat investigation documents as production implementation.

Report whether any evidence file is currently under the wrong documentation category.

---

# 9. REQUIRED OUTPUT

Return:

```text
1. Executive verdict

2. Repository root and branch

3. Current Git state

4. Commit 0086845 preservation confirmation

5. Complete path classification table

6. Mixed-file hunk classification

7. Exact files to restore from HEAD

8. Exact untracked files/directories to delete

9. Exact files to keep

10. Exact documentation files to preserve

11. Exact documentation reclassification deferred

12. Proposed CODEX-ROLLBACK-01 allowed files

13. Proposed CODEX-ROLLBACK-01 prohibited files

14. Exact validation commands after rollback

15. Final git status --short
```

---

# 10. STOP CONDITION

Do not modify anything.

Do not generate broad commands such as:

```text
git reset --hard
git clean -fd
git restore .
```

The rollback must be selective and evidence-based.

Stop after the audit.

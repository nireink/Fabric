# CODEX-ROLLBACK-01

## GYPPORT® PLATFORM OS

**Track:** Repository Recovery  
**Step:** RECOVERY-01 — Selective Rollback of Unauthorized Boundary Expansion  
**Mode:** Minimal Recovery Implementation  
**Agent:** Codex  
**Status:** Ready for Execution  

---

# 1. ARCHITECTURE COMPLIANCE

Read first:

```text
gypport/AGENTS.md
gypport/Reglas.md
gypport/docs/architecture/ARCHITECTURE_GOVERNANCE.md
gypport/docs/architecture/STRUCTURE_CANONICAL.md
gypport/docs/architecture/BOUNDARY_RULES.md
gypport/docs/architecture/ACTIVE_TRACKS.md
gypport/docs/ai/claude/CLAUDE-ROLLBACK-01.md
```

Then report:

```text
Active Track:
Repository Recovery

Authorized Boundary:
Only the exact files and directories listed in this STEP

Architecture Change:
NO — selective rollback to previously authorized boundaries

Decision:
PASS / STOP
```

If `Decision` is not `PASS`, stop.

---

# 2. PURPOSE

Remove only the unauthorized implementation expansion that moved beyond:

```text
Toolchain
+
Dashboard Engine
```

into:

```text
Legacy UI Migration
Journey
Module UI
Channel/UI support changes created only for that migration
```

Preserve all validated work in:

```text
Toolchain
Dashboard Engine
Dashboard contracts
Registry contracts
Vitest contract harness
DashboardValidator correction
Kernel recovery
Core Runtime recovery
StudioBootstrap getAllWorkspaces correction
Foundation v3 documentation
Investigation/audit knowledge
```

Do not perform a broad rollback.

Do not use:

```text
git reset --hard
git clean -fd
git restore .
git checkout .
```

---

# 3. REPOSITORY ROOT

Expected Git repository root:

```text
D:/NZXTG7/GYPPORT/GYPPORT Fabric/Gystigo
```

Expected branch:

```text
master
```

Run:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

If root or branch differs, stop.

---

# 4. PROTECTED COMMIT

Preserve:

```text
0086845 docs(architecture): establish GYPPORT Foundation v3 governance
```

Do not revert this commit.

Do not rewrite history.

Do not reset HEAD.

---

# 5. PREEXISTING CHANGES TO PROTECT

Do not modify:

```text
gypport/Reglas.md

gypport/platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
gypport/platform_os/studio/channel/browser/shell/vitest.config.js

gypport/platform_os/studio/engine/**
gypport/platform_os/studio/contracts/**

gypport/docs/investigations/**
gypport/docs/ai/**
gypport/docs/architecture/**

gypport/developer_platform/toolchain/**
gypport/platform_os/server/**
```

Exception:

```text
Do not touch docs/architecture legacy-organigram relocation in this STEP.
That documentation correction is deferred.
```

---

# 6. EXACT AUTHORIZED RESTORATION

Restore these 9 tracked Legacy UI files from `HEAD`:

```text
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/component/FormularioParties.jsx
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/component/FormularioPartyIdentidad.jsx
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/component/FormularioPartyTributario.jsx
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/component/ListaParties.jsx
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/employee/views/FormularioEmpleado.jsx
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/employee/views/ModuloEquipo.jsx
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/views/Dashboard.jsx
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/views/LoginPage.jsx
gypport/platform_os/studio/channel/browser/shell/src/legacy/module/views/ShortRegisterView.jsx
```

Use:

```text
git restore --source=HEAD -- <exact paths>
```

Do not restore any other file.

---

# 7. EXACT AUTHORIZED DELETIONS

Delete only these untracked unauthorized implementation directories/files:

```text
gypport/platform_os/studio/journey/

gypport/platform_os/studio/module/party/ui/

gypport/platform_os/studio/module/tax/

gypport/platform_os/studio/module/workforce/

gypport/docs/archive/legacy-ui/Dashboard.jsx
```

After deleting `Dashboard.jsx`, remove:

```text
gypport/docs/archive/legacy-ui/
gypport/docs/archive/
```

only if those directories are empty.

Do not delete any other documentation.

Do not delete:

```text
gypport/platform_os/studio/module/party/index.js
gypport/platform_os/studio/module/party/service/
```

---

# 8. PACKAGE.JSON CORRECTION

File:

```text
gypport/platform_os/studio/channel/browser/shell/package.json
```

Preserve:

```json
"contracts": "vitest run --config vitest.config.js"
```

Remove only:

```json
"react-router-dom": "^7.18.1"
```

Do not alter any other script or dependency.

Do not remove Vitest.

---

# 9. PACKAGE-LOCK CORRECTION

File:

```text
gypport/platform_os/studio/channel/browser/shell/package-lock.json
```

Regenerate it only as required to remove the dependency tree introduced by:

```text
react-router-dom
react-router
cookie
```

Preferred method:

1. Remove `react-router-dom` from `package.json`.
2. From the Browser Shell package directory, run:

```text
npm install --package-lock-only
```

Do not run a broad dependency upgrade.

Do not change package versions unrelated to removing `react-router-dom`.

After regeneration, verify no `react-router-dom` entry remains.

If unrelated lockfile drift appears, stop and report.

---

# 10. VITE ALIAS CORRECTION

File:

```text
gypport/platform_os/studio/channel/browser/shell/vite.alias.js
```

Preserve:

```javascript
"@kernel": path.resolve(rootDir, "../../../engine/kernel")
```

Remove only:

```javascript
"@journey": path.resolve(rootDir, "../../../journey")
```

Do not modify other aliases.

---

# 11. STRICTLY PROHIBITED CHANGES

Do not modify:

```text
StudioBootstrap.js
vitest.config.js
DashboardValidator.js
Kernel.js
KernelDiagnostics.js
KernelHealth.js
KernelLifecycle.js
Core Runtime files
contracts/**
Reglas.md
Foundation documents
investigation documents
Toolchain
Server
```

Do not fix:

```text
installedPlugins
Theme
App composition
DashboardRuntime
WidgetRegistry resolution
```

Do not stage.

Do not commit.

Do not push.

---

# 12. REQUIRED SEARCHES AFTER CLEANUP

Confirm zero active source paths remain under:

```text
gypport/platform_os/studio/journey/
gypport/platform_os/studio/module/party/ui/
gypport/platform_os/studio/module/tax/
gypport/platform_os/studio/module/workforce/
```

Confirm:

```text
@journey
react-router-dom
```

have zero active source/config matches under:

```text
gypport/platform_os/studio/
```

excluding investigation/archive documentation.

Confirm the 9 Legacy UI files exist again at their original tracked paths.

---

# 13. CONTRACT VALIDATION

Run exactly:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Expected baseline:

```text
6 test files
42 tests
exit code 0
```

Report actual counts.

Do not modify contracts to obtain a pass.

---

# 14. BUILD VALIDATION

Run exactly:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

Expected result:

```text
The rollback must not reintroduce:
@core/kernel
plugins/PluginRegistry
getWorkspaces
```

The build may still stop on:

```text
installedPlugins is not exported by module/index.js
```

That blocker is expected and out of scope.

Do not fix it.

---

# 15. GIT VALIDATION

Run:

```text
git status --short
git --no-pager diff --stat
git diff --cached --stat
```

Success requires:

```text
no deleted Legacy UI files

no untracked journey/

no untracked module/party/ui/

no untracked module/tax/

no untracked module/workforce/

no docs/archive/legacy-ui/Dashboard.jsx

package.json retains only the Vitest contracts change

vite.alias.js retains only the @kernel change

nothing staged
```

The following valid pending changes may remain:

```text
Reglas.md
StudioBootstrap.js
vitest.config.js
Core Runtime @kernel corrections
Kernel plugin-path corrections
DashboardValidator.js
Dashboard contracts
Registry contracts
investigation documents
documentation relocation state
```

---

# 16. REQUIRED FINAL REPORT

Return:

```text
1. Repository root

2. Branch

3. Initial git status --short

4. Authorization compliance result

5. Exact 9 files restored

6. Exact directories/files deleted

7. Exact package.json diff

8. Exact package-lock result

9. Exact vite.alias.js diff

10. Confirmation @kernel was preserved

11. Confirmation @journey was removed

12. Confirmation react-router-dom was removed

13. Confirmation Legacy UI files exist again

14. Confirmation unauthorized journey/module UI paths are gone

15. Full contracts command and output

16. Contracts exit code and counts

17. Full build command and output

18. Build exit code

19. Confirmation prior Runtime blockers were not reintroduced

20. Exact next build blocker

21. git --no-pager diff --stat

22. Final git status --short

23. git diff --cached --stat

24. Confirmation Foundation commit 0086845 was preserved

25. Confirmation StudioBootstrap was untouched

26. Confirmation Engine and contracts were untouched

27. Confirmation Toolchain was untouched

28. Confirmation documentation investigations were untouched

29. Confirmation nothing was staged, committed or pushed
```

---

# 17. STOP CONDITIONS

Stop immediately if:

```text
repository root differs

branch differs

a tracked file outside the 9 Legacy files would be restored

package-lock regeneration changes unrelated dependency versions

a protected file changes

contracts fail because of the rollback

an unexpected file outside the authorized boundary changes
```

Do not improvise.

---

# 18. STOP AFTER VALIDATION

After cleanup and validation:

```text
STOP
```

Do not proceed to:

```text
documentation relocation
commit
installedPlugins
Toolchain policy implementation
Dashboard continuation
```

End with:

```text
git status --short
```

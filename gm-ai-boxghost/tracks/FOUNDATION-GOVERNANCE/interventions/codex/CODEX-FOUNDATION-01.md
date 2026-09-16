# CODEX-FOUNDATION-01

## GYPPORT® PLATFORM FOUNDATION v3.0

**Track:** Foundation Governance  
**Step:** FOUNDATION-01 — Adopt Architecture Foundation Documents  
**Mode:** Documentation-Only Implementation  
**Agent:** Codex  
**Status:** Ready for Execution  

---

# 1. ARCHITECTURE COMPLIANCE

Before doing anything, read:

```text
gypport/AGENTS.md
gypport/Reglas.md
gypport/docs/project/GYPPORT_MASTER_PROJECT_CONTEXT.md
```

Also inspect any nearest hierarchical `AGENTS.md` that applies to:

```text
gypport/docs/
gypport/docs/architecture/
```

The authoritative sources for this STEP are:

```text
CURRENT REPOSITORY
CURRENT GIT STATE
CURRENT DOCUMENTATION POLICIES
THE PROVIDED FOUNDATION v3.0 DOCUMENT PACKAGE
```

This STEP is documentation-only.

It must not modify Platform OS, Developer Platform, Toolchain, Studio, UI, Server, modules, journeys, runtime code, contracts, dependencies, aliases, build files or production source.

---

# 2. PURPOSE

Adopt the prepared GYPPORT® Architecture Foundation v3.0 documentation package into:

```text
gypport/docs/architecture/
```

The package contains governance documents, ADRs and templates.

This STEP only copies or creates the provided documentation files in the repository.

It does not:

```text
update AGENTS.md
update CLAUDE.md
create or update CODEX.md
rewrite Reglas.md
reclassify existing documents
move Legacy UI files
revert unauthorized Studio changes
implement Toolchain policies
modify active track code
```

Those actions belong to later FOUNDATION STEPs.

---

# 3. INPUT PACKAGE

Use the package supplied by the user:

```text
GYPPORT_FOUNDATION_V3_DOCUMENTS.zip
```

The package has this internal root:

```text
gypport/docs/architecture/
```

Do not invent additional documents.

Do not rewrite or “improve” the supplied contents during adoption.

Do not rename files unless an existing repository policy makes the proposed name invalid. If that occurs, stop and report before copying anything.

---

# 4. REPOSITORY ROOT

Operate only in:

```text
D:/NZXTG7/GYPPORT/GYPPORT Fabric/Gystigo
```

Expected branch:

```text
master
```

---

# 5. REQUIRED INITIAL COMMANDS

Run and report:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

If the repository root or branch differs, stop and report.

Do not:

```text
switch branches
create a worktree
stash
clean
restore
reset
stage
commit
push
```

---

# 6. AUTHORIZED BOUNDARY

The only authorized destination boundary is:

```text
gypport/docs/architecture/
```

Allowed subdirectories:

```text
gypport/docs/architecture/decisions/
gypport/docs/architecture/templates/
```

No file outside:

```text
gypport/docs/architecture/
```

may be created, deleted, renamed or modified.

---

# 7. PREEXISTING WORKING TREE PROTECTION

The repository may already contain pending changes from:

```text
Toolchain
Dashboard Engine
Runtime recovery
Legacy UI migration
Journey
Party
Tax
Workforce
Theme
documentation investigations
```

Protect every preexisting change.

Do not:

```text
restore
delete
rename
format
stage
commit
merge
overwrite
```

any unrelated file.

If `gypport/docs/architecture/` already contains pending files, inspect them before adoption.

Do not overwrite an existing file blindly.

---

# 8. COLLISION CHECK

Before copying, compare the package file list against the current repository.

For every destination file, classify:

```text
NEW
EXISTS IDENTICAL
EXISTS DIFFERENT
```

Rules:

## NEW

Safe to create.

## EXISTS IDENTICAL

Do not rewrite unnecessarily. Report it as already present and identical.

## EXISTS DIFFERENT

Stop before modifying that file.

Report:

```text
destination path
current SHA256
package SHA256
first meaningful differences
```

Do not merge automatically.

Do not choose one version unilaterally.

The user must decide how to resolve a content collision.

---

# 9. EXPECTED FILES

The package is expected to contain these 21 files:

```text
gypport/docs/architecture/README.md

gypport/docs/architecture/ARCHITECTURE_GOVERNANCE.md
gypport/docs/architecture/PLATFORM_FOUNDATION.md
gypport/docs/architecture/STRUCTURE_CANONICAL.md
gypport/docs/architecture/BOUNDARY_RULES.md
gypport/docs/architecture/DEVELOPMENT_GOVERNANCE.md
gypport/docs/architecture/TOOLCHAIN_GOVERNANCE.md
gypport/docs/architecture/NAMING_CONVENTIONS.md
gypport/docs/architecture/DOCUMENTATION_GOVERNANCE.md
gypport/docs/architecture/AI_GOVERNANCE.md
gypport/docs/architecture/FOUNDATION_CHANGE_PROCESS.md
gypport/docs/architecture/ACTIVE_TRACKS.md
gypport/docs/architecture/REPOSITORY_ADOPTION_PLAN.md

gypport/docs/architecture/decisions/ADR-0001-SINGLE-KERNEL-OWNERSHIP.md
gypport/docs/architecture/decisions/ADR-0002-BROWSER-CHANNEL-UI-OWNERSHIP.md
gypport/docs/architecture/decisions/ADR-0003-DASHBOARD-PARALLEL-TRACK-LIMIT.md
gypport/docs/architecture/decisions/ADR-0004-REGISTRY-CENTRALIZATION.md

gypport/docs/architecture/templates/CODEX_STEP_TEMPLATE.md
gypport/docs/architecture/templates/CLAUDE_AUDIT_TEMPLATE.md
gypport/docs/architecture/templates/ADR_TEMPLATE.md
gypport/docs/architecture/templates/TRACK_DECLARATION_TEMPLATE.md
```

If the package contains more or fewer files, stop and report the exact package inventory before writing.

---

# 10. EXACT IMPLEMENTATION

After completing all collision checks:

1. Create only the required directories under:

```text
gypport/docs/architecture/
```

2. Copy the package files byte-for-byte to their matching repository paths.

3. Preserve:

```text
UTF-8 text
file names
directory names
Markdown content
status labels
document ordering
```

4. Do not normalize or reformat document contents.

5. Do not add generated headers, timestamps or agent signatures.

---

# 11. STRICTLY PROHIBITED FILES AND AREAS

Do not modify:

```text
gypport/AGENTS.md
gypport/CLAUDE.md
gypport/CODEX.md
gypport/Reglas.md
```

Do not modify:

```text
gypport/docs/project/
gypport/docs/investigations/
gypport/docs/archive/
```

Do not modify anything under:

```text
gypport/platform_os/
gypport/developer_platform/
```

Do not touch:

```text
Toolchain
Dashboard Engine
contracts
Kernel
Core
Framework
StudioBootstrap
Legacy UI
journey/
module/
channel/
app/
server/
database/
package.json
package-lock.json
vite.alias.js
```

---

# 12. NON-GOALS

This STEP does not authorize:

```text
reverting unauthorized migrations
moving JSX
creating app/business-studio
fixing installedPlugins
continuing Dashboard Engine
continuing Runtime recovery
adding Toolchain policies
running migrations
updating agent instructions
changing project context
archiving Legacy UI documents
```

If any of those are needed, record them as future FOUNDATION STEPs and stop.

---

# 13. DOCUMENT VALIDATION

After copying, validate:

```text
all 21 expected files exist

no expected file is empty

all files are readable as UTF-8

all Markdown code fences are balanced where practically verifiable

all relative links remain unchanged

the package and destination SHA256 match per file
```

Generate a table:

```text
File
Package SHA256
Destination SHA256
Result
```

Every copied file must show:

```text
MATCH
```

---

# 14. SCOPE VALIDATION

Run:

```text
git status --short
```

Then verify that the only STEP-specific changes are under:

```text
gypport/docs/architecture/
```

If any new change outside that boundary appears, stop and report.

Do not attempt to clean or repair the unexpected change.

---

# 15. OPTIONAL DOCUMENT SEARCH

Search the newly adopted documents for the following closed rules and report the files containing them:

```text
Boundary Expansion Rule
single Kernel
Dashboard parallel track
React/JSX browser ownership
Toolchain does not automatically enforce Markdown
project owner final authority
```

This search is validation only.

Do not edit documents if wording differs.

---

# 16. REQUIRED GIT COMMANDS

Run:

```text
git --no-pager diff --stat
git status --short
git diff --cached --stat
```

Because new files may be untracked, also print:

```text
Get-ChildItem -Recurse gypport/docs/architecture | Select-Object FullName
```

or an equivalent repository-safe listing command.

Nothing may be staged.

---

# 17. SUCCESS CRITERIA

This STEP succeeds only if:

```text
repository root and branch are correct

the package contains exactly the expected 21 files

no conflicting existing file was overwritten

all package files were adopted under docs/architecture

all per-file hashes match

no file outside docs/architecture changed in this STEP

no code or runtime area was touched

nothing was staged

nothing was committed

nothing was pushed
```

---

# 18. STOP CONDITIONS

Stop immediately if:

```text
repository root differs

branch differs

the package is unavailable

the package inventory differs

a destination file exists with different content

an existing documentation policy prohibits the destination

a file outside docs/architecture changes

a copy requires editing production code or root governance files
```

Do not improvise.

Do not merge conflicting documents.

Do not continue to FOUNDATION-02.

---

# 19. REQUIRED FINAL REPORT

Return:

```text
1. Repository root

2. Branch

3. Initial git status --short

4. Package path used

5. Package file count

6. Exact package inventory

7. Collision-check result per file

8. Files created

9. Files already identical

10. Conflicting files, if any

11. Per-file SHA256 verification table

12. Confirmation all files are UTF-8 readable

13. Confirmation only docs/architecture changed in this STEP

14. Full recursive destination tree

15. git --no-pager diff --stat

16. Final git status --short

17. git diff --cached --stat

18. Confirmation AGENTS.md was untouched

19. Confirmation CLAUDE.md was untouched

20. Confirmation CODEX.md was untouched

21. Confirmation Reglas.md was untouched

22. Confirmation Platform OS was untouched

23. Confirmation Toolchain was untouched

24. Confirmation contracts were untouched

25. Confirmation nothing was staged, committed or pushed
```

---

# 20. STOP AFTER SUCCESS

After adoption and validation:

```text
STOP
```

Do not begin:

```text
FOUNDATION-02
FOUNDATION-03
rollback/reversion
Toolchain policy implementation
Dashboard work
Runtime recovery
```

End with:

```text
git status --short
```

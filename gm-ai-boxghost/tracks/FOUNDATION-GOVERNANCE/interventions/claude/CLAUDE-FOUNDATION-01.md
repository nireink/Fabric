# CLAUDE-FOUNDATION-01

## GYPPORT® PLATFORM FOUNDATION v3.0

**Track:** Foundation Governance  
**Step:** FOUNDATION-01 — Architecture Foundation Adoption Audit  
**Mode:** Read-Only Documentation and Process Audit  
**Agent:** Claude  
**Status:** Ready for Audit  

---

# 1. ARCHITECTURE COMPLIANCE

Before doing anything, read:

```text
gypport/AGENTS.md
gypport/Reglas.md
gypport/docs/project/GYPPORT_MASTER_PROJECT_CONTEXT.md
```

Then read the newly adopted Foundation documents under:

```text
gypport/docs/architecture/
```

Also inspect any nearest hierarchical `AGENTS.md` applicable to:

```text
gypport/docs/
gypport/docs/architecture/
```

The authoritative sources for this audit are:

```text
CURRENT REPOSITORY
CURRENT GIT STATE
CURRENT DOCUMENTATION POLICIES
ADOPTED FOUNDATION DOCUMENTS
CODEX-FOUNDATION-01 RESULT
```

This audit is strictly read-only.

Do not modify files.

---

# 2. PURPOSE

Audit the execution of:

```text
CODEX-FOUNDATION-01
```

which was authorized only to adopt the prepared GYPPORT® Architecture Foundation v3.0 documentation package into:

```text
gypport/docs/architecture/
```

Determine whether:

```text
FOUNDATION-01
```

can be formally closed.

This audit must verify:

```text
package adoption completeness
file integrity
hash consistency
scope integrity
document readability
working-tree protection
absence of production/code changes
```

Do not begin FOUNDATION-02.

---

# 3. REPOSITORY ROOT

Audit only:

```text
D:/NZXTG7/GYPPORT/GYPPORT Fabric/Gystigo
```

Expected branch:

```text
master
```

---

# 4. REQUIRED INITIAL COMMANDS

Run and report:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

If root or branch differs, stop and report.

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

# 5. EXPECTED FOUNDATION INVENTORY

The adopted package must contain exactly these 21 files:

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

No additional file created by FOUNDATION-01 is expected.

---

# 6. FILESYSTEM AUDIT

Inspect recursively:

```text
gypport/docs/architecture/
```

Confirm:

```text
all 21 expected files exist

no expected file is missing

no unexpected FOUNDATION-01 file exists

all expected directories exist

no empty expected file exists
```

Produce the exact tree.

If the existing repository already had unrelated files under `docs/architecture/`, classify them separately as:

```text
PREEXISTING
NOT PART OF FOUNDATION-01
```

Do not treat legitimate preexisting files as an automatic failure.

---

# 7. CONTENT INTEGRITY AUDIT

Read all 21 files.

Confirm each is:

```text
UTF-8 readable

non-empty

valid Markdown text

not truncated

not replaced by binary content

not altered by generated headers or agent signatures
```

Check practical Markdown integrity:

```text
balanced fenced code blocks where verifiable

no obvious accidental truncation

no broken file encoding

no merge-conflict markers
```

Search for:

```text
<<<<<<<
=======
>>>>>>>
```

Expected result:

```text
zero merge-conflict markers
```

---

# 8. REQUIRED RULE PRESENCE AUDIT

Confirm the adopted Foundation contains the following decisions.

## Project owner authority

A rule stating that the user/project owner retains final architecture and Git authority.

## Boundary Expansion Rule

A finding outside the authorized boundary does not authorize implementation.

## Single Kernel

One Kernel at:

```text
engine/kernel/
```

and rejection of:

```text
engine/core/kernel/
@core/kernel
```

## Browser Channel UI ownership

React/JSX for browser belongs to:

```text
channel/browser/shell/
```

and these are rejected as final structures:

```text
module/*/ui/browser/
journey/*/ui/browser/
```

## Dashboard parallel-track limit

Dashboard Engine authorization does not authorize general Studio reorganization.

## Toolchain limitation

Markdown rules are not automatically enforced unless implemented as Toolchain policies/contracts/commands.

## AI role separation

Codex implements, Claude audits, ChatGPT coordinates governance, and the project owner remains final authority.

For each rule, report:

```text
file
section/heading
exact conclusion
```

---

# 9. DOCUMENT PRECEDENCE AUDIT

Read:

```text
ARCHITECTURE_GOVERNANCE.md
DOCUMENTATION_GOVERNANCE.md
```

Confirm they establish that:

```text
Governance and approved ADRs outrank investigations

filesystem proves current state but not architectural validity

investigation documents cannot silently become canonical

chat narrative is supplementary
```

Classify:

```text
PRECEDENCE CLEAR

PRECEDENCE PARTIALLY CLEAR

PRECEDENCE CONFLICTING
```

---

# 10. ACTIVE TRACKS AUDIT

Read:

```text
ACTIVE_TRACKS.md
ADR-0003-DASHBOARD-PARALLEL-TRACK-LIMIT.md
DEVELOPMENT_GOVERNANCE.md
```

Confirm the current governance baseline states:

```text
Main Track:
Developer Platform / Toolchain

Parallel Active:
Dashboard Engine stabilization

Frozen:
Legacy UI migration
Journey restructuring
Module UI restructuring
Channel restructuring
App composition
Theme restructuring
Party/Tax/Workforce UI expansion
```

Report any contradiction among those three documents.

Do not change track status.

---

# 11. SCOPE / PROCESS INTEGRITY AUDIT

Compare initial and final Git state reported by Codex.

Independently inspect:

```text
git status --short
git --no-pager diff --stat
git diff --cached --stat
```

Determine whether FOUNDATION-01 introduced changes only under:

```text
gypport/docs/architecture/
```

Confirm no STEP-specific modification to:

```text
gypport/AGENTS.md
gypport/CLAUDE.md
gypport/CODEX.md
gypport/Reglas.md

gypport/platform_os/
gypport/developer_platform/
gypport/docs/project/
gypport/docs/investigations/
gypport/docs/archive/
```

Do not confuse unrelated preexisting changes with FOUNDATION-01 changes.

Use:

```text
initial Git state
current Git state
file timestamps only as secondary evidence
Codex report
actual diff/content
```

---

# 12. HASH / COPY AUDIT

If the original package remains available locally, independently compare package files and repository files using SHA256.

For each expected file report:

```text
File
Package SHA256
Repository SHA256
MATCH / MISMATCH
```

If the original package is unavailable in Claude's environment, report:

```text
SOURCE PACKAGE UNAVAILABLE FOR INDEPENDENT HASH COMPARISON
```

Then verify integrity through:

```text
Codex hash report
repository file inventory
full content inspection
```

Do not invent hashes.

---

# 13. ROOT GOVERNANCE FILE PROTECTION

Confirm FOUNDATION-01 did not modify:

```text
gypport/AGENTS.md
gypport/CLAUDE.md
gypport/CODEX.md
gypport/Reglas.md
```

These files belong to later adoption steps.

Classify each:

```text
UNTOUCHED BY FOUNDATION-01

PREEXISTING CHANGE, PROTECTED

UNAUTHORIZED FOUNDATION-01 CHANGE
```

---

# 14. CODE / PLATFORM PROTECTION

Confirm no FOUNDATION-01 change occurred under:

```text
gypport/platform_os/
gypport/developer_platform/
```

Specifically confirm no change to:

```text
Toolchain
Dashboard Engine
contracts
Kernel
Core
Framework
Studio
Server
UI
journey
module
channel
app
dependencies
aliases
build configuration
```

This STEP is rejected if documentation adoption caused any code or production mutation.

---

# 15. DOCUMENT CLASSIFICATION AUDIT

Confirm the new Foundation correctly classifies existing documentation:

```text
GYPPORT_MASTER_PROJECT_CONTEXT.md
→ Project Context

CODEX_PROJECT_CONTEXT_GYPPORT.md
→ Historical Context

Dashboard stabilization audit trail
→ Audit Trail

LEGACY_UI_MIGRATION_ORGANIGRAM.md
→ Investigation / executed migration record
→ not canonical structure

Reglas.md
→ historical rule inventory until consolidation
```

This audit checks only that the classification is documented.

Do not move or rename those files.

---

# 16. CONTRADICTION SCAN

Search the 21 adopted files for internal contradictions concerning:

```text
Kernel ownership

React/JSX ownership

Module responsibility

Journey responsibility

App composition

Dashboard parallel authorization

Toolchain authority

AI authority

document precedence
```

Distinguish:

```text
REAL CONTRADICTION

WORDING TENSION

NO CONTRADICTION
```

Do not edit documents in this audit.

If a contradiction exists, FOUNDATION-01 may still be closed only if it is non-blocking and explicitly scheduled for FOUNDATION-02.

---

# 17. FOUNDATION-01 CLOSURE CLASSIFICATION

Choose exactly one:

```text
APPROVE — FOUNDATION-01 CLOSED

APPROVE WITH NON-BLOCKING OBSERVATIONS — FOUNDATION-01 CLOSED

REQUIRES MINIMAL DOCUMENT CORRECTION — FOUNDATION-01 REMAINS OPEN

REJECT — INCOMPLETE FOUNDATION ADOPTION

REJECT — OUT-OF-SCOPE FILE MODIFICATIONS

REJECT — FOUNDATION CONTENT INTEGRITY FAILURE
```

Also classify separately:

```text
Inventory completeness

Filesystem placement

Content readability

Rule presence

Document precedence

Active track consistency

Hash/copy integrity

Root governance file protection

Platform/Toolchain protection

Git/process integrity
```

---

# 18. NEXT STEP DECISION

If FOUNDATION-01 is approved, recommend:

```text
FOUNDATION-02
Foundation Consistency and Contradiction Audit
```

Mode:

```text
Read-Only Architecture Audit
```

FOUNDATION-02 must compare the new Foundation against:

```text
Reglas.md

AGENTS.md

CLAUDE.md

existing project context

existing ADRs

Legacy UI migration documentation

Dashboard audit trails

current repository structure
```

It must identify:

```text
rules already consolidated

rules still missing

conflicting wording

historical residue

required updates for AGENTS/CLAUDE/CODEX

Toolchain policies still absent
```

Do not generate an implementation prompt to modify root governance files before FOUNDATION-02 is complete.

---

# 19. REQUIRED OUTPUT FORMAT

Return:

```text
1. EXECUTIVE VERDICT

2. REPOSITORY ROOT AND BRANCH

3. INITIAL GIT STATE

4. FOUNDATION FILESYSTEM TREE

5. INVENTORY AUDIT

6. CONTENT INTEGRITY AUDIT

7. REQUIRED RULE PRESENCE AUDIT

8. DOCUMENT PRECEDENCE AUDIT

9. ACTIVE TRACKS AUDIT

10. SCOPE / PROCESS INTEGRITY AUDIT

11. HASH / COPY AUDIT

12. ROOT GOVERNANCE FILE PROTECTION

13. PLATFORM / TOOLCHAIN PROTECTION

14. DOCUMENT CLASSIFICATION AUDIT

15. CONTRADICTION SCAN

16. FOUNDATION-01 CLOSURE DECISION

17. NEXT STEP DECISION

18. READY-TO-PASTE FOUNDATION-02 PROMPT
    optional suggestion only, clearly non-authoritative

19. FINAL git status --short
```

For anything not proven, use:

```text
INSUFFICIENT EXECUTABLE EVIDENCE
```

---

# 20. STRICTLY PROHIBITED

Do not modify files.

Do not:

```text
correct wording
merge documents
rename files
move documents
update AGENTS.md
update CLAUDE.md
create/update CODEX.md
rewrite Reglas.md
revert Legacy UI migration
touch Platform OS
touch Toolchain
touch contracts
stage
commit
push
clean
restore
stash
switch branches
```

This is a read-only audit.

---

# 21. STOP CONDITION

Stop after the FOUNDATION-01 audit and next-step recommendation.

Do not execute FOUNDATION-02.

End with:

```text
git status --short
```

The final Git state must match the initial Git state exactly.

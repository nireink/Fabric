# CLAUDE-FOUNDATION-02

## GYPPORT® PLATFORM FOUNDATION v3.0

**Track:** Foundation Governance  
**Step:** FOUNDATION-02 — Final Consistency and Closure Audit  
**Mode:** Read-Only Audit  
**Agent:** Claude  
**Status:** Ready for Execution  

## 1. Purpose

Close Foundation v3.0.

Audit only the documentation adopted under:

```text
gypport/docs/architecture/
gypport/docs/ai/
```

Compare it against:

```text
gypport/AGENTS.md
gypport/CLAUDE.md
gypport/Reglas.md
gypport/docs/project/GYPPORT_MASTER_PROJECT_CONTEXT.md
```

Do not modify files.

## 2. Required checks

Confirm:

1. No Foundation document contradicts a closed project rule.
2. Kernel remains single and independent at `engine/kernel/`.
3. Browser React/JSX ownership belongs to `channel/browser/shell/`.
4. Dashboard Engine remains an isolated parallel track.
5. Toolchain remains the main track.
6. Legacy UI, Journey restructuring, Module UI restructuring, App composition and Theme remain frozen.
7. Codex, Claude and ChatGPT roles are correctly separated.
8. Root-directory responsibilities are explicit.
9. No duplicated or conflicting Foundation rule exists.
10. No implementation or code change is included in this documentation STEP.

## 3. Git integrity

Run:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
git --no-pager diff --stat
git diff --cached --stat
```

Do not stage, commit, push, restore, clean or modify anything.

## 4. Required verdict

Return exactly one:

```text
APPROVE — FOUNDATION v3.0 CLOSED
APPROVE WITH NON-BLOCKING OBSERVATIONS — FOUNDATION v3.0 CLOSED
REQUIRES DOCUMENT CORRECTION — FOUNDATION REMAINS OPEN
REJECT — FOUNDATION CONTRADICTS CLOSED ARCHITECTURE
```

## 5. Required output

Return:

1. Repository root and branch.
2. Initial Git state.
3. Documents audited.
4. Contradictions found.
5. Missing rules found.
6. Duplicate rules found.
7. Track-governance consistency.
8. AI-governance consistency.
9. Final verdict.
10. Exact files authorized for commit if approved.
11. Recommended commit message.
12. Final `git status --short`.

Stop after the audit.

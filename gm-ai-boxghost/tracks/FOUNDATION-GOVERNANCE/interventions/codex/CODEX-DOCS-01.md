# CODEX-DOCS-01

## GYPPORT® DOCUMENTATION

**Track:** Foundation Governance  
**Step:** DOCS-01 — Finalize Legacy UI Investigation Reclassification  
**Mode:** Documentation-Only Correction  
**Agent:** Codex  
**Status:** Ready for Execution  

## 1. Purpose

Finalize the already-started relocation of these two files:

```text
gypport/docs/architecture/GYPPORT_Legacy_UI_Organigrama.pdf
gypport/docs/architecture/LEGACY_UI_MIGRATION_ORGANIGRAM.md
```

to:

```text
gypport/docs/investigations/legacy-ui/GYPPORT_Legacy_UI_Organigrama.pdf
gypport/docs/investigations/legacy-ui/LEGACY_UI_MIGRATION_ORGANIGRAM.md
```

These are investigation/migration records, not canonical architecture.

## 2. Required checks

Run:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

Confirm branch `master`.

Verify both destination files exist.

Compute SHA256 for:

```text
HEAD:gypport/docs/architecture/GYPPORT_Legacy_UI_Organigrama.pdf
destination PDF

HEAD:gypport/docs/architecture/LEGACY_UI_MIGRATION_ORGANIGRAM.md
destination Markdown
```

Both source/destination pairs must match byte-for-byte.

If either pair does not match, stop.

## 3. Allowed paths only

```text
gypport/docs/architecture/GYPPORT_Legacy_UI_Organigrama.pdf
gypport/docs/architecture/LEGACY_UI_MIGRATION_ORGANIGRAM.md
gypport/docs/investigations/legacy-ui/GYPPORT_Legacy_UI_Organigrama.pdf
gypport/docs/investigations/legacy-ui/LEGACY_UI_MIGRATION_ORGANIGRAM.md
```

Do not modify file contents.

Do not touch Platform OS, Toolchain, contracts, Foundation documents or other investigations.

## 4. Git action

Stage only the four paths above so Git records the relocation.

Use exact path-limited `git add -A -- <paths>`.

Then run:

```text
git diff --cached --name-status
git diff --cached --stat
```

Expected result: two renames, or two deletions plus two additions if Git does not detect rename similarity.

Do not commit.

Do not push.

## 5. Final report

Return:

1. Repository root and branch.
2. SHA256 source/destination pairs.
3. Byte-for-byte comparison result.
4. Exact staged paths.
5. `git diff --cached --name-status`.
6. `git diff --cached --stat`.
7. Final `git status --short`.
8. Confirmation no code file changed.
9. Confirmation nothing committed or pushed.

Stop after staging and reporting.

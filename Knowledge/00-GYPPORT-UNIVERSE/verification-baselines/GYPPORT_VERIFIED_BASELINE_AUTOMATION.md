# GYPPORT — Automatic Verified Baseline Generation

**Automation ID:** `GYPPORT-VERIFIED-BASELINE-AUTOMATION-01`  
**Status:** `IMPLEMENTED_GENERATE_ONLY_PENDING_OWNER_REVIEW`  
**Implemented by:** `GYPPORT_UNIVERSAL_MDM_VERIFICATION_BASELINE_FOUNDATION_01` (2026-09-15)

## Objective

Make Verified Baseline creation a standard automatic closeout action after every
Owner-accepted controlled commit.

The automation does NOT approve work and does NOT start the next STEP.

It only materializes already accepted evidence into canonical Fabric documentation.

## Target location

Script:

```text
Fabric/tools/verification/New-GypportVerifiedBaseline.ps1
```

Canonical output directory:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/
```

Registration log, the canonical and only writable copy:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md
```

The script runs on Windows PowerShell 5.1 or later. It is ASCII-only, because Windows PowerShell
5.1 reads a script without a byte order mark in the ANSI code page.

## Trigger

The script is invoked only after the agent has obtained:

```text
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
```

and the post-commit smoke has passed.

## Required inputs

The closeout process provides a small evidence JSON file:

```json
{
  "baselineId": "GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15",
  "step": "GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15",
  "phase": "PKG_2C_CONTEXTUAL_ACCESS_AND_FK_RECONCILIATION",
  "date": "2026-09-15",
  "migrationHead": "V58",
  "repositories": [
    {
      "name": "gm-entities",
      "commit": "e6d3cbcc5e004e8fbd11c78dc1817b5a00e6bffb"
    },
    {
      "name": "gm-security",
      "commit": "1654f271711e96761ae7d5470dce3d161cb4333b"
    },
    {
      "name": "Gystigo",
      "commit": "a3b7bfeb1b52f06110cd08af185b04f3690b4a43"
    }
  ],
  "verifiedFiles": 52,
  "status": "OWNER_ACCEPTED_COMMITTED_LOCAL"
}
```

The evidence JSON should be generated from the just-completed controlled commit report,
not manually reconstructed from historical chat text.

Required fields:

| Field | Rule |
|---|---|
| `baselineId` | `GYPPORT-<SUBJECT>-VERIFIED-BASELINE-<YYYY-MM-DD>`, whose date equals `date` |
| `step`, `phase` | letters, digits, `_`, `.` and `-` |
| `date` | a calendar date, `YYYY-MM-DD` |
| `migrationHead` | a Flyway version, such as `V58` |
| `repositories` | one entry or more: `name` and the full 40-character `commit`, with an optional `path` |
| `verifiedFiles` | a positive integer, equal to the number of files the accepted commits change |
| `status` | exactly `OWNER_ACCEPTED_COMMITTED_LOCAL` |

Optional fields:

| Field | Rendered as |
|---|---|
| `verification` | object of `KEY: value` pairs, rendered as `KEY=value` under "Verification evidence" |
| `invariants` | object of `KEY: value` pairs, rendered under "Architecture invariants" |
| `knownDebts` | array of one-line strings, rendered under "Known pre-existing debts" |
| `invalidationTriggers` | array of one-line strings, rendered under "Baseline invalidation triggers" |
| `supersedes` | the id of the baseline this one supersedes |

An unknown field is refused, so a misspelt field never disappears silently. Every value is a
single line and never contains a Markdown code fence.

The document's file name derives from the id: `GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15`
gives `GYPPORT_PKG2C_VERIFIED_BASELINE_2026-09-15.md`.

## Automated actions

The generator:

```text
1. validates STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL and every evidence field
2. validates, with read-only git commands, that each repository commit exists locally
3. records commit SHA and parent(s)
4. records commit file lists (status, abbreviated blob id, path); their total must equal verifiedFiles
5. records the migration head supplied by the evidence
6. renders the baseline Markdown from a canonical template (deterministic, UTF-8 without BOM, LF)
7. writes it to Fabric/Knowledge/.../verification-baselines/, never overwriting a different document
8. appends a compact registration to Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md,
   unless its BASELINE_ID is already registered
9. does NOT commit
10. does NOT push
11. does NOT start the next STEP
```

Everything is validated before anything is written: a refused run writes nothing.

## Guarantees

```text
MODIFIES_IMPLEMENTATION_REPOSITORIES=NO
WRITES_OUTSIDE_FABRIC=NO
EXECUTES_TESTS=NO
APPROVES_BASELINE=NO
STARTS_NEXT_STEP=NO
COMMITS=NO
PUSHES=NO
DEFAULT_MODE=GENERATE_ONLY
```

The generator writes only inside Fabric: the baseline document and, only by appending, the
canonical `Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md`. It refuses, as a registration target,
any file whose first heading is `# MOVED`, that is, a compatibility pointer.

The append is byte-level: the existing bytes stay an exact prefix, the entry uses the file's own
line ending, and it keeps the log's separation of two blank lines between entries. A line
`BASELINE_ID=<id>` that is already present is never appended again; a line that carries the id
inside a longer value or after another key is not mistaken for it.

An existing baseline document with identical content is left as it is. One with different content
is refused, because a superseding baseline needs its own id.

## Important separation

Two automation modes were proposed:

```text
GENERATE_ONLY
GENERATE_AND_COMMIT
```

Default:

```text
GENERATE_ONLY
```

`GENERATE_ONLY` is implemented and is the only accepted value. `GENERATE_AND_COMMIT` is not
implemented: it would require explicit Owner authorization, because Fabric may contain unrelated
WIP, and a STEP of its own. Until then, the generated files reach Git only through the Owner's
controlled commit gate, staged by explicit path.

## Parameters and output

| Parameter | Default | Purpose |
|---|---|---|
| `-EvidenceFile` | required | the evidence JSON |
| `-Mode` | `GENERATE_ONLY` | the only mode |
| `-FabricRoot` | two levels above the script | the Fabric repository |
| `-OutputDirectory` | `<FabricRoot>\Knowledge\00-GYPPORT-UNIVERSE\verification-baselines` | where the document is written; it must be named `verification-baselines` |
| `-ReglasPath` (alias `-RulesFile`) | `<FabricRoot>\Knowledge\00-GYPPORT-UNIVERSE\Reglas.md` | the canonical rules log; it must be named `Reglas.md`, and a compatibility pointer is refused |
| `-WorkspaceRoot` | the parent of `-FabricRoot` | where repositories are found: `<root>\<name>` or `<root>\Modules\<name>` |

The output is `KEY=VALUE` lines. A successful run ends with
`STATUS=VERIFIED_BASELINE_GENERATED_PENDING_OWNER_REVIEW` and exit code 0. A refused run prints
`STATUS=REFUSED` and `REASON=`, and exits with code 1.

## Recommended future closeout contract

Every controlled commit prompt should end with:

```text
IF STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL:

1. run the post-commit smoke
2. generate/update Verified Baseline automatically
3. append its registration to Reglas.md
4. report exact generated paths
5. stop for Owner review

DO NOT start the next STEP automatically.
```

It completes the closeout contract of `VERIFIED_BASELINE_REUSE.md`:

```text
IMPLEMENT
→ VERIFY
→ OWNER REVIEW
→ CONTROLLED COMMIT
→ POST-COMMIT SMOKE
→ GENERATE VERIFIED BASELINE
→ REGISTER BASELINE IN Reglas.md
→ OWNER REVIEW
→ NEXT STEP
```

## Why this belongs in Fabric

Verified Baselines are cross-module project knowledge, not runtime source code.

They describe:

```text
- accepted architecture
- commit identities
- reusable verification evidence
- known debts
- invalidation boundaries
```

Therefore Fabric/Knowledge is the canonical owner.

Fabric is the single GYPPORT memory root; the roots and their ownership are defined in
`Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md`.

## Suggested generated path example

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/
GYPPORT_PKG2C_VERIFIED_BASELINE_2026-09-15.md
```

## Suggested evidence input path

Temporary/generated evidence may live under:

```text
Fabric/.verification/evidence/
```

and SHOULD NOT become the canonical source unless intentionally retained. The evidence file is
input only: it is not staged, and it may equally live in a temporary directory.

## Usage

```powershell
.\Fabric\tools\verification\New-GypportVerifiedBaseline.ps1 `
  -EvidenceFile .\Fabric\.verification\evidence\pkg2c.json `
  -Mode GENERATE_ONLY
```

Disposable validation always targets temporary copies, never the real log:

```powershell
.\Fabric\tools\verification\New-GypportVerifiedBaseline.ps1 `
  -EvidenceFile <temp>\evidence.json `
  -OutputDirectory <temp>\verification-baselines `
  -ReglasPath <temp>\Reglas.md
```

This should remain a documentation/evidence generator, not an approval engine.

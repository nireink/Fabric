# GYPPORT Policy — VERIFIED_BASELINE_REUSE

**Policy ID:** `GYPPORT-VERIFIED-BASELINE-REUSE-01`  
**Status:** `OWNER_APPROVED`  
**Effective:** 2026-09-15

## Rule

Once a STEP has been:

```text
IMPLEMENTED
→ VERIFIED
→ OWNER_ACCEPTED
→ COMMITTED_LOCAL
```

its accepted verification evidence becomes a reusable baseline.

Core rule:

```text
An Owner-accepted committed STEP MUST NOT automatically rerun its complete
historical regression while its accepted baseline remains valid.
```

A future agent MUST NOT rerun the complete historical regression merely because it is starting
a new STEP.

Before running historical suites, the agent must first determine whether the relevant accepted
baseline is still valid.

## Required decision

Every future implementation/audit prompt that touches an area with a verified baseline must report:

```text
BASELINE_FOUND=YES|NO
BASELINE_ID=<id or NONE>
BASELINE_REUSE_DECISION=REUSE|PARTIAL_INVALIDATION|FULL_INVALIDATION
BASELINE_REUSE_REASON=<short evidence-based reason>
```

### REUSE

Use when accepted commits/bytes and relevant contracts/invariants remain valid:

```text
verified bytes/hashes remain identical
accepted commits remain valid and reachable
relevant invariants remain unchanged
no materially dependent contract invalidates the baseline
```

Then:

```text
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

Run only:

```text
1. tests for the current STEP
2. tests selected by impact analysis
3. integration smoke needed for current contracts
```

A full regression is repeated only when the previous baseline is explicitly invalidated.

### PARTIAL_INVALIDATION

Use when a new change affects only part of a previous baseline.

Rerun only the affected verification slice and update the baseline with a superseding evidence record.
The superseding record is a new baseline document with its own `BASELINE_ID`, which names the baseline
it supersedes. An existing baseline document is never overwritten.

### FULL_INVALIDATION

Use only when a change materially invalidates the accepted architecture or broad runtime evidence,
for example:

```text
- core ownership changes
- cross-cutting public contract changes
- migration semantics rewritten
- security/session identity model materially changed
- widespread dependency contract change
```

A full regression must never be selected merely "to be safe" without an impact reason. A full
rerun requires a concrete impact analysis that names the invalidated evidence; "Run everything
again to be safe" is NOT sufficient.

### No baseline found

With `BASELINE_FOUND=NO`, the STEP verifies its own scope as usual: its own tests, the suites
selected by impact analysis and the required integration smoke. Once it is Owner-accepted and
committed, it creates the first baseline of its area.

## Canonical evidence hierarchy

Primary byte evidence:

```text
Git commit SHA(s)
```

Secondary evidence:

```text
path manifest
blob/file hashes
test summaries
migration head
known debt list
runtime matrix evidence
```

Conversation history and temporary scratchpad files are NOT canonical baseline storage.

## Memory roots

The GYPPORT memory roots and their ownership are defined in one document:
`Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md`.

For verified baselines this means: baseline documents and their registrations are canonical
knowledge, so they live in `Fabric/Knowledge`; operational evidence retained from a verification
run belongs in `Fabric/gm-ai-boxghost`; a scratchpad or a conversation is neither.

```text
CANONICAL_REGLAS_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md
```

## Storage

Canonical baseline documents live under:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/
```

Each Owner-accepted committed STEP that establishes meaningful reusable verification SHOULD create:

```text
GYPPORT_<STEP>_VERIFIED_BASELINE_<YYYY-MM-DD>.md
```

The registry of baselines is the set of registration entries in
`Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md` together with the documents in this directory.

## Automatic generation rule

After a controlled commit gate returns:

```text
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
```

the closing agent must automatically prepare or update the STEP's Verified Baseline document
BEFORE proposing the next implementation package.

The agent must NOT automatically start the next package.

Closeout contract:

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

This contract extends, without replacing, `ONE STEP → VERIFY → OWNER REVIEW → CONTROLLED COMMIT →
NEXT STEP`: it adds the steps that follow the commit. Generating and registering a baseline
approves nothing, commits nothing, pushes nothing, runs no tests and starts no STEP.

The tool is `Fabric/tools/verification/New-GypportVerifiedBaseline.ps1`, in mode
`GENERATE_ONLY`; see `GYPPORT_VERIFIED_BASELINE_AUTOMATION.md`.

## Reglas.md registration

`Reglas.md` remains append-only. It exists only as
`Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md`; no other copy is writable, and the former
`Gystigo/Reglas.md` pointer was removed on 2026-09-15.

Each new verified baseline should append a compact registration entry containing:

```text
date
baseline id
STEP
accepted commit SHAs
migration head
location of baseline document
reuse status
```

The entry follows the log's own style: a dated heading, two lines of prose and one text block.

````text
<YYYY-MM-DD> — GYPPORT® Universe / Registro de Verified Baseline <SUBJECT>

Verified Baseline de un STEP aceptado por el Owner y committed localmente.
Se reutiliza según VERIFIED_BASELINE_REUSE.

```text
BASELINE_ID=<baseline id>
BASELINE_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/<document>
STEP=<step>
PHASE=<phase>
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
ACCEPTED_COMMITS=<repository>=<sha>; <repository>=<sha>
MIGRATION_HEAD=<migration head>
VERIFIED_FILE_COUNT=<count>
BASELINE_REUSE_ALLOWED=YES
```
````

A baseline whose `BASELINE_ID=` line is already present is never registered twice.

Do not rewrite or renumber historical rules.

## Safety against stale evidence

A baseline can be reused only after checking current repository ancestry and relevant impact.

Never assume:

```text
"commit exists" == "baseline is automatically valid"
```

The current STEP must still perform impact analysis:

```text
1. DISCOVER    list Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/ and search
               Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md for the BASELINE_ID=
               registrations of the affected area
2. ANCESTRY    git -C <repository> merge-base --is-ancestor <accepted commit> HEAD,
               for every accepted commit
3. PATHS       git -C <repository> diff --name-only <accepted commit> HEAD, compared with
               the baseline manifest and its invalidation triggers
4. MIGRATIONS  migrations after the baseline migration head that touch its tables or semantics
5. DECISIONS   Owner decisions or ADRs newer than the baseline that change its invariants
6. DECIDE      REUSE | PARTIAL_INVALIDATION | FULL_INVALIDATION, with the reason
```

If an accepted commit is no longer an ancestor, for example after a rebase or squash, compare the
blob ids of the baseline manifest with the current tree before declaring an invalidation.

## Agent output example

```text
VERIFIED_BASELINE_CHECK

BASELINE_FOUND=YES
BASELINE_ID=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15
ACCEPTED_COMMITS_PRESENT=YES
RELEVANT_CONTRACT_DRIFT=NO
MIGRATION_SEMANTICS_DRIFT=NO
OWNER_DECISION_DRIFT=NO

BASELINE_REUSE_DECISION=REUSE
BASELINE_REUSE_REASON=accepted commits are ancestors of HEAD; no PKG-2C path, V57/V58 semantics or Owner decision changed
FULL_HISTORICAL_REGRESSION_RERUN=NO

CURRENT_STEP_VERIFICATION=
- current module tests
- selected impact suites
- Host integration smoke
```

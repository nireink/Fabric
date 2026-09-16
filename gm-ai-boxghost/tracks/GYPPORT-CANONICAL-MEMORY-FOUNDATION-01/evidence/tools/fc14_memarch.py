# -*- coding: utf-8 -*-
"""Final form of GYPPORT_MEMORY_ARCHITECTURE.md: logical storage role, location registry,
availability contract, Google Drive decision, CURRENT_STEP and the closeout lifecycle."""
import os

U = os.path.join("D:" + os.sep, "NZXTG7", "GYPPORT", "GYPPORT ERP", "GYPPORT", "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE")
P = os.path.join(U, "GYPPORT_MEMORY_ARCHITECTURE.md")
text = open(P, encoding="utf-8").read()
original = text

lines = text.split("\n")
hit = [i for i, l in enumerate(lines) if l.startswith("RAW_PERSISTENT_STORAGE_ROOT=")]
assert len(hit) == 1, hit
lines[hit[0]:hit[0] + 1] = ["GYPPORT_STORAGE_ID=GYPPORT_STORAGE",
                            "GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties",
                            "ACTIVE_WORK_ROOT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work"]
text = "\n".join(lines)

PAIRS = [
("| `GYPPORT-Storage` | raw, original and heavy sources | what GYPPORT was given or collected |",
 "| `GYPPORT_STORAGE` (logical role) | raw, original and heavy sources | what GYPPORT was given or collected |"),

("| `Gystigo` | product | the Host and its own technical documentation |",
 "| `Gystigo` | product | the Host and its own technical documentation |\n| `active-work/CURRENT_STEP.md` | the active work pointer | what GYPPORT is working on now |"),

("""Paths are relative to the GYPPORT workspace root, the directory that contains `Gystigo/`,
`Fabric/` and `Modules/`. `GYPPORT-Storage` is a sibling of that root.""",
 """Paths are relative to the GYPPORT workspace root, the directory that contains `Gystigo/`,
`Fabric/` and `Modules/`. `GYPPORT_STORAGE` is a logical role, never a hardcoded path: its physical
root is resolved through the location registry (section 2.3.1)."""),

("### 2.3 `GYPPORT-Storage` — raw persistent storage",
 "### 2.3 `GYPPORT_STORAGE` — raw persistent storage (logical role)"),

("""```text
GYPPORT_STORAGE_IS_CANONICAL_KNOWLEDGE=NO
GYPPORT_STORAGE_IS_OPERATIONAL_MEMORY=NO
GYPPORT_STORAGE_IS_A_SECOND_MEMORY_ROOT=NO
GYPPORT_STORAGE_DUPLICATE_CANONICAL_ROLE=NO
```""",
 """```text
GYPPORT_STORAGE_IS_CANONICAL_KNOWLEDGE=NO
GYPPORT_STORAGE_IS_OPERATIONAL_MEMORY=NO
GYPPORT_STORAGE_IS_A_SECOND_MEMORY_ROOT=NO
GYPPORT_STORAGE_DUPLICATE_CANONICAL_ROLE=NO
GYPPORT_STORAGE_GOOGLE_DRIVE_SYNC=DISABLED
GOOGLE_DRIVE_IS_GYPPORT_STORAGE_BACKEND=NO
GOOGLE_DRIVE_IS_GYPPORT_BACKUP=NO
GOOGLE_DRIVE_IS_PART_OF_GYPPORT_MEMORY_ARCHITECTURE=NO
```"""),

("""Nothing in `GYPPORT-Storage` is canonical or authoritative, whatever a file there is named.
Canonical Fabric documents are not copied into it. Dated backups and superseded versions may be
archived there, and they are history, never the live document.""",
 """Nothing in `GYPPORT_STORAGE` is canonical or authoritative, whatever a file there is named.
Canonical Fabric documents are not copied into it. Dated backups and superseded versions may be
archived there, and they are history, never the live document.

Its areas are `External/` (raw external collections), `Fabric/` and `Gystigo/` (raw sources, dated
backups, inventory and recovery packages), `IAs Agents/` (archived AI project bases) and
`Restricted/` (sensitive archives).

### 2.3.1 Physical location and availability

The logical role is permanent; the physical location is configuration. One registry holds it:

```text
GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties
KEY=GYPPORT_STORAGE_ROOT
STORAGE_LOCATION_SINGLE_SOURCE=YES
FUTURE_NAS_MOVE_REQUIRES_ARCHITECTURE_CHANGE=NO
```

Every agent and tool resolves the root before reading or writing raw material:

```text
resolve(GYPPORT_STORAGE) -> GYPPORT_LOCATIONS.properties -> GYPPORT_STORAGE_ROOT
```

If the resolved root does not exist or is unavailable:

```text
GYPPORT_STORAGE_AVAILABLE=NO
-> STOP and report STORAGE UNAVAILABLE
STORAGE_UNAVAILABLE_FALLBACK_CREATION=NO
```

It never creates a replacement storage root, never falls back to a temporary folder, the Desktop or
Downloads, and never edits the registry without Owner-approved intent.

Moving the library to a NAS is a configuration migration: update `GYPPORT_STORAGE_ROOT`, validate
the new root, continue. Prefer a stable UNC path over a machine-dependent mapped drive letter. No
governance, memory, BoxGhost, CURRENT_STEP or Brain document changes.

Storage and backup are separate concerns:

```text
PRIMARY_STORAGE_LOCATION != BACKUP_MECHANISM
```

Google Drive is outside this architecture: it is not the storage backend, not the backup, and not a
sync, availability or lock-management dependency. A future backup may use NAS snapshots, a second
NAS or an encrypted external copy without changing the information model.

### 2.3.2 Restricted source material

A raw source that carries credentials or other secrets is classified `SENSITIVE_ARCHIVE` and kept
under `Restricted/` inside the resolved root, never copied into canonical knowledge:

```text
RESTRICTED_SOURCE_AUTOMATIC_CONTEXT_INGESTION=NO
RESTRICTED_SOURCE_SECRET_QUOTING=NO
RESTRICTED_SOURCE_AUTOMATIC_EXTERNAL_SYNC=NO
RESTRICTED_SOURCE_AUTO_UPLOAD=NO
```

Only safe metadata is recorded: path, size, hash and classification. A future Brain may index the
fact that a restricted artifact exists; it must not read secret-bearing content into agent
context."""),
]

for old, new in PAIRS:
    assert text.count(old) == 1, "expected one occurrence of: %r" % old[:80]
    text = text.replace(old, new)

INDEX_HEADING = "## 6. Canonical index"
assert text.count(INDEX_HEADING) == 1
NEW_SECTION = """## 5.1 CURRENT_STEP — the active work pointer

```text
ONE_GLOBAL_CURRENT_STEP=YES
CURRENT_STEP_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md
```

CURRENT_STEP names the track, the STEP, its mode, its status, the prompt source to read in full and
the verified baselines to reuse. It is a continuity pointer: not canonical knowledge, not a prompt
copy, not a transcript, not a replacement for BoxGhost, not an approval and not an execution
trigger. Execution requires `OWNER_EXECUTION_AUTHORIZED=YES` or a current explicit Owner
instruction. Repository and schema evidence outrank it; a disagreement is reported, never guessed.

For the MVP period there is exactly one global CURRENT_STEP. Per-module variants require an
explicit Owner decision.

## 5.2 Closeout lifecycle

```text
IMPLEMENT
-> VERIFY
-> OWNER REVIEW
-> CONTROLLED COMMIT
-> POST-COMMIT SMOKE
-> GENERATE VERIFIED BASELINE
-> REGISTER VERIFIED BASELINE
-> PREPARE/UPDATE CURRENT_STEP
-> OWNER REVIEW
-> NEXT STEP

AUTO_BASELINE_GENERATION=YES
AUTO_BASELINE_REGISTRATION=YES
AUTO_CURRENT_STEP_PREPARATION=YES

AUTO_OWNER_APPROVAL=NO
AUTO_IMPLEMENT_NEXT_STEP=NO
AUTO_PUSH=NO
```

Automatic means the closing workflow materializes the canonical files, so the Owner never
reconstructs them by hand. It never means automatic execution: a freshly prepared CURRENT_STEP
defaults to `OWNER_EXECUTION_AUTHORIZED=NO`. The materializer lives in `Fabric/tools/continuity/`
and only validates and writes that file.

"""
text = text.replace(INDEX_HEADING, NEW_SECTION + INDEX_HEADING)

OLD_INDEX = """├── Reglas.md                        the canonical, append-only rules log (only writable copy)
├── GYPPORT_MEMORY_ARCHITECTURE.md   this document"""
NEW_INDEX = """├── Reglas.md                        the canonical, append-only rules log (only writable copy)
├── GYPPORT_MEMORY_ARCHITECTURE.md   this document
├── GYPPORT_LOCATIONS.properties     the physical location registry (GYPPORT_STORAGE_ROOT)
├── active-work/CURRENT_STEP.md      the single global pointer to the work that is active now"""
assert text.count(OLD_INDEX) == 1
text = text.replace(OLD_INDEX, NEW_INDEX)

OLD_ROW = "| provider caches and sessions | `~/.claude/projects`, `~/.codex/sessions`: provider cache, not GYPPORT memory |"
NEW_ROW = OLD_ROW + "\n| Google Drive | not the storage backend, not the backup, not part of this architecture |"
assert text.count(OLD_ROW) == 1
text = text.replace(OLD_ROW, NEW_ROW)

open(P, "w", encoding="utf-8", newline="\n").write(text)
print("UPDATED GYPPORT_MEMORY_ARCHITECTURE.md %d -> %d bytes" % (len(original), len(text)))
print("hardcoded storage path still present:", "NZXTG7" in text)

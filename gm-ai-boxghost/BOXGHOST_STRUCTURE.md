# BoxGhost — structure and ownership

```text
BOXGHOST_ROLE=PERMANENT_OPERATIONAL_MEMORY
BOXGHOST_ROOT=Fabric/gm-ai-boxghost
SECOND_BOXGHOST_ROOT=0
CANONICAL_KNOWLEDGE=Fabric/Knowledge
RAW_HEAVY_STORAGE=GYPPORT_STORAGE (logical role; resolve through GYPPORT_LOCATIONS.properties)
MEMORY_ARCHITECTURE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md
```

BoxGhost is the single operational memory of GYPPORT: everything that happened, kept so that it
stays reconstructable. There is one BoxGhost root; no second root is created anywhere.

## 1. What belongs here

Full conversations; sessions and captures; durable prompts and responses; interventions; handoffs;
execution reports; Owner review packets; operational decisions; approvals; evidence; audits;
continuity packets; context history; generated operational artifacts; raw AI collaboration
history; track state.

## 2. What does not belong here

- Canonical knowledge: architecture, ADRs, rules, standards, agent and collaboration governance,
  verified baselines and Owner-approved derived knowledge live in `Fabric/Knowledge`.
- Raw, original and heavy sources: books, PDFs, dumps, datasets, exports and binary evidence live
  in `GYPPORT_STORAGE`, resolved through
  `Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties`; BoxGhost references them by
  logical path instead of copying them.
- Product code, migrations, tests and product documentation: they live in `Gystigo` and in each
  module.
- Secrets. A file that carries a credential is not imported; see
  `tracks/GM-IA-COLLABORATION-WORKSPACE-01/interventions/chatgpt-work/05-handoff-verifiable/SENSITIVITY_AND_SECRET_HANDLING_POLICY.md`.

## 3. Layout

```text
gm-ai-boxghost/
├── BOXGHOST_STRUCTURE.md        this document
├── tracks/
│   └── <TRACK-ID>/
│       ├── TRACK_STATE.md       lifecycle state (reader contract; optional for imported history)
│       ├── SCOPE.md
│       ├── CONTEXT_PACK.md      derived and regenerable
│       ├── SOURCE_MANIFEST.json paths, hashes and sensitivity of the track files
│       ├── dialog/              conversations, including events.jsonl
│       ├── captures/            provider sessions, by provider and session id
│       ├── interventions/       one folder per agent: prompts, requests and responses
│       ├── handoffs/            handoff packages, by direction (for example codex-to-review/)
│       ├── decisions/
│       ├── approvals/
│       ├── evidence/            verification and execution evidence
│       ├── audits/              independent reviews, by status (for example accepted/)
│       ├── continuity/
│       ├── artifacts/           generated operational artifacts; retired/ for artifacts a STEP retires
│       ├── attachments/
│       ├── working-files/
│       ├── scope-versions/
│       └── exports/
├── imports/
│   └── <IMPORT-ID>/             material imported without a declared track, source path preserved
├── objects/sha256/              content-addressed objects
├── archive/                     archived legacy workspaces
├── backups/
├── global/                      workspace-wide operational context, when it exists
└── projects/                    per-project operational context, when it exists
```

A folder is created when there is content for it. An empty folder means nothing.

The Owner's artifact types map onto these names: `conversations` are `dialog/`, `sessions` are
`captures/`, and everything else keeps its own name. Only one tree exists per type.

## 4. Track identifiers

```text
TRACK_ID_PATTERN=^[A-Z0-9][A-Z0-9-]{2,99}$
```

A track folder uses the track's declared id. A legacy artifact that declares a track name instead
of an id uses the uppercase-hyphenated form of that name (`Dashboard Engine` becomes
`DASHBOARD-ENGINE`, `GYPPORT_EXPENSES_UIX_COMPLIANCE` becomes `GYPPORT-EXPENSES-UIX-COMPLIANCE`).
An artifact that declares no track is imported under `imports/<IMPORT-ID>/` with its original
relative path, so nothing is attributed to a track it never declared.

## 5. Rules

```text
RAW_OPERATIONAL_MEMORY_MUST_NOT_BE_REPLACED_BY_SUMMARY=YES
SUMMARIES_ARE_DERIVED=YES
SUMMARIES_MUST_REFERENCE_SOURCE=YES
CONTEXT_PACKS_ARE_REGENERABLE=YES
IMPORTED_CONTENT_IS_BYTE_EXACT=YES
```

- Imported history keeps its bytes; the migration that brought it records the source path and both
  hashes.
- Heavy or binary evidence stays in `GYPPORT_STORAGE` and is referenced from the track.
- An index or projection over BoxGhost is disposable and rebuildable; a divergence invalidates the
  index, never the source.

## 6. Readers

`Modules/gm-ai-workspace` reads this root, validates structure, references, hashes and path safety,
and never writes to it. Its first read-only slice and the detailed reader contract — the
`TRACK_STATE.md` front matter, the `SOURCE_MANIFEST.json` schema, dialog events, reference findings
and read limits — were specified in
`tracks/GM-IA-COLLABORATION-WORKSPACE-01/interventions/chatgpt-work/05-handoff-verifiable/BOXGHOST_STRUCTURE.md`
on the unmerged Fabric branch `docs/gm-ai-workspace-canonical-unification-01` (d43b4fd). That
specification keeps the folder names used here; this document is the structure and ownership rule,
and it does not restate the reader contract.

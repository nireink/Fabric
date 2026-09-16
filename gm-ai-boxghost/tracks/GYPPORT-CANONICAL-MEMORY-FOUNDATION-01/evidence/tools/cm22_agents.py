# -*- coding: utf-8 -*-
"""Build the canonical GYPPORT agent governance files and the two Gystigo technical entrypoints.

The four canonical files are assembled from the current Gystigo agent files, so every governance
sentence is preserved byte-for-byte; the shared body is written once, in AGENTS.md.
"""
import hashlib
import os
import sys

W = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
G = os.path.join(W, "Gystigo")
AG = os.path.join(W, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE", "agents")
NAMES = ["AGENTS", "CLAUDE", "CHATGPT", "CODEX"]
SHARED = ["GYPPORT Universe — Mandatory Knowledge Gate", "Working Governance", "Canonical Domain Boundaries",
          "UIX Baseline", "Mandatory Architecture Gate", "Mandatory Conflict Gate",
          "Audit / Provenance Granularity Protection", "Continuity Packet"]

ROOTS = u"""## GYPPORT Memory Roots and Artifact Placement

Fabric is the single GYPPORT memory root. The full contract is
`Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md`.

```text
FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT=YES
CANONICAL_KNOWLEDGE_ROOT=Fabric/Knowledge
OPERATIONAL_MEMORY_ROOT=Fabric/gm-ai-boxghost
RAW_PERSISTENT_STORAGE_ROOT=D:\\NZXTG7\\GYPPORT\\GYPPORT ERP\\GYPPORT-Storage
PRODUCT_HOST_ROOT=Gystigo
MODULE_ROOT=Modules
GM_AI_WORKSPACE_ROOT=Modules/gm-ai-workspace
```

Paths are relative to the GYPPORT workspace root, the directory that contains `Gystigo/`,
`Fabric/` and `Modules/`. `GYPPORT-Storage` is a sibling of that root.

Placement rules:

```text
DO_NOT_CREATE_CANONICAL_KNOWLEDGE_IN_TEMP
DO_NOT_CREATE_OPERATIONAL_HISTORY_IN_ARBITRARY_PRODUCT_DOCS
PROMOTE_VALUABLE_TEMP_ARTIFACTS_BEFORE_STEP_CLOSE
RAW_SOURCE_TO_GYPPORT_STORAGE
DERIVED_CANONICAL_KNOWLEDGE_TO_FABRIC_KNOWLEDGE
OPERATIONAL_EXECUTION_HISTORY_TO_BOXGHOST
```

- Create every new durable GYPPORT artifact directly in its canonical owner path.
- What GYPPORT knows, once it is canonical, belongs to `Fabric/Knowledge`.
- What happened — conversations, sessions, prompts, interventions, handoffs, decisions, approvals,
  evidence, audits and continuity — belongs to `Fabric/gm-ai-boxghost`; see its
  `BOXGHOST_STRUCTURE.md`.
- Raw, original and heavy sources belong to `GYPPORT-Storage`. Nothing there is canonical knowledge
  or operational memory, whatever a file there is named.
- Scratchpads, `AppData\\Local\\Temp`, Codex temporary folders, provider caches, provider
  compaction, the Desktop and Downloads are never durable GYPPORT memory. Promote anything valuable
  before the STEP closes.
- Copies of governance files in git worktrees, `UI_Experiments/`, `GYPPORT-Storage` or the legacy
  `Governance/` repository are historical and never authoritative.
"""

LOCATION_NOTE = {
    "AGENTS": u"""Canonical location: `Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/AGENTS.md`. The agent-specific files
`CLAUDE.md`, `CHATGPT.md` and `CODEX.md` live next to it and require this file. The shared governance
below exists only here. `Gystigo/AGENTS.md` and `Gystigo/CLAUDE.md` are technical entrypoints that
carry no governance text.
""",
    "CLAUDE": u"""@AGENTS.md

## Shared Governance

`AGENTS.md` in this folder is mandatory for Claude and is imported above. It holds the Mandatory
Knowledge Gate, Working Governance, Canonical Domain Boundaries, UIX Baseline, Architecture Gate,
Conflict Gate, Audit / Provenance protection and the Continuity Packet. This file adds only the
Claude-specific rules. `Gystigo/CLAUDE.md` is a technical entrypoint that imports this file.
""",
    "CHATGPT": u"""## Shared Governance

`AGENTS.md` in this folder is mandatory for ChatGPT, and ChatGPT cannot discover it: it has no
filesystem access. Every GYPPORT ChatGPT project or conversation must receive both `AGENTS.md` and
`CHATGPT.md` from this folder; if `AGENTS.md` is not in the context, request it before any GYPPORT
work. `AGENTS.md` holds the Mandatory Knowledge Gate, Working Governance, Canonical Domain
Boundaries, UIX Baseline, Architecture Gate, Conflict Gate, Audit / Provenance protection and the
Continuity Packet. This file adds only the ChatGPT-specific rules.
""",
    "CODEX": u"""## Shared Governance

`AGENTS.md` in this folder is mandatory for Codex. Codex discovers `Gystigo/AGENTS.md`, which is a
technical entrypoint: it points here. Read `AGENTS.md` and this file in full before any work.
`AGENTS.md` holds the Mandatory Knowledge Gate, Working Governance, Canonical Domain Boundaries,
UIX Baseline, Architecture Gate, Conflict Gate, Audit / Provenance protection and the Continuity
Packet. This file adds only the Codex-specific rules.
""",
}

ENTRY_AGENTS = u"""# AGENTS.md — GYPPORT® Agent Entrypoint (Gystigo)

This file is a permanent technical entrypoint. GYPPORT agent governance does not live here and must
not be copied here.

Before any work in this repository, read in full:

1. `../Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/AGENTS.md` — shared governance for every agent.
2. The agent-specific file in the same folder: `CODEX.md`, `CLAUDE.md` or `CHATGPT.md`.
3. `../Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md` — the canonical append-only rules log.
4. `../Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md` — where every durable
   GYPPORT artifact belongs.

```text
CANONICAL_KNOWLEDGE_ROOT=Fabric/Knowledge
OPERATIONAL_MEMORY_ROOT=Fabric/gm-ai-boxghost
RAW_PERSISTENT_STORAGE_ROOT=D:\\NZXTG7\\GYPPORT\\GYPPORT ERP\\GYPPORT-Storage
PRODUCT_HOST_ROOT=Gystigo
MODULE_ROOT=Modules
GM_AI_WORKSPACE_ROOT=Modules/gm-ai-workspace
```

## Why this file exists here

- Codex reads `AGENTS.md` from the project root down to the working directory; it does not read
  `CODEX.md`, and no fallback filename is configured.
- The Gystigo Toolchain uses this file as its project-root marker:
  `developer_platform/toolchain/tool/core/path/ToolProjectRootResolver.mjs` requires `AGENTS.md`
  next to `developer_platform/` and `platform_os/`. Do not delete, rename or move it.

Keep this file short. Change governance only in Fabric.
"""

ENTRY_CLAUDE = u"""# CLAUDE.md — GYPPORT® Claude Entrypoint (Gystigo)

This file is a permanent technical entrypoint: Claude Code reads `CLAUDE.md`, never `AGENTS.md`.
GYPPORT governance lives in Fabric and is imported here:

@../Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/CLAUDE.md

That file imports `AGENTS.md` from the same Fabric folder. If the imports are not loaded — for
example in a session started inside `Gystigo/` where external imports were declined — read both
files in full before any work:

- `../Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/AGENTS.md`
- `../Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/CLAUDE.md`

The canonical append-only rules log is
`../Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md`, and where every durable GYPPORT artifact
belongs is defined in `../Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md`.

Keep this file short. Change governance only in Fabric.
"""


def sections(text):
    out, cur, buf = [], "(preamble)", []
    for line in text.splitlines():
        if line.startswith("## "):
            out.append((cur, "\n".join(buf).strip("\n")))
            cur, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out.append((cur, "\n".join(buf).strip("\n")))
    return out


def main():
    BK = os.path.join(r"C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP",
                      "8142c294-1815-45b4-90ee-94d1198faa7d", "scratchpad", "cm_backup", "GYPPORT", "Gystigo")

    def read_agent(name):
        # the pre-migration originals; the backup copy is authoritative once the migration has run
        path = os.path.join(BK, name + ".md")
        if not os.path.isfile(path):
            path = os.path.join(G, name + ".md")
        print("SOURCE %s" % path)
        return open(path, "rb").read().decode("utf-8")

    src = {n: read_agent(n) for n in NAMES}
    sec = {n: sections(src[n]) for n in NAMES}
    body = {}
    for title in SHARED:
        bodies = {hashlib.sha256(dict(sec[n])[title].encode()).hexdigest() for n in NAMES}
        assert len(bodies) == 1, "shared section differs between agent files: " + title
        body[title] = dict(sec["AGENTS"])[title]

    out = {}
    for n in NAMES:
        parts = []
        for title, text in sec[n]:
            if title == "(preamble)":
                parts.append(text.rstrip("\n") + "\n\n" + LOCATION_NOTE[n].rstrip("\n") + "\n\n" + ROOTS.rstrip("\n"))
            elif title in SHARED:
                if n == "AGENTS":
                    parts.append("## " + title + "\n\n" + text.rstrip("\n"))
            else:
                parts.append("## " + title + "\n\n" + text.rstrip("\n"))
        out[n] = "\n\n\n".join(parts) + "\n"

    missing = {}
    for n in NAMES:
        joined = "\n".join(out[x] for x in NAMES)
        miss = [l for l in src[n].splitlines() if l.strip() and l not in joined.splitlines()]
        if miss:
            missing[n] = miss
    if missing:
        for n, m in missing.items():
            print("CONTENT_LOSS in", n, len(m))
            for l in m[:10]:
                print("   ", l[:120])
        raise SystemExit("content loss detected")

    if "--write" in sys.argv:
        os.makedirs(AG, exist_ok=True)
        for n in NAMES:
            p = os.path.join(AG, n + ".md")
            open(p, "w", encoding="utf-8", newline="\n").write(out[n])
            print("WROTE %s %d bytes sha=%s" % (p, os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]))
        for name, text in (("AGENTS", ENTRY_AGENTS), ("CLAUDE", ENTRY_CLAUDE)):
            p = os.path.join(G, name + ".md")
            open(p, "w", encoding="utf-8", newline="\n").write(text)
            print("WROTE %s %d bytes sha=%s" % (p, os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]))
    else:
        for n in NAMES:
            print("%s.md -> %d lines, %d bytes (dry run)" % (n, len(out[n].splitlines()), len(out[n].encode("utf-8"))))
        print("CONTENT_LOSS=0 (every non-empty line of the four Gystigo agent files appears in the canonical set)")
        print("no '@' import outside the intended one:",
              sum(l.startswith("@") for n in NAMES for l in out[n].splitlines()))


if __name__ == "__main__":
    main()

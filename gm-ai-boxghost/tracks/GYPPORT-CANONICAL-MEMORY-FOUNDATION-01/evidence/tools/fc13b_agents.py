# -*- coding: utf-8 -*-
"""Logical-storage indirection, startup discovery and artifact routing for the canonical agent
governance, the two Gystigo entrypoints and the BoxGhost structure document.
The token ~T~ stands for a backtick (the shell heredoc cannot carry one)."""
import os

BT = chr(96)
def bt(s):
    return s.replace("~T~", BT)

W = os.path.join("D:" + os.sep, "NZXTG7", "GYPPORT", "GYPPORT ERP", "GYPPORT")
U = os.path.join(W, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE")
AG = os.path.join(U, "agents")
G = os.path.join(W, "Gystigo")
BG = os.path.join(W, "Fabric", "gm-ai-boxghost")

ROOTS_NEW = ["GYPPORT_STORAGE_ID=GYPPORT_STORAGE",
             "GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties",
             "ACTIVE_WORK_ROOT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work"]

SIBLING_OLD = bt("~T~GYPPORT-Storage~T~ is a sibling of that root.")
SIBLING_NEW = bt("~T~GYPPORT_STORAGE~T~ is a logical role, not a path: resolve its physical root through\nthe location registry above and never hardcode it.")

RAW_BULLET_OLD = bt("""- Raw, original and heavy sources belong to ~T~GYPPORT-Storage~T~. Nothing there is canonical knowledge
  or operational memory, whatever a file there is named.""")
RAW_BULLET_NEW = bt("""- Raw, original and heavy sources belong to ~T~GYPPORT_STORAGE~T~, resolved through the location
  registry. Nothing there is canonical knowledge or operational memory, whatever a file there is
  named. If the resolved root is missing, report ~T~GYPPORT_STORAGE_AVAILABLE=NO~T~ and stop: never
  create a replacement root, and never fall back to a temporary folder, the Desktop or Downloads.""")

ANCHOR_OLD = bt("- Copies of governance files in git worktrees, ~T~UI_Experiments/~T~, ~T~GYPPORT-Storage~T~ or the legacy\n  ~T~Governance/~T~ repository are historical and never authoritative.")
ANCHOR_NEW = bt("- Copies of governance files in git worktrees, ~T~UI_Experiments/~T~, ~T~GYPPORT_STORAGE~T~ or the legacy\n  ~T~Governance/~T~ repository are historical and never authoritative.")

FENCE = chr(96) * 3
EXTRA = bt("""

## Startup Discovery

Every GYPPORT agent starts here, in this order:

FENCEtext
1. CURRENT_STEP        Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md
2. RULES               Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md
3. AGENT GOVERNANCE    Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/ (AGENTS.md and this file)
4. LOCATIONS           Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties
                       when external raw storage is involved
5. PROMPT_SOURCE       resolve it from CURRENT_STEP and read it completely
6. REQUIRED_BASELINES  resolve the ids under verification-baselines/ and apply
                       VERIFIED_BASELINE_REUSE.md before any historical regression
7. ACT                 only on the current Owner-authorized action
FENCE

- ~T~STATUS=READY_TO_START~T~ is not permission. Execution requires ~T~OWNER_EXECUTION_AUTHORIZED=YES~T~
  in CURRENT_STEP, or a current explicit Owner instruction authorizing that STEP.
- Never restart an Owner-accepted completed STEP.
- Do not choose a full baseline invalidation to be safe; apply the reuse policy.
- Repository, schema and test evidence outrank a continuity file. If they disagree, stop and report
  the discrepancy; never guess.

## Artifact Routing

Classify a durable artifact before creating it, then route it:

FENCEtext
CANONICAL_KNOWLEDGE                  -> Fabric/Knowledge
  architecture, ADRs, rules, standards, verified baselines, Owner-approved derived knowledge,
  canonical agent and collaboration governance

OPERATIONAL_MEMORY                   -> Fabric/gm-ai-boxghost
  conversations, sessions, interventions, handoffs, execution reports, continuity, audit evidence,
  operational decisions, track and context history, Owner review evidence

RAW_HEAVY_ORIGINAL_SOURCE            -> resolve(GYPPORT_STORAGE)
  books, PDFs, datasets, database dumps, source archives, external reference collections, raw
  research, large exports, original binaries

PRODUCT_CODE_OR_PRODUCT_SPECIFIC_DOC -> the owning repository or module

TEMPORARY_DISPOSABLE_WORK            -> a scratchpad is allowed, but
                                        VALUABLE_TEMP_ONLY_ARTIFACTS_AT_STEP_CLOSE=0
FENCE

If a temporary artifact turns out to be valuable, promote it before the STEP closes: knowledge to
~T~Fabric/Knowledge~T~, history and evidence to ~T~Fabric/gm-ai-boxghost~T~, raw sources to
resolve(GYPPORT_STORAGE). The only durable copy of anything valuable never stays in a temporary
folder, a provider cache, the Desktop or Downloads.""").replace("FENCE", FENCE)

changed = []


def edit(path, pairs, line_prefix_replace=None):
    text = open(path, encoding="utf-8").read()
    original = text
    if line_prefix_replace:
        prefix, newlines = line_prefix_replace
        lines = text.split("\n")
        hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
        assert len(hits) == 1, "%s: expected 1 line with prefix %s, found %d" % (path, prefix, len(hits))
        lines[hits[0]:hits[0] + 1] = newlines
        text = "\n".join(lines)
    for old, new in pairs:
        assert text.count(old) == 1, "%s: expected one occurrence of %r" % (path, old[:70])
        text = text.replace(old, new)
    if text != original:
        open(path, "w", encoding="utf-8", newline="\n").write(text)
        changed.append((os.path.relpath(path, W), len(original), len(text)))


for name in ("AGENTS", "CLAUDE", "CHATGPT", "CODEX"):
    edit(os.path.join(AG, name + ".md"),
         [(SIBLING_OLD, SIBLING_NEW), (RAW_BULLET_OLD, RAW_BULLET_NEW), (ANCHOR_OLD, ANCHOR_NEW + EXTRA)],
         ("RAW_PERSISTENT_STORAGE_ROOT=", ROOTS_NEW))

edit(os.path.join(G, "AGENTS.md"),
     [(bt("""1. ~T~../Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/AGENTS.md~T~ - shared governance for every agent.""").replace(" - ", " — "),
       bt("""1. ~T~../Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md~T~ — the work that is
   active now, with its prompt source and required baselines.
2. ~T~../Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/AGENTS.md~T~ — shared governance for every agent."""))],
     None)

edit(os.path.join(G, "CLAUDE.md"),
     [(bt("""The canonical append-only rules log is"""),
       bt("""Start from ~T~../Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md~T~, the single
pointer to the work that is active now. The canonical append-only rules log is"""))])

edit(os.path.join(BG, "BOXGHOST_STRUCTURE.md"),
     [(bt("""- Raw, original and heavy sources: books, PDFs, dumps, datasets, exports and binary evidence live
  in ~T~GYPPORT-Storage~T~; BoxGhost references them by path instead of copying them."""),
       bt("""- Raw, original and heavy sources: books, PDFs, dumps, datasets, exports and binary evidence live
  in ~T~GYPPORT_STORAGE~T~, resolved through
  ~T~Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties~T~; BoxGhost references them by
  logical path instead of copying them.""")),
      (bt("- Heavy or binary evidence stays in ~T~GYPPORT-Storage~T~ and is referenced from the track."),
       bt("- Heavy or binary evidence stays in ~T~GYPPORT_STORAGE~T~ and is referenced from the track."))],
     ("RAW_HEAVY_STORAGE=", ["RAW_HEAVY_STORAGE=GYPPORT_STORAGE (logical role; resolve through GYPPORT_LOCATIONS.properties)"]))

for rel, a, b in changed:
    print("UPDATED %-56s %d -> %d bytes" % (rel, a, b))
print("FILES_UPDATED=%d" % len(changed))

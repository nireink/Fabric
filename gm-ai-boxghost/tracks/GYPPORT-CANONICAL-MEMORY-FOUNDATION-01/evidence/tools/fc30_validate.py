# -*- coding: utf-8 -*-
"""Completion validation: discovery chain, obsolete active architecture claims, references, tree."""
import os, re

BT = chr(96)
W = os.path.join("D:" + os.sep, "NZXTG7", "GYPPORT", "GYPPORT ERP", "GYPPORT")
U = os.path.join(W, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE")
AG = os.path.join(U, "agents")
G = os.path.join(W, "Gystigo")
rd = lambda p: open(p, encoding="utf-8", errors="replace").read()
res = []
def check(name, ok, detail=""):
    res.append((name, "PASS" if ok else "FAIL", detail))

print("##### 1. discovery chain, end to end")
entry_a = rd(os.path.join(G, "AGENTS.md"))
entry_c = rd(os.path.join(G, "CLAUDE.md"))
# every ../Fabric path named by the two entrypoints must resolve
refs = set(re.findall(r"\.\./Fabric/[A-Za-z0-9_./\-]+", entry_a + entry_c))
missing = [r for r in refs if not os.path.exists(os.path.join(G, r.replace("/", os.sep)))]
check("ENTRYPOINT_REFERENCES_RESOLVE", not missing, "%d refs, missing %s" % (len(refs), missing))
check("CLAUDE_ENTRYPOINT_IMPORTS_CANONICAL", "@../Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/CLAUDE.md" in entry_c)
canon_claude = rd(os.path.join(AG, "CLAUDE.md"))
check("CANONICAL_CLAUDE_IMPORTS_AGENTS", canon_claude.lstrip().count("@AGENTS.md") >= 1 and os.path.isfile(os.path.join(AG, "AGENTS.md")))
agents_txt = rd(os.path.join(AG, "AGENTS.md"))
cs_path = os.path.join(U, "active-work", "CURRENT_STEP.md")
check("CURRENT_STEP_RESOLUTION_TEST", os.path.isfile(cs_path) and "active-work/CURRENT_STEP.md" in agents_txt, cs_path)
cs = rd(cs_path)
kv = dict(re.findall(r"^([A-Z_]+)=(.*)$", cs, re.M))
prompt = os.path.join(W, kv.get("PROMPT_SOURCE", "").replace("/", os.sep))
check("PROMPT_SOURCE_RESOLUTION_TEST", os.path.isfile(prompt), kv.get("PROMPT_SOURCE", ""))
bl_dir = os.path.join(U, "verification-baselines")
ids = {}
for f in os.listdir(bl_dir):
    if f.endswith(".md"):
        for line in rd(os.path.join(bl_dir, f)).splitlines():
            m = re.match(r"^\s*BASELINE_ID\s*=\s*(\S+)\s*$", line)
            if m and "<" not in m.group(1) and f not in ("VERIFIED_BASELINE_REUSE.md", "GYPPORT_VERIFIED_BASELINE_AUTOMATION.md"):
                ids[m.group(1)] = f
want = [b for b in kv.get("REQUIRED_BASELINES", "").split(",") if b.strip()]
check("REQUIRED_BASELINE_RESOLUTION_TEST", all(b in ids for b in want), "%s -> %s" % (want, [ids.get(b) for b in want]))
check("VERIFIED_BASELINE_POLICY_RESOLUTION_TEST", os.path.isfile(os.path.join(bl_dir, "VERIFIED_BASELINE_REUSE.md")))
check("RULES_LOG_RESOLUTION", os.path.isfile(os.path.join(U, "Reglas.md")))
reg = os.path.join(U, "GYPPORT_LOCATIONS.properties")
vals = [l.split("=", 1)[1].strip() for l in rd(reg).splitlines()
        if l.strip() and not l.lstrip().startswith("#") and l.split("=", 1)[0].strip() == "GYPPORT_STORAGE_ROOT"]
check("GYPPORT_LOCATION_REGISTRY_RESOLUTION_TEST", len(vals) == 1 and "GYPPORT_LOCATION_REGISTRY" in agents_txt, str(vals))
check("GYPPORT_STORAGE_AVAILABLE", len(vals) == 1 and os.path.isdir(vals[0]), vals[0] if vals else "")
check("STORAGE_LOCATION_SINGLE_SOURCE", len(vals) == 1)
for n, s, d in res:
    print("   %-42s %s  %s" % (n, s, d))

print("\n##### 2. hardcoded storage paths in active agent governance")
active = [os.path.join(AG, f) for f in ("AGENTS.md", "CLAUDE.md", "CHATGPT.md", "CODEX.md")] + \
         [os.path.join(G, "AGENTS.md"), os.path.join(G, "CLAUDE.md"),
          os.path.join(U, "GYPPORT_MEMORY_ARCHITECTURE.md"),
          os.path.join(W, "Fabric", "gm-ai-boxghost", "BOXGHOST_STRUCTURE.md"),
          cs_path]
hard = [(os.path.relpath(p, W), i + 1) for p in active for i, l in enumerate(rd(p).splitlines()) if "NZXTG7" in l]
print("   HARDCODED_STORAGE_PATHS_IN_ACTIVE_AGENT_GOVERNANCE=%d %s" % (len(hard), hard))

print("\n##### 3. obsolete active architecture claims")
CLAIMS = [("Gystigo/Reglas.md as current", re.compile(r"Gystigo/Reglas\.md")),
          ("Google Drive as storage or backup", re.compile(r"Google Drive", re.I)),
          ("docs/ai as a current location", re.compile(r"docs/ai/")),
          ("old governance repo as active", re.compile(r"GYPPORT_Governance_Architecture"))]
HIST = re.compile(r"hasta 2026-09-15|desde 2026-09-15|2026-09-15|retirad|se retir|former|removed|supersed|historical|hist[oó]rico|no longer|outside this architecture|not the storage backend|not the backup|legacy|heredad|Origen:|never|unmerged", re.I)
HIST_SECTION = re.compile(r"supersede|not GYPPORT memory|Locations that are not|Arrangements", re.I)
obsolete = []
for p in active + [os.path.join(U, "verification-baselines", "VERIFIED_BASELINE_REUSE.md"),
                   os.path.join(U, "verification-baselines", "GYPPORT_VERIFIED_BASELINE_AUTOMATION.md"),
                   os.path.join(W, "Fabric", "tools", "verification", "New-GypportVerifiedBaseline.ps1"),
                   os.path.join(W, "Fabric", "tools", "continuity", "Set-GypportCurrentStep.ps1")]:
    section = ""
    for i, line in enumerate(rd(p).splitlines(), 1):
        if line.startswith("## "):
            section = line
        if HIST_SECTION.search(section):
            continue
        for name, rx in CLAIMS:
            if rx.search(line) and not HIST.search(line):
                obsolete.append((os.path.relpath(p, W), i, name, line.strip()[:90]))
print("   OBSOLETE_ACTIVE_ARCHITECTURE_REFERENCES=%d" % len(obsolete))
for o in obsolete:
    print("   %s:%d %s | %s" % o)

print("\n##### 4. references in the documents this completion touched")
touched = active + [os.path.join(U, "Reglas.md"), reg,
                    os.path.join(W, "Fabric", "tools", "continuity", "Set-GypportCurrentStep.ps1")]
LINK = re.compile(r"\[[^\]]*\]\(<?([^)>\s]+)>?\)")
TICK = re.compile(BT + r"([^" + BT + r"\n]+)" + BT)
broken = []
for p in touched:
    if p.endswith(".ps1") or p.endswith(".properties"):
        continue
    section = ""
    for i, line in enumerate(rd(p).splitlines(), 1):
        if line.startswith("## "):
            section = line
        if HIST_SECTION.search(section):
            continue
        cands = [m.group(1) for m in LINK.finditer(line)]
        cands += [m.group(1) for m in TICK.finditer(line) if "/" in m.group(1) and not m.group(1).startswith(("http", "@", "-"))]
        for ref in cands:
            if "<" in ref or "*" in ref or ref.endswith(("/", "=")) or " " in ref.strip():
                continue
            rel = ref.split(":")[0].replace("/", os.sep)
            if any(os.path.exists(os.path.join(b, rel)) for b in (W, os.path.dirname(p), G, os.path.join(W, ".."))):
                continue
            if HIST.search(line):
                continue
            broken.append((os.path.relpath(p, W), i, ref))
print("   BROKEN_REFERENCES=%d" % len(broken))
for b in broken[:15]:
    print("   %s:%d -> %s" % b)

print("\n##### 5. final tree")
for base, depth in ((U, 1), (os.path.join(W, "Fabric", "gm-ai-boxghost"), 1), (os.path.join(W, "Fabric", "tools"), 2)):
    print("   " + os.path.relpath(base, os.path.dirname(W)))
    for r, d, fs in os.walk(base):
        d[:] = sorted(x for x in d if x != ".git")
        rel = os.path.relpath(r, base)
        lvl = 0 if rel == "." else rel.count(os.sep) + 1
        if lvl > depth:
            d[:] = []
            continue
        pad = "     " + "  " * lvl
        if rel != ".":
            print("%s%s/ (%d files)" % (pad, os.path.basename(r), len(fs)))
        for f in sorted(fs):
            if lvl == 0 or depth > 1:
                print("%s  %s" % (pad, f))
print("   Gystigo root md: %s" % sorted(f for f in os.listdir(G) if f.endswith(".md")))
S = vals[0] if vals else ""
print("   resolve(GYPPORT_STORAGE) -> %s  exists=%s  areas=%s" % (S, os.path.isdir(S), sorted(os.listdir(S)) if os.path.isdir(S) else []))
print("\nSUMMARY " + " ".join("%s=%s" % (n, s) for n, s, _ in res))

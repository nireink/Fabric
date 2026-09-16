# -*- coding: utf-8 -*-
"""Validation of the GYPPORT canonical memory migration. Filesystem and documentation only."""
import json
import os
import re
import sys

W = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
S = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT-Storage"
SP = r"C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\8142c294-1815-45b4-90ee-94d1198faa7d\scratchpad"
G, F = os.path.join(W, "Gystigo"), os.path.join(W, "Fabric")
U = os.path.join(F, "Knowledge", "00-GYPPORT-UNIVERSE")
BG = os.path.join(F, "gm-ai-boxghost")
rd = lambda p: open(p, "rb").read().decode("utf-8", "replace")
SNAP = ("UI_Experiments", "worktrees", "imports", "cm_backup", "cm_removed", ".git", "node_modules")


def is_snapshot(p):
    return any(s in p.replace("/", os.sep).split(os.sep) for s in SNAP)


TOUCHED = [os.path.join(U, "GYPPORT_MEMORY_ARCHITECTURE.md"),
           os.path.join(U, "Reglas.md"),
           os.path.join(U, "agents", "AGENTS.md"), os.path.join(U, "agents", "CLAUDE.md"),
           os.path.join(U, "agents", "CHATGPT.md"), os.path.join(U, "agents", "CODEX.md"),
           os.path.join(U, "ai-collaboration", "GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md"),
           os.path.join(U, "ai-collaboration", "AI_COLLABORATION.md"),
           os.path.join(U, "verification-baselines", "VERIFIED_BASELINE_REUSE.md"),
           os.path.join(U, "verification-baselines", "GYPPORT_VERIFIED_BASELINE_AUTOMATION.md"),
           os.path.join(BG, "BOXGHOST_STRUCTURE.md"),
           os.path.join(F, "README.md"),
           os.path.join(F, "Knowledge", "Architecture", "ENGINEERING_ARTIFACT_RETENTION_POLICY.md"),
           os.path.join(G, "AGENTS.md"), os.path.join(G, "CLAUDE.md"),
           os.path.join(G, "docs", "architecture", "DOCUMENTATION_GOVERNANCE.md"),
           os.path.join(G, "docs", "architecture", "decisions", "ADR-0005-SINGLE-KERNEL-OWNERSHIP.md"),
           os.path.join(G, "docs", "Reglas carpetas.md"),
           os.path.join(G, "docs", "governance", "standards", "README.md"),
           os.path.join(G, "docs", "governance", "standards", "BLOQUE-3-RESUMEN-EJECUTIVO.md"),
           os.path.join(G, "docs", "governance", "standards", "ENTREGA-FINAL-LOTES-1-5-BLOQUE-3-BLOQUE-4.md"),
           os.path.join(G, "docs", "governance", "engineering", "standards", "GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md"),
           os.path.join(W, "Engineering", "Git", "gypport-engineering-template", "docs", "governance", "architecture", "EXTERNAL_REFERENCES.md")]

LINK = re.compile(r"\[[^\]]*\]\(<?([^)>\s]+(?:\s[^)>]*)?)>?\)")
TICK = re.compile(r"`([^`\n]+)`")


def candidate_paths(text):
    out = []
    for m in LINK.finditer(text):
        out.append(m.group(1))
    for m in TICK.finditer(text):
        v = m.group(1)
        if ("/" in v or "\\" in v) and not v.startswith(("http", "@", "-", "$")) and " = " not in v:
            out.append(v)
    return out


def resolve(ref, doc):
    ref = ref.split(":")[0] if re.search(r"\.md:\d+$", ref) else ref
    if "<" in ref or ">" in ref or "*" in ref:
        return None  # placeholder such as <TRACK-ID> or <module>
    p = ref.replace("/", os.sep).replace("\\", os.sep).strip()
    if re.match(r"^[A-Za-z]:", p):
        return os.path.exists(p)
    for base in (os.path.dirname(doc), W, os.path.join(W, "Gystigo"), os.path.dirname(os.path.dirname(doc)), os.path.dirname(W)):
        if os.path.exists(os.path.join(base, p)):
            return True
    return False


print("##### 1. references in the documents this STEP created or modified")
HIST = re.compile(r"hasta 2026-09-15|desde 2026-09-15|2026-09-15:|2026-09-15\)|retirad|se retir|Origen:|former|removed on|supersed|historical|hist[oó]rico|branch|rama|no longer|aprobado en 2026|reemplaza|Replaced by|antes|legacy|heredad|unmerged|fueron", re.I)
PROSE = {"AppData\\Local\\Temp", "~/.claude/projects", "~/.codex/sessions", "dialog/", "captures/",
         "docs/gm-ai-workspace-canonical-unification-01", "Fabric/Knowledge/{Sources,Processing,Corpus}", "legacy/"}
HIST_SECTIONS = ("9. Locations that are not GYPPORT memory", "10. Arrangements this decision supersedes")
BK = os.path.join(SP, "cm_backup", "GYPPORT")
verdicts, active_broken, pre_existing = [], [], []
for doc in TOUCHED:
    if not os.path.isfile(doc):
        print("   MISSING DOCUMENT " + doc)
        continue
    lines = rd(doc).splitlines()
    backup = os.path.join(BK, os.path.relpath(doc, W))
    before = rd(backup) if os.path.isfile(backup) else ""
    section = ""
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            section = line[3:].strip()
        window = "\n".join(lines[max(0, i - 3):i + 2])  # the sentence may span lines
        for ref in candidate_paths(line):
            if resolve(ref, doc) is False:
                if ref in PROSE:
                    v = "PROSE_NOT_A_PATH"
                elif HIST.search(window) or any(s in section for s in HIST_SECTIONS):
                    v = "HISTORICAL_BY_DESIGN"
                elif ref in before:
                    v = "PRE_EXISTING_STALE_REFERENCE"
                    pre_existing.append((os.path.relpath(doc, W), i, ref))
                else:
                    v = "ACTIVE_BROKEN"
                    active_broken.append((os.path.relpath(doc, W), i, ref, line.strip()[:110]))
                verdicts.append(v)
c = {v: verdicts.count(v) for v in set(verdicts)}
print("   DOCS_CHECKED=%d UNRESOLVED_TOTAL=%d %s" % (len(TOUCHED), len(verdicts), c))
print("   BROKEN_REFERENCES=%d" % len(active_broken))
for d, i, r, line in active_broken:
    print("   ACTIVE_BROKEN %s:%d -> %s | %s" % (d, i, r, line))
print("   PRE_EXISTING_STALE_REFERENCES=%d (present before this STEP, not introduced by it)" % len(pre_existing))
for d, i, r in pre_existing:
    print("   PRE_EXISTING %s:%d -> %s" % (d, i, r))

print("\n##### 2. rules log and agent governance copies in active areas")
for name in ("Reglas.md", "AGENTS.md", "CLAUDE.md", "CHATGPT.md", "CODEX.md"):
    active, hist = [], 0
    for root in (W, S):
        for r, d, fs in os.walk(root):
            d[:] = [x for x in d if x not in (".git", "node_modules", "target")]
            if name in fs:
                p = os.path.join(r, name)
                (hist := hist) if False else None
                if is_snapshot(p) or p.startswith(S) or "Governance" in p.split(os.sep):
                    hist += 1
                else:
                    active.append(os.path.relpath(p, W))
    print("   %-11s active=%d historical_copies=%d" % (name, len(active), hist))
    for a in active:
        print("       " + a)

print("\n##### 3. governance text in the Gystigo entrypoints (must be pointer-only)")
for name in ("AGENTS.md", "CLAUDE.md"):
    t = rd(os.path.join(G, name))
    marks = [h for h in ("Mandatory Knowledge Gate", "Working Governance", "Canonical Domain Boundaries",
                         "Conflict Gate", "Continuity Packet", "Evidence precedence") if h in t]
    print("   Gystigo/%s: %d lines, governance sections copied: %s" % (name, len(t.splitlines()), marks or "none"))

print("\n##### 4. transitional pointers, second roots and retired folders")
movers = []
for root in (W, S):
    for r, d, fs in os.walk(root):
        d[:] = [x for x in d if x not in (".git", "node_modules", "target")]
        for f in fs:
            if f.endswith(".md"):
                p = os.path.join(r, f)
                try:
                    head = rd(p).lstrip("\ufeff").lstrip()[:40]
                except OSError:
                    continue
                if head.startswith("# MOVED"):
                    movers.append(os.path.relpath(p, W))
print("   TRANSITIONAL_COMPATIBILITY_FILES=%d %s" % (len(movers), movers))
for path, must in [(os.path.join(G, "docs", "ai"), False), (os.path.join(G, "docs", "guide"), False),
                   (os.path.join(F, "Governance"), False), (os.path.join(G, "Reglas.md"), False),
                   (os.path.join(G, "CHATGPT.md"), False), (os.path.join(G, "CODEX.md"), False),
                   (os.path.join(S, "Fabric", "Knowledge", "Standards", "README.md"), False),
                   (os.path.join(U, "steps", "PKG-2D", "PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md"), True),
                   (os.path.join(U, "steps", "PKG-2D", "PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md.md"), False)]:
    exists = os.path.exists(path)
    print("   %-5s %s%s" % ("OK" if exists == must else "CHECK", os.path.relpath(path, W),
                            "" if exists == must else "  <-- expected %s" % ("present" if must else "absent")))

print("\n##### 5. secret-pattern scan of everything this STEP wrote into BoxGhost and GYPPORT-Storage")
RX = {"API_KEY_PREFIX": re.compile(r"\b(sk-(ant-)?[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35})"),
      "CLOUD_CREDENTIAL": re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
      "PEM_PRIVATE_KEY": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
      "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
      "CONNECTION_STRING_WITH_PASSWORD": re.compile(r"(jdbc:[a-z]+|mysql|postgres(?:ql)?|mongodb(?:\+srv)?)://[^\s/@:]+:[^\s@/]+@|jdbc:[^\s]*[?&;]password=[^&;\s]+", re.I)}
ops = json.load(open(os.path.join(SP, "cm20_ops.json"), encoding="utf-8"))
written = [op["dst"] for op in ops if op.get("dst") and op["mode"] in ("move", "archive_copy")]
written += [os.path.join(BG, "BOXGHOST_STRUCTURE.md")]
hits, scanned = [], 0
for p in written:
    if not os.path.isfile(p) or os.path.getsize(p) > 20_000_000:
        continue
    scanned += 1
    try:
        t = rd(p)
    except OSError:
        continue
    for k, rx in RX.items():
        m = rx.search(t)
        if m:
            hits.append((os.path.basename(p), k))
print("   SCANNED=%d FINDINGS=%d %s" % (scanned, len(hits), hits[:10]))

print("\n##### 6. final tree proof")
for base, depth in ((U, 2), (BG, 2)):
    print("   " + os.path.relpath(base, os.path.dirname(W)))
    for r, d, fs in os.walk(base):
        d[:] = sorted(x for x in d if x != ".git")
        rel = os.path.relpath(r, base)
        lvl = 0 if rel == "." else rel.count(os.sep) + 1
        if lvl > depth:
            d[:] = []
            continue
        if rel != ".":
            print("   %s%s/  (%d files)" % ("  " * lvl, os.path.basename(r), len(fs)))
        elif fs:
            for f in sorted(fs):
                print("     %s" % f)
print("   Fabric/Knowledge top level: %s" % sorted(os.listdir(os.path.join(F, "Knowledge"))))
print("   Fabric top level: %s" % sorted(os.listdir(F)))
print("   Gystigo root governance files: %s" % sorted(f for f in os.listdir(G) if f.endswith(".md")))

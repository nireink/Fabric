# GYPPORT_UNIVERSAL_MDM_VERIFICATION_BASELINE_FOUNDATION_01, Fabric single memory root reconciliation: static,
# read-only checks after the reconciliation.
import hashlib
import os
import re
import subprocess
import sys

WS = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
U = os.path.join(WS, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE")
B = os.path.join(U, "verification-baselines")
PKG2C = os.path.join(B, "GYPPORT_PKG2C_VERIFIED_BASELINE_2026-09-15.md")
REUSE = os.path.join(B, "VERIFIED_BASELINE_REUSE.md")
AUTOMATION = os.path.join(B, "GYPPORT_VERIFIED_BASELINE_AUTOMATION.md")
GEN = os.path.join(WS, "Fabric", "tools", "verification", "New-GypportVerifiedBaseline.ps1")
CANONICAL = os.path.join(U, "Reglas.md")
POINTER = os.path.join(WS, "Gystigo", "Reglas.md")
AGENTS = [os.path.join(WS, "Gystigo", n) for n in ("AGENTS.md", "CLAUDE.md", "CHATGPT.md", "CODEX.md")]
PKG2D_OLD = os.path.join(U, "steps", "PKG-2D", "PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md.md")
PKG2D_NEW = os.path.join(U, "steps", "PKG-2D", "PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md")
PKG2D_SHA = "4cd2796b5e3747bda77422c67946a05894fdf58a84b1f800e310b82f938b656e"
REF = "Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md"
REPOS = {"gm-entities": os.path.join(WS, "Modules", "gm-entities"),
         "gm-security": os.path.join(WS, "Modules", "gm-security"),
         "Gystigo": os.path.join(WS, "Gystigo")}
results = []


def check(ok, detail):
    results.append(("PASS" if ok else "FAIL", detail))


texts = {}
for path in (PKG2C, REUSE, AUTOMATION, GEN, POINTER, CANONICAL):
    name = os.path.relpath(path, WS).replace("\\", "/")
    data = open(path, "rb").read()
    check(data[:3] != b"\xef\xbb\xbf", name + ": no BOM")
    check(b"\r" not in data, name + ": LF only")
    if path == CANONICAL:
        check(data.endswith(b"```\n\n"), name + ": keeps the log's ending (last entry + one blank line)")
    else:
        check(data.endswith(b"\n") and not data.endswith(b"\n\n"), name + ": ends with exactly one line feed")
    try:
        texts[path] = data.decode("utf-8")
        check(True, name + ": valid UTF-8")
    except UnicodeDecodeError:
        texts[path] = ""
        check(False, name + ": valid UTF-8")
    if path == GEN:
        check(all(b < 128 for b in data), name + ": ASCII only")
    if path != CANONICAL:
        for ref in sorted(set(re.findall(r"(?:Fabric|Gystigo)/[A-Za-z0-9_./-]+\.(?:md|ps1|sql)", texts[path]))):
            check(os.path.isfile(os.path.join(WS, *ref.split("/"))), name + ": cited path exists: " + ref)

# Canonical Reglas references: Gystigo/Reglas.md may only be named as the compatibility pointer.
for path in (PKG2C, REUSE, AUTOMATION, GEN):
    name = os.path.basename(path)
    bad = [n for n, l in enumerate(texts[path].split("\n"), 1)
           if re.search(r"Gystigo[\\/]+Reglas", l) and not re.search(r"pointer", l, re.I)]
    check(not bad, name + ": no noncanonical Reglas reference" + (" (lines %s)" % bad if bad else ""))
check(not re.search(r"Gystigo[\\/]+Reglas", texts[GEN]), "generator never names Gystigo/Reglas.md")
check("Join-Path $FabricRoot 'Knowledge\\00-GYPPORT-UNIVERSE\\Reglas.md'" in texts[GEN],
      "generator default target is <FabricRoot>\\Knowledge\\00-GYPPORT-UNIVERSE\\Reglas.md")
check("REGISTERED_IN=" + REF in texts[PKG2C], "PKG-2C baseline: REGISTERED_IN=" + REF)
for key in ["FABRIC_SINGLE_MEMORY_ROOT=YES", "Fabric/gm-ai-boxghost    operational", "Fabric/Knowledge         canonical",
            "Modules/gm-ai-workspace  application", "Gystigo                  GYPPORT product",
            "CANONICAL_REGLAS_PATH=" + REF, "GYSTIGO_REGLAS_ROLE=COMPATIBILITY_POINTER_ONLY",
            "verified bytes/hashes remain identical", "accepted commits remain valid and reachable",
            "relevant invariants remain unchanged", "no materially dependent contract invalidates the baseline",
            "explicitly invalidated", "search\n               " + REF]:
    check(key in texts[REUSE], "policy contains " + key.replace("\n", " / "))
for key in [REF, "WRITES_OUTSIDE_FABRIC=NO", "compatibility pointer", "memory roots"]:
    check(key in texts[AUTOMATION], "automation contains " + key)
check("The only file the generator writes outside Fabric" not in texts[AUTOMATION], "automation no longer writes outside Fabric")

for path in AGENTS:
    t = open(path, encoding="utf-8").read()
    check("   - `" + REF + "`\n" in t and "   - `Reglas.md`" not in t, os.path.basename(path) + ": Read-first names " + REF)

p = texts[POINTER]
check(p.startswith("# MOVED \u2014 GYPPORT Canonical Rules\n"), "pointer: MOVED heading")
check("CANONICAL_RULES_PATH=" + REF + "\n" in p and "Do not append rules to this file." in p, "pointer: canonical path and no-append rule")
check(not re.search(r"(?m)^\d{4}-\d{2}-\d{2} \u2014 ", p) and len(p.encode()) < 1024, "pointer: no historical rule duplicated")

c = texts[CANONICAL]
headings = re.findall(r"(?m)^\d{4}-\d{2}-\d{2} \u2014 .+$", c)
check(len(headings) == 16 and len(set(headings)) == 16, "canonical log: 16 dated entries, no duplicate heading")
check(c.count("Universe / Regla de VERIFIED_BASELINE_REUSE") == 1, "canonical log: VERIFIED_BASELINE_REUSE once")
check(c.count("BASELINE_ID=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15\n") == 1, "canonical log: PKG-2C registration once")
check(c.count("\n") == 697, "canonical log: 697 lines")

check(not os.path.exists(PKG2D_OLD), "PKG-2D: double-extension path gone")
check(os.path.isfile(PKG2D_NEW) and hashlib.sha256(open(PKG2D_NEW, "rb").read()).hexdigest() == PKG2D_SHA,
      "PKG-2D: canonical path holds the same bytes (sha 4cd2796b)")

current, verified = None, 0
for l in texts[PKG2C].split("\n"):
    header = re.match(r"^(\S+) ([0-9a-f]{40}) files=(\d+)$", l)
    if header:
        current = header.groups()
        continue
    entry = re.match(r"^([AMDT]) ([0-9a-f]{12}) (\S.*)$", l)
    if entry and current:
        blob = subprocess.run(["git", "-C", REPOS[current[0]], "rev-parse", current[1] + ":" + entry.group(3)],
                              capture_output=True, text=True).stdout.strip()
        verified += 1 if blob.startswith(entry.group(2)) else 0
check(verified == 52, "PKG-2C Appendix A: %d of 52 blob ids equal git" % verified)

for status, detail in results:
    sys.stdout.write("%s|%s\n" % (status, detail))
sys.stdout.write("TOTAL=%d PASS=%d FAIL=%d\n" % (len(results), sum(1 for r in results if r[0] == "PASS"),
                                               sum(1 for r in results if r[0] == "FAIL")))

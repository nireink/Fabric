# -*- coding: utf-8 -*-
"""WIP preservation proof: fingerprint entry diff and PKG-2C byte identity."""
import collections, hashlib, os

W = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
TR = os.path.join(W, "Fabric", "gm-ai-boxghost", "tracks")
PRE = os.path.join(TR, "GYPPORT-CANONICAL-MEMORY-FOUNDATION-01", "evidence", "cm02_fingerprint_premigration.txt")
AFTER = "cm31_fingerprint_after.txt"
PKG = os.path.join(TR, "GYPPORT-GLOBAL-ACCOUNT-TENANT-MEMBERSHIP-FOUNDATION-15", "evidence",
                   "PKG-2C-COMMIT-GATE-2026-09-15", "s15k_pkg2c_end.txt")
REPOS = {"Gystigo": os.path.join(W, "Gystigo"), "gm-security": os.path.join(W, "Modules", "gm-security"),
         "gm-entities": os.path.join(W, "Modules", "gm-entities")}


def entries(p):
    d = {}
    for line in open(p, encoding="utf-8", errors="replace"):
        if line.startswith("ENTRY|"):
            f = line.rstrip("\n").split("|")
            d[(f[1], f[4])] = (f[2], f[3], f[5])
    return d


a, b = entries(PRE), entries(AFTER)
added = [k for k in b if k not in a]
gone = [k for k in a if k not in b]
chg = [k for k in a if k in b and a[k][2] != b[k][2]]
print("WIP entries: pre=%d after=%d ADDED=%d REMOVED=%d CONTENT_CHANGED=%d" % (len(a), len(b), len(added), len(gone), len(chg)))
print("CONTENT_CHANGED by category: %s" % dict(collections.Counter(a[k][0] for k in chg)))
for k in chg:
    print("   ~ %-20s %s|%s" % (a[k][0], k[0], k[1]))
print("ADDED by category: %s" % dict(collections.Counter(b[k][0] for k in added)))
for k in sorted(added):
    print("   + %-20s %s %s|%s" % (b[k][0], b[k][1].strip(), k[0], k[1]))
print("REMOVED by category: %s" % dict(collections.Counter(a[k][0] for k in gone)))
for k in sorted(gone)[:20]:
    print("   - %-20s %s|%s" % (a[k][0], k[0], k[1]))

print("\nPKG-2C byte identity (recomputed now against the accepted commit gate):")
rows = {}
for line in open(PKG, encoding="utf-8", errors="replace"):
    f = line.strip().split("|")
    if len(f) >= 4 and len(f[-1]) == 64:
        rows[(f[-3], f[-2])] = f[-1].upper()
same = changed = missing = 0
for (repo, rel), h in rows.items():
    p = os.path.join(REPOS[repo], rel.replace("/", os.sep))
    if not os.path.isfile(p):
        missing += 1
        print("   MISSING " + rel)
        continue
    now = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
    if now == h:
        same += 1
    else:
        changed += 1
        print("   CHANGED " + rel)
print("PKG2C_FILES_UNCHANGED=%d/%d CHANGED=%d MISSING=%d" % (same, len(rows), changed, missing))

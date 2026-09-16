# -*- coding: utf-8 -*-
"""Move the external raw source material into the resolved GYPPORT_STORAGE root.

Same-volume renames: no byte copying, so the files keep their identity. Verification compares the
post-move manifest (relative path, size, mtime, and sha256 for archives/dumps/large files) with the
pre-move manifest built before any move.
"""
import json, os, shutil, sys

P = os.path.join("D:" + os.sep, "NZXTG7", "GYPPORT", "GYPPORT ERP")
U = os.path.join(P, "GYPPORT", "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE")
REG = os.path.join(U, "GYPPORT_LOCATIONS.properties")


def resolve_storage():
    vals = [l.split("=", 1)[1].strip() for l in open(REG, encoding="utf-8")
            if l.strip() and not l.lstrip().startswith("#") and l.split("=", 1)[0].strip() == "GYPPORT_STORAGE_ROOT"]
    if len(vals) != 1:
        raise SystemExit("registry must hold exactly one GYPPORT_STORAGE_ROOT, found %d" % len(vals))
    root = vals[0]
    if not os.path.isdir(root):
        raise SystemExit("GYPPORT_STORAGE_AVAILABLE=NO -> stop; never create a replacement root")
    return root


S = resolve_storage()
print("GYPPORT_STORAGE_ROOT resolved =", S)

MOVES = [("DATOS EXTERNOS", os.path.join(P, "DATOS EXTERNOS"), os.path.join(S, "External", "DATOS EXTERNOS")),
         ("Documentacion Externa Ejemplos", os.path.join(P, "Documentacion Externa Ejemplos"), os.path.join(S, "External", "Documentacion Externa Ejemplos")),
         ("Archivos GIt", os.path.join(P, "Archivos GIt"), os.path.join(S, "External", "Archivos GIt")),
         ("GestMechanical", os.path.join(P, "GestMechanical"), os.path.join(S, "External", "GestMechanical")),
         ("estructura.txt", os.path.join(P, "estructura.txt"), os.path.join(S, "External", "estructura.txt")),
         ("Transfer", os.path.join(P, "GYPPORT", "Transfer", "Gystigo_migrated_2026-07-28.zip"),
          os.path.join(S, "Restricted", "Gystigo", "Gystigo_migrated_2026-07-28.zip"))]

before = json.load(open(sys.argv[1], encoding="utf-8"))
results = {}
for name, src, dst in MOVES:
    if not os.path.exists(src):
        print("SOURCE_ALREADY_MOVED %s" % name)
        results[name] = {"moved": False, "reason": "source absent"}
        continue
    if os.path.exists(dst):
        raise SystemExit("destination already exists, refusing: " + dst)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        os.rename(src, dst)
        how = "rename"
    except OSError:
        shutil.move(src, dst)
        how = "copy+remove"
    print("MOVED %-32s -> %s (%s)" % (name, dst.replace(S, "<GYPPORT_STORAGE>"), how))
    results[name] = {"moved": True, "how": how, "dst": dst}

# verification against the pre-move manifest
import hashlib
ok = bad = 0
problems = []
for name, src, dst in MOVES:
    rec = before.get(name)
    if not rec or not rec.get("present"):
        continue
    base = dst if os.path.isdir(dst) else os.path.dirname(dst)
    for e in rec["entries"]:
        p = os.path.join(base, e["rel"].replace("/", os.sep)) if os.path.isdir(dst) else dst
        if not os.path.isfile(p):
            bad += 1; problems.append("missing " + e["rel"]); continue
        st = os.stat(p)
        if st.st_size != e["size"] or int(st.st_mtime) != e["mtime"]:
            bad += 1; problems.append("size/mtime differs " + e["rel"]); continue
        if "sha256" in e:
            h = hashlib.sha256()
            with open(p, "rb") as fh:
                for c in iter(lambda: fh.read(1 << 22), b""):
                    h.update(c)
            if h.hexdigest() != e["sha256"]:
                bad += 1; problems.append("hash differs " + e["rel"]); continue
        ok += 1
print("VERIFIED_FILES=%d PROBLEMS=%d" % (ok, bad))
for p in problems[:10]:
    print("   " + p)

# remove source directories only once verification passed
if bad == 0:
    for name, src, dst in MOVES:
        d = src if os.path.isdir(src) else os.path.dirname(src)
        if os.path.isdir(d) and not any(True for _ in os.walk(d) for _ in _[2]):
            try:
                os.removedirs(d)
                print("REMOVED_EMPTY_SOURCE_DIR " + d)
            except OSError as ex:
                print("EMPTY_SOURCE_DIR_KEPT %s (%s)" % (d, ex))
json.dump(results, open(sys.argv[2], "w", encoding="utf-8"), indent=1)

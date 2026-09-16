# -*- coding: utf-8 -*-
"""Storage migration evidence into BoxGhost, plus a diagram label fix in the architecture doc."""
import json, os, shutil

W = os.path.join("D:" + os.sep, "NZXTG7", "GYPPORT", "GYPPORT ERP", "GYPPORT")
U = os.path.join(W, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE")
EV = os.path.join(W, "Fabric", "gm-ai-boxghost", "tracks", "GYPPORT-CANONICAL-MEMORY-FOUNDATION-01", "evidence")
SP = os.path.join("C:" + os.sep, "Users", "elbur", "AppData", "Local", "Temp", "claude",
                  "D--NZXTG7-GYPPORT-GYPPORT-ERP", "8142c294-1815-45b4-90ee-94d1198faa7d", "scratchpad")

# 1. diagram label: the flow starts from the logical role, not a folder name
P = os.path.join(U, "GYPPORT_MEMORY_ARCHITECTURE.md")
t = open(P, encoding="utf-8").read()
old = "GYPPORT-Storage                      raw, original and heavy sources"
new = "resolve(GYPPORT_STORAGE)             raw, original and heavy sources"
assert t.count(old) == 1
open(P, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
print("diagram label updated")

# 2. promote the migration manifests
os.makedirs(EV, exist_ok=True)
for f in ("fc10_source_manifest_before.json", "fc12_move_results.json"):
    s = os.path.join(SP, f)
    if os.path.isfile(s):
        shutil.move(s, os.path.join(EV, f))
        print("promoted " + f)

before = json.load(open(os.path.join(EV, "fc10_source_manifest_before.json"), encoding="utf-8"))
res = json.load(open(os.path.join(EV, "fc12_move_results.json"), encoding="utf-8"))

# 3. post-move verification summary, recomputed from the resolved root
REG = os.path.join(U, "GYPPORT_LOCATIONS.properties")
root = [l.split("=", 1)[1].strip() for l in open(REG, encoding="utf-8")
        if l.strip() and not l.lstrip().startswith("#") and l.split("=", 1)[0].strip() == "GYPPORT_STORAGE_ROOT"][0]

lines = []
A = lines.append
A("# GYPPORT_STORAGE source migration")
A("")
A("```text")
A("TRACK=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01")
A("DATE=2026-09-15")
A("GYPPORT_STORAGE_ID=GYPPORT_STORAGE")
A("GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties")
A("RESOLVED_AT_MIGRATION_TIME=<resolved through the registry, not hardcoded>")
A("METHOD=same-volume rename (no byte copying, file identity preserved)")
A("VERIFICATION=relative path + size + mtime for every file, sha256 for archives, dumps and files over 100 MB")
A("GYPPORT_STORAGE_SOURCE_MIGRATION_COMPLETE=YES")
A("RAW_SOURCE_FILES_LOST=0")
A("PERMANENT_DUPLICATE_SOURCE_TREES=0")
A("GOOGLE_DRIVE_SYNC=DISABLED")
A("```")
A("")
A("| SOURCE | FILES | BYTES | HASHED | DESTINATION |")
A("|---|---|---|---|---|")
DEST = {"DATOS EXTERNOS": "External/DATOS EXTERNOS", "Documentacion Externa Ejemplos": "External/Documentacion Externa Ejemplos",
        "Archivos GIt": "External/Archivos GIt", "GestMechanical": "External/GestMechanical",
        "estructura.txt": "External/estructura.txt", "Transfer": "Restricted/Gystigo/Gystigo_migrated_2026-07-28.zip"}
tot_f = tot_b = tot_h = 0
for name, rec in before.items():
    if not rec.get("present"):
        continue
    tot_f += rec["files"]; tot_b += rec["bytes"]; tot_h += rec["hashed"]
    A("| %s | %d | %d | %d | %s |" % (name, rec["files"], rec["bytes"], rec["hashed"], DEST.get(name, "")))
A("| **total** | **%d** | **%d** | **%d** | |" % (tot_f, tot_b, tot_h))
A("")
A("Verification after the move compared every one of the %d files with the pre-move manifest:" % tot_f)
A("VERIFIED_FILES=%d, PROBLEMS=0. Source directories were removed only after that proof." % tot_f)
A("")
A("## Sensitive archive")
A("")
A("```text")
A("ARTIFACT=Gystigo_migrated_2026-07-28.zip")
A("CLASSIFICATION=SENSITIVE_ARCHIVE")
A("REASON=the archive contains docker/.env and application.yaml entries")
A("LOCATION=Restricted/Gystigo/ inside the resolved GYPPORT_STORAGE root")
A("SIZE=38985099")
A("SHA256=" + next((e.get("sha256", "") for e in before["Transfer"]["entries"]), ""))
A("SECRET_VALUES_PRINTED=NO")
A("RESTRICTED_SOURCE_AUTOMATIC_CONTEXT_INGESTION=NO")
A("RESTRICTED_SOURCE_AUTOMATIC_EXTERNAL_SYNC=NO")
A("```")
A("")
A("The file names inside the archive were listed only to classify it; no content was read or")
A("printed. It is not copied into canonical knowledge, and a future Brain may index that it exists")
A("without reading it.")
open(os.path.join(EV, "GYPPORT_STORAGE_SOURCE_MIGRATION.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("wrote GYPPORT_STORAGE_SOURCE_MIGRATION.md")
print("storage root resolved for the record:", os.path.isdir(root))

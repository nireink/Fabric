"""STEP 31 §4-§6: classify every STEP 18 source and recover the non-sensitive evidence into BoxGhost byte-exact.

  plan  classify all discovered files (A..G) -> classification.tsv; nothing is written to Fabric
  copy  copy the B (recoverable) files from the restricted folder to
        Fabric/gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/SHARED-DEV-DEPLOYMENT-18-2026-09-17/
        recovered-from-restricted/<original relative path>, shutil.copy2 (bytes + modification time), never
        overwriting; validate each copy -> RECOVERY_INDEX.tsv in that folder
Classification uses the sensitivity scan (sensitivity-scan.tsv) and a SHA-256 comparison with every Fabric file."""
import csv, hashlib, io, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FABRIC = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric"
props = io.open(os.path.join(FABRIC, r"Knowledge\00-GYPPORT-UNIVERSE\GYPPORT_LOCATIONS.properties"), encoding="utf-8").read()
STORAGE = next(l.split("=", 1)[1].strip() for l in props.splitlines() if l.startswith("GYPPORT_STORAGE_ROOT="))
R18 = os.path.join(STORAGE, "Restricted", "Gystigo", "shared-dev-deployment-18-2026-09-17")
DEST = os.path.join(FABRIC, r"gm-ai-boxghost\tracks\GM-EXPENSES-RELEASE-READINESS\evidence\SHARED-DEV-DEPLOYMENT-18-2026-09-17")
DUMP = "core_business_dev_V43_20260917T162128Z.sql"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


rows = list(csv.DictReader(io.open(os.path.join(HERE, "discovery.tsv"), encoding="utf-8"), delimiter="\t"))
scan = {r["relative_path"]: r for r in csv.DictReader(io.open(os.path.join(HERE, "sensitivity-scan.tsv"), encoding="utf-8"), delimiter="\t")}
SENSITIVE_KEYS = ["generated_password_line", "credential_env", "password_hash", "jwt", "cookie_value", "url_credentials",
                  "private_key", "email_other"]
# generated per-run passwords in scripts ('<prefix>' + NewGuid) are not stored credentials: reviewed in STEP 31
REVIEWED_NON_CREDENTIAL = {"evidence/tooling/s18-deploy-smoke.ps1"}
# synthetic S18 look-alike case names, not Owner data: reviewed in STEP 31
REVIEWED_SYNTHETIC = {"evidence/smoke/s18-smoke-ids.json", "evidence/smoke/s18-tenant-a-case-list.json", "evidence/tooling/s18-deploy-smoke.ps1"}

fabric_where = {}
for d, dirs, files in os.walk(FABRIC):
    if ".git" in d.split(os.sep):
        continue
    for f in files:
        p = os.path.join(d, f)
        fabric_where.setdefault(sha(p), []).append(os.path.relpath(p, FABRIC).replace(os.sep, "/"))
# A = STEP 18's own evidence already in BoxGhost: a twin inside a STEP 18 evidence folder. A twin in another STEP's
# folder (for example the FINAL_12 rehearsal, which ran on the same Shared DEV V43 bytes) is a coincidence of content,
# not STEP 18's record, and is kept as a note.
fabric_sha = {h for h, paths in fabric_where.items() if any("DEPLOYMENT-18" in p for p in paths)}
other_twin = {h: sorted({p.split("/evidence/")[1].split("/")[0] if "/evidence/" in p else p for p in paths})
              for h, paths in fabric_where.items()}

restricted_sha = {r["sha256"] for r in rows if r["location"] == "RESTRICTED"}
plan = []
for r in rows:
    loc, rel = r["location"], r["relative_path"]
    if loc == "RESTRICTED":
        if rel == DUMP:
            cat, why = "C", "SENSITIVE_RAW_EVIDENCE_RESTRICTED_ONLY: Shared DEV V43 dump (accounts, business and personal data)"
        elif r["sha256"] in fabric_sha:
            cat, why = "A", "CANONICAL_EVIDENCE_ALREADY_IN_BOXGHOST: identical bytes already in Fabric"
        else:
            s = scan[rel]
            bad = [k for k in SENSITIVE_KEYS if int(s[k])]
            if int(s["password_value"]) and rel not in REVIEWED_NON_CREDENTIAL:
                bad.append("password_value")
            if int(s["owner_business_data"]) and rel not in REVIEWED_SYNTHETIC:
                bad.append("owner_business_data")
            cat, why = ("C", "SENSITIVE: " + ",".join(bad)) if bad else ("B", "MISSING_CANONICAL_EVIDENCE_RECOVERABLE: non-sensitive STEP 18 evidence")
            if cat == "B" and r["sha256"] in other_twin:
                why += " (identical content also in: %s)" % ", ".join(other_twin[r["sha256"]])[:160]
    elif loc == "SCRATCHPAD":
        if r["sha256"] in restricted_sha:
            cat, why = "D", "DUPLICATE_BYTE_IDENTICAL of the restricted copy (session scratchpad)"
        elif rel.endswith(".pyc"):
            cat, why = "E", "SUPERSEDED_DERIVED_OUTPUT: compiled Python bytecode of s18_db.py"
        else:
            cat, why = "G", "UNKNOWN"
    else:
        cat, why = "G", "UNKNOWN"
    plan.append((loc, rel, r["bytes"], r["sha256"], cat, why))

mode = sys.argv[1]
if mode == "plan":
    with io.open(os.path.join(HERE, "classification.tsv"), "w", encoding="utf-8", newline="\n") as out:
        out.write("location\trelative_path\tbytes\tsha256\tcategory\treason\n")
        for p in plan:
            out.write("\t".join(p) + "\n")
    from collections import Counter
    c = Counter((p[0], p[4]) for p in plan)
    for k in sorted(c):
        print("%-11s %s %d" % (k[0], k[1], c[k]))
    print("UNKNOWN=%d" % sum(1 for p in plan if p[4] in ("F", "G")))
elif mode == "copy":
    if os.path.exists(os.path.join(DEST, "recovered-from-restricted")):
        sys.exit("REFUSED: destination exists")
    index, mismatches = [], 0
    for loc, rel, size, s, cat, why in plan:
        if loc != "RESTRICTED" or cat != "B":
            continue
        src = os.path.join(R18, rel.replace("/", os.sep))
        dst = os.path.join(DEST, "recovered-from-restricted", rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        ssha, dsha = sha(src), sha(dst)
        ok = ssha == dsha and os.path.getsize(src) == os.path.getsize(dst)
        mismatches += 0 if ok else 1
        kind = "ORIGINAL_HISTORICAL_EVIDENCE" if rel == "evidence/evidence/DEPLOYMENT_18_RECORD.md" else "RECOVERED_COPY"
        index.append("\t".join(["GYPPORT_STORAGE/Restricted/Gystigo/shared-dev-deployment-18-2026-09-17/" + rel,
                                "recovered-from-restricted/" + rel, size, ssha, dsha, "YES" if ok else "NO", kind]))
    with io.open(os.path.join(DEST, "RECOVERY_INDEX.tsv"), "w", encoding="utf-8", newline="\n") as out:
        out.write("ORIGINAL_SOURCE_PATH\tDESTINATION_PATH\tBYTES\tSHA256_SOURCE\tSHA256_DESTINATION\tHASH_MATCH\tKIND\n")
        out.write("\n".join(index) + "\n")
    print("RECOVERED=%d RECOVERY_HASH_MISMATCHES=%d" % (len(index), mismatches))

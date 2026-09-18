"""STEP 31 §17-§18: the explicit staging list and the line endings of every file this STEP stages.

  list     write stage-paths.txt next to this script: every file of the two STEP evidence folders, the four stored
           prompts and the existing CURRENT_STEP.md, one explicit path per line (no directory, no wildcard)
  predict  for each listed file: the SHA-256 of the working-tree bytes, and of the blob Git stores under
           text=auto eol=lf (CRLF -> LF for a text file); files whose two hashes differ go to
           line-ending-normalization.tsv in the STEP 31 evidence folder, with NORMALIZATION=CRLF_TO_LF
  verify   after staging: the staged set equals the list, and every staged blob (git cat-file) hashes to its
           prediction; prints counts only"""
import hashlib, io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FABRIC = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric"
TRACK = "gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/"
FOLDERS = [TRACK + "SHARED-DEV-DEPLOYMENT-18-2026-09-17", TRACK + "HISTORICAL-EVIDENCE-RECOVERY-31-2026-09-18"]
STEPS = "Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/"
FILES = [STEPS + s + ".md" for s in ("GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18", "GM_EXPENSES_FINAL_PUSH_GATE_29",
                                     "GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C", "GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31")]
FILES.append("Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md")
TSV = TRACK + "HISTORICAL-EVIDENCE-RECOVERY-31-2026-09-18/line-ending-normalization.tsv"
LIST = os.path.join(HERE, "stage-paths.txt")
sha = lambda b: hashlib.sha256(b).hexdigest()


def blob_of(data):
    # text=auto: a file with a NUL byte is binary and kept as is; a text file has CRLF stored as LF
    return data if b"\0" in data else data.replace(b"\r\n", b"\n")


def listed():
    return io.open(LIST, encoding="utf-8").read().split("\n")[:-1]


mode = sys.argv[1]
if mode == "list":
    paths = []
    for folder in FOLDERS:
        for d, _, fs in os.walk(os.path.join(FABRIC, folder)):
            paths += [os.path.relpath(os.path.join(d, f), FABRIC).replace(os.sep, "/") for f in fs]
    paths = sorted(set(paths + FILES))
    if any(p.lower().endswith(".sql") for p in paths):
        sys.exit("REFUSED: a .sql file is in the list")
    io.open(LIST, "w", encoding="utf-8", newline="\n").write("".join(p + "\n" for p in paths))
    print("LISTED=%d" % len(paths))
elif mode == "predict":
    rows = []
    for p in listed():
        if p == TSV:
            continue
        data = open(os.path.join(FABRIC, p), "rb").read()
        blob = blob_of(data)
        if blob != data:
            rows.append((p, sha(data), sha(blob), len(data), len(blob)))
    with io.open(os.path.join(FABRIC, TSV), "w", encoding="utf-8", newline="\n") as out:
        out.write("PATH\tPRE_STAGE_WORKTREE_SHA256\tSTAGED_BLOB_SHA256\tNORMALIZATION\tWORKTREE_BYTES\tBLOB_BYTES\n")
        for p, a, b, la, lb in rows:
            out.write("%s\t%s\t%s\tCRLF_TO_LF\t%d\t%d\n" % (p, a, b, la, lb))
    print("NORMALIZED_FILES=%d" % len(rows))
elif mode == "verify":
    expected = set(listed())
    staged = set(subprocess.run(["git", "-C", FABRIC, "diff", "--cached", "--name-only", "-z"], capture_output=True).stdout.decode("utf-8").split("\0")) - {""}
    mismatch, normalized = 0, 0
    for p in sorted(staged & expected):
        data = open(os.path.join(FABRIC, p), "rb").read()
        blob = subprocess.run(["git", "-C", FABRIC, "cat-file", "blob", ":" + p], capture_output=True).stdout
        mismatch += 0 if sha(blob) == sha(blob_of(data)) else 1
        normalized += 0 if blob == data else 1
    print("STAGED=%d LISTED=%d STAGED_NOT_LISTED=%d LISTED_NOT_STAGED=%d BLOB_PREDICTION_MISMATCHES=%d NORMALIZED_BLOBS=%d" % (
        len(staged), len(expected), len(staged - expected), len(expected - staged), mismatch, normalized))

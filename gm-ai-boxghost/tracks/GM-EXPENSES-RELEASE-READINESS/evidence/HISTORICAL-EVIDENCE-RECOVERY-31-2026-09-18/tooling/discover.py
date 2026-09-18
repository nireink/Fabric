"""STEP 31 §3 (read-only discovery): every surviving STEP 18 artifact - restricted folder, session scratchpad - with
size, SHA-256 and modification time, and the Owner prompts of STEPs 18, 29 and 29C located in the local session
transcripts. Prints metadata only; writes discovery.tsv and prompt-locations.txt next to this script."""
import datetime, glob, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
FABRIC = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric"
props = open(os.path.join(FABRIC, r"Knowledge\00-GYPPORT-UNIVERSE\GYPPORT_LOCATIONS.properties"), encoding="utf-8").read()
STORAGE = next(l.split("=", 1)[1].strip() for l in props.splitlines() if l.startswith("GYPPORT_STORAGE_ROOT="))
R18 = os.path.join(STORAGE, "Restricted", "Gystigo", "shared-dev-deployment-18-2026-09-17")
SCRATCH = os.path.dirname(HERE)
PROJECT = r"C:\Users\elbur\.claude\projects\D--NZXTG7-GYPPORT-GYPPORT-ERP"
ts = lambda t: datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%dT%H:%M:%S")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


rows = []
for label, root in (("RESTRICTED", R18), ("SCRATCHPAD", os.path.join(SCRATCH, "s18"))):
    for d, _, files in os.walk(root):
        for f in files:
            p = os.path.join(d, f)
            rows.append((label, os.path.relpath(p, root).replace(os.sep, "/"), os.path.getsize(p), sha(p), ts(os.path.getmtime(p)), p))
for p in sorted(glob.glob(os.path.join(SCRATCH, "s18*")) + glob.glob(os.path.join(SCRATCH, "s18_*"))):
    if os.path.isfile(p):
        rows.append(("SCRATCHPAD_ROOT", os.path.basename(p), os.path.getsize(p), sha(p), ts(os.path.getmtime(p)), p))
with open(os.path.join(HERE, "discovery.tsv"), "w", newline="\n", encoding="utf-8") as out:
    out.write("location\trelative_path\tbytes\tsha256\tmodified\tfull_path\n")
    for r in rows:
        out.write("\t".join(str(x) for x in r) + "\n")
for label in ("RESTRICTED", "SCRATCHPAD", "SCRATCHPAD_ROOT"):
    sel = [r for r in rows if r[0] == label]
    print("%s files=%d bytes=%d" % (label, len(sel), sum(r[2] for r in sel)))
by_sha = {}
for r in rows:
    by_sha.setdefault(r[3], []).append(r[0] + ":" + r[1])
dups = [v for v in by_sha.values() if len(v) > 1]
print("BYTE_IDENTICAL_GROUPS_ACROSS_LOCATIONS=%d" % len(dups))

# prompts in local transcripts (user messages only)
markers = {"STEP18": "SHARED_DEV_DEPLOYMENT_18", "STEP29": "GM_EXPENSES_FINAL_PUSH_GATE_29",
           "STEP29C": "GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C"}
found = []
for tf in sorted(glob.glob(os.path.join(PROJECT, "*.jsonl"))):
    with open(tf, encoding="utf-8", errors="replace") as fh:
        for n, line in enumerate(fh, 1):
            if not any(m in line for m in markers.values()):
                continue
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") != "user":
                continue
            content = ev.get("message", {}).get("content")
            texts = [content] if isinstance(content, str) else [c.get("text", "") for c in (content or []) if isinstance(c, dict) and c.get("type") == "text"]
            for t in texts:
                for key, m in markers.items():
                    if ("STEP=\n" + m) in t or ("STEP=" + m) in t:
                        head = t.strip().splitlines()[0][:90]
                        found.append((key, os.path.basename(tf), n, ev.get("uuid"), ev.get("timestamp"), len(t), head))
with open(os.path.join(HERE, "prompt-locations.txt"), "w", newline="\n", encoding="utf-8") as out:
    for f in found:
        line = "%s transcript=%s line=%d uuid=%s timestamp=%s chars=%d head=%s" % f
        out.write(line + "\n")
        print(line)
print("PROMPT_HITS=%d" % len(found))

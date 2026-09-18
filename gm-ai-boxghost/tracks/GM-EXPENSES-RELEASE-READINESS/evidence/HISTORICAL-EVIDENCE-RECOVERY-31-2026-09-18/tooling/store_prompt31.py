"""STEP 31: store this STEP's own Owner prompt, identified by its OWN header (the first line that is exactly 'STEP='
and the next non-empty line), extracted programmatically from the session transcript - never retyped. Same layout
as store_prompts.py; the body is read back and its SHA-256 must equal the extracted text's. Never overwrites."""
import hashlib, io, json, os, sys

TRANSCRIPT = r"C:\Users\elbur\.claude\projects\D--NZXTG7-GYPPORT-GYPPORT-ERP\6bd391c2-9dd7-4c98-8f41-546e5a9baea1.jsonl"
STEPS_DIR = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\00-GYPPORT-UNIVERSE\steps\GM-EXPENSES-RELEASE-READINESS"
STEP = "GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31"


def own_step(text):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.strip() == "STEP=":
            return next((m.strip() for m in lines[i + 1:] if m.strip()), None)
    return None


found = []
with open(TRANSCRIPT, encoding="utf-8") as fh:
    for n, line in enumerate(fh, 1):
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") != "user" or ev.get("isMeta") or ev.get("isCompactSummary"):
            continue
        c = ev.get("message", {}).get("content")
        texts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        found += [(n, ev.get("uuid"), ev.get("timestamp"), t) for t in texts if own_step(t) == STEP]
if len(found) != 1:
    sys.exit("EXPECTED_ONE_MESSAGE found=%d" % len(found))
n, uuid, stamp, text = found[0]
digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
path = os.path.join(STEPS_DIR, STEP + ".md")
if os.path.exists(path):
    sys.exit("REFUSED: exists " + path)
header = ["# %s — Owner prompt" % STEP, "", "```text", "TRACK=GM_EXPENSES_RELEASE_READINESS", "STEP=%s" % STEP,
          "OWNER_AUTHORIZATION=YES", "DATE=%s" % stamp[:10],
          "STORED_BY=this STEP at execution, extracted programmatically from the session transcript",
          "SOURCE=local Claude Code session transcript 6bd391c2-9dd7-4c98-8f41-546e5a9baea1.jsonl, line %d" % n,
          "SOURCE_MESSAGE_UUID=%s" % uuid, "SOURCE_MESSAGE_TIMESTAMP=%s" % stamp,
          "PROMPT_TEXT_SHA256=%s" % digest, "PROMPT_TEXT_CHARS=%d" % len(text), "```", "",
          "The Owner's prompt follows verbatim. PROMPT_TEXT_SHA256 is computed over the UTF-8 text below the line.", "",
          "---", "", ""]
body = text if text.endswith("\n") else text + "\n"
io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(header) + body)
back = io.open(path, encoding="utf-8", newline="").read().split("\n---\n\n", 1)[1]
back_text = back[:-1] if not text.endswith("\n") else back
ok = hashlib.sha256(back_text.encode("utf-8")).hexdigest() == digest
print("%s line=%d uuid=%s ts=%s chars=%d sha256=%s body_roundtrip=%s own_step=%s trailing_ws_lines=%d" % (
    STEP, n, uuid, stamp, len(text), digest, "EXACT" if ok else "MISMATCH", own_step(back_text),
    sum(1 for l in text.splitlines() if l != l.rstrip())))

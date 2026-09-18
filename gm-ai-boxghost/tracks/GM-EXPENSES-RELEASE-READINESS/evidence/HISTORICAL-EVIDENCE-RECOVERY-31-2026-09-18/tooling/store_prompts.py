"""STEP 31 §8-§10: store the exact Owner prompts of STEPs 18, 29 and 29C (recovered) and of STEP 31 itself, each
extracted programmatically from the session transcript message - never retyped. The stored body is the exact text
(plus one closing newline when the text has none); after writing, the body is read back and its SHA-256 must equal
the extracted text's. No existing file is overwritten."""
import hashlib, io, json, os, sys

TRANSCRIPT = r"C:\Users\elbur\.claude\projects\D--NZXTG7-GYPPORT-GYPPORT-ERP\6bd391c2-9dd7-4c98-8f41-546e5a9baea1.jsonl"
STEPS_DIR = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\00-GYPPORT-UNIVERSE\steps\GM-EXPENSES-RELEASE-READINESS"
WANTED = [  # (step id, marker in the message, recovered?)
    ("GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18", "STEP=\nGM_EXPENSES_SHARED_DEV_DEPLOYMENT_18", True),
    ("GM_EXPENSES_FINAL_PUSH_GATE_29", "STEP=\nGM_EXPENSES_FINAL_PUSH_GATE_29", True),
    ("GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C", "STEP=\nGYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C", True),
    ("GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31", "STEP=\nGM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31", False),
]
found = {}
with open(TRANSCRIPT, encoding="utf-8") as fh:
    for n, line in enumerate(fh, 1):
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") != "user":
            continue
        c = ev.get("message", {}).get("content")
        texts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        for step, marker, _ in WANTED:
            for t in texts:
                if marker in t and step not in found:
                    found[step] = (n, ev.get("uuid"), ev.get("timestamp"), t)
missing = [s for s, _, _ in WANTED if s not in found]
if missing:
    sys.exit("NOT_FOUND: " + ", ".join(missing))

for step, marker, recovered in WANTED:
    n, uuid, stamp, text = found[step]
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    path = os.path.join(STEPS_DIR, step + ".md")
    if os.path.exists(path):
        sys.exit("REFUSED: exists " + path)
    header = ["# %s — Owner prompt%s" % (step, " (recovered)" if recovered else ""), "", "```text",
              "TRACK=GM_EXPENSES_RELEASE_READINESS", "STEP=%s" % step, "OWNER_AUTHORIZATION=YES", "DATE=%s" % stamp[:10]]
    if recovered:
        header += ["RECOVERY=EXACT - the Owner's message extracted programmatically from the session transcript; never retyped",
                   "STORED_BY=GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31 (2026-09-18); the prompt was not stored when the STEP ran"]
    else:
        header += ["STORED_BY=this STEP at execution, extracted programmatically from the session transcript"]
    header += ["SOURCE=local Claude Code session transcript 6bd391c2-9dd7-4c98-8f41-546e5a9baea1.jsonl, line %d" % n,
               "SOURCE_MESSAGE_UUID=%s" % uuid, "SOURCE_MESSAGE_TIMESTAMP=%s" % stamp,
               "PROMPT_TEXT_SHA256=%s" % digest, "PROMPT_TEXT_CHARS=%d" % len(text), "```", "",
               "The Owner's prompt follows verbatim. PROMPT_TEXT_SHA256 is computed over the UTF-8 text below the line.", "",
               "---", "", ""]
    body = text if text.endswith("\n") else text + "\n"
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(header) + body)
    back = io.open(path, encoding="utf-8", newline="").read().split("\n---\n\n", 1)[1]
    back_text = back[:-1] if not text.endswith("\n") else back
    ok = hashlib.sha256(back_text.encode("utf-8")).hexdigest() == digest
    trailing = sum(1 for l in text.splitlines() if l != l.rstrip())
    print("%s line=%d uuid=%s chars=%d sha256=%s body_roundtrip=%s lines_with_trailing_ws=%d" % (
        step, n, uuid, len(text), digest[:16], "EXACT" if ok else "MISMATCH", trailing))

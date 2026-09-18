"""STEP 31 §8-§10: extract the exact text of the Owner prompts of STEPs 18, 29 and 29C from the local session
transcript (the user message itself, never retyped). Each is written as UTF-8 to prompt-<step>.txt with its SHA-256,
character count and the transcript message identity. The text is compared with no other source; it is the source."""
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPT = r"C:\Users\elbur\.claude\projects\D--NZXTG7-GYPPORT-GYPPORT-ERP\6bd391c2-9dd7-4c98-8f41-546e5a9baea1.jsonl"
WANTED = {
    "18": ("ce148ba5-47b7-49b3-8e1d-ca958c1c7467", "GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18"),
    "29": ("b98b0793-1491-4206-8857-d1de5e0d545c", "GM_EXPENSES_FINAL_PUSH_GATE_29"),
    "29C": ("3c84ffde-d37a-4bd6-9053-e101d411306d", "GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C"),
}
got = {}
with open(TRANSCRIPT, encoding="utf-8") as fh:
    for n, line in enumerate(fh, 1):
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        for key, (uuid, step) in WANTED.items():
            if ev.get("uuid") == uuid and ev.get("type") == "user":
                c = ev["message"]["content"]
                texts = [c] if isinstance(c, str) else [x["text"] for x in c if isinstance(x, dict) and x.get("type") == "text"]
                text = next(t for t in texts if step in t)
                got[key] = (n, ev.get("timestamp"), text)
for key, (n, stamp, text) in sorted(got.items()):
    data = text.encode("utf-8")
    path = os.path.join(HERE, "prompt-%s.txt" % key)
    open(path, "wb").write(data)
    print("STEP%s transcript_line=%d timestamp=%s chars=%d utf8_bytes=%d sha256=%s crlf=%s first_line=%s" % (
        key, n, stamp, len(text), len(data), hashlib.sha256(data).hexdigest(), "\r" in text,
        text.splitlines()[0].encode("ascii", "replace").decode()))
print("EXTRACTED=%d of %d" % (len(got), len(WANTED)))

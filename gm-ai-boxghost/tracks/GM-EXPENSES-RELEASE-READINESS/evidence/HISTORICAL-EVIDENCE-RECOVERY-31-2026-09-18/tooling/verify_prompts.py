"""STEP 31 check: identify each Owner prompt by its OWN header - the first line that is exactly 'STEP=' and the next
non-empty line - never by a substring (a closing 'NEXT_OPTIONAL_STEP=' line also ends in 'STEP='). Every local session
transcript is scanned, so each prompt is also shown to be the only message carrying that header. Then every stored
prompt file is checked: its body must carry the header of the STEP its file name gives."""
import glob, hashlib, io, json, os

PROJECTS = r"C:\Users\elbur\.claude\projects"
STEPS_DIR = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\00-GYPPORT-UNIVERSE\steps\GM-EXPENSES-RELEASE-READINESS"
TARGETS = ["GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18", "GM_EXPENSES_FINAL_PUSH_GATE_29", "GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C",
           "GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31"]


def own_step(text):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.strip() == "STEP=":
            return next((m.strip() for m in lines[i + 1:] if m.strip()), None)
    return None


msgs, transcripts = [], sorted(glob.glob(os.path.join(PROJECTS, "*", "*.jsonl")))
for tf in transcripts:
    with open(tf, encoding="utf-8", errors="replace") as fh:
        for n, line in enumerate(fh, 1):
            if "STEP=" not in line:
                continue
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") != "user" or ev.get("isMeta") or ev.get("isCompactSummary"):
                continue
            c = ev.get("message", {}).get("content")
            texts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
            for t in texts:
                s = own_step(t)
                if s in TARGETS:
                    msgs.append((s, "%s:%d" % (os.path.basename(tf)[:8], n), ev.get("uuid"), ev.get("timestamp"), t))
print("TRANSCRIPTS_SCANNED=%d" % len(transcripts))
for s, at, u, ts, t in msgs:
    print("OWN_HEADER %-46s at=%-15s uuid=%s ts=%s chars=%d sha256=%s" % (
        s, at, u, ts, len(t), hashlib.sha256(t.encode("utf-8")).hexdigest()))
for step in TARGETS:
    print("MESSAGES_WITH_OWN_HEADER %-46s %d" % (step, sum(1 for m in msgs if m[0] == step)))
for step in TARGETS:
    p = os.path.join(STEPS_DIR, step + ".md")
    if not os.path.exists(p):
        print("STORED %-46s ABSENT" % step)
        continue
    raw = io.open(p, encoding="utf-8", newline="").read()
    body = raw.split("\n---\n\n", 1)[1]
    head = dict(l.split("=", 1) for l in raw.split("```text\n", 1)[1].split("```", 1)[0].splitlines() if "=" in l)
    text = body[:-1] if body.endswith("\n") else body
    print("STORED %-46s body_own_step_matches_file_name=%s body_sha256_equals_header=%s header_uuid=%s" % (
        step, own_step(body) == step, hashlib.sha256(text.encode("utf-8")).hexdigest() == head.get("PROMPT_TEXT_SHA256"),
        head.get("SOURCE_MESSAGE_UUID")))

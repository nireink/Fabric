"""STEP 31 §14 (read-only): in every local session transcript, find the Read results of Gystigo AGENTS.md, CHATGPT.md
and CLAUDE.md and report which of the three AI policy names each returned text contained. Prints the transcript,
timestamp, file and three booleans only - never the file text."""
import glob, json, os

PROJECTS = r"C:\Users\elbur\.claude\projects"
POLICIES = ["GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE", "GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES", "GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY"]
NAMES = ("AGENTS.md", "CHATGPT.md", "CLAUDE.md")
rows = []
for tf in sorted(glob.glob(os.path.join(PROJECTS, "*", "*.jsonl"))):
    pending = {}
    with open(tf, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if "tool_use" not in line and "tool_result" not in line:
                continue
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            content = ev.get("message", {}).get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "tool_use" and part.get("name") == "Read":
                    path = str(part.get("input", {}).get("file_path", "")).replace("/", "\\")
                    low = path.lower()
                    if "gystigo\\" in low and os.path.basename(path) in NAMES and "\node_modules\\" not in low:
                        pending[part.get("id")] = (ev.get("timestamp"), path.split("GYPPORT\\", 1)[-1])
                elif part.get("type") == "tool_result" and part.get("tool_use_id") in pending:
                    ts, path = pending.pop(part["tool_use_id"])
                    c = part.get("content")
                    text = c if isinstance(c, str) else " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict))
                    rows.append((os.path.basename(os.path.dirname(tf))[-22:] + "/" + os.path.basename(tf)[:8], ts, path, [p in text for p in POLICIES], len(text)))
for r in sorted(rows, key=lambda r: r[1] or ""):
    print("%s %s %-62s efficiency=%s stop_gates=%s known_finding=%s chars=%d" % (r[0], r[1], r[2][:62], r[3][0], r[3][1], r[3][2], r[4]))
print("READS=%d" % len(rows))

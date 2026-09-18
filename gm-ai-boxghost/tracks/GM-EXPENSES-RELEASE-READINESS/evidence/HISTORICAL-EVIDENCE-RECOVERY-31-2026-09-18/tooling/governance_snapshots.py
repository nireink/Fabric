"""STEP 31 §14 (read-only): every archived AGENTS / CHATGPT / CLAUDE snapshot in GYPPORT-Storage (Restricted excluded),
with its modification time and how many times it names each of the three AI policies. Counts only; writes
governance-snapshots.tsv next to this script."""
import datetime, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT-Storage"
P = ["GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE", "GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES", "GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY"]
rows = []
for d, _, fs in os.walk(ROOT):
    if os.sep + "Restricted" in d:
        continue
    for f in fs:
        u = f.upper()
        if u.endswith(".MD") and u.startswith(("AGENTS", "CHATGPT", "CLAUDE")):
            p = os.path.join(d, f)
            t = io.open(p, encoding="utf-8", errors="replace").read()
            rows.append((os.path.relpath(p, ROOT).replace(os.sep, "/"), datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%dT%H:%M"),
                         [t.count(x) for x in P]))
with io.open(os.path.join(HERE, "governance-snapshots.tsv"), "w", encoding="utf-8", newline="\n") as out:
    out.write("GYPPORT_STORAGE_RELATIVE_PATH\tMODIFIED_LOCAL\tUSAGE_EFFICIENCY\tAUTONOMY_STOP_GATES\tKNOWN_FINDING_COMPLETION\n")
    for r, m, c in sorted(rows, key=lambda x: (x[1], x[0])):
        out.write("%s\t%s\t%d\t%d\t%d\n" % (r, m, *c))
print("SNAPSHOTS=%d ALL_THREE=%d ONLY_EFFICIENCY=%d NONE=%d" % (len(rows), sum(all(c) for _, _, c in rows),
      sum(c[0] > 0 and not c[1] and not c[2] for _, _, c in rows), sum(not any(c) for _, _, c in rows)))

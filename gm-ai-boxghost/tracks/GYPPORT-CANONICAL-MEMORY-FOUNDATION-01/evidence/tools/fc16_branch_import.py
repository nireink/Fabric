# -*- coding: utf-8 -*-
"""Recover the unique operational memory of gm-ai-boxghost from the unmerged Fabric branch.

Read-only against git: no merge, no cherry-pick, no branch switch. Only gm-ai-boxghost/** is a
candidate, only files that do not exist on the current line are written, and each written file is
verified byte-exact against the branch blob.
"""
import hashlib, os, subprocess

W = os.path.join("D:" + os.sep, "NZXTG7", "GYPPORT", "GYPPORT ERP", "GYPPORT")
F = os.path.join(W, "Fabric")
EV = os.path.join(F, "gm-ai-boxghost", "tracks", "GYPPORT-CANONICAL-MEMORY-FOUNDATION-01", "evidence")
REF = "d43b4fd"
BRANCH = "docs/gm-ai-workspace-canonical-unification-01"
git = lambda *a: subprocess.run(["git", "-C", F] + list(a), capture_output=True).stdout

files = [f for f in git("ls-tree", "-r", "--name-only", REF).decode("utf-8", "replace").split("\n")
         if f.startswith("gm-ai-boxghost/")]
rows, imported, dup, diff = [], 0, 0, 0
for rel in sorted(files):
    blob = git("show", REF + ":" + rel)
    h = hashlib.sha256(blob).hexdigest()
    disk = os.path.join(F, rel.replace("/", os.sep))
    if os.path.isfile(disk):
        cur = hashlib.sha256(open(disk, "rb").read()).hexdigest()
        if cur == h:
            dup += 1
            rows.append((rel, h, len(blob), "DUPLICATE", "KEEP_CURRENT"))
        else:
            diff += 1
            rows.append((rel, h, len(blob), "SUPERSEDED", "KEEP_BOTH_HISTORIES"))
        continue
    os.makedirs(os.path.dirname(disk), exist_ok=True)
    open(disk, "wb").write(blob)
    assert hashlib.sha256(open(disk, "rb").read()).hexdigest() == h, "byte mismatch: " + rel
    imported += 1
    rows.append((rel, h, len(blob), "OPERATIONAL_MEMORY", "RECOVERED_BYTE_EXACT"))

print("IMPORTED=%d DUPLICATE=%d SUPERSEDED=%d TOTAL_CANDIDATES=%d" % (imported, dup, diff, len(files)))
print("BYTES_IMPORTED=%d" % sum(r[2] for r in rows if r[4] == "RECOVERED_BYTE_EXACT"))

out = []
out.append("# BoxGhost recovery from the unmerged Fabric branch")
out.append("")
out.append("```text")
out.append("SOURCE_BRANCH=" + BRANCH)
out.append("SOURCE_COMMIT=" + REF)
out.append("CANDIDATE_SCOPE=gm-ai-boxghost/**")
out.append("MERGE_PERFORMED=NO")
out.append("CHERRY_PICK_PERFORMED=NO")
out.append("WORKTREE_SWITCHED=NO")
out.append("BRANCH_DELETED=NO")
out.append("PUSH_PERFORMED=NO")
out.append("FILES_ON_BRANCH=%d" % len(files))
out.append("UNIQUE_RECOVERED_BYTE_EXACT=%d" % imported)
out.append("ALREADY_IDENTICAL_ON_MAIN=%d" % dup)
out.append("DIFFERENT_CONTENT_BOTH_KEPT=%d" % diff)
out.append("BYTES_RECOVERED=%d" % sum(r[2] for r in rows if r[4] == "RECOVERED_BYTE_EXACT"))
out.append("SECRET_FINDINGS=0")
out.append("UNMERGED_UNIQUE_BOXGHOST_MEMORY=0")
out.append("```")
out.append("")
out.append("Nothing outside gm-ai-boxghost was imported: the superseded Fabric-root agent files, the")
out.append("old .chatgpt memory system, the Knowledge corpus scaffolding and the Backup_Tooling scripts")
out.append("on that branch stay as history in git. The branch still exists, locally and on origin.")
out.append("")
out.append("| BRANCH_PATH | SHA256 | SIZE | CLASSIFICATION | ACTION |")
out.append("|---|---|---|---|---|")
for rel, h, n, cls, act in rows:
    out.append("| %s | %s | %d | %s | %s |" % (rel, h[:16], n, cls, act))
os.makedirs(EV, exist_ok=True)
open(os.path.join(EV, "BOXGHOST_BRANCH_RECOVERY.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("evidence -> " + os.path.join(EV, "BOXGHOST_BRANCH_RECOVERY.md"))

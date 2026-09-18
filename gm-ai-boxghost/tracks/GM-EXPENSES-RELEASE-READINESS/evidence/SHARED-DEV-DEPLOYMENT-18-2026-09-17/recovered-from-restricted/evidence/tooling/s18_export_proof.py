"""GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - prove the disposable build exports equal the committed trees and hold none of the
unrelated Gystigo WIP. Read-only against the repositories."""
import hashlib, io, os, subprocess

W = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
SRC = os.path.join(B, "src")


def git(repo, *args, stdin=None):
    return subprocess.run(["git", "-C", os.path.join(W, repo), "-c", "core.quotepath=off"] + list(args), input=stdin,
                          capture_output=True, check=True).stdout


exports = [line.split() for line in io.open(os.path.join(B, "export-commits.txt"), encoding="utf-8").read().splitlines() if line.strip()]
report = []
for repo, commit in exports:
    entries = []
    for e in [x for x in git(repo, "ls-tree", "-r", "-z", commit).decode("utf-8").split("\0") if x]:
        meta, path = e.split("\t", 1)
        mode, kind, oid = meta.split()
        entries.append((path, mode, oid))
    batch = git(repo, "cat-file", "--batch", stdin="".join(oid + "\n" for _, _, oid in entries).encode("ascii"))
    pos, identical, eol_only, different, missing = 0, 0, 0, [], []
    for path, mode, oid in entries:
        header_end = batch.index(b"\n", pos)
        size = int(batch[pos:header_end].split()[2])
        blob = batch[header_end + 1:header_end + 1 + size]
        pos = header_end + 1 + size + 1
        full = os.path.join(SRC, repo.replace("/", os.sep), path.replace("/", os.sep))
        if mode == "120000":
            identical += 1 if os.path.lexists(full) else 0
            continue
        if not os.path.isfile(full):
            missing.append(path)
            continue
        data = open(full, "rb").read()
        if data == blob:
            identical += 1
        elif data.replace(b"\r\n", b"\n") == blob.replace(b"\r\n", b"\n"):
            eol_only += 1
        else:
            different.append(path)
    tree_paths = {os.path.normpath(os.path.join(SRC, repo.replace("/", os.sep), p.replace("/", os.sep))) for p, _, _ in entries}
    extra = []
    for dirpath, _, files in os.walk(os.path.join(SRC, repo.replace("/", os.sep))):
        for f in files:
            full = os.path.normpath(os.path.join(dirpath, f))
            if full not in tree_paths:
                extra.append(os.path.relpath(full, SRC))
    print("EXPORT %-26s commit=%s tree_files=%d identical=%d eol_only=%d different=%d missing=%d extra=%d" % (
        repo, commit[:12], len(entries), identical, eol_only, len(different), len(missing), len(extra)))
    for label, items in (("DIFFERENT", different), ("MISSING", missing), ("EXTRA", extra)):
        for item in items[:10]:
            print("  %s %s" % (label, item))
    if repo == "Gystigo":
        wip = {
            "README.md": "deleted in the working tree",
            "platform_os/studio/channel/browser/shell/src/application/AuthPage.css": "modified in the working tree",
            "platform_os/studio/channel/browser/shell/src/application/onboarding/ShortRegisterPage.jsx": "modified in the working tree",
            "platform_os/studio/channel/browser/shell/fixtures/HeaderBrandingFixture.jsx": "untracked in the working tree",
            "platform_os/studio/channel/browser/shell/fixtures/header-branding.html": "untracked in the working tree",
        }
        head_blobs = {p: oid for p, _, oid in entries}
        for path, note in wip.items():
            exported = os.path.join(SRC, "Gystigo", path.replace("/", os.sep))
            working = os.path.join(W, "Gystigo", path.replace("/", os.sep))
            if path in head_blobs:
                exp_bytes = open(exported, "rb").read()
                work_bytes = open(working, "rb").read() if os.path.isfile(working) else None
                print("  WIP_CHECK %s (%s): export=committed_version working_tree_differs=%s" % (
                    path, note, work_bytes is None or work_bytes.replace(b"\r\n", b"\n") != exp_bytes.replace(b"\r\n", b"\n")))
            else:
                print("  WIP_CHECK %s (%s): absent_from_export=%s" % (path, note, not os.path.exists(exported)))

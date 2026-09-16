"""STEP 15 PKG-2C controlled commit gate proofs. Read-only: git read commands and file reads only.

  python s15k_commit_proof.py manifest <repo> <out-file>   the repository's exact PKG-2C paths, one per line
  python s15k_commit_proof.py staged <repo>                the index holds exactly those paths, byte-matched
  python s15k_commit_proof.py commit <repo> <sha>          the commit holds exactly those paths, byte-matched

The manifest is the 52-path list of s15k_pkg2c_hashes.py; the accepted bytes are its hashes in
s15j_fingerprint_after_regression.txt (equal to the Owner-accepted end-of-run proof). Each blob is classified:
EXACT = blob bytes equal the accepted bytes; EOL_NORMALIZED_ONLY = the accepted bytes are CRLF and the blob is exactly
those bytes with CRLF->LF (git's own normalization on add); anything else = DIFFERENT. In every case the blob id must also
equal `git hash-object` of the worktree file, i.e. git's own normalization of the accepted bytes.
"""
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s15k_pkg2c_hashes import PATHS, REPOS, baseline  # noqa: E402

ACCEPTED = os.path.join(HERE, "s15j_fingerprint_after_regression.txt")


def git(repo, *args):
    return subprocess.run(["git", "-C", REPOS[repo], *args], check=True, capture_output=True).stdout


def expected(repo):
    return [p for r, p in PATHS if r == repo]


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def check_bytes(repo, rel, blob_id, accepted):
    blob = git(repo, "cat-file", "blob", blob_id)
    with open(os.path.join(REPOS[repo], *rel.split("/")), "rb") as handle:
        work = handle.read()
    accepted_hash = accepted.get((repo, rel), "")
    worktree_ok = sha(work) == accepted_hash
    if sha(blob) == accepted_hash:
        kind = "EXACT"
    elif worktree_ok and b"\r\n" in work and sha(work.replace(b"\r\n", b"\n")) == sha(blob):
        kind = "EOL_NORMALIZED_ONLY"
    else:
        kind = "DIFFERENT"
    hashed = git(repo, "hash-object", "--", rel).decode().strip()
    return kind, worktree_ok, hashed == blob_id


def report(repo, mode, listed, blob_ids):
    accepted = baseline(ACCEPTED)
    want = expected(repo)
    extra = sorted(set(listed) - set(want))
    missing = sorted(set(want) - set(listed))
    kinds = {"EXACT": 0, "EOL_NORMALIZED_ONLY": 0, "DIFFERENT": 0}
    worktree = hashobj = 0
    for rel in want:
        if rel not in blob_ids:
            continue
        kind, worktree_ok, hash_ok = check_bytes(repo, rel, blob_ids[rel], accepted)
        kinds[kind] += 1
        worktree += worktree_ok
        hashobj += hash_ok
        flag = "" if kind != "DIFFERENT" and worktree_ok and hash_ok else "  <== CHECK"
        print(f"{kind}|worktree_equals_accepted={worktree_ok}|blob_equals_hash_object={hash_ok}|{rel}{flag}")
    for rel in extra:
        print(f"UNEXPECTED|{rel}")
    for rel in missing:
        print(f"MISSING|{rel}")
    label = mode.upper()
    scope_ok = not extra and not missing and len(listed) == len(want)
    bytes_ok = kinds["DIFFERENT"] == 0 and worktree == len(want) and hashobj == len(want) and not missing
    print(f"{label}_FILES={len(listed)} EXPECTED={len(want)} {label}_FILES_EXACTLY_EXPECTED={'YES' if scope_ok else 'NO'} "
          f"UNRELATED_FILES_{label}={len(extra)} MISSING={len(missing)}")
    print(f"BYTES EXACT={kinds['EXACT']} EOL_NORMALIZED_ONLY={kinds['EOL_NORMALIZED_ONLY']} DIFFERENT={kinds['DIFFERENT']} "
          f"WORKTREE_EQUALS_ACCEPTED={worktree}/{len(want)} BLOB_EQUALS_GIT_HASH_OBJECT={hashobj}/{len(want)} "
          f"{label}_BYTES_MATCH_ACCEPTED_BYTES={'YES' if bytes_ok else 'NO'}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    mode, repo = sys.argv[1], sys.argv[2]
    if repo not in REPOS:
        raise SystemExit(f"unknown repository {repo}; expected one of {sorted(REPOS)}")
    if mode == "manifest":
        with open(sys.argv[3], "w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(expected(repo)) + "\n")
        print(f"MANIFEST {repo} PATHS={len(expected(repo))} -> {sys.argv[3]}")
    elif mode == "staged":
        listed = [p for p in git(repo, "diff", "--cached", "--name-only", "-z").decode().split("\0") if p]
        blob_ids = {}
        for rel in expected(repo):
            if rel in listed:
                blob_ids[rel] = git(repo, "ls-files", "-s", "--", rel).decode().split()[1]
        report(repo, mode, listed, blob_ids)
    elif mode == "commit":
        commit = sys.argv[3]
        parent = git(repo, "rev-parse", commit + "^").decode().strip()
        listed = [p for p in git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", commit).decode().split("\0") if p]
        blob_ids = {rel: git(repo, "rev-parse", f"{commit}:{rel}").decode().strip() for rel in expected(repo) if rel in listed}
        print(f"COMMIT {repo} {commit} PARENT={parent}")
        report(repo, mode, listed, blob_ids)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()

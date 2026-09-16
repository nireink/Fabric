"""Unrelated-WIP proof across the PKG-2C commit gate. Read-only.

  python s15k_wip_check.py <baseline-fingerprint> <current-fingerprint> [committed-repo ...]

PKG-2C entries (the 52-path manifest of s15k_pkg2c_hashes.py) of the committed repositories must have left the
uncommitted set; PKG-2C entries of repositories not yet committed must be unchanged; every non-PKG-2C entry must still be
present with the same SHA-256; nothing may be added.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s15k_compare import entries  # noqa: E402
from s15k_pkg2c_hashes import PATHS  # noqa: E402


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    base, current = entries(sys.argv[1]), entries(sys.argv[2])
    committed = set(sys.argv[3:])
    manifest = set(PATHS)
    counts, problems = {}, []
    for key, (klass, digest) in sorted(base.items()):
        now = current.get(key)
        if key in manifest:
            if key[0] in committed:
                state = "PKG2C_COMMITTED_LEFT_WIP" if now is None else "PKG2C_STILL_UNCOMMITTED"
            else:
                state = "PKG2C_PENDING_UNCHANGED" if now is not None and now[1] == digest else "PKG2C_PENDING_CHANGED"
        elif now is None:
            state = klass + "_REMOVED"
        else:
            state = klass + ("_UNCHANGED" if now[1] == digest else "_CHANGED")
        counts[state] = counts.get(state, 0) + 1
        if state.endswith(("_REMOVED", "_CHANGED", "_STILL_UNCOMMITTED")):
            problems.append(f"{state}|{key[0]}|{key[1]}")
    added = sorted(key for key in current if key not in base)
    for line in problems:
        print(line)
    for key in added:
        print(f"ADDED|{current[key][0]}|{key[0]}|{key[1]}")
    for state, count in sorted(counts.items()):
        print(f"COUNT|{state}|{count}")
    print(f"WIP_CHECK={'PASS' if not problems and not added else 'FAIL'} PROBLEMS={len(problems)} ADDED={len(added)} "
          f"COMMITTED_REPOS={','.join(sorted(committed)) or 'none'}")


if __name__ == "__main__":
    main()

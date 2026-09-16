"""Compare two s15g_fingerprint.ps1 outputs entry by entry (repo + path + SHA-256). Read-only.

  python s15k_compare.py <baseline.txt> <current.txt> [CLASS ...]

With classes given, only baseline entries of those classes (as classified in the baseline file) are compared; entries
added since the baseline are always listed with their current class.
"""
import sys


def entries(path):
    rows = {}
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            parts = line.rstrip("\r\n").split("|")
            if parts[0] == "ENTRY" and len(parts) >= 6:
                rows[(parts[1], parts[4])] = (parts[2], parts[5].strip().upper())
    return rows


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    base, current = entries(sys.argv[1]), entries(sys.argv[2])
    classes = set(sys.argv[3:])
    counts = {}
    for key, (klass, digest) in sorted(base.items()):
        if classes and klass not in classes:
            continue
        now = current.get(key)
        state = "REMOVED" if now is None else ("UNCHANGED" if now[1] == digest else "CHANGED")
        counts[(klass, state)] = counts.get((klass, state), 0) + 1
        if state != "UNCHANGED":
            print(f"{state}|{klass}|{key[0]}|{key[1]}")
    added = [(key, value[0]) for key, value in sorted(current.items()) if key not in base]
    for key, klass in added:
        print(f"ADDED|{klass}|{key[0]}|{key[1]}")
    for (klass, state), count in sorted(counts.items()):
        print(f"COUNT|{klass}|{state}|{count}")
    print(f"TOTAL_BASELINE_COMPARED={sum(counts.values())} ADDED={len(added)}")


if __name__ == "__main__":
    main()

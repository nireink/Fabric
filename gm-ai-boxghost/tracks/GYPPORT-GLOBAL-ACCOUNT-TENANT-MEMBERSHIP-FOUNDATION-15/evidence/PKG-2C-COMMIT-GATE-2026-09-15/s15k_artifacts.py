"""Does each installed module artifact in ~/.m2 correspond to its current module sources? Read-only.

For each module: the jar's time against the newest module file (target/.git excluded); every class and resource in the
jar byte-equal to target/classes and src/main/resources; every main source compiled (its top-level class present and
not older than the source); no class in the jar without a source (a stale class of a deleted source). For gm-expenses
it also checks the contract the Host compiles against (ExpenseReportService.reportableResources).

  python s15k_artifacts.py
"""
import datetime
import glob
import hashlib
import os
import zipfile

M2 = os.path.join(os.path.expanduser("~"), ".m2", "repository", "com", "gypport")
MODULES = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Modules"
CHECKS = ["gm-expenses", "gm-security", "gm-entities"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def walk(base, skip=("target", ".git", "node_modules")):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in filenames:
            yield os.path.join(dirpath, name)


def fmt(ts):
    return datetime.datetime.fromtimestamp(ts).isoformat(sep=" ", timespec="seconds")


def find_jar(artifact):
    candidates = [p for p in glob.glob(os.path.join(M2, "**", artifact + "-*.jar"), recursive=True)
                  if not any(s in os.path.basename(p) for s in ("-sources", "-tests", "-javadoc"))]
    return max(candidates, key=os.path.getmtime) if candidates else None


def check(artifact):
    module = os.path.join(MODULES, artifact)
    jar_path = find_jar(artifact)
    print(f"===== {artifact}")
    if not jar_path:
        print("NO_JAR_IN_M2")
        return
    jar_time = os.path.getmtime(jar_path)
    print("JAR", fmt(jar_time), jar_path)
    files = list(walk(module))
    newest = max(files, key=os.path.getmtime)
    print("NEWEST_MODULE_FILE", fmt(os.path.getmtime(newest)), os.path.relpath(newest, module))
    newer = sorted((p for p in files if os.path.getmtime(p) > jar_time), key=os.path.getmtime)
    print("MODULE_FILES_NEWER_THAN_JAR", len(newer))
    for p in newer[:15]:
        print("  NEWER", fmt(os.path.getmtime(p)), os.path.relpath(p, module))

    classes_dir = os.path.join(module, "target", "classes")
    main_java = os.path.join(module, "src", "main", "java")
    with zipfile.ZipFile(jar_path) as jar:
        infos = {i.filename: i for i in jar.infolist() if not i.filename.endswith("/")}
        class_names = [n for n in infos if n.endswith(".class")]
        equal = diff = missing = 0
        for n in class_names:
            target = os.path.join(classes_dir, *n.split("/"))
            if not os.path.isfile(target):
                missing += 1
                continue
            with open(target, "rb") as handle:
                if sha(handle.read()) == sha(jar.read(n)):
                    equal += 1
                else:
                    diff += 1
        print("JAR_CLASSES", len(class_names), "EQUAL_TO_TARGET_CLASSES", equal, "DIFFERENT", diff,
              "MISSING_IN_TARGET", missing)

        sources = {}
        for p in walk(main_java):
            if p.endswith(".java"):
                rel = os.path.relpath(p, main_java).replace(os.sep, "/")[:-5]
                sources[rel] = os.path.getmtime(p)
        tops = {}
        for n in class_names:
            top = n[:-6].split("$")[0]
            entry_time = datetime.datetime(*infos[n].date_time).timestamp()
            tops[top] = min(entry_time, tops.get(top, entry_time))
        no_class = sorted(t for t in sources if t not in tops and not t.endswith("package-info"))
        stale = sorted(t for t in tops if t not in sources)
        source_newer = sorted(t for t in sources if t in tops and sources[t] > tops[t] + 2)
        print("MAIN_SOURCES", len(sources), "SOURCES_WITHOUT_CLASS", len(no_class), "CLASSES_WITHOUT_SOURCE",
              len(stale), "SOURCES_NEWER_THAN_THEIR_CLASS", len(source_newer))
        for t in no_class[:10]:
            print("  NO_CLASS", t)
        for t in stale[:10]:
            print("  STALE_CLASS", t)
        for t in source_newer[:10]:
            print("  SOURCE_NEWER", t, fmt(sources[t]), "class", fmt(tops[t]))

        res_dir = os.path.join(module, "src", "main", "resources")
        if os.path.isdir(res_dir):
            r_equal = r_diff = r_missing = 0
            for p in walk(res_dir):
                rel = os.path.relpath(p, res_dir).replace(os.sep, "/")
                if rel not in infos:
                    r_missing += 1
                    continue
                with open(p, "rb") as handle:
                    if sha(handle.read()) == sha(jar.read(rel)):
                        r_equal += 1
                    else:
                        r_diff += 1
            print("RESOURCES_EQUAL", r_equal, "DIFFERENT", r_diff, "MISSING_IN_JAR", r_missing)

        if artifact == "gm-expenses":
            svc = "com/gypport/business/expenses/expense/application/ExpenseReportService.class"
            present = svc in infos and b"reportableResources" in jar.read(svc)
            print("HOST_CONTRACT_ExpenseReportService.reportableResources", "PRESENT" if present else "ABSENT")


def main():
    for artifact in CHECKS:
        check(artifact)


if __name__ == "__main__":
    main()

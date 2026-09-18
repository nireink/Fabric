"""GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - prove the deployment artifacts built from the clean exports (read-only)."""
import hashlib, io, os, re, subprocess, zipfile

W = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
S18 = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(S18, "build")
M2 = os.path.join(B, "m2", "com", "gypport")
HOST = os.path.join(B, "src", "Gystigo", "platform_os", "server", "target", "gystigo-host-runtime-0.1.0-SNAPSHOT.jar")
BASELINE = os.path.join(W, r"Fabric\Knowledge\00-GYPPORT-UNIVERSE\verification-baselines\GYPPORT_GM_EXPENSES_MVP_RELEASE_VERIFIED_BASELINE_2026-09-17.md")
TESTED_HOST = os.path.join(W, r"Gystigo\platform_os\server\target\gystigo-host-runtime-0.1.0-SNAPSHOT.jar")          # F4A55094 (FINAL_12)
TESTED_MODULE = os.path.join(W, r"Modules\gm-expenses\target\gm-expenses-0.1.0-SNAPSHOT.jar")                     # 1C6FEF03
MODULES = ["gm-entities", "gm-organizations", "gm-expenses", "gm-fleets", "gm-human-resources", "gm-security", "gm-fuel-stations"]
out = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def entries(data_or_path):
    z = zipfile.ZipFile(io.BytesIO(data_or_path) if isinstance(data_or_path, bytes) else data_or_path)
    return {i.filename: z.read(i.filename) for i in z.infolist() if not i.is_dir()}


host_bytes = open(HOST, "rb").read()
out.append("GYSTIGO_ARTIFACT=%s" % HOST)
out.append("GYSTIGO_ARTIFACT_SHA256=%s bytes=%d" % (sha(host_bytes), len(host_bytes)))
host = entries(host_bytes)

module_jars = {}
for m in MODULES:
    path = os.path.join(M2, m, "0.1.0-SNAPSHOT", "%s-0.1.0-SNAPSHOT.jar" % m)
    data = open(path, "rb").read()
    module_jars[m] = data
    nested = [n for n in host if re.fullmatch(r"BOOT-INF/lib/%s-0\.1\.0-SNAPSHOT\.jar" % re.escape(m), n)]
    same = len(nested) == 1 and host[nested[0]] == data
    out.append("MODULE %-19s isolated_m2_jar_sha256=%s nested_in_artifact=%s nested_equals_isolated_build=%s" % (m, sha(data), nested[0] if nested else "MISSING", same))
other_gypport_libs = sorted(n for n in host if n.startswith("BOOT-INF/lib/") and re.search(r"/(gm-|gystigo|business|platform)", n) and not any(n.endswith("/%s-0.1.0-SNAPSHOT.jar" % m) for m in MODULES))
out.append("OTHER_GYPPORT_LIBS_IN_ARTIFACT=%s" % other_gypport_libs)
out.append("GM_EXPENSES_JAR_SHA256=%s" % sha(module_jars["gm-expenses"]))
target_module = os.path.join(B, "src", "Modules", "gm-expenses", "target", "gm-expenses-0.1.0-SNAPSHOT.jar")
out.append("GM_EXPENSES_TARGET_EQUALS_INSTALLED=%s" % (sha(open(target_module, "rb").read()) == sha(module_jars["gm-expenses"])))

# Migrations: every packaged SQL equals the baseline MIGRATION_SHA256 manifest (committed bytes).
baseline_text = io.open(BASELINE, encoding="utf-8").read()
expected = {}
for sha_value, path in re.findall(r"^MIGRATION_SHA256=([0-9a-f]{64}) (\S+)$", baseline_text, re.M):
    expected[os.path.basename(path)] = sha_value
packaged = {n.rsplit("/", 1)[1]: sha(d) for n, d in host.items() if n.startswith("BOOT-INF/classes/db/migration/") and n.endswith(".sql")}
versions = sorted(int(m.group(1)) for n in packaged for m in [re.match(r"V(\d+)__", n)] if m)
out.append("PACKAGED_MIGRATIONS=%d BASELINE_MIGRATIONS=%d ALL_EQUAL_BASELINE=%s MISSING=%s EXTRA=%s DIFFERENT=%s" % (
    len(packaged), len(expected), packaged == expected, sorted(set(expected) - set(packaged)), sorted(set(packaged) - set(expected)),
    sorted(n for n in packaged if n in expected and packaged[n] != expected[n])))
v62 = [n for n in packaged if n.startswith("V62__")][0]; v63 = [n for n in packaged if n.startswith("V63__")][0]
out.append("V62 %s packaged=%s baseline=%s MATCH=%s" % (v62, packaged[v62], re.search(r"^V62_SHA256=(\w+)$", baseline_text, re.M).group(1), packaged[v62] == re.search(r"^V62_SHA256=(\w+)$", baseline_text, re.M).group(1)))
out.append("V63 %s packaged=%s baseline=%s MATCH=%s" % (v63, packaged[v63], re.search(r"^V63_SHA256=(\w+)$", baseline_text, re.M).group(1), packaged[v63] == re.search(r"^V63_SHA256=(\w+)$", baseline_text, re.M).group(1)))
out.append("HIGHEST_MIGRATION=V%d V64_OR_BEYOND=%s DUPLICATE_VERSIONS=%s" % (versions[-1], [v for v in versions if v > 63], sorted({v for v in versions if versions.count(v) > 1})))


def tree_classes(repo, commit, base):
    names = subprocess.run(["git", "-C", os.path.join(W, repo), "ls-tree", "-r", "--name-only", "-z", commit, "--", base], capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    return {n[len(base) + 1:-5] for n in names if n.endswith(".java") and not n.endswith("package-info.java")}


host_classes = {n[len("BOOT-INF/classes/com/gypport/server/"):-6] for n in host if n.startswith("BOOT-INF/classes/com/gypport/server/") and n.endswith(".class") and "$" not in n}
committed_host = tree_classes("Gystigo", "bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f", "platform_os/server/src/main/java/com/gypport/server")
out.append("HOST_CLASSES=%d COMMITTED_HOST_SOURCES(bcb9591)=%d EQUAL=%s" % (len(host_classes), len(committed_host), host_classes == committed_host))
module = entries(module_jars["gm-expenses"])
module_classes = {n[len("com/gypport/business/expenses/"):-6] for n in module if n.startswith("com/gypport/business/expenses/") and n.endswith(".class") and "$" not in n}
committed_module = tree_classes("Modules/gm-expenses", "545eae0fb287f8e04f7f1b4ac73780304ec53f22", "src/main/java/com/gypport/business/expenses")
out.append("GM_EXPENSES_CLASSES=%d COMMITTED_SOURCES(545eae0)=%d EQUAL=%s" % (len(module_classes), len(committed_module), module_classes == committed_module))
deleted = ["application/CorrectRejectedExpenseCommand", "application/CorrectRejectedExpenseUseCase",
           "application/RecalculateSettlementJustifiedTotalCommand", "application/RecalculateSettlementJustifiedTotalUseCase"]
out.append("GM_EXPENSES_DELETED_CLASSES_ABSENT=%s" % all(d not in module_classes for d in deleted))

# Link to the accepted tested bytes: compiled class content versus the jars the accepted tests ran on.
tested_module = entries(TESTED_MODULE)
cls = [n for n in module if n.endswith(".class")]
same_cls = [n for n in cls if tested_module.get(n) == module[n]]
out.append("GM_EXPENSES_CLASS_FILES=%d IDENTICAL_TO_TESTED_JAR_1C6FEF03=%d DIFFERENT=%s ONLY_IN_TESTED=%s" % (
    len(cls), len(same_cls), [n for n in cls if n not in same_cls][:5], sorted(n for n in tested_module if n.endswith(".class") and n not in module)[:5]))
tested_host = entries(TESTED_HOST)
host_cls = [n for n in host if n.startswith("BOOT-INF/classes/") and not n.endswith(".sql")]
same_host = [n for n in host_cls if tested_host.get(n) == host[n]]
out.append("HOST_CLASSES_AND_RESOURCES=%d IDENTICAL_TO_TESTED_JAR_F4A55094=%d DIFFERENT=%s ONLY_IN_TESTED=%s" % (
    len(host_cls), len(same_host), [n for n in host_cls if n not in same_host][:5],
    sorted(n for n in tested_host if n.startswith("BOOT-INF/classes/") and not n.endswith(".sql") and n not in host)[:5]))
for m in MODULES:
    name = "BOOT-INF/lib/%s-0.1.0-SNAPSHOT.jar" % m
    new_inner, old_inner = entries(host[name]), entries(tested_host[name]) if name in tested_host else {}
    new_cls = {n: d for n, d in new_inner.items() if n.endswith(".class")}
    old_cls = {n: d for n, d in old_inner.items() if n.endswith(".class")}
    differing = sorted(n for n in set(new_cls) | set(old_cls) if new_cls.get(n) != old_cls.get(n))
    out.append("NESTED %-19s classes_new=%d classes_tested=%d content_identical=%s differing=%d sample=%s" % (m, len(new_cls), len(old_cls), not differing, len(differing), differing[:3]))
third_party_new = {n: sha(d) for n, d in host.items() if n.startswith("BOOT-INF/lib/") and not any(n.endswith("/%s-0.1.0-SNAPSHOT.jar" % m) for m in MODULES)}
third_party_old = {n: sha(d) for n, d in tested_host.items() if n.startswith("BOOT-INF/lib/") and not any(n.endswith("/%s-0.1.0-SNAPSHOT.jar" % m) for m in MODULES)}
out.append("THIRD_PARTY_LIBS=%d IDENTICAL_TO_TESTED_JAR=%s DIFFERENT=%s" % (len(third_party_new), third_party_new == third_party_old,
    sorted(n for n in set(third_party_new) | set(third_party_old) if third_party_new.get(n) != third_party_old.get(n))[:5]))
with io.open(os.path.join(S18, "evidence", "artifact-proof.txt"), "w", encoding="utf-8", newline="\n") as handle:
    handle.write("\n".join(out) + "\n")
print("\n".join(out))

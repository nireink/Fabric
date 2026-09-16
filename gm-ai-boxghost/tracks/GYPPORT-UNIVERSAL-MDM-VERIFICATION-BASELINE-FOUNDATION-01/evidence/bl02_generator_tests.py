# GYPPORT_UNIVERSAL_MDM_VERIFICATION_BASELINE_FOUNDATION_01, Fabric single memory root reconciliation: disposable
# validation of Fabric/tools/verification/New-GypportVerifiedBaseline.ps1, whose canonical target is now
# Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md. Every run targets temporary copies; the real canonical log, the
# Gystigo compatibility pointer and the real verification-baselines files are only read.
#   pre           before the real reconciliation: T1-T12 as in bl01, T13 default target, T14 pointer refused,
#                 T15 prefix collision.
#   post <pre>    after it: the real canonical log and pointer, T3 duplicate protection on a copy of the real log,
#                 determinism against T1, T14b refusal of a copy of the real pointer, curated manifest.
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

WS = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
GEN = os.path.join(WS, "Fabric", "tools", "verification", "New-GypportVerifiedBaseline.ps1")
REAL_CANONICAL = os.path.join(WS, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE", "Reglas.md")
REAL_POINTER = os.path.join(WS, "Gystigo", "Reglas.md")
REAL_DIR = os.path.join(WS, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE", "verification-baselines")
S = r"C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\8142c294-1815-45b4-90ee-94d1198faa7d\scratchpad"
ORIGINAL = os.path.join(S, "bl01_reglas_original.md")
RULE = os.path.join(S, "bl01_reglas_entry_rule.md")
REG = os.path.join(S, "bl01_reglas_entry_registration_pkg2c.md")
POINTER = os.path.join(S, "bl02_gystigo_reglas_pointer.md")
EVIDENCE = os.path.join(S, "bl01_evidence_pkg2c.json")
DOC = "GYPPORT_PKG2C_VERIFIED_BASELINE_2026-09-15.md"
BID = "GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15"
CANONICAL_PATH = "Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/" + DOC
REPOS = {"gm-entities": os.path.join(WS, "Modules", "gm-entities"),
         "gm-security": os.path.join(WS, "Modules", "gm-security"),
         "Gystigo": os.path.join(WS, "Gystigo")}

phase = sys.argv[1]
root = os.path.join(S, "bl02_gen_" + phase + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
os.makedirs(root)
results = []


def read(path):
    with open(path, "rb") as f:
        return f.read()


def write(path, data):
    with open(path, "wb") as f:
        f.write(data)


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def real_state():
    state = {"canonical Reglas.md": sha(read(REAL_CANONICAL)), "Gystigo/Reglas.md": sha(read(REAL_POINTER)),
             "generator": sha(read(GEN))}
    for name in sorted(os.listdir(REAL_DIR)):
        state[name] = sha(read(os.path.join(REAL_DIR, name)))
    return state


def check(test, ok, detail):
    results.append(("PASS" if ok else "FAIL", test, detail))


def setup(name, reglas_bytes, reglas_name="Reglas.md", dir_name="verification-baselines", docs=None):
    case = os.path.join(root, name)
    out = os.path.join(case, dir_name)
    os.makedirs(out)
    reglas = os.path.join(case, reglas_name)
    write(reglas, reglas_bytes)
    for doc_name, data in (docs or {}).items():
        write(os.path.join(out, doc_name), data)
    return out, reglas


def run(evidence, out=None, reglas=None, generator=GEN):
    command = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", generator,
               "-EvidenceFile", evidence]
    if out:
        command += ["-OutputDirectory", out]
    if reglas:
        command += ["-ReglasPath", reglas]
    proc = subprocess.run(command, capture_output=True)
    text = proc.stdout.decode("utf-8", "replace").replace("\r", "")
    keys = {}
    for line in text.split("\n"):
        if "=" in line:
            key, value = line.split("=", 1)
            keys.setdefault(key, value)
    with open(os.path.join(root, "runs.log"), "a", encoding="utf-8", newline="\n") as log:
        log.write("### %s | %s | %s | %s | exit=%d\n" % (os.path.basename(evidence), generator, out, reglas, proc.returncode))
        log.write(text + proc.stderr.decode("utf-8", "replace").replace("\r", "") + "\n")
    return proc.returncode, keys


def variant(name, mutate):
    with open(EVIDENCE, encoding="utf-8") as f:
        data = json.load(f)
    mutate(data)
    path = os.path.join(root, name + ".json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
    return path


def manifest(text):
    pattern = re.compile(r"^(?:[AMDT] [0-9a-f]{12} \S.*|\S+ [0-9a-f]{40} files=\d+)$")
    return [line for line in text.split("\n") if pattern.match(line)]


original, rule, reg, pointer = read(ORIGINAL), read(RULE), read(REG), read(POINTER)
base = original + b"\n" + rule  # the log after the rule entry, before the registration
line = ("BASELINE_ID=" + BID + "\n").encode()
before = real_state()


def refused(test, evidence, expect, reglas_bytes=None, reglas_name="Reglas.md", dir_name="verification-baselines"):
    data = base if reglas_bytes is None else reglas_bytes
    out, reglas = setup(test, data, reglas_name=reglas_name, dir_name=dir_name)
    code, keys = run(evidence, out, reglas)
    reason = keys.get("REASON", "")
    check(test, code == 1 and keys.get("STATUS") == "REFUSED" and expect.lower() in reason.lower(),
          "exit=%s reason=%s" % (code, reason))
    check(test, os.listdir(out) == [] and read(reglas) == data, "nothing written")


if phase == "pre":
    check("PRE", read(REAL_CANONICAL) == original, "the real canonical log is still the pre-reconciliation Fabric copy")
    check("PRE", read(REAL_POINTER) == original + b"\n" + rule + b"\n" + reg,
          "Gystigo/Reglas.md still holds the complete history")

    out, reglas = setup("t1_fresh", base)
    code, keys = run(EVIDENCE, out, reglas)
    doc = os.path.join(out, DOC)
    check("T1", code == 0 and keys.get("STATUS") == "VERIFIED_BASELINE_GENERATED_PENDING_OWNER_REVIEW",
          "exit=%s status=%s reason=%s" % (code, keys.get("STATUS"), keys.get("REASON")))
    check("T1", sorted(os.listdir(out)) == [DOC], "expected path produced: " + doc)
    check("T1", keys.get("BASELINE_PATH") == CANONICAL_PATH, "BASELINE_PATH=" + keys.get("BASELINE_PATH", ""))
    check("T1", keys.get("BASELINE_DOCUMENT") == "WRITTEN" and keys.get("REGLAS_REGISTRATION") == "APPENDED",
          "document=%s registration=%s" % (keys.get("BASELINE_DOCUMENT"), keys.get("REGLAS_REGISTRATION")))
    check("T1", keys.get("COMMITS_VERIFIED_LOCALLY") == "3/3" and keys.get("COMMIT_FILES_TOTAL") == "52",
          "commits=%s files=%s" % (keys.get("COMMITS_VERIFIED_LOCALLY"), keys.get("COMMIT_FILES_TOTAL")))
    after = read(reglas)
    check("T1", after[:len(base)] == base, "append-only: existing Reglas bytes are an exact prefix")
    check("T1", after == base + b"\n" + reg, "appended bytes == LF + the PKG-2C registration fragment")
    check("T1", after.count(line) == 1, "one registration line")
    data = read(doc) if os.path.isfile(doc) else b""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = ""
    check("T1", data[:3] != b"\xef\xbb\xbf" and b"\r" not in data and text != "", "document is UTF-8 without BOM, LF only")
    check("T1", text.startswith("# GYPPORT \u2014 PKG2C Verified Baseline\n") and "\u00e2\u20ac" not in text,
          "PowerShell 5.1-safe encoding: em dash correct, no mojibake")
    check("T1", len([l for l in manifest(text) if " files=" not in l]) == 52, "52 manifest file lines")
    for expected in ["BASELINE_ID=" + BID, "MIGRATION_HEAD=V58", "VERIFIED_FILE_COUNT=52", "BASELINE_REUSE_ALLOWED=YES",
                     "gm-entities=7b2c56fc5141f38f2bb1e14f11c6d32e3eecca2e", "KNOWN_PREEXISTING_FAILURES=3",
                     "OWNER_REVIEW_REQUIRED=YES", "GENERATOR_APPROVAL=NONE"]:
        check("T1", ("\n" + expected + "\n") in text, "document line " + expected)
    write(os.path.join(root, "t1_result_Reglas.md"), after)
    write(os.path.join(root, "t1_result_" + DOC), data)
    t1_after, t1_doc = after, data

    code, keys = run(EVIDENCE, out, reglas)
    check("T2", code == 0 and keys.get("BASELINE_DOCUMENT") == "UNCHANGED_ALREADY_PRESENT"
          and keys.get("REGLAS_REGISTRATION") == "ALREADY_PRESENT_SKIPPED",
          "exit=%s document=%s registration=%s" % (code, keys.get("BASELINE_DOCUMENT"), keys.get("REGLAS_REGISTRATION")))
    check("T2", read(reglas) == t1_after and read(doc) == t1_doc and read(reglas).count(line) == 1,
          "duplicate run: no byte changed, still one registration")

    curated = read(os.path.join(REAL_DIR, DOC))
    out, reglas = setup("t4_overwrite", base, docs={DOC: curated})
    code, keys = run(EVIDENCE, out, reglas)
    check("T4", code == 1 and keys.get("STATUS") == "REFUSED" and "never overwritten" in keys.get("REASON", ""),
          "exit=%s reason=%s" % (code, keys.get("REASON")))
    check("T4", read(os.path.join(out, DOC)) == curated and read(reglas) == base and os.listdir(out) == [DOC],
          "curated document copy and Reglas copy unchanged")

    refused("T5_status", variant("t5", lambda e: e.update(status="IMPLEMENTED_PENDING_OWNER_REVIEW")), "status must be")
    refused("T6_missing_field", variant("t6", lambda e: e.pop("migrationHead")),
            "Missing required evidence field: migrationHead")
    refused("T7_unknown_commit",
            variant("t7", lambda e: e["repositories"][2].update(commit="0123456789abcdef0123456789abcdef01234567")),
            "does not exist")
    refused("T8_file_count", variant("t8", lambda e: e.update(verifiedFiles=51)), "verifiedFiles is 51")
    refused("T9_reglas_name", EVIDENCE, "named Reglas.md", reglas_name="Rules.md")
    refused("T10_output_name", EVIDENCE, "named verification-baselines", dir_name="baselines")
    refused("T11_unknown_field", variant("t11", lambda e: e.update(verifedFiles=52)), "Unknown evidence field: verifedFiles")

    crlf = base.replace(b"\n", b"\r\n")
    out, reglas = setup("t12_crlf_log", crlf)
    code, keys = run(EVIDENCE, out, reglas)
    check("T12", code == 0 and read(reglas) == crlf + (b"\n" + reg).replace(b"\n", b"\r\n"),
          "CRLF log: prefix kept, entry appended with CRLF (exit=%s)" % code)

    ws = os.path.join(root, "t13_default_target", "ws")
    tools = os.path.join(ws, "Fabric", "tools", "verification")
    universe = os.path.join(ws, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE")
    os.makedirs(tools)
    os.makedirs(os.path.join(universe, "verification-baselines"))
    os.makedirs(os.path.join(ws, "Gystigo"))
    generator_copy = os.path.join(tools, "New-GypportVerifiedBaseline.ps1")
    shutil.copyfile(GEN, generator_copy)
    canonical_copy = os.path.join(universe, "Reglas.md")
    write(canonical_copy, base)
    write(os.path.join(ws, "Gystigo", "Reglas.md"), pointer)
    evidence = variant("t13", lambda e: [r.update(path=REPOS[r["name"]]) for r in e["repositories"]])
    code, keys = run(evidence, generator=generator_copy)
    check("T13", code == 0 and keys.get("REGLAS_IS_CANONICAL") == "YES" and keys.get("OUTPUT_DIRECTORY_IS_CANONICAL") == "YES",
          "exit=%s reglas_canonical=%s output_canonical=%s reason=%s" % (
              code, keys.get("REGLAS_IS_CANONICAL"), keys.get("OUTPUT_DIRECTORY_IS_CANONICAL"), keys.get("REASON")))
    check("T13", keys.get("REGLAS_FILE", "").lower() == canonical_copy.lower(),
          "default REGLAS_FILE=" + keys.get("REGLAS_FILE", ""))
    check("T13", read(canonical_copy) == base + b"\n" + reg,
          "without -ReglasPath the registration goes to Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md")
    check("T13", read(os.path.join(ws, "Gystigo", "Reglas.md")) == pointer, "the Gystigo pointer copy is untouched")
    check("T13", os.listdir(os.path.join(universe, "verification-baselines")) == [DOC],
          "document written to the canonical directory by default")
    check("T13", read(generator_copy) == read(GEN), "the copy runs the real generator bytes")

    refused("T14_pointer_refused", EVIDENCE, "compatibility pointer", reglas_bytes=pointer)

    bid = BID.encode()
    near = b"".join([b"\n```text\n", b"BASELINE_ID=" + bid + b"X\n", b"BASELINE_ID=" + bid[:-1] + b"\n",
                     b"SUPERSEDES_BASELINE_ID=" + bid + b"\n", b"NOTE BASELINE_ID=" + bid + b"\n", b"```\n\n"])
    collision = base + near
    out, reglas = setup("t15_prefix_collision", collision)
    code, keys = run(EVIDENCE, out, reglas)
    check("T15", code == 0 and keys.get("REGLAS_REGISTRATION") == "APPENDED",
          "near-miss lines are not a registration (exit=%s registration=%s)" % (code, keys.get("REGLAS_REGISTRATION")))
    check("T15", read(reglas) == collision + b"\n" + reg and read(reglas).split(b"\n").count(line.rstrip(b"\n")) == 1,
          "prefix kept, exactly one exact registration line")
    code, keys = run(EVIDENCE, out, reglas)
    check("T15", code == 0 and keys.get("REGLAS_REGISTRATION") == "ALREADY_PRESENT_SKIPPED"
          and read(reglas) == collision + b"\n" + reg, "rerun: the exact line is found, nothing appended")

if phase == "post":
    pre = sys.argv[2]
    canonical = read(REAL_CANONICAL)
    complete = read(os.path.join(S, "bl02_backup", "gystigo_Reglas.md"))
    check("REAL", canonical[:len(original)] == original,
          "the pre-reconciliation Fabric log is an exact prefix of the canonical log")
    check("REAL", canonical == complete, "canonical log == the complete pre-pointer Gystigo/Reglas.md (history loss 0)")
    check("REAL", canonical == original + b"\n" + rule + b"\n" + reg, "canonical log == history + rule entry + registration")
    check("REAL", canonical == read(os.path.join(pre, "t1_result_Reglas.md")), "canonical log == the generator's T1 result")
    headings = re.findall(rb"(?m)^\d{4}-\d{2}-\d{2} \xe2\x80\x94 .+$", canonical)
    check("REAL", len(headings) == 16 and len(set(headings)) == 16, "16 dated entries, no duplicate heading")
    check("REAL", canonical.count(line) == 1 and canonical.count("Universe / Regla de VERIFIED_BASELINE_REUSE".encode()) == 1,
          "VERIFIED_BASELINE_REUSE once, PKG-2C registration once")
    check("REAL", read(REAL_POINTER) == pointer, "Gystigo/Reglas.md is the prepared compatibility pointer")

    out, reglas = setup("t3_registered_log", canonical)
    code, keys = run(EVIDENCE, out, reglas)
    check("T3", code == 0 and keys.get("REGLAS_REGISTRATION") == "ALREADY_PRESENT_SKIPPED"
          and keys.get("REGLAS_APPENDED_BYTES") == "0", "exit=%s registration=%s" % (code, keys.get("REGLAS_REGISTRATION")))
    check("T3", read(reglas) == canonical, "copy of the real canonical log unchanged")
    generated = read(os.path.join(out, DOC))
    check("T3", generated == read(os.path.join(pre, "t1_result_" + DOC)), "deterministic: same document bytes as T1")
    code, keys = run(EVIDENCE, out, reglas)
    check("T3", code == 0 and keys.get("BASELINE_DOCUMENT") == "UNCHANGED_ALREADY_PRESENT"
          and keys.get("REGLAS_REGISTRATION") == "ALREADY_PRESENT_SKIPPED" and read(reglas) == canonical,
          "second run on the registered copy: unchanged")
    refused("T14b_real_pointer", EVIDENCE, "compatibility pointer", reglas_bytes=read(REAL_POINTER))
    curated = manifest(read(os.path.join(REAL_DIR, DOC)).decode("utf-8"))
    check("DOC", curated == manifest(generated.decode("utf-8")) and len(curated) == 55,
          "curated Appendix A == generated manifest (%d lines)" % len(curated))

check("REAL_FILES_UNTOUCHED_BY_TESTS", real_state() == before,
      "the real canonical log, Gystigo/Reglas.md, the real verification-baselines files and the generator are "
      "byte-identical before and after this phase")

summary = os.path.join(root, "summary.txt")
with open(summary, "w", encoding="utf-8", newline="\n") as f:
    for status, test, detail in results:
        f.write("%s|%s|%s\n" % (status, test, detail))
    f.write("TOTAL=%d PASS=%d FAIL=%d\n" % (len(results), sum(1 for r in results if r[0] == "PASS"),
                                            sum(1 for r in results if r[0] == "FAIL")))
sys.stdout.write("ROOT=" + root + "\n")
with open(summary, encoding="utf-8") as f:
    sys.stdout.write(f.read())

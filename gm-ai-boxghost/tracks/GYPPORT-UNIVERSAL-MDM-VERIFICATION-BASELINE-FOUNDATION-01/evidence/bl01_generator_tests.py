# GYPPORT_UNIVERSAL_MDM_VERIFICATION_BASELINE_FOUNDATION_01: disposable validation of
# Fabric/tools/verification/New-GypportVerifiedBaseline.ps1. Every run targets temporary copies; the real Reglas.md
# and the real verification-baselines files are only read.
#   pre           T1 fresh generation (registration bytes == the manual PKG-2C fragment), T2 duplicate run,
#                 T4 overwrite refusal, T5-T11 refusals, T12 CRLF log.
#   post <pre>    real Reglas.md == T1 result; T3 duplicate protection on a copy of the registered real log;
#                 determinism against T1; the curated manifest equals the generated one.
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

WS = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
GEN = os.path.join(WS, "Fabric", "tools", "verification", "New-GypportVerifiedBaseline.ps1")
REAL_REGLAS = os.path.join(WS, "Gystigo", "Reglas.md")
REAL_DIR = os.path.join(WS, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE", "verification-baselines")
S = r"C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\8142c294-1815-45b4-90ee-94d1198faa7d\scratchpad"
ORIGINAL = os.path.join(S, "bl01_reglas_original.md")
RULE = os.path.join(S, "bl01_reglas_entry_rule.md")
REG = os.path.join(S, "bl01_reglas_entry_registration_pkg2c.md")
EVIDENCE = os.path.join(S, "bl01_evidence_pkg2c.json")
DOC = "GYPPORT_PKG2C_VERIFIED_BASELINE_2026-09-15.md"
BID = "GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15"
CANONICAL_PATH = "Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/" + DOC

phase = sys.argv[1]
root = os.path.join(S, "bl01_gen_" + phase + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
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
    state = {"Gystigo/Reglas.md": sha(read(REAL_REGLAS)), "generator": sha(read(GEN))}
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


def run(evidence, out, reglas):
    proc = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", GEN,
                           "-EvidenceFile", evidence, "-OutputDirectory", out, "-ReglasPath", reglas],
                          capture_output=True)
    text = proc.stdout.decode("utf-8", "replace").replace("\r", "")
    keys = {}
    for line in text.split("\n"):
        if "=" in line:
            key, value = line.split("=", 1)
            keys.setdefault(key, value)
    with open(os.path.join(root, "runs.log"), "a", encoding="utf-8", newline="\n") as log:
        log.write("### %s | %s | %s | exit=%d\n" % (os.path.basename(evidence), out, reglas, proc.returncode))
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


original, rule, reg = read(ORIGINAL), read(RULE), read(REG)
base = original + b"\n" + rule  # the log after the rule entry, before the registration
line = ("BASELINE_ID=" + BID + "\n").encode()
before = real_state()

if phase == "pre":
    check("PRE", read(REAL_REGLAS) == original, "the real Reglas.md is still the original during the pre phase")

    out, reglas = setup("t1_fresh", base)
    code, keys = run(EVIDENCE, out, reglas)
    doc = os.path.join(out, DOC)
    check("T1", code == 0 and keys.get("STATUS") == "VERIFIED_BASELINE_GENERATED_PENDING_OWNER_REVIEW",
          "exit=%s status=%s reason=%s" % (code, keys.get("STATUS"), keys.get("REASON")))
    check("T1", sorted(os.listdir(out)) == [DOC], "expected path produced: " + doc)
    check("T1", keys.get("BASELINE_FILE", "").lower() == doc.lower(), "BASELINE_FILE=" + keys.get("BASELINE_FILE", ""))
    check("T1", keys.get("BASELINE_PATH") == CANONICAL_PATH, "BASELINE_PATH=" + keys.get("BASELINE_PATH", ""))
    check("T1", keys.get("BASELINE_DOCUMENT") == "WRITTEN" and keys.get("REGLAS_REGISTRATION") == "APPENDED",
          "document=%s registration=%s" % (keys.get("BASELINE_DOCUMENT"), keys.get("REGLAS_REGISTRATION")))
    check("T1", keys.get("COMMITS_VERIFIED_LOCALLY") == "3/3" and keys.get("COMMIT_FILES_TOTAL") == "52",
          "commits=%s files=%s" % (keys.get("COMMITS_VERIFIED_LOCALLY"), keys.get("COMMIT_FILES_TOTAL")))
    after = read(reglas)
    check("T1", after[:len(base)] == base, "existing Reglas bytes are an exact prefix")
    check("T1", after == base + b"\n" + reg, "appended bytes == LF + the manual PKG-2C registration fragment")
    check("T1", after.count(line) == 1, "one registration line")
    data = read(doc) if os.path.isfile(doc) else b""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = ""
    check("T1", data[:3] != b"\xef\xbb\xbf" and b"\r" not in data and text != "", "document is UTF-8 without BOM, LF only")
    check("T1", text.startswith("# GYPPORT \u2014 PKG2C Verified Baseline\n") and "\u00e2\u20ac" not in text,
          "em dash encoded correctly, no mojibake")
    check("T1", len([l for l in manifest(text) if not l.endswith(tuple("files=%d" % n for n in (17, 8, 27)))]) == 52,
          "52 manifest file lines")
    for expected in ["BASELINE_ID=" + BID, "MIGRATION_HEAD=V58", "VERIFIED_FILE_COUNT=52", "BASELINE_REUSE_ALLOWED=YES",
                     "gm-entities=e6d3cbcc5e004e8fbd11c78dc1817b5a00e6bffb",
                     "gm-entities=7b2c56fc5141f38f2bb1e14f11c6d32e3eecca2e",
                     "gm-security=ee3c2a95efb4efa61b3eaf6405df4e3822b56e4b",
                     "Gystigo=59bd77f0bf6a2aa6b1c3083097a8c8e0b258ff56",
                     "KNOWN_PREEXISTING_FAILURES=3", "OWNER_REVIEW_REQUIRED=YES", "GENERATOR_APPROVAL=NONE"]:
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

    def refused(test, evidence, expect, reglas_name="Reglas.md", dir_name="verification-baselines"):
        out, reglas = setup(test, base, reglas_name=reglas_name, dir_name=dir_name)
        code, keys = run(evidence, out, reglas)
        reason = keys.get("REASON", "")
        check(test, code == 1 and keys.get("STATUS") == "REFUSED" and expect.lower() in reason.lower(),
              "exit=%s reason=%s" % (code, reason))
        check(test, os.listdir(out) == [] and read(reglas) == base, "nothing written")

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

if phase == "post":
    pre = sys.argv[2]
    real = read(REAL_REGLAS)
    check("REAL", real[:len(original)] == original, "the original Reglas.md bytes are an exact prefix of the real file")
    check("REAL", real == original + b"\n" + rule + b"\n" + reg, "real Reglas.md == original + rule entry + registration")
    check("REAL", real == read(os.path.join(pre, "t1_result_Reglas.md")), "real Reglas.md == the generator's T1 result")
    check("REAL", real.count(line) == 1, "one PKG-2C registration in the real log")

    out, reglas = setup("t3_registered_log", real)
    code, keys = run(EVIDENCE, out, reglas)
    check("T3", code == 0 and keys.get("REGLAS_REGISTRATION") == "ALREADY_PRESENT_SKIPPED"
          and keys.get("REGLAS_APPENDED_BYTES") == "0",
          "exit=%s registration=%s" % (code, keys.get("REGLAS_REGISTRATION")))
    check("T3", read(reglas) == real, "copy of the registered real log unchanged")
    generated = read(os.path.join(out, DOC))
    check("T3", generated == read(os.path.join(pre, "t1_result_" + DOC)), "deterministic: same document bytes as T1")
    code, keys = run(EVIDENCE, out, reglas)
    check("T3", code == 0 and keys.get("BASELINE_DOCUMENT") == "UNCHANGED_ALREADY_PRESENT"
          and keys.get("REGLAS_REGISTRATION") == "ALREADY_PRESENT_SKIPPED" and read(reglas) == real,
          "second run on the registered copy: unchanged")
    curated = manifest(read(os.path.join(REAL_DIR, DOC)).decode("utf-8"))
    check("DOC", curated == manifest(generated.decode("utf-8")) and len(curated) == 55,
          "curated Appendix A == generated manifest (%d lines)" % len(curated))

check("REAL_FILES_UNTOUCHED_BY_TESTS", real_state() == before,
      "the real Reglas.md, the real verification-baselines files and the generator are byte-identical before and after")

summary = os.path.join(root, "summary.txt")
with open(summary, "w", encoding="utf-8", newline="\n") as f:
    for status, test, detail in results:
        f.write("%s|%s|%s\n" % (status, test, detail))
    f.write("TOTAL=%d PASS=%d FAIL=%d\n" % (len(results), sum(1 for r in results if r[0] == "PASS"),
                                            sum(1 for r in results if r[0] == "FAIL")))
sys.stdout.write("ROOT=" + root + "\n")
with open(summary, encoding="utf-8") as f:
    sys.stdout.write(f.read())

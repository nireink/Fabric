# GYPPORT_UNIVERSAL_MDM_VERIFICATION_BASELINE_FOUNDATION_01: static checks of the four delivered files (read-only).
# Encoding and line endings, repository paths the documents cite, Appendix A against git, and the fields the Owner
# prompt requires.
import os
import re
import subprocess
import sys

WS = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
B = os.path.join(WS, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE", "verification-baselines")
PKG2C = os.path.join(B, "GYPPORT_PKG2C_VERIFIED_BASELINE_2026-09-15.md")
REUSE = os.path.join(B, "VERIFIED_BASELINE_REUSE.md")
AUTOMATION = os.path.join(B, "GYPPORT_VERIFIED_BASELINE_AUTOMATION.md")
GEN = os.path.join(WS, "Fabric", "tools", "verification", "New-GypportVerifiedBaseline.ps1")
REPOS = {"gm-entities": os.path.join(WS, "Modules", "gm-entities"),
         "gm-security": os.path.join(WS, "Modules", "gm-security"),
         "Gystigo": os.path.join(WS, "Gystigo")}
results = []


def check(ok, detail):
    results.append(("PASS" if ok else "FAIL", detail))


texts = {}
for path in (PKG2C, REUSE, AUTOMATION, GEN):
    name = os.path.basename(path)
    data = open(path, "rb").read()
    check(data[:3] != b"\xef\xbb\xbf", name + ": no BOM")
    check(b"\r" not in data, name + ": LF only")
    check(data.endswith(b"\n") and not data.endswith(b"\n\n"), name + ": ends with exactly one line feed")
    try:
        texts[path] = data.decode("utf-8")
        check(True, name + ": valid UTF-8")
    except UnicodeDecodeError:
        texts[path] = ""
        check(False, name + ": valid UTF-8")
    check(texts[path][:1] in ("#", "<"), name + ": starts with its heading, no stray character")
    if path == GEN:
        check(all(b < 128 for b in data), name + ": ASCII only")
    for ref in sorted(set(re.findall(r"(?:Fabric|Gystigo)/[A-Za-z0-9_./-]+\.(?:md|ps1|sql)", texts[path]))):
        check(os.path.isfile(os.path.join(WS, *ref.split("/"))), name + ": cited path exists: " + ref)

text = texts[PKG2C]
current, verified = None, 0
for line in text.split("\n"):
    header = re.match(r"^(\S+) ([0-9a-f]{40}) files=(\d+)$", line)
    if header:
        current = header.groups()
        continue
    entry = re.match(r"^([AMDT]) ([0-9a-f]{12}) (\S.*)$", line)
    if entry and current:
        repo, commit, _ = current
        blob = subprocess.run(["git", "-C", REPOS[repo], "rev-parse", commit + ":" + entry.group(3)],
                              capture_output=True, text=True).stdout.strip()
        ok = blob.startswith(entry.group(2))
        verified += 1 if ok else 0
        if not ok:
            check(False, "Appendix A blob mismatch: %s %s" % (repo, entry.group(3)))
check(verified == 52, "Appendix A: %d of 52 blob ids equal git rev-parse <commit>:<path>" % verified)
rows = [l for l in text.split("\n") if re.match(r"^\| \d+ \| m_", l)]
check(len(rows) == 39, "Appendix B: %d matrix rows" % len(rows))
check(sum(1 for r in rows if r.rstrip().endswith("| PASS |")) == 36, "Appendix B: 36 PASS rows")
check(sum(1 for r in rows if "KNOWN DEBT" in r) == 3, "Appendix B: 3 KNOWN DEBT rows")

required = ["BASELINE_ID=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15", "STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL",
            "STEP=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15",
            "PHASE=PKG_2C_CONTEXTUAL_ACCESS_AND_FK_RECONCILIATION",
            "e6d3cbcc5e004e8fbd11c78dc1817b5a00e6bffb", "1654f271711e96761ae7d5470dce3d161cb4333b",
            "a3b7bfeb1b52f06110cd08af185b04f3690b4a43", "MIGRATION_HEAD=V58", "VERIFIED_FILE_COUNT=52",
            "GM_ENTITIES_TESTS=217/217", "GM_SECURITY_TESTS=111/111", "GM_EXPENSES_REAL_DB=84/84",
            "NORMAL_HOST_TESTS=675 run, 0 failures, 0 errors, 251 skipped", "STUDIO_CONTRACTS=581/581",
            "STUDIO_BUILD=PASS", "FULL_RUNTIME_MATRIX=39/39_EXECUTED", "NEW_FAILURES=0",
            "KNOWN_PREEXISTING_FAILURES=3", "1. TeamEmployeeRealDatabaseAcceptanceTest",
            "2. TeamEmployeeControllerScopeBoundaryRealDatabaseAcceptanceTest",
            "3. PersonIdentityReconciliationHttpTest:222", "IDENTITY=GLOBAL",
            "BUSINESS_PARTICIPATION=TENANT_CONTEXTUAL", "ACCESS=SECURITY", "EMPLOYMENT=HR",
            "AUDIT_ACTOR=GLOBAL_ACCOUNT", "ACTIVE_MEMBERSHIP_REQUIRES_PARTY=NO", "PARTY_PROJECTION_POLICY=LAZY_EXPLICIT",
            "CONTEXTUAL_PARTY_READ_IS_READ_ONLY=YES", "LOGIN_CREATES_PARTY=NO", "AUTH_ME_CREATES_PARTY=NO",
            "AUTHORIZATION_READ_CREATES_PARTY=NO", "ACTOR_FKS=GLOBAL_USER_ACCOUNT",
            "ACTOR_FIELDS_MOVED_TO_MEMBERSHIP=0", "ACCESS_SUBJECTS=USER_TENANT_MEMBERSHIP",
            "EVC_PRC_ACCOUNT_FK_RESHAPE=DEFER", "BASELINE_REUSE_ALLOWED=YES"]
for key in required:
    check(key in text, "PKG-2C baseline contains " + key)

policy = texts[REUSE]
for key in ["MUST NOT automatically rerun its complete", "BASELINE_FOUND=YES|NO", "BASELINE_ID=<id or NONE>",
            "BASELINE_REUSE_DECISION=REUSE|PARTIAL_INVALIDATION|FULL_INVALIDATION", "BASELINE_REUSE_REASON=",
            "FULL_HISTORICAL_REGRESSION_RERUN=NO", "\"Run everything\nagain to be safe\" is NOT sufficient",
            "Git commit SHA(s)", "NOT canonical baseline storage", "IMPLEMENT\n\u2192 VERIFY\n\u2192 OWNER REVIEW\n"
            "\u2192 CONTROLLED COMMIT\n\u2192 POST-COMMIT SMOKE\n\u2192 GENERATE VERIFIED BASELINE\n"
            "\u2192 REGISTER BASELINE IN Reglas.md\n\u2192 OWNER REVIEW\n\u2192 NEXT STEP"]:
    check(key in policy, "policy contains " + key.replace("\n", " / "))
for key in ["GENERATE_ONLY", "REGISTER BASELINE IN Reglas.md", "MODIFIES_IMPLEMENTATION_REPOSITORIES=NO",
            "EXECUTES_TESTS=NO", "APPROVES_BASELINE=NO", "STARTS_NEXT_STEP=NO", "COMMITS=NO", "PUSHES=NO"]:
    check(key in texts[AUTOMATION], "automation contains " + key)

for status, detail in results:
    sys.stdout.write("%s|%s\n" % (status, detail))
sys.stdout.write("TOTAL=%d PASS=%d FAIL=%d\n" % (len(results), sum(1 for r in results if r[0] == "PASS"),
                                               sum(1 for r in results if r[0] == "FAIL")))

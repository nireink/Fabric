# GYPPORT_UNIVERSAL_MDM_VERIFICATION_BASELINE_FOUNDATION_01, Owner decision FABRIC_SINGLE_MEMORY_ROOT_AND_OPTION_B.
# The only authorized real writes of the reconciliation, each gated by the one before it:
#   1. append the STEP delta (rule entry + PKG-2C registration) to Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md;
#   2. only when that file equals the complete Gystigo/Reglas.md, replace Gystigo/Reglas.md with the pointer;
#   3. rename the PKG-2D double extension, byte-preserving.
import hashlib
import os
import re
import sys

W = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
S = r"C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\8142c294-1815-45b4-90ee-94d1198faa7d\scratchpad"
B = os.path.join(S, "bl02_backup")
CANONICAL = os.path.join(W, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE", "Reglas.md")
GYSTIGO = os.path.join(W, "Gystigo", "Reglas.md")
PKG2D_OLD = os.path.join(W, "Fabric", "Knowledge", "00-GYPPORT-UNIVERSE", "steps", "PKG-2D",
                         "PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md.md")
PKG2D_NEW = PKG2D_OLD[:-len(".md")]
PKG2D_SHA = "4cd2796b5e3747bda77422c67946a05894fdf58a84b1f800e310b82f938b656e"
REGISTRATION = b"BASELINE_ID=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15\n"
RULE_HEADING = "Universe / Regla de VERIFIED_BASELINE_REUSE".encode()


def read(path):
    with open(path, "rb") as f:
        return f.read()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stop(reason):
    print("STOPPED=" + reason)
    sys.exit(1)


original = read(os.path.join(S, "bl01_reglas_original.md"))
delta = (b"\n" + read(os.path.join(S, "bl01_reglas_entry_rule.md")) + b"\n"
         + read(os.path.join(S, "bl01_reglas_entry_registration_pkg2c.md")))
pointer = read(os.path.join(S, "bl02_gystigo_reglas_pointer.md"))
fabric = read(CANONICAL)
gystigo = read(GYSTIGO)

# Preconditions: both logs are exactly the compared and backed-up states; the pointer holds no rule.
if fabric != original or fabric != read(os.path.join(B, "fabric_Reglas.md")):
    stop("Fabric Reglas.md is not the compared state; nothing written")
if gystigo != original + delta or gystigo != read(os.path.join(B, "gystigo_Reglas.md")):
    stop("Gystigo Reglas.md is not the compared state; nothing written")
if REGISTRATION in fabric or RULE_HEADING in fabric:
    stop("Fabric Reglas.md already holds a STEP entry; nothing written")
if not pointer.startswith("# MOVED \u2014 GYPPORT Canonical Rules\n".encode()) or re.search(rb"(?m)^\d{4}-\d{2}-\d{2} ", pointer):
    stop("the prepared pointer is not a pure pointer; nothing written")

# 1. Reconciliation of the canonical log: append only.
with open(CANONICAL, "ab") as f:
    f.write(delta)
final = read(CANONICAL)
print(f"CANONICAL_BEFORE bytes={len(fabric)} lines={fabric.count(b'\n')} sha={sha(fabric)[:16].upper()}")
print(f"CANONICAL_AFTER bytes={len(final)} lines={final.count(b'\n')} sha={sha(final)[:16].upper()}")
print(f"CANONICAL_PREFIX_PRESERVED={'YES' if final[:len(fabric)] == fabric else 'NO'}")
print(f"CANONICAL_EQUALS_COMPLETE_GYSTIGO_HISTORY={'YES' if final == gystigo else 'NO'}")
print(f"VERIFIED_BASELINE_REUSE_ENTRIES={final.count(RULE_HEADING)} PKG2C_REGISTRATIONS={final.count(REGISTRATION)}")
if final != gystigo or final[:len(fabric)] != fabric:
    stop("the canonical log is not the complete Gystigo history; the pointer was NOT written")

# 2. Compatibility pointer, only now that the canonical log is proven complete.
with open(GYSTIGO, "wb") as f:
    f.write(pointer)
written = read(GYSTIGO)
print(f"GYSTIGO_POINTER bytes={len(written)} lines={written.count(b'\n')} sha={sha(written)[:16].upper()} "
      f"equals_prepared={'YES' if written == pointer else 'NO'}")
if written != pointer:
    stop("the pointer bytes differ after writing")

# 3. PKG-2D double extension: rename, byte-preserving, never over an existing file.
if not os.path.isfile(PKG2D_OLD):
    stop("PKG-2D double-extension file not found")
if os.path.exists(PKG2D_NEW):
    stop("PKG-2D canonical path already exists; not overwritten")
before = sha(read(PKG2D_OLD))
if before != PKG2D_SHA:
    stop("PKG-2D file changed since it was recorded")
os.rename(PKG2D_OLD, PKG2D_NEW)
after = sha(read(PKG2D_NEW))
print(f"PKG2D_RENAMED old_exists={os.path.exists(PKG2D_OLD)} new_exists={os.path.isfile(PKG2D_NEW)} "
      f"sha_before={before[:16]} sha_after={after[:16]} byte_preserving={'YES' if before == after else 'NO'}")
print("REAL_WRITES=COMPLETE")

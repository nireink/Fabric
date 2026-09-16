"""STEP 15 PKG-2C byte-identity proof. Read-only.

Hashes (SHA-256 of the raw bytes) the 52 PKG-2C paths and compares them with the ENTRY rows of an earlier fingerprint
(s15g_fingerprint.ps1 format: ENTRY|repo|class|status|path|SHA256|time).

  python s15k_pkg2c_hashes.py <baseline-fingerprint.txt> [<out.txt>]
"""
import hashlib
import os
import sys

ROOT = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
REPOS = {
    "Gystigo": os.path.join(ROOT, "Gystigo"),
    "gm-security": os.path.join(ROOT, "Modules", "gm-security"),
    "gm-entities": os.path.join(ROOT, "Modules", "gm-entities"),
}
SERVER_MAIN = "platform_os/server/src/main/java/com/gypport/server/"
SERVER_TEST = "platform_os/server/src/test/java/com/gypport/server/"
SEC_MAIN = "src/main/java/com/gypport/business/security/"
SEC_TEST = "src/test/java/com/gypport/business/security/"
ENT_MAIN = "src/main/java/com/gypport/business/entities/"
ENT_TEST = "src/test/java/com/gypport/business/entities/"

PATHS = [
    ("Gystigo", "database/core/migration/V57__tenant_access_subject_membership_fks.sql"),
    ("Gystigo", "database/core/migration/V58__global_user_account_actor_fks.sql"),
    ("Gystigo", "docs/testing/TEST_DATABASE_ISOLATION.md"),
    ("Gystigo", SERVER_MAIN + "module/humanresources/EmployeeAccessGrantService.java"),
    ("Gystigo", SERVER_MAIN + "module/onboarding/application/RegisterPersonAccountUseCase.java"),
    ("Gystigo", SERVER_MAIN + "module/organizations/ClaimOrganizationControlUseCase.java"),
    ("Gystigo", SERVER_MAIN + "module/organizations/ConfirmOrganizationControlUseCase.java"),
    ("Gystigo", SERVER_MAIN + "module/organizations/ReviewOrganizationControlUseCase.java"),
    ("Gystigo", SERVER_MAIN + "shared/config/GmOrganizationsConfig.java"),
    ("Gystigo", SERVER_TEST + "module/entities/ContextualPartyReadRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "module/entities/GmEntitiesHostIntegrationTest.java"),
    ("Gystigo", SERVER_TEST + "module/humanresources/EmployeeAccessRevocationRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "module/humanresources/EmployeeEmploymentUpdateRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "module/humanresources/TeamEmployeeRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "module/onboarding/application/RegisterPersonAccountUseCaseTest.java"),
    ("Gystigo", SERVER_TEST + "module/organizations/ClaimOrganizationControlUseCaseTest.java"),
    ("Gystigo", SERVER_TEST + "module/organizations/ConfirmOrganizationControlUseCaseTest.java"),
    ("Gystigo", SERVER_TEST + "module/organizations/GmOrganizationsRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "module/organizations/OrganizationControlActivationRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "module/organizations/ReviewOrganizationControlUseCaseTest.java"),
    ("Gystigo", SERVER_TEST + "module/platform/PlatformAdminRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "module/profile/application/MyProfileServiceTest.java"),
    ("Gystigo", SERVER_TEST + "module/profile/application/ProfileIdentityServiceTest.java"),
    ("Gystigo", SERVER_TEST + "module/security/GlobalUserAccountActorRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "shared/persistence/GlobalUserAccountActorFkMigrationRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "shared/persistence/TenantAccessSubjectMembershipFkMigrationRealDatabaseAcceptanceTest.java"),
    ("Gystigo", SERVER_TEST + "shared/persistence/TenantAccessSubjectMembershipFkMigrationStopRealDatabaseAcceptanceTest.java"),
    ("gm-security", SEC_MAIN + "application/RoleProvisioningPort.java"),
    ("gm-security", SEC_MAIN + "application/UserAccountProfileRecord.java"),
    ("gm-security", SEC_MAIN + "application/UserAccountRepository.java"),
    ("gm-security", SEC_MAIN + "infrastructure/persistence/jdbc/JdbcPartyAccessQueryAdapter.java"),
    ("gm-security", SEC_MAIN + "infrastructure/persistence/jdbc/JdbcRoleProvisioningAdapter.java"),
    ("gm-security", SEC_MAIN + "infrastructure/persistence/jdbc/JdbcUserAccountRepository.java"),
    ("gm-security", SEC_TEST + "infrastructure/persistence/jdbc/JdbcPartyAccessQueryAdapterTest.java"),
    ("gm-security", SEC_TEST + "infrastructure/persistence/jdbc/JdbcUserAccountRepositoryTest.java"),
    ("gm-entities", ENT_MAIN + "application/ReviewOrganizationControlClaimUseCase.java"),
    ("gm-entities", ENT_MAIN + "party/domain/PartyRelationshipVerification.java"),
    ("gm-entities", ENT_MAIN + "party/domain/PartyRelationshipVerificationEvidence.java"),
    ("gm-entities", ENT_MAIN + "party/domain/TenantPartyRepository.java"),
    ("gm-entities", ENT_MAIN + "party/infrastructure/persistence/jdbc/JdbcPartyRelationshipVerificationEvidenceRepository.java"),
    ("gm-entities", ENT_MAIN + "party/infrastructure/persistence/jdbc/JdbcPartyRelationshipVerificationRepository.java"),
    ("gm-entities", ENT_MAIN + "party/infrastructure/persistence/jdbc/JdbcTenantPartyRepository.java"),
    ("gm-entities", ENT_TEST + "application/AddPartyIdentifierUseCaseTest.java"),
    ("gm-entities", ENT_TEST + "application/CreateOrganizationPartyUseCaseTest.java"),
    ("gm-entities", ENT_TEST + "application/CreatePersonPartyUseCaseTest.java"),
    ("gm-entities", ENT_TEST + "application/GetPartyProfileUseCaseTest.java"),
    ("gm-entities", ENT_TEST + "application/ReviewOrganizationControlClaimUseCaseTest.java"),
    ("gm-entities", ENT_TEST + "identity/application/IdentityClaimServiceTest.java"),
    ("gm-entities", ENT_TEST + "intake/application/SubmitIdentityIntakeUseCaseTest.java"),
    ("gm-entities", ENT_TEST + "party/domain/PartyRelationshipVerificationEvidenceTest.java"),
    ("gm-entities", ENT_TEST + "party/domain/PartyRelationshipVerificationTest.java"),
    ("gm-entities", ENT_TEST + "party/infrastructure/persistence/jdbc/JdbcTenantPartyRepositoryTest.java"),
]


def baseline(path):
    entries = {}
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            parts = line.rstrip("\r\n").split("|")
            if parts[0] == "ENTRY" and len(parts) >= 6:
                entries[(parts[1], parts[4])] = parts[5].strip().upper()
    return entries


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    base = baseline(sys.argv[1])
    counts = {"MATCH": 0, "MISMATCH": 0, "MISSING_NOW": 0, "NOT_IN_BASELINE": 0}
    rows = []
    for repo, rel in PATHS:
        full = os.path.join(REPOS[repo], *rel.split("/"))
        digest = ""
        if not os.path.isfile(full):
            state = "MISSING_NOW"
        else:
            with open(full, "rb") as handle:
                digest = hashlib.sha256(handle.read()).hexdigest().upper()
            expected = base.get((repo, rel))
            if expected is None:
                state = "NOT_IN_BASELINE"
            elif expected == digest:
                state = "MATCH"
            else:
                state = "MISMATCH"
        counts[state] += 1
        rows.append(f"{state}|{repo}|{rel}|{digest}")
    summary = ("PKG2C_PATHS={0} MATCH={1} MISMATCH={2} MISSING_NOW={3} NOT_IN_BASELINE={4} BASELINE={5}".format(
        len(PATHS), counts["MATCH"], counts["MISMATCH"], counts["MISSING_NOW"], counts["NOT_IN_BASELINE"],
        os.path.basename(sys.argv[1])))
    for row in rows:
        if not row.startswith("MATCH|"):
            print(row)
    print(summary)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(rows) + "\n" + summary + "\n")


if __name__ == "__main__":
    main()

# GYPPORT — PKG-2C Verified Baseline

**Baseline ID:** `GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15`  
**Status:** `OWNER_ACCEPTED_COMMITTED_LOCAL`  
**Date:** 2026-09-15  
**Step:** `GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15`  
**Phase:** `PKG_2C_CONTEXTUAL_ACCESS_AND_FK_RECONCILIATION`

## 0. Baseline record

```text
BASELINE_ID=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
STEP=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
PHASE=PKG_2C_CONTEXTUAL_ACCESS_AND_FK_RECONCILIATION
DATE=2026-09-15
MIGRATION_HEAD=V58
VERIFIED_FILE_COUNT=52
BASELINE_REUSE_ALLOWED=YES
REUSE_POLICY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/VERIFIED_BASELINE_REUSE.md
REGISTERED_IN=Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md
```

Its registration in `Reglas.md` is the entry
`2026-09-15 — GYPPORT® Universe / Registro de Verified Baseline PKG2C`.

## 1. Purpose

This document is the canonical reusable verification baseline for PKG-2C.

Future STEPs MUST NOT rerun the complete PKG-2C regression when this baseline remains valid.
They must first prove whether the baseline is still valid by checking the accepted commits,
relevant paths/contracts, migrations and architecture invariants.

If the baseline remains valid:

```text
PKG_2C_BASELINE_REUSED=YES
PKG_2C_FULL_REGRESSION_RERUN=NO
```

If a later change invalidates this baseline, only the affected verification scope must be rerun,
unless the impact analysis requires the full matrix.

## 2. Accepted commits

```text
gm-entities
e6d3cbcc5e004e8fbd11c78dc1817b5a00e6bffb

gm-security
1654f271711e96761ae7d5470dce3d161cb4333b

Gystigo
a3b7bfeb1b52f06110cd08af185b04f3690b4a43
```

Baseline parent commits:

```text
gm-entities
7b2c56fc5141f38f2bb1e14f11c6d32e3eecca2e

gm-security
ee3c2a95efb4efa61b3eaf6405df4e3822b56e4b

Gystigo
59bd77f0bf6a2aa6b1c3083097a8c8e0b258ff56
```

Branches at commit time: gm-entities `feat/entities-initial-development`, gm-security `master`,
Gystigo `feature/gm-fleets-minimum-vehicle-master-01`. Nothing was pushed.

## 3. Accepted scope

```text
GM_ENTITIES_FILES_COMMITTED=17
GM_SECURITY_FILES_COMMITTED=8
GYSTIGO_FILES_COMMITTED=27
TOTAL_PKG_2C_FILES_COMMITTED=52
VERIFIED_FILE_COUNT=52
UNRELATED_FILES_COMMITTED=0
```

The 52 accepted files are represented canonically by the three accepted Git commits above.
Per-file hashes may be retained as secondary evidence, but the commit SHAs are the primary
byte identity for this baseline. Appendix A lists the files with their blob ids.

Commit-gate byte proof:

```text
COMMITTED_BYTES_MATCH_ACCEPTED_BYTES=YES
WORKTREE_EQUALS_ACCEPTED=52/52
BLOB_EQUALS_GIT_HASH_OBJECT=52/52
BYTE_IDENTICAL=50
EOL_NORMALIZED_ONLY=2
```

The two `EOL_NORMALIZED_ONLY` files are gm-entities tests (`AddPartyIdentifierUseCaseTest`,
`GetPartyProfileUseCaseTest`): Git stored their CRLF working copies as LF, as that repository's
`.gitattributes` requires.

## 4. Migration baseline

```text
MIGRATION_HEAD=V58

V57=tenant access subject membership FKs
V58=global user account actor FKs
```

```text
Gystigo/database/core/migration/V57__tenant_access_subject_membership_fks.sql
Gystigo/database/core/migration/V58__global_user_account_actor_fks.sql
```

Shared DEV was intentionally not migrated by this STEP.

```text
SHARED_DEV_FLYWAY_VERSION=V43
SHARED_DEV_CHANGED=NO
DEV_WRITES_BY_THIS_STEP=0
```

Three read-only snapshots of shared DEV, taken before the final regression, after it and at the
commit gate, are identical.

## 5. Canonical architecture invariants

```text
IDENTITY=GLOBAL
BUSINESS_PARTICIPATION=TENANT_CONTEXTUAL
ACCESS=SECURITY
EMPLOYMENT=HR
AUDIT_ACTOR=GLOBAL_ACCOUNT
```

```text
MdmParty=GLOBAL_IDENTITY_GOLDEN_RECORD
Party=TENANT_CONTEXTUAL_BUSINESS_PARTICIPATION
GlobalUserAccount=GLOBAL_AUTHENTICATION_ACCOUNT
UserTenantMembership=ACCOUNT_TO_TENANT_ACCESS
HistoricalActor=GLOBAL_USER_ACCOUNT
```

```text
ACTIVE_MEMBERSHIP_REQUIRES_PARTY=NO
PARTY_PROJECTION_POLICY=LAZY_EXPLICIT
CONTEXTUAL_PARTY_READ_IS_READ_ONLY=YES
LOGIN_CREATES_PARTY=NO
AUTH_ME_CREATES_PARTY=NO
AUTHORIZATION_READ_CREATES_PARTY=NO
```

Access subject ownership:

```text
ACCESS_SUBJECTS=USER_TENANT_MEMBERSHIP

user_roles -> UserTenantMembership
organization_access -> UserTenantMembership
tenant user_sessions -> UserTenantMembership
user_branches -> UserTenantMembership
user_establishments -> UserTenantMembership
```

Historical actor ownership:

```text
ACTOR_FKS=GLOBAL_USER_ACCOUNT
ACTOR_FIELDS_MOVED_TO_MEMBERSHIP=0
TENANT_REMAINS_ACTOR_CONTEXT=YES
PLATFORM_ADMIN_ACTOR_WITHOUT_MEMBERSHIP_SUPPORTED=YES
```

Deferred:

```text
EVC_PRC_ACCOUNT_FK_RESHAPE=DEFER
USER_ACCOUNTS_TENANT_ID_CHANGED=NO
USER_ACCOUNTS_PARTY_ID_CHANGED=NO
```

## 6. Owner-accepted verification evidence

Final regression ran on one stable snapshot with zero drift: 2026-09-15, 11:38–12:21 (-05:00),
on the parent commits above plus the 52 accepted working-tree files. Their hashes matched the
accepted fingerprint (52/52) at the start and at the end, and the controlled commits recorded
exactly those bytes (section 3).

```text
FULL_RUNTIME_MATRIX=39/39_EXECUTED
NEW_FAILURES=0
KNOWN_PREEXISTING_FAILURES=3
```

Module and host evidence:

```text
GM_ENTITIES_TESTS=217/217
GM_SECURITY_TESTS=111/111
GM_EXPENSES_REAL_DB=84/84
NORMAL_HOST_TESTS=675 run, 0 failures, 0 errors, 251 skipped
STUDIO_CONTRACTS=581/581
STUDIO_BUILD=PASS
HOST_POST_COMMIT_COMPILE=PASS
PKG_2C_HOST_UNIT_TESTS=113/113
```

`HOST_POST_COMMIT_COMPILE` and `PKG_2C_HOST_UNIT_TESTS` are the post-commit smoke: gm-entities
(217/217) and gm-security (111/111) were reinstalled from their clean committed HEADs, then the
Host test-compiled against them and ran nine PKG-2C Host unit test classes (113 tests).

The 39 matrix entries ran on disposable MySQL, with disposable Mailpit where needed, through
`Gystigo/platform_os/server/scripts/run-host-isolated-db-tests.ps1`. Every container was
disposed. Appendix B lists the entries.

PKG-2C checkpoints:

```text
PKG2C1_CHECKPOINT=GREEN
PKG2C2_CHECKPOINT=GREEN
PKG2C3_CHECKPOINT=GREEN
```

## 7. Known pre-existing debts

These failures were reproduced identically and are NOT PKG-2C regressions:

```text
1. TeamEmployeeRealDatabaseAcceptanceTest
   current line: 90
   previous line: 84
   expected: 2
   actual: 0
   matrix entry: 22 (m_team)

2. TeamEmployeeControllerScopeBoundaryRealDatabaseAcceptanceTest
   createRole:194
   expected: 201
   actual: 403
   matrix entry: 25 (m_rbac_scope)

3. PersonIdentityReconciliationHttpTest:222
   expected: 200
   actual: 403
   matrix entry: 37 (m_identity_reconciliation)
```

The TeamEmployee assertion moved from line 84 to line 90 because PKG-2C added six import and
field lines to that test; the failing assertion itself is unchanged.

Future STEPs must not opportunistically fix these debts unless they are explicitly in scope.

## 8. Baseline reuse rule

A future STEP MAY reuse this baseline when all are true:

```text
A. Accepted commits are still ancestors of the current repository state.
B. No PKG-2C relevant path or contract has changed in a way that affects the invariant being reused.
C. No migration supersedes or reshapes V57/V58 semantics.
D. No security/MDM ownership decision above has changed.
E. No dependency contract change invalidates the tested behavior.
```

When reusable:

```text
BASELINE_FOUND=YES
BASELINE_ID=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15
BASELINE_REUSE_DECISION=REUSE
FULL_HISTORICAL_REGRESSION_RERUN=NO
PKG_2C_BASELINE_REUSED=YES
PKG_2C_FULL_REGRESSION_RERUN=NO
```

The new STEP runs only:

```text
- its own unit/module tests
- impact-selected regression tests
- required integration smoke tests
```

Appendix A gives the paths for check B, and Appendix B the suites from which impact-selected
tests are chosen. The validity check procedure is in `VERIFIED_BASELINE_REUSE.md`.

## 9. Baseline invalidation triggers

This baseline MUST be reviewed or partially/full invalidated if a later STEP changes any of:

```text
MdmParty / Party identity-participation relationship
tenant_id + mdm_party_id contextual Party resolution
Global UserAccount identity relationship
UserTenantMembership semantics
user_roles subject ownership
organization_access subject ownership
tenant user_sessions subject ownership
user_branches subject ownership
user_establishments subject ownership
historical actor FK ownership
V57 or V58 migration semantics
login/auth/me/authorization Party provisioning behavior
Platform Admin tenantless actor behavior
```

A baseline invalidation does not automatically require a full 39-entry rerun.
Impact analysis determines the smallest sufficient verification scope.

## 10. Commit-gate result

```text
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
PKG_2C_CLOSED=YES
UNRELATED_FILES_COMMITTED=0
OWNER_WIP_PRESERVED=YES
GM_EXPENSES_WIP_PRESERVED=YES
OTHER_UNRELATED_WIP_PRESERVED=YES
FILES_STAGED_AFTER_GATE=0
PUSH_PERFORMED=NO
```

## 11. Next package

```text
NEXT_PACKAGE=PKG_2D
PKG_2D_SCOPE=CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
AUTO_START_NEXT_PACKAGE=NO
```

PKG-2D must begin from this baseline rather than reconstructing or rerunning PKG-2C.

## 12. Related documents

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/VERIFIED_BASELINE_REUSE.md
Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MDM_UNIVERSAL_GLOBAL_ACCOUNT_PKG2C_2026-09-15.md
Gystigo/docs/architecture/decisions/ADR-0018-GLOBAL-USER-ACCOUNT-AND-TENANT-MEMBERSHIP.md
Gystigo/docs/testing/TEST_DATABASE_ISOLATION.md
```

## Appendix A — Accepted commit manifest

Secondary evidence read from the accepted commits, one line per file:
`<status> <abbreviated blob id> <path>`, with paths relative to the repository. A full blob id
is `git -C <repository> rev-parse <commit>:<path>`.

```text
gm-entities e6d3cbcc5e004e8fbd11c78dc1817b5a00e6bffb files=17
M e04313a0c60d src/main/java/com/gypport/business/entities/application/ReviewOrganizationControlClaimUseCase.java
M f7c6c5ffb3f5 src/main/java/com/gypport/business/entities/party/domain/PartyRelationshipVerification.java
M d467df171f56 src/main/java/com/gypport/business/entities/party/domain/PartyRelationshipVerificationEvidence.java
M 9f0141904a31 src/main/java/com/gypport/business/entities/party/domain/TenantPartyRepository.java
M 7d7d9e090808 src/main/java/com/gypport/business/entities/party/infrastructure/persistence/jdbc/JdbcPartyRelationshipVerificationEvidenceRepository.java
M d273991a0ee4 src/main/java/com/gypport/business/entities/party/infrastructure/persistence/jdbc/JdbcPartyRelationshipVerificationRepository.java
M e6801d6973e9 src/main/java/com/gypport/business/entities/party/infrastructure/persistence/jdbc/JdbcTenantPartyRepository.java
M d0227da80137 src/test/java/com/gypport/business/entities/application/AddPartyIdentifierUseCaseTest.java
M 0706c1a7804c src/test/java/com/gypport/business/entities/application/CreateOrganizationPartyUseCaseTest.java
M f5e158371c13 src/test/java/com/gypport/business/entities/application/CreatePersonPartyUseCaseTest.java
M 6e49bf0b9d91 src/test/java/com/gypport/business/entities/application/GetPartyProfileUseCaseTest.java
M c95ff7ba4ac6 src/test/java/com/gypport/business/entities/application/ReviewOrganizationControlClaimUseCaseTest.java
M 22167f03941e src/test/java/com/gypport/business/entities/identity/application/IdentityClaimServiceTest.java
M 5fc3310a3d09 src/test/java/com/gypport/business/entities/intake/application/SubmitIdentityIntakeUseCaseTest.java
M a5bc7444c531 src/test/java/com/gypport/business/entities/party/domain/PartyRelationshipVerificationEvidenceTest.java
M 6a946e1123df src/test/java/com/gypport/business/entities/party/domain/PartyRelationshipVerificationTest.java
M c0d307603ee9 src/test/java/com/gypport/business/entities/party/infrastructure/persistence/jdbc/JdbcTenantPartyRepositoryTest.java
```

```text
gm-security 1654f271711e96761ae7d5470dce3d161cb4333b files=8
M da26186d6b47 src/main/java/com/gypport/business/security/application/RoleProvisioningPort.java
M 799712dbf137 src/main/java/com/gypport/business/security/application/UserAccountProfileRecord.java
M d393f8540c3f src/main/java/com/gypport/business/security/application/UserAccountRepository.java
M e4675e6fd78c src/main/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcPartyAccessQueryAdapter.java
M a8e5a2f88b1e src/main/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcRoleProvisioningAdapter.java
M 5a510525f6f7 src/main/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcUserAccountRepository.java
M 5080b10ef665 src/test/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcPartyAccessQueryAdapterTest.java
M ff382107705f src/test/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcUserAccountRepositoryTest.java
```

```text
Gystigo a3b7bfeb1b52f06110cd08af185b04f3690b4a43 files=27
A c675cceccc98 database/core/migration/V57__tenant_access_subject_membership_fks.sql
A cd0145d4243e database/core/migration/V58__global_user_account_actor_fks.sql
M 1cd0a970d6bb docs/testing/TEST_DATABASE_ISOLATION.md
M 74512773435b platform_os/server/src/main/java/com/gypport/server/module/humanresources/EmployeeAccessGrantService.java
M d70b8a00465d platform_os/server/src/main/java/com/gypport/server/module/onboarding/application/RegisterPersonAccountUseCase.java
M 785f730b7f01 platform_os/server/src/main/java/com/gypport/server/module/organizations/ClaimOrganizationControlUseCase.java
M aef187ad7df0 platform_os/server/src/main/java/com/gypport/server/module/organizations/ConfirmOrganizationControlUseCase.java
M 1bf89c011a07 platform_os/server/src/main/java/com/gypport/server/module/organizations/ReviewOrganizationControlUseCase.java
M 2eee9f203e3f platform_os/server/src/main/java/com/gypport/server/shared/config/GmOrganizationsConfig.java
A e2764e2e25e1 platform_os/server/src/test/java/com/gypport/server/module/entities/ContextualPartyReadRealDatabaseAcceptanceTest.java
M 735b3bbb1ab6 platform_os/server/src/test/java/com/gypport/server/module/entities/GmEntitiesHostIntegrationTest.java
M b7a11a8affeb platform_os/server/src/test/java/com/gypport/server/module/humanresources/EmployeeAccessRevocationRealDatabaseAcceptanceTest.java
M 5319c4bd50dc platform_os/server/src/test/java/com/gypport/server/module/humanresources/EmployeeEmploymentUpdateRealDatabaseAcceptanceTest.java
M 6e1623fe6e5e platform_os/server/src/test/java/com/gypport/server/module/humanresources/TeamEmployeeRealDatabaseAcceptanceTest.java
M 0e23c960784b platform_os/server/src/test/java/com/gypport/server/module/onboarding/application/RegisterPersonAccountUseCaseTest.java
M e741dc777acb platform_os/server/src/test/java/com/gypport/server/module/organizations/ClaimOrganizationControlUseCaseTest.java
M 3eb72d6e8ae8 platform_os/server/src/test/java/com/gypport/server/module/organizations/ConfirmOrganizationControlUseCaseTest.java
M 7ad8ae27ec10 platform_os/server/src/test/java/com/gypport/server/module/organizations/GmOrganizationsRealDatabaseAcceptanceTest.java
M 948ee15665ba platform_os/server/src/test/java/com/gypport/server/module/organizations/OrganizationControlActivationRealDatabaseAcceptanceTest.java
M 91468dcf9cfd platform_os/server/src/test/java/com/gypport/server/module/organizations/ReviewOrganizationControlUseCaseTest.java
M b4928a21aac7 platform_os/server/src/test/java/com/gypport/server/module/platform/PlatformAdminRealDatabaseAcceptanceTest.java
M 60c1e84c462c platform_os/server/src/test/java/com/gypport/server/module/profile/application/MyProfileServiceTest.java
M 2704a09186e2 platform_os/server/src/test/java/com/gypport/server/module/profile/application/ProfileIdentityServiceTest.java
A 124a0b303165 platform_os/server/src/test/java/com/gypport/server/module/security/GlobalUserAccountActorRealDatabaseAcceptanceTest.java
A 38fb9fda771d platform_os/server/src/test/java/com/gypport/server/shared/persistence/GlobalUserAccountActorFkMigrationRealDatabaseAcceptanceTest.java
A 96fee48253c7 platform_os/server/src/test/java/com/gypport/server/shared/persistence/TenantAccessSubjectMembershipFkMigrationRealDatabaseAcceptanceTest.java
A 5bf50d2a324b platform_os/server/src/test/java/com/gypport/server/shared/persistence/TenantAccessSubjectMembershipFkMigrationStopRealDatabaseAcceptanceTest.java
```

## Appendix B — Runtime matrix

The final regression's 39 disposable entries, in execution order. `Flyway` is the highest
migration the entry's database reached; migration and STOP suites pin their own version.
Errors were 0 in every entry, and skipped tests were 0 except in entry 6 (246).

| # | Entry | Suite | Tests | Failures | Flyway | Result |
|---:|---|---|---:|---:|---|---|
| 1 | m_contextual_party | ContextualPartyReadRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 2 | m_v57 | TenantAccessSubjectMembershipFkMigrationRealDatabaseAcceptanceTest | 1 | 0 | V57 | PASS |
| 3 | m_v57_stop | TenantAccessSubjectMembershipFkMigrationStopRealDatabaseAcceptanceTest | 1 | 0 | V57 | PASS |
| 4 | m_v58 | GlobalUserAccountActorFkMigrationRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 5 | m_v58_actor | GlobalUserAccountActorRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 6 | m_context_all | every Host test, against a disposable database | 675 | 0 | V58 | PASS |
| 7 | m_group_a | GmEntitiesHostIntegrationTest, CorsConfigurationSecurityTest, OnboardingHostIntegrationTest, GmHumanResourcesRealDatabaseAcceptanceTest, GystigoAuthenticatedTenantBoundaryHttpTest, MyProfileHostIntegrationTest, MailpitEmailVerificationAcceptanceTest, MailpitPasswordRecoveryAcceptanceTest (with Mailpit) | 43 | 0 | V58 | PASS |
| 8 | m_pending_acceptance | PendingAccountIdentityRealDatabaseAcceptanceTest | 9 | 0 | V58 | PASS |
| 9 | m_pending_migration | PendingAccountIdentityMigrationRealDatabaseAcceptanceTest | 1 | 0 | V52 | PASS |
| 10 | m_pending_migration_stop | PendingAccountIdentityMigrationStopRealDatabaseAcceptanceTest | 1 | 0 | V51 | PASS |
| 11 | m_membership_v53_v54 | UserTenantMembershipMigrationRealDatabaseAcceptanceTest | 1 | 0 | V54 | PASS |
| 12 | m_membership_v53_stop | UserTenantMembershipMigrationStopRealDatabaseAcceptanceTest | 1 | 0 | V53 | PASS |
| 13 | m_membership_v54_stop | OneActiveAccountPerGoldenRecordMigrationStopRealDatabaseAcceptanceTest | 1 | 0 | V54 | PASS |
| 14 | m_membership_v55 | UserTenantMembershipCatchUpMigrationRealDatabaseAcceptanceTest | 1 | 0 | V55 | PASS |
| 15 | m_membership_v55_stop | UserTenantMembershipCatchUpMigrationStopRealDatabaseAcceptanceTest | 1 | 0 | V55 | PASS |
| 16 | m_membership_runtime | UserTenantMembershipRuntimeWriterRealDatabaseAcceptanceTest | 8 | 0 | V58 | PASS |
| 17 | m_membership_v56 | TenantlessPlatformSessionMigrationRealDatabaseAcceptanceTest | 1 | 0 | V56 | PASS |
| 18 | m_signin_gate | SignInMembershipGateRealDatabaseAcceptanceTest | 6 | 0 | V58 | PASS |
| 19 | m_platform_session | PlatformSessionRealDatabaseAcceptanceTest | 5 | 0 | V58 | PASS |
| 20 | m_route_boundary | SessionRouteBoundaryRealDatabaseAcceptanceTest | 4 | 0 | V58 | PASS |
| 21 | m_team_access | EmployeeAccessGrantRealDatabaseAcceptanceTest (with Mailpit) | 1 | 0 | V58 | PASS |
| 22 | m_team | TeamEmployeeRealDatabaseAcceptanceTest | 1 | 1 | V58 | KNOWN DEBT 1 |
| 23 | m_team_employment | EmployeeEmploymentUpdateRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 24 | m_team_revocation | EmployeeAccessRevocationRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 25 | m_rbac_scope | TeamEmployeeControllerScopeBoundaryRealDatabaseAcceptanceTest | 1 | 1 | V58 | KNOWN DEBT 2 |
| 26 | m_organization_rbac | OrganizationRoleAdministrationRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 27 | m_organization_control | OrganizationControlActivationRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 28 | m_gm_organizations | GmOrganizationsRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 29 | m_platform_admin | PlatformAdminRealDatabaseAcceptanceTest | 1 | 0 | V58 | PASS |
| 30 | m_tenant_safe_fk | TenantSafeReferenceIntegrityRealDatabaseAcceptanceTest | 4 | 0 | V47 | PASS |
| 31 | m_tenant_safe_stop | TenantSafeProductScopeMigrationStopRealDatabaseAcceptanceTest | 1 | 0 | V46 | PASS |
| 32 | m_tax_subject | TaxSubjectFoundationRealDatabaseAcceptanceTest | 4 | 0 | V49 | PASS |
| 33 | m_establishment_stop | UserEstablishmentAccessMigrationStopRealDatabaseAcceptanceTest | 1 | 0 | V48 | PASS |
| 34 | m_collation | IdentityCollationReconciliationRealDatabaseAcceptanceTest | 3 | 0 | V50 | PASS |
| 35 | m_collation_stop | IdentityCollationMigrationStopRealDatabaseAcceptanceTest | 1 | 0 | V49 | PASS |
| 36 | m_identity_intake | UniversalIdentityIntakeRealDatabaseAcceptanceTest | 17 | 0 | V51 | PASS |
| 37 | m_identity_reconciliation | PersonIdentityReconciliationHttpTest | 10 | 1 | V58 | KNOWN DEBT 3 |
| 38 | m_fleets | GmFleetsHttpApiTest | 17 | 0 | V58 | PASS |
| 39 | m_fuel_stations | GmFuelStationsHttpApiTest, GmFuelStationsTransportTankConcurrencyHttpApiTest, GmFuelStationsDischargeMeterHttpApiTest, GmFuelStationsDischargeMeterConcurrencyHttpApiTest | 29 | 0 | V58 | PASS |

```text
MATRIX_ENTRIES=39
PASS=36
KNOWN_DEBT=3
NEW_FAILURES=0
LEFTOVER_TEST_CONTAINERS=0
DRIFT_AFTER_EVERY_ENTRY=0
```

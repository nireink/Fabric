# GYPPORT — PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT Verified Baseline

**Baseline ID:** `GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16`  
**Status:** `OWNER_ACCEPTED_COMMITTED_LOCAL`  
**Date:** 2026-09-16  
**Step:** `GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15`  
**Phase:** `PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION`

## Purpose

This is the canonical reusable verification baseline of an Owner-accepted, locally committed STEP.

Future STEPs MUST NOT rerun its complete historical regression while this baseline remains valid. They first
classify it as REUSE, PARTIAL_INVALIDATION or FULL_INVALIDATION under the policy:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/VERIFIED_BASELINE_REUSE.md
```

## Baseline record

```text
BASELINE_ID=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
STEP=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
PHASE=PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
DATE=2026-09-16
MIGRATION_HEAD=V61
VERIFIED_FILE_COUNT=101
BASELINE_REUSE_ALLOWED=YES
```

## Accepted commits

```text
gm-security=d3fa0b470cb117fb5c1620b6860ecc34ad73a50d
Gystigo=d9f3ddecc76d81993168de7536f756c7c4d0a3ac
Fabric=cc194e4d3d63bed4369fbc934ca0695d8fc6a990
```

Parent commits:

```text
gm-security=1654f271711e96761ae7d5470dce3d161cb4333b
Gystigo=0544e2ec9dcf7bc883e8f57c498e7ac5fb23cbeb
Fabric=026959b6a5d24a8bd57808cf4c2f68a50a5ad3dd
```

## Accepted commit manifest

Secondary evidence read from the accepted commits, one line per file: `<status> <abbreviated blob id> <path>`,
with paths relative to the repository.

```text
gm-security d3fa0b470cb117fb5c1620b6860ecc34ad73a50d files=18
A 350dfc16c6b8 src/main/java/com/gypport/business/security/application/ActiveUserAccountLookupPort.java
A c29e2ce9c00b src/main/java/com/gypport/business/security/application/AdoptExistingUserAccountIntoTenantUseCase.java
M 6a79dced5801 src/main/java/com/gypport/business/security/application/NewUserAccount.java
A ef02b2e707ac src/main/java/com/gypport/business/security/application/TenantAdoptionOutcome.java
M 98dc2e5b82f1 src/main/java/com/gypport/business/security/application/UserAccountAuthRecord.java
M 20c1eb5639f9 src/main/java/com/gypport/business/security/application/UserAccountListing.java
M 8e1c84ba84e1 src/main/java/com/gypport/business/security/application/UserAccountProfileRecord.java
M 0ba5702bbec9 src/main/java/com/gypport/business/security/application/UserAccountRepository.java
M 59a5fb7a7fde src/main/java/com/gypport/business/security/application/UserTenantMembershipRepository.java
M 9fe88a3cf229 src/main/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcPartyAccessQueryAdapter.java
M bd4676fd83d1 src/main/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcUserAccountDirectoryAdapter.java
M c4b560946fa5 src/main/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcUserAccountRepository.java
M 139a35e1a500 src/main/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcUserTenantMembershipRepository.java
A 89a6a2c5f24c src/test/java/com/gypport/business/security/application/AdoptExistingUserAccountIntoTenantUseCaseTest.java
M bea16a9b3937 src/test/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcPartyAccessQueryAdapterTest.java
M 4ee829299897 src/test/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcUserAccountDirectoryAdapterTest.java
M 3e8ca787f8af src/test/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcUserAccountRepositoryLinkTest.java
M f32950b9dbbc src/test/java/com/gypport/business/security/infrastructure/persistence/jdbc/JdbcUserAccountRepositoryTest.java
```

```text
Gystigo d9f3ddecc76d81993168de7536f756c7c4d0a3ac files=77
A ba38975dd1ac database/core/migration/V59__global_account_challenge_references.sql
A f5a73e9c6b87 database/core/migration/V60__global_username_uniqueness.sql
A e65c7c066951 database/core/migration/V61__user_account_origin_columns.sql
M bf51eb8d94ff docs/architecture/decisions/ADR-0018-GLOBAL-USER-ACCOUNT-AND-TENANT-MEMBERSHIP.md
M ac63020f09c9 docs/testing/TEST_DATABASE_ISOLATION.md
M 6c5636c55daf platform_os/server/src/main/java/com/gypport/server/module/auth/application/EmailVerificationService.java
M f1a98ad13582 platform_os/server/src/main/java/com/gypport/server/module/auth/application/PasswordRecoveryService.java
M 61d205e4d70e platform_os/server/src/main/java/com/gypport/server/module/auth/application/SessionService.java
M e3ef2db515da platform_os/server/src/main/java/com/gypport/server/module/auth/domain/EmailVerificationChallenge.java
M d02a36c8dee4 platform_os/server/src/main/java/com/gypport/server/module/auth/domain/EmailVerificationChallengeRepository.java
M c968f96f620f platform_os/server/src/main/java/com/gypport/server/module/auth/domain/NewEmailVerificationChallenge.java
M e96d5cb4d34c platform_os/server/src/main/java/com/gypport/server/module/auth/domain/NewPasswordRecoveryChallenge.java
M 5408e79642f9 platform_os/server/src/main/java/com/gypport/server/module/auth/domain/PasswordRecoveryChallenge.java
M 1b158117a548 platform_os/server/src/main/java/com/gypport/server/module/auth/domain/PasswordRecoveryChallengeRepository.java
M 4acd9c1398d6 platform_os/server/src/main/java/com/gypport/server/module/auth/infrastructure/persistence/jdbc/JdbcEmailVerificationChallengeRepository.java
M 642eb83a5f72 platform_os/server/src/main/java/com/gypport/server/module/auth/infrastructure/persistence/jdbc/JdbcPasswordRecoveryChallengeRepository.java
M 4d421d63130a platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseAdvanceController.java
M 189fc3fca6b5 platform_os/server/src/main/java/com/gypport/server/module/humanresources/EmployeeAccessGrantService.java
M 6e388eca0538 platform_os/server/src/main/java/com/gypport/server/module/onboarding/application/ExistingAccountClaimContinuationService.java
A 0b48d5e1a767 platform_os/server/src/main/java/com/gypport/server/module/onboarding/application/RegisterAdditionalTenantUseCase.java
A 05669f345af5 platform_os/server/src/main/java/com/gypport/server/module/party/application/ContextualParticipationService.java
M d1b1112d9bd7 platform_os/server/src/main/java/com/gypport/server/module/platform/JdbcPlatformUserAccountQueryAdapter.java
M cd636941f426 platform_os/server/src/main/java/com/gypport/server/module/profile/application/MyProfileService.java
M bb6b6a7acdff platform_os/server/src/main/java/com/gypport/server/module/profile/application/ProfileIdentityService.java
M 2be5fcba2e17 platform_os/server/src/main/java/com/gypport/server/module/profile/controller/MeProfileController.java
A f4f664ade2a1 platform_os/server/src/main/java/com/gypport/server/module/tenant/application/TenantDirectoryPort.java
M 4ae5a005d9c1 platform_os/server/src/main/java/com/gypport/server/module/tenant/controller/AuthController.java
A 51edea64c29d platform_os/server/src/main/java/com/gypport/server/module/tenant/infrastructure/persistence/jdbc/JdbcTenantDirectoryAdapter.java
M 35a46fbad63d platform_os/server/src/main/java/com/gypport/server/shared/config/GmHumanResourcesConfig.java
M 890b99964a7e platform_os/server/src/main/java/com/gypport/server/shared/config/GmSecurityConfig.java
M 4ffc74894df5 platform_os/server/src/main/java/com/gypport/server/shared/config/OnboardingConfig.java
M b7a56e596117 platform_os/server/src/main/java/com/gypport/server/shared/config/ProfileConfig.java
M 9485f3cd2919 platform_os/server/src/main/java/com/gypport/server/shared/config/TenantProvisioningConfig.java
M a1a8e3becbd6 platform_os/server/src/test/java/com/gypport/server/module/auth/GystigoAuthenticatedTenantBoundaryHttpTest.java
M bd4f4c9c0711 platform_os/server/src/test/java/com/gypport/server/module/auth/PlatformSessionRealDatabaseAcceptanceTest.java
M 93fb568114cb platform_os/server/src/test/java/com/gypport/server/module/auth/SignInMembershipGateRealDatabaseAcceptanceTest.java
M 074c8818f330 platform_os/server/src/test/java/com/gypport/server/module/auth/application/EmailVerificationServiceTest.java
M a62523ff0cd4 platform_os/server/src/test/java/com/gypport/server/module/auth/application/PasswordRecoveryServiceTest.java
M 6b673ad25c69 platform_os/server/src/test/java/com/gypport/server/module/auth/application/SessionServiceTest.java
M 81ab655fe6d8 platform_os/server/src/test/java/com/gypport/server/module/auth/infrastructure/persistence/jdbc/JdbcEmailVerificationChallengeRepositoryTest.java
M 0a2691464b22 platform_os/server/src/test/java/com/gypport/server/module/entities/ContextualPartyReadRealDatabaseAcceptanceTest.java
M b69a9f85b3d9 platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseCaseHttpApiTest.java
M 693797ad70da platform_os/server/src/test/java/com/gypport/server/module/expenses/GmExpensesHttpApiTest.java
M a3235a39049a platform_os/server/src/test/java/com/gypport/server/module/fleets/GmFleetsHttpApiTest.java
M 7c40ea49b985 platform_os/server/src/test/java/com/gypport/server/module/fuelstations/GmFuelStationsDischargeMeterHttpApiTest.java
M a5e66263ec00 platform_os/server/src/test/java/com/gypport/server/module/fuelstations/GmFuelStationsHttpApiTest.java
M eb4e9c5eb6ba platform_os/server/src/test/java/com/gypport/server/module/humanresources/EmployeeAccessGrantRealDatabaseAcceptanceTest.java
M c8678775fe48 platform_os/server/src/test/java/com/gypport/server/module/humanresources/EmployeeAccessGrantServiceTest.java
M cc685b498bfa platform_os/server/src/test/java/com/gypport/server/module/humanresources/EmployeeAccessRevocationRealDatabaseAcceptanceTest.java
M b27bb07202c7 platform_os/server/src/test/java/com/gypport/server/module/humanresources/EmployeeEmploymentUpdateRealDatabaseAcceptanceTest.java
M 8deb0d2983c5 platform_os/server/src/test/java/com/gypport/server/module/humanresources/GmHumanResourcesRealDatabaseAcceptanceTest.java
M b29e9011d206 platform_os/server/src/test/java/com/gypport/server/module/humanresources/TeamEmployeeControllerScopeBoundaryRealDatabaseAcceptanceTest.java
M ca34636b9b71 platform_os/server/src/test/java/com/gypport/server/module/humanresources/TeamEmployeeRealDatabaseAcceptanceTest.java
M 4f0625f3625c platform_os/server/src/test/java/com/gypport/server/module/onboarding/OnboardingHostIntegrationTest.java
M 32509ee4a0fe platform_os/server/src/test/java/com/gypport/server/module/onboarding/PendingAccountIdentityRealDatabaseAcceptanceTest.java
M f0c90e5b4853 platform_os/server/src/test/java/com/gypport/server/module/onboarding/application/RegisterPersonAccountUseCaseTest.java
M 70ae47d1e9ee platform_os/server/src/test/java/com/gypport/server/module/organizations/ClaimOrganizationControlUseCaseTest.java
M fc308492cae7 platform_os/server/src/test/java/com/gypport/server/module/organizations/ConfirmOrganizationControlUseCaseTest.java
M e75b33c554e4 platform_os/server/src/test/java/com/gypport/server/module/organizations/GmOrganizationsRealDatabaseAcceptanceTest.java
M a9b2b3d8eb7b platform_os/server/src/test/java/com/gypport/server/module/organizations/OrganizationControlActivationRealDatabaseAcceptanceTest.java
M c61474f16dd8 platform_os/server/src/test/java/com/gypport/server/module/platform/PlatformAdminRealDatabaseAcceptanceTest.java
M 12add0dc5797 platform_os/server/src/test/java/com/gypport/server/module/profile/MyProfileHostIntegrationTest.java
M a38c4a8fda2b platform_os/server/src/test/java/com/gypport/server/module/profile/PersonIdentityReconciliationHttpTest.java
M 3b625388cd68 platform_os/server/src/test/java/com/gypport/server/module/profile/application/MyProfileServiceTest.java
M 63592f624919 platform_os/server/src/test/java/com/gypport/server/module/profile/application/ProfileIdentityServiceTest.java
A 3ee11bb37a7b platform_os/server/src/test/java/com/gypport/server/module/security/CrossTenantAccountAdoptionRealDatabaseAcceptanceTest.java
M a4bf0730db8d platform_os/server/src/test/java/com/gypport/server/module/security/GlobalUserAccountActorRealDatabaseAcceptanceTest.java
M b5de1b625e9e platform_os/server/src/test/java/com/gypport/server/module/security/OrganizationRoleAdministrationRealDatabaseAcceptanceTest.java
M 6f5e25b137ad platform_os/server/src/test/java/com/gypport/server/module/security/UserTenantMembershipRuntimeWriterRealDatabaseAcceptanceTest.java
M 1b3897c9863e platform_os/server/src/test/java/com/gypport/server/shared/config/ResolvedRegistrationFixture.java
A 497bc2f26cc9 platform_os/server/src/test/java/com/gypport/server/shared/persistence/GlobalAccountOriginColumnsMigrationRealDatabaseAcceptanceTest.java
M fd43fc7d1cf3 platform_os/server/src/test/java/com/gypport/server/shared/persistence/PendingAccountIdentityMigrationRealDatabaseAcceptanceTest.java
M a4b9620b992a platform_os/server/src/test/java/com/gypport/server/shared/persistence/TenantAccessSubjectMembershipFkMigrationRealDatabaseAcceptanceTest.java
M aa0d0a707840 platform_os/server/src/test/java/com/gypport/server/shared/persistence/UserTenantMembershipMigrationRealDatabaseAcceptanceTest.java
M 6fad6d400e55 platform_os/studio/channel/browser/shell/src/application/authentication/LoginPage.jsx
M 79035d755741 platform_os/studio/channel/browser/shell/src/application/authentication/authService.js
M b70655dabdb1 platform_os/studio/channel/browser/shell/src/application/authentication/sessionAccess.js
```

```text
Fabric cc194e4d3d63bed4369fbc934ca0695d8fc6a990 files=6
A 7b1ae1a345cf Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MDM_UNIVERSAL_GLOBAL_ACCOUNT_PKG2D_2026-09-16.md
M f40b83aa8226 Knowledge/00-GYPPORT-UNIVERSE/Reglas.md
A 11fc6408a90f Knowledge/00-GYPPORT-UNIVERSE/steps/PKG-2D/PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md
A a3ac1480cccc gm-ai-boxghost/tracks/GYPPORT-GLOBAL-ACCOUNT-TENANT-MEMBERSHIP-FOUNDATION-15/audits/PKG_2D_CROSS_TENANT_ADOPTION_AUDIT_2026-09-15.md
A 4153de769bee gm-ai-boxghost/tracks/GYPPORT-GLOBAL-ACCOUNT-TENANT-MEMBERSHIP-FOUNDATION-15/evidence/PKG_2D_IMPLEMENTATION_EVIDENCE_2026-09-16.md
M bea4387bbaea tools/continuity/Set-GypportCurrentStep.ps1
```

## Verification evidence

```text
PKG2C_BASELINE_IMPACT=PARTIAL_INVALIDATION
PKG2C_BASELINE_IMPACT_REASON=PKG-2D deliberately changed 21 of the 52 files of GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15; the other 31 files and every PKG-2C invariant are unchanged, so the untouched PKG-2C slices stay reusable and the affected slice is superseded by this evidence
UNTOUCHED_PKG2C_SLICE_REUSABLE=YES
FULL_PKG2C_REGRESSION_RERUN=NO
HOST_UNIT_SUITE=675 run, 0 failures
GM_SECURITY_SUITE=122/122, clean install from the committed HEAD d3fa0b4
STUDIO_CONTRACTS=581/581, production build PASS
GLOBAL_ACCOUNT_ADOPTION=PASS (CrossTenantAccountAdoptionRealDatabaseAcceptanceTest, scenarios B-F, H, I, K, L, M, idempotence, create race, REVOKED refused)
MULTI_TENANT_LOGIN=PASS (SessionServiceTest 24/24, SignInMembershipGate, scenarios C and D)
TENANT_SELECTION_REQUIRED=PASS
AUTH_ME_GLOBAL_IDENTITY=PASS (MyProfileHostIntegration, scenario M)
AUTH_ME_AVAILABLE_TENANTS=PASS
CONTEXTUAL_PARTY_RESOLUTION=PASS (ContextualPartyRead, MyProfileServiceTest 10/10, ProfileIdentityServiceTest 5/5, scenarios E and F)
STUDIO_TENANT_SELECTION=PASS (Studio contracts 581/581 and production build)
GLOBAL_USERNAME_UNIQUENESS=PASS (V60 on a real database; scenario L)
EVC_ACCOUNT_REFERENCE_GLOBAL=PASS (V59 on a real database; Mailpit email verification 2/2)
PRC_ACCOUNT_REFERENCE_GLOBAL=PASS (V59 on a real database; password recovery 6/6; scenario K)
IDENTITY_LINK_GLOBAL_ACCOUNT_SEMANTICS=PASS (ProfileIdentityServiceTest, PersonIdentityReconciliationHttpTest 10/10)
PLATFORM_ADMIN_TENANTLESS_SESSION=PASS (PlatformSession, SessionRouteBoundary, PlatformAdmin)
MIGRATION_ACCEPTANCE_SUITES=PASS (GlobalAccountOriginColumnsMigration for V59-V61; every earlier migration and STOP suite at its own Flyway target)
TEAM_EMPLOYEE_ACCEPTANCE=PASS 1/1 (formerly PKG-2C known debt 1)
TEAM_EMPLOYEE_SCOPE_BOUNDARY_ACCEPTANCE=PASS 1/1 (formerly PKG-2C known debt 2)
PERSON_IDENTITY_RECONCILIATION_HTTP=PASS 10/10 (formerly PKG-2C known debt 3)
POST_COMMIT_SMOKE=PASS: gm-security 122/122 from the committed HEAD; TeamEmployee 1/1, ScopeBoundary 1/1 and PersonIdentityReconciliation 10/10 from a worktree holding exactly the committed Gystigo bytes, against the committed gm-expenses module
COMMITTED_TREE_COMPILES_WITHOUT_UNRELATED_WIP=YES (Host main and test sources of the exact commit tree compiled against committed gm-entities, gm-security and gm-expenses)
MIGRATION_BYTES_MATCH_TESTED_STATE=YES (V59, V60 and V61 last written 2026-09-15 22:35, every real-database run later)
DISPOSABLE_DATABASES_ONLY=YES
SHARED_DEV_CHANGED=NO
GM_EXPENSES_WIP_PRESERVED=YES
OTHER_OWNER_WIP_PRESERVED=YES
GM_OPERATIONAL_RESOURCES_TOUCHED=NO
PUSH_PERFORMED=NO
```

## Architecture invariants

```text
IDENTITY=GLOBAL
BUSINESS_PARTICIPATION=TENANT_CONTEXTUAL
ACCESS=SECURITY
EMPLOYMENT=HR
AUDIT_ACTOR=GLOBAL_ACCOUNT
ACCESS_SUBJECT=UserTenantMembership
GLOBAL_USER_ACCOUNT_TENANT_OWNED=NO
USER_TENANT_MEMBERSHIP_IS_ACCESS_SUBJECT=YES
ACTIVE_MEMBERSHIP_REQUIRES_PARTY=NO
PARTY_PROJECTION_POLICY=LAZY_EXPLICIT
CURRENT_TENANT_FROM_ORIGIN_TENANT=NO
CURRENT_PARTY_FROM_ORIGIN_PARTY=NO
ORIGIN_TENANT_AUTHORIZATION_READERS=0
ORIGIN_PARTY_CONTEXTUAL_READERS=0
ACTIVE_LEGACY_ACCOUNT_COLUMN_REFERENCES=0
PLATFORM_ADMIN_REQUIRES_CLIENT_MEMBERSHIP=NO
ADOPTED_MEMBERSHIP_INITIAL_STATUS=ACTIVE
ADOPTION_CREATES_ACCOUNT=NO
ADOPTION_CREATES_PARTY=NO
MULTIPLE_ACTIVE_MEMBERSHIPS_BEHAVIOR=EXPLICIT_TENANT_SELECTION
MVP_USERNAME_MODEL=EMAIL_ALIAS
USERNAME_EQUALS_NORMALIZED_EMAIL=YES
GLOBAL_USERNAME_LOOKUP_TENANT_UNIQUE_MISMATCH=0
EVC_ACCOUNT_REFERENCE_GLOBAL=YES
PRC_ACCOUNT_REFERENCE_GLOBAL=YES
EVC_ORIGIN_ACCOUNT_FK_COUPLING=0
PRC_ORIGIN_ACCOUNT_FK_COUPLING=0
IDENTITY_LINK_ORIGIN_TENANT_COUPLING=0
STUDIO_MULTI_TENANT_GAP=0
FINAL_MIGRATION_HEAD=V61
PKG2D_MIGRATION_COUNT=3
KNOWN_REPRODUCIBLE_TEST_FAILURES_REMAINING=0
KNOWN_DEFERRED_PKG2D_DEBT=0
FORMER_PKG2C_KNOWN_DEBT_1=RESOLVED
FORMER_PKG2C_KNOWN_DEBT_2=RESOLVED
FORMER_PKG2C_KNOWN_DEBT_3=RESOLVED
```

## Known pre-existing debts

```text
KNOWN_PREEXISTING_FAILURES=0
```

## Reuse contract

```text
BASELINE_FOUND=YES
BASELINE_ID=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
BASELINE_REUSE_DECISION=REUSE|PARTIAL_INVALIDATION|FULL_INVALIDATION
BASELINE_REUSE_REASON=<short evidence-based reason>
```

REUSE means `FULL_HISTORICAL_REGRESSION_RERUN=NO`: the new STEP runs only its own tests, impact-selected tests
and the required integration smoke. The decision is proven from repository ancestry, path and contract impact,
migration semantics and current Owner decisions. A complete historical regression is never selected merely
"to be safe".

## Baseline invalidation triggers

- a migration after V61 changes user_accounts, user_tenant_memberships, user_sessions, the challenge tables or the username keys
- any reader derives the current tenant or the contextual Party from user_accounts.origin_tenant_id or origin_party_id
- sign-in stops resolving its candidate tenants from ACTIVE memberships, or accepts a client-supplied tenant without a membership check
- adoption creates an account, a Golden Record, a Person, a Party or a credential, or undoes a REVOKED membership
- the OWNER template becomes tenant-wide or TENANT_USER gains an authority permission, which the three closed suites would fail again
- the gm-expenses Host WIP is committed without its adaptation to MyProfileService.getProfile(tenantId, userAccountId)

An invalidation does not by itself require a full rerun: impact analysis selects the smallest sufficient
verification scope.

## Closeout

```text
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
GENERATED_BY=Fabric/tools/verification/New-GypportVerifiedBaseline.ps1
GENERATOR_MODE=GENERATE_ONLY
GENERATOR_APPROVAL=NONE
OWNER_REVIEW_REQUIRED=YES
AUTO_START_NEXT_STEP=NO
COMMIT_PERFORMED_BY_GENERATOR=NO
PUSH_PERFORMED=NO
```

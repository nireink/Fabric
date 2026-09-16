# PKG-2D audit — cross-tenant global account reuse and adoption

Owner-accepted audit of 2026-09-15, executed in AUDIT_ONLY_FIRST mode against
`steps/PKG-2D/PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md`. Read-only: no file was changed, no test
was run and no database was touched. It is preserved here as operational evidence; the Owner accepted
it and opened the complete implementation package with it.

```text
STATUS=OWNER_ACCEPTED
TRACK=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
PHASE=PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
DATE=2026-09-15
HEADS=Gystigo 0544e2e, gm-entities e6d3cbc, gm-security 1654f27, Fabric 026959b
MIGRATION_HEAD=V58
PKG2C_BASELINE_FOUND=YES
PKG2C_BASELINE_REUSE_DECISION=REUSE
FULL_PKG2C_REGRESSION_RERUN=NO
PKG2C_FILES_UNCHANGED=52/52
FILES_CHANGED=0
```

## Baseline reuse gate

The three accepted PKG-2C commits exist locally and are ancestors of their HEAD. gm-entities and
gm-security have no commit since; Gystigo has one, `0544e2e`, whose 78 files are documentation only,
with zero code or schema paths. Migration head V58 unchanged, V57 and V58 bytes untouched. No Owner
decision since touches an invalidation trigger. Decision: REUSE. The 39-entry matrix was not run.

## Central finding

The schema is already cross-tenant ready; the application is not. V57 moved `user_roles`,
`organization_access`, `user_sessions`, `user_branches` and `user_establishments` onto
`user_tenant_memberships (tenant_id, user_account_id)`, and V56 gave `user_sessions` a single-column
key to `user_accounts`. A membership row in a second tenant is therefore sufficient for a session,
roles and Organization access there, with no migration. What is missing is a writer: only
`RegisterPersonAccountUseCase` (always a brand-new tenant) and `EmployeeAccessGrantService` (only for
accounts it creates itself) create memberships.

## The thirteen known problems

```text
 1 no writer for an existing global account plus an existing tenant
 2 the HR path dead-ends on GLOBAL_ACCOUNT_MEMBERSHIP_REQUIRED / TENANT_MEMBERSHIP_NOT_ACTIVE
 3 SessionService.signInContext considers only user_accounts.tenant_id
 4 /auth/me does not separate global identity from tenant context
 5 MyProfileService, ProfileIdentityService and the login actor read the origin Party
 6 Studio has one tenant and no tenant dimension
 7 LINK_LOCK_ACCOUNT_SQL, LINK_UPDATE_SQL, LINK_PARTY_HOLDERS_SQL and countAccountsForParty are
   keyed by the origin tenant
 8 user_accounts.tenant_id and party_id are consumed as current context in some paths
 9 email_verification_challenge and password_recovery_challenge keep the origin-pair account key
10 the username lookup is global while uk_user_username is tenant-scoped
11 registration still reasons as one account, one tenant
12 adoption must stay safe for pending, unverified and disabled accounts
13 Platform Admin tenantless behaviour must survive the change
```

## What was already correct

Discovery is global (`findActiveByIdentifier` has no tenant predicate;
`findActiveByParty` goes Party → Golden Record → account → membership or legacy origin). Duplication is
blocked by `uk_user_accounts_email_address`, `uk_user_accounts_one_active_per_golden_record` (V54) and
`isGoldenRecordHeldByAnotherAccount`. `uk_party_tenant_mdm` makes a second contextual Party per tenant
impossible. No Party write exists in any login, `/auth/me` or authorization path: the only three
`INSERT INTO parties` sites are reached from explicit provisioning use cases, so LAZY_EXPLICIT holds.

## Classification of the origin-Party readers found

```text
CROSS_TENANT_UNSAFE   MyProfileService:63,87  ProfileIdentityService:32  AuthController:205
ORIGIN_DATA_BY_DESIGN JdbcPlatformUserAccountQueryAdapter:68,102,105,108
                      JdbcPlatformOrganizationControlQueryAdapter:167
NULL_CHECK_ONLY       EmployeeAccessGrantService:208  ExistingAccountClaimContinuationService:83
WRITER                JdbcUserAccountRepository:173 (INSERT_RESOLVED, the account's own origin Party)
```

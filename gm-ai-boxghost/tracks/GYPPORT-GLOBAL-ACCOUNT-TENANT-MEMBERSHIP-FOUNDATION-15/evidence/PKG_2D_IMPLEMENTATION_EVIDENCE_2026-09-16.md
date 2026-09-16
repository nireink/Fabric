# PKG-2D — implementation evidence

```text
TRACK=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
STEP=PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION
PHASE=PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
DATE=2026-09-16
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
COMMIT_STATUS=COMMITTED_LOCAL (gm-security d3fa0b4, Gystigo d9f3dde, Fabric cc194e4 + the closeout commit)
PUSH_STATUS=NOT_PUSHED
SHARED_DEV_STATUS=UNTOUCHED (V43; no database read or write outside disposable containers)
```

## Checkpoints, in the order they were executed and verified

```text
A  gm-security adoption writer                         10/10 unit tests
B  schema: V59, V60, V61 + the code that follows them  gm-security 122/122, disposable-database proof
C  Host, HR and onboarding adoption                    EmployeeAccessGrantServiceTest 19/19
D  membership-driven sign-in and tenant selection      SessionServiceTest 24/24
E  /auth/me, profile and contextual participation      MyProfile 10/10, ProfileIdentity 5/5
F  Studio tenant selection                             581/581 contracts, production build
G  origin misuse sweep                                 ORIGIN_TENANT_AUTHORIZATION_READERS=0
```

## Verification

```text
PKG2C_BASELINE_REUSE_DECISION_BEFORE=REUSE (zero code or schema drift since the accepted commits)
PKG2C_POST_IMPLEMENTATION_IMPACT_DECISION=PARTIAL_INVALIDATION
FULL_PKG2C_REGRESSION_RERUN=NO (the affected slices were rerun, not the 39-entry matrix)

Host unit suite                                   675 run, 0 failures
gm-security suite                                 122 run, 0 failures
Studio contracts                                  581 run, 0 failures; production build succeeds
CrossTenantAccountAdoptionRealDatabaseAcceptanceTest        PASS (scenarios A-F, H, I, K, L, M)
GlobalAccountOriginColumnsMigrationRealDatabaseAcceptanceTest PASS (V59, V60, V61 on a real database)
UserTenantMembershipRuntimeWriterRealDatabaseAcceptanceTest  PASS 8/8
SignInMembershipGate / PlatformSession / SessionRouteBoundary PASS
ContextualPartyRead / MyProfileHostIntegration / GlobalUserAccountActor PASS
PendingAccountIdentity 9/9, OnboardingHostIntegration 3/3      PASS
Mailpit email verification 2/2 and password recovery 6/6       PASS
gm-expenses real-database suite                                84/84 PASS
fleets 17/17, fuel stations 25/25, tenant boundary 10/10       PASS
every migration acceptance and STOP suite                      PASS
```

Every database run used a disposable MySQL container created for that run and removed afterwards. The shared DEV
database, its port and its container were never used.

## The three PKG-2C known debts, closed

The accepted PKG-2C baseline records three known debts. Each was traced from a real run to its first divergence
between the contract the fixture asserts and current behaviour, and each turned out to be an obsolete fixture
expectation of the pre-05C_R1/05C_R2 world, not a production defect. No production file was changed to close them.

```text
KNOWN DEBT 1  TeamEmployeeRealDatabaseAcceptanceTest                         expected 2, actual 0     RESOLVED
KNOWN DEBT 2  TeamEmployeeControllerScopeBoundaryRealDatabaseAcceptanceTest  expected 201, actual 403 RESOLVED
KNOWN DEBT 3  PersonIdentityReconciliationHttpTest:222                       expected 200, actual 403 RESOLVED
```

Registration provisions TENANT_USER, which is scoped tenant-wide but deliberately carries no Organization authority
and no Person-directory administration; the unscoped OWNER template becomes real authority only through an explicit
Organization-scoped grant. The three fixtures each assumed the older model:

- Debt 1 expected the two Employee permissions to exist immediately after registering, and read a tenant-level
  endpoint (`/statuses`, which answers in the session's own context) from the PERSONAL context. It now asserts the
  rule in both directions: zero before the grant, both codes after `grantOrganizationScopedOwnerRole`, 403 on
  `/statuses` while no Organization is selected and 200 once the account operates as the Organization it administers.
- Debt 2 called the Roles API before any Organization-scoped grant existed. It now asserts the absence of
  `security.role.manage` first, makes the explicit grant, and asserts its presence. TENANT_USER's own tenant-wide
  permissions do resolve in every Organization, so the rule is about authority codes, not about an empty set.
- Debt 3 listed and fetched the tenant-wide Person directory from a bare registration. 05C_R2 keeps
  `entities.person.read` out of TENANT_USER deliberately, and the Studio hides the Personas module for the same
  reason, so the fixture now assigns that capability as a role of its own, the way an administrator would.

The same run also caught one real consequence of V61 that had been missed: a fixture query in
`PersonIdentityReconciliationHttpTest` still joined `user_accounts.party_id`. It now reads `origin_party_id`, and the
suite's own tenant lookup for a role assignment reads the account's ACTIVE membership rather than its origin tenant.

```text
TeamEmployeeRealDatabaseAcceptanceTest                         PASS  1/1
TeamEmployeeControllerScopeBoundaryRealDatabaseAcceptanceTest  PASS  1/1
PersonIdentityReconciliationHttpTest                           PASS  10/10
EmployeeAccessGrant / AccessRevocation / EmploymentUpdate      PASS
GmHumanResourcesRealDatabaseAcceptanceTest                     PASS  2/2
OrganizationRoleAdministrationRealDatabaseAcceptanceTest       PASS  1/1
KNOWN_REPRODUCIBLE_TEST_FAILURES_REMAINING=0
```

## Consequences worth recording

- Test suites that prove a historical migration run the Host at a schema older than V61, where the account's origin
  columns still have their legacy names. The shared registration fixture and those suites' own helpers now ask the
  schema which names it has, and the two suites that exercised a production writer at an old schema either migrate to
  the head first or reproduce the effect with the statement the writer issues.
- The HR grant now writes `organization_access` on a successful adoption, so the counts those suites assert moved
  from 1 to 2 where two adoptions happen.
- `git diff --check` is clean for everything this STEP authored.

## Commit gate (2026-09-16, Owner authorized)

Read-only audit first: every uncommitted path of every repository was classified against the post-PKG-2C WIP
fingerprint, the PKG-2D content markers and the PKG-2D time window. UNEXPLAINED_PATHS=0. Two files were shared
with the gm-expenses Host WIP: `ExpenseController.java` carries only an adaptation of WIP code to the new
`MyProfileService.getProfile(tenantId, userAccountId)` signature and stays with that WIP;
`ExpenseCaseHttpApiTest.java` was committed as HEAD plus its two PKG-2D lines only. Before any commit the exact
Gystigo commit tree was compiled, main and test, in a temporary worktree against the committed gm-entities,
gm-security and gm-expenses modules. The gate also registered the two new real-database suites in
`TEST_DATABASE_ISOLATION.md`, which the implementation had left out.

```text
GM_SECURITY_COMMIT=d3fa0b470cb117fb5c1620b6860ecc34ad73a50d   parent 1654f271711e96761ae7d5470dce3d161cb4333b   18 files
GYSTIGO_COMMIT=d9f3ddecc76d81993168de7536f756c7c4d0a3ac       parent 0544e2ec9dcf7bc883e8f57c498e7ac5fb23cbeb   77 files
FABRIC_PKG2D_COMMIT=cc194e4d3d63bed4369fbc934ca0695d8fc6a990  parent 026959b6a5d24a8bd57808cf4c2f68a50a5ad3dd    6 files
FINAL_SCOPE_FILE_COUNT=101
STAGED_SCOPE_EXACT=YES in every commit   UNRELATED_STAGED_PATHS=0   WHITESPACE_CHECK=PASS
FINAL_MIGRATION_HEAD=V61   PKG2D_MIGRATION_COUNT=3   MIGRATION_NUMBER_CONFLICT=NO
ACTIVE_LEGACY_ACCOUNT_COLUMN_REFERENCES=0   ORIGIN_TENANT_AUTHORIZATION_READERS=0   ORIGIN_PARTY_CONTEXTUAL_READERS=0
STALE_ACTIVE_KNOWN_DEBT_REFERENCES=0
POST_COMMIT_SMOKE=PASS (gm-security 122/122 from the committed HEAD; TeamEmployee 1/1, ScopeBoundary 1/1,
                        PersonIdentityReconciliation 10/10 from the committed Gystigo bytes)
PKG2C_BASELINE_IMPACT=PARTIAL_INVALIDATION (21 of 52 files changed; the untouched slice stays reusable)
PKG2D_BASELINE_ID=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
GM_EXPENSES_WIP_PRESERVED=YES   OTHER_OWNER_WIP_PRESERVED=YES   GM_OPERATIONAL_RESOURCES_TOUCHED=NO
SHARED_DEV_CHANGED=NO   PUSH_PERFORMED=NO
```

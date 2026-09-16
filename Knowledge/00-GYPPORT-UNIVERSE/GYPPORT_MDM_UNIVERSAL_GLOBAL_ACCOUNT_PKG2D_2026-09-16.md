# GYPPORT — Global account across tenants (PKG-2D)

```text
TRACK=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
STEP=PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION
PHASE=PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
DATE=2026-09-16
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
SUPERSEDES_RULES_OF=ADR-0018 (the STEP 14 interim guard), GYPPORT_MDM_UNIVERSAL_GLOBAL_ACCOUNT_PKG2C_2026-09-15.md
  (the deferral of the EVC/PRC account keys)
```

This is the single canonical record of what a GYPPORT account means across tenants after PKG-2D. It states the final
semantics; it does not repeat the PKG-2A, PKG-2B or PKG-2C documents, which stay as they are.

## 1. The account

A UserAccount is global. It belongs to no tenant, it is the same account in every tenant, and it is what every
historical actor column names.

```text
IDENTITY=GLOBAL
BUSINESS_PARTICIPATION=TENANT_CONTEXTUAL
ACCESS=SECURITY
EMPLOYMENT=HR
AUDIT_ACTOR=GLOBAL_ACCOUNT
GLOBAL_USER_ACCOUNT_TENANT_OWNED=NO
```

## 2. Origin tenant and origin Party reference

`user_accounts` keeps two columns that record where the account came from. Since V61 their names say exactly that:

```text
user_accounts.origin_tenant_id   the tenant the account was created in
user_accounts.origin_party_id    the Party of that tenant the account was resolved to
```

They are origin data. They are never the current tenant and never the current Party:

```text
CURRENT_TENANT_FROM_ORIGIN_TENANT=NO
CURRENT_PARTY_FROM_ORIGIN_PARTY=NO
ORIGIN_TENANT_AUTHORIZATION_READERS=0
ORIGIN_PARTY_CONTEXTUAL_READERS=0
```

Reading them is legitimate only as provenance: a platform view of where an account came from, the account's own
creation, an identity claim resumed in the tenant it was started in, and migration or backfill logic. Every such
reader is documented at its site.

## 3. Where an account may operate

`user_tenant_memberships` is the only authority. V57 made it the subject of every tenant-scoped access row, so a
membership is what makes a session, a role, an Organization access, a branch and an establishment legal in a tenant.

```text
USER_TENANT_MEMBERSHIP_IS_ACCESS_SUBJECT=YES
ACTIVE_MEMBERSHIP_REQUIRES_PARTY=NO
```

## 4. Adoption

`AdoptExistingUserAccountIntoTenantUseCase` (gm-security) gives an existing global account access to an existing
tenant. It grants access and nothing else.

```text
ADOPTED_MEMBERSHIP_INITIAL_STATUS=ACTIVE
ADOPTION_CREATES_ACCOUNT=NO
ADOPTION_CREATES_MDM_PARTY=NO
ADOPTION_CREATES_PERSON=NO
ADOPTION_CREATES_CONTEXTUAL_PARTY=NO
ADOPTION_CREATES_CREDENTIAL=NO
ADOPTION_CREATES_TENANT=NO
PKG2D_INTRODUCES_INVITATION_WORKFLOW=NO
```

It is idempotent by status: no membership becomes ACTIVE; an ACTIVE one is left as it is, with no second event;
INVITED and SUSPENDED take their canonical transition to ACTIVE; REVOKED is refused, because a revocation was
deliberate and its only canonical way back is a new invitation, which this package does not introduce. Two callers
adopting the same account into the same tenant produce one membership row.

"Dar acceso a GYPPORT" uses it: a Person who already has a GYPPORT account is adopted into the employer's tenant
instead of being refused. The canonical identity decides, so the email typed in the form is not consulted at all when
the Person's Golden Record already has an account.

An account that already exists may also create one more tenant for itself
(`RegisterAdditionalTenantUseCase`, `POST /auth/tenants`): a new tenant, a membership and its roles, reusing the same
account and the same credential.

## 5. Sign-in and tenant selection

The candidate tenants are the account's ACTIVE memberships, never its origin tenant.

```text
MULTIPLE_ACTIVE_MEMBERSHIPS_BEHAVIOR=EXPLICIT_TENANT_SELECTION
0 ACTIVE memberships  -> no tenant session; an active Platform Admin grant still opens a PLATFORM session
1 ACTIVE membership   -> that tenant, directly
>1 ACTIVE memberships -> TENANT_SELECTION_REQUIRED, with the tenants the account may choose between
explicit selection    -> accepted only when the account holds an ACTIVE membership in that tenant
```

No chooser session is created, no credential is persisted, and the chooser carries only a tenant id and a display
name. A tenant id supplied by a client is a request, never a grant.

```text
PLATFORM_ADMIN_REQUIRES_CLIENT_MEMBERSHIP=NO
LOGIN_CREATES_PARTY=NO
```

## 6. Contextual participation

The Party an account participates as, in a tenant, is resolved from the account's Golden Record and that tenant:

```text
current tenant + user_accounts.mdm_party_id -> parties (tenant_id, mdm_party_id) -> Optional contextual Party
```

`ContextualParticipationService` is that read. It never creates, ensures or saves a Party, and absence is a
legitimate answer: an account may hold an ACTIVE membership in a tenant and have no Party there.

```text
PARTY_PROJECTION_POLICY=LAZY_EXPLICIT
CONTEXTUAL_PARTY_MAY_BE_ABSENT=YES
AUTH_ME_CREATES_PARTY=NO
AUTHORIZATION_READ_CREATES_PARTY=NO
MY_PROFILE_MODEL=GLOBAL_IDENTITY_PLUS_CURRENT_TENANT_CONTEXT
```

`/auth/me` reports the three things separately: the global account, the tenants it may operate in, and its
participation in the tenant of this session. A tenant is not an Organization: `availableOrganizations` remains the
Organizations inside the session's tenant. The authenticated actor in a login response is the global account; a Party,
when exposed, is contextual business participation and is reported on its own.

## 7. Username

```text
MVP_USERNAME_MODEL=EMAIL_ALIAS
USERNAME_EQUALS_NORMALIZED_EMAIL=YES
CUSTOM_USERNAME_SUPPORT=NO
GLOBAL_USERNAME_LOOKUP_MATCHES_GLOBAL_UNIQUENESS=YES
```

Authentication looks an account up globally, so uniqueness is global: V60 replaced the tenant-scoped
`uk_user_username` with `uk_user_accounts_username` and retired `uk_user_email`, which the global email key already
covered. `NewUserAccount` normalises the email and refuses any username that is not it.

## 8. Email verification and password recovery

```text
EVC_ACCOUNT_REFERENCE_GLOBAL=YES
PRC_ACCOUNT_REFERENCE_GLOBAL=YES
```

V59 replaced the last two composite account keys in the schema. A challenge names the account alone, "one active
challenge" is per account, and each table keeps `tenant_id` as nullable context that no lookup uses.

## 9. Identity linking

An account is locked and updated by its own global key. The Party it is linked to is still tenant-scoped, and the
caller's tenant is checked against the account's origin tenant explicitly instead of being assumed to be it.

```text
IDENTITY_LINK_ACCOUNT_LOOKUP_GLOBAL=YES
```

## 10. Schema

```text
MIGRATIONS=V59 global account challenge references
           V60 global username uniqueness
           V61 user account origin columns
DATA_CHANGED=0
IDS_PRESERVED=YES
```

Each migration runs its precondition before any change and stops with evidence rather than choosing a winner.

## 11. What PKG-2D did not do

No Brain, no gm-ai-workspace, no invitation workflow, no new authentication-token architecture, no HR, expenses,
fleets, fuel-station, SRI or general Studio redesign, and no change to shared DEV.

## 12. Accepted commits

```text
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL

gm-security
d3fa0b470cb117fb5c1620b6860ecc34ad73a50d   (parent 1654f271711e96761ae7d5470dce3d161cb4333b)

Gystigo
d9f3ddecc76d81993168de7536f756c7c4d0a3ac   (parent 0544e2ec9dcf7bc883e8f57c498e7ac5fb23cbeb)
```

The three PKG-2C known test debts were closed before this commit gate, each an obsolete fixture expectation of
the pre-05C_R1/05C_R2 authority model, none a production defect: KNOWN_REPRODUCIBLE_TEST_FAILURES_REMAINING=0.
The Fabric documentation commit, the verified baseline
GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16 and its registration in `Reglas.md`
follow the implementation commits.

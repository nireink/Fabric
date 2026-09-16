# PKG-2D — Complete cross-tenant global account reuse and adoption

```text
TRACK=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
STEP=PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION
PHASE=PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
MODE=IMPLEMENT_AND_VERIFY
OWNER_AUTHORIZATION=YES
SUPERSEDES_PROMPT=steps/PKG-2D/PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_ADOPTION.md (the AUDIT_ONLY_FIRST prompt, accepted)
REQUIRED_BASELINES=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15
BASELINE_REUSE_REQUIRED=YES
FULL_PKG2C_REGRESSION_RERUN=NO
NO_DEFERRED_PKG2D_CLEANUP=YES
```

## 1. Owner correction that opened this step

The PKG-2D audit was accepted. Its proposal to postpone part of the findings into a later package was
rejected: a known architectural problem inside the current scope is fixed now. Every debt the audit
named belongs to this package and must be resolved before PKG-2D closes. The work is sequenced in
internal checkpoints for safety, not split into future Owner projects.

## 2. Accepted audit facts, not to be re-derived

```text
PKG2C_BASELINE_FOUND=YES
PKG2C_BASELINE_REUSE_DECISION=REUSE
FULL_PKG2C_REGRESSION_RERUN=NO
PKG2C_FILES_UNCHANGED=52/52
CURRENT_MIGRATION_HEAD_AT_AUDIT=V58
GLOBAL_ACCOUNT_REUSE_CURRENT_STATE=STRUCTURALLY_READY_NO_WRITER
CROSS_TENANT_MEMBERSHIP_ADOPTION=ABSENT
PARTY_CREATION_SIDE_EFFECTS_FOUND=0
LAZY_EXPLICIT=VALID
```

The thirteen known problems to correct: no adoption writer; the HR dead end; login bound to the origin
tenant; /auth/me not separating global identity from tenant context; profile reading the origin Party;
no tenant dimension in Studio; identity linking keyed to the origin tenant; ambiguous
`user_accounts.tenant_id` and `party_id`; EVC and PRC origin-pair account keys; global username lookup
against tenant-scoped uniqueness; one-account-one-tenant reasoning in registration and adoption;
adoption safety for pending, unverified and disabled accounts; and preserving Platform Admin
tenantless behaviour.

## 3. Closed Owner decisions

```text
OD-A ADOPTED_MEMBERSHIP_INITIAL_STATUS=ACTIVE, PKG2D_INTRODUCES_INVITATION_WORKFLOW=NO
OD-B MULTIPLE_ACTIVE_MEMBERSHIPS_BEHAVIOR=EXPLICIT_TENANT_SELECTION, no chooser session
OD-C MY_PROFILE_MODEL=GLOBAL_IDENTITY_PLUS_CURRENT_TENANT_CONTEXT, CONTEXTUAL_PARTY_MAY_BE_ABSENT=YES
OD-D MEMBERSHIP_ADOPTION_CREATES_PARTY=NO, PARTY_PROJECTION_POLICY=LAZY_EXPLICIT
OD-E user_accounts.tenant_id -> origin_tenant_id, user_accounts.party_id -> origin_party_id
OD-F MVP_USERNAME_MODEL=EMAIL_ALIAS, username uniqueness becomes GLOBAL
```

They are recorded in `Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md`, entry
"2026-09-15 — GYPPORT® Universe / Reglas de reutilización de la cuenta global entre tenants (PKG-2D)".

## 4. Checkpoints

```text
A  gm-security: the adoption writer, existing account + existing tenant -> ACTIVE membership + event
B  schema: origin columns, global username uniqueness, EVC/PRC global account key, identity linking
C  Host: HR, onboarding and registration adopt an existing global account instead of dead-ending
D  auth: sign-in candidate tenants from ACTIVE memberships, explicit tenant selection
E  auth/me and profile: global identity, available tenants, optional contextual Party
F  Studio: tenant selection distinct from organization selection
G  sweep: no origin-tenant or origin-Party misuse remains anywhere
```

Each checkpoint is finished and verified before the next begins, on the current active line, with no
new branch or worktree and no intermediate commit.

## 5. Invariants required at completion

```text
IDENTITY=GLOBAL
BUSINESS_PARTICIPATION=TENANT_CONTEXTUAL
ACCESS=SECURITY
EMPLOYMENT=HR
AUDIT_ACTOR=GLOBAL_ACCOUNT
GLOBAL_USER_ACCOUNT_TENANT_OWNED=NO
USER_TENANT_MEMBERSHIP_IS_ACCESS_SUBJECT=YES
ACTIVE_MEMBERSHIP_REQUIRES_PARTY=NO
MEMBERSHIP_ADOPTION_CREATES_PARTY=NO
PARTY_PROJECTION_POLICY=LAZY_EXPLICIT
LOGIN_CREATES_PARTY=NO
AUTH_ME_CREATES_PARTY=NO
AUTHORIZATION_READ_CREATES_PARTY=NO
CURRENT_TENANT_FROM_ORIGIN_TENANT=NO
CURRENT_PARTY_FROM_ORIGIN_PARTY=NO
GLOBAL_USERNAME_LOOKUP_MATCHES_GLOBAL_UNIQUENESS=YES
EVC_ACCOUNT_REFERENCE_GLOBAL=YES
PRC_ACCOUNT_REFERENCE_GLOBAL=YES
IDENTITY_LINK_ACCOUNT_LOOKUP_GLOBAL=YES
PLATFORM_ADMIN_REQUIRES_CLIENT_MEMBERSHIP=NO
ORIGIN_TENANT_AUTHORIZATION_READERS=0
ORIGIN_PARTY_CONTEXTUAL_READERS=0
KNOWN_DEFERRED_PKG2D_DEBT=0
```

## 6. Scenarios that must pass

A new account in its origin tenant signs in. B an existing global account is adopted into a second
tenant with no duplicate account. C an account with two ACTIVE memberships gets TENANT_SELECTION_REQUIRED.
D selecting the second tenant opens a session whose permissions come from that membership. E a tenant
with a membership and no contextual Party works, and the read creates none. F explicit provisioning
later creates exactly one Party there. G HR grants access to a person who already has an account and
the membership is adopted. H an unowned tenant selection is denied. I a disabled account gains nothing
from a membership. J the Platform Admin tenantless session still works. K email verification and
password recovery work on the global account key with their gates intact. L the global username lookup
matches a global unique constraint. M profile and /auth/me in the second tenant show the same global
identity, that tenant's context, and never the origin Party.

## 7. Boundaries

Migrations are forward-only, focused, preserve every id and row, and follow the existing Flyway head.
Shared DEV is never written or inspected. Disposable databases only. Verification is impact-scoped
under VERIFIED_BASELINE_REUSE, with PARTIAL_INVALIDATION expected; the full historical matrix is run
only if impact evidence proves broad invalidation. Nothing is staged, committed or pushed: the Owner
reviews the complete implementation first.

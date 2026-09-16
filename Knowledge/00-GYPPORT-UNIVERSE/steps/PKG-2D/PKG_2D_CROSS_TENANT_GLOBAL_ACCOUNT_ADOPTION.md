TRACK=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15

PHASE=PKG_2D_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION

MODE=AUDIT_ONLY_FIRST

OWNER_GOAL

Continue the Global Account / Universal MDM foundation after the completed PKG-2C.

Do NOT restart PKG-2A, PKG-2B or PKG-2C.

PKG-2C is an Owner-accepted committed reusable baseline.

Expected baseline:

BASELINE_ID=
GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15

Expected accepted commits:

gm-entities=
e6d3cbcc5e004e8fbd11c78dc1817b5a00e6bffb

gm-security=
1654f271711e96761ae7d5470dce3d161cb4333b

Gystigo=
a3b7bfeb1b52f06110cd08af185b04f3690b4a43

Expected migration head:
V58

==================================================
1. BASELINE REUSE GATE
==================================================

Before any historical regression, read:

Fabric/Knowledge/00-GYPPORT-UNIVERSE/
verification-baselines/
GYPPORT_PKG2C_VERIFIED_BASELINE_2026-09-15.md

Fabric/Knowledge/00-GYPPORT-UNIVERSE/
verification-baselines/
VERIFIED_BASELINE_REUSE.md

Also read the normal mandatory governance and Universal MDM sources.

Then report:

BASELINE_FOUND=
ACCEPTED_COMMITS_PRESENT=
RELEVANT_PKG2C_CONTRACT_DRIFT=
MIGRATION_SEMANTICS_DRIFT=
OWNER_DECISION_DRIFT=

BASELINE_REUSE_DECISION=
REUSE | PARTIAL_INVALIDATION | FULL_INVALIDATION

If REUSE:

FULL_PKG2C_REGRESSION_RERUN=NO

Do not run the PKG-2C 39-entry matrix.

==================================================
2. CANONICAL ARCHITECTURE
==================================================

The following decisions are closed:

MdmParty = global identity / Golden Record

Party = tenant-contextual business participation

Global UserAccount = global authentication account

UserTenantMembership = account-to-tenant access

Employment = HR

Historical Actor = Global UserAccount

Therefore:

IDENTITY=GLOBAL
BUSINESS_PARTICIPATION=TENANT_CONTEXTUAL
ACCESS=SECURITY
EMPLOYMENT=HR
AUDIT_ACTOR=GLOBAL_ACCOUNT

And:

UserTenantMembership != Party

ACTIVE Membership does NOT automatically create Party.

RESOLVED_NON_ORIGIN_PARTY_PROJECTION=
LAZY_EXPLICIT

Reads never provision Party.

No Party creation from:

login
/auth/me
session authentication
authorization
permission resolution
read-only contextual lookup

==================================================
3. PKG-2D OBJECTIVE
==================================================

Audit the remaining paths needed for one global account to participate safely in multiple tenants.

Target conceptual model:

MdmParty #1000
        |
Global UserAccount #50
        |
        +-- Membership Tenant A
        +-- Membership Tenant B
        +-- Membership Tenant C

Tenant A may have contextual Party A.

Tenant B may have ACTIVE Membership and no Party yet.

Tenant C may independently acquire Party C only when a real business relationship requires it.

No code may interpret:

user_accounts.party_id

as the universal cross-tenant Party.

==================================================
4. AUDIT QUESTIONS
==================================================

Determine from current code/schema/tests:

A. Where is account reuse still restricted by tenant assumptions?

B. Which registration/invitation/adoption paths still assume:

one account -> one tenant

C. How is an existing Global UserAccount discovered when the same identity/email appears in another tenant?

D. Which flows should create only:

UserTenantMembership

without creating Party?

E. Which flows legitimately need explicit contextual Party provisioning?

F. Does login/session tenant selection correctly operate from memberships rather than origin Party?

G. Does /auth/me expose global identity separately from contextual participation?

H. Are any APIs still deriving current Party directly from user_accounts.party_id in a cross-tenant context?

I. Are any uniqueness constraints preventing legitimate cross-tenant account reuse?

J. Does any writer accidentally duplicate:

Global UserAccount
MdmParty
Person
Party

when adopting an existing identity into another tenant?

K. What behavior exists for:

RESOLVED existing identity
PENDING identity
unverified account
Platform Admin
tenantless platform session

L. What Studio/UI/API behavior would need adoption for tenant selection or reused accounts?

==================================================
5. SCOPE OWNERSHIP
==================================================

gm-entities owns:

MdmParty
Person identity
Organization identity
identifiers
Universal Intake
matching/resolution
contextual Party
explicit contextual Party provisioning

gm-security owns:

Global UserAccount
authentication
UserTenantMembership
roles
permissions
tenant access/session security

Do not move responsibilities between these modules without an explicit new Owner decision.

PKG-2D must not become:

HR redesign
gm-expenses redesign
gm-fleets redesign
SRI redesign
OrganizationAccess redesign beyond required adoption
general Studio redesign

==================================================
6. EVC / PRC
==================================================

Existing Owner decision:

EVC_PRC_ACCOUNT_FK_RESHAPE=DEFER

Do not pull that reshape into PKG-2D unless current evidence proves PKG-2D is impossible without it.

If such a conflict exists:

STOP_FOR_OWNER_REVIEW.

==================================================
7. OUTPUT
==================================================

This first PKG-2D STEP is AUDIT ONLY.

Do not implement.

Do not create migration yet.

Do not modify production code.

Do not modify Studio.

Do not run broad historical regression.

Return:

STATUS=STOPPED_PENDING_OWNER_REVIEW

PKG2C_BASELINE_FOUND=
PKG2C_BASELINE_REUSE_DECISION=
FULL_PKG2C_REGRESSION_RERUN=

CURRENT_HEADS=
CURRENT_MIGRATION_HEAD=

GLOBAL_ACCOUNT_REUSE_CURRENT_STATE=

CROSS_TENANT_ACCOUNT_DISCOVERY=

CROSS_TENANT_MEMBERSHIP_ADOPTION=

ORIGIN_TENANT_ASSUMPTIONS_FOUND=

USER_ACCOUNTS_PARTY_ID_REMAINING_READERS=

PARTY_CREATION_SIDE_EFFECTS_FOUND=

DUPLICATE_GLOBAL_ACCOUNT_RISK=

DUPLICATE_MDM_PARTY_RISK=

DUPLICATE_CONTEXTUAL_PARTY_RISK=

LOGIN_SESSION_ADOPTION_GAPS=

AUTH_ME_ADOPTION_GAPS=

STUDIO_ADOPTION_GAPS=

SCHEMA_CHANGES_REQUIRED=
MIGRATION_REQUIRED=

EVC_PRC_BLOCKER=YES|NO

PROPOSED_PKG2D_SUBPACKAGES=

NEW_OWNER_DECISIONS_REQUIRED=

RECOMMENDED_NEXT_STEP=

FILES_CHANGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

STOP_FOR_OWNER_REVIEW=YES
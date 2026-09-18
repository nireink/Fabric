# GYPPORT ORGANIZATION CONTROL FOUNDATION

PROJECT=GYPPORT
DOCUMENT_TYPE=CANONICAL_SECURITY_KNOWLEDGE
STATUS=OWNER_BASELINE
SCOPE=BUSINESS_PLATFORM_ORGANIZATION_CONTROL
CANONICAL_PATH=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\Security\GYPPORT_ORGANIZATION_CONTROL_FOUNDATION.md

---

## 1. Purpose

This document defines the canonical GYPPORT rules for Organization identity,
creation, traceability, control, corporate-authority verification, and first
Organization OWNER activation.

It must be read together with:

- `GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE.md`
- `GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES.md`
- `GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY.md`

---

## 2. Business Platform model

```text
BUSINESS_PLATFORM_PERSON_FIRST=YES
CAPABILITY_FIRST=YES

ORGANIZATION_REQUIRED_FOR_PLATFORM_USE=NO
RUC_REQUIRED_FOR_PLATFORM_USE=NO

MODULES_ARE_NOT_CLASSIFIED_AS_PERSONAL_OR_ORGANIZATIONAL=YES
CAPABILITIES_HAVE_CONTEXT_REQUIREMENTS=YES
```

GYPPORT Business Platform can be used by:

1. a Person;
2. a Person with RUC / professional or commercial activity;
3. an Organization / company.

An Organization must not be fabricated merely because a Person uses
professional, commercial, fiscal, fleet, fuel, expense, sales, purchase,
reservation, or other Business Platform capabilities.

---

## 3. Canonical Party identity

```text
Party
├── Person
└── Organization
```

`gm-entities` is the canonical Party / MDM identity source.

```text
PERSON != EMPLOYEE
PERSON != USER_ACCOUNT
PERSON != SECURITY_ROLE

EMPLOYEE != USER_ACCOUNT

PARTY_BUSINESS_CONTEXT != SECURITY_ROLE
```

Customer, Supplier, Driver, Operator, Representative, Shareholder, Contact and
similar concepts must not create parallel mutable identity masters.

Examples:

```text
Sales / Customer
→ canonical Party

Purchases / Supplier
→ canonical Party

Internal Operator
→ Person + Employee + UserAccount when login is needed + Security Role

Internal Driver
→ Person + Employee when applicable
```

---

## 4. Ecuador taxpayer classification

RUC does not imply Organization.

```text
RUC_DOES_NOT_IMPLY_ORGANIZATION=YES
PERSON_WITH_RUC_REMAINS_PERSON=YES
```

When authoritative Ecuador SRI information is available:

```text
Tipo contribuyente = PERSONA NATURAL
→ PartyType = PERSON

Tipo contribuyente = SOCIEDAD
→ PartyType = ORGANIZATION
```

Legal-name suffix is not the primary classification authority.

Do not classify solely from:

- S.A.S.
- C.L.
- Cía. Ltda.
- S.A.
- other textual endings.

For a `SOCIEDAD`, official evidence may include:

- RUC;
- Razón social;
- Tipo contribuyente;
- taxpayer status;
- legal representative;
- representative identification;
- establishments;
- other fiscal attributes.

---

## 5. Authority layers

```text
PLATFORM
!=
TENANT
!=
ORGANIZATION
!=
HUMAN_RESOURCES
!=
USER_ACCOUNT
```

### Platform

`GYPPORT_SAAS_ADMIN` is Platform-scoped.

A Platform Admin does not automatically become an Organization OWNER, ADMIN or
Employee.

### Tenant

Tenant is the SaaS technical/data-isolation boundary.

`tenant_role_scopes` is canonical and may legitimately express intentionally
Tenant-wide RBAC authority.

### Organization

Organization is the business/company authority boundary.

`organization_role_scopes` is canonical for Organization-scoped security
authority.

### Organization access

```text
ORGANIZATION_ACCESS_IS_AUTHORITY=NO
```

`organization_access` represents visibility/context/membership and must not by
itself grant Organization administration or ownership.

---

## 6. TENANT_USER

`TENANT_USER` is a technical system role representing baseline authenticated
Business Platform capabilities inside a Tenant.

```text
TENANT_USER_IS_SYSTEM=YES
TENANT_USER_IS_GENERAL_BUSINESS_PLATFORM_BASE_ROLE=YES

TENANT_USER_IS_PLATFORM_ROLE=NO
TENANT_USER_IS_ORGANIZATION_ROLE=NO
TENANT_USER_IS_EMPLOYEE_ROLE=NO
TENANT_USER_IS_MEMBERSHIP_CONCEPT=NO

TENANT_USER_AUTOMATIC_ORGANIZATION_AUTHORITY=NO
```

Valid general Business Platform permissions must not be removed merely because
a module sounds business-oriented.

However, `TENANT_USER` must never acquire permissions whose actual semantics
constitute Platform control or Organization security/administrative control.

This invariant must be enforced in code/tests using the existing permission
model whenever possible.

---

## 7. Organization creation and creator traceability

Creating/preparing an Organization is not proof of legal control.

```text
ORGANIZATION_CREATOR_IS_AUTOMATIC_OWNER=NO
CREATED_BY_USER_ID_IS_AUTHORITY=NO
```

`organizations.created_by_user_id` means only:

> the authenticated UserAccount that created/prepared the Organization record.

It must not grant:

- OWNER;
- ADMIN;
- legal representative status;
- verified corporate authority;
- Organization permission.

Historical rows whose creator cannot be established authoritatively must remain
NULL.

```text
HISTORICAL_UNKNOWN_CREATOR=KEEP_NULL
DO_NOT_GUESS_BACKFILL=YES
```

---

## 8. Corporate relationships vs Security roles

A corporate/business relationship is not itself a Security role.

Examples:

```text
LEGAL_REPRESENTATIVE
SHAREHOLDER
AUTHORIZED_DELEGATE
```

These describe a Party relationship.

Security roles such as:

```text
OWNER
ADMIN
OPERADOR
SUPERVISOR
CONTADOR
```

describe what a UserAccount is authorized to do.

```text
LEGAL_REPRESENTATIVE != SECURITY_OWNER
```

The correct conceptual chain is:

```text
evidence
→ verified Party relationship / authority
→ explicit Organization control approval
→ Organization-scoped Security OWNER grant
```

---

## 9. Self-attestation and password confirmation

```text
SELF_ATTESTED_CAN_GRANT_OWNER=NO
PASSWORD_CONFIRMATION_CAN_GRANT_OWNER=NO
```

A self-attested claim is a declaration, not verified corporate authority.

Password confirmation proves control of the current UserAccount only. It does
not prove legal authority over an Organization.

`PENDING` / `SELF_ATTESTED` must never silently become OWNER.

---

## 10. First Organization OWNER activation

The first legitimate Organization OWNER must be activated through an explicit,
auditable Organization-control verification process.

No tenant-wide OWNER may be created as the final model.

```text
TENANT_WIDE_OWNER_AS_FINAL_MODEL=NO
FIRST_OWNER_SCOPE=ORGANIZATION
```

When authoritative automatic registry verification does not exist, GYPPORT may
use a controlled manual Platform Admin review for the MVP, provided the Owner
has explicitly approved the workflow.

The review must verify, at minimum where applicable:

- target Organization identity;
- Organization RUC;
- authoritative taxpayer type;
- taxpayer active status;
- legal representative;
- legal representative identification;
- canonical claimant Person identity;
- match between claimant identity and the authority evidence.

Approval must not rely solely on:

- Organization creation;
- `organization_access`;
- password confirmation;
- self-attestation.

---

## 11. Manual Platform Admin verification provenance

When a Platform Admin performs a cross-tenant Organization-control review,
reviewer/grantor provenance must be relational and auditable.

Do not accept text-only reviewer provenance as the completed design when a
proper relational reference can be modeled safely.

Canonical target:

```text
party_relationship_verifications
→ verified_by_platform_admin_id
→ platform_admins

organization_role_scopes
→ granted_by_platform_admin_id
→ platform_admins
```

Existing same-Tenant provenance fields remain valid for same-Tenant actors.

For a Platform Admin review:

```text
verified_by_platform_admin_id = reviewer
verified_by_user_id = NULL when cross-tenant FK rules require it

granted_by_platform_admin_id = grantor
created_by_user_id = NULL when cross-tenant FK rules require it
```

The schema must preserve who actually performed the Platform action without
pretending the Platform Admin belonged to the customer Tenant.

---

## 12. Verification evidence

Existing verification/evidence structures should be reused when sufficient.

A manual approval must preserve:

- verification status;
- verification method;
- observed/verified timestamps;
- authoritative source;
- external/source reference where available;
- evidence metadata/content according to the existing evidence model;
- evidence hash where supported;
- reviewer provenance.

Possible statuses include the existing canonical catalog values such as:

```text
PENDING
VERIFIED
REJECTED
EXPIRED
```

Do not fabricate `VERIFIED`.

Rejection or identity mismatch must never grant OWNER.

---

## 13. First-owner grant

After legitimate verification/approval:

```text
verified authority
→ grantOrganizationScopedOwnerRole(...)
→ Organization scope only
```

Required:

```text
NEW_TENANT_WIDE_OWNER_CREATED=NO
GLOBAL_ADMIN_AUTOMATIC_OWNER=NO
ORGANIZATION_ACCESS_ALONE_GRANTS_OWNER=NO
CREATED_BY_USER_ID_ALONE_GRANTS_OWNER=NO
```

The grant must be:

- target-Organization exact;
- tenant-isolated;
- auditable;
- safe on retries/idempotent;
- compatible with last-effective-admin protections.

If an existing bootstrap guard makes a valid first OWNER impossible in a
legitimate preexisting state, stop and obtain an Owner decision rather than
silently bypassing it.

---

## 14. Platform Admin write boundary

Platform Admin is normally Platform-scoped and must not silently operate as a
customer Organization actor.

A narrowly authorized Platform write is allowed only for explicit platform
administration/support functions approved by the Owner.

First Organization control verification/activation is such an approved
Platform-controlled function when executed through the dedicated, audited
workflow.

This does NOT make Platform Admin an Organization OWNER.

---

## 15. Completion policy

Known Organization-control correctness/security/traceability findings must not
be left as vague future work.

```text
KNOWN_IN_SCOPE_PROBLEM
→ RESOLVE_NOW

AMBIGUOUS_NEW_DECISION
→ STOP
→ OWNER DECISION
→ RESUME SAME STEP
→ COMPLETE
```

Do not use:

```text
"not necessary today"
"later"
"future improvement"
"follow-up someday"
```

as the default disposition for a known in-scope problem.

---

## 16. Canonical invariants summary

```text
BUSINESS_PLATFORM_PERSON_FIRST=YES
ORGANIZATION_REQUIRED_FOR_PLATFORM_USE=NO

PARTY_IS_CANONICAL_IDENTITY_SOURCE=YES

RUC_DOES_NOT_IMPLY_ORGANIZATION=YES
SRI_PERSONA_NATURAL_MAPS_TO=PERSON
SRI_SOCIEDAD_MAPS_TO=ORGANIZATION

GLOBAL_ADMIN_IS_PLATFORM_SCOPED=YES

TENANT_ROLE_SCOPES_IS_CANONICAL=YES
ORGANIZATION_ROLE_SCOPES_IS_CANONICAL=YES

ORGANIZATION_ACCESS_IS_AUTHORITY=NO

TENANT_USER_AUTOMATIC_ORGANIZATION_AUTHORITY=NO

ORGANIZATION_CREATOR_IS_AUTOMATIC_OWNER=NO
CREATED_BY_USER_ID_IS_AUTHORITY=NO

SELF_ATTESTED_CAN_GRANT_OWNER=NO
PASSWORD_CONFIRMATION_CAN_GRANT_OWNER=NO

LEGAL_REPRESENTATIVE != SECURITY_OWNER

FIRST_OWNER_REQUIRES_VERIFIED_OR_APPROVED_AUTHORITY=YES
FIRST_OWNER_SCOPE=ORGANIZATION
TENANT_WIDE_OWNER_AS_FINAL_MODEL=NO

PLATFORM_ADMIN_REVIEWER_PROVENANCE_MUST_BE_AUDITABLE=YES
TEXT_ONLY_PLATFORM_REVIEWER_PROVENANCE_AS_FINAL_DESIGN=NO

DO_NOT_GUESS_HISTORICAL_CREATOR=YES
```

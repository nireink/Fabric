# GYPPORT® Business Platform Universal
## Canonical Architecture, Database Contracts, Domain Ownership and Development Rules

**Date:** 2026-09-12  
**Document:** `GYPPORT_BUSINESS_PLATFORM_UNIVERSAL_CANONICAL_ARCHITECTURE_2026-09-12.md`  
**Scope:** GYPPORT Universe, Universal MDM, Party, UserAccount, Tenant Context, Employment, Organization, Tax/Fiscal Context, Contact/Address History, and rules that every future module must follow.  
**Purpose:** Prevent architectural drift, duplicate masters, destructive data modeling, and module-specific reinvention of identity, access, relationships, contacts, or business context.

---

# 1. Why this document exists

GYPPORT has accumulated architecture decisions across:

- historical conversations;
- historical uploaded documents;
- database dumps and schema;
- canonical baselines;
- ADRs;
- closed and Owner-accepted STEPs;
- current repository implementation;
- recent Owner decisions.

The important lesson is:

> GYPPORT architecture must not be projected only from the most recent conversation.

Historical documents already contained foundational concepts that later became physical schema and current architecture.

Therefore, future work must contrast all available evidence before proposing a new model.

This document consolidates the current canonical interpretation of that history.

---

# 2. Canonical evidence hierarchy

For any future architectural decision, use this order:

```text
1. MOST RECENT OWNER DECISION
        ↓
2. CANONICAL DOCUMENTS / ADRs / OWNER-ACCEPTED STEPs
        ↓
3. HISTORICAL DOCUMENTS AND CONVERSATIONS
        ↓
4. CURRENT REPOSITORY AND DATABASE
        ↓
5. NEW PROPOSAL
```

Important interpretation:

```text
HISTORY
= explains WHY

CURRENT REPOSITORY / DATABASE
= proves HOW IT WORKS NOW

OWNER DECISION
= defines WHERE THE PLATFORM MUST EVOLVE
```

If these disagree, do NOT silently choose one.

Report explicitly:

```text
HISTORICAL_INTENT
CURRENT_IMPLEMENTATION
CURRENT_CANONICAL_DECISION
CONFLICT
RECOMMENDED_RECONCILIATION
```

before implementation.

---

# 3. The foundational GYPPORT equation

The most important architectural distinction is:

```text
IDENTITY = GLOBAL
BUSINESS RELATIONSHIP / OPERATIONAL CONTEXT = TENANT
```

Equivalent formulation:

```text
WHO IT IS
≠
HOW IT PARTICIPATES
```

This distinction controls Universal MDM, Party, HR, Security, CRM, Sales, Purchases, Accounting, Tax, Fleet, Expenses and every future module.

---

# 4. GYPPORT Business Platform Universal

GYPPORT is not merely a collection of ERP modules.

It is a shared business universe over which all operational modules operate.

Canonical high-level model:

```text
                    GYPPORT UNIVERSE
                          │
                          ▼
                    UNIVERSAL MDM
                          │
          ┌───────────────┴────────────────┐
          │                                │
       PERSON                         ORGANIZATION
          │                                │
          ├── Identifiers                  ├── Identifiers
          ├── Contacts                     ├── Contacts
          ├── Addresses                    ├── Addresses
          ├── Tax profiles                 ├── Tax profiles
          └── Provenance                   └── Provenance
                          │
                          ▼
                    TENANT CONTEXT
                          │
                         Party
                          │
       ┌──────────────────┼────────────────────┐
       │                  │                    │
   Customer           Supplier            Employee
       │                  │                    │
      CRM             Purchasing              HR
       │                  │                    │
      Sales           AP / Inventory       Employment
```

Parallel access model:

```text
MdmParty PERSON
      │
      └── GYPPORT UserAccount
             │
             ├── Tenant Membership A
             │      ├── Party A
             │      └── Roles A
             │
             ├── Tenant Membership B
             │      ├── Party B
             │      └── Roles B
             │
             └── Tenant Membership C
                    ├── Party C
                    └── Roles C
```

The membership model is the target direction for the Global Account foundation; it is not yet fully implemented.

---

# 5. Universal architectural classification rule

Before approving any new entity, table, aggregate, service, endpoint or module concept, ask:

```text
¿ESTO REPRESENTA QUIÉN ES?
→ MDM / gm-entities

¿REPRESENTA CÓMO PARTICIPA EN ESTE TENANT?
→ Party / relación específica

¿REPRESENTA UNA RELACIÓN LABORAL?
→ gm-human-resources / Employment

¿REPRESENTA ACCESO?
→ gm-security

¿REPRESENTA ESTRUCTURA EMPRESARIAL?
→ gm-organizations

¿REPRESENTA CONTEXTO FISCAL?
→ TaxSubject / fiscal domain

¿REPRESENTA UNA TRANSACCIÓN?
→ módulo operacional correspondiente
```

This is a mandatory design gate.

Never introduce a new master entity before answering it.

---

# 6. Reuse-before-create rule

Before creating a Person or Organization anywhere:

```text
¿YA EXISTE ESTA PERSONA / ORGANIZACIÓN
EN EL UNIVERSO GYPPORT?

SI
→ REFERENCIAR / REUTILIZAR

NO
→ INTAKE / RESOLVER / VERIFICAR

NUNCA
→ CREAR OTRO MAESTRO POR COMODIDAD
```

This rule is mandatory for all modules.

---

# 7. MdmParty

`MdmParty` is the global Golden Record.

It answers:

> Who is this real Person or Organization in the GYPPORT universe?

Canonical types:

```text
PERSON
ORGANIZATION
```

A single real-world subject should map to one global `MdmParty`.

---

# 8. What MdmParty is NOT

`MdmParty` is not:

- Employee;
- Customer;
- Supplier;
- UserAccount;
- Security Role;
- Organization Membership;
- TaxSubject;
- Tenant;
- Branch;
- Establishment;
- transaction participant type.

Those are relationships, capabilities or operational contexts around the identity.

---

# 9. Party

`Party` answers:

> How does this global identity participate inside a specific tenant?

Example:

```text
MdmParty #1000
├── Party #10 → Tenant A
├── Party #42 → Tenant B
└── Party #91 → Tenant C
```

One `MdmParty` may have multiple tenant-scoped Party projections.

---

# 10. Party database contract

Mandatory invariant:

```text
parties.mdm_party_id IS NOT NULL
```

Never create:

- a provisional Party;
- a Party without MDM;
- a fake Party just to satisfy authorization;
- a duplicate Party for the same `(tenant_id, mdm_party_id)`.

Canonical uniqueness:

```text
(tenant_id, mdm_party_id)
→ at most one Party
```

If identity is unresolved, keep it in Intake / Claim / pending account state.

Do not weaken Party to accommodate incomplete identity.

---

# 11. One Person, many roles

A single Person may participate differently across companies.

```text
MdmParty PERSON #1000

Tenant A
→ Customer

Tenant B
→ Employee

Tenant C
→ Supplier

Tenant D
→ Shareholder

Tenant E
→ Organization Owner
```

These are not five Persons. They are five contexts for one identity.

---

# 12. Roles are contextual

Canonical rule:

```text
SAME PERSON
!=
SAME ROLE IN EVERY COMPANY
```

Example:

```text
Empresa A
→ Employee

Empresa B
→ Accountant

Empresa C
→ Organization Owner

Personal context
→ no company role
```

Roles and permissions belong to a tenant/organization/access context.

Do not attach business roles globally to `MdmParty`.

---

# 13. Person != Employee != UserAccount != Role

Mandatory distinction:

```text
Person
= identity

Employee
= employment/business relationship

UserAccount
= authentication/access identity

Role
= authorization inside a context
```

Never collapse these concepts.

---

# 14. gm-entities canonical ownership

`gm-entities` owns global identity.

Responsibilities include:

- `MdmParty`;
- Person;
- Organization identity;
- canonical identifiers;
- MDM resolution;
- Universal Intake;
- identity provenance;
- global contact history;
- global address history;
- canonical identity enrichment.

Other modules reference identity. They do not create competing identity masters.

---

# 15. Universal MDM Intake

Unresolved identity must enter through Universal Intake.

```text
SOURCE
→ INTAKE / STAGING
→ NORMALIZATION
→ EXACT MDM MATCH
→ AUTHORITATIVE VERIFICATION WHEN NEEDED
→ MDM RESOLUTION
→ PARTY TENANT PROJECTION
```

Potential sources include registration, HR, CRM, Sales, Purchases, SRI, Registro Civil and future approved external integrations.

---

# 16. Universal MDM search rule

Priority:

```text
1. Search GYPPORT Universal MDM
2. Exact canonical match → reuse
3. If absent → authoritative verification when available
4. Verified → create/update MDM
5. Unavailable/unverified → PENDING_VERIFICATION
```

Do not create canonical identity merely because the format looks valid.

---

# 17. Structural validation != identity verification

Freeze:

```text
STRUCTURAL_VALIDATION
!=
IDENTITY_VERIFICATION
```

Checksums, modulo algorithms, province inference or similar local heuristics are not identity authority.

---

# 18. External verification and internal truth

```text
GOVERNMENT / AUTHORITATIVE SOURCE
= external verification authority

GYPPORT UNIVERSAL MDM
= internal canonical source of truth
  after identity is established / verified
```

If an authoritative source is unavailable:

```text
PENDING_VERIFICATION
```

Do not fabricate truth.

---

# 19. Names, email, phone and address are not deterministic identity keys

Freeze:

```text
NAME_AUTOMATCH=NO
EMAIL_AUTOMATCH=NO
PHONE_AUTOMATCH=NO
ADDRESS_AUTOMATCH=NO
```

They may be evidence, communication channels, candidate hints and review data.

They do not automatically merge MdmParties.

---

# 20. Historical contact/address model

The GYPPORT design already established that changing addresses or contacts must not destroy previous data.

Conceptual example:

```text
Quito · Dirección A
2024 → 2026
is_current = false

Quito · Dirección B
2026 →
is_current = true
```

Address A remains.

The same principle applies to emails and phone numbers.

---

# 21. `mdm_party_contacts`

The database already contains a global MDM contact structure.

Canonical relevant semantics include:

```text
mdm_party_contacts
├── mdm_party_id
├── contact_type_id
├── contact_value
├── is_primary
├── is_current
├── is_verified
├── valid_from
├── valid_to
├── usage_count
├── updated_by_tenant_id
└── created_at
```

The schema can hold multiple contact rows for one `MdmParty`.

The domain/application code still needs to mature to fully exploit that capability.

---

# 22. `mdm_party_addresses`

The database already contains historical MDM addresses.

```text
mdm_party_addresses
├── mdm_party_id
├── geo_location_id
├── address_type_id
├── address_line_1
├── address_line_2
├── postal_code
├── is_primary
├── is_current
├── valid_from
├── valid_to
├── usage_count
├── updated_by_tenant_id
└── created_at
```

The schema permits multiple addresses per subject.

---

# 23. ContactPoint canonical target

```text
MdmParty
→ ContactPoints[]
   ├── type
   ├── value
   ├── purpose
   ├── verified
   ├── source / provenance
   ├── valid_from
   ├── valid_to
   ├── is_current
   └── is_primary
```

Possible purposes may include PERSONAL, WORK, HOME, MOBILE, ALTERNATE, CORRESPONDENCE, REGISTRATION and OTHER, subject to a controlled domain catalog.

---

# 24. Address canonical target

```text
MdmParty
→ Addresses[]
   ├── type / purpose
   ├── geo
   ├── address
   ├── source / provenance
   ├── valid_from
   ├── valid_to
   ├── is_current
   └── is_primary
```

Do not replace history when a new address becomes current.

---

# 25. Primary does not mean only

```text
is_primary = true
```

means preferred/default.

It does not mean only one value may exist historically or even currently where the domain permits multiple current channels.

---

# 26. Current does not mean delete previous

```text
is_current = false
```

means no longer current.

It does not mean useless or deletable.

---

# 27. Contact ownership split

Long-term ownership:

```text
GLOBAL MDM
→ reusable personal/global contact history

TENANT / PARTY
→ tenant-private overrides only when semantically necessary

EMPLOYMENT
→ work email / work phone / work context

USERACCOUNT
→ authentication / recovery identifier

BRANCH
→ branch contact/address

SRI ESTABLISHMENT
→ fiscal establishment address
```

Do not mix these meanings.

---

# 28. UserAccount email

Canonical role:

```text
UserAccount.email
= PRIMARY AUTHENTICATION / RECOVERY IDENTIFIER
```

It is not automatically the Person's canonical email master.

Freeze:

```text
LOGIN_EMAIL_IS_PERSON_CONTACT_MASTER=NO
```

---

# 29. Legacy login-email copies in MDM

Historical code copied registration login email into MDM contacts.

Current rule:

- preserve existing historical data;
- do not delete it in unrelated STEPs;
- do not automatically copy future login emails into MDM;
- later reconcile provenance/purpose in a dedicated contact-history STEP.

---

# 30. Work contacts

Example:

```text
MdmParty Sofia Salinas

Employment A
→ sofia@company-a.com
→ work phone A

Employment B
→ sofia@company-b.com
→ work phone B
```

These are contextual work contacts and do not create another Person.

---

# 31. gm-human-resources canonical ownership

`gm-human-resources` owns employment relationships:

- Employee;
- Employment;
- Position;
- assignment;
- supervisor;
- lifecycle;
- future work contacts.

It references canonical Person/Party.

It does not create a competing Person master.

---

# 32. Position != Security Role

```text
Position
= organizational / employment function

Security Role
= permission bundle
```

Do not collapse them.

---

# 33. gm-security canonical ownership

`gm-security` owns:

- UserAccount;
- authentication;
- email verification;
- password recovery;
- roles;
- permissions;
- scopes;
- authorization;
- UserAccount identity linkage.

It does not own Person identity.

---

# 34. Email verification != identity verification

```text
EMAIL_VERIFICATION
!=
IDENTITY_VERIFICATION
```

Email OTP proves control of the account/email.

It does not prove ownership of an `MdmParty` identity.

---

# 35. Pending UserAccount model

Canonical target:

```text
PENDING
user_accounts.party_id = NULL
user_accounts.mdm_party_id = NULL
```

Resolved:

```text
RESOLVED
user_accounts.party_id != NULL
user_accounts.mdm_party_id != NULL
```

No half-linked state.

---

# 36. IdentityClaim

IdentityClaim answers:

> Does this account/user prove ownership/control of this identity?

Universal Intake answers:

> Which identity corresponds to this identifier/candidate?

Do not collapse the responsibilities.

---

# 37. Existing account linking flow

```text
UserAccount exists
→ user enters NUI/RUC
→ exact MDM match
→ IDENTITY_FOUND
→ do not auto-link
→ IdentityClaim
→ account-control confirmation
→ identity ownership verification
→ APPROVED
→ link canonical MdmParty / Party
```

---

# 38. Existing Person gets GYPPORT access

Starting point:

```text
MdmParty / Party exists
UserAccount may or may not exist
```

Cases:

```text
No account exists anywhere
→ invite/create first account

Email belongs to same MdmParty account
→ reuse account / continue claim

Email belongs to different MdmParty
→ conflict

Same MdmParty already has account in another tenant
→ do not create second credential
→ future tenant membership required
```

---

# 39. Create-account flow when identity and email already exist

If registration detects:

```text
existing MdmParty
+
existing UserAccount email
```

Do not create another account.

Canonical continuation:

```text
authenticate / OTP existing account
→ resume same IdentityClaim
→ verify identity ownership
→ link when approved
```

---

# 40. No duplicate credentials for the same MdmParty

Interim safety rule:

```text
same MdmParty
already has active UserAccount
+
another tenant attempts another account
=
NO SECOND USERACCOUNT
```

Different email does not create a different identity.

Until Global Account / Tenant Membership exists, use a bounded outcome such as:

```text
GLOBAL_ACCOUNT_MEMBERSHIP_REQUIRED
```

---

# 41. Future Global Account model

```text
MdmParty
        ↓
Global UserAccount
        ↓
Tenant Memberships
        ├── Tenant A
        │    ├── Party A
        │    ├── Roles A
        │    └── OrganizationAccess A
        │
        ├── Tenant B
        │    ├── Party B
        │    ├── Roles B
        │    └── OrganizationAccess B
        │
        └── Tenant C
             ├── Party C
             ├── Roles C
             └── OrganizationAccess C
```

Authentication target:

```text
authenticate once
→ choose active tenant/context
→ choose organization when applicable
→ resolve authorization for that context
```

---

# 42. Profile context model

Future experience:

```text
Cuenta GYPPORT

Personal

Mis organizaciones
├── Empresa A · Employee
├── Empresa B · Accountant
├── Empresa C · Owner
└── Mi negocio · Admin
```

A future visibility preference may hide contexts from a profile view, but must never remove memberships or permissions.

---

# 43. gm-organizations canonical ownership

`gm-organizations` owns internal tenant/company structure:

- organizations;
- branches;
- departments;
- cost centers;
- organization settings;
- internal structure.

Do not confuse:

```text
internal Branch
≠
SRI Establishment
```

---

# 44. TaxSubject / fiscal ownership

`TaxSubject` answers:

> In what fiscal/tax context does this identity operate?

Canonical chain:

```text
MdmParty
→ Party
→ TaxSubject
→ SRI Establishment
→ Emission Point
→ Document Sequence
```

A natural Person with RUC remains `MdmParty PERSON`.

Do not create an Organization merely because a natural person has a RUC.

---

# 45. Global vs contextual data

Global / Universal:

```text
MdmParty
Identifiers
Canonical identity
Identity provenance
Global reusable contact history
Global address history
Official reusable tax identity facts
```

Tenant / relationship context:

```text
Customer relationship
Supplier relationship
Credit terms
Commercial notes
Price lists
Sales history
Purchasing history
Employment
Work contacts
Organization membership
Roles / permissions
```

---

# 46. Module contract — gm-sales

`gm-sales` sells to a Party/Customer relationship.

It must not create another customer identity master.

If identity is unresolved, use Universal Intake.

---

# 47. Module contract — gm-purchases

`gm-purchases` buys from a Party/Supplier relationship.

It must not create another supplier identity master.

Supplier-specific commercial conditions belong to the tenant relationship.

---

# 48. Module contract — CRM

CRM owns interactions, opportunities, commercial notes and relationship history.

CRM references Party/Customer.

CRM must not become another Person/Organization master.

---

# 49. Module contract — Accounting

Accounting should reference canonical counterparties derived from Party, Organization and TaxSubject as semantically appropriate.

Accounting must not invent another party identity master.

---

# 50. Module contract — gm-expenses

Expenses owns expense operations.

Responsible/payee/supplier references should converge on canonical identity where appropriate.

Immutable snapshots may be stored as evidence, but are not competing masters.

---

# 51. Module contract — gm-fleets

Owners, drivers, responsible persons and suppliers should reference canonical Party/Person when appropriate.

Fleet must not duplicate the Person master.

---

# 52. Module contract — gm-fuel-stations

`FuelExternalParty` is valid while the party is genuinely external/unresolved.

If the subject later becomes canonical GYPPORT identity, reconciliation should be possible.

Do not prematurely force every temporary external reference into MDM.

---

# 53. Module contract — SRI / e-documents

Emitters and recipients should be resolved against canonical identity.

E-document processing must not create parallel Person/Organization masters.

---

# 54. Snapshot vs Master rule

Operational modules may preserve immutable snapshots.

Example:

```text
Invoice recipient snapshot
```

may retain name, identifier, address and fiscal details as evidence.

That snapshot is not a competing master.

---

# 55. Cross-module FK policy

```text
MODULE_TO_CORE_FK_POLICY
= ALLOWED_WHEN_SEMANTICALLY_STABLE
```

Requirements:

- tenant-safe;
- no cross-domain write ownership violation;
- no duplicate master;
- compatible collation;
- no destructive cross-owner cascade.

---

# 56. Tenant safety contract

Every tenant-scoped relationship must prove tenant consistency.

Cross-tenant access must be explicit architecture, never accidental FK bypass.

---

# 57. Global vs tenant decision rule

Ask:

```text
Would this fact remain true if the Person participated in another company?
```

If yes, it is likely global.

Ask:

```text
Does this fact exist because of a specific company relationship?
```

If yes, it is likely tenant/contextual.

---

# 58. Master vs relationship rule

Never put relationship data into the master merely because it is convenient.

```text
MdmParty != Customer
MdmParty != Supplier
MdmParty != Employee
MdmParty != Owner
```

---

# 59. Master vs transaction rule

A transaction may reference master data and preserve immutable snapshots.

It must not redefine canonical identity.

---

# 60. Provenance contract

For important MDM facts, GYPPORT should be able to answer:

```text
Where did this value come from?
Who/what supplied it?
When?
Was it verified?
By which source?
When was it valid?
What replaced it?
```

Provenance is part of trustworthy master data.

---

# 61. Schema migration contract

Every migration affecting core identity or access must:

- declare invariants;
- stop on contradictory data;
- preserve IDs;
- preserve history;
- prove tenant safety;
- prove no duplicates;
- run against disposable DB first;
- not touch shared DEV without explicit Owner authorization.

---

# 62. Shared DEV contract

```text
tests → disposable MySQL
shared DEV → manual runtime only
```

No migration, cleanup or test mutation on shared DEV without explicit Owner authorization.

---

# 63. Development evidence rule

A passing test is not enough if it encodes the wrong architecture.

Classify failures as:

```text
REAL REGRESSION
PRE-EXISTING DEBT
LEGACY TEST ASSUMPTION
EXPECTED CONTRACT CHANGE
```

Do not weaken architecture to preserve stale assertions.

---

# 64. Existing != wrong

```text
EXISTING != WRONG
```

Do not replace a model simply because a newer design appears cleaner.

First determine original purpose, current use, canonical owner, compatibility and migration impact.

---

# 65. Audit before rebuild

```text
AUDIT BEFORE REBUILD
```

Especially for identity, Party, UserAccount, contacts, addresses, tenant access, tax, HR, RBAC and canonical catalogs.

---

# 66. Future module admission checklist

Before authorizing a new module, answer:

```text
1. What is the domain owner?
2. Does it create identity?
3. Does it need Party?
4. Does it need MdmParty?
5. Is the data global or tenant-scoped?
6. Is it master, relationship, configuration or transaction?
7. Does another module already own this master?
8. What immutable snapshots are required?
9. What historical data must be preserved?
10. Which FK relationships are semantically stable?
11. What tenant-safety invariants apply?
12. What happens when identity is unresolved?
13. What happens if the Person already exists?
14. What happens across multiple tenants?
15. Are roles contextual?
```

No implementation before these are answered.

---

# 67. Quick ownership decision tree

```text
NEW CONCEPT
     │
     ├── WHO IS IT?
     │      → gm-entities / MDM
     │
     ├── HOW DOES IT PARTICIPATE HERE?
     │      → Party / tenant relationship
     │
     ├── EMPLOYMENT?
     │      → gm-human-resources
     │
     ├── LOGIN / PERMISSION?
     │      → gm-security
     │
     ├── BUSINESS STRUCTURE?
     │      → gm-organizations
     │
     ├── FISCAL CONTEXT?
     │      → TaxSubject / fiscal
     │
     └── BUSINESS EVENT / TRANSACTION?
            → operational module
```

This decision tree is mandatory reference for future domain modeling.

---

# 68. Canonical database philosophy

The GYPPORT database must model the business universe, not individual UI screens.

Persist concepts because they have domain meaning.

Good:

```text
MdmParty
Party
Employment
TaxSubject
UserAccount
OrganizationAccess
ContactPoint
Address
```

Bad as competing masters:

```text
EmployeePersonCopy
CustomerPersonCopy
SupplierPersonCopy
FleetPersonCopy
ExpensePersonCopy
```

---

# 69. Identity lifecycle

```text
UNKNOWN
→ INTAKE
→ NORMALIZED
→ PENDING_VERIFICATION
→ RESOLVED
```

Possible exceptional states:

```text
CONFLICT
REJECTED
MANUAL_REVIEW
```

Do not insert unresolved subjects directly into Golden Record merely to unblock a flow.

---

# 70. Account lifecycle vs identity lifecycle

```text
UserAccount created
→ email verified
→ identity pending
→ limited allowed functionality
→ IdentityClaim approved
→ MDM/Party linked
→ identity-resolved account
```

Do not require fake Person creation merely to authenticate.

---

# 71. Personal context

A Person may have a personal GYPPORT context independent of business memberships.

Possible future domains include personal profile, documents, expenses, fiscal interactions, assets/liabilities and consumer behavior.

Do not interpret Personal as a company.

---

# 72. Business contexts

One Person may have:

```text
Personal
My Business
Company A
Company B
Company C
```

Each context may expose different modules and permissions.

Membership visibility does not imply authorization.

---

# 73. UI must reflect domain truth

If identity exists:

```text
"Identidad encontrada"
```

not:

```text
"Crear nueva Persona"
```

If email account exists:

```text
"Continuar con la cuenta existente"
```

not:

```text
"Crear otro UserAccount"
```

If membership is missing:

```text
"Se requiere acceso a esta organización"
```

not:

```text
"Crear otra identidad"
```

---

# 74. Canonical profile separation

Future profile should distinguish:

```text
IDENTITY PROFILE
→ MDM canonical data

ACCOUNT PROFILE
→ authentication/security data

CONTACTS
→ multiple historical ContactPoints

ADDRESSES
→ multiple historical Addresses

BUSINESS CONTEXT
→ active tenant/organization

EMPLOYMENT
→ work-specific relationship/contact data

ROLES
→ contextual authorization
```

Do not collapse everything into one profile record.

---

# 75. Current universal foundation status

```text
Universal MDM                 ✅
Universal Intake              ✅
Party tenant                  ✅
TaxSubject universal          ✅
Identity collation            ✅
Pending account identity      ⏳ STEP 14
Global Account/Membership     ⏭ STEP 15
Contact/Address History       schema exists;
                              full domain/use-cases pending
```

---

# 76. Immediate development sequence

Before broad module expansion:

```text
1. Close STEP 14 correctly
2. Build Global Account / Tenant Membership foundation
3. Complete Contact / Address History domain
4. Expand operational modules against these canonical foundations
```

This reduces future dismantling of CRM, Sales, Purchases, Accounting, Inventory and HR.

---

# 77. Historical architecture is part of the evidence

When reviewing a domain, search:

```text
historical conversations
+
uploaded historical documents
+
canonical baselines
+
ADRs
+
Owner-accepted STEPs
+
historical schema/dumps
+
current repository
```

before proposing structural change.

---

# 78. Conflict protocol

If historical documents, current implementation and recent decisions differ:

```text
HISTORICAL_INTENT=
CURRENT_IMPLEMENTATION=
CURRENT_CANONICAL_DECISION=
CONFLICT=
IMPACT=
RECOMMENDED_RECONCILIATION=
OWNER_DECISION_REQUIRED=
```

Stop for Owner review when the conflict changes architecture.

---

# 79. Contracts for future AI agents

Any AI agent working on GYPPORT must:

1. identify canonical domain owner;
2. search existing schema/code before adding tables;
3. read relevant historical and canonical documents;
4. classify global vs tenant;
5. classify master vs relationship vs transaction;
6. preserve history;
7. preserve IDs and UUIDs;
8. avoid duplicate source of truth;
9. maintain tenant safety;
10. stop on architectural conflict;
11. not weaken MDM/Party for local convenience;
12. not commit or migrate without Owner authorization.

---

# 80. Minimum reading before identity-related changes

Before touching MDM, Party, registration, UserAccount, Employee, contacts, addresses, TaxSubject, customer/supplier master or organization identity, read at minimum:

```text
GYPPORT_UNIVERSE_CANONICAL_BASELINE.md
GYPPORT_MDM_FOUNDATION_MEMORY_2026-09-11.md
GYPPORT_UNIVERSAL_MDM_CANONICAL_MEMORY_2026-09-11.md
this document
relevant ADRs
relevant Owner-accepted STEP documents
historical Base de Clientes / Global Registry materials
```

---

# 81. Canonical summary

```text
MdmParty
= QUIÉN ES

Party
= CÓMO PARTICIPA EN UN TENANT

UserAccount
= CÓMO INGRESA A GYPPORT

Tenant Membership
= EN QUÉ CONTEXTOS PUEDE OPERAR

Employment
= QUÉ RELACIÓN LABORAL TIENE

Role
= QUÉ PUEDE HACER EN ESE CONTEXTO

gm-organizations
= CÓMO ESTÁ ESTRUCTURADA LA EMPRESA

TaxSubject
= EN QUÉ CONTEXTO FISCAL OPERA

ContactPoints / Addresses
= CÓMO Y DÓNDE PUEDE SER CONTACTADO,
  CONSERVANDO HISTORIA

Operational Module
= QUÉ TRANSACCIÓN / PROCESO DE NEGOCIO OCURRE
```

---

# 82. Canonical human-readable rule

```text
1 Persona
≠ 1 empresa

1 Persona
≠ 1 rol

1 Persona
≠ 1 email

1 Persona
≠ 1 teléfono

1 Persona
≠ 1 dirección

1 Persona
≠ 1 UserAccount por empresa

1 Persona
= 1 identidad global
  con múltiples contextos,
  relaciones,
  contactos,
  direcciones,
  roles e historia.
```

---

# 83. Final GYPPORT principle

GYPPORT Business Platform Universal must be designed so that every new module asks:

```text
¿Ya existe este concepto en el Universo?

SI
→ lo referencia

NO
→ identifica su verdadero owner
→ lo modela una sola vez
```

The objective is not merely to avoid duplicate tables.

The objective is to preserve one coherent business universe across ERP, CRM, HR, Accounting, Sales, Purchases, Expenses, Fleet, Fuel, Tax, e-Documents, Analytics, Consulting and future modules.

# GYPPORT® Business Platform Universal

> One canonical universe, many business contexts, many operational modules, no duplicate truth.

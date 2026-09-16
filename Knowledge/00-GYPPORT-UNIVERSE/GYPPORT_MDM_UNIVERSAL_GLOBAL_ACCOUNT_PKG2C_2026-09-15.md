# GYPPORT® — MDM Universal + Global Account / Tenant Membership Foundation — PKG-2C

**Fecha:** 2026-09-15  
**Estado:** `OWNER_DECISIONS_RESOLVED_READY_FOR_IMPLEMENTATION`  
**Track correcto:** Fundación transversal de Identidad, MDM, Cuenta Global, Membership y Party contextual.  
**No pertenece a:** `gm-fleets` como dominio funcional.

## 1. Propósito

Este documento separa formalmente el trabajo de **Universal MDM / Global Account / Tenant Membership** del desarrollo de `gm-fleets`.

La conversación original salió de Flotas y terminó entrando en una cadena transversal:

```text
gm-fleets
→ Person / Organization references
→ Global identity
→ Global UserAccount
→ UserTenantMembership
→ tenant/platform sessions
→ contextual Party
→ PKG-2C FK reconciliation
```

La cadena arquitectónica es válida, pero **PKG-2C no es trabajo funcional de gm-fleets**.

La continuidad correcta está en:

```text
GYPPORT Global Account / Tenant Membership Foundation
+
gm-entities / Universal MDM
```

## 2. Principios canónicos

```text
IDENTITY = GLOBAL
BUSINESS PARTICIPATION = TENANT-CONTEXTUAL
ACCESS = SECURITY
EMPLOYMENT = HR
AUDIT ACTOR = GLOBAL ACCOUNT
```

### MdmParty

```text
MdmParty = identidad global / Golden Record
```

Responde:

> ¿Quién es esta persona u organización en todo GYPPORT?

Tipos canónicos:

```text
PERSON
ORGANIZATION
```

Una persona natural con RUC sigue siendo `PERSON`. El RUC no convierte por sí solo una persona en organización.

### Party

```text
Party = participación/proyección de una identidad global dentro de un tenant
```

Ejemplo:

```text
MdmParty #1000
├── Party #10 Tenant A
├── Party #42 Tenant B
└── Party #91 Tenant C
```

Regla absoluta:

```text
mdm_party_id != party_id
MdmParty = GLOBAL
Party = TENANT-CONTEXTUAL
```

No debe existir Party sin Golden Record MDM.

### UserAccount

```text
UserAccount = identidad global de autenticación
```

Una cuenta puede participar en múltiples tenants. Los campos legacy `user_accounts.tenant_id` y `user_accounts.party_id` permanecen temporalmente por compatibilidad/origen, pero no representan el modelo multi-tenant final.

### UserTenantMembership

```text
UserTenantMembership = ACCOUNT_TO_TENANT_ACCESS_ONLY
```

Responde:

> ¿Puede esta cuenta operar en este tenant?

No representa Person, Party, Employee, Role, OrganizationAccess, business relationship ni actor histórico.

Estados:

```text
INVITED
ACTIVE
SUSPENDED
REVOKED
```

Solo `ACTIVE` autoriza operación tenant.

### Actor histórico

Los campos de actor representan:

```text
Global UserAccount
```

El tenant representa contexto/provenance.

Por tanto, `created_by`, `approved_by`, `revoked_by`, `granted_by`, `assigned_by`, `verified_by`, etc. **no se mueven a Membership**.

## 3. Ownership por módulo

### gm-entities

Owner de:

```text
Universal MDM
MdmParty
Person
Organization identity
Identifiers
Identity Intake / staging
Normalization
Matching / resolution
Consolidation / merge
Contact history
Address history
Provenance
Tenant Party projections
Contextual Party read APIs
```

### gm-security

Owner de:

```text
Global UserAccount
Authentication
Authorization
UserTenantMembership
Roles
Permissions
Security scopes
```

### gm-organizations

Owner de estructura empresarial interna: Organizations, Branches, Departments, Cost Centers.

### gm-human-resources

Owner de Employment, Employee, Position, assignments y lifecycle laboral.

### Fiscal / Tax Subject

Owner de TaxSubject, SRI Establishments, Emission Points, Sequences y contexto tributario operativo.

## 4. Universal MDM Intake

Flujo canónico:

```text
SOURCE
→ INTAKE / STAGING
→ NORMALIZATION
→ GYPPORT MDM MATCHING
→ AUTHORITATIVE VERIFICATION WHEN NEEDED
→ MDM RESOLUTION
   ├── existing → reuse
   └── verified new → create
→ PARTY TENANT PROJECTION
→ business relationship / capability
```

No crear un `MdmParty` falso o incompleto solo para desbloquear un flujo.

## 5. Party no se crea por Membership

Decisión Owner:

```text
ACTIVE UserTenantMembership != Party creation
```

Una cuenta global RESOLVED puede tener Membership ACTIVE en Tenant B y todavía no tener Party B.

Política:

```text
RESOLVED_NON_ORIGIN_PARTY_PROJECTION = LAZY_EXPLICIT
```

Party se provisiona cuando una relación empresarial real lo requiere, por ejemplo Employment, Customer/Supplier, Fleet owner/driver u otra relación Party-dependent.

Nunca por:

```text
login
/auth/me
session authentication
permission lookup
authorization read
contextual Party lookup
```

Regla:

```text
READ PATHS READ
PROVISIONING PATHS PROVISION
```

## 6. Baseline técnico cerrado

### PKG-2A — Runtime Membership Writers

```text
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL

gm-security
b42b55f4100fea3f2dc71359c2f41acae8d6fc69

Gystigo
53ea507a23392847c1502562f3f69bf844dbc084
```

### PKG-2B — Tenant + Platform Session Foundation

```text
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL

gm-security
ee3c2a95efb4efa61b3eaf6405df4e3822b56e4b

Gystigo
59bd77f0bf6a2aa6b1c3083097a8c8e0b258ff56
```

Migración:

```text
V56__tenantless_platform_sessions.sql
```

Modelo:

```text
Global UserAccount
├── TENANT SESSION
│   └── ACTIVE UserTenantMembership required
└── PLATFORM SESSION
    ├── tenant_id = NULL
    ├── active_organization_id = NULL
    └── active Platform Admin required
```

Política temporal:

```text
Platform Admin + ACTIVE origin membership
→ TENANT SESSION

Platform Admin without ACTIVE origin membership
→ PLATFORM SESSION

Explicit context selection
→ PKG-2D
```

## 7. PKG-2C — objetivo

Preparar la base para:

```text
one Global UserAccount
→ many tenant memberships
→ correct contextual Party
→ correct tenant access relations
→ correct global historical actor
```

sin implementar todavía selector/cambio real de tenant.

## 8. PKG-2C.1 — Contextual Party Read Foundation

Objetivo:

```text
Global UserAccount.mdm_party_id
+
current tenant
→ Party of that tenant
```

No usar `user_accounts.party_id` como si fuera Party universal.

Read port esperado en `gm-entities`:

```java
Optional<TenantParty> findByMdmParty(
    TenantId tenantId,
    MdmPartyId mdmPartyId
)
```

Debe ser estrictamente read-only. Si no existe Party:

```text
Optional.empty
```

y cero filas creadas.

Lectores a reconciliar incluyen, según la auditoría: `JdbcPartyAccessQueryAdapter`, `JdbcUserAccountRepository.findActiveByParty` y sus callers de EmployeeAccess, `ConfirmOrganizationControlUseCase`, `ClaimOrganizationControlUseCase`, `MyProfileService` y `JdbcPlatformOrganizationControlQueryAdapter`.

`ProfileIdentityService` requiere revisión específica antes de reinterpretarlo como tenant-contextual.

## 9. PKG-2C.2 — V57 Access-Subject FK Reconciliation

Migración autorizada:

```text
V57__tenant_access_subject_membership_fks.sql
```

Cinco relaciones de sujeto de acceso pasan de:

```text
(tenant_id,user_account_id)
→ user_accounts(tenant_id,user_account_id)
```

a:

```text
(tenant_id,user_account_id)
→ user_tenant_memberships(tenant_id,user_account_id)
```

Tablas:

```text
user_roles
organization_access
user_sessions
user_branches
user_establishments
```

No agregar `membership_id`. No cambiar filas. No borrar datos. No cambiar IDs/UUIDs.

La FK prueba que Membership **existe**, no que esté ACTIVE. ACTIVE sigue siendo regla de aplicación.

## 10. PKG-2C.3 — V58 Global Actor FK Reconciliation

Decisión Owner:

```text
OPTION_A_APPROVED
```

Los actores históricos dejan de estar físicamente restringidos a:

```text
actor origin tenant == action tenant
```

y pasan a:

```text
actor_user_account_id
→ user_accounts(user_account_id)
```

manteniendo `tenant_id` como contexto/provenance.

Migración esperada:

```text
V58__global_user_account_actor_fks.sql
```

Regla absoluta:

```text
ACTOR_FIELDS_MOVED_TO_MEMBERSHIP=0
```

Mantener columnas de provenance de Platform Admin como `granted_by_platform_admin_id`, `verified_by_platform_admin_id`, `actor_platform_admin_id` cuando existan.

## 11. Decisiones Owner cerradas

```text
OWNER_DECISION_1=OPTION_A_APPROVED
ACTOR_FKS=GLOBAL_USER_ACCOUNT
NEVER_USER_TENANT_MEMBERSHIP
```

```text
OWNER_DECISION_2=INCLUDE_USER_BRANCHES_AND_USER_ESTABLISHMENTS_IN_V57
```

Solo se re-pointa su FK de sujeto de acceso. No se reasigna ownership, no se borran tablas, no se limpian keys.

```text
OWNER_DECISION_3=RESOLVED_NON_ORIGIN_PARTY_PROJECTION_LAZY_EXPLICIT
```

Membership nunca crea Party por existir.

```text
OWNER_DECISION_4=EVC_PRC_ACCOUNT_FK_RESHAPE_DEFER
```

Email verification y password recovery siguen lógicamente account-level, pero su reshape no es necesario en PKG-2C.

## 12. user_accounts legacy fields

Se mantienen:

```text
user_accounts.tenant_id
user_accounts.party_id
```

No se eliminan, no se relajan.

Pero `user_accounts.party_id` ya no debe tratarse como la respuesta universal al Party del tenant actual.

La respuesta correcta:

```text
current tenant
+
user_accounts.mdm_party_id
→ parties
```

## 13. Relaciones después de PKG-2C

```text
MdmParty
   ├── Party Tenant A
   ├── Party Tenant B
   └── Party Tenant C

Global UserAccount
   ├── mdm_party_id
   ├── Membership Tenant A
   ├── Membership Tenant B
   └── Membership Tenant C

Membership
   ├── user_roles
   ├── organization_access
   ├── tenant sessions
   ├── user_branches
   └── user_establishments

Historical actions
   └── Global UserAccount actor + tenant context
```

Esto separa identidad, acceso, participación empresarial y auditoría histórica.

## 14. Fuera de PKG-2C

No implementar todavía:

```text
tenant selector
context switch UI
multi-tenant navigation
invitation acceptance UX
membership catalog UI/API
cross-tenant login selection
removal of GLOBAL_ACCOUNT_MEMBERSHIP_REQUIRED
removal of user_accounts.tenant_id
removal of user_accounts.party_id
Personal/Business/Home classification
MDM redesign
HR redesign
Fiscal redesign
```

El flujo real multi-tenant queda para `PKG-2D`.

## 15. Shared DEV

Shared DEV permanece:

```text
Flyway V43
```

No aplicar V53–V58 allí durante este STEP. Pruebas de DB: MySQL disposable.

## 16. Deuda preexistente conocida

```text
1. TeamEmployeeRealDatabaseAcceptanceTest:84
   expected 2
   actual 0

2. TeamEmployeeControllerScopeBoundaryRealDatabaseAcceptanceTest
   createRole
   expected 201
   actual 403

3. PersonIdentityReconciliationHttpTest:222
   expected 200
   actual 403
```

## 17. Estado actual

Última auditoría PKG-2C:

```text
STATUS=AUDIT_COMPLETE_READY_FOR_OWNER_REVIEW
CONFLICT_FOUND=YES
```

El conflicto de actor FKs fue resuelto por Owner:

```text
OPTION_A_APPROVED
```

Estado de continuidad correcto:

```text
PKG_2C_STATUS=
OWNER_DECISIONS_RESOLVED_READY_FOR_IMPLEMENTATION
```

Siguiente secuencia:

```text
2C.1
→ contextual Party read foundation

2C.2
→ V57 membership subject FKs

2C.3
→ V58 global actor FKs
```

Sin commit hasta verificación completa y Owner Review.

## 18. Separación con gm-fleets

`gm-fleets` no es owner de estas decisiones.

Flotas consume referencias canónicas a Party/Person/Organization cuando corresponda, pero no debe crear maestros locales ni redefinir MDM, Party, Membership o UserAccount.

Ejemplo:

```text
Vehicle
→ owner/driver relationship
→ canonical Party / Person reference
```

No:

```text
gm-fleets
→ local driver/person master
```

## 19. Continuity Packet

```text
TRACK=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION

UNIVERSAL_MDM_OWNER=gm-entities
GLOBAL_USER_ACCOUNT_OWNER=gm-security
USER_TENANT_MEMBERSHIP_OWNER=gm-security
TENANT_PARTY_OWNER=gm-entities

PKG2A=OWNER_ACCEPTED_COMMITTED_LOCAL
PKG2B=OWNER_ACCEPTED_COMMITTED_LOCAL

GYSTIGO_BASELINE=59bd77f0bf6a2aa6b1c3083097a8c8e0b258ff56
GM_SECURITY_BASELINE=ee3c2a95efb4efa61b3eaf6405df4e3822b56e4b
GM_ENTITIES_BASELINE=7b2c56fc5141f38f2bb1e14f11c6d32e3eecca2e
GM_EXPENSES_BASELINE=ab74610094dcdbdbb93564fc7b9fe05b51c7b8c2
FABRIC_BASELINE=1798ac4e657a3d0408d1cea3ee082a97ac203511

MIGRATION_HEAD=V56
NEXT_FREE_MIGRATION=V57

PKG2C_OWNER_DECISIONS_RESOLVED=YES
PKG2C_NEXT=2C.1 → 2C.2/V57 → 2C.3/V58

PARTY_PROJECTION_POLICY=LAZY_EXPLICIT
ACTOR_REFERENCE_POLICY=GLOBAL_USER_ACCOUNT
ACCESS_SUBJECT_REFERENCE_POLICY=USER_TENANT_MEMBERSHIP
EVC_PRC_RESHAPE=DEFER

STUDIO_MULTI_TENANT_WORK=DEFER_TO_PKG2D
CROSS_TENANT_SELECTION=DEFER_TO_PKG2D

SHARED_DEV=V43_READ_ONLY

COMMIT_STATUS=NO_PKG2C_COMMIT_YET
PUSH_STATUS=NOT_AUTHORIZED
```

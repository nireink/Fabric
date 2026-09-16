# GYPPORT® Business Platform — Universo de Datos, MDM, Seguridad, Fiscalidad y Trazabilidad

**Fecha de consolidación:** 2026-09-13  
**Estado:** `OWNER_APPROVED_CANONICAL_CONTEXT`  
**Propósito:** crear un punto único, granular y legible por humanos/agentes para entender GYPPORT antes de proponer o ejecutar cambios sobre base de datos, MDM, identidad, Party, organizaciones, RRHH, seguridad, fiscalidad, SRI, auditoría o módulos operativos.

> Este documento consolida decisiones Owner, ADRs/STEPs aceptados, auditorías recientes, memoria canónica MDM, evidencia histórica de junio de 2026 y realidad verificada de base de datos/runtime.
> No sustituye silenciosamente los ADRs ya aprobados. Cuando exista conflicto, rige la precedencia definida en este documento y el agente debe detenerse para revisión Owner.

---

# 0. Regla de precedencia y método de trabajo

## 0.1 Precedencia obligatoria

```text
1. OWNER EXPLICIT DECISION MÁS RECIENTE
2. FABRIC / UNIVERSE BASELINE / ADR APROBADO
3. STEPs OWNER-ACCEPTED / OWNERSHIP MATRICES
4. DOCUMENTACIÓN HISTÓRICA Y DUMPS
5. IMPLEMENTACIÓN Y BASE DE DATOS ACTUAL VERIFICADA
6. MEMORIAS DE CONTINUIDAD
7. PROPUESTAS NUEVAS
```

Una propuesta nueva nunca puede borrar una decisión anterior por comodidad.

Si hay conflicto:

```text
HISTORICAL_INTENT=
CURRENT_CANONICAL_DOCUMENT=
CURRENT_SCHEMA=
CURRENT_CODE=
CONFLICT=
IMPACT=
PROPOSED_RECONCILIATION=
OWNER_DECISION_REQUIRED=
```

## 0.2 Regla operativa

```text
EXISTING != WRONG
AUDIT BEFORE REBUILD
HISTORY EXPLAINS WHY
REPO/DB DEMONSTRATES HOW NOW
OWNER DECISION DEFINES WHERE TO EVOLVE
```

## 0.3 Knowledge Gate obligatorio para futuros agentes

Antes de modificar arquitectura o datos:

1. Leer `Fabric/Knowledge/00-GYPPORT-UNIVERSE/`.
2. Leer el Universe Baseline.
3. Leer este documento.
4. Leer los ADRs directamente relacionados.
5. Revisar las ownership matrices de los módulos afectados.
6. Verificar HEADs reales.
7. Revisar migraciones y esquema real.
8. Revisar código que realmente lee/escribe esas tablas.
9. Revisar pruebas que materializan invariantes.
10. Solo después proponer.

No trabajar únicamente desde memoria conversacional.


## 0.4 Conflict Gate — STOP obligatorio antes de ejecutar

Detectar un conflicto entre historia, documentación canónica, esquema, código, pruebas o una nueva propuesta **no autoriza al agente a resolverlo por su cuenta**.

Regla:

```text
CONFLICT_FOUND=YES
→ STOP EXECUTION
→ REPORT EVIDENCE
→ EXPLAIN IMPACT
→ PROPOSE RECONCILIATION OPTIONS
→ RECOMMEND ONE OPTION WITH REASONS
→ OWNER REVIEW
→ DO NOT MODIFY FILES / SCHEMA / DATA TO RESOLVE THE CONFLICT
```

El agente debe devolver como mínimo:

```text
HISTORICAL_INTENT=
CURRENT_CANONICAL_DOCUMENT=
CURRENT_SCHEMA=
CURRENT_CODE=
CURRENT_TEST_EVIDENCE=
CONFLICT=
IMPACT=

RECONCILIATION_OPTIONS=
OPTION_A=
OPTION_A_IMPACT=
OPTION_B=
OPTION_B_IMPACT=
OPTION_C=   # si aplica
OPTION_C_IMPACT=

RECOMMENDED_RECONCILIATION=
RECOMMENDATION_REASON=

OWNER_DECISION_REQUIRED=
EXECUTION_STATUS=STOPPED_PENDING_OWNER_REVIEW
SAFE_CHANGES_ALREADY_COMPLETED=
UNEXECUTED_SCOPE=
```

### 0.4.1 Qué significa STOP

Mientras `OWNER_DECISION_REQUIRED` no esté resuelto:

- no implementar la reconciliación propuesta;
- no crear/alterar migraciones para “arreglar” el conflicto;
- no renombrar ni borrar campos;
- no mover ownership;
- no simplificar historia/auditoría;
- no hacer commit del cambio conflictivo;
- no continuar hacia fases dependientes;
- no reinterpretar la decisión histórica para que encaje con el código actual.

Puede completar únicamente verificaciones **read-only** necesarias para explicar mejor el conflicto.

### 0.4.2 El agente debe sugerir cómo resolverlo

El STOP no debe limitarse a decir “hay un conflicto”.

Debe explicar:

```text
WHAT_CONFLICTS=
WHY_IT_MATTERS=
WHAT_BREAKS_IF_IGNORED=
WHAT_EACH_SOURCE_WAS_TRYING_TO_PROTECT=
```

y presentar alternativas concretas.

La recomendación debe distinguir:

```text
FACT=
OWNER_DECISION=
INFERENCE=
PROPOSAL=
```

Una `PROPOSAL` nunca puede presentarse como decisión canónica antes de aprobación Owner.

### 0.4.3 Reanudación después de la decisión Owner

Cuando el Owner responda:

```text
OWNER_DECISION_RECEIVED=YES
```

el agente **no debe empezar desde cero ni reinterpretar la decisión**.

Debe:

1. releer la decisión exacta del Owner;
2. releer este documento y los ADRs afectados;
3. verificar nuevamente HEAD, `git status`, migración head y WIP;
4. confirmar que no hubo drift mientras estuvo detenido;
5. actualizar el checkpoint/continuity packet;
6. reanudar el mismo STEP desde el punto detenido;
7. ejecutar únicamente la opción aprobada;
8. volver a probar todo el alcance afectado.

Formato mínimo antes de reanudar:

```text
OWNER_DECISION_RECEIVED=YES
OWNER_DECISION=
PREVIOUS_CONFLICT=
APPROVED_RECONCILIATION=

CURRENT_HEAD=
CURRENT_MIGRATION_HEAD=
WORKING_TREE_RECHECKED=YES
DRIFT_SINCE_STOP=YES|NO

IF_DRIFT=
IMPACT_OF_DRIFT=
SECOND_OWNER_REVIEW_REQUIRED=YES|NO

RESUME_FROM=
RESTART_FROM_ZERO=NO
```

Si apareció drift que cambia la validez de la decisión:

```text
SECOND_OWNER_REVIEW_REQUIRED=YES
EXECUTION_STATUS=STOPPED_PENDING_OWNER_REVIEW
```

### 0.4.4 Una propuesta nueva nunca reemplaza historia silenciosamente

Esta regla es absoluta:

```text
NEW_PROPOSAL
!=
PERMISSION_TO_OVERRIDE_HISTORY
```

Si una propuesta nueva exige cambiar algo previamente aprobado:

```text
OLD_DECISION=
NEW_NEED=
WHY_OLD_DECISION_NO_LONGER_FITS=
COMPATIBILITY_IMPACT=
MIGRATION_IMPACT=
AUDIT_HISTORY_IMPACT=
RECOMMENDED_CHANGE=
OWNER_DECISION_REQUIRED=YES
```

Hasta aprobación:

```text
CANONICAL_STATE=OLD_DECISION_REMAINS_ACTIVE
```

### 0.4.5 Conflicto descubierto durante implementación

Si el conflicto aparece después de haber comenzado a implementar un STEP:

1. detener la parte conflictiva inmediatamente;
2. conservar exactamente los cambios no conflictivos ya verificados;
3. no “terminar para ver si funciona”;
4. no commit del paquete completo;
5. identificar los archivos afectados;
6. presentar diff/scope del trabajo ya realizado;
7. proponer reconciliación;
8. esperar Owner.

Formato:

```text
CONFLICT_DISCOVERED_DURING_IMPLEMENTATION=YES
FILES_ALREADY_CHANGED=
FILES_CONFLICT_AFFECTS=
SAFE_CHANGES=
CHANGES_REQUIRING_OWNER_DECISION=
COMMIT_ALLOWED=NO
EXECUTION_STATUS=STOPPED_PENDING_OWNER_REVIEW
```

### 0.4.6 Conflicto descubierto en un prompt de auditoría

En auditorías read-only:

- continuar únicamente la recolección de evidencia que ayude a explicar el conflicto;
- no convertir la auditoría en implementación;
- terminar el informe con `STOP_FOR_OWNER_REVIEW=YES`.

### 0.4.7 Regla para agentes sucesores

Un agente nuevo que encuentre un checkpoint detenido por conflicto debe:

```text
READ_EXISTING_CONFLICT_PACKET=YES
DO_NOT_RESTART_STEP=YES
DO_NOT_PICK_OPTION_AUTONOMOUSLY=YES
```

Debe continuar desde la decisión Owner o permanecer detenido.


---

## 0.5 Rol de `Reglas.md` — bitácora histórica acumulativa

`Reglas.md` no es un manual homogéneo ni un catálogo que deba normalizarse.
Es la bitácora histórica donde el Owner va dejando reglas, principios,
decisiones, estados y aprendizajes surgidos en conversaciones y STEPs.

Reglas de preservación:

```text
REGLAS_MD_ROLE=HISTORICAL_DECISION_AND_RULE_LOG
PRESERVE_EXISTING_TEXT=YES
APPEND_ONLY=YES
RENUMBER_EXISTING_RULES=NO
REORGANIZE_EXISTING_HISTORY=NO
CONSOLIDATE_OLD_RULES=NO
DELETE_SUPERSEDED_RULES=NO
```

Cuando una regla posterior sustituye otra, la anterior permanece como evidencia
histórica. La nueva entrada debe indicar de forma explícita qué decisión
reemplaza o corrige.

`Reglas.md` debe leerse como evidencia persistente de decisiones Owner, pero no
autoriza a ignorar documentos canónicos más específicos, ADRs o el estado real
del repositorio. Si existe contradicción, aplica el Conflict Gate.

Cuando `Reglas.md` cambie, deberá entregarse el archivo completo actualizado,
preservando el contenido anterior y añadiendo las nuevas entradas al final.


# 1. Principio central del Universo GYPPORT

```text
IDENTITY = GLOBAL
BUSINESS / OPERATIONAL RELATIONSHIP = TENANT-CONTEXTUAL
ACCESS = SECURITY
EMPLOYMENT = HR
FISCAL OPERATION = TAX SUBJECT
AUDIT ACTOR = GLOBAL ACCOUNT
```

El núcleo conceptual es:

```text
                         GYPPORT UNIVERSAL MDM
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
         MdmParty PERSON                   MdmParty ORGANIZATION
         Persona humana                    Organización / entidad
                 │                                 │
                 └──────── identidad global ───────┘
                                  │
                                  ▼
                             Party por tenant
                                  │
           ┌──────────────────────┼──────────────────────┐
           │                      │                      │
     relaciones comerciales   Employment          TaxSubject
           │                      │                      │
       Customer/Supplier        HR               Fiscal/SRI
                                  │
                                  ▼
                              Seguridad
                     UserAccount + Memberships
```

Reglas:

```text
MdmParty != Party
Person != UserAccount
Person != Employee
Employee != UserAccount
Position != Security Role
Tenant != Organization
Branch != SRI Establishment
RUC != Organization
TaxSubject != Organization
OrganizationAccess != Authorization
Membership != Role
Actor != Membership
```

---

# 2. MDM global — `MdmParty`

## 2.1 Qué representa

`MdmParty` responde:

> ¿Quién es esta Persona u Organización globalmente dentro del ecosistema GYPPORT?

Tipos fundamentales:

```text
MdmParty PERSON
MdmParty ORGANIZATION
```

No usar maestros paralelos por módulo.

## 2.2 Golden Record

Un MdmParty es un Golden Record global.

Debe ser:

- reutilizable por varios tenants;
- estable;
- no provisional;
- resoluble mediante identificadores canónicos;
- consolidable de forma controlada;
- compatible con provenance e historia.

Nunca crear un MdmParty incompleto únicamente para desbloquear un flujo.

## 2.3 Múltiples tenants

```text
MdmParty #1000
├── Party #10 · Tenant A
├── Party #42 · Tenant B
└── Party #91 · Tenant C
```

`mdm_party_id` es global.

`party_id` es contextual al tenant.

No colapsar ambos conceptos.

---

# 3. Universal MDM Intake

Todo origen que pueda introducir una Persona u Organización debe converger hacia una frontera común.

```text
SOURCE
→ INTAKE / STAGING
→ NORMALIZATION
→ DETERMINISTIC MATCHING
→ VALIDATION / VERIFICATION
→ MDM RESOLUTION
   ├── EXISTING
   ├── NEW VERIFIED
   ├── PENDING
   └── CONFLICT
→ PARTY TENANT PROJECTION
→ DOMAIN RELATIONSHIP
```

Fuentes potenciales:

- registro;
- Crear Persona;
- Crear Organización;
- RRHH;
- CRM;
- Ventas;
- Compras;
- SRI;
- Registro Civil;
- integraciones;
- importaciones;
- módulos operativos.

## 3.1 No provisional Party

La regla canónica es:

```text
parties.mdm_party_id = NOT NULL
```

Por tanto:

- no Party con MDM nulo;
- no MdmParty ficticio;
- candidatos incompletos permanecen en Intake;
- Party se crea/reutiliza después de resolver MDM.

## 3.2 Matching

```text
INITIAL_MDM_MATCHING
= DETERMINISTIC_CANONICAL_IDENTIFIERS_ONLY
```

Ejemplos:

- CÉDULA / NUI;
- RUC;
- PASSPORT;
- otros identificadores oficiales soportados.

No auto-merge por:

```text
NAME
EMAIL
PHONE
ADDRESS
```

Estos son evidencia, no claves determinísticas de identidad.

## 3.3 Normalización

```text
normalize
→ trim
→ validate structurally
→ compare
→ verify when necessary
→ persist
```

La validación estructural local no equivale a verificación de identidad.

---

# 4. Persona, organización, usuario y perfil

## 4.1 Toda persona usuaria termina resolviendo a PERSON

Técnicamente puede existir una cuenta pendiente antes de la resolución MDM.

```text
Registro
→ UserAccount PENDING
→ Universal Intake
→ resolución
→ MdmParty PERSON
```

Regla:

```text
Person != UserAccount
```

`UserAccount` autentica.  
`MdmParty PERSON` representa a la Persona.

## 4.2 Persona Natural con RUC

Regla definitiva:

```text
PERSONA NATURAL + RUC
= MdmParty PERSON
```

Nunca:

```text
RUC → crear Organization
```

Ejemplo:

```text
MdmParty PERSON
├── Cédula / NUI
├── RUC personal
├── contactos
├── direcciones
├── Tax Profile
└── TaxSubject
    ├── SRI Establishment 001
    ├── SRI Establishment 002
    └── ...
```

Un RUC personal puede tener uno o múltiples establecimientos.

El nombre comercial de un establecimiento no implica que exista otra Organization.

## 4.3 Organización con RUC

Una entidad jurídica distinta sí tiene su propio Golden Record:

```text
MdmParty ORGANIZATION
├── RUC
├── nombre/identidad canónica
├── Tax Profile
└── TaxSubject
    ├── SRI Establishment 001
    └── SRI Establishment 002
```

Una Persona puede relacionarse con múltiples Organizations sin transformarse en ellas.

---

# 5. Party tenant projection

`Party` responde:

> ¿Cómo participa esta identidad global dentro de este tenant?

Regla:

```text
Party
= tenant projection of MdmParty
```

Invariante actual:

```text
UNIQUE (tenant_id, mdm_party_id)
```

Objetivo:

```text
MdmParty PERSON/ORGANIZATION
→ 0..N Party tenant projections
```

Party no es:

- cliente master;
- proveedor master;
- empleado master;
- usuario master.

Es el ancla tenant-safe para relaciones y operación.

---

# 6. Customer, Supplier, Employee y otros roles

No crear otro maestro de Persona/Organización.

Patrón:

```text
MdmParty
→ Party tenant
→ relationship/capability
```

Ejemplos:

```text
Customer
Supplier
Contact
Shareholder
Responsible
Owner
Legal Representative
```

La evidencia histórica de junio ya contenía catálogos de relación como:

- `OWNER`;
- `LEGAL_REPRESENTATIVE`;
- `EMPLOYEE_OF`;
- `SUPPLIER_OF`;
- `CUSTOMER_OF`;
- `PARENT_COMPANY`;
- `SUBSIDIARY`.

Pero el ownership moderno debe respetarse:

```text
Employment
→ gm-human-resources

Security Role
→ gm-security

Customer/Supplier business relationship
→ domain relationship, not duplicate MDM
```

No asumir que un catálogo histórico define automáticamente el owner moderno.

---

# 7. Organizations

## 7.1 Dos niveles que no deben confundirse

```text
MdmParty ORGANIZATION
= identidad global de la organización

organizations
= representación/estructura operacional dentro del tenant
```

`gm-organizations` posee:

- organizations;
- branches;
- departments;
- cost centers;
- settings;
- estructura interna.

La base actual todavía presenta huecos de integridad: la auditoría demostró que puede existir una `organizations` row sin Party correspondiente. Debe tratarse como gap, no como modelo deseado.

## 7.2 Branch

Branch pertenece a estructura empresarial.

```text
Branch != SRI Establishment
```

Una Branch puede relacionarse operativamente con establecimientos, pero no son la misma identidad ni el mismo dominio.

---

# 8. Human Resources

Owner:

```text
gm-human-resources
```

Conceptos:

- Employee;
- Employment;
- Position;
- assignments;
- supervisor;
- lifecycle laboral;
- contactos laborales futuros.

Reglas:

```text
Person != Employee
Employee != UserAccount
Employment != UserTenantMembership
Position != Security Role
```

Una Persona puede tener varios Employment a lo largo del tiempo o simultáneamente.

El trabajo/contacto laboral debe vivir en la relación laboral, no contaminar el contacto personal global.

---

# 9. Security — Global Account

## 9.1 Target canónico

```text
MdmParty PERSON
      │
      ▼
Global UserAccount
      │
      ├── UserTenantMembership → Tenant A
      ├── UserTenantMembership → Tenant B
      └── UserTenantMembership → Tenant C
```

V54 impone:

```text
ONE_ACTIVE_RESOLVED_USERACCOUNT_PER_MDMPARTY=YES
```

Las cuentas pendientes con `mdm_party_id = NULL` siguen permitidas.

## 9.2 UserAccount no es la identidad maestra

`UserAccount` posee:

- login;
- password/authentication;
- email de autenticación;
- estado de cuenta;
- capacidades de plataforma.

No posee la verdad maestra de contactos personales.

## 9.3 Email de login

```text
UserAccount.email
= authentication/recovery/verification channel
```

No es automáticamente:

```text
MdmParty primary email
```

La auditoría encontró legado donde correos de login fueron copiados al MDM. Eso es deuda histórica, no patrón futuro.

---

# 10. User Tenant Membership — STEP 15 PKG-1

PKG-1 quedó committed localmente:

```text
Gystigo
dc14e0d539d17a9f72159e5ca7640d733b1b765b

feat(security): establish global account tenant membership foundation
```

Migraciones:

```text
V53__user_tenant_membership_foundation.sql
V54__one_active_account_per_golden_record.sql
```

## 10.1 Semántica

```text
UserTenantMembership
= ¿puede esta cuenta operar en este tenant?
```

Nada más.

No contiene:

- PERSONAL;
- BUSINESS;
- HOME;
- UNCLASSIFIED;
- LEGACY_ORIGIN;
- Organization;
- Employment;
- TaxSubject;
- default context.

## 10.2 Estados

```text
INVITED
ACTIVE
SUSPENDED
REVOKED
```

Solo `ACTIVE` autoriza.

## 10.3 Eventos

Lifecycle mediante eventos append-only.

No `left_at` duplicado por ahora.

Las reglas de transición son NULL-safe.

## 10.4 Legacy backfill

```text
user_accounts.tenant_id
→ ACTIVE membership
```

Solo demuestra acceso histórico al tenant.

No clasifica el tenant.

---

# 11. STEP 15 PKG-2 — auditoría de runtime

La auditoría determinó que PKG-2 debe dividirse:

```text
PKG-2A
membership writers + V55 catch-up

PKG-2B
login/session membership gate + active context

PKG-2C
FK/contextual Party reconciliation

PKG-2D
cross-tenant account reuse + API/Studio adoption
```

No es seguro implementarlo como un solo bloque.

## 11.1 Realidad runtime actual

Actualmente:

- login copia `user_accounts.tenant_id` a `user_sessions`;
- no valida membership;
- authorization usa tenant de la sesión;
- `party_id` sigue anclado al tenant del account;
- no hay writer productivo para membership;
- cuentas creadas después de V53 pueden quedar sin membership;
- cross-tenant reuse todavía devuelve `GLOBAL_ACCOUNT_MEMBERSHIP_REQUIRED`.

## 11.2 Estado de FKs

Auditoría V54:

- 39 FKs referencian `user_accounts`;
- 29 son compuestas `(tenant_id, user_account_id)`;
- 10 son single-column global account references;
- el audit detectó además muchos actor-like columns sin FK.

No mover FKs por similitud visual. Cada una debe clasificarse semánticamente.

---

# 12. Regla canónica de audit actor

Esta sección es CRÍTICA.

## 12.1 Actor global

Campos como:

```text
created_by_user_account_id
updated_by_user_account_id
deleted_by_user_account_id
assigned_by_user_account_id
granted_by_user_account_id
revoked_by_user_account_id
verified_by_user_account_id
approved_by_user_account_id
submitted_by_user_account_id
reviewed_by_user_account_id
```

responden principalmente:

> ¿Qué cuenta global ejecutó la acción?

Por defecto:

```text
AUDIT ACTOR
→ UserAccount
```

No:

```text
AUDIT ACTOR
→ UserTenantMembership
```

## 12.2 Contexto de la acción

Separar:

```text
user_account_id
→ WHO

tenant_id
→ WHERE / tenant context

organization_id
→ narrower business context

session_id
→ authenticated execution context

role/scope
→ authority context, if historically captured

source/provenance
→ origin of data/evidence

reason
→ why

request_id / correlation_id
→ technical trace

ip / user_agent
→ technical execution evidence

timestamps
→ when
```

No colapsar esos campos en un `membership_id`.

## 12.3 Platform Admin

Platform Admin es account-level.

Puede actuar sobre un tenant sin ser miembro cliente de ese tenant.

Por tanto, convertir actor FKs a membership puede bloquear acciones legítimas y distorsionar historia.

## 12.4 Regla para PKG-2C

```text
SUBJECT / ACCESS RELATION
→ candidate for membership FK

HISTORICAL / ACTION ACTOR
→ global UserAccount + tenant context/provenance
```

Ejemplos que sí pueden depender de membership:

- `user_roles`;
- `organization_access`;
- `user_branches`;
- `user_establishments`;
- tenant-bound `user_sessions`.

Ejemplos que no deben moverse automáticamente:

- `created_by`;
- `granted_by`;
- `revoked_by`;
- `assigned_by`;
- `verified_by`;
- `approved_by`;
- `submitted_by`.

Cada FK debe revisarse individualmente con Fabric + schema + code.

---

# 13. Audit log — granularidad histórica

La base histórica ya contenía `audit_logs` con granularidad como:

- `tenant_id`;
- `user_account_id`;
- `audit_action_type_id`;
- `entity_name`;
- `entity_id`;
- `entity_uuid`;
- `entity_version`;
- `request_id`;
- `correlation_id`;
- `old_values`;
- `new_values`;
- `ip_address`;
- `user_agent`;
- `created_at`.

Esta estructura muestra una intención temprana clara:

```text
actor
+ context
+ entity
+ before/after
+ request trace
+ technical evidence
+ time
```

No reducir ese modelo.

---

# 14. Contactos globales

Desde junio de 2026 existen físicamente:

```text
mdm_party_contacts
```

Campos históricos relevantes:

- `mdm_party_id`;
- `contact_type_id`;
- `contact_value`;
- `is_primary`;
- `is_current`;
- `is_verified`;
- `valid_from`;
- `valid_to`;
- `usage_count`;
- `updated_by_tenant_id`;
- `created_at`.

## 14.1 Semántica

Una Persona u Organización puede tener:

```text
0..N emails
0..N teléfonos
0..N otros canales
```

`is_primary` no significa único.

`is_current=false` no significa borrar.

## 14.2 Deuda actual

La auditoría determinó:

```text
MULTI_VALUE_SCHEMA=YES
CODE_SUPPORT=PARTIAL/NO
PURPOSE=INSUFFICIENT
PROVENANCE=PARTIAL
```

Futuro:

- purpose explícito;
- provenance;
- verification provenance;
- historia operacional real.

---

# 15. Direcciones globales

Desde junio existe:

```text
mdm_party_addresses
```

Campos:

- `mdm_party_id`;
- `geo_location_id`;
- `address_type_id`;
- lines;
- postal;
- `is_primary`;
- `is_current`;
- `valid_from`;
- `valid_to`;
- `usage_count`;
- `updated_by_tenant_id`;
- `created_at`.

Modelo histórico deseado:

```text
Dirección A
2024 → 2026
CURRENT=NO

Dirección B
2026 →
CURRENT=YES
```

Nunca borrar A porque B se vuelve actual.

Separar además:

```text
MdmParty address
Branch address
SRI establishment fiscal address
Employment/work location
```

---

# 16. Identificadores

Owner físico/canónico:

```text
gm-entities
mdm_party_identifiers
```

Tipos:

- CÉDULA/NUI;
- RUC;
- PASSPORT;
- otros oficiales.

Regla:

```text
RUC
→ identifier of MdmParty
```

No:

```text
RUC
→ Organization discriminator
```

La autoridad fiscal `Tipo contribuyente` determina Persona Natural vs Sociedad cuando aplica.

---

# 17. Tax Profile — hechos oficiales

Datos oficiales tributarios reutilizables pertenecen semánticamente a Fiscal/Tax, con escritura física global controlada por gm-entities según ADR-0015.

Tabla existente:

```text
mdm_party_tax_profiles
```

`legal_name` en tax profile significa:

```text
OFFICIAL_FISCAL_SOURCE_OBSERVED_NAME
```

No reemplaza el nombre de identidad del MdmParty.

## 17.1 Campos de negocio relevantes

Ejemplos Owner-supplied:

- RUC;
- razón social fiscal;
- estado contribuyente;
- motivo de suspensión;
- contribuyente fantasma;
- transacciones inexistentes;
- tipo contribuyente;
- régimen;
- categoría;
- obligado a llevar contabilidad;
- agente de retención;
- contribuyente especial;
- fecha inicio;
- fecha actualización;
- fecha cese;
- fecha reinicio;
- actividad económica principal;
- establecimientos.

## 17.2 Estado actual

La auditoría encontró:

- varias columnas existen;
- no hay writer productivo completo;
- historia tributaria insuficiente;
- provenance insuficiente;
- motivo de suspensión ausente;
- algunos catálogos sin FK;
- `tax_identifier` no está suficientemente restringido a RUC.

---

# 18. Actividades económicas

Regla semántica:

```text
Economic Activity
= actividad declarada/desarrollada por el contribuyente
```

No es:

- membership kind;
- tenant type;
- Organization;
- TaxSubject;
- Business context.

## 18.1 Estado actual

Actualmente solo existe de forma parcial:

```text
mdm_party_tax_profiles.main_economic_activity
```

como texto libre.

Falta un modelo real para:

```text
code / CIIU / SRI
description
principal yes/no
secondary activities
valid_from
valid_to
is_current
source/provenance
```

No implementar esto dentro de STEP 15.

---

# 19. TaxSubject

`TaxSubject` responde:

> ¿Cómo opera fiscalmente esta identidad dentro de este tenant?

Cadena:

```text
MdmParty PERSON|ORGANIZATION
→ Party tenant
→ TaxSubject
→ SRI Establishment
→ Emission Point
→ Document Sequence
```

Regla cerrada:

```text
PERSON_NATURAL_REQUIRES_ORGANIZATION_ANYWHERE_IN_TAX_CHAIN=NO
```

`organization_id` en partes legacy es contexto opcional, no discriminador fiscal final.

---

# 20. SRI Establishments

Un contribuyente puede tener:

```text
1 matriz
0..N adicionales
```

Persona Natural y Sociedad comparten la misma cadena fiscal.

Ejemplos:

```text
MdmParty PERSON
→ RUC personal
→ TaxSubject
→ Establishment 001
→ Establishment 002
```

```text
MdmParty ORGANIZATION
→ RUC sociedad
→ TaxSubject
→ Establishment 001
→ Establishment 002
```

## 20.1 Gap actual

La auditoría encontró que la BD todavía no impide correctamente ciertas contradicciones, por ejemplo:

- más de una matriz;
- más de un primario vigente;
- vigencias invertidas;
- TaxSubject sobre identificador que no necesariamente sea RUC.

Estas son deudas de la fundación fiscal, no de security membership.

---

# 21. Emission Points y Document Sequences

Cadena tenant-safe:

```text
TaxSubject
→ SRI Establishment
→ EmissionPoint
→ DocumentSequence
```

Preservar:

- establecimiento;
- código de punto;
- tipo documental;
- secuencia;
- vigencia;
- tenant safety.

No mezclar Branch con Establishment.

---

# 22. Representante legal

## 22.1 Regla Owner más reciente

```text
LEGAL_REPRESENTATIVE
= PERSON | ORGANIZATION
```

No asumir Persona únicamente.

Modelo conceptual:

```text
MdmParty ORGANIZATION representada
        │
        └── LEGAL_REPRESENTATIVE
                │
                ├── MdmParty PERSON
                └── MdmParty ORGANIZATION
```

## 22.2 Historia

La base de junio ya incluía `LEGAL_REPRESENTATIVE` dentro de catálogos de relaciones.

## 22.3 Estado actual verificado

Hoy:

- existe relación Party tenant;
- Organization Control la utiliza;
- evidencia oficial SRI puede quedar en JSON;
- todavía no hay un hecho global canónico completo de representación oficial.

## 22.4 Target futuro

Cuando se cierre esta foundation deberá preservar:

- represented party;
- representative party;
- representative kind PERSON|ORGANIZATION;
- relationship type;
- valid_from;
- valid_to;
- current/effective;
- source;
- provenance;
- verification;
- evidence;
- actor;
- audit history.

No diseñar `legal_representative_person_id`.

---

# 23. Organization Control

Reglas aceptadas:

- crear una Organization no convierte al creador automáticamente en OWNER;
- `created_by_user_id` es trazabilidad, no autoridad;
- `organization_access` es acceso/contexto, no permiso;
- `SELF_ATTESTED` no prueba autoridad corporativa;
- password re-entry no prueba autoridad corporativa;
- OWNER de organización debe ser organization-scoped;
- Platform Admin no se convierte silenciosamente en Organization OWNER.

Evidencia SRI de representante legal es una fuente mucho más fuerte que auto-declaración, pero no se debe inventar integración SRI inexistente.

---

# 24. Role / Permission / RBAC

Owner:

```text
gm-security
```

Conceptos:

- Role;
- Permission;
- role_permissions;
- user_roles;
- tenant scope;
- organization scope;
- branch/establishment access where applicable.

Reglas:

```text
Role != Position
Permission != OrganizationAccess
Tenant membership != Role
```

Autorización actual hace unión de permisos de múltiples roles activos.

La arquitectura futura debe preservar:

```text
validated session tenant
→ roles/scopes in that tenant
→ optional active organization
→ effective permissions
```

---

# 25. Platform Admin

```text
Platform Admin
= account-level platform capability
```

No requiere client membership.

Decisión de evolución:

```text
same Global UserAccount
→ tenant-less platform session
→ platform endpoints/capabilities only
```

No crear un segundo sistema de login.

---

# 26. Sesiones y contexto

## 26.1 Estado actual

`user_sessions` hoy:

- requiere tenant;
- copia tenant desde `user_accounts.tenant_id`;
- puede almacenar active organization;
- no valida membership por request.

## 26.2 Target

```text
authenticate Global UserAccount
→ validate ACTIVE membership
→ choose/validate tenant
→ resolve Party by (tenant, mdm_party_id)
→ optional OrganizationAccess
→ roles/permissions
→ issue session
```

Cambio de tenant/contexto:

```text
request switch
→ server validates
→ new session/context
```

No confiar en `tenant_id` crudo del cliente.

## 26.3 Last-used

Decisión:

- derivar inicialmente de sesiones autorizadas recientes;
- revalidar;
- no crear tabla de preferencias todavía.

No depender de PERSONAL/BUSINESS classification.

---

# 27. Personal / Business

IMPORTANTE:

No son membership kinds.

No deben existir en `UserTenantMembership` ni como regla de security.

Un usuario humano puede tener:

```text
MdmParty PERSON
├── perfil personal
├── RUC personal / actividad fiscal
└── relaciones con Organizations
```

Eso no obliga a introducir:

```text
membership_kind = PERSONAL|BUSINESS
```

El significado económico/fiscal lo aportan los dominios reales:

- TaxSubject;
- Organization;
- Employment;
- relationships.

---

# 28. Tenant

Tenant significa:

```text
operational/data isolation workspace
```

No significa automáticamente:

- una Persona;
- una Organization;
- un RUC;
- una membership kind;
- una empresa legal.

Reglas:

```text
Tenant != Organization
Tenant != TaxSubject
Tenant != Person
```

La seguridad debe trabajar sobre acceso validado al tenant, no sobre una inferencia de qué “tipo de negocio” es.

---

# 29. Module ownership

## gm-entities

Posee:

- MdmParty;
- PERSON/ORGANIZATION identity;
- identifiers;
- MDM resolution;
- merge/consolidation;
- Universal Intake;
- global contacts/addresses;
- physical write boundary de ciertos hechos MDM/tax globales;
- Party creation/reuse after resolution.

## gm-security

Posee:

- UserAccount;
- UserTenantMembership;
- OrganizationAccess;
- Role;
- Permission;
- UserRole;
- scopes;
- platform admin security capabilities.

## gm-organizations

Posee:

- organization operational structure;
- branches;
- departments;
- cost centers;
- settings.

## gm-human-resources

Posee:

- Employment;
- Employee;
- Position;
- assignments;
- supervisor;
- workforce lifecycle.

## Fiscal / SRI

Posee semántica de:

- TaxSubject;
- tax rules;
- establishments;
- emission points;
- document sequences;
- fiscal data interpretation.

No escribir MDM global directamente fuera de la frontera aprobada.

## Gystigo Host

Posee orquestación técnica:

- Spring Security;
- controllers;
- sessions;
- filters;
- CORS/CSRF;
- wiring;
- adapters host;
- migrations core.

No debe apropiarse de dominios.

## Módulos operativos

Sales, Purchases, CRM, Accounting, Expenses, Fleets, Fuel Stations, etc.:

- consumen identidades;
- referencian Party/MdmParty cuando corresponda;
- no crean maestros paralelos;
- pueden almacenar snapshots transaccionales cuando la inmutabilidad lo exige.

---

# 30. Module-to-core foreign keys

Regla aprobada:

```text
MODULE_TO_CORE_FK_POLICY
= ALLOWED_WHEN_SEMANTICALLY_STABLE
```

Requisitos:

- tenant-safe;
- ownership respetado;
- no duplicar masters;
- collation compatible;
- no cascadas destructivas cross-owner;
- FK no otorga derecho de escritura.

No eliminar FK solo por “modularidad”.

---

# 31. Collation

Default canónico para nuevo texto general:

```text
utf8mb4_0900_ai_ci
```

Excepciones:

- opaque/binary;
- strict technical identifiers;
- ASCII codes;
- FK textual que requiera compatibilidad exacta.

La identidad fue reconciliada en V50 para eliminar errores de collation en los puntos probados.

No migrar collations masivamente sin STEP dedicado.

---

# 32. Realidad de base de datos — 2026-09-13

## 32.1 Committed

Gystigo HEAD verificado:

```text
dc14e0d539d17a9f72159e5ca7640d733b1b765b
```

Schema committed incluye:

```text
V53
V54
```

## 32.2 Shared DEV

```text
Flyway V43
```

No tiene V44+.

No aplicar V44–V54 a shared DEV sin autorización Owner.

## 32.3 Build limpio

La auditoría descubrió que el path reproducible de instalación limpia es:

```text
B17
→ V18
→ ...
→ current migration
```

No asumir que V1→V17 es el path fresco válido.

---

# 33. Gaps verificados en la auditoría de DB

## Already correct

- MdmParty global;
- RUC como identificador MDM;
- Party tenant con MDM NOT NULL;
- uniqueness tenant+MDM;
- TaxSubject puede ser PERSON u ORGANIZATION;
- SRI chain tenant-safe en schema committed;
- V52 pending/resolved pair;
- V54 one-active-account-per-Golden-Record.

## Partial

- tax facts;
- contact history;
- address history;
- legal representatives;
- natural-person business writer;
- identifiers history;
- global account runtime multi-tenant.

## Missing / insufficient

- economic activities modeled properly;
- tax fact history;
- tax provenance;
- suspension reason;
- global canonical legal-representative fact;
- global/official establishment registry if needed;
- contact/address purpose;
- employment contact points;
- fiscal/SRI writers;
- address writers;
- membership runtime writers before PKG-2A.

## Legacy debt

- `organization_tax_profiles`;
- `party_tax_profiles`;
- old identity structures;
- user_accounts tenant-bound runtime;
- user_accounts party_id;
- duplicate tax/name fields;
- login-email copies into MDM;
- `SOLE_PROPRIETOR` semantics;
- historical direct MDM creation paths outside Intake.

---

# 34. Deuda crítica: MDM creation bypass

La auditoría detectó que no todos los flujos pasan por Intake.

Ejemplos reportados:

- registro sí usa Intake;
- alta administrativa de Persona puede crear MdmParty directamente;
- ciertos participantes de gm-expenses pueden crear directamente;
- creación de Organization puede crear MdmParty directamente;
- Organization puede nacer sin identificador.

Riesgo:

```text
same real-world organization
→ created in two tenants
→ two MdmParty
```

Esto requiere reconciliación futura, no una corrección improvisada dentro de security.

---

# 35. Actor field inventory — regla de preservación

Antes de cualquier migración, buscar todas las variantes:

```text
created_by
updated_by
deleted_by
assigned_by
unassigned_by
granted_by
revoked_by
approved_by
rejected_by
verified_by
reviewed_by
submitted_by
closed_by
opened_by
cancelled_by
activated_by
deactivated_by
suspended_by
reactivated_by
linked_by
merged_by
resolved_by
performed_by
changed_by
actor
operator
source
provenance
reason
session
request
correlation
trace
```

Clasificar cada campo como:

```text
GLOBAL_ACTOR_ACCOUNT
PLATFORM_ACTOR
TENANT_CONTEXT
ORGANIZATION_CONTEXT
ROLE_CONTEXT
SESSION_CONTEXT
DOMAIN_OWNER
LIFECYCLE_ACTOR
PROVENANCE
SOURCE
REASON
TECHNICAL_TRACE
SNAPSHOT
LEGACY
UNKNOWN
```

No mover ni renombrar hasta entender su semántica.

---

# 36. Granularidad — principio de auditoría

GYPPORT debe poder responder, cuando el dominio lo requiera:

```text
WHO
WHAT
WHERE
WHEN
WHY
SOURCE
UNDER_WHICH_CONTEXT
BEFORE
AFTER
REQUEST/CORRELATION
```

No todo módulo necesita todos los campos, pero si ya existen y tienen propósito:

```text
DO NOT SIMPLIFY
DO NOT COLLAPSE
DO NOT DELETE
```

Una aparente redundancia puede ser:

- audit snapshot;
- historical provenance;
- immutable transaction evidence.

No clasificar automáticamente como duplicación.

---

# 37. Soft delete / history

El histórico de junio muestra amplia presencia de:

- `is_active`;
- `deleted_at`;
- `deleted_by_user_id`;
- `valid_from`;
- `valid_to`;
- `is_current`;
- event tables.

Pero no todas las tablas actuales usan el mismo patrón.

Regla:

```text
NO GLOBAL SOFT-DELETE REWRITE WITHOUT DOMAIN AUDIT
```

Cada aggregate debe conservar su semántica de lifecycle.

---

# 38. Immutable snapshots

Un master canónico y un snapshot histórico no son duplicados equivalentes.

Ejemplo:

```text
MdmParty current legal name
!=
invoice issuer name snapshot at issue time
```

Los módulos transaccionales pueden conservar:

- names;
- tax ids;
- address;
- document reference;
- other historically material facts

como snapshot inmutable.

Nunca usar un snapshot como nuevo master.

---

# 39. Security failure rules

Futuro multi-tenant debe fallar cerrado:

- account sin ACTIVE membership;
- tenant solicitado sin membership;
- INVITED;
- SUSPENDED;
- REVOKED;
- Party faltante para identidad resuelta;
- Organization sin access;
- role de otro tenant;
- pending identity en funciones que requieran Party;
- duplicate active account blocked by V54.

Platform Admin es excepción account-level con platform session, no client membership.

---

# 40. Decisiones PKG-2 congeladas hasta aquí

## 40.1 Access grant actual

PKG-2A:

```text
initial membership = ACTIVE
```

Preserva comportamiento actual.

No crear invitation workflow todavía.

## 40.2 Platform Admin

```text
same Global UserAccount
→ tenant-less platform session
```

## 40.3 Personal/Business

No meter clasificación en Security/Membership.

## 40.4 Last-used context

Derivar de sesiones autorizadas, revalidar.

## 40.5 Actor keys

No mover automáticamente actor keys a membership.

Por defecto:

```text
actor → global UserAccount
tenant → context/provenance
```

---

# 41. PKG-2C Knowledge Gate específico

Antes de mover una FK:

```text
TABLE=
COLUMN=
FIELD_SEMANTICS=
FABRIC_EVIDENCE=
ADR_EVIDENCE=
SCHEMA_EVIDENCE=
CODE_USAGE=
CAN_PLATFORM_ADMIN_BE_ACTOR_WITHOUT_MEMBERSHIP=
CURRENT_FK=
RECOMMENDED_TARGET_FK=
WHY=
```

No agrupar 20 FKs solo porque comparten `(tenant_id,user_account_id)`.

---

# 42. Casos canónicos de referencia

## Caso A — Persona humana sin RUC

```text
MdmParty PERSON
├── Cédula/NUI
├── contacts
├── addresses
└── UserAccount
```

## Caso B — Persona Natural con RUC

```text
MdmParty PERSON
├── Cédula
├── RUC
├── Tax Profile
├── Economic Activities
└── TaxSubject
    ├── Establishment 001
    ├── Establishment 002
    └── ...
```

No Organization artificial.

## Caso C — Sociedad

```text
MdmParty ORGANIZATION
├── RUC
├── Tax Profile
├── Economic Activities
└── TaxSubject
    ├── Establishment 001
    └── Establishment 002
```

## Caso D — Persona relacionada con sociedad

```text
MdmParty PERSON
       │
       ├── legal representative / owner / administrator / employment / access
       │
       ▼
MdmParty ORGANIZATION
```

## Caso E — Organización representante legal de otra

```text
MdmParty ORGANIZATION A
       │
       └── LEGAL_REPRESENTATIVE
               │
               ▼
       MdmParty ORGANIZATION B
```

Debe ser representable.

## Caso F — una cuenta, varios tenants

```text
MdmParty PERSON
      ▼
Global UserAccount
      ├── ACTIVE Membership → Tenant A → Party A
      ├── ACTIVE Membership → Tenant B → Party B
      └── ACTIVE Membership → Tenant C → Party C
```

---

# 43. Gobernanza de desarrollo

Flujo preferido:

```text
ONE BOUNDED STEP
→ audit
→ implementation
→ verification
→ Owner review
→ explicit-path staging
→ controlled commit
→ next STEP
```

No:

- `git add .`;
- `git add -A`;
- broad unreviewed migrations;
- shared DEV testing;
- worktree/branch nuevo sin necesidad real y autorización.

Shared DEV protegido.

Tests DB reales:

```text
fresh/disposable MySQL
```

---

# 44. Baseline técnico

Stack actual de referencia:

- Java 25;
- Spring Boot 4.1;
- Maven;
- MySQL 8.4.x para entorno actual/disposable;
- JdbcTemplate en adapters, no en dominio/aplicación;
- React + Vite + TypeScript/Tailwind en frontend;
- SaaS only.

Data Access ADR:

```text
domain/application
→ no JdbcTemplate

JDBC adapter
→ may use JdbcTemplate

DataAccessException
→ must not escape adapter boundary
```

---

# 45. Test debt conocida

Tres fallos preexistentes, no introducidos por STEP 15:

1. `TeamEmployeeRealDatabaseAcceptanceTest:84`;
2. RBAC `createRole` 403;
3. `PersonIdentityReconciliationHttpTest:222` expected 200, actual 403.

No arreglarlos incidentalmente dentro de otro STEP.

---

# 46. Documentos / evidencia revisada para esta consolidación

Este documento fue construido contrastando, entre otros:

## Memoria / arquitectura reciente

- `GYPPORT_MDM_FOUNDATION_MEMORY_2026-09-11.md`;
- ADR-0014 Module-to-Core FK Policy;
- ADR-0015 RUC and Tax Data Homes;
- ADR-0016 Collation;
- ADR-0017 Tax Subject Foundation;
- ADR-0018 Global User Account and Tenant Membership;
- resultados de STEP 14;
- resultados de STEP 15 PKG-1;
- auditoría `GYPPORT_UNIVERSE_DATABASE_CANONICAL_AUDIT`;
- auditoría `PKG_2_RUNTIME_MEMBERSHIP_INTEGRATION_AUDIT`.

## Evidencia histórica

- dump master 2026-06-07;
- snapshot `core_business_dev` 2026-06-10;
- dumps 2026-06-11;
- `Campos_Tributarios_RUCSOCIEDAD.txt`;
- formularios tributarios históricos;
- documentación temprana de Party/MDM/relations.

La evidencia de junio confirma que historial de contactos/direcciones, Party relations y granularidad de auditoría no son ideas recientes.

---

# 47. Qué no debe hacer un agente

Nunca:

1. asumir que `RUC => Organization`;
2. crear Organization falsa para Persona Natural;
3. crear Person/Organization master dentro de CRM/Sales/Purchases/Expenses;
4. auto-merge por nombre/email;
5. crear Party antes de resolver MDM;
6. convertir `UserAccount.email` en contact master;
7. convertir actor global en membership por comodidad;
8. eliminar audit/provenance sin explicar semántica;
9. usar `created_by` como authority;
10. usar `organization_access` como permission;
11. confundir Branch con SRI Establishment;
12. confundir Position con Role;
13. mezclar Employment con Membership;
14. migrar shared DEV sin autorización;
15. reescribir historia para hacerla coincidir con una propuesta nueva.

---

# 48. Qué debe hacer un agente antes de ejecutar un prompt

```text
READ
→ Fabric/Knowledge
→ Universe baseline
→ this document
→ relevant ADRs
→ relevant module ownership docs
→ current STEP checkpoint

VERIFY
→ repo HEAD
→ git status
→ schema/migration head
→ shared DEV version
→ unrelated WIP hashes

AUDIT
→ current code
→ current database
→ existing tests
→ existing actor/history/provenance

THEN
→ execute bounded prompt
```

Si no entiende el propósito original:

```text
STOP_FOR_OWNER_REVIEW=YES
```

---

# 49. Próximas fundaciones después de STEP 15

Orden recomendado sujeto a Owner review:

```text
STEP 15
Global Account + Tenant Membership runtime completion

→ MDM Contact / Address History Foundation
   purpose + provenance + writers

→ Fiscal Identity / Tax Facts Foundation
   RUC writers
   tax history/provenance
   economic activities
   legal representation
   SRI establishments guarantees
   legacy reconciliation

→ operational modules continue on top
```

No convertir esos futuros STEPs en excusa para rediseñar lo que ya está cerrado.

---

# 50. Checkpoint actual

```text
GYPPORT STEP 15
PKG-1
= OWNER_ACCEPTED_COMMITTED_LOCAL

Gystigo HEAD
= dc14e0d539d17a9f72159e5ca7640d733b1b765b

V53
= membership foundation

V54
= one active account per MdmParty

PKG-2 runtime audit
= COMPLETE

Recommended split
= 2A → 2B → 2C → 2D

PKG-2A
= next implementation package

Shared DEV
= V43

Push
= NO
```

---

# 51. Owner review items aún abiertos

Este documento NO debe presentar como cerrados estos temas:

- modelo final de actividades económicas;
- versionado/provenance completo de hechos tributarios;
- enforcement DB de TaxSubject → RUC;
- modelo global final de representante legal;
- representación oficial PERSON|ORGANIZATION con historia;
- global-vs-tenant official establishment registry;
- propósito/provenance completo de contactos/direcciones;
- reconciliación de direct-MDM creation paths hacia Universal Intake;
- retiro destructivo final de `user_accounts.tenant_id` y `party_id`;
- destino definitivo de tablas fiscales legacy;
- catálogo/semántica definitiva de algunos roles históricos.

---

# 52. Regla final

La arquitectura de GYPPORT debe preservar simultáneamente:

```text
IDENTITY
RELATIONSHIP
ACCESS
EMPLOYMENT
FISCALITY
HISTORY
PROVENANCE
AUDITABILITY
TENANT SAFETY
DOMAIN OWNERSHIP
```

Optimizar una de ellas destruyendo las demás no es simplificación válida.

La pregunta de diseño no debe ser:

> ¿Cómo hago menos tablas/campos?

Debe ser:

> ¿Cuál es la verdad de dominio, cuál es su owner, qué contexto la modifica y qué evidencia debemos conservar para poder explicarla años después?

---

# 53. Directiva para Agent Files y `Reglas.md`

Este documento queda Owner-approved como contexto canónico del Universo de Datos
de GYPPORT.

## 53.1 Agent Files

Los archivos:

```text
AGENTS.md
CLAUDE.md
CHATGPT.md
CODEX.md
```

deben obligar a los agentes a:

1. localizar y leer este documento;
2. leer `GYPPORT_UNIVERSE_CANONICAL_BASELINE.md`;
3. leer `Reglas.md` como bitácora histórica acumulativa de decisiones;
4. leer los ADRs y ownership docs del dominio afectado;
5. revisar schema/código/pruebas antes de proponer o ejecutar;
6. distinguir `FACT / OWNER_DECISION / INFERENCE / PROPOSAL`;
7. preservar granularidad de identidad, auditoría y provenance;
8. detenerse ante conflicto mediante el Conflict Gate;
9. ejecutar únicamente el STEP/prompt autorizado;
10. preservar unrelated WIP;
11. dejar un Continuity Packet suficiente al detenerse o cerrar trabajo.

Los Agent Files contienen gobernanza operativa vigente. No sustituyen la
arquitectura canónica detallada que vive en Fabric.

## 53.2 `Reglas.md`

`Reglas.md` es distinto de los Agent Files.

```text
AGENT FILES
→ instrucciones operativas vigentes para agentes

Reglas.md
→ bitácora histórica acumulativa de reglas/decisiones Owner
```

Al actualizar `Reglas.md`:

- conservar el contenido existente;
- añadir nuevas reglas al final;
- no renumerar reglas históricas;
- no borrar reglas sustituidas;
- no reorganizar el documento para hacerlo “más limpio”;
- cuando una regla nueva reemplace una anterior, dejar constancia explícita;
- generar el archivo completo actualizado.

---

**FIN — OWNER-APPROVED CANONICAL CONTEXT**

# GYPPORT — Memoria canónica de esta conversación
**Fecha:** 2026-09-11  
**Propósito:** conservar las conclusiones arquitectónicas y el punto exacto de continuidad antes de iniciar el Universal MDM Intake.

## 1. Regla central

```text
IDENTITY = GLOBAL
RELATIONSHIP / BUSINESS CONTEXT = TENANT
```

- `mdm_party_id` identifica a la Persona u Organización globalmente en GYPPORT.
- `party_id` representa cómo esa identidad participa dentro de un tenant.
- No deben colapsarse.

```text
MdmParty #1000
├── Party Tenant A
├── Party Tenant B
└── Party Tenant C
```

## 2. Ownership canónico

### gm-entities
Posee:
- MDM global.
- Person / Organization como identidad.
- `MdmParty`.
- identificadores globales.
- resolución y consolidación.
- escritura física de MDM.
- futura frontera Universal MDM Intake.
- creación/reutilización de Party tenant después de resolver MDM.

### gm-organizations
Posee estructura organizacional interna:
- branches;
- departments;
- cost centers;
- settings.

Un establecimiento SRI no es automáticamente una Branch.

### gm-human-resources
Posee relación laboral:
- Employee;
- Employment;
- Position;
- assignments;
- supervisor;
- lifecycle.

```text
Person != Employee
Position != Security Role
```

### gm-security
Posee acceso/autorización:
- UserAccount;
- OrganizationAccess;
- Role;
- Permission;
- UserRole;
- scopes.

```text
Person != UserAccount
Employee != UserAccount
```

### Gystigo Host
Solo infraestructura/orquestación:
- Spring Security;
- JWT/session;
- filters/controllers;
- CORS/CSRF;
- wiring/adapters técnicos.

No debe ser propietario del comportamiento de dominio.

---

## 3. Registro rápido: qué idea veníamos construyendo

El Registro Rápido histórico ya contenía la idea de:
- entrar con datos mínimos;
- completar/verificar identidad después;
- mantener información oficial pendiente mientras el usuario avanzaba.

El problema conceptual fue usar MDM demasiado pronto como espacio provisional.

Modelo antiguo aproximado:

```text
Registro rápido
→ datos mínimos
→ MdmParty incompleto
→ Party tenant
→ UserAccount
→ completar identidad después
```

Modelo correcto actual:

```text
Registro rápido
→ Universal MDM Intake / Staging
→ normalización
→ validación
→ matching determinístico
→ resolución
   ├── existing MdmParty
   ├── new MdmParty
   ├── PENDING
   └── CONFLICT
→ Party tenant
```

Conclusión:

```text
ANTES:
datos incompletos → MdmParty incompleto

AHORA:
datos incompletos → Intake/Staging
solo al resolver → MdmParty Golden Record
```

---

## 4. Universal MDM Intake — regla canónica

Todo origen que pueda introducir una Persona u Organización deberá pasar por una frontera reutilizable de Intake.

Fuentes:
- Registro rápido;
- Crear Persona;
- Crear Organización;
- RRHH;
- CRM;
- Ventas;
- Compras;
- SRI;
- Registro Civil;
- integraciones externas.

Flujo:

```text
SOURCE
→ INTAKE / STAGING
→ NORMALIZATION
→ DETERMINISTIC MATCHING
→ VALIDATION
→ MDM RESOLUTION
→ PARTY TENANT PROJECTION
→ BUSINESS RELATIONSHIP
```

El Intake es provisional.  
MDM es canónico.

---

## 5. Party nunca debe ser provisional

La base ya establece:

```text
parties.mdm_party_id = NOT NULL
```

Por tanto:
- no crear Party con `mdm_party_id = NULL`;
- no debilitar esa restricción;
- no inventar un MdmParty falso para satisfacer un flujo incompleto;
- el candidato permanece en Intake hasta resolverse.

---

## 6. user_accounts.mdm_party_id

Semántica:

```text
NULL
= PENDING_GLOBAL_IDENTITY_RESOLUTION

NOT NULL
= GLOBAL_IDENTITY_RESOLVED
```

`NULL` es transitorio, no estado final válido para una identidad ya resuelta.

`user_accounts.party_id` y `user_accounts.mdm_party_id` tampoco son redundantes:
- `party_id` = participación tenant.
- `mdm_party_id` = identidad global.

---

## 7. identity_claims

`identity_claims` es un mecanismo especializado de verificación/reclamación.

No debe convertirse en Universal Staging.

Ejemplo:

```text
Universal Intake
→ identificador coincide con MDM
→ si requiere demostrar identidad
→ IdentityClaim
→ verificación
→ resolución MDM
```

---

## 8. Matching automático inicial

Decisión cerrada:

```text
INITIAL_MDM_MATCHING
= DETERMINISTIC_CANONICAL_IDENTIFIERS_ONLY
```

Ejemplos:
- CÉDULA / NUI;
- RUC;
- PASSPORT;
- otros identificadores oficiales soportados.

```text
NAMES_AS_AUTOMATIC_MATCH_KEY = NO
EMAIL_AS_AUTOMATIC_MATCH_KEY = NO
```

Nombres/emails pueden:
- capturarse;
- conservarse como evidencia;
- mostrarse para revisión;
- participar en revisión asistida/manual futura.

Pero no deben auto-fusionar identidades en el Intake inicial.

---

## 9. Normalización de identificadores

Regla:

```text
normalize
→ trim
→ validate
→ compare
→ persist
```

No se agregó aún un `CHECK` DB de trim.  
Ese refuerzo queda diferido.

---

## 10. Resultados canónicos de resolución

### A. Un identificador resuelve a un MdmParty
Reutilizar ese MdmParty.

### B. Varios identificadores resuelven al mismo MdmParty
Reutilizar ese MdmParty.

### C. Ningún identificador existe y son suficientes/validables
Crear un solo MdmParty y sus identificadores canónicos.

### D. Identificadores resuelven a MdmParty diferentes

```text
CONFLICT
NO automatic merge
NO new MdmParty
NO Party projection
```

### E. No hay identificador determinístico suficiente

```text
PENDING / REQUIRES_VERIFICATION
```

No crear MDM solo por nombre/email.

---

## 11. Idempotencia y concurrencia

Invariante:

```text
same canonical identifier
→ at most one global MdmParty
```

La protección debe combinar:
- unique constraints;
- transacción;
- manejo de colisión en aplicación.

No depender solo de un `SELECT` previo.

La repetición del mismo evento externo tampoco debe crear:
- Intake duplicado;
- MdmParty duplicado;
- Party duplicado.

---

## 12. Persona Natural con RUC

Regla definitiva:

```text
PERSONA NATURAL + RUC
= MdmParty PERSON
```

Nunca:

```text
RUC → Organization
```

Modelo:

```text
MdmParty PERSON
├── CÉDULA / NUI
├── RUC ...001
├── perfil PERSONAL
└── perfil NEGOCIO / TRIBUTARIO
```

---

## 13. Sociedad con RUC

```text
TIPO_CONTRIBUYENTE = SOCIEDAD
→ MdmParty ORGANIZATION
```

---

## 14. Hogares canónicos de datos fiscales

### RUC

```text
RUC
→ mdm_party_identifiers
→ type RUC
```

### Datos oficiales tributarios

```text
mdm_party_tax_profiles
```

### Nombre fiscal observado

`mdm_party_tax_profiles.legal_name` no es otro Golden Record.

Semántica:

```text
OFFICIAL_FISCAL_SOURCE_OBSERVED_NAME
```

La identidad canónica sigue en `mdm_parties`.

---

## 15. Tax Subject universal

Se eliminó la suposición:

```text
negocio tributario = Organization
```

Regla:

```text
TaxSubject
may be PERSON
or ORGANIZATION
```

Cadena:

```text
MdmParty PERSON|ORGANIZATION
→ Party tenant
→ tax_subjects
→ sri_establishments
→ emission_points
→ document_sequences
```

Una Persona Natural con RUC ya no requiere Organization en esa cadena.

---

## 16. Acceso a establecimientos

Modelo:

```text
User
→ tenant
→ establishment
→ tax subject
```

`user_establishments.tax_subject_id` quedó aprobado para:

```text
ONE DEFAULT ESTABLISHMENT
PER USER
PER TAX SUBJECT
```

`organization_id` queda como:

```text
OPTIONAL_LEGACY_CONTEXT
```

---

## 17. Política de FK módulo → core

Regla:

```text
MODULE_TO_CORE_FK_POLICY
= ALLOWED_WHEN_SEMANTICALLY_STABLE
```

La modularidad es ownership de dominio/código, no prohibición de integridad referencial.

Requisitos:
- tenant-safe;
- no violar ownership de escritura;
- no duplicar maestros;
- collation compatible;
- evitar cascadas destructivas entre ownerships.

---

## 18. Tenant-safe FK reconciliation

STEP 08 cerró:

```text
FKS_AUDITED=12
FKS_TENANT_SAFE=12
FKS_UNRESOLVED=0
```

Migraciones:

```text
V45
V46
V47
```

---

## 19. Collation canónica

ADR-0016:

```text
DEFAULT_COLLATION_FOR_NEW_GENERAL_TEXT
= utf8mb4_0900_ai_ci
```

Con excepciones semánticas:
- binary/opaque;
- strict technical identifiers;
- ASCII codes;
- textual FKs con compatibilidad exacta.

---

## 20. V50 — superficie de identidad

STEP 12 comprometió V50.

Resultado:
- 5 columnas de identificadores reconciliadas;
- 2 table defaults reconciliados;
- `ERROR 1267` eliminado en la superficie probada;
- stop-path para impedir colisiones por cambio de collation;
- strict/binary exceptions preservadas.

```text
ERROR_1267_AFTER=0
```

Nombres y emails no bloquean el Intake inicial porque no son matching keys automáticas.

---

## 21. SRI y routing futuro

Modelo futuro:

```text
recipient NUI/CÉDULA
→ PERSONAL context

recipient RUC PERSONA NATURAL
→ BUSINESS/TAX context

recipient RUC SOCIEDAD
→ ORGANIZATION BUSINESS/TAX context
```

Routing del documento y tratamiento tributario son decisiones distintas.

---

## 22. Perfil personal vs negocio

Una Persona Natural puede tener:

```text
Cuenta GYPPORT
├── Personal
└── Mi negocio · RUC ...001
```

Misma identidad, pero contextos económicos segregados.

```text
misma identidad
≠
mismos libros
```

---

# 23. STEPs cerrados y commits

## STEP 08 — Tenant-safe FK reconciliation
**Estado:** `OWNER_ACCEPTED_COMMITTED_LOCAL`

gm-fuel-stations:
```text
8ee330d78149b8f8d0b1886b0d34ac82efc9361b
fix(fuel-stations): enforce tenant-safe fuel product scope
```

Gystigo:
```text
f2dfd5312d646f7d4da56e1a9b94ba6e0dd62cc4
fix(db): enforce tenant-safe cross-module references
```

## STEP 09 — Database canonical foundation reconciliation
**Estado:** `OWNER_ACCEPTED_COMMITTED_LOCAL`

Gystigo:
```text
561e92d734a1e88f0573ae757ddf95a3655c079c
```

gm-entities:
```text
ad500170af94893298aef806d0a24a1e7e40265f
```

gm-organizations:
```text
62f3de4cf6e30b874c2342b1cb864f704293504c
```

Fabric:
```text
e0ba3a01b5fc6d4edd00610c97ce73b6ee768dbf
```

## STEP 10 — Universal Tax Subject Foundation
**Estado:** `OWNER_ACCEPTED_COMMITTED_LOCAL`

Gystigo:
```text
799d2f8cf0f617d2e66472dd0a83312a9f0ba010
feat(fiscal): establish universal tax subject foundation
```

Migraciones:
```text
V48
V49
```

Resultado:

```text
PERSON_NATURAL_REQUIRES_ORGANIZATION_ANYWHERE_IN_TAX_CHAIN=NO
```

## STEP 11 — Fabric history reconciliation
**Estado:** `OWNER_ACCEPTED_RECONCILED_AND_PUSHED`

```text
Fabric main = origin/main
= 1798ac4e657a3d0408d1cea3ee082a97ac203511
```

## STEP 12 — Identity Collation Reconciliation
**Estado:** `OWNER_ACCEPTED_COMMITTED_LOCAL`

Gystigo:
```text
a122ab48fffce69b0b5c1e125d0b84e1d4ac8b9b
fix(identity): reconcile canonical identifier collations
```

Migración:
```text
V50__identity_identifier_collation_reconciliation.sql
```

---

# 24. Shared DEV

```text
DEV_DATABASE=core_business_dev
DEV_FLYWAY_VERSION=43
```

No están aplicadas:

```text
V44
V45
V46
V47
V48
V49
V50
```

No migrar shared DEV sin autorización explícita.

Los tests reales deben usar MySQL descartable.

---

# 25. Próximo STEP

```text
GYPPORT_UNIVERSAL_MDM_INTAKE_FOUNDATION_13
```

Objetivo:

```text
SOURCE
→ INTAKE / STAGING
→ NORMALIZATION
→ DETERMINISTIC MATCHING
→ VALIDATION
→ MDM RESOLUTION
→ PARTY TENANT PROJECTION
```

Debe auditar/reutilizar lo ya existente:
- ShortRegister;
- onboarding;
- identity_claims;
- mdm_identity_claims;
- MdmParty;
- Party;
- UserAccount.

No crear otro sistema paralelo.

---

# 26. Deudas conocidas que NO bloquean STEP 13

1. `PersonIdentityReconciliationHttpTest` tiene una expectativa 200 antigua; existe un 403 preexistente ligado a permisos.
2. Hay identificadores personales o parecidos a reales hardcodeados en pruebas antiguas y `UI_Experiments`.
3. No se agregó todavía `CHECK` DB para trim.
4. Algunos legacy indexes/keys permanecen intencionalmente.
5. Writer operativo de Tax Subject todavía no está implementado.
6. Studio conserva algunos labels/conceptos antiguos, por ejemplo `SOLE_PROPRIETOR`.
7. Nombres/emails podrían requerir reconciliación futura si se usan en matching asistido, pero no bloquean el Intake inicial.

---

# 27. Checkpoint de continuidad

```text
Gystigo HEAD
= a122ab48fffce69b0b5c1e125d0b84e1d4ac8b9b

Fabric main/origin-main
= 1798ac4e657a3d0408d1cea3ee082a97ac203511

gm-entities relevant HEAD
= ad500170af94893298aef806d0a24a1e7e40265f

gm-organizations relevant HEAD
= 62f3de4cf6e30b874c2342b1cb864f704293504c

gm-fuel-stations relevant HEAD
= 8ee330d78149b8f8d0b1886b0d34ac82efc9361b

DEV Flyway
= V43

NEXT_STEP
= GYPPORT_UNIVERSAL_MDM_INTAKE_FOUNDATION_13
```

---

# 28. Regla para futuros agentes

Antes de modificar MDM, registro, identidad, fiscalidad o tenant relationships:

1. leer este documento;
2. leer `GYPPORT_UNIVERSE_CANONICAL_BASELINE.md`;
3. leer ADR-0015, ADR-0016 y ADR-0017;
4. verificar HEADs reales;
5. auditar implementación existente;
6. preservar Golden Record;
7. preservar tenant safety;
8. no usar nombres/emails para auto-merge;
9. no crear Party antes de resolver MDM;
10. no inventar Organization para Persona Natural con RUC;
11. no migrar shared DEV sin autorización;
12. ante conflicto documental o semántico: STOP FOR OWNER.

```text
EXISTING != WRONG
AUDIT BEFORE REBUILD
```

---

# 29. Integración obligatoria con el Universe Baseline

Este documento no debe quedar aislado.

Debe existir una referencia explícita desde:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_UNIVERSE_CANONICAL_BASELINE.md
```

La referencia recomendada es:

```md
## Continuidad MDM / Identity Foundation

Para las decisiones consolidadas de MDM, Universal Intake, TaxSubject,
tenant-safe references, fiscal identity y collation hasta STEP 12, leer:

`GYPPORT_MDM_FOUNDATION_MEMORY_2026-09-11.md`

Este documento complementa el Universe Baseline y debe consultarse antes de
modificar MDM, registro rápido, onboarding, Party, UserAccount, TaxSubject,
SRI identity routing o Universal MDM Intake.
```

## Regla de precedencia

Este documento **no reemplaza** el Universe Baseline.

La precedencia continúa siendo:

```text
Owner explicit decision
→ Universe Baseline / approved ADR
→ canonical domain docs
→ verified implementation / DB
→ continuity memory
→ historical/proposal docs
```

Si una futura decisión Owner modifica algo contenido aquí, este archivo debe
actualizarse o marcarse como parcialmente superseded.

## Ubicación canónica recomendada

```text
Fabric/
└── Knowledge/
    └── 00-GYPPORT-UNIVERSE/
        ├── GYPPORT_UNIVERSE_CANONICAL_BASELINE.md
        └── GYPPORT_MDM_FOUNDATION_MEMORY_2026-09-11.md
```

De esta forma ambos documentos forman el punto de entrada obligatorio para
cualquier agente que trabaje sobre identidad, MDM, onboarding, fiscalidad o
multitenancy.


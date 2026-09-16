# GYPPORT® — Universal MDM
## Memoria canónica de arquitectura, reglas y estado actual

**Fecha:** 2026-09-11  
**Ámbito:** exclusivamente Universal MDM, Identity Intake, resolución, verificación y continuidad  
**Estado:** memoria canónica de trabajo; actualizar al cerrar STEP 13 y STEP 14  
**No reemplaza:** `GYPPORT_UNIVERSE_CANONICAL_BASELINE.md`

---

## 1. Propósito

Este documento consolida únicamente lo definido hasta ahora sobre el **Universal MDM de GYPPORT**.

Debe permitir que cualquier agente futuro entienda sin reconstruir conversaciones:

- qué es el Universal MDM;
- qué problema resuelve;
- cómo entra una Persona u Organización;
- cuándo se reutiliza una identidad existente;
- cuándo una identidad queda pendiente;
- qué papel tienen SRI, Registro Civil y otras fuentes estatales;
- qué datos sirven para matching automático y cuáles solo como evidencia;
- cómo se relacionan `MdmParty`, `Party`, `UserAccount` e `IdentityClaim`;
- qué está implementado y qué sigue pendiente.

---

## 2. Regla central

```text
IDENTITY = GLOBAL
RELATIONSHIP / BUSINESS CONTEXT = TENANT
```

### `MdmParty`
Representa la identidad global única de una Persona u Organización.

### `Party`
Representa la participación de esa identidad dentro de un tenant.

```text
MdmParty #1000
├── Party Tenant A
├── Party Tenant B
└── Party Tenant C
```

Una misma Persona u Organización puede participar en varios tenants sin duplicarse globalmente.

---

## 3. Qué NO es `MdmParty`

`MdmParty` no representa por sí solo:

- Employee;
- UserAccount;
- cliente;
- proveedor;
- responsable;
- propietario;
- contribuyente operativo.

Eso pertenece a relaciones/capacidades construidas sobre la identidad global.

---

## 4. Regla crítica de `Party`

La base establece:

```text
parties.mdm_party_id = NOT NULL
```

Por tanto:

- no crear Party provisional;
- no crear Party con identidad global pendiente;
- no debilitar esta restricción;
- si la identidad aún no está resuelta, permanece en Intake/Staging.

---

## 5. El problema histórico del Registro Rápido

La idea histórica era correcta:

```text
entrar rápido
→ completar identidad después
```

Pero conceptualmente se podía crear MDM demasiado pronto.

Modelo antiguo aproximado:

```text
Registro rápido
→ datos mínimos
→ MdmParty incompleto
→ Party
→ UserAccount
→ completar identidad después
```

Modelo correcto:

```text
Registro rápido
→ Universal MDM Intake / Staging
→ normalización
→ búsqueda
→ verificación
→ resolución
→ MdmParty
→ Party
```

Regla:

```text
DATOS INCOMPLETOS
→ INTAKE / STAGING

IDENTIDAD RESUELTA
→ UNIVERSAL MDM
```

---

## 6. Universal MDM Intake

El Intake es la frontera universal de entrada de identidad.

Fuentes actuales o futuras:

- Registro rápido;
- Crear Persona;
- Crear Organización;
- RRHH;
- CRM;
- Ventas;
- Compras;
- SRI;
- Registro Civil;
- otras integraciones.

Flujo:

```text
SOURCE
→ INTAKE / STAGING
→ NORMALIZATION
→ GYPPORT MDM MATCHING
→ AUTHORITATIVE VERIFICATION WHEN NEEDED
→ MDM RESOLUTION
→ PARTY TENANT PROJECTION
```

El Intake es provisional.  
El MDM es canónico.

---

## 7. Ownership

Owner canónico:

```text
gm-entities
```

`gm-entities` posee:

- Universal Intake semantics;
- normalización;
- matching;
- resolución;
- creación/reutilización de `MdmParty`;
- identificadores globales;
- creación/reutilización de `Party` luego de resolver MDM;
- provenance de identidad.

Otros módulos pueden enviar candidatos, pero no deben escribir directamente en:

```text
mdm_parties
mdm_party_identifiers
mdm_party_tax_profiles
```

---

## 8. Fuente canónica interna y fuentes externas oficiales

Decisión:

```text
GYPPORT UNIVERSAL MDM
= FUENTE CANÓNICA INTERNA DE VERDAD
```

pero solo después de que la información haya sido establecida o verificada suficientemente.

Fuentes externas verificadoras:

```text
SRI
Registro Civil
otras fuentes estatales verificables
```

Relación:

```text
FUENTE OFICIAL EXTERNA
= autoridad de verificación

GYPPORT UNIVERSAL MDM
= fuente canónica interna
  después de verificar/establecer identidad
```

---

## 9. Prioridad de resolución

```text
1. Buscar primero en GYPPORT Universal MDM
2. Si existe match exacto → reutilizar
3. Si no existe → intentar verificación oficial
4. Si se verifica → crear/actualizar MDM
5. Si no puede verificarse → PENDING_VERIFICATION
```

Nunca:

```text
nombre parecido → auto-merge
checksum local → identidad verdadera
formato correcto → Golden Record automático
```

---

## 10. Validación estructural vs verificación real

Regla:

```text
STRUCTURAL_VALIDATION
!=
IDENTITY_VERIFICATION
```

Ejemplos:

### Cédula
Validación local básica:

```text
longitud esperada
tipo de caracteres
forma mínima
```

### RUC
Validación local básica:

```text
13 dígitos numéricos
```

Eso significa:

> “el dato tiene forma suficiente para intentar verificarlo”.

No significa:

> “la identidad es verdadera”.

---

## 11. Checksums locales NO son autoridad

Decisión Owner:

> Universal MDM no debe usar algoritmos locales de cédula o RUC como fuente cierta de identidad.

No tratar como autoridad:

```text
módulo 10
módulo 11
checksum local
provincia inferida
tercer dígito inferido
```

Pueden existir en flujos legacy, pero Universal Intake no los usa como prueba de existencia real.

---

## 12. Match exacto contra MDM existente

Si el identificador ya existe canónicamente:

```text
input
→ normalize
→ mdm_party_identifiers
→ exact match
→ reuse MdmParty
```

No se crea otro MdmParty.

No es necesario consultar fuente externa solo para redescubrir la identidad, salvo futura política de frescura.

---

## 13. Identificador desconocido

Si la cédula/RUC tiene estructura plausible pero no existe en GYPPORT:

```text
NO MDM MATCH
→ PENDING_VERIFICATION
```

Todavía no crear:

```text
MdmParty
Party
```

---

## 14. Fuente gubernamental disponible

```text
usuario ingresa identificador
→ GYPPORT no lo conoce
→ consultar fuente oficial
→ fuente responde
→ contrastar
→ verified
→ crear MdmParty
→ crear Party
```

Ejemplos:

```text
Persona → Registro Civil
Contribuyente/RUC → SRI
```

La integración concreta todavía no está implementada.

---

## 15. Fuente gubernamental no disponible

Decisión cerrada:

```text
NO MDM MATCH
+
NO OFFICIAL VERIFICATION AVAILABLE
=
PENDING_VERIFICATION
```

Aplica cuando:

- SRI cae;
- HTTP 500;
- timeout;
- consulta no autorizada;
- Registro Civil no disponible;
- no existe servicio utilizable.

No se debe:

- crear MdmParty;
- crear Party;
- inventar datos;
- inferir identidad por nombre;
- rechazar definitivamente por una falla técnica externa.

---

## 16. Motivos conceptuales de pendiente

```text
OFFICIAL_SOURCE_UNAVAILABLE
OFFICIAL_SOURCE_TIMEOUT
OFFICIAL_SOURCE_NOT_AUTHORIZED
IDENTIFIER_NOT_FOUND
DATA_MISMATCH
MANUAL_REVIEW_REQUIRED
```

Esto permite diferenciar:

```text
"No pude verificar"
```

de:

```text
"La fuente oficial confirmó que no corresponde"
```

---

## 17. Dato incorrecto + nombre correcto

Ejemplo:

```text
RUC = 1799999999999
Nombre = ISAGRUB CORPORACIÓN C.L.
```

Si el RUC no existe en MDM pero el nombre se parece a una entidad conocida:

```text
NO auto-resolve
NO auto-correct identifier
NO merge by name
```

El nombre puede servir como:

```text
evidence
candidate hint
review assistance
```

Resultado:

```text
PENDING_VERIFICATION
o
DATA_MISMATCH
```

---

## 18. Posible coincidencia durante el ingreso

La UX futura puede ayudar:

```text
RUC: 179...
Posible coincidencia:
ISAGRUB CORPORACIÓN C.L.
```

Pero esta ayuda es:

```text
ADVISORY_ONLY
```

No significa:

```text
IDENTITY_VERIFIED
```

Reglas:

- no revelar registros arbitrarios con prefijos muy cortos;
- preferir match exacto/suficiente;
- en personas usar visualización limitada/masked;
- no confirmar identidad por nombre.

---

## 19. Objetivo UX del Universal MDM

La idea histórica de GYPPORT es:

```text
primera vez
→ más verificación

siguientes veces
→ menos digitación
→ menos duplicados
→ más velocidad
→ mejor UX
```

Ejemplo:

```text
usuario ingresa RUC
→ MDM ya conoce entidad
→ mostrar nombre
→ recuperar datos conocidos
→ evitar reescribir ficha completa
```

---

## 20. Nombres y emails

Decisión:

```text
NAME_AUTOMATCH = NO
EMAIL_AUTOMATCH = NO
```

Pueden servir como:

- atributos;
- evidencia;
- hints;
- candidate search.

No como auto-merge.

---

## 21. Matching automático inicial

```text
INITIAL_MDM_MATCHING
= DETERMINISTIC_CANONICAL_IDENTIFIERS_ONLY
```

Ejemplos:

```text
CEDULA / NUI
RUC
PASSPORT
DNI
otros identificadores oficiales soportados
```

---

## 22. No auto-adjuntar identificadores adicionales

Ejemplo:

```text
CEDULA → match MdmParty X
RUC → desconocido
```

Regla:

```text
AUTO_ATTACH_UNMATCHED_IDENTIFIERS_ON_REUSE = NO
```

El RUC desconocido queda como Intake evidence hasta verificarse.

---

## 23. Identificadores derivados

No promover automáticamente:

```text
RUC first 10 digits
→ canonical CEDULA
```

Como máximo puede existir como:

```text
derived hint
provisional evidence
```

Para ser canónico debe existir previamente en MDM o ser verificado oficialmente.

---

## 24. Provenance

El Universal Intake debe poder responder:

```text
¿Qué ingresó el usuario?
¿De dónde vino?
¿Qué tenant lo envió?
¿Qué identificador original se recibió?
¿Qué se normalizó?
¿Hubo match MDM?
¿Fue necesario verificar?
¿Por qué sigue pendiente?
¿Qué fuente oficial verificó?
¿Cuándo?
¿Qué MdmParty resultó?
¿Qué Party resultó?
```

Datos provisionales no deben contaminar el Golden Record.

---

## 25. Idempotencia

Una repetición del mismo evento externo no debe crear:

```text
duplicate intake
duplicate MdmParty
duplicate Party
```

Modelo:

```text
source namespace
+
source reference
+
same content
→ same result
```

---

## 26. Concurrencia

Invariante:

```text
same canonical identifier
→ at most one global MdmParty
```

Protección:

```text
DB uniqueness
+
transaction
+
application conflict handling
```

No depender solo de un SELECT previo.

---

## 27. Estados conceptuales del Intake

```text
RECEIVED
NORMALIZED
PENDING_VERIFICATION
RESOLVED
CONFLICT
REJECTED
```

Regla importante:

```text
external technical failure
→ PENDING_VERIFICATION
```

No:

```text
external technical failure
→ REJECTED
```

---

## 28. Identity Claims

`identity_claims` queda como:

```text
SPECIALIZED_VERIFICATION_MECHANISM
```

No es Universal Staging.

Puede utilizarse en futuros flujos de reclamación/verificación.

---

## 29. UserAccount pendiente

Modelo objetivo para STEP 14:

```text
PENDING_GLOBAL_IDENTITY_RESOLUTION

user_accounts.party_id = NULL
user_accounts.mdm_party_id = NULL
```

Una vez resuelto:

```text
user_accounts.party_id != NULL
user_accounts.mdm_party_id != NULL
```

Invariantes:

```text
UserAccount tenant = Party tenant
Party.mdm_party_id = UserAccount.mdm_party_id
```

---

## 30. Party sigue siendo estricto

Aunque UserAccount pueda estar pendiente:

```text
parties.mdm_party_id
```

permanece:

```text
NOT NULL
```

No crear Party provisional.

---

## 31. Registro rápido futuro

```text
Usuario crea cuenta
→ UserAccount pending
→ Intake candidate
→ completa datos permitidos
→ verificación pendiente
→ identidad resuelta:
   MdmParty
   Party
   UserAccount linked
```

Esto conserva la experiencia rápida sin contaminar MDM.

---

## 32. Persona Natural con RUC

Regla:

```text
PERSONA NATURAL + RUC
= MdmParty PERSON
```

No crear Organization solo por tener RUC.

Su contexto tributario futuro se expresa mediante:

```text
TaxSubject
```

---

## 33. Organization con RUC

Una sociedad verificada:

```text
MdmParty ORGANIZATION
```

RUC:

```text
mdm_party_identifiers
```

Datos tributarios oficiales reutilizables:

```text
mdm_party_tax_profiles
```

---

## 34. Relación con TaxSubject

Universal MDM responde:

```text
¿Quién es?
```

TaxSubject responde:

```text
¿En qué contexto tributario opera?
```

Cadena:

```text
MdmParty
→ Party tenant
→ TaxSubject
→ SRI Establishment
→ Emission Point
→ Document Sequence
```

---

## 35. Collation de identidad

STEP 12:

```text
TARGET_IDENTITY_COLLATION
= utf8mb4_0900_ai_ci
```

V50 eliminó los `ERROR 1267` conocidos en las superficies de identificadores.

Intake puede comparar:

```text
normalized incoming identifiers
↔ canonical MDM identifiers
```

sin hacks por query.

---

## 36. Implementación actual de STEP 13

Migración:

```text
V51__universal_identity_intake.sql
```

Tablas:

```text
mdm_identity_intakes
mdm_identity_intake_identifiers
```

Owner:

```text
gm-entities
```

Entrada principal:

```text
SubmitIdentityIntakeUseCase
```

Procesamiento interno:

```text
receive
normalize
resolve
```

---

## 37. Principios ya implementados/probados en STEP 13

Hasta antes de la última corrección semántica se probaron:

- new person;
- existing person reuse;
- same MDM across tenants;
- person with RUC;
- organization;
- conflict;
- name/email only;
- idempotency;
- concurrency;
- tenant safety.

Resultado previo:

```text
DUPLICATE_MDM_CREATED=0
DUPLICATE_PARTY_CREATED=0
```

La última ronda debe ajustar el comportamiento para que identificadores nuevos no verificados queden `PENDING_VERIFICATION`.

---

## 38. Shared DEV

```text
core_business_dev
Flyway V43
```

No están aplicadas allí las migraciones V44–V51.

Todas las pruebas de Universal MDM/Intake se realizan en MySQL descartable.

---

## 39. STEPs directamente relacionados

### STEP 08
Tenant-safe FK reconciliation.

### STEP 09
Canonical database foundations.

### STEP 10
Universal Tax Subject Foundation.

### STEP 11
Fabric history reconciliation.

### STEP 12
Identity collation reconciliation.

### STEP 13
Universal MDM Intake Foundation.

Estado actual:

```text
IN PROGRESS
FINAL VERIFICATION SEMANTICS BEING RECONCILED
```

### STEP 14
Próximo:

```text
GYPPORT_PENDING_ACCOUNT_IDENTITY_RECONCILIATION_14
```

Objetivo:

```text
Registro rápido / UserAccount pending
→ Universal Intake
→ resolución
→ MdmParty
→ Party
→ enlazar cuenta
```

---

## 40. Qué todavía NO está implementado

- SRI connector;
- Registro Civil connector;
- verification scheduler/retry;
- manual review UI;
- fuzzy matching;
- AI identity matching;
- full pending→verified UserAccount transition;
- government freshness policy.

---

## 41. Regla de seguridad de identidad

Nunca:

```text
nombre parecido
→ auto-merge

email parecido
→ auto-merge

RUC con 13 dígitos
→ create Golden Record

checksum local válido
→ create Golden Record

fuente oficial caída
→ permanent reject
```

Siempre:

```text
unknown + unverified
→ PENDING_VERIFICATION
```

---

## 42. Arquitectura objetivo

```text
Usuario / módulo
      ↓
identifier
      ↓
GYPPORT Universal MDM
      ↓
EXACT MATCH?
├── YES
│    → reuse identity
│
└── NO
     ↓
authoritative verification
     ↓
verified?
├── YES
│    → create/update MDM
│
└── NO
     → PENDING_VERIFICATION
```

---

## 43. Filosofía del Universal MDM

Universal MDM no existe para acumular datos.

Existe para construir una memoria global, reutilizable y confiable de Personas y Organizaciones.

La primera vez puede requerir más verificación.

Las siguientes veces debe ofrecer:

```text
menos digitación
menos duplicados
mayor consistencia
mayor velocidad
mejor experiencia
```

---

## 44. Definición final de fuente de verdad

```text
Government source
= external authoritative verification source

GYPPORT Universal MDM
= internal canonical source of truth
  after verification/establishment
```

---

## 45. Regla para futuros agentes

Antes de modificar Universal MDM:

1. leer este documento;
2. leer `GYPPORT_UNIVERSE_CANONICAL_BASELINE.md`;
3. leer `GYPPORT_MDM_FOUNDATION_MEMORY_2026-09-11.md`;
4. leer ADR-0015, ADR-0016 y ADR-0017;
5. auditar implementación existente;
6. no crear Party antes de resolver MDM;
7. no auto-merge por nombres/emails;
8. no usar checksum como autoridad;
9. buscar primero match exacto en GYPPORT MDM;
10. si no existe y no puede verificarse: `PENDING_VERIFICATION`;
11. preservar provenance;
12. no migrar shared DEV sin autorización.

```text
EXISTING != WRONG
AUDIT BEFORE REBUILD
```

---

## 46. Continuity checkpoint

```text
Gystigo baseline before STEP 13
= a122ab48fffce69b0b5c1e125d0b84e1d4ac8b9b

Repo Flyway before STEP 13
= V50

STEP 13 migration
= V51__universal_identity_intake.sql

Shared DEV
= V43

CURRENT WORK
= finalize STEP 13 verification semantics

NEXT STEP AFTER STEP 13
= GYPPORT_PENDING_ACCOUNT_IDENTITY_RECONCILIATION_14
```

---

## 47. Frase canónica del Universal MDM

```text
GYPPORT primero busca en su Universo.

Si ya conoce la identidad:
→ la reutiliza.

Si no la conoce:
→ intenta verificarla con una fuente oficial.

Si no puede verificarla:
→ la deja PENDING.

Nunca inventa una identidad.
Nunca fusiona por nombre.
Nunca crea un Golden Record solo porque el formato parece válido.
```

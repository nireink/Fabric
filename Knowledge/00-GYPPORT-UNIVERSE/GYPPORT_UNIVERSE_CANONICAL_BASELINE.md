# GYPPORT® — UNIVERSO CANÓNICO
## Baseline fundacional de arquitectura, identidad, datos, ownership, evolución y UIX

**Estado:** CANÓNICO / OWNER BASELINE  
**Fecha de consolidación:** 2026-09-10  
**Ámbito temporal:** consolidado con el material histórico recuperable más antiguo disponible del proyecto y las decisiones vigentes hasta hoy. No debe reinterpretarse una estructura existente solo porque un agente no encuentre de inmediato su conversación de origen.

---

# 0. Regla superior: NO DESTRUIR Y REHACER

GYPPORT debe evolucionar de forma acumulativa, trazable y controlada.

Antes de crear, eliminar, renombrar, mover, duplicar o sustituir:

- tablas;
- columnas;
- IDs;
- relaciones;
- módulos;
- entidades;
- ownership;
- endpoints;
- conceptos de dominio;
- navegación estructural;

el agente debe demostrar primero:

```text
WHAT_EXISTS_TODAY=
ORIGINAL_PURPOSE=
CANONICAL_OWNER=
GLOBAL_OR_TENANT_SCOPE=
MASTER_OR_OPERATIONAL=
WHO_REFERENCES_IT=
IDS_AND_RELATIONSHIPS_PRESERVED=
HISTORICAL_EVIDENCE_REVIEWED=
```

Si alguna respuesta importante es `UNKNOWN`:

```text
STOP
AUDIT FIRST
DO NOT IMPLEMENT
```

Regla permanente:

> **EXISTING != WRONG**

Una estructura existente no se elimina por parecer redundante, legacy o poco elegante. Primero se debe comprender su semántica original.

---

# 1. Regla fundacional del universo GYPPORT

```text
IDENTITY = GLOBAL
RELATIONSHIP / BUSINESS CONTEXT = TENANT
```

GYPPORT no debe convertir cada empresa cliente en un mundo aislado de copias.

Una Persona u Organización existe una sola vez como identidad global y puede participar en múltiples tenants.

```text
IDENTIDAD GLOBAL
      ↓
MÚLTIPLES PARTICIPACIONES TENANT
      ↓
RELACIONES DE NEGOCIO PROPIAS DE CADA TENANT
```

---

# 2. Master Party / MDM

## 2.1 `mdm_party_id`

`mdm_party_id` representa la identidad global/cross-tenant dentro del universo GYPPORT.

```text
MdmParty
= Master Data Identity
= Golden Record
= identidad global
```

No depende de un tenant.

Responde:

```text
¿QUIÉN ES ESTA PERSONA U ORGANIZACIÓN EN GYPPORT?
```

## 2.2 `party_id`

`party_id` representa la participación/proyección de esa identidad dentro de un tenant.

```text
MdmParty #1000
      │
      ├── Party #10  Tenant A
      ├── Party #42  Tenant B
      └── Party #91  Tenant C
```

Responde:

```text
¿CÓMO PARTICIPA ESTA IDENTIDAD EN ESTE TENANT?
```

Regla canónica:

```text
mdm_party_id = identidad global
party_id     = relación/contexto tenant
```

No sustituir uno por el otro.

---

# 3. MDM Party y Party no son duplicados

Son dos niveles distintos.

```text
MDM_GOLDEN_RECORD
!=
TENANT_PARTY_PROJECTION
```

Por tanto, no debe concluirse que `mdm_party_id` es redundante solo porque una tabla también tenga `party_id`.

Si una tabla concreta contiene ambos campos, se debe auditar su intención antes de normalizarla.

Especialmente para `user_accounts`:

```text
party_id
mdm_party_id
```

NO asumir automáticamente:

```text
party_id = identidad maestra
```

Antes de eliminar cualquier referencia directa a MDM se debe estudiar:

- acceso multi-organización;
- acceso multi-tenant;
- fusiones MDM;
- trazabilidad;
- login/registro;
- referencias de auditoría;
- integridad histórica.

---

# 4. Caso fundacional: Punto de Venta / POS

El Master Party Registry existe también para reducir fricción operacional.

Flujo:

```text
Cliente llega al POS
      ↓
cajero solicita identificación
      ↓
GYPPORT busca primero en el universo global
```

## Caso A — ya existe globalmente y ya existe en el tenant

```text
MdmParty encontrado
Party tenant encontrado
      ↓
usar registro existente
      ↓
confirmar datos actuales
```

## Caso B — existe globalmente pero no en el tenant

```text
MdmParty encontrado
      ↓
autocompletar datos maestros permitidos
      ↓
confirmar/actualizar correo, teléfono, dirección u otros datos
      ↓
crear Party local
      ↓
crear relación comercial necesaria
      ↓
continuar venta
```

## Caso C — no existe globalmente

```text
buscar/validar en fuente disponible
      ↓
crear MdmParty
      ↓
crear Party tenant
      ↓
crear relación comercial
      ↓
continuar venta
```

Regla:

> **Si una Persona u Organización ya existe en el universo GYPPORT, no se vuelve a crear desde cero en cada tenant.**

---

# 5. Datos maestros vs datos privados del tenant

Compartir identidad NO significa compartir información comercial privada.

## Datos candidatos a maestro global

Según dominio, procedencia y privacidad:

- identificación;
- nombres legales;
- apellidos;
- fecha de nacimiento;
- razón social;
- RUC;
- datos oficiales;
- contactos maestros;
- direcciones maestras;
- información tributaria/legal;
- información validada desde fuentes autorizadas.

## Datos tenant-scoped

Ejemplos:

- cupo de crédito;
- descuento;
- clasificación comercial;
- deuda;
- compras;
- comportamiento comercial;
- relación laboral;
- cargo;
- acceso;
- roles y permisos dentro de la organización;
- configuraciones particulares.

---

# 6. Datos cambiantes: nunca borrar historia por comodidad

Correo, teléfono, dirección y otros datos pueden cambiar.

Cuando corresponda, conservar:

```text
valor
vigencia
is_current
fecha de captura
fecha de actualización
fuente/procedencia
quién confirmó
tenant/proceso que aportó el dato
```

El dato nuevo puede convertirse en vigente y el anterior mantenerse como histórico.

Regla:

> **Actualizar no significa destruir el valor anterior cuando el historial aporta valor al MDM, auditoría o autocompletado.**

---

# 7. Identidad propia de conceptos estables

Un concepto maestro/reutilizable debe tener:

```text
identidad canónica
owner canónico
ID estable
referencias estables
ciclo de vida
sin fuente paralela de verdad
```

Ejemplos:

- MdmParty;
- Party;
- Person;
- Organization;
- Employee;
- UserAccount;
- Role;
- Permission;
- Vehicle;
- Department;
- CostCenter;
- Establishment;
- TaxpayerProfile;
- Meter;
- Tank.

Pero:

> **No todo campo constante necesita una tabla o ID independiente.**

Solo crear identidad propia cuando el dominio necesite relaciones, ciclo de vida, historial, reutilización o referencias.

---

# 8. Mapa conceptual de identidades y capacidades

```text
MdmParty
   ↓
Person / Organization
   ↓
Party tenant-scoped
   ├── Customer / Supplier / other commercial roles
   ├── Employee / Employment
   └── UserAccount / OrganizationAccess
```

No confundir:

```text
Person != Employee
Person != UserAccount
Employee != UserAccount
Position != Security Role
Organization != Tenant
Branch != SRI Establishment
```

---

# 9. Fronteras canónicas actuales

## `gm-entities`

```text
QUIÉN EXISTE
```

Responsabilidad:

- MDM / Master Party Registry;
- Party base;
- Person;
- Organization identity;
- identificadores;
- datos maestros;
- resolución/consolidación de identidad;
- relaciones maestras de identidad.

## `gm-organizations`

```text
CÓMO SE ESTRUCTURA UNA ORGANIZACIÓN
```

Responsabilidad:

- estructura organizacional;
- departments;
- cost centers;
- branches;
- settings organizacionales;
- relaciones estructurales;
- componentes operativos de organización según su dominio.

No duplicar Person/Organization master identity.

## `gm-human-resources`

```text
QUIÉN ES EMPLEADO Y CUÁL ES SU RELACIÓN LABORAL
```

Responsabilidad:

- Employee;
- Employment;
- Position;
- estado y lifecycle laboral;
- supervisor;
- asignaciones.

## `gm-security`

```text
QUIÉN PUEDE ENTRAR Y QUÉ PUEDE HACER
```

Responsabilidad:

- UserAccount;
- OrganizationAccess;
- Role;
- Permission;
- UserRole;
- RolePermission;
- Scope;
- authorization policies/query ports.

Security consume identidades; no sustituye MDM ni Party.

## `gm-configurations`

```text
CÓMO SE CONFIGURA GYPPORT
```

Puede componer superficies administrativas reutilizables.

No debe convertirse en un God Module ni apropiarse del dominio de todos los datos que muestra.

## Gystigo

```text
HOST / ORQUESTADOR TÉCNICO
```

Puede conservar:

- Spring Security;
- SecurityFilterChain;
- JWT/session/cookies;
- CORS/CSRF;
- HTTP;
- wiring;
- runtime;
- adapters técnicos.

Infraestructura técnica no equivale a ownership de dominio.

---

# 10. Trazabilidad

Cadena conceptual:

```text
MdmParty
  ↓
Party tenant
  ↓
Person / Organization
  ↓
Employee            si aplica
  ↓
UserAccount         si aplica
  ↓
OrganizationAccess
  ↓
Roles
  ↓
Permissions
  ↓
Scopes
  ↓
Audit Actor
```

Todo refactor debe preservar:

- IDs;
- UUIDs;
- FKs;
- assignments;
- eventos históricos;
- referencias de auditoría.

---

# 11. Persona: maestro y UI

Antes de crear nuevos campos, revisar DB y código real.

Objetivo de UI posible:

```text
Persona
├── Identidad
├── Documento
├── Información civil
├── Contacto
└── Acceso a GYPPORT
```

Clasificar cada campo como:

```text
EXISTING_CANONICAL
EXISTING_NOT_EXPOSED
DERIVABLE_FROM_EXISTING_DATA
MISSING
WRONG_DOMAIN_OWNER
SENSITIVE_REQUIRES_RESTRICTED_UI
```

Datos sensibles no deben hacerse visibles solo porque existan en DB.

---

# 12. Organización: maestro, tributación y UI

Objetivo conceptual:

```text
Organization identity
      ↓
TaxpayerProfile
      ↓
LegalRepresentative
      ↓
TaxEstablishments
```

UI posible:

```text
Organización
├── Información general
├── Configuración tributaria
├── Representante legal
├── Establecimientos
└── Equipo / acceso
```

La pantalla compone información de varios dominios. La ubicación visual no cambia el owner real.

---

# 13. Perfil tributario

Los datos tributarios pertenecen al contribuyente, no a Security.

Puede abarcar:

- RUC;
- razón social/nombre legal;
- estado RUC;
- tipo contribuyente;
- régimen;
- categoría;
- obligado a llevar contabilidad;
- agente de retención;
- contribuyente especial;
- indicadores tributarios;
- actividad económica;
- fechas tributarias;
- representante legal;
- establecimientos.

Cuando el representante legal tenga identidad verificable, preferir referencia a Person/MdmParty frente a texto duplicado.

---

# 14. Establecimientos

Distinguir:

```text
establishmentId
= identidad interna estable

001 / 002 / ...
= código/número oficial del contribuyente
```

Y también:

```text
SRI Establishment
!=
Branch operativa
```

Pueden relacionarse, pero no son automáticamente el mismo concepto.

---

# 15. Ownership lógico vs ubicación física

GYPPORT utiliza Shared Schema multitenant.

Cambiar ownership de código NO significa mover físicamente tablas.

```text
misma tabla
mismos IDs
mismas relaciones
nuevo owner canónico de código
```

Regla:

> **No renombrar, copiar o recrear tablas únicamente para demostrar modularidad.**

---

# 16. Migraciones

Preferir:

```text
ADDITIVE
RECONCILE IN PLACE
PRESERVE IDS
PRESERVE UUIDS
PRESERVE ASSIGNMENTS
PRESERVE AUDIT HISTORY
```

Evitar:

```text
DROP + RECREATE
REGENERATE IDS
COPY INTO PARALLEL SOURCE OF TRUTH
RENAME FOR AESTHETICS
```

Una eliminación física requiere STEP y auditoría específicos.

---

# 17. UIX: modelo mental y modelo futuro

Baseline:

```text
Nivel 1 = Módulo
Nivel 2 = Sección amplia
Nivel 3 = navegación local
```

Diseñar pensando en:

```text
Maestros
Operaciones
Historiales
Configuraciones
Reportes
```

No nombrar una sección principal solo por la única función disponible hoy.

Ejemplo:

```text
Descargas
├── Medidores de descarga
└── Operaciones de descarga
```

La UI definitiva puede evolucionar cuando el Owner diseñe mejor los flujos.

---

# 18. Fuel Stations: ejemplo del principio

```text
Estaciones de combustible
├── Estaciones
│   ├── Puntos receptores
│   └── Tanques receptores
├── Transporte
│   └── Tanqueros
│       ├── Tanque de transporte
│       └── Compartimentos
└── Descargas
    ├── Medidores de descarga
    └── Operaciones de descarga
```

```text
Tanque receptor != Tanque de transporte
```

---

# 19. Fleets: identidad del vehículo

ADN canónico actual:

```text
Plate
Brand
Model
Chassis
Year
```

No convertir correcciones excepcionales de identidad en edición cotidiana.

Para legacy incompleto puede existir `fill-only-if-null`.

---

# 20. Conocimiento obligatorio antes de cualquier STEP

Los agentes deben inspeccionar:

```text
Fabric/Knowledge/
Gystigo/docs/
Modules/<module>/docs/   si existe
```

Flujo:

```text
1. descubrir contenido
2. leer README/índices
3. buscar términos del STEP
4. leer documentación canónica relevante
5. revisar historia/origen cuando una estructura parezca rara o legacy
6. contrastar documentación contra DB/código real
7. detenerse ante contradicciones
```

No es necesario releer recursivamente todo en cada tarea.

Sí es obligatorio descubrir y cargar todo lo materialmente relevante.

---

# 21. Jerarquía de autoridad

Cuando existan contradicciones:

```text
1. decisión explícita actual del Owner
2. baseline/ADR canónico Owner-approved
3. documentación canónica vigente
4. implementación/DB real verificada
5. documentación técnica vigente
6. handoffs
7. propuestas/drafts
8. documentación histórica
```

La historia no domina automáticamente al presente.

Pero una estructura existente no puede eliminarse sin revisar su historia cuando esa historia explica su propósito.

---

# 22. Regla de agentes: ANTI-REBUILD

Antes de tocar una frontera arquitectónica:

```text
DO NOT ASSUME
DO NOT RECREATE
DO NOT DUPLICATE
DO NOT RENAME FOR CLEANLINESS
DO NOT DELETE BECAUSE IT LOOKS LEGACY
```

Primero:

```text
DISCOVER
AUDIT
UNDERSTAND
CLASSIFY
PRESERVE
THEN EVOLVE
```

---

# 23. Gate obligatorio

Todo STEP que toque MDM, Party, identidad, ownership, tablas maestras o arquitectura debe reportar:

```text
GYPPORT_UNIVERSE_GATE

KNOWLEDGE_ROOTS_INSPECTED=YES|NO
ORIGINAL_PURPOSE_UNDERSTOOD=YES|NO
CANONICAL_OWNER_IDENTIFIED=YES|NO
GLOBAL_VS_TENANT_SCOPE_IDENTIFIED=YES|NO
MASTER_VS_OPERATIONAL_IDENTIFIED=YES|NO

MDM_IDENTITY_IMPACT=NONE|ASSESSED
TENANT_PARTY_IMPACT=NONE|ASSESSED

EXISTING_IDS_PRESERVED=YES|NO
EXISTING_UUIDS_PRESERVED=YES|NO
EXISTING_RELATIONSHIPS_PRESERVED=YES|NO
AUDIT_HISTORY_PRESERVED=YES|NO

DUPLICATE_SOURCE_OF_TRUTH_INTRODUCED=NO
DESTRUCTIVE_MIGRATION_REQUIRED=NO|YES_WITH_OWNER_APPROVAL

HISTORICAL_EVIDENCE_REVIEWED=YES|NO
ACTIVE_DOCUMENT_CONFLICTS=0|N

IF ANY REQUIRED ITEM IS NO/UNKNOWN:
STATUS=BLOCKED_FOR_ARCHITECTURE_REVIEW
DO_NOT_IMPLEMENT
```

---

# 24. STEP discipline

```text
ONE STEP
→ ONE BOUNDED INTENT
→ VERIFY
→ OWNER REVIEW
→ CONTROLLED COMMIT
→ NEXT STEP
```

No mezclar en una misma intervención:

- Security extraction;
- MDM redesign;
- HR redesign;
- Organization tax profile;
- UI overhaul;
- technical debt;
- schema cleanup.

---

# 25. Resumen del Universo GYPPORT

```text
MDM / MASTER PARTY
= identidad global / Golden Record

PARTY
= participación tenant-scoped

gm-entities
= quién existe

gm-organizations
= cómo se estructura la organización

gm-human-resources
= relación laboral

gm-security
= acceso y autorización

gm-configurations
= configuración reusable

módulos operativos
= qué ocurre en el negocio

Gystigo
= Host/orquestador técnico

Studio / Mobile / futuras interfaces
= superficies de interacción
```

Regla final:

> **GYPPORT no debe destruir y reconstruir su arquitectura cada vez que aparece una nueva interpretación. Debe descubrir lo ya existente, comprender su propósito original, preservar identidad y trazabilidad, y evolucionar de forma aditiva y controlada.**

---

# 26. Regla mínima para AGENTS / CLAUDE / CHATGPT / CODEX

No copiar este documento completo en cada archivo de agente.

Agregar una regla estable equivalente a:

```text
Before any GYPPORT design, implementation, refactor or architecture change:

1. Inspect Fabric/Knowledge/, Gystigo/docs/, and the relevant Modules/<module>/docs/.
2. Read the canonical Universe baseline and all materially relevant current documents.
3. Search historical documentation when an existing structure appears redundant, legacy, or unclear.
4. Never delete, rename, duplicate, recreate or reassign ownership before understanding the original purpose and proving IDs, tenant boundaries, MDM identity and traceability are preserved.
5. If canonical sources conflict, STOP for Owner review.

Canonical principle:
IDENTITY = GLOBAL
RELATIONSHIP / BUSINESS CONTEXT = TENANT

mdm_party_id = global Master Data identity.
party_id = tenant-scoped participation/projection.
```

---

# 27. Ubicación recomendada

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_UNIVERSE_CANONICAL_BASELINE.md
```

Este archivo debe funcionar como puerta de entrada conceptual a la arquitectura, no como reemplazo de ADRs, ownership matrices o documentación específica de cada módulo.

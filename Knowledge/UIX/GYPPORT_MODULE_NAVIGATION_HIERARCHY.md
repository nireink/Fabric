# GYPPORT MODULE NAVIGATION HIERARCHY

PROJECT=GYPPORT
DOCUMENT_TYPE=CANONICAL_UX_KNOWLEDGE
RULE_ID=GYPPORT_MODULE_NAVIGATION_HIERARCHY
STATUS=OWNER_APPROVED_BASELINE
SCOPE=ALL_CUSTOMER_FACING_OPERATIONAL_AND_ADMINISTRATION_MODULES

RECOMMENDED_PATH=
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\UIX\GYPPORT_MODULE_NAVIGATION_HIERARCHY.md

---

## 1. PURPOSE

GYPPORT must use one consistent navigation mental model across modules so the
sidebar does not grow indefinitely as the product expands.

The user should learn once where things are and preserve that mental model
across GYPPORT.

Canonical hierarchy:

```text
LEVEL_1 = MODULE
LEVEL_2 = SECTION
LEVEL_3 = SUBSECTION / TAB / LOCAL NAVIGATION
```

---

## 2. SIDEBAR RULE

The global/sidebar navigation must not permanently expose every domain entity,
screen, catalog, status, or workflow.

Canonical rule:

```text
MAX_VISIBLE_SIDEBAR_DEPTH=2
```

Level 3 belongs inside the selected page/section as tabs, segmented local
navigation, or another current Studio-approved in-page pattern.

Therefore:

```text
SIDEBAR
Module
└── Section
```

and then:

```text
PAGE
Section
[ Subsection A ] [ Subsection B ] [ Subsection C ]
```

---

## 3. CONSISTENCY RULE

```text
EVERY_MODULE_USES_SAME_NAVIGATION_MODEL=YES
SIDEBAR_SHOULD_NOT_LIST_EVERY_ENTITY=YES
LEVEL_3_RENDERING=IN_PAGE_LOCAL_NAVIGATION
DOMAIN_OWNERSHIP_DOES_NOT_CHANGE_BY_UI_GROUPING=YES
```

Visual composition does not alter backend/domain ownership.

A section may compose data and actions from multiple canonical modules through
Gystigo Host without moving ownership between domains.

---

## 4. ENTITIES REFERENCE

Canonical experience:

```text
Entities
├── Personas
├── Organizaciones
└── Equipo
```

Inside Equipo:

```text
Equipo

[ Empleados ] [ Roles ] [ Permisos ]
```

Ownership remains:

```text
Personas       -> gm-entities
Organizaciones -> gm-organizations
Empleados      -> gm-human-resources
Roles          -> gm-security
Permisos       -> gm-security
```

Do not place Roles and Permisos as permanent sidebar siblings of Equipo in the
final canonical information architecture.

---

## 5. GM-FUEL-STATIONS REFERENCE

Preferred conceptual structure:

```text
Estaciones de combustible
├── Estaciones
├── Transporte
├── Descargas
├── Conciliación
└── Configuración
```

Possible Level 3 examples:

```text
Estaciones
[ Sitios ] [ Tanques ] [ Productos ]
```

```text
Transporte
[ Tanqueros ] [ Compartimientos ]
```

```text
Descargas
[ Operaciones ] [ Tickets ] [ Medidores ] [ Metrología ]
```

```text
Conciliación
[ Resumen ] [ Volumétrica ] [ Financiera ]
```

These are information-architecture examples, not authorization or domain-model
definitions.

Operational people such as conductores, despachadores, receptores or
supervisores should reuse canonical Person / Employee identities where
appropriate instead of creating duplicated human identity masters inside
gm-fuel-stations.

---

## 6. GM-EXPENSES REFERENCE

Preferred conceptual structure:

```text
Gastos
├── Gastos
├── Anticipos
├── Rendiciones
└── Configuración
```

Level 3 may be used only when it improves the workflow.

Examples:

```text
Gastos
[ Registrados ] [ En revisión ] [ Aprobados ] [ Observados ]
```

or, when states work better as filters:

```text
Gastos
└── one canonical list + state filters
```

Do not create navigation tabs merely because an enum/status exists.

---

## 7. GM-FLEETS REFERENCE

Preferred conceptual structure:

```text
Flotas
├── Vehículos
├── Operación
├── Historial
└── Configuración
```

Possible Level 3:

```text
Historial
[ Gastos ] [ Mantenimiento ] [ Repuestos ]
```

Execution of workshop/work-order processes remains outside gm-fleets where the
canonical domain assigns it to another module.

---

## 8. LEVEL-3 DESIGN RULE

A Level-3 item is justified when it represents a stable user task or
sub-area inside a selected section.

Do NOT automatically convert into Level 3:

- every database table
- every aggregate
- every status
- every permission code
- every catalog
- every backend endpoint

Prefer filters, table states, dialogs, drawers, or detail panels when those
produce a simpler mental model.

---

## 9. RESPONSIVE RULE

Level-3 navigation must work on desktop and responsive web.

At narrow widths, tabs/local navigation may become:

- horizontally scrollable tabs when appropriate
- a compact selector
- stacked local navigation

but must not create page-level horizontal overflow.

Canonical responsive target for MVP verification:

```text
390x844
```

---

## 10. SECURITY RULE

Navigation visibility is presentation only.

```text
UI_HIDDEN != SECURITY
```

The backend remains the authority.

Navigation and Level-3 actions should be filtered using effective permissions,
but direct API authorization must remain independently enforced.

---

## 11. PLATFORM ADMIN BOUNDARY

The customer module hierarchy must not merge with the private platform
administration experience.

```text
GYPPORT ADMIN / PLATFORM
!=
CUSTOMER MODULE NAVIGATION
```

Global SaaS administration may use its own clearly distinct navigation model
when required by platform operations.

GYPPORT Support / SupportSession is also a separate future context and must not
be silently represented as ordinary customer membership.

---

## 12. IMPLEMENTATION GOVERNANCE

This document defines the canonical UX hierarchy.

It does not itself enforce runtime behavior.

Implementation should eventually be enforced through:

1. Studio navigation registry conventions.
2. Reusable local-section/tab component conventions.
3. Contract tests for hierarchy and permission filtering.
4. Responsive verification.
5. Module-specific navigation definitions.

Do not hardcode the entire product navigation into one monolithic component.

Prefer registry/config-driven module navigation.

---

## 13. CHANGE CONTROL

Changes to this hierarchy require an explicit UX/product decision when they
would alter the global mental model.

Module teams may define their Level-2 and Level-3 labels within this framework
without redefining the framework itself.

If a module requires deeper navigation than Level 3, first evaluate whether the
problem should instead be represented as:

- detail view
- workflow step
- filter
- nested content panel
- contextual action
- secondary page

before adding another persistent navigation level.

---

## 14. CANONICAL SUMMARY

```text
GYPPORT_MODULE_NAVIGATION_HIERARCHY

LEVEL_1=MODULE
LEVEL_2=SECTION
LEVEL_3=SUBSECTION_OR_LOCAL_NAVIGATION

MAX_VISIBLE_SIDEBAR_DEPTH=2

LEVEL_3_RENDERING=IN_PAGE

EVERY_MODULE_USES_SAME_NAVIGATION_MODEL=YES

SIDEBAR_SHOULD_NOT_LIST_EVERY_ENTITY=YES

DOMAIN_OWNERSHIP_DOES_NOT_CHANGE_BY_UI_GROUPING=YES

BACKEND_SECURITY_AUTHORITY=YES

PLATFORM_ADMIN_NAVIGATION_SEPARATE=YES
```

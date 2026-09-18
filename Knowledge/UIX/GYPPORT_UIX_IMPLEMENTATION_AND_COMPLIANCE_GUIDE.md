# GYPPORT UIX IMPLEMENTATION AND COMPLIANCE GUIDE

PROJECT=GYPPORT  
DOCUMENT_TYPE=CANONICAL_UIX_IMPLEMENTATION_GUIDANCE  
RULE_ID=GYPPORT_UIX_IMPLEMENTATION_AND_COMPLIANCE_GUIDE  
STATUS=OWNER_APPROVED_BASELINE  
REVISION=2026-09-09_MODULE_FIRST_SIDEBAR_AND_STATE_FILTER_STANDARD  
SCOPE=ALL_CUSTOMER_FACING_OPERATIONAL_AND_ADMINISTRATION_MODULES  

RECOMMENDED_PATH=  
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\UIX\GYPPORT_UIX_IMPLEMENTATION_AND_COMPLIANCE_GUIDE.md

---

## 1. PURPOSE

This document does **not** redefine the GYPPORT navigation hierarchy.

The canonical hierarchy already exists in:

```text
Fabric\Knowledge\UIX\GYPPORT_MODULE_NAVIGATION_HIERARCHY.md
```

and remains:

```text
LEVEL_1 = MODULE
LEVEL_2 = SECTION
LEVEL_3 = SUBSECTION / TAB / LOCAL NAVIGATION

MAX_VISIBLE_SIDEBAR_DEPTH = 2
LEVEL_3_RENDERING = IN_PAGE_LOCAL_NAVIGATION
EVERY_MODULE_USES_SAME_NAVIGATION_MODEL = YES
```

This document defines how that approved hierarchy should be **implemented,
reconciled, reviewed, and verified consistently across modules**.

Canonical principle:

```text
DO_NOT_REDESIGN_THE_GLOBAL_UIX_MODEL
APPLY_THE_APPROVED_MODEL
AUDIT_COMPLIANCE
FIX_MODULE_DRIFT
PRESERVE_DOMAIN_OWNERSHIP
```

---

## 2. STATUS OF THE GLOBAL UIX MODEL

The global UIX navigation model is already defined and Owner-approved.

Therefore:

```text
GLOBAL_UIX_NAVIGATION_DESIGN=COMPLETE
GLOBAL_UIX_NAVIGATION_REDESIGN_REQUIRED=NO
GLOBAL_UIX_COMPLIANCE_REQUIRED=YES
```

Future module work must not open a new architecture discussion for:

```text
Level 1
Level 2
Level 3
sidebar depth
local navigation placement
responsive Level-3 behavior
UI-hidden vs backend-security separation
```

unless a real contradiction with the approved Knowledge baseline is proven.

---

## 3. REFERENCE IMPLEMENTATION — ENTITIES / EQUIPO

Entities is the first major reference implementation of the global hierarchy.

Canonical experience:

```text
Entidades
├── Personas
├── Organizaciones
└── Equipo
```

Inside Equipo:

```text
Equipo

[ Empleados ] [ Roles ] [ Permisos ]
```

Canonical ownership remains:

```text
Personas       -> gm-entities
Organizaciones -> gm-organizations
Empleados      -> gm-human-resources
Roles          -> gm-security
Permisos       -> gm-security
```

Important:

```text
UI_GROUPING_DOES_NOT_CHANGE_DOMAIN_OWNERSHIP=YES
```

Entities should be used as a **reference implementation**, not as a new
definition of the global rule.

---

## 4. PRODUCT-WIDE COMPLIANCE OBJECTIVE

Every customer-facing module should be reconciled against the same mental model:

```text
GYPPORT
│
├── LEVEL 1
│   MODULE
│
├── LEVEL 2
│   FUNCTIONAL SECTION
│
└── LEVEL 3
    SUBSECTION / TAB / LOCAL NAVIGATION
```

The user should be able to move between modules while preserving the same
interaction logic.

Desired product perception:

```text
"Different function, same GYPPORT."
```

### 4.1. Visible sidebar root = real module

For ordinary customer-facing modules, the visible Level-1 sidebar root should be
the **real module name**, not a generic umbrella such as `Operación`.

Canonical clarification:

```text
SIDEBAR_LEVEL_1_VISIBLE_ROOT=MODULE_NAME
GENERIC_OPERATION_UMBRELLA_AS_NAV_PARENT=NO
GENERIC_ADMINISTRATION_UMBRELLA_AS_NAV_PARENT=NO
```

Reason:

```text
"Operación" is too broad to teach, document, search, or remember reliably.
Almost every business process is an operation.
The module name carries the useful business meaning.
```

Preferred instruction model:

```text
Ventas → Comprobantes → Retención
Gastos → Anticipos
Flotas → Vehículos
Estaciones de combustible → Descargas → Medidores
```

Avoid:

```text
Operación → Ventas → Comprobantes → Retención
Operación → Gastos → Anticipos
```

The sidebar should therefore expose:

```text
Ventas
├── <sections>

Compras
├── <sections>

Catálogo
├── <sections>

Gastos
├── Gastos
├── Anticipos
├── Rendiciones
└── Configuración

Flotas
├── Vehículos
├── Operación
├── Historial
└── Configuración

Estaciones de combustible
├── Estaciones
├── Transporte
├── Descargas
├── Conciliación
└── Configuración

Entidades
├── Personas
├── Organizaciones
└── Equipo
```

Important distinction:

```text
GLOBAL_GENERIC_OPERATION_GROUP=NO
MODULE_INTERNAL_SECTION_NAMED_OPERATION=ALLOWED_WHEN_BUSINESS_MEANINGFUL
```

For example:

```text
Flotas → Operación
```

may be valid because `Operación` is a specific functional section **inside the
Flotas module**.

This rule does not remove the Level-1 / Level-2 / Level-3 model. It makes the
existing model visible and teachable:

```text
LEVEL_1 = MODULE NAME
LEVEL_2 = MODULE FUNCTION / SECTION
LEVEL_3 = SUBSECTION / TAB / LOCAL NAVIGATION
```

---


## 5. MODULE COMPLIANCE RULE

For each module, verify:

```text
MODULE_HAS_CLEAR_LEVEL_1=YES
SIDEBAR_LEVEL_1_LABEL_IS_REAL_MODULE_NAME=YES
GENERIC_OPERATION_OR_ADMINISTRATION_PARENT_USED=NO
LEVEL_2_REPRESENTS_STABLE_USER_AREAS=YES
LEVEL_3_USED_ONLY_WHEN_NEEDED=YES
SIDEBAR_DEPTH_GREATER_THAN_2=NO
LEVEL_3_RENDERED_IN_PAGE=YES
DOMAIN_TABLES_NOT_EXPOSED_AS_NAVIGATION_BY_DEFAULT=YES
STATUS_ENUMS_NOT_AUTOMATICALLY_TABS=YES
SECURITY_NOT_DELEGATED_TO_NAV_VISIBILITY=YES
RESPONSIVE_LOCAL_NAVIGATION=YES
```

A module is not compliant merely because it uses tabs.

The hierarchy must represent stable user tasks and mental groupings.

---

## 6. LEVEL-2 DESIGN RULE

A Level-2 section should represent a stable functional area.

Good examples:

```text
Gastos
├── Gastos
├── Anticipos
├── Rendiciones
└── Configuración
```

```text
Flotas
├── Vehículos
├── Operación
├── Historial
└── Configuración
```

```text
Estaciones de combustible
├── Estaciones
├── Transporte
├── Descargas
├── Conciliación
└── Configuración
```

Avoid Level-2 entries that are merely:

```text
database tables
technical aggregates
individual statuses
permission codes
API resources
implementation details
```

---

## 7. LEVEL-3 DESIGN RULE

Level 3 is justified when it helps the user navigate a stable sub-area inside a
selected Level-2 section.

Examples:

```text
Equipo
[ Empleados ] [ Roles ] [ Permisos ]
```

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
Historial
[ Gastos ] [ Mantenimiento ] [ Repuestos ]
```

Do not create Level 3 merely because the backend exposes multiple entities or
statuses.

Prefer instead:

```text
filters
detail panels
drawers
dialogs
workflow steps
state chips
contextual actions
```

when they preserve a simpler mental model.

---

## 8. LIST PAGE STANDARD

Operational and administration list pages should converge on a common GYPPORT
pattern.

Recommended structure:

```text
PAGE HEADER
├── section identity
├── concise context
└── primary action when authorized

LOCAL NAVIGATION (Level 3 when applicable)

FILTER / SEARCH AREA

DATA AREA
├── canonical columns
├── status
├── relevant context
└── row actions

EMPTY / LOADING / ERROR STATES
```

Guidelines:

```text
ONE_PRIMARY_ACTION_PER_PAGE_WHEN_POSSIBLE=YES
ROW_ACTIONS_CONTEXTUAL=YES
TECHNICAL_IDS_AS_PRIMARY_COLUMNS=NO
PERMISSION_CODES_AS_PRIMARY_BUSINESS_LABELS=NO
EXCESSIVE_COLUMN_FILTERS=NO
ENUM_TO_TAB_AUTOMATION=NO
```

---

## 9. DETAIL PAGE STANDARD

Detail pages should preserve a predictable structure across modules.

Recommended pattern:

```text
DETAIL HEADER
├── identity
├── current state
├── key context
└── authorized actions

IN-PAGE SECTIONS / TABS
├── General
├── domain-specific information
├── relationships
├── history
└── access / configuration where applicable
```

The exact labels remain module-specific.

Avoid turning every attribute into a separate screen.

---

## 10. EDIT AND ACTION STANDARD

Canonical action behavior:

```text
VIEW_ACTION
→ available when the user can read

EDIT_ACTION
→ available only when the user can manage

DESTRUCTIVE_OR_IRREVERSIBLE_ACTION
→ explicit confirmation

SECURITY_OR_ACCESS_ACTION
→ explain exactly what changes
→ explain what does NOT change when relevant
```

Use real accessible buttons and approved iconography.

Avoid ambiguous text glyphs such as:

```text
✎
⋮
```

when a canonical icon component exists.

---

## 11. LOCAL NAVIGATION VS STATE FILTERS

GYPPORT must distinguish **navigation hierarchy** from **operational state
filtering**.

Example in Expenses:

```text
LOCAL NAVIGATION / FUNCTIONAL SUBLEVEL
[ Expedientes ] [ Gastos ] [ Anticipos ] [ Reportes ]

STATE FILTERS
[ Todos ] [ Registrado ] [ En revisión ] [ Observado ] [ Aprobado ] [ Rechazado ]
```

These controls may share the same visual family so GYPPORT feels homogeneous,
but they do not have the same semantic role.

Canonical:

```text
LOCAL_NAVIGATION_ROLE=NAVIGATION
STATE_FILTER_ROLE=SECONDARY_OPERATIONAL_FILTER

STATE_FILTER_IS_PRIMARY_CTA=NO
STATE_FILTER_IS_LEVEL_3_BY_DEFAULT=NO
STATUS_ENUM_AUTOMATICALLY_BECOMES_NAVIGATION=NO
```

Do not convert a status enum into navigation merely to reuse a visual style.

---

## 12. GYPPORT STATE FILTER VISUAL STANDARD

State filters must be quiet, precise, and visually subordinate to primary
actions and module navigation.

A saturated cyan/turquoise filled active state must not be used for ordinary
list-state filters.

Canonical:

```text
SATURATED_TURQUOISE_STATE_FILTER_ACTIVE=NO
SOFT_GYPPORT_STATE_FILTER_STYLE=YES
```

Approved visual family:

```text
STATE_FILTER_ACTIVE_BACKGROUND=#EAF1FD
STATE_FILTER_ACTIVE_TEXT=#06204D
STATE_FILTER_ACTIVE_BORDER=#29A9E0

STATE_FILTER_INACTIVE_BACKGROUND=#FFFFFF
STATE_FILTER_INACTIVE_TEXT=#64748B
STATE_FILTER_INACTIVE_BORDER=#E2E8F0

STATE_FILTER_HOVER_BACKGROUND=#F8FAFC
STATE_FILTER_HOVER_TEXT=#06204D
STATE_FILTER_HOVER_BORDER=#CFE0F5
```

Where design-system tokens already represent these values, implementations must
consume the token rather than duplicate raw values.

The active filter should be clearly identifiable without looking like a primary
CTA.

Recommended characteristics:

```text
ACTIVE_FILL=SOFT
ACTIVE_BORDER=VISIBLE_BUT_QUIET
ACTIVE_TEXT=BRAND_PRIMARY
ACTIVE_FONT_WEIGHT=SEMIBOLD_OR_EXISTING_EQUIVALENT
SHADOW=NONE_OR_EXISTING_QUIET_PATTERN
```

The style should visually harmonize with the approved local-navigation family
used by GYPPORT sections such as the Expenses sublevel, while preserving the
different semantic role.

Example target:

```text
Expenses local navigation:
[ Expedientes ] [ Gastos ] [ Anticipos ] [ Reportes ]

Expenses state filters:
[ Todos ] [ Registrado ] [ En revisión ] [ Observado ] [ Aprobado ] [ Rechazado ]
```

Both should feel like the same product, but state filters must have lower visual
priority than the module/section navigation.

---

## 13. STATE FILTER INTERACTION STANDARD

For a single-select state-filter set:

```text
ONE_EFFECTIVE_FILTER_AT_A_TIME=YES
ALL_FILTER_OPTION_ALLOWED=YES_WHEN_BUSINESS_LIST_SUPPORTS_IT
ACTIVE_STATE_VISIBLE_WITHOUT_COLOR_ALONE=YES
KEYBOARD_ACCESSIBLE=YES
FOCUS_VISIBLE=YES
```

Preserve the current accessible control semantics when they are already
correct.

If a new accessibility pattern is required, prefer the smallest standard
single-select pattern supported by the existing component system.

Do not invent a new design-system primitive merely to complete one module.
If no suitable shared pattern exists and a new reusable primitive is required:

```text
OWNER_DECISION_REQUIRED_NOW
```

State filters should normally alter the current list/query/filter state, not
create new permanent sidebar entries.

Responsive behavior:

```text
390x844
PAGE_HORIZONTAL_OVERFLOW=NO
FILTERS_REMAIN_REACHABLE=YES
```

When the row cannot fit:

```text
horizontal scroll inside the filter control area
OR
an existing compact responsive filter pattern
```

is acceptable, provided the page itself does not overflow horizontally.

---

## 14. PERMISSION-AWARE UX

Canonical:

```text
UI_HIDDEN != SECURITY
```

Frontend:

```text
FILTER_VISIBILITY_BY_EFFECTIVE_PERMISSION=YES
SHOW_READ_ONLY_AFFORDANCE_WHEN_APPROPRIATE=YES
```

Backend:

```text
AUTHORIZE_INDEPENDENTLY=YES
USE_EXACT_DOMAIN_SCOPE=YES
```

A hidden action must never be the security boundary.

---

## 15. RESPONSIVE STANDARD

The same information architecture must survive narrow screens.

Canonical MVP verification target:

```text
390x844
```

Level-3 navigation may become:

```text
horizontal scroll tabs
compact selector
stacked local navigation
```

provided:

```text
PAGE_HORIZONTAL_OVERFLOW=NO
SECOND_MOBILE_INFORMATION_ARCHITECTURE=NO
CORE_ACTIONS_REMAIN_REACHABLE=YES
```

Mobile is a responsive/adaptive form of the same React application and API.

---

## 16. TRAINING, DOCUMENTATION, AND SUPPORT LANGUAGE

Navigation labels must support human instructions.

Preferred syntax:

```text
<Módulo> → <Sección> → <Subsección/Tab>
```

Examples:

```text
Ventas → Comprobantes → Retención
Gastos → Rendiciones
Entidades → Equipo → Roles
Estaciones de combustible → Descargas → Metrología
```

Avoid instructions that require a generic shell bucket first:

```text
Operación → ...
Administración → ...
```

Canonical:

```text
TRAINING_PATH_STARTS_WITH_MODULE=YES
DOCUMENTATION_PATH_STARTS_WITH_MODULE=YES
SUPPORT_PATH_STARTS_WITH_MODULE=YES
```

This improves learnability, support communication, product documentation, and
future AI-guided instructions because the first navigation term identifies the
actual business module.

---

## 17. MODULE-SPECIFIC RECONCILIATION TARGETS

### 13.1 gm-expenses

Preferred Level-2:

```text
Gastos
├── Gastos
├── Anticipos
├── Rendiciones
└── Configuración
```

Possible Level-3 should be evaluated based on user workflow.

Do not automatically create tabs for:

```text
REGISTRADO
PENDIENTE_REVISION
APROBADO
OBSERVADO
RECHAZADO
```

Use filters when one canonical list is simpler.

---

### 13.2 gm-fleets

Preferred Level-2:

```text
Flotas
├── Vehículos
├── Operación
├── Historial
└── Configuración
```

Possible Level-3:

```text
Historial
[ Gastos ] [ Mantenimiento ] [ Repuestos ]
```

Workshop / work-order execution remains outside gm-fleets when domain ownership
assigns it to `gm-service-management`.

---

### 13.3 gm-fuel-stations

Preferred Level-2:

```text
Estaciones de combustible
├── Estaciones
├── Transporte
├── Descargas
├── Conciliación
└── Configuración
```

Possible Level-3:

```text
Estaciones
[ Sitios ] [ Tanques ] [ Productos ]

Transporte
[ Tanqueros ] [ Compartimientos ]

Descargas
[ Operaciones ] [ Tickets ] [ Medidores ] [ Metrología ]

Conciliación
[ Resumen ] [ Volumétrica ] [ Financiera ]
```

This is information architecture only.

It must not redefine the gm-fuel-stations domain model.

---

## 18. PERSONAS AND ORGANIZACIONES

Their Level-2 location inside Entities is already defined.

Future UIX work should focus on **internal experience compliance**, not relocation.

Audit areas:

```text
Personas
├── list
├── detail
├── relationships
├── Organization context
├── actions
└── states

Organizaciones
├── list
├── detail
├── configuration
├── establishments
├── branches
├── departments
├── cost centers
└── administration actions
```

Do not reopen:

```text
Entities placement
Level-1 hierarchy
Equipo composition
```

without explicit Owner decision.

---

## 19. PLATFORM / CUSTOMER BOUNDARY

Canonical:

```text
GYPPORT_PLATFORM_ADMIN
!=
CUSTOMER_MODULE_NAVIGATION
```

Likewise:

```text
GYPPORT_CONSULTING_EXPERIENCE
!=
CUSTOMER_OPERATIONAL_DASHBOARD

GYPPORT_SUPPORT_SESSION
!=
ORDINARY_CUSTOMER_MEMBERSHIP
```

These contexts may require distinct navigation behavior.

They must not be silently inserted into the ordinary customer module hierarchy.

---

## 20. IMPLEMENTATION ENFORCEMENT

The global navigation hierarchy should be reinforced through:

```text
Studio navigation registry conventions
reusable local navigation component/pattern
contract tests
permission-filter tests
responsive verification
module-specific navigation definitions
```

Prefer:

```text
REGISTRY_DRIVEN_NAVIGATION=YES
```

Avoid:

```text
ONE_MONOLITHIC_HARDCODED_PRODUCT_NAVIGATION_COMPONENT=YES
```

---

## 21. COMPLIANCE AUDIT FORMAT

For each module, produce:

```text
MODULE=
STATUS=COMPLIANT|PARTIAL|NON_COMPLIANT

LEVEL_1=
LEVEL_2=
LEVEL_3=

SIDEBAR_DEPTH=
LOCAL_NAVIGATION_PATTERN=
RESPONSIVE_VERIFIED=
PERMISSION_FILTERING=
BACKEND_SECURITY_INDEPENDENT=

STATE_FILTER_PATTERN=NOT_APPLICABLE|COMPLIANT|DRIFT
SATURATED_STATE_FILTER_ACTIVE=YES|NO
STATE_FILTER_RESPONSIVE_VERIFIED=YES|NO|NOT_APPLICABLE

DRIFT_FOUND=
FIX_REQUIRED=
OWNER_DECISION_REQUIRED=

UNRESOLVED_IN_SCOPE_FINDINGS=
```

A module may be marked COMPLIANT only when:

```text
UNRESOLVED_IN_SCOPE_FINDINGS=0
```

---

## 22. AI EXECUTION GOVERNANCE

Substantial UIX implementation/audit STEPs must also apply:

```text
GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE.md
GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES.md
GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY.md
GYPPORT_MODULE_NAVIGATION_HIERARCHY.md
```

Canonical execution:

```text
AUDIT_TARGETED_FIRST
→ IMPLEMENT APPROVED MODEL
→ TARGETED TESTS
→ FINAL VERIFICATION
→ OWNER ACCEPTANCE
```

Unexpected finding:

```text
BOUNDED DIAGNOSIS
→ STOP
→ OWNER DECISION
```

After the Owner decides and the resolution is clear:

```text
RESOLVE_NOW
```

Do not silently repair.

Do not vaguely defer.

---

## 23. RECOMMENDED UIX ROADMAP

```text
1. ENTITIES / EQUIPO
   → final reconciliation
   → FINAL OWNER ACCEPTANCE

2. GLOBAL UIX CANON
   → already defined
   → OWNER_APPROVED_BASELINE
   → NO REDESIGN

3. MODULE COMPLIANCE
   → gm-expenses
   → gm-fleets
   → gm-fuel-stations
   → Personas internal experience
   → Organizaciones internal experience
   → remaining MVP modules

4. GLOBAL UIX COMPLIANCE AUDIT

5. MVP_OPERATIVE_UIX_BASELINE
   → OWNER ACCEPTED

6. VPS
```

Do not open a new global navigation-design track unless a genuine conflict with
the canonical baseline is proven.

---

## 24. SUGGESTED TRACK NAMING

Prefer:

```text
GYPPORT_GLOBAL_UIX_NAVIGATION_COMPLIANCE
```

or module-specific tracks such as:

```text
GYPPORT_EXPENSES_UIX_COMPLIANCE
GYPPORT_FLEETS_UIX_COMPLIANCE
GYPPORT_FUEL_STATIONS_UIX_COMPLIANCE
```

Avoid:

```text
GYPPORT_GLOBAL_UIX_NAVIGATION_REDESIGN
```

unless the Owner explicitly authorizes a redesign.

---

## 25. CHANGE CONTROL

This guide complements but does not replace:

```text
GYPPORT_MODULE_NAVIGATION_HIERARCHY.md
```

If this guide conflicts with that canonical hierarchy:

```text
GYPPORT_MODULE_NAVIGATION_HIERARCHY.md
WINS
```

Changes to the global mental model require explicit Owner approval.

Module teams may refine Level-2 and Level-3 labels inside the approved framework
without redefining the framework itself.

---

## 26. CANONICAL SUMMARY

```text
GYPPORT_UIX_IMPLEMENTATION_AND_COMPLIANCE_GUIDE

GLOBAL_UIX_NAVIGATION_MODEL_ALREADY_DEFINED=YES
GLOBAL_UIX_REDESIGN_REQUIRED=NO

LEVEL_1=MODULE
LEVEL_2=SECTION
LEVEL_3=SUBSECTION_OR_LOCAL_NAVIGATION
MAX_VISIBLE_SIDEBAR_DEPTH=2
LEVEL_3_RENDERING=IN_PAGE

SIDEBAR_LEVEL_1_VISIBLE_ROOT=MODULE_NAME
GENERIC_OPERATION_UMBRELLA_AS_NAV_PARENT=NO
GENERIC_ADMINISTRATION_UMBRELLA_AS_NAV_PARENT=NO
TRAINING_PATH_STARTS_WITH_MODULE=YES

STATE_FILTER_ROLE=SECONDARY_OPERATIONAL_FILTER
SATURATED_TURQUOISE_STATE_FILTER_ACTIVE=NO
SOFT_GYPPORT_STATE_FILTER_STYLE=YES
STATE_FILTER_ACTIVE_BACKGROUND=#EAF1FD
STATE_FILTER_ACTIVE_TEXT=#06204D
STATE_FILTER_ACTIVE_BORDER=#29A9E0

ENTITIES=REFERENCE_IMPLEMENTATION

NEXT_PRODUCT_TASK=
APPLY_AND_AUDIT_COMPLIANCE

MODULES_SHARE_ONE_MENTAL_MODEL=YES
DOMAIN_OWNERSHIP_PRESERVED=YES
UI_HIDDEN_IS_NOT_SECURITY=YES
RESPONSIVE_USES_SAME_INFORMATION_ARCHITECTURE=YES

GLOBAL_COMPLIANCE_AUDIT_BEFORE_MVP_UIX_FREEZE=YES

MVP_OPERATIVE_UIX_BASELINE
→ OWNER_ACCEPTED
→ VPS
```

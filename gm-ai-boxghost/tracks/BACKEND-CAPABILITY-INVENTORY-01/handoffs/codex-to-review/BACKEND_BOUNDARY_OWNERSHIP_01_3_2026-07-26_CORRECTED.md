# BACKEND_BOUNDARY_OWNERSHIP_01_3_2026-07-26

## 1. Baseline Git y delta relevante

```text
REPOSITORY_ROOT=D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo
BRANCH=master
HEAD=595f0d4 refactor(database): extract canonical database assets
STEP_01_2_HEAD=595f0d4
BASELINE_DELTA=NONE
STAGED_CHANGES=NONE
UNSTAGED_CHANGES=NONE
```

Untracked permitido:

```text
DATABASE_EXTRACTION_SCOPE_AUDIT_2026-07-26.md
```

No hubo drift desde `01.2`. No se repitieron `01.1` ni `01.2`.

## 2. Entradas normativas y fe de erratas

Entradas aplicadas:

```text
STEP_01_1=ACCEPTED_WITH_DOCUMENTARY_LABEL_CORRECTIONS
STEP_01_2=ACCEPTED_WITH_CONSOLIDATED_ERRATA
READY_FOR_STEP_01_3=YES
```

Estado oficial consolidado de este STEP:

```text
STEP_01_3_ANALYSIS=COMPLETE
STEP_01_3_AUDIT=ACCEPTED_WITH_ADDITIONAL_ERRATA
STEP_01_3_DOCUMENTARY_CORRECTION=APPLIED
STEP_01_3_STATUS=COMPLETE_PENDING_ARCHITECTURE_DECISION
READY_FOR_FINAL_ARCHITECTURE_APPROVAL=NO
```

La nota anterior que describía `01.3` como `PAUSADO` y afirmaba que no se había ejecutado queda **sustituida** por este estado oficial. Esa nota correspondía a un momento anterior a la recepción y revisión del informe completo; no representa el estado actual del STEP.

Normalización aplicada:

```text
BLOCKS_01_3
→ MUST_BE_RESOLVED_DURING_01_3
```

Separación Tenant:

```text
CM-01A
CAPABILITY=TENANT_PROVISIONING
CURRENT_BACKEND_ENDPOINT=/auth/register-short
CONNECTION_STATUS=BACKEND_OBSOLETE
```

```text
CM-01B
CAPABILITY=ACTIVE_TENANT_RESOLUTION_DURING_AUTHENTICATION
CURRENT_BACKEND_ENDPOINT=/auth/login
CONNECTION_STATUS=BACKEND_PROVISIONAL
```

Owners que permanecen inicialmente indeterminados:

```text
CAP-02_PARTY_MDM_CANDIDATE_OWNER=UNDETERMINED
ORGANIZATION_CANDIDATE_OWNER=UNDETERMINED
BRANCH_CANDIDATE_OWNER=UNDETERMINED
ESTABLISHMENT_CANDIDATE_OWNER=UNDETERMINED
```

Corrección mantenida:

```text
FILE=UserAccountJdbcRepository.java
CLASSIFICATION=REUTILIZABLE
ISSUE=Username lookup is not tenant-scoped
ACTION=ADAPT_LATER
```

## 3. Método de separación entre evidencia, recomendación y decisión

Se aplican tres niveles independientes:

```text
CURRENT_IMPLEMENTATION_LOCATION
→ hecho verificable del repositorio

RECOMMENDED_ARCHITECTURAL_OWNER
→ recomendación basada en dependencias y reglas vigentes

FINAL_APPROVED_OWNER
→ decisión exclusiva de ChatGPT Work / Architecture Owner
```

Estados utilizados:

- `EVIDENCE_CONFIRMED`: ubicación, dependencia o comportamiento estático demostrado.
- `ARCHITECTURAL_RECOMMENDATION`: owner recomendado, todavía no aprobado.
- `REQUIRES_CHATGPT_DECISION`: la evidencia no permite cerrar el owner.
- `CONFLICTED_BY_EVIDENCE`: existen implementaciones o fuentes de verdad incompatibles.

```text
FINAL_APPROVED_OWNER=NONE
```

## 4. Mapa general de responsabilidades

Cada fila agrupa todos los campos exigidos: ubicación, state owner, source of truth, scope, callers, dependencias, endpoint, owner actual/recomendado, contrato, evidencia y pregunta pendiente.

| BOUNDARY_ID / RESPONSIBILITY | Implementación, estado y scope actuales | Callers, dependencias y endpoint | CURRENT_OWNER → RECOMMENDED_OWNER | CONTRACT / STATUS | Evidencia, rationale y pregunta no resuelta |
|---|---|---|---|---|---|
| BND-01 `TENANT_PROVISIONING` | `AuthController.registerShort` y `TenantJdbcRepository`; DB pretendida; scope global de creación Tenant | ShortRegisterView → authService; `/auth/register-short` | UNDETERMINED → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | Provisioning crea el límite tenant, pero el SQL actual es obsoleto. ¿Es provisioning una capacidad central o un producto/onboarding separado? |
| BND-02 `ACTIVE_TENANT_CONTEXT` | `/auth/login` devuelve tenant; `RuntimeContext` lo conserva en memoria; scope usuario | LoginPage, App, StudioShell, DashboardHost | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | El contexto cruza backend/frontend. ¿Cómo se selecciona tenant antes de autenticar username? |
| BND-03 `AUTHENTICATION` | AuthController, authService y LoginPage; backend + frontend memory; scope usuario | LoginPage; UserAccountJdbcRepository; `/auth/login` | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | Seguridad global no debe pertenecer a un módulo externo. Falta decisión de protocolo/sesión. |
| BND-04 `SESSION_CONTEXT` | `user_sessions` existe en V1 y `RuntimeContext.session` existe, pero ningún flujo los usa | Sin caller productivo; endpoint `NONE` | UNDETERMINED → PLATFORM_OS_CORE | YES / REQUIRES_CHATGPT_DECISION | Existe estructura, no implementación. ¿Cuál es el modelo oficial de sesión? |
| BND-05 `USER_ACCOUNTS` | `UserAccountJdbcRepository` + `user_accounts`; estado DB; scope tenant/usuario | AuthController; `/auth/login` indirecto | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | Identidad de acceso es transversal; lookup username no tenant-scoped. |
| BND-06 `RBAC_AND_SCOPES` | Tablas V1 + permission gates frontend; estado real dividido; scope tenant/user/scope | DashboardHost consume permiso fijo; endpoint directo `NONE` | UNDETERMINED → PLATFORM_OS_CORE | YES / REQUIRES_CHATGPT_DECISION | Schema no equivale a enforcement. Falta fuente de roles, permisos y scopes. |
| BND-07 `MDM_GOLDEN_RECORD` | `mdm_parties` y tablas MDM en V1; sin writer backend actual; scope global/cross-tenant | AdminProfileRepository intenta leer MDM con SQL obsoleto | UNDETERMINED → UNDETERMINED | YES / REQUIRES_CHATGPT_DECISION | No tiene `tenant_id`; no debe asignarse automáticamente a Commercial. ¿Qué owner gobierna identidad maestra global? |
| BND-08 `TENANT_PARTY_PROJECTION` | `parties` contiene `tenant_id` + `mdm_party_id`; legacy Party repository incompatible | PartyService/AuthController legacy; endpoint `NONE` | UNDETERMINED → UNDETERMINED | YES / REQUIRES_CHATGPT_DECISION | Es una relación tenant-scoped con identidad global. ¿Es Platform core, shared business foundation u otro owner? |
| BND-09 `ORGANIZATION_CONTEXT` | `organizations` enlaza tenant y MDM; RuntimeContext tiene company pero login no la llena | AdminProfile chain obsoleta; `/api/admin/profile` | UNDETERMINED → UNDETERMINED | YES / REQUIRES_CHATGPT_DECISION | Organization pertenece al tenant, pero combina contexto operativo y semántica empresarial. |
| BND-10 `BRANCH_CONTEXT` | `branches` pertenece a tenant+organization; no contexto runtime efectivo | AdminProfile query obsoleta; endpoint efectivo `NONE` | UNDETERMINED → UNDETERMINED | YES / REQUIRES_CHATGPT_DECISION | Branch es unidad operativa y también scope potencial. |
| BND-11 `ESTABLISHMENT_CONTEXT` | `sri_establishments` depende de tax profile; `user_establishments` relaciona usuario | Sin backend consumidor; endpoint `NONE` | UNDETERMINED → UNDETERMINED | YES / REQUIRES_CHATGPT_DECISION | Es unidad tributaria, no Branch. Falta decidir owner de contexto frente a dominio fiscal. |
| BND-12 `CATALOGS` | Tablas globales/tenant y `CatalogDomain` frontend; source dividido | Commercial declara CatalogDomain; endpoint `NONE` | UNDETERMINED → UNDETERMINED | YES / REQUIRES_CHATGPT_DECISION | Algunos catálogos son globales y otros tenant-scoped. |
| BND-13 `AUDIT` | `audit_logs`, `security_logs` y metadata DB; sin writers backend | Sin callers productivos; endpoint `NONE` | UNDETERMINED → UNDETERMINED | YES / REQUIRES_CHATGPT_DECISION | Persistencia parece infraestructura, política/eventos son transversales. Requiere separación adicional. |
| BND-14 `MODULE_CATALOG` | `installedPlugins.js`, `PackageRepository`, `permissionEngine.MODULES={}` | StudioBootstrap y managers | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / CONFLICTED_BY_EVIDENCE | Hay más de un catálogo y uno está vacío. ¿Cuál es el catálogo operativo? |
| BND-15 `MODULE_INSTALLATION` | PluginManager/PluginInstaller/DomainManager/FeatureManager; memoria global | StudioBootstrap; sin backend | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | Los módulos declaran; Platform instala. |
| BND-16 `INSTALLED_MODULE_STATE` | PluginManager Map, PackageManager Map, KernelContext y RuntimeContext | Bootstrap, Kernel, RuntimeState | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / CONFLICTED_BY_EVIDENCE | Múltiples fuentes no equivalentes; ninguna persistente. |
| BND-17 `FEATURE_ACTIVATION` | FeatureContext `activeFeature`; memoria global | `activateFeature` sin caller productivo | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | Falta decidir semántica y scope tenant/global. |
| BND-18 `WORKSPACE_DISCOVERY` | WorkspaceRegistry Map; global | FeatureManager y StudioBootstrap; endpoint `NONE` | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | El owner permanece central; módulos solo deberían publicar definiciones. |
| BND-19 `DASHBOARD_DISCOVERY` | DashboardRegistry Map; global | FeatureManager, DashboardRuntime/Host | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | Discovery central con contrato compartido. |
| BND-20 `WIDGET_DISCOVERY` | WidgetRegistry Map; global | FeatureManager y CompositionResolver | PLATFORM_OS_CORE → PLATFORM_OS_CORE | YES / ARCHITECTURAL_RECOMMENDATION | El módulo declara widgets; no debe mutar registry directamente. |
| BND-21 `NAVIGATION_COMPOSITION` | NavigationRegistry y `StudioShell.navigationGroups` son fuentes paralelas | FeatureManager, NavigationResolver y Shell | UNDETERMINED → PLATFORM_OS_CORE | YES / CONFLICTED_BY_EVIDENCE | Debe existir un owner central, pero la shell actual lo evita. |
| BND-22 `APPLICATION_HEALTH` | Backend Docker TCP healthcheck; sin health semántico Spring | Docker Compose; endpoint `NONE` | PLATFORM_OS_INFRASTRUCTURE → PLATFORM_OS_INFRASTRUCTURE | YES / ARCHITECTURAL_RECOMMENDATION | Abrir 8080 no prueba aplicación ni DB. |
| BND-23 `DATABASE_INFRASTRUCTURE` | compose, datasource, MySQL, V1/V2; scope environment | Spring backend y Docker | PLATFORM_OS_INFRASTRUCTURE → PLATFORM_OS_INFRASTRUCTURE | NO / EVIDENCE_CONFIRMED | Infraestructura técnica claramente separada del dominio. |
| BND-24 `COMMERCIAL_BUSINESS_CAPABILITY` | `module/commercial`: plugin, domains, features, workspace, dashboard y widgets | PluginInstaller/FeatureManager consumen declaraciones | EXTERNAL_BUSINESS_MODULE → EXTERNAL_BUSINESS_MODULE | YES / EVIDENCE_CONFIRMED | Commercial declara capacidades sin modificar owners centrales. |

## 5. Frontera Platform OS ↔ módulos externos

| PRODUCER → CONSUMER | RESPONSIBILITY | CURRENT_DEPENDENCY_DIRECTION | RECOMMENDED_DEPENDENCY_DIRECTION | BOUNDARY_RELATION | DIRECT_INTERNAL_ACCESS | CONTRACT NEEDED | VIOLATION | EVIDENCE |
|---|---|---|---|---|---|---|---|---|
| CommercialPlugin → PluginManager | Declarar plugin/domains | Core consume objeto del módulo | Módulo publica declaración; Core consume | DECLARES | NO | YES | NO | `installedPlugins`, PluginManager |
| Commercial feature → FeatureManager | Declarar capabilities | Feature importa builders/framework internos | Módulo consume API compartida; Core instala | DECLARES | YES | YES | UNDETERMINED | Imports `@framework/*`, `@core/ui` |
| FeatureManager → registries | Registrar capabilities | Core modifica registries | Debe mantenerse | OWNS | NO | NO | NO | `installFeatureCapabilities` |
| Commercial → WorkspaceRegistry | Workspace | No acceso directo | Declaración → manager → registry | DECLARES | NO | YES | NO | BusinessPartnerProfileFeature |
| Commercial → DashboardRegistry | Dashboard | No acceso directo | Declaración → manager → registry | DECLARES | NO | YES | NO | CommercialDashboard |
| Commercial → WidgetRegistry | Widgets | No acceso directo | Declaración → manager → registry | DECLARES | NO | YES | NO | Commercial widgets |
| Commercial → NavigationRegistry | Navegación | No acceso directo | Declaración → manager → registry | DECLARES | NO | YES | NO | Feature navigation |
| Commercial → PermissionRegistry | Permisos requeridos | Declara strings; manager registra | Debe declarar, no conceder | DECLARES | NO | YES | NO | `commercial.*` permissions |
| Shell → DashboardHost/core runtime | Renderizado | Channel importa APIs internas | Channel consume contrato público de runtime | CONSUMES | YES | YES | UNDETERMINED | DashboardHost imports `@core` |
| Party frontend → backend | Party operations | `partyService` y fetch directos divergentes | Módulo consume contrato compartido | CONSUMES | NO | YES | YES | partyService y Party pages |
| authService → backend | Autenticación | Shell conoce endpoints backend | Shell consume contrato auth compartido | CONSUMES | NO | YES | UNDETERMINED | authService/LoginPage |
| StudioShell → navegación | Composición visible | Shell conserva catálogo paralelo | Shell consume navegación publicada por Core | CONFIGURES | YES | YES | YES | `navigationGroups` |
| PluginManager/PackageManager/Kernel | Installed plugin state | Varias fuentes en memoria | Un owner publica snapshots | PERSISTS | YES | YES | YES | Maps y KernelContext |
| Módulo externo → Kernel/Toolchain | Lifecycle interno | No dependencia encontrada | Prohibido | CONSUMES | NO | NO | NO | Búsqueda de imports/mutaciones |

Un módulo externo debería poder:

- declarar plugin, domains, features y capacidades;
- declarar permisos requeridos;
- publicar definiciones de workspace, dashboard, widget y navegación;
- consumir contratos compartidos;
- implementar su semántica empresarial dentro de su módulo.

No debería poder:

- registrar directamente en registries centrales;
- controlar PluginManager, Kernel o Toolchain;
- conceder permisos globales;
- establecer tenant o usuario global;
- conservar estado de otros módulos;
- seleccionar la fuente de verdad del lifecycle;
- modificar seguridad global;
- controlar navegación ajena.

## 6. Party/MDM, Party tenant-scoped y Commercial

### MDM golden record

Evidencia SQL:

```text
mdm_parties
- mdm_party_id
- mdm_party_uuid
- datos maestros de persona/organización
- NO tenant_id
```

Características confirmadas:

- identidad global/cross-tenant;
- contactos, direcciones, identificadores, perfiles fiscales y merge logs asociados;
- no existe writer backend actual;
- AdminProfileRepository intenta leerlo con SQL incompatible.

```text
CURRENT_OWNER=UNDETERMINED
RECOMMENDED_OWNER=UNDETERMINED
DECISION_STATUS=REQUIRES_CHATGPT_DECISION
```

### Party tenant-scoped

```text
parties
- party_id
- party_uuid
- tenant_id
- mdm_party_id
- tenant_display_name
- status_id
```

La combinación única es:

```text
tenant_id + mdm_party_id
```

Representa la relación de una identidad global con un tenant. Sus roles, relaciones, consentimientos y tax profiles son tenant-scoped.

```text
CURRENT_OWNER=UNDETERMINED
RECOMMENDED_OWNER=UNDETERMINED
DECISION_STATUS=REQUIRES_CHATGPT_DECISION
```

### Commercial Business Partner

Commercial declara features sobre Business Partner, pero no contiene ni controla el golden record MDM.

```text
COMMERCIAL_BUSINESS_PARTNER
→ semántica comercial
→ capabilities y UI declarativas
→ EXTERNAL_BUSINESS_MODULE
```

```text
MDM_GOLDEN_RECORD
!= TENANT_PARTY_PROJECTION
!= COMMERCIAL_BUSINESS_PARTNER
```

### Dependencias confirmadas

- `user_accounts` depende de `tenant_id` y `party_id`; `mdm_party_id` es opcional.
- `employees` depende de Party, Tenant y Organization.
- `organizations` depende de Tenant y MDM.
- `party_roles` expresa roles tenant-scoped.
- `supplier_profiles` amplía una Party; no crea otra identidad.
- Commercial consume conceptos Business Partner, pero no demuestra ownership de MDM ni Party base.

Riesgo:

> Asignar todo Party/MDM a Commercial acoplaría identidad global, autenticación, employees, organizations y otros futuros dominios a un único módulo comercial.

## 7. Tenant, Organization y jerarquía de scope

### Jerarquía confirmada

```text
Tenant
├── Organization
│   ├── Organization Settings
│   ├── Organization Tax Profiles
│   │   └── SRI Establishments
│   ├── Branches
│   ├── Departments
│   └── Cost Centers
└── User Account
    ├── User Roles
    │   └── Role Scopes
    ├── User Branches
    ├── User Establishments
    └── User Sessions
```

### Significado y almacenamiento

| Nivel | Evidencia | Scope confirmado | Relación con auth/RBAC | Owner final |
|---|---|---|---|---|
| Tenant | `tenants`, `user_accounts.tenant_id` | Límite SaaS principal | Login devuelve tenant desde account | REQUIRES_CHATGPT_DECISION |
| Organization | `organizations.tenant_id` | Dentro del tenant | No llega al runtime actual | UNDETERMINED |
| Branch | tenant + organization | Unidad operativa | `user_branches` existe; no se aplica | UNDETERMINED |
| Establishment | organization tax profile | Unidad tributaria | `user_establishments` existe; no se aplica | UNDETERMINED |
| Department | tenant + organization | Estructura organizacional | Puede aparecer en `role_scopes`; no se aplica | UNDETERMINED |
| User | `user_accounts` | Una cuenta pertenece a un tenant | Fuente actual de tenant login | PLATFORM_OS_CORE recomendado |
| Role | `roles.tenant_id` | Rol por tenant | No consultado en login | PLATFORM_OS_CORE recomendado |
| Scope | `role_scopes(scope_type,scope_id)` | Polimórfico | No enforcement backend actual | PLATFORM_OS_CORE recomendado |

### Contradicciones y límites

- Branch no equivale a SRI Establishment.
- Departments pertenecen a Organization, no a Branch.
- Organization está dentro del tenant, pero RuntimeContext mantiene `company` separado y el login no lo llena.
- `role_scopes` documenta Tenant, Organization, Branch, Establishment y Department, pero el schema no impone FK polimórfica sobre `scope_id`.
- `user_branches` y `user_establishments` existen, pero el backend no los consulta.
- Una `user_account` pertenece directamente a un solo tenant.
- La evidencia no confirma si una persona puede operar varios tenants mediante varias cuentas.
- La restricción global `uk_user_accounts_email_address(email_address)` dificulta múltiples cuentas por tenant con el mismo email, aunque además exista unique tenant+email.

## 8. Lifecycle modular

| Etapa | Owner/source actual | Scope / persistencia | Caller productivo | Contrato | Owner recomendado | Hallazgo |
|---|---|---|---|---|---|---|
| MODULE_DECLARATION | `installedPlugins.js`, CommercialPlugin | Global/static | StudioBootstrap | YES | PLATFORM_OS_CORE para catálogo; módulo declara | Solo Commercial |
| MODULE_AVAILABILITY | Archivo app composition | Global/static | StudioBootstrap | YES | PLATFORM_OS_CORE | No entitlement |
| MODULE_INSTALLATION | PluginManager/Installer | Global/memory | StudioBootstrap | YES | PLATFORM_OS_CORE | No persistencia |
| MODULE_ACTIVATION | Package enable/disable y Kernel enabled plugins | Global/memory | Flujo productivo divergente | YES | PLATFORM_OS_CORE | Semántica duplicada |
| FEATURE_ACTIVATION | FeatureContext | Global/memory | Ningún caller de `activateFeature` | YES | PLATFORM_OS_CORE | Instalación no equivale formalmente a activación |
| CAPABILITY_DISCOVERY | Registries | Global/memory | Managers/runtime | YES | PLATFORM_OS_CORE | No backend |
| WORKSPACE_REGISTRATION | WorkspaceRegistry | Global/memory | FeatureManager | YES | PLATFORM_OS_CORE | Sin tenant/permisos |
| DASHBOARD_REGISTRATION | DashboardRegistry | Global/memory | FeatureManager | YES | PLATFORM_OS_CORE | Autorización posterior |
| WIDGET_REGISTRATION | WidgetRegistry | Global/memory | FeatureManager | YES | PLATFORM_OS_CORE | Datasource no resuelto |
| NAVIGATION_COMPOSITION | NavigationRegistry + StudioShell static | Global/memory/static | FeatureManager y Shell | YES | PLATFORM_OS_CORE | Dos fuentes |
| TENANT_ENTITLEMENT | No implementado | Ninguno | Ninguno | YES | PLATFORM_OS_CORE recomendado | Ausente |
| USER_AUTHORIZATION | Backend permiso fijo + RuntimeContext | Usuario/memory | LoginPage/DashboardHost | YES | PLATFORM_OS_CORE | Provisional |
| STATE_PERSISTENCE | No existe | Ninguna | Ninguno | YES | UNDETERMINED | Falta decidir qué persiste |

### Fuentes divergentes

Plugins/módulos instalados:

1. `installedPlugins.js`: plugins disponibles.
2. `PluginManager.installedPlugins`: recibos de instalación.
3. `PackageManager.installedPackages`: packages habilitados.
4. `KernelContext.activePlugins`: plugins activos del Kernel.
5. `RuntimeContext.plugins`: sincronizado desde PackageManager.

Conflicto confirmado:

```text
StudioBootstrap instala mediante PluginManager.
RuntimeState sincroniza plugins desde PackageManager.
Kernel mantiene su propia colección activePlugins.
```

Features activas:

- `FeatureContext.activeFeature`.
- Ningún caller productivo de `activateFeature`.

Workspaces:

- WorkspaceRegistry es catálogo.
- RuntimeWorkspace es estado activo.
- No existe entitlement tenant.

Navegación:

- NavigationRegistry contiene definiciones.
- StudioShell contiene la navegación realmente visible.

```text
LIFECYCLE_SOURCE_OF_TRUTH=CONFLICTED_BY_EVIDENCE
```

## 9. Sesión, RBAC y navegación

```text
AUTHENTICATION_PRESENT=YES
SESSION_CONTEXT_PRESENT=NO
RBAC_DATA_PRESENT=SCHEMA_CONFIRMED
RBAC_ENFORCEMENT_PRESENT=NO
NAVIGATION_PERMISSION_FILTERING_PRESENT=NO
```

### Autenticación

- `/auth/login` verifica BCrypt.
- Lee `user_accounts`.
- Actualiza éxito/fallo.
- Devuelve actor, tenant y permiso fijo.
- No selecciona tenant antes de buscar username.

### Sesión

- `user_sessions` existe en V1.
- RuntimeContext tiene campo `session`.
- Login no crea sesión.
- No devuelve JWT.
- No devuelve refresh token.
- No establece cookie observable.
- El contexto desaparece al recargar.

### RBAC

- V1 contiene roles, permissions, role_permissions, user_roles y role_scopes.
- Login no consulta ninguna de esas tablas.
- DashboardHost comprueba permisos del RuntimeContext.
- El permiso procede de `List.of("commercial.dashboard.view")`.
- Ese gate es autorización provisional, no enforcement RBAC.

### Navegación

- La feature Commercial declara permisos de navegación.
- NavigationRegistry conserva esas declaraciones.
- NavigationResolver filtra por enabled/workspace, no por permisos.
- StudioShell no usa NavigationResolver.
- La navegación visible está hardcodeada.

### Riesgo inter-tenant

Confirmado como condición estructural, no como exposición runtime demostrada:

- username no tenant-scoped;
- registries globales;
- lifecycle global;
- workspace seleccionado antes de identidad;
- permiso Commercial fijo;
- ausencia de scopes;
- datasources futuros sin frontera tenant-scoped definida.

## 10. Ownership de datos

| Datos | SCHEMA_OWNER actual | WRITE_OWNER actual | READ_CONSUMERS actuales | SECURITY_SCOPE_OWNER actual | LIFECYCLE_OWNER actual |
|---|---|---|---|---|---|
| `tenants` | `database/core/migration/V1` | TenantJdbcRepository obsoleto | AdminProfile obsoleto; login vía account | No enforcement | Provisioning indeterminado |
| `user_accounts` | V1 | UserAccountJdbcRepository actualiza login; no creator vigente | AuthController | AuthController provisional | PLATFORM_OS_CORE recomendado |
| Roles/scopes | V1 | Ninguno | Admin query obsoleta para role; resto ninguno | No enforcement | UNDETERMINED |
| MDM | V1 | Ninguno | AdminProfile query obsoleta | Cross-tenant no implementado | UNDETERMINED |
| Parties | V1 | PartyJdbcRepository obsoleto | Party service/repository obsoletos | Tenant scope no aplicado | UNDETERMINED |
| Organizations | V1 | Ninguno | AdminProfile obsoleto | No context/enforcement | UNDETERMINED |
| Branches | V1 | Ninguno | AdminProfile obsoleto | Tablas user_branches no consumidas | UNDETERMINED |
| Establishments | V1 | Ninguno | Ninguno | user_establishments no consumida | UNDETERMINED |
| Installed modules | No tabla | PluginManager/PackageManager memory | Bootstrap/Runtime | Sin tenant scope | CONFLICTED |
| Active features | No tabla | FeatureContext memory | Ningún consumidor productivo | Sin tenant scope | PLATFORM_OS_CORE recomendado |
| Audit | V1 | Ninguno | Ninguno | No owner efectivo | UNDETERMINED |

La ubicación en V1 no asigna el owner semántico. `database/core` representa el schema canónico, no convierte a infraestructura en owner de cada negocio.

## 11. Resolución basada en evidencia de preguntas heredadas

### 11.1 Stack Java/Spring Boot

```text
IMPLEMENTED_STACK=Java 25 / Spring Boot 4.1.0
DOCUMENTED_STACK=Java 21 / Spring Boot 3.5.x
DIVERGENCE=YES
```

Trazabilidad:

```text
ea437fa build(backend): migrate Java baseline from 21 to 25
b9f7587 build(backend): migrate Spring Boot from 3.5.15 to 4.1.0
```

`git blame` confirma que esas versiones actuales provienen de dichos commits.

```text
DECISION_OWNER=ChatGPT Work / Architecture Owner
DECISION_STATUS=REQUIRES_CHATGPT_DECISION
```

La evidencia resuelve el stack implementado, no la versión arquitectónica oficial.

### 11.2 `EMAIL_SLUG_RANDOM`

Resultados de historial:

- `git log -S EMAIL_SLUG_RANDOM`: sin commits.
- El ejemplo `ELBURGASI_GMAIL_COM_81447` aparece cuando se incorpora el análisis/baseline DB en `dbc374e`.
- El historial de AuthController lleva el registro corto hasta `0531bdf`.
- Desde su introducción usa `gypport-<apellido>`.
- No apareció generador de slug-email ni sufijo aleatorio.
- No apareció implementación eliminada relevante.

```text
ALTERNATE_REGISTRATION_FLOW=NOT_FOUND_IN_REPOSITORY_SCOPE
EXTERNAL_OR_HISTORICAL_IMPLEMENTATION=NOT_DISPROVEN
EMAIL_SLUG_RANDOM_ORIGIN=NOT_CONFIRMED
```

### 11.3 Healthcheck

MySQL:

```text
HEALTHCHECK_FILE=docker/compose.yaml
TARGET_SERVICE=mysql
TARGET_CONTAINER=gypport-mysql-dev
CHECK_TYPE=MYSQL_PROCESS_READINESS
CHECK_COMMAND=mysqladmin ping -h 127.0.0.1 -uroot -p$MYSQL_ROOT_PASSWORD --silent
DATABASE_INFRASTRUCTURE_HEALTHCHECK=EVIDENCE_CONFIRMED
RUNTIME_RESULT=UNVERIFIED
```

Backend:

```text
TARGET_SERVICE=backend
TARGET_CONTAINER=gypport-backend-dev
CHECK_TYPE=TCP_PORT_OPEN
CHECK_COMMAND=bash -c 'exec 3<>/dev/tcp/127.0.0.1/8080'
APPLICATION_HEALTH_CAPABILITY=ABSENT
RUNTIME_RESULT=UNVERIFIED
```

Reclasificación:

```text
APPLICATION_HEALTH_CONNECTION_STATUS=CAPABILITY_ABSENT
INFRASTRUCTURE_DB_HEALTHCHECK=EVIDENCE_CONFIRMED_TARGET_MYSQL
```

### 11.4 Fuente de verdad lifecycle

```text
MODULES_AVAILABLE=installedPlugins.js
MODULES_INSTALLED=CONFLICTED
FEATURES_ACTIVE=FeatureContext memory, no caller
TENANT_ENTITLEMENT=NOT_IMPLEMENTED
USER_AUTHORIZATION=backend fixed permission + RuntimeContext
LIFECYCLE_SOURCE_OF_TRUTH=CONFLICTED_BY_EVIDENCE
```

## 12. Matriz consolidada de ownership

| Área | CURRENT_OWNER_CLASS | RECOMMENDED_OWNER_CLASS | FINAL_APPROVED_OWNER | DECISION_STATUS |
|---|---|---|---|---|
| Tenant provisioning | UNDETERMINED | PLATFORM_OS_CORE | NONE | REQUIRES_CHATGPT_DECISION |
| Active tenant context | PLATFORM_OS_CORE | PLATFORM_OS_CORE | NONE | ARCHITECTURAL_RECOMMENDATION |
| Authentication | PLATFORM_OS_CORE | PLATFORM_OS_CORE | NONE | ARCHITECTURAL_RECOMMENDATION |
| Session model | UNDETERMINED | PLATFORM_OS_CORE | NONE | REQUIRES_CHATGPT_DECISION |
| User accounts | PLATFORM_OS_CORE | PLATFORM_OS_CORE | NONE | ARCHITECTURAL_RECOMMENDATION |
| RBAC/scopes | UNDETERMINED | PLATFORM_OS_CORE | NONE | REQUIRES_CHATGPT_DECISION |
| MDM golden record | UNDETERMINED | UNDETERMINED | NONE | REQUIRES_CHATGPT_DECISION |
| Tenant Party projection | UNDETERMINED | UNDETERMINED | NONE | REQUIRES_CHATGPT_DECISION |
| Organization | UNDETERMINED | UNDETERMINED | NONE | REQUIRES_CHATGPT_DECISION |
| Branch | UNDETERMINED | UNDETERMINED | NONE | REQUIRES_CHATGPT_DECISION |
| Establishment | UNDETERMINED | UNDETERMINED | NONE | REQUIRES_CHATGPT_DECISION |
| Catalogs | UNDETERMINED | UNDETERMINED | NONE | REQUIRES_CHATGPT_DECISION |
| Audit | UNDETERMINED | UNDETERMINED | NONE | REQUIRES_CHATGPT_DECISION |
| Module catalog/lifecycle | PLATFORM_OS_CORE | PLATFORM_OS_CORE | NONE | CONFLICTED_BY_EVIDENCE |
| Capability registries | PLATFORM_OS_CORE | PLATFORM_OS_CORE | NONE | ARCHITECTURAL_RECOMMENDATION |
| Navigation composition | UNDETERMINED | PLATFORM_OS_CORE | NONE | CONFLICTED_BY_EVIDENCE |
| Application health | PLATFORM_OS_INFRASTRUCTURE | PLATFORM_OS_INFRASTRUCTURE | NONE | ARCHITECTURAL_RECOMMENDATION |
| Database infrastructure | PLATFORM_OS_INFRASTRUCTURE | PLATFORM_OS_INFRASTRUCTURE | NONE | EVIDENCE_CONFIRMED |
| Commercial | EXTERNAL_BUSINESS_MODULE | EXTERNAL_BUSINESS_MODULE | NONE | EVIDENCE_CONFIRMED |
| Public cross-boundary definitions | Internos dispersos | SHARED_CONTRACT | NONE | ARCHITECTURAL_RECOMMENDATION |

## 13. Matriz candidata de acceso del desarrollador

No existe `CODEOWNERS` actual. Los nombres siguientes son candidatos conceptuales, no permisos aplicados.

La existencia de cada ruta se registra separadamente de la recomendación de acceso:

```text
CURRENT_LOCATION_STATUS
→ evidencia verificable de la ubicación actual

PROPOSED_ACCESS_STATUS
→ estado de una recomendación de acceso todavía no aprobada
```

Por tanto, `EVIDENCE_CONFIRMED` en esta matriz solo confirma la ubicación actual. No aprueba `PROTECTED_CORE`, `PLATFORM_OS_READ_ONLY`, `SHARED_CONTRACT_CHANGE_BY_REVIEW` ni `MODULE_WRITE_ALLOWED_CANDIDATE`.

| PATH_OR_COMPONENT | OWNER_CLASS | CURRENT_LOCATION_STATUS | PROPOSED_ACCESS | PROPOSED_ACCESS_STATUS | JUSTIFICATION | REVIEW_REQUIRED | CODEOWNER_CANDIDATE |
|---|---|---|---|---|---|---|---|
| `platform_os/studio/module/commercial/` | EXTERNAL_BUSINESS_MODULE | EVIDENCE_CONFIRMED | MODULE_WRITE_ALLOWED_CANDIDATE | ARCHITECTURAL_RECOMMENDATION | Ubicación empresarial confirmada; el permiso de escritura continúa pendiente de aprobación | YES | COMMERCIAL_MODULE_TEAM |
| `platform_os/studio/module/party/` | UNDETERMINED | EVIDENCE_CONFIRMED | UNDETERMINED | REQUIRES_CHATGPT_DECISION | Party/MDM ownership no resuelto | YES | UNDETERMINED |
| `platform_os/server/.../module/party/` | UNDETERMINED | EVIDENCE_CONFIRMED | UNDETERMINED | REQUIRES_CHATGPT_DECISION | Implementación actual obsoleta y owner abierto | YES | UNDETERMINED |
| `platform_os/server/.../module/tenant/` | PLATFORM_OS_CORE | EVIDENCE_CONFIRMED | PLATFORM_OS_READ_ONLY | ARCHITECTURAL_RECOMMENDATION | Provisioning/auth afecta el límite SaaS; el acceso propuesto no está aprobado | YES | PLATFORM_OS_CORE_TEAM |
| `platform_os/server/.../module/identity/` | PLATFORM_OS_CORE | EVIDENCE_CONFIRMED | PLATFORM_OS_READ_ONLY | ARCHITECTURAL_RECOMMENDATION | Identidad y tenant context transversales; el acceso propuesto no está aprobado | YES | PLATFORM_OS_CORE_TEAM |
| `platform_os/server/shared/config/` | PLATFORM_OS_INFRASTRUCTURE | EVIDENCE_CONFIRMED | PROTECTED_CORE | ARCHITECTURAL_RECOMMENDATION | Seguridad global y CORS; la protección propuesta no constituye permiso vigente | YES | PLATFORM_INFRASTRUCTURE_TEAM |
| `platform_os/server/shared/repository/` | PLATFORM_OS_INFRASTRUCTURE | EVIDENCE_CONFIRMED | PLATFORM_OS_READ_ONLY | ARCHITECTURAL_RECOMMENDATION | Base JDBC transversal; el acceso propuesto no está aprobado | YES | PLATFORM_INFRASTRUCTURE_TEAM |
| `platform_os/studio/contracts/` | SHARED_CONTRACT | EVIDENCE_CONFIRMED | SHARED_CONTRACT_CHANGE_BY_REVIEW | ARCHITECTURAL_RECOMMENDATION | Los contratos cruzan fronteras; la revisión obligatoria continúa como recomendación | YES | ARCHITECTURE_REVIEW |
| `platform_os/studio/engine/framework/` | PLATFORM_OS_CORE | EVIDENCE_CONFIRMED | PLATFORM_OS_READ_ONLY | ARCHITECTURAL_RECOMMENDATION | Los módulos consumen APIs, no su implementación; el acceso propuesto no está aprobado | YES | PLATFORM_OS_CORE_TEAM |
| `platform_os/studio/engine/core/registry/` | PLATFORM_OS_CORE | EVIDENCE_CONFIRMED | PROTECTED_CORE | ARCHITECTURAL_RECOMMENDATION | Ubicación central de registries confirmada; la protección propuesta no está aprobada | YES | PLATFORM_OS_CORE_TEAM |
| `platform_os/studio/engine/core/runtime/` | PLATFORM_OS_CORE | EVIDENCE_CONFIRMED | PROTECTED_CORE | ARCHITECTURAL_RECOMMENDATION | Tenant, usuario, permisos y workspace context; la protección propuesta no está aprobada | YES | PLATFORM_OS_CORE_TEAM |
| `platform_os/studio/engine/kernel/` | PLATFORM_OS_CORE | EVIDENCE_CONFIRMED | PROTECTED_CORE | ARCHITECTURAL_RECOMMENDATION | La ubicación en Kernel es evidencia; su nivel de protección sigue siendo recomendación | YES | PLATFORM_OS_CORE_TEAM |
| `platform_os/studio/app/business-studio/` | PLATFORM_OS_CORE | EVIDENCE_CONFIRMED | SHARED_CONTRACT_CHANGE_BY_REVIEW | ARCHITECTURAL_RECOMMENDATION | Composición global del producto; la revisión obligatoria continúa pendiente de aprobación | YES | PLATFORM_OS_CORE_TEAM |
| `platform_os/studio/channel/browser/shell/` | PLATFORM_OS_CORE | EVIDENCE_CONFIRMED | PLATFORM_OS_READ_ONLY | ARCHITECTURAL_RECOMMENDATION | El shell no debe ser negocio ni source of truth; el acceso propuesto no está aprobado | YES | BROWSER_CHANNEL_TEAM |
| `database/core/migration/V1__...` y `V2__...` | PLATFORM_OS_INFRASTRUCTURE | EVIDENCE_CONFIRMED | PROTECTED_CORE | ARCHITECTURAL_RECOMMENDATION | La ubicación de las migraciones canónicas es evidencia; la inmutabilidad propuesta no constituye permiso vigente | YES | DATABASE_GOVERNANCE |
| `docker/compose.yaml` | PLATFORM_OS_INFRASTRUCTURE | EVIDENCE_CONFIRMED | PLATFORM_OS_READ_ONLY | ARCHITECTURAL_RECOMMENDATION | Infraestructura compartida; el acceso propuesto no está aprobado | YES | PLATFORM_INFRASTRUCTURE_TEAM |
| `developer_platform/toolchain/` | PLATFORM_OS_INFRASTRUCTURE | EVIDENCE_CONFIRMED | PROTECTED_CORE | ARCHITECTURAL_RECOMMENDATION | La ubicación y el cierre previo del track son evidencia; esta matriz no aprueba el permiso propuesto | YES | TOOLCHAIN_OWNER |
| `docs/architecture/` | UNDETERMINED | EVIDENCE_CONFIRMED | SHARED_CONTRACT_CHANGE_BY_REVIEW | ARCHITECTURAL_RECOMMENDATION | La ruta existe; el owner y la revisión obligatoria requieren decisión arquitectónica formal | YES | ARCHITECTURE_OWNER |

```text
SECTION_13_ROWS_CORRECTED=18/18
PROPOSED_ACCESS_EVIDENCE_CONFIRMED_ROWS=0/18
PROPOSED_ACCESS_ARCHITECTURAL_RECOMMENDATION_ROWS=16/18
PROPOSED_ACCESS_REQUIRES_CHATGPT_DECISION_ROWS=2/18
```

## 14. Gaps evaluados durante `01.3`

La normalización usa exclusivamente esta taxonomía en `RECOMMENDED_OWNER`:

```text
PLATFORM_OS_CORE
PLATFORM_OS_INFRASTRUCTURE
SHARED_CONTRACT
EXTERNAL_BUSINESS_MODULE
UNDETERMINED
```

`DECISION_OWNER` identifica quién debe aprobar una recomendación; no representa ownership técnico.

| GAP_ID | BOUNDARY_DECISION analizada | RECOMMENDED_OWNER | DECISION_STATUS | RESOLVED_BY_EVIDENCE | REQUIRES_CHATGPT_DECISION | DECISION_OWNER | SECURITY | NEXT DEPENDENCY |
|---|---|---|---|---|---|---|---|---|
| GAP-IDENTITY-01 | Active tenant context debe ser central y cruzar auth contract | PLATFORM_OS_CORE | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Alto | Selección tenant |
| GAP-IDENTITY-02 | Tenant provisioning separado de active tenant context | PLATFORM_OS_CORE | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Alto | Flujo de alta vigente |
| GAP-SESSION-01 | Sesión es responsabilidad transversal | PLATFORM_OS_CORE | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Alto | Modelo de sesión |
| GAP-RBAC-01 | Concesión/enforcement central; módulos solo declaran requisitos | PLATFORM_OS_CORE | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Alto | RBAC/scopes |
| GAP-RBAC-02 | Entitlement y filtrado no pertenecen a módulos | PLATFORM_OS_CORE | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Alto | Scope por tenant/user |
| GAP-LIFECYCLE-01 | Catálogo/instalación necesitan owner único central | PLATFORM_OS_CORE | CONFLICTED_BY_EVIDENCE | NO | YES | ChatGPT Work / Architecture Owner | Medio/Alto | Source of truth |
| GAP-LIFECYCLE-02 | Activación distinta de instalación | PLATFORM_OS_CORE | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Medio | Semántica de activación |
| GAP-LIFECYCLE-03 | PluginManager, PackageManager, Kernel y Runtime divergen | PLATFORM_OS_CORE | CONFLICTED_BY_EVIDENCE | NO | YES | ChatGPT Work / Architecture Owner | Medio/Alto | Consolidación futura |
| GAP-DISCOVERY-01 | Registries siguen centrales; acceso mediante shared contract | PLATFORM_OS_CORE | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Medio | Discovery contract |
| GAP-PERSISTENCE-01 | Semántica Core; mecanismo persistente aún indeterminado | UNDETERMINED | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Medio | Qué estado persiste |
| GAP-CONTRACT-01 | Party/MDM requiere separación antes del contrato | UNDETERMINED | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Alto | Owner Party/MDM |
| GAP-CONTRACT-02A | El módulo externo es candidato a poseer sus datos de dominio Business | EXTERNAL_BUSINESS_MODULE | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Medio/Alto | Datasource contract |
| GAP-CONTRACT-02B | Platform Infrastructure es candidato a poseer el mecanismo datasource compartido | PLATFORM_OS_INFRASTRUCTURE | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Medio/Alto | Datasource contract |
| GAP-BOUNDARY-01 | Módulos deben consumir shared contracts, no fetch divergentes | SHARED_CONTRACT | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Medio | Frontera pública |
| GAP-NAV-01 | Core compone; módulos declaran; shell consume | PLATFORM_OS_CORE | CONFLICTED_BY_EVIDENCE | NO | YES | ChatGPT Work / Architecture Owner | Medio | Fuente navegación |
| GAP-OBS-01 | Application health pertenece a infraestructura | PLATFORM_OS_INFRASTRUCTURE | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Medio | Definición health |
| GAP-DOC-01A | El stack implementado actual está confirmado por evidencia del filesystem | UNDETERMINED | EVIDENCE_CONFIRMED | YES | NO | NONE | Medio | Ninguna para el hecho implementado |
| GAP-DOC-01B | El stack arquitectónico oficial continúa pendiente de aprobación | UNDETERMINED | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Medio | Actualización normativa |
| GAP-DOC-02 | Origen EMAIL_SLUG_RANDOM no confirmado | UNDETERMINED | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Medio | Evidencia externa |
| GAP-PARTY-01A | MDM golden record y Party tenant-scoped son responsabilidades distintas | UNDETERMINED | EVIDENCE_CONFIRMED | YES | YES | ChatGPT Work / Architecture Owner | Alto | Owner MDM y Party projection |
| GAP-PARTY-01B | Party tenant-scoped y Commercial Business Partner son responsabilidades distintas | UNDETERMINED | EVIDENCE_CONFIRMED | YES | YES | ChatGPT Work / Architecture Owner | Alto | Owner Party projection |
| GAP-PARTY-01C | Commercial Business Partner es candidato a permanecer en el módulo empresarial externo | EXTERNAL_BUSINESS_MODULE | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Alto | Owner Commercial |
| GAP-SCOPE-01 | Jerarquía existe en schema, enforcement ausente | PLATFORM_OS_CORE | REQUIRES_CHATGPT_DECISION | NO | YES | ChatGPT Work / Architecture Owner | Alto | Scope resolution |
| GAP-HEALTH-01A | El healthcheck inspeccionado tiene como target el servicio MySQL | PLATFORM_OS_INFRASTRUCTURE | EVIDENCE_CONFIRMED | YES | NO | NONE | Bajo | Ninguna para el target confirmado |
| GAP-HEALTH-01B | La capacidad de application health está ausente y su owner propuesto es infraestructura | PLATFORM_OS_INFRASTRUCTURE | ARCHITECTURAL_RECOMMENDATION | NO | YES | ChatGPT Work / Architecture Owner | Medio | Health semantics |

```text
SECTION_14_COMPOUND_FINDINGS_SPLIT=COMPLETE
GAP_CONTRACT_02_OWNER_SPLIT=COMPLETE
GAP_DOC_01_RECOMMENDED_OWNER=UNDETERMINED
CHATGPT_WORK_IN_RECOMMENDED_OWNER=0
RECOMMENDED_OWNER_TAXONOMY_VIOLATIONS=0
SECTION_14_NORMALIZATION=COMPLETE_PENDING_CLAUDE_VERIFICATION
```

Ningún gap de ownership quedó aprobado definitivamente.

## 15. Decisiones que requieren aprobación de ChatGPT Work

1. Stack arquitectónico oficial Java/Spring Boot.
2. Owner de Tenant Provisioning.
3. Mecanismo de selección del tenant durante login.
4. Modelo oficial de sesión.
5. Owner y enforcement de RBAC/scopes.
6. Owner de MDM golden record.
7. Owner de la proyección Party tenant-scoped.
8. Owner de Organization.
9. Owner de Branch.
10. Owner de Establishment.
11. Separación de catálogos globales y tenant-scoped.
12. Separación entre almacenamiento de auditoría y política/eventos.
13. Fuente única del catálogo/lifecycle modular.
14. Semántica de available/registered/installed/enabled/active.
15. Alcance global o tenant-scoped de módulos y features.
16. Estado de lifecycle que debe persistirse.
17. Ownership del discovery público.
18. Fuente definitiva de navegación.
19. Frontera pública Party/MDM.
20. Contrato de datasource Business ↔ Dashboard.
21. Áreas de escritura permitidas al desarrollador externo.
22. CODEOWNER real de cada frontera.
23. Definición de application health.
24. Procedencia/vigencia de `EMAIL_SLUG_RANDOM`.

## 16. Contradicciones y preguntas no resueltas

Contradicciones:

- Java 25/Boot 4.1 implementado frente a Java 21/Boot 3.5 documentado.
- PluginManager declarado como lifecycle owner, pero KernelContext, PackageManager y RuntimeContext conservan estados paralelos.
- NavigationRegistry existe, pero StudioShell usa navegación estática.
- Feature activation existe, pero el flujo productivo solo instala/registra.
- RBAC existe en schema, pero login entrega permiso fijo.
- `user_sessions` existe, pero no hay sesión.
- MDM es global, mientras Party/Organization/Employee son tenant-scoped; el backend legacy los trata como modelo plano.
- MySQL tiene healthcheck específico; backend solo prueba apertura TCP.
- Evidencia DB muestra `EMAIL_SLUG_RANDOM`, pero código e historial no contienen el generador.

Preguntas no resueltas principales:

- ¿Quién gobierna la identidad global MDM?
- ¿Quién gobierna Party base compartida entre dominios?
- ¿Organization/Branch/Establishment son Platform context, business capability o responsabilidades divididas?
- ¿Un usuario humano puede operar múltiples tenants?
- ¿Cómo se representa esa pertenencia sin ambigüedad?
- ¿Qué scope se activa durante una sesión?
- ¿Qué source of truth reemplaza las cinco representaciones actuales de plugins?
- ¿Qué estado es configuración de producto y qué estado es operación tenant-scoped?
- ¿Qué APIs internas se convierten formalmente en shared contracts?
- ¿Cuál es la frontera de escritura del desarrollador de módulo?

## 17. Cobertura y veredicto

```text
GIT_GATE_COMMANDS=6/6
BASELINE_HEAD_MATCH=YES
BASELINE_DELTA_FILES=0
RESPONSIBILITIES_MAPPED=24/24
MINIMUM_RESPONSIBILITIES_COVERED=24/24
EXTERNAL_MODULE_INTERACTIONS_REVIEWED=14
PARTY_MDM_LAYERS_SEPARATED=3/3
SCOPE_LEVELS_REVIEWED=8/8
LIFECYCLE_STAGES_REVIEWED=13/13
DATA_OWNERSHIP_GROUPS_REVIEWED=11/11
ACCESS_AREAS_CLASSIFIED=18
SECTION_13_ROWS_CORRECTED=18/18
PROPOSED_ACCESS_EVIDENCE_CONFIRMED_ROWS=0
INHERITED_GAPS_REEVALUATED=16/16
ADDITIONAL_BOUNDARY_GAPS=4
GIT_HISTORY_SEARCHES_COMPLETED=YES
RUNTIME_VALIDATIONS=0
FINAL_APPROVED_OWNERS=0
ACCESS_CHANGES=0
```

El análisis está completo para auditoría y decisión arquitectónica. Las recomendaciones no constituyen owners aprobados ni permisos concedidos.

```text
FILES_MODIFIED=NONE
FILES_CREATED=NONE
TESTS_EXECUTED=NONE
APPLICATIONS_STARTED=NONE
DATABASE_QUERIES_EXECUTED=NONE
ENDPOINTS_DESIGNED=NONE
OWNERSHIP_DECISIONS_APPROVED=NONE
DEVELOPER_ACCESS_APPROVED=NONE
ACCESS_CHANGES_EXECUTED=NONE
STEP_01_3_STATUS=COMPLETE_PENDING_ARCHITECTURE_DECISION
RESULT=BOUNDARY_ANALYSIS_COMPLETE_READY_FOR_ARCHITECTURE_DECISION
```

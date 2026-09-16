# Studio PERSONAL Dashboard, account and icon refinement

PEGAR EN: CHATGPT / CLAUDE — evidencia de implementación y gate de aceptación visual.

```text
PROJECT=GYPPORT
TRACK=GYPPORT-MVP-GENERAL-01
STEP=STUDIO_PERSONAL_DASHBOARD_USER_MENU_AND_ICON_REFINEMENT_01
MODE=CONTROLLED_UI_AUDIT_AND_IMPLEMENTATION
AGENT=CODEX
DATE=2026-08-30
STATUS=OWNER_DECISION_REQUIRED
IMPLEMENTATION=IMPLEMENTED
VALIDATION=DIRECTLY_CONFIRMED
INDEPENDENT_AUDIT=NOT_PERFORMED
OWNER_VISUAL_ACCEPTANCE=PENDING
```

Implementación y comprobaciones terminadas. El estado pendiente identifica exclusivamente el gate visual del Owner; no implica permiso para comenzar Expense Case.

## Continuidad

- Checkout: `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo`.
- Branch: `feature/gm-fleets-minimum-vehicle-master-01`.
- HEAD inicial/final: `beb88046837a1afce8b1d25b722ed80b0adb959c`.
- Predecesor: `STUDIO_PRESTASHOP_INSPIRED_PRIMARY_UI_REBASELINE_01.md`, preservado. El Owner aceptó la dirección del shell y autorizó únicamente Dashboard PERSONAL, cuenta e iconografía.
- Estado inicial: 24 archivos dirty/untracked, índice vacío. Se registraron hashes de esos archivos y de tres archivos limpios que requerían cambios.
- Sin staging, commits, push, cambios remotos ni resets. AGENTS.md exige autorización expresa para operaciones Git de publicación; este STEP no la otorga.

## Auditoría de iconos y avatar, antes de editar

```text
CURRENT_ICON_LIBRARY_BEFORE=NONE
CURRENT_ICON_USAGE_BEFORE=StudioIcon.jsx con SVG locales; flechas Unicode en navegación/cuenta
ICON_LIBRARY_REUSED=NO
NEW_ICON_LIBRARY_ADDED=YES
CURRENT_ICON_LIBRARY=lucide-react@1.37.0
```

Se inspeccionaron package.json del shell, package.json/package-lock.json de Gystigo, manifiestos del workspace, node_modules y fuentes de Studio/design-system. No había una librería React de iconos declarada, instalada y utilizable por Studio. Se aplicó la excepción explícita del Owner para ese caso: instalar **una** librería, sin trasladar dependencias desde UI_Experiments.

La versión se consultó en el registro npm; sus peer dependencies incluyen React 19. Se instaló con versión exacta, `--ignore-scripts --no-audit --no-fund`. El diff del lockfile incorpora únicamente Lucide y su referencia en el workspace; no se actualizaron otras dependencias. Se verificaron los exports reales antes de importarlos. Esto no constituye una auditoría de seguridad de terceros.

Mapeo de presentación, sin alterar registry, rutas ni permisos:

| Concepto | Export de Lucide |
|---|---|
| Inicio | Home |
| Ventas | ShoppingCart |
| Compras | ShoppingBag |
| Catálogo | Package |
| Gastos | Receipt |
| Vehículos | Truck |
| Talleres | Wrench |
| Administración / Clientes | Users |
| Análisis / Reportes / BI | ChartColumn |
| Configuración | Settings |
| Contabilidad / Proveedores / Empleados | Landmark / Building2 / BriefcaseBusiness |
| Perfil / logout | UserRound / LogOut |
| Flechas / menú / cerrar | ChevronDown / ChevronRight / ChevronLeft / Menu / X |
| Búsqueda / notificaciones | Search / Bell |

Todos los SVG del sidebar y header renderizados provienen de Lucide; no quedan SVG manuales, flechas Unicode ni emoji en ese sistema primario. Stroke uniforme 1.75, tamaño calculado desde los tokens de espacio existentes (18 px verificados), alineación y color heredado del estado activo/inactivo. No se modificó la navegación interna de otros módulos.

No existe backend de foto de perfil implementado: el perfil actual expone identidad e identificadores, no upload de avatar. Se conserva `UserAvatar` sin cambios: iniciales del nombre autenticado, forma circular, slot futuro de URL de imagen y fallback. No se agregó persistencia ni petición de imagen.

## Causa exacta del Dashboard y corrección

Antes del cambio, el DOM real de Inicio mostraba `data-browser-dashboard-host="ACCESS_DENIED"`. La traza es:

1. `browserSessionSource` hidrata tenant, usuario/accountId y permisos efectivos desde `/auth/me`, con enriquecimiento opcional de perfil. Login también obtiene actor.accountId del servidor. Ambos conservan `activeOrganizationId=null` para PERSONAL.
2. `RuntimeWorkspace.activeDashboard` apunta a `commercial-dashboard`.
3. `resolveCurrentDashboard()` delegaba directamente en `resolveDashboard()`.
4. `requiredPermissions(composition)` reúne los permisos del dashboard y sus widgets. CommercialDashboard, CommercialTotalKpiWidget y CommercialMonthlyChartWidget requieren `commercial.dashboard.view`.
5. El filtro `!permissions.includes(permission)` produce `missingPermissions` y `ACCESS_DENIED`. DashboardHost traduce ese resultado al mensaje genérico «Se requiere un contexto seguro de tenant, usuario y permisos» aunque la sesión PERSONAL es válida.

**La causa no era una condición `activeOrganization != null`, ni falta de cédula, RUC o configuración fiscal.** Se estaba utilizando la composición comercial protegida como única presentación de Inicio PERSONAL.

Se agregó `resolveStudioHome` exclusivamente en la capa de presentación Browser Shell. Valida tenant y usuario con identificadores no vacíos/válidos, y exige un array de permisos cuyos elementos sean strings no vacíos. Conserva compatibilidad con identificadores opacos de los adaptadores Runtime; accountId no se transforma ni se confunde con Party id. La hidratación autenticada, sus validadores y todos los permisos permanecen intactos.

Con contexto válido y `activeOrganizationId === null`, devuelve un estado vacío explícito `PERSONAL_HOME`: saludo con nombre real, Inicio, Operando como Personal y accesos del registry filtrados por permisos. Un array válido vacío es admisible, pero no muestra accesos que requieren grants. No se resuelve ni renderiza contenido comercial, analítica o datos simulados para ese estado.

Para otros contextos se mantiene `resolveDashboard` con sus gates originales. No se añade `commercial.dashboard.view`, no se modifican permisos y no se convierte ACCESS_DENIED comercial en READY. Los contextos ausentes/malformados siguen denegados antes de la bienvenida PERSONAL. La ruta protegida sigue redirigiendo a login sin identidad autenticada.

## Cuenta y branding

- Trigger nativo button: avatar, nombre truncable y ChevronDown; title y aria-label exponen el nombre completo; móvil conserva avatar/flecha.
- Dropdown: avatar, «Bienvenido de nuevo,», nombre autenticado, Mi perfil con icono, Operando como / Personal, separador y Cerrar sesión con icono.
- Mi perfil reutiliza `/mi-perfil`; logout reutiliza el handler seguro existente sin modificar StudioLayout ni authService.
- Escape y clic exterior conservados. Acciones de 44 px y tarjeta de 264 px limitada al viewport.
- Notificaciones y búsqueda siguen deshabilitadas y marcadas Próximamente, sin contadores/resultados ficticios.
- Branding izquierdo usa `GYPPORT® / Business Platform` sin nombre comercial activo. No se inventa un nombre comercial ni se implementa switching futuro; la cuenta permanece independiente del branding. No se afirma implementada la variante futura comercial/Powered by.
- Se conserva la geometría aceptada del shell: sidebar 216/60 px, topbar fija 56 px, breakpoints y drawer existentes. No se rediseñó el shell.

## Pruebas

1. Contrato de regresión antes de corregir: 12 tests, **2 fallos esperados**, ambos reproduciendo ACCESS_DENIED en PERSONAL válido.
2. Primera suite después de corregir: **3 fallos** en contratos existentes porque la primera validación solo admitía IDs numéricos. Se corrigió la implementación para preservar los IDs opacos admitidos por Runtime; no se debilitaron ni editaron esos contratos.
3. Suite posterior: 243/243 PASS; lint PASS; build design-system y shell PASS.
4. Se agregaron cuatro casos negativos directos para permisos ausentes/malformados. Suite final: **247/247 PASS en 27 archivos**. No hubo cambios posteriores de producción.

Comandos: `npm run contracts`, `npm run lint`, `npm run build`, cada uno con `--workspace=@gypport/platform-os-browser-shell`, desde Gystigo. El build final produjo 2145 módulos transformados y bundle JS de 390.74 kB / 113.02 kB gzip.

Cobertura de seguridad: falta de tenant/usuario, objetos vacíos, IDs inválidos, ausencia de permisos, arrays malformados, runtime limpiado después de sesión, contexto organizacional sin permiso comercial; todos siguen denegados. PERSONAL con permisos vacíos válidos obtiene solo bienvenida, sin accesos protegidos. Los contratos anteriores de sesión, ownership y autorización siguen pasando sin cambios.

Se recuperaron incidencias operativas: acceso bloqueado a caché npm (consulta repetida con aprobación), lectura inicial de baseline JSON contaminada por warning (se repitió antes de editar), paths largos Git (core.longpaths por comando), y selectores de navegador afectados por cambios de estado/elementos cubiertos (snapshot fresco y repetición sobre controles visibles). Git advierte que no puede leer el ignore global; status y hashes locales se obtuvieron correctamente. No se ocultaron fallos de tests.

### Navegador real

`http://localhost:5173`, Host existente 8080. Se reutilizó la cuenta sintética PERSONAL ya existente, sin cédula/organización configuradas, con datos de prueba anteriores. **No se creó un usuario nuevo ni se repitió registro/verificación de email**, fuera del alcance de este refinamiento. No se crearon gastos, vehículos ni identificadores. Login/logout normales usan el runtime existente.

| Comprobación | Resultado |
|---|---|
| Login PERSONAL → Inicio | PASS: PERSONAL_HOME y nombre real |
| Reload `/dashboard` | PASS: PERSONAL_HOME |
| Acceso no disponible con PERSONAL válido | ABSENT |
| Accesos rápidos Gastos / menú Vehículos / volver Inicio | PASS |
| Navegación móvil Inicio / Gastos / Vehículos | PASS |
| Perfil desde dropdown escritorio y móvil | PASS |
| Logout escritorio y móvil | PASS |
| `/dashboard` después de logout | Redirige a login |
| Escape / clic exterior | PASS |
| 1440×900 / 1366×768 / 390×844 | PASS visual/técnico; aceptación estética pendiente |
| Iconos primarios renderizados | Todos identificados como Lucide en DOM |

En 1366 y 390, ancho del documento igual al viewport. En móvil, tarjeta x=114, derecha=378, ancho=264, alto=311, dentro de 390×844. Las vistas se inspeccionaron por captura, no solo por contratos. La preferencia de viewport se restauró al finalizar.

Capturas bajo `C:\Users\elbur\.codex\visualizations\2026\08\30\01a05471-5d5b-7400-98b0-77b7b0304670`:
`personal-dashboard-1440.png`, `personal-dashboard-1366.png`, `personal-dashboard-390.png`, `personal-icons-390-drawer.png`.

## Archivos e integridad

12 archivos de este STEP, relativos al checkout:

```text
package-lock.json
platform_os/studio/channel/browser/shell/package.json
platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.jsx
platform_os/studio/channel/browser/shell/src/application/dashboard/resolveDashboard.js
platform_os/studio/channel/browser/shell/src/layout/StudioHeader.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioIcon.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioNavigation.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioSidebar.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioUserMenu.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioPrimaryShell.css
platform_os/studio/verification/contracts/browser/PersonalDashboard.contract.mjs
docs/ai/handoffs/codex-to-review/STUDIO_PERSONAL_DASHBOARD_USER_MENU_AND_ICON_REFINEMENT_01.md
```

Se compararon SHA-256 contra el inicio. De los siete borradores visuales originales, seis permanecen byte a byte iguales: Button, tokens, AuthPage.css, DashboardHost.css, ShortRegisterPage y StudioLayout.css. DashboardHost.jsx se refinó conforme a la autorización actual y conserva los cambios previos compatibles de estados vacíos/CTA.

Sin cambios en StudioLayout.jsx, authService.js, browserSessionSource.js, main.jsx, BusinessPlatformComposition.js, UserAvatar.jsx, contratos anteriores e informes anteriores. Sin escrituras en UI_Experiments. El diff acumulado contra HEAD incluye pasos anteriores y no representa por sí solo este alcance. Estado final: 29 paths dirty/untracked, índice vacío, HEAD sin cambios; `git diff --check` PASS.

## Cierre

`git status --short` final (incluye trabajo previo; no es una allowlist de staging):

```text
 M design_system/src/components/Button/Button.tsx
 M design_system/src/tokens/tokens.css
 M package-lock.json
 M platform_os/studio/channel/browser/shell/package.json
 M platform_os/studio/channel/browser/shell/src/application/AuthPage.css
 M platform_os/studio/channel/browser/shell/src/application/authentication/authService.js
 M platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.css
 M platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.jsx
 M platform_os/studio/channel/browser/shell/src/application/dashboard/resolveDashboard.js
 M platform_os/studio/channel/browser/shell/src/application/onboarding/ShortRegisterPage.jsx
 M platform_os/studio/channel/browser/shell/src/layout/StudioHeader.jsx
 M platform_os/studio/channel/browser/shell/src/layout/StudioLayout.css
 M platform_os/studio/channel/browser/shell/src/layout/StudioLayout.jsx
 M platform_os/studio/channel/browser/shell/src/layout/StudioNavigation.jsx
 M platform_os/studio/channel/browser/shell/src/layout/StudioSidebar.jsx
 M platform_os/studio/channel/browser/shell/src/main.jsx
 M platform_os/studio/composition/business-platform/BusinessPlatformComposition.js
 M platform_os/studio/verification/integration/FrontendCanonicalIntegration.contract.mjs
?? docs/ai/handoffs/codex-to-review/STUDIO_LEFT_NAVIGATION_MODULE_INTEGRATION_01.md
?? docs/ai/handoffs/codex-to-review/STUDIO_PERSONAL_DASHBOARD_USER_MENU_AND_ICON_REFINEMENT_01.md
?? docs/ai/handoffs/codex-to-review/STUDIO_PRESTASHOP_INSPIRED_PRIMARY_UI_REBASELINE_01.md
?? platform_os/studio/channel/browser/shell/src/application/authentication/browserSessionSource.js
?? platform_os/studio/channel/browser/shell/src/layout/StudioIcon.jsx
?? platform_os/studio/channel/browser/shell/src/layout/StudioPrimaryShell.css
?? platform_os/studio/channel/browser/shell/src/layout/StudioUserMenu.jsx
?? platform_os/studio/channel/browser/shell/src/layout/UserAvatar.jsx
?? platform_os/studio/verification/contracts/browser/PersonalDashboard.contract.mjs
?? platform_os/studio/verification/contracts/browser/StudioPrimaryShell.contract.mjs
?? platform_os/studio/verification/contracts/browser/StudioSessionNavigation.contract.mjs
```

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=STUDIO_PERSONAL_DASHBOARD_USER_MENU_AND_ICON_REFINEMENT_01
STATUS=OWNER_DECISION_REQUIRED
CURRENT_ICON_LIBRARY=lucide-react@1.37.0; NONE antes del STEP
ICON_LIBRARY_REUSED=NO
NEW_ICON_LIBRARY_ADDED=YES; excepción autorizada por ausencia de librería
SIDEBAR_ICON_REFINEMENT=PASS; Lucide uniforme
TOPBAR_ICON_REFINEMENT=PASS; Lucide uniforme
USER_TRIGGER=PASS; nombre runtime; title; truncado; responsive
ACCOUNT_DROPDOWN=PASS; saludo; perfil; Personal; separador; logout
AVATAR_IMPLEMENTATION=Iniciales; componente existente preservado
PROFILE_NAV=PASS
LOGOUT=PASS
PERSONAL_CONTEXT_DISPLAY=PASS
DASHBOARD_ACCESS_ROOT_CAUSE=Inicio resolvía composición comercial que exige commercial.dashboard.view
PERSONAL_DASHBOARD=PASS
ACCESS_UNAVAILABLE_REMOVED_FOR_VALID_PERSONAL=PASS
INVALID_SECURITY_CONTEXT_STILL_DENIED=PASS
EXPENSES_NAV=PASS
VEHICLES_NAV=PASS
DESKTOP_1440=PASS
DESKTOP_1366=PASS
MOBILE_390=PASS
BACKEND_CHANGED=NO
DATABASE_CHANGED=NO
FLYWAY_CHANGED=NO
FILES_CHANGED=12; lista exacta arriba
PREEXISTING_VISUAL_DRAFT_PRESERVED=YES; refinamientos acotados y compatibles
STUDIO_TESTS=247_PASS_IN_27_FILES
LINT=PASS
BUILD=PASS
TESTS_FAILED=0_FINAL; historial de regresión y correcciones documentado arriba
LOCAL_COMMITS_CREATED=0
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
NEXT_EXACT_ACTION=OWNER_VISUAL_ACCEPTANCE_OF_STUDIO_ACCOUNT_AND_DASHBOARD
```

No se modificaron backend, APIs, base de datos, Flyway, permisos, email verification, recuperación de contraseña, dominios, esquema vehicular, RUC/SRI ni Organization switching. DATABASE_CHANGED=NO refiere a ausencia de intervención SQL/schema/datos de negocio, no a ausencia de efectos normales de login/logout. No se afirma auditoría independiente ni aprobación visual. STOP: no iniciar Expense Case.

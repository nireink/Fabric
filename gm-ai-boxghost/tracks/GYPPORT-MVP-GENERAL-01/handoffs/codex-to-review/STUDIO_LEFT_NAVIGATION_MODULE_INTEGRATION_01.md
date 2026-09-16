# STUDIO_LEFT_NAVIGATION_MODULE_INTEGRATION_01

PEGAR EN: CHATGPT / CLAUDE - evidencia de auditoría del borrador e implementación.

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=STUDIO_LEFT_NAVIGATION_MODULE_INTEGRATION_01
MODE=CONTROLLED_AUDIT_AND_IMPLEMENTATION
AGENT=CODEX
STATUS=COMPLETED
START_HEAD=beb88046837a1afce8b1d25b722ed80b0adb959c
FINAL_HEAD=beb88046837a1afce8b1d25b722ed80b0adb959c
EVIDENCE_STATE=IMPLEMENTED_AND_DIRECTLY_CONFIRMED
INDEPENDENT_AUDIT=NOT_PERFORMED
LOCAL_COMMITS_CREATED=0
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
DESTRUCTIVE_RESET_PERFORMED=NO
```

## Revisión forense y continuidad

Checkout confirmado: `D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo`.
Rama conservada: `feature/gm-fleets-minimum-vehicle-master-01`.
El STEP anterior entregó gm-fleets; este STEP no modifica ese módulo ni el Host.
La solicitud actual autoriza auditoría e implementación. No repite la autorización
expresa de staging/commit del STEP anterior; se dejan los cambios sin staging ni
commit conforme a AGENTS.md. La implementación y su aceptación sí están completas.

CURRENT_NAVIGATION_ARCHITECTURE: `main.jsx` llama a `bootstrapStudio`, que registra
`businessPlatformNavigation` desde la composición en `NavigationRegistry`.
`StudioNavigation` consume `resolveNavigationTree()` y React Router; `StudioLayout`
posee sidebar compacto, drawer, scrim y header. `App.jsx` mantiene las rutas reales.
DashboardHost continúa consumiendo sus resolvers y renderer existentes; no se
introduce un menú paralelo ni se modifica ningún propietario del Engine/Kernel.

Se inspeccionaron los componentes, rutas, composición/registry, bootstrap y sesión,
design-system (Button, Card, tokens), los siete diffs previos y su historial Git.
El historial muestra el menú estático de `cdacc9e`, trasladado a composición/registry
en `2e6c724`; `96874fe` agregó el shortcut de Gastos al header y `beb8804` incorporó
Vehículos en la navegación declarativa. La búsqueda en el Studio actual no encontró
otra estructura completa dormida/comentada que debiera reactivarse. El menú estático
histórico no se restaura ni se duplica.

EXISTING_FRONTEND_DRAFT_FOUND=YES. DRAFT_REUSED=YES, sin editar sus bytes:

| Archivo previo | Intención del borrador preservada |
|---|---|
| `design_system/src/components/Button/Button.tsx` | Botón primario con gradiente, peso, tamaños y estados |
| `design_system/src/tokens/tokens.css` | Tokens compartidos de acción primaria |
| `platform_os/studio/channel/browser/shell/src/application/AuthPage.css` | Acceso/registro en paneles y adaptación móvil |
| `platform_os/studio/channel/browser/shell/src/application/onboarding/ShortRegisterPage.jsx` | Presentación de registro PERSONAL; conserva payload de cuatro campos |
| `platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.css` | Dashboard compacto, widgets y estados |
| `platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.jsx` | Mensaje vacío y CTA contextual a Gastos |
| `platform_os/studio/channel/browser/shell/src/layout/StudioLayout.css` | Sidebar blanco compacto, header azul, hover y drawer responsive |

PREEXISTING_DIRTY_FILES_PRESERVED=YES. Sus siete hashes SHA-256 coinciden con la
evidencia de entrada. También permanecen idénticos los 23 archivos SQL previamente
protegidos (30/30). PREEXISTING_DIRTY_FILES_INCLUDED_IN_COMMIT=NONE.

## Menú y comportamiento

LEFT_SIDEBAR_IMPLEMENTED=YES. La única composición agrupa:

- Operación: Ventas, Compras, Catálogo, Gastos, Vehículos, Talleres.
- Administración: Contabilidad, Clientes, Proveedores, Empleados.
- Análisis: Reportes, Dashboard, BI.
- Configuración: Configuración.

Se conservan `/expenses`, `/fleets/vehicles`, `/dashboard` y los códigos existentes
aplicables. Inicio se presenta como Dashboard en Análisis, conservando su código
`workspace.home` y ruta. Los antiguos placeholders Comercial/Socios de negocio/
Equipo se reemplazan por la organización solicitada; no tenían rutas funcionales.
Los módulos no implementados permanecen deshabilitados, sin rutas ficticias.

EXPENSES_LEFT_NAV=ENABLED_BY_expenses.expense.read.
FLEETS_LEFT_NAV=ENABLED_BY_fleets.vehicle.read.
La selección activa reconoce subrutas delimitadas (`/expenses/new`, no
`/expenses-other`). El drawer existente se cierra al navegar. Se preserva el
MobileTabBar interno de Gastos; no se crea un segundo menú global.

TOP_RIGHT_EXPENSES_SHORTCUT=REMOVED. Se conservan identidad, búsqueda, notificaciones
y Salir en el header. Las reglas CSS previas que ocultan algunos controles en móvil
no se alteran. No se implementa Operando Como ni un rediseño del Dashboard.

## Recargas y cierre de sesión

Antes del cambio, `main.jsx` llamaba al bootstrap sin accessContextSource; recargar
vacía el Runtime y la ruta protegida redirige al login. Se conecta un adaptador HTTP
local del Browser al puerto de bootstrap existente, usando `GET /auth/me` con la
cookie HttpOnly y los permisos efectivos del servidor. Se espera el resultado antes
de montar App. No se guarda identidad ni autorización en localStorage/sessionStorage.

El adaptador valida los identificadores y deja la validación de permisos al límite
RuntimeAccessContext existente. Una sesión ausente, inválida o fallida no restaura
identidad previa. `/api/me/profile` solo enriquece la presentación y su fallo no
invalida una sesión válida. `/auth/me` expone userAccountId, no PartyId: se conserva
`user.accountId` y no se inventa el `actor.id` que devuelve login.

Para que la restauración no revierta un logout, Salir llama al endpoint existente
`POST /auth/logout` y limpia Runtime después de confirmar el cierre. Si falla,
muestra error y no declara la sesión cerrada. El cliente solo reintenta una vez un
rechazo 401/403 cuando faltaba CSRF y la respuesta emitió su cookie diferida; no
reintenta fallos de red. No se cambia CSRF ni la autorización del backend.

BACKEND_CHANGED=NO. Sin migraciones, SQL manual, RUC, organización obligatoria,
modificaciones de gm-expenses/gm-fleets ni integración de vehículos con gastos.

## Validación

| Evidencia final | Resultado |
|---|---|
| Studio contracts | 228 PASS, 25 archivos; 13 pruebas nuevas de sesión/navegación |
| Lint | PASS |
| Build | PASS; 340 módulos transformados |
| PERSONAL_EXPENSES_NAV | PASS |
| PERSONAL_VEHICLES_NAV | PASS |
| DIRECT_ROUTE_EXPENSES | PASS; recarga real desktop y móvil |
| DIRECT_ROUTE_VEHICLES | PASS; recarga real desktop y móvil |
| Crear ABC-1234 / Chevrolet | PASS; formulario normal en nuevo tenant PERSONAL |
| Vehículos → Gastos → Vehículos | PASS; sesión/lista persistidas |
| Logout y acceso posterior a ruta protegida | PASS; retorna al login |
| DESKTOP_WEB | PASS a 1440 x 900, sidebar normal y compacto |
| MOBILE_WEB | PASS a 390 x 844, drawer y ambas pantallas |
| Ancho de página | 1440/1440 desktop y 390/390 móvil; sin overflow global |
| Consola en recorrido autenticado final | Sin errores/advertencias |
| TESTS_FAILED | 0 |

Comandos desde Gystigo: `npm run contracts`, `npm run lint`, `npm run build`, cada
uno con `--workspace=@gypport/platform-os-browser-shell`. El primer intento de
contratos no arrancó por EPERM de `.vite-temp`; se repitió fuera del sandbox con
autorización, sin cambiar dependencias ni debilitar contratos. Se actualizó la
expectativa del contrato de integración al nuevo orden solicitado de grupos.

La aceptación usa una cuenta PERSONAL sintética nueva registrada en la UI,
verificada mediante Mailpit y autenticada por el login normal. Conserva un vehículo
de prueba en su tenant (ABC-1234 / Chevrolet). Se mantienen las cuentas y vehículos
del STEP previo; no se ejecutó SQL manual ni limpieza destructiva.

Capturas inspeccionadas en la carpeta local
`C:/Users/elbur/.codex/visualizations/2026/08/30/01a05471-5d5b-7400-98b0-77b7b0304670/`:
`left-nav-desktop-expenses.png`, `left-nav-desktop-vehicles.png`,
`left-nav-desktop-compact.png`, `left-nav-mobile-menu.png`,
`left-nav-mobile-expenses.png`, `left-nav-mobile-vehicles.png`.
La prueba visual y build corresponden al checkout con el borrador preservado;
no se presenta como una aceptación visual de estilos ya incluidos en HEAD.
El Dashboard general conserva su aviso previo de permisos/contexto; su rediseño
no forma parte del STEP y no impide navegar a los módulos autorizados.

## Archivos del STEP y cierre

Siete archivos existentes modificados: composición BusinessPlatformComposition.js,
StudioNavigation.jsx, StudioHeader.jsx, StudioLayout.jsx, main.jsx, authService.js
y FrontendCanonicalIntegration.contract.mjs.
Tres nuevos: browserSessionSource.js, StudioSessionNavigation.contract.mjs y este
informe. Ninguno era uno de los siete archivos dirty previos. Índice vacío.

NEXT_EXACT_ACTION=DESIGN_GM_EXPENSES_EXPENSE_CASE_FOUNDATION

STOP. No se inicia Expense Case ni la selección de vehículos dentro de gastos.

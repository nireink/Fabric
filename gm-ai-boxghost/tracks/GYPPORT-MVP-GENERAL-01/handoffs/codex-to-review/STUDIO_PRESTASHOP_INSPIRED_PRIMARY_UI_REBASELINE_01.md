# Studio primary shell — execution evidence

PEGAR EN: CHATGPT / CLAUDE — revisión de evidencia y aceptación visual del Owner.

```text
PROJECT=GYPPORT
TRACK=GYPPORT-MVP-GENERAL-01
STEP=STUDIO_PRESTASHOP_INSPIRED_PRIMARY_UI_REBASELINE_01
MODE=CONTROLLED_UI_DISCOVERY_AND_IMPLEMENTATION
AGENT=CODEX
DATE=2026-08-30
STATUS=OWNER_DECISION_REQUIRED
IMPLEMENTATION=IMPLEMENTED
AUTOMATED_AND_BROWSER_VALIDATION=DIRECTLY_CONFIRMED
INDEPENDENT_AUDIT=NOT_PERFORMED
OWNER_VISUAL_ACCEPTANCE=PENDING
```

La implementación y verificación del shell están terminadas. El estado pendiente corresponde a la aceptación visual del Owner, no a autorización para continuar hacia Expense Case. No se atribuye a Codex una auditoría independiente ni aprobación del Owner.

## Continuidad y alcance

- Checkout: `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo`.
- Branch: `feature/gm-fleets-minimum-vehicle-master-01`.
- HEAD inicial/final: `beb88046837a1afce8b1d25b722ed80b0adb959c`.
- Predecesor: `STUDIO_LEFT_NAVIGATION_MODULE_INTEGRATION_01.md`, existente y preservado.
- Working tree inicial: 17 archivos modificados/no rastreados; índice vacío.
- Autorización: descubrimiento e implementación de presentación del shell. Sin staging, commit, push, cambios remotos, reset, backend, permisos ni base de datos.
- Arquitectura conservada: bootstrap → composición de Business Platform → NavigationRegistry → resolveNavigationTree → StudioNavigation; la sesión sigue viniendo de las fuentes existentes del servidor.
- La implementación segura de logout y la hidratación de sesión ya eran cambios locales del STEP anterior. No se alteraron sus semánticas en este STEP. El diff contra HEAD incluye esos cambios anteriores y no debe atribuirse enteramente a esta intervención.

## Descubrimiento de referencias, antes de editar Studio

Raíz de referencias: `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\UI_Experiments`.

```text
PROTOTYPES_FOUND=ui-prototype React/Vite; Gystigo_V20260729; Gystigo_V20260713; Gystigo_Ultimate; Gystigox; g-modules/gm-service-management/gypport-app-complete.jsx
MOST_RELEVANT_PRESTASHOP_STYLE_PROTOTYPE=E-commerce-develop/dashimg/ui-prototype
OTHER_RELEVANT_MENU_DRAFTS=StudioShell histórico de Gystigo_V20260729/V20260713; menús de cuenta de Dashboard en Gystigo_Ultimate/Gystigox
SOURCE_PROTOTYPE_USED=E-commerce-develop/dashimg/ui-prototype, frontend Header/Sidebar/variables/App CSS
```

Primero se revisó el prototipo exacto indicado: README, componentes Header/Sidebar y sus CSS, variables y App CSS. Su backend mock no se ejecutó ni se trasladó al Host. Después se inventarió el directorio amplio, excluyendo dependencias y compilados. También se identificaron Gystigo_Basic, Gystigo_V001 y Bacl; no se afirma revisión exhaustiva de cada archivo de esos árboles. Los HTML adicionales encontrados eran principalmente entradas de Vite.

Se inventariaron 31 PNG de `E-commerce-develop/dashimg`. Se inspeccionaron visualmente `Screenshot 2026-05-25 220602.png` (sidebar completo, barra superior y dropdown de usuario; mejor referencia) y `Screenshot 2026-06-10 055848.png` (menú lateral). Los otros drafts aportaron comparaciones de menú y perfil, pero contienen navegación hardcoded o contextos simulados que no se incorporaron.

Se reutilizó únicamente la idea estructural: barra superior continua, menú lateral compacto y dropdown de cuenta. No se copiaron logos, assets, código ni identidad de PrestaShop. Los pequeños SVG nuevos son trazados propios; los colores y medidas usan tokens GYPPORT existentes.

## Resultado implementado

- Shell actual refinado, no reemplazado por el prototipo.
- Barra superior fija de 56 px de extremo a extremo: identidad GYPPORT, Business Studio, búsqueda visual deshabilitada y marcada Próximamente, ubicación discreta de notificaciones también deshabilitada sin contador ficticio.
- Sidebar persistente de 216 px, compacto de 60 px: iconos y etiquetas, grupos plegables y selección con fondo/acento cyan. Preferencia de compacto conservada entre módulos mediante una única clave de presentación `gypport.studio.sidebar.compact` en sessionStorage, tolerando almacenamiento no disponible. No almacena identidad, tokens ni permisos.
- Mobile: drawer de hasta 300 px, botón de apertura y cierre, scrim, cierre al navegar; el sidebar cerrado se oculta también de la navegación accesible mediante visibility. Avatar/dropdown siempre accesible.
- Dropdown: nombre de la sesión, contexto Personal, Mi perfil → `/mi-perfil`, Cerrar sesión → flujo seguro existente. Escape devuelve foco al disparador y cierra; clic exterior cierra. No se simula un selector de organizaciones ni capacidades de WP_04.
- No se encontró capacidad canónica de foto de perfil implementada. `UserAvatar` muestra iniciales y admite un `src` de presentación para una futura integración, con fallback ante fallo. Actualmente no se proporciona imagen, no hay uploads ni persistencia binaria.
- Centro reservado al módulo; no hay enlace duplicado a Gastos en el header. Se mantienen las vistas y los componentes propios de cada módulo, incluidos los filtros y navegación inferior móvil ya existentes de Gastos.

### Registry y agrupación

| Grupo | Entradas |
|---|---|
| Inicio | Inicio → `/dashboard` |
| Operación | Ventas, Compras, Catálogo, Gastos → `/expenses`, Vehículos → `/fleets/vehicles`, Talleres |
| Administración | Contabilidad, Clientes, Proveedores, Empleados |
| Análisis | Reportes, BI |
| Configuración | Configuración |

Administración/Análisis/Configuración se conservan del estado funcional local previo. Solo Inicio se separó como grupo y se retiró su aparición en Análisis para evitar duplicación. Las entradas sin implementación siguen deshabilitadas conforme al registry; no se crearon pantallas ni rutas nuevas. Se preservan `expenses.expense.read`, `fleets.vehicle.read`, metadata y resolución de permisos.

## Verificación automatizada y de navegador

Comandos ejecutados desde Gystigo:

```text
npm run contracts --workspace=@gypport/platform-os-browser-shell
npm run lint --workspace=@gypport/platform-os-browser-shell
npm run build --workspace=@gypport/platform-os-browser-shell
```

Resultado final después de los ajustes visuales: 26 archivos de contratos, 231 tests PASS, 0 FAIL; lint PASS; build de design-system y shell PASS. Se mantuvieron los contratos de sesión/permisos y se ajustaron expectativas de agrupación y presentación; se agregó cobertura del estado honesto de búsqueda y avatar. Las pruebas SSR no sustituyen la interacción real descrita a continuación.

Navegador conectado a `http://localhost:5173`, Host existente en 8080. Se reutilizó una cuenta sintética PERSONAL preexistente, sin crear usuarios, gastos ni vehículos en este STEP. La tabla existente contiene el vehículo de prueba ABC-1234 / Chevrolet. No se incluyen credenciales en este informe.

| Comprobación real | Resultado |
|---|---|
| Login PERSONAL en escritorio y móvil → shell con nombre real | PASS |
| Gastos → Vehículos → Inicio → Gastos | PASS de navegación; limitación previa de contenido Inicio indicada abajo |
| `/expenses` y `/fleets/vehicles`, navegación lateral | PASS |
| Reload de ambas rutas en escritorio y móvil | PASS, sesión mantenida y vista del módulo visible |
| Dropdown, nombre/contexto Personal, Mi perfil | PASS en escritorio y móvil |
| Logout en escritorio y móvil | PASS, vuelve a login |
| Acceso a `/expenses` después de logout de escritorio | PASS, redirige a login |
| Escape y clic exterior del menú de cuenta | PASS |
| Grupos plegables y menú compacto; navegación entre módulos conserva compacto | PASS |
| Drawer móvil, cierre explícito y cierre al elegir módulo | PASS |
| 1440×900, 1366×768, 390×844 | PASS visual/técnico; aceptación estética del Owner pendiente |

Medidas DOM finales: ancho de documento igual al viewport en 1440, 1366 y 390; sin overflow horizontal del shell. Alto de documento igual a 900, 768 y 844 en las vistas capturadas. El scroll horizontal interno de filtros de Gastos en móvil es preexistente y se mantiene. Se corrigió el alto mínimo del área central para evitar un scroll vertical extra introducido por la nueva barra fija.

Las capturas inspeccionadas están en `C:\Users\elbur\.codex\visualizations\2026\08\30\01a05471-5d5b-7400-98b0-77b7b0304670`:

- `studio-primary-1440.png`: Gastos y dropdown de cuenta.
- `studio-primary-1366.png`: Vehículos y navegación expandida.
- `studio-primary-390-content.png`: Gastos móvil.
- `studio-primary-390-drawer.png`: drawer móvil.
- `studio-primary-390-account.png`: dropdown móvil sobre Vehículos.

### Límites y hallazgos

1. Inicio conserva el DashboardHost existente y su mensaje «Acceso no disponible / Se requiere un contexto seguro de tenant, usuario y permisos» para esta cuenta PERSONAL. La ruta funciona, pero no se declara funcionalmente habilitado el dashboard para esa cuenta. No se modificaron permisos ni DashboardHost para esconder esta limitación previa.
2. Búsqueda global y notificaciones no están implementadas: UI explícitamente deshabilitada, sin resultados, contadores ni atajos fingidos.
3. No hay auditoría independiente ni aceptación visual del Owner en esta entrega. No se afirma compatibilidad verificada en otros navegadores o viewports diferentes de los solicitados.
4. Durante la validación se detectó que el atributo HTML hidden impedía mostrar grupos colapsados en modo compacto por estilos globales; se sustituyó por una clase de presentación comprobada en navegador. Un selector de expansión encontró cero elementos porque el layout se remontaba al cambiar módulo; se verificó el estado real, se conservó la preferencia compacta y se repitió la comprobación con éxito. Estos intentos no fueron fallos de la suite de contratos.
5. Hubo errores operativos de lectura/validación de patch y una reconexión del navegador durante el trabajo, recuperados sin descarte de archivos. Git emitió una advertencia de lectura del ignore global por permisos; status, diff e integridad por hashes se obtuvieron correctamente. No se ocultaron fallos de tests.

## Conservación y archivos de esta intervención

Los siete borradores visuales originales conservan SHA-256 idéntico al inicio: Button.tsx, tokens.css, AuthPage.css, DashboardHost.css, DashboardHost.jsx, ShortRegisterPage.jsx y StudioLayout.css. Se reutilizan su identidad, tokens y componentes sin editar esos archivos. `StudioPrimaryShell.css` aplica ajustes acotados al shell por encima del CSS anterior.

También conservan SHA-256 idéntico authService.js, browserSessionSource.js, main.jsx y el informe del STEP previo. Los seis archivos previos restantes fueron refinados dentro del alcance autorizado. Las 67 referencias fuente/capturas incluidas en el control previo de UI_Experiments mantienen SHA-256 idéntico; no se ejecutaron escrituras en UI_Experiments.

Rutas relativas al checkout Gystigo; **13 archivos tocados por este STEP**: seis ya dirty/untracked, StudioSidebar que estaba tracked y limpio, y seis archivos creados:

```text
platform_os/studio/channel/browser/shell/src/layout/StudioHeader.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioLayout.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioNavigation.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioSidebar.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioIcon.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioPrimaryShell.css
platform_os/studio/channel/browser/shell/src/layout/StudioUserMenu.jsx
platform_os/studio/channel/browser/shell/src/layout/UserAvatar.jsx
platform_os/studio/composition/business-platform/BusinessPlatformComposition.js
platform_os/studio/verification/integration/FrontendCanonicalIntegration.contract.mjs
platform_os/studio/verification/contracts/browser/StudioSessionNavigation.contract.mjs
platform_os/studio/verification/contracts/browser/StudioPrimaryShell.contract.mjs
docs/ai/handoffs/codex-to-review/STUDIO_PRESTASHOP_INSPIRED_PRIMARY_UI_REBASELINE_01.md
```

No hay cambios de backend, dominios gm-expenses/gm-fleets, APIs, SQL, Flyway, reglas de autenticación, RUC/SRI ni Expense Case. Las operaciones normales de login/logout usan el runtime existente; no se ejecutó ninguna modificación SQL, reset o seed.

## Cierre solicitado

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=STUDIO_PRESTASHOP_INSPIRED_PRIMARY_UI_REBASELINE_01
STATUS=OWNER_DECISION_REQUIRED
SOURCE_PROTOTYPE_USED=UI_Experiments/E-commerce-develop/dashimg/ui-prototype
UI_EXPERIMENTS_REVIEWED=YES; inventario y referencias descritos arriba
CURRENT_SHELL_REPLACED_OR_REFINED=REFINED
LEFT_MENU_STYLE=COMPACT_HIERARCHICAL_COLLAPSIBLE
TOP_BAR_STYLE=FIXED_GYPPORT_SEARCH_ACCOUNT_DROPDOWN
NAVIGATION_GROUPS=Inicio; Operación; Administración; Análisis; Configuración
EXPENSES_NAV=PASS
VEHICLES_NAV=PASS
TOP_RIGHT_USER_MENU=PASS
PROFILE_NAV=PASS
LOGOUT=PASS
AVATAR_IMPLEMENTATION=INITIALS_FALLBACK_OPTIONAL_PRESENTATION_IMAGE_SLOT
GLOBAL_SEARCH_STATUS=DISABLED_PROXIMAMENTE_NO_BACKEND
DESKTOP_1440=PASS
DESKTOP_1366=PASS
MOBILE_390=PASS
DIRECT_ROUTE_EXPENSES=PASS
DIRECT_ROUTE_VEHICLES=PASS
PREEXISTING_VISUAL_DRAFT_REUSED=YES
PREEXISTING_DIRTY_FILES_PRESERVED=YES; 7 originales idénticos; refinamientos compatibles de 6 archivos previos
BACKEND_CHANGED=NO
DATABASE_CHANGED=NO
FLYWAY_CHANGED=NO
STUDIO_TESTS=231_PASS_IN_26_FILES
LINT=PASS
BUILD=PASS
TESTS_FAILED=0
FILES_CHANGED=13; lista exacta arriba
LOCAL_COMMITS_CREATED=0
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
NEXT_EXACT_ACTION=OWNER_VISUAL_ACCEPTANCE_OF_PRIMARY_STUDIO_SHELL
```

Estado final completo del checkout (incluye trabajo anterior, no es una allowlist de staging):

```text
 M design_system/src/components/Button/Button.tsx
 M design_system/src/tokens/tokens.css
 M platform_os/studio/channel/browser/shell/src/application/AuthPage.css
 M platform_os/studio/channel/browser/shell/src/application/authentication/authService.js
 M platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.css
 M platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.jsx
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
?? docs/ai/handoffs/codex-to-review/STUDIO_PRESTASHOP_INSPIRED_PRIMARY_UI_REBASELINE_01.md
?? platform_os/studio/channel/browser/shell/src/application/authentication/browserSessionSource.js
?? platform_os/studio/channel/browser/shell/src/layout/StudioIcon.jsx
?? platform_os/studio/channel/browser/shell/src/layout/StudioPrimaryShell.css
?? platform_os/studio/channel/browser/shell/src/layout/StudioUserMenu.jsx
?? platform_os/studio/channel/browser/shell/src/layout/UserAvatar.jsx
?? platform_os/studio/verification/contracts/browser/StudioPrimaryShell.contract.mjs
?? platform_os/studio/verification/contracts/browser/StudioSessionNavigation.contract.mjs
```

Índice vacío, HEAD sin cambios, `git diff --check` PASS. No se hizo staging ni commit porque AGENTS.md requiere autorización expresa para ambos y este STEP no la otorgó. No se solicita autorización adicional para realizar trabajo ya autorizado. El siguiente gate es exclusivamente la aceptación visual del Owner. STOP: no iniciar Expense Case.

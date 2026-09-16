# Studio top header — branding and account alignment

PEGAR EN: CHATGPT / CLAUDE — evidencia para aceptación visual del Owner.

```text
PROJECT=GYPPORT
TRACK=GYPPORT-MVP-GENERAL-01
STEP=STUDIO_TOP_HEADER_BRANDING_AND_ACCOUNT_REBASELINE_02
MODE=CONTROLLED_UI_IMPLEMENTATION
AGENT=CODEX
DATE=2026-08-30
STATUS=OWNER_DECISION_REQUIRED
IMPLEMENTATION=IMPLEMENTED
VALIDATION=DIRECTLY_CONFIRMED
OWNER_VISUAL_ACCEPTANCE=PENDING
INDEPENDENT_AUDIT=NOT_PERFORMED
```

La implementación y validación están terminadas. Pendiente únicamente la aceptación visual del Owner. No se reabren Dashboard PERSONAL, navegación, iconografía ni comportamiento de cuenta ya aceptados.

## Continuidad y auditoría previa

- Checkout: `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo`.
- Branch: `feature/gm-fleets-minimum-vehicle-master-01`.
- HEAD inicial/final: `beb88046837a1afce8b1d25b722ed80b0adb959c`.
- STEP previo: `STUDIO_PERSONAL_DASHBOARD_USER_MENU_AND_ICON_REFINEMENT_01`, informe preservado.
- 29 archivos dirty/untracked al inicio, índice vacío; hashes SHA-256 registrados antes de editar.
- El header previo era un único flex: la marca ocupaba solo el ancho de su texto y no el de la columna lateral. El texto principal tenía 15 px y un espaciado vertical excesivo para el bloque de marca.
- Fuentes de ancho actuales verificadas: `--studio-sidebar=216px`, `--studio-sidebar-compact=60px`; alto `--studio-topbar=56px`. Se reutilizan sin crear medidas independientes para la marca.

## Implementación acotada

El header ahora usa tres zonas Grid: marca, búsqueda y acciones. La primera columna usa exactamente `var(--studio-sidebar)`; en compacto usa `var(--studio-sidebar-compact)`. El sidebar conserva sus medidas, navegación, estado y comportamiento previos. La transición de columna acompaña la transición existente de 180 ms.

La marca base es `GYPPORT® / Business Platform`. El texto principal aumenta a 22 px, peso 800, con el bloque de dos líneas centrado verticalmente y padding alineado con la navegación. A 390 px se usa 20 px y se oculta la segunda línea. No se muestra Business Studio en el header.

Con sidebar compacto, el bloque adopta un monograma de 22 px dentro de la columna de 60 px, conservando el nombre completo mediante title/aria-label. No retiene la columna expandida.

La búsqueda queda alineada al inicio del espacio restante, con margen interno de 24 px y ancho máximo 560 px. Sigue deshabilitada y marcada Próximamente. En 1024 px y móvil se oculta, respetando el breakpoint de drawer existente. No se añadieron backend, resultados ni atajos ficticios.

Cuenta, avatar, dropdown, Lucide, saludo, perfil, contexto y logout conservan sus componentes y comportamiento. Solo se ajustaron los mínimos de ancho y la colocación de la zona derecha para permitir truncado sin expulsar controles.

## Nombre comercial: fuente y límites

La fachada existente `RuntimeTenant.js` expone `getRuntimeOrganization()` desde el company/organization del Runtime, con nombres `name` o `companyName`. `getRuntimeOrganizationName()` también puede caer al nombre del tenant, y RuntimeBranding se sincroniza desde Kernel: esos fallbacks genéricos no se consideran una identidad comercial autenticada.

StudioLayout consume `getRuntimeOrganization().name/companyName` solo cuando existe usuario, `tenant.activeOrganizationId` no es null y el `organization.id` coincide con dicho ID activo. No se sustituye por códigos de tenant, nombre personal, branding de Kernel o valores estáticos. Si no hay nombre válido no vacío, se usa la marca base.

La sesión actual (`/auth/me` y login) transmite activeOrganizationId y no transmite un nombre comercial; el bootstrap actual no llena esa organización con un nombre. Por ello la ejecución PERSONAL real muestra el fallback. No se implementó hidratación nueva, switching ni endpoint adicional. La variante comercial muestra `<nombre> / Powered by GYPPORT®` cuando recibe el valor válido.

## Fixture de presentación

Se agregó un fixture aislado y explícitamente rotulado como simulación:

`http://localhost:5173/fixtures/header-branding.html`

Renderiza el **mismo StudioHeader** y sus estilos, con props de nombre comercial y usuario largos. Tiene controles para vaciar la marca y compactar la columna. No ejecuta bootstrap, no escribe en Runtime autenticado, no hace peticiones API ni crea organizaciones/sesiones. La columna de referencia usa las clases/tokens reales del sidebar; no contiene navegación de negocio simulada.

El fixture no forma parte de la entrada de producción. Se verificó que `dist` contiene index.html, assets y el recurso público previo vite.svg, sin el fixture.

## Validación real y visual

Se reutilizó la cuenta sintética PERSONAL existente en `localhost:5173`, con Host existente en 8080. No se crearon datos. Login, perfil desde dropdown y logout se comprobaron sin modificar sus implementaciones. Dashboard siguió mostrando PERSONAL_HOME.

| Viewport | Marca/sidebar desktop | Ancho documento | Cuenta: borde derecho | Resultado |
|---|---:|---:|---:|---|
| 1920×1080 | 216 / 216 px | 1920 px | 1900 px | PASS |
| 1440×900 | 216 / 216 px | 1440 px | 1420 px | PASS |
| 1366×768 | 216 / 216 px | 1366 px | 1346 px | PASS |
| 1024×768 | Drawer; marca flexible | 1024 px | 1012 px | PASS |
| 390×844 | Drawer; marca flexible | 390 px | 378 px | PASS |

Desktop compacto real: marca/sidebar **60 / 60 px**; búsqueda comienza en x=84; alto de barra 56 px. Con nombre comercial largo en fixture compacto, misma medición 60/60 px. La variante expandida inicia la búsqueda en x=240 y no invade la marca.

Nombre comercial de prueba: ancho natural 919 px, espacio disponible de texto 183 px en la columna desktop; `overflow:hidden`, `text-overflow:ellipsis`, `white-space:nowrap` y title con el nombre completo. El usuario de prueba ocupa 383 px naturales y se trunca a 190 px. En móvil su nombre se oculta y quedan avatar/flecha; el comercial también se trunca. Se probaron nombres largos en los cinco viewports sin scroll horizontal ni aumento del ancho de columna.

Las capturas de los cinco viewports, el estado compacto y los fixtures se inspeccionaron visualmente. Se verificaron las dimensiones sobre DOM visible; no se alteró estado oculto del navegador. Viewport restablecido al terminar.

Capturas bajo `C:\Users\elbur\.codex\visualizations\2026\08\30\01a05471-5d5b-7400-98b0-77b7b0304670`:

- `header-02-1920.png`, `header-02-1440.png`, `header-02-1366.png`.
- `header-02-1024.png`, `header-02-390.png`, `header-02-collapsed.png`.
- `header-02-long-name-1440.png`, `header-02-long-name-390.png`, `header-02-long-name-collapsed.png`.

## Comprobaciones automatizadas

- `npm run contracts --workspace=@gypport/platform-os-browser-shell`: **247/247 PASS, 27 archivos**, sin cambiar contratos existentes.
- `npm run lint --workspace=@gypport/platform-os-browser-shell`: PASS final. El primer intento detectó un export faltante en el fixture para Fast Refresh; se corrigió exportando su componente y se repitió lint. No se deshabilitaron reglas.
- `npm run build --workspace=@gypport/platform-os-browser-shell`: PASS, incluido prebuild del design-system.
- Build: 2145 módulos; JS 391.46 kB / 113.22 kB gzip.
- `git diff --check`: PASS. Índice vacío, HEAD sin cambios.
- Se observaron warnings previos de Git sobre ignore global y conversión CRLF; no se modificó configuración global ni se descartó trabajo.

## Archivos e integridad

6 archivos de este STEP, relativos al checkout:

```text
platform_os/studio/channel/browser/shell/src/layout/StudioHeader.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioLayout.jsx
platform_os/studio/channel/browser/shell/src/layout/StudioPrimaryShell.css
platform_os/studio/channel/browser/shell/fixtures/header-branding.html
platform_os/studio/channel/browser/shell/fixtures/HeaderBrandingFixture.jsx
docs/ai/handoffs/codex-to-review/STUDIO_TOP_HEADER_BRANDING_AND_ACCOUNT_REBASELINE_02.md
```

Comparación SHA-256: de los 29 archivos iniciales, **26 permanecen idénticos**. Solo cambiaron los tres archivos de presentación listados. DashboardHost, resolveDashboard, Expenses, Vehicles, registry/composición, StudioNavigation, StudioSidebar, StudioUserMenu, UserAvatar, StudioIcon, autenticación, tokens, CSS visual original, dependencias e informes previos no se tocaron. No se escribieron archivos en UI_Experiments.

La modificación de StudioLayout se limita a obtener el nombre de la organización activa y pasarlo al header; el handler de logout y el resto de sus comportamientos permanecen iguales. Los cambios de CSS se limitan a la geometría/branding del header y mínimos de ancho de cuenta necesarios para su ajuste.

## Reporte solicitado

`git status --short` final, incluido trabajo anterior (no es allowlist de staging):

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
?? docs/ai/handoffs/codex-to-review/STUDIO_TOP_HEADER_BRANDING_AND_ACCOUNT_REBASELINE_02.md
?? platform_os/studio/channel/browser/shell/fixtures/HeaderBrandingFixture.jsx
?? platform_os/studio/channel/browser/shell/fixtures/header-branding.html
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
STEP=STUDIO_TOP_HEADER_BRANDING_AND_ACCOUNT_REBASELINE_02
STATUS=OWNER_DECISION_REQUIRED
HEADER_LAYOUT=Grid: marca / búsqueda / notificaciones y cuenta
BRAND_AREA_WIDTH_SOURCE=--studio-sidebar; --studio-sidebar-compact
BASE_BRAND_PRIMARY=GYPPORT®
BASE_BRAND_SECONDARY=Business Platform
ACTIVE_COMPANY_PRIMARY_SOURCE=getRuntimeOrganization().name/companyName; ID debe coincidir con tenant.activeOrganizationId
ACTIVE_COMPANY_SECONDARY=Powered by GYPPORT®
LONG_NAME_TRUNCATION=PASS
SIDEBAR_ALIGNMENT=PASS
COLLAPSED_SIDEBAR_ALIGNMENT=PASS
SEARCH_AREA=PASS
ACCOUNT_TRIGGER=PASS
ACCOUNT_DROPDOWN=PASS
LUCIDE_REUSED=YES
NEW_ICON_LIBRARY_ADDED=NO
DESKTOP_1920=PASS
DESKTOP_1440=PASS
DESKTOP_1366=PASS
TABLET_1024=PASS
MOBILE_390=PASS
BACKEND_CHANGED=NO
DATABASE_CHANGED=NO
FLYWAY_CHANGED=NO
FILES_CHANGED=6; lista exacta arriba
STUDIO_TESTS=247_PASS_IN_27_FILES
LINT=PASS
BUILD=PASS
TESTS_FAILED=0; incidencia inicial de lint documentada y corregida
LOCAL_COMMITS_CREATED=0
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
NEXT_EXACT_ACTION=OWNER_VISUAL_ACCEPTANCE_TOP_HEADER
```

No se afirma una organización comercial real activa: esa variante se probó mediante fixture autorizado. No se afirma auditoría independiente ni aceptación estética del Owner. No se hizo staging/commit porque AGENTS.md exige autorización expresa y no fue otorgada. No hubo intervención SQL; login/logout normales usan el backend existente. STOP: no iniciar Expense Case.

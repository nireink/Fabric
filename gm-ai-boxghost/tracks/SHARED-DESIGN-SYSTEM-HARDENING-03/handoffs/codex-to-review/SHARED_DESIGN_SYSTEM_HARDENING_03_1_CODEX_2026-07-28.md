# SHARED_DESIGN_SYSTEM_HARDENING_03_1_CODEX_2026-07-28

**Track:** `SHARED-DESIGN-SYSTEM-HARDENING-03`

**Step:** `03.1`

**Mode:** Corrección focalizada de hallazgos aceptados

**Agent:** Codex

**Resultado:** `READY_FOR_CLAUDE_VERIFICATION`

## 1. Identidad del repositorio

| Campo | Valor |
|---|---|
| Ruta local real | `D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo` |
| Raíz Git | `D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo` |
| Rama | `master` |
| HEAD | `1f58cac38a9e5b1e55d2444db660dbec3223f6b6` |
| Relación remota | `master...origin/master [ahead 2]` |

Git requirió `-c safe.directory=D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo`
para las consultas ejecutadas por el usuario aislado. No se modificó la
configuración global de Git.

## 2. Estado inicial

El STEP comenzó sobre el working tree real todavía sin commit. El estado
inicial fue:

```text
## master...origin/master [ahead 2]
 M AGENTS.md
 M CLAUDE.md
 M README.md
 M docs/ai/shared/AI_COLLABORATION.md
 M docs/architecture/ACTIVE_TRACKS.md
 M docs/architecture/BOUNDARY_RULES.md
 M docs/architecture/STRUCTURE_CANONICAL.md
 D platform_os/studio/channel/browser/shell/package-lock.json
 M platform_os/studio/channel/browser/shell/package.json
 M platform_os/studio/channel/browser/shell/src/app/authentication/LoginPage.jsx
 M platform_os/studio/channel/browser/shell/src/app/onboarding/ShortRegisterView.jsx
 M platform_os/studio/channel/browser/shell/src/app/shell/StudioShell.css
 M platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
 M platform_os/studio/channel/browser/shell/src/main.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/party/form/PartyForm.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/party/form/section/PartyIdentitySection.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/party/page/PartyListPage.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/tax/form/section/TaxProfileSection.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/workforce/employee/form/EmployeeForm.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/workforce/employee/page/EmployeeTeamPage.jsx
 M platform_os/studio/channel/browser/shell/vite.alias.js
 M platform_os/studio/channel/browser/shell/vite.config.js
 D platform_os/studio/engine/framework/theme/base/reset.css
 D platform_os/studio/engine/framework/theme/base/typography.css
 D platform_os/studio/engine/framework/theme/base/variables.css
 D platform_os/studio/engine/framework/theme/dark/dark-theme.css
 D platform_os/studio/engine/framework/theme/light/light-theme.css
 D platform_os/studio/engine/framework/theme/print/print-theme.css
 D platform_os/studio/engine/framework/theme/style/runtime-theme.css
?? CHATGPT.md
?? design_system/
?? docs/ai/handoffs/codex-to-review/SHARED_DESIGN_SYSTEM_RECONCILIATION_01_1_CODEX_2026-07-28.md
?? docs/ai/reviews/accepted/SHARED_DESIGN_SYSTEM_DIRECT_AUDIT_02_1_CLAUDE_2026-07-28.md
?? docs/ai/reviews/accepted/SHARED_DESIGN_SYSTEM_DIRECT_AUDIT_02_2_CLAUDE_2026-07-28.md
?? docs/ai/shared/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0(1).md
?? docs/architecture/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md
?? docs/governance/
?? package-lock.json
?? package.json
```

`git diff --check` global confirmó el hallazgo preexistente y fuera de alcance
en `docs/ai/shared/AI_COLLABORATION.md`: trailing whitespace en las líneas 3-6
y una línea en blanco final en la línea 149. Este archivo no fue corregido.

## 3. Archivos modificados por este STEP

```text
design_system/README.md
design_system/src/architectureBoundary.test.ts
design_system/src/themes/tenantTheme.test.ts
design_system/src/themes/tenantTheme.ts
design_system/src/tokens/brand.ts
design_system/src/tokens/tokens.css
docs/ai/handoffs/codex-to-review/SHARED_DESIGN_SYSTEM_HARDENING_03_1_CODEX_2026-07-28.md
```

No se modificó ningún archivo de backend, database, Docker, Toolchain,
`platform_contracts/` ni dependencias.

## 4. Implementación exacta

### F1 — `onSecondary`

- `GYPPORT_BRAND` declara como contrato canónico:
  `secondary: "#29A9E0"` y `onSecondary: "#06204D"`.
- `GYPPORT_DEFAULT_THEME` conserva y publica ese foreground corporativo.
- `createTenantTheme()` usa `#06204D` únicamente cuando no se proporciona un
  `secondary` de tenant.
- Cuando el tenant proporciona un `secondary`, incluso si es un hexadecimal
  válido de marca, `onSecondary` se deriva mediante
  `readableForeground(secondary)`.
- `TenantThemeInput` no recibió un override público nuevo. La API no prometía
  esa capacidad y este STEP no la amplía.
- `TenantTheme.onSecondary` representa los dos resultados automáticos
  (`#000000` y `#FFFFFF`) más el valor corporativo canónico `#06204D`.
- `applyGypportTheme()` delega al tema predeterminado sin convertir sus colores
  en overrides de tenant.
- `applyTenantTheme()` continúa publicando
  `--gyp-color-on-secondary`.
- `tokens.css` declara
  `--color-on-secondary: var(--gyp-color-on-secondary)` dentro de `@theme
  inline`, habilitando las utilidades Tailwind del namespace de color, como
  `text-on-secondary` y `bg-on-secondary`, cuando son usadas por una fuente.
- `themes.css` ya declaraba `#06204d`; no necesitó modificación. La prueba
  compara el valor estático sin sensibilidad a mayúsculas y confirma paridad
  con el runtime.
- `README.md` documenta el foreground corporativo, su cumplimiento AA, el
  cálculo para un `secondary` de tenant y la ausencia de override directo.

La ejecución contra el paquete compilado produjo:

```text
default secondary    = #29A9E0
default onSecondary  = #06204D
default contrast     = 5.9370097511034565
custom secondary     = #ABCDEF
custom onSecondary   = #000000
custom contrast      = 12.710513042069605
```

No se cambió el valor corporativo automáticamente a negro.

### F2 — architecture boundary

- El filtro usa exactamente:

  ```ts
  /\.test\.(ts|tsx)$/
  ```

- No se agregaron exclusiones para `.spec.ts` ni `.spec.tsx`.
- El helper construye rutas mediante `node:path.join`, por lo que el contrato
  es portable en Windows.
- La validación de violaciones se mantiene sobre archivos productivos.
- El fixture se crea bajo el directorio temporal del sistema, contiene:
  `Contract.test.ts`, `Component.test.tsx` y `Productive.tsx`, y se elimina en
  `finally`.
- Los dos archivos de prueba contienen imports prohibidos y quedan excluidos.
- `Productive.tsx` contiene un import prohibido, permanece en el escaneo y se
  reporta como violación. El contrato real del paquete continúa exigiendo cero
  violaciones productivas.

## 5. Pruebas agregadas o modificadas

`tenantTheme.test.ts` ahora cubre:

1. tema predeterminado con `onSecondary === "#06204D"`;
2. contraste del foreground corporativo `>= 4.5`;
3. `secondary` personalizado con foreground igual a
   `readableForeground(secondary)`;
4. contraste mínimo del resultado automático;
5. consistencia entre `themes.css` y `createTenantTheme()`;
6. exposición de `--color-on-secondary` mediante `@theme`;
7. publicación de `--gyp-color-on-secondary` por `applyTenantTheme()`.

`architectureBoundary.test.ts` ahora cubre:

1. exclusión de `.test.ts`;
2. exclusión de `.test.tsx`;
3. inclusión de un `.tsx` productivo;
4. detección de una importación productiva prohibida;
5. ausencia de imports prohibidos en el código productivo real.

El paquete pasó `2` archivos y `11/11` pruebas.

## 6. Comandos y resultados

| Comando | Resultado |
|---|---|
| `npm run typecheck:design-system` | PASS |
| Primer `npm run test:design-system` | FAIL: el fixture comparaba una ruta creada con `join()` contra una ruta interna construida con `/`; se corrigió el helper para usar `join()` |
| `npm run test:design-system` final | PASS; 2 archivos, 11/11 pruebas |
| `npm run build:design-system` | PASS; 11 módulos, `styles.css` 16.46 kB, `index.js` 8.09 kB |
| Primer `npm run test:frontend` dentro del sandbox | FAIL de entorno: `EPERM` al crear `shell/node_modules/.vite-temp/vitest.config...mjs` |
| `npm run test:frontend` fuera del sandbox | PASS; 20 archivos, 187/187 pruebas |
| Primer `npm run build:frontend` dentro del sandbox | design system PASS; shell FAIL de entorno por el mismo `EPERM` de `.vite-temp` |
| `npm run build:frontend` fuera del sandbox | PASS; design system y shell, 308 módulos |
| `npm run lint --workspace=@gypport/platform-os-browser-shell` | PASS |
| `git diff --check -- <6 rutas fuente>` | PASS, sin salida; las rutas están todavía no rastreadas |
| `git diff --no-index --check` de cada una de las 6 rutas fuente contra un archivo temporal vacío | PASS 6/6; comprobación suplementaria que sí incluye el contenido no rastreado |
| Primer chequeo final de las 7 rutas, incluido este informe | FAIL: cuatro espacios de salto Markdown introducidos en el encabezado del informe; corregidos antes de la puerta final |
| Búsqueda independiente de imports prohibidos en `.ts/.tsx` productivos | PASS; cero coincidencias |
| `git ls-files` filtrado por `node_modules/` o `dist/` | PASS; cero rutas versionadas |

Los `dist/` generados por los builds permanecen ignorados. No se modificó
`node_modules/`, no se ejecutó `npm ci`, `npm install` ni actualización de
dependencias.

## 7. Aspectos deliberadamente no corregidos

- No se agregó script ni configuración lint propios para `design_system`.
- No se creó API de restauración o reset de tema.
- No se crearon generadores de tokens para Flutter, Dart o Python.
- No se creó `platform_contracts/`.
- No se hicieron refactorizaciones generales.
- No se modificaron backend, database, Docker ni Toolchain.
- No se corrigió whitespace de `docs/ai/shared/AI_COLLABORATION.md`.
- No se modificaron dependencias ni lockfiles.
- No se agregaron exclusiones `.spec.ts` o `.spec.tsx`.

## 8. Integridad de informes anteriores

| Informe | SHA-256 inicial y final |
|---|---|
| `SHARED_DESIGN_SYSTEM_RECONCILIATION_01_1_CODEX_2026-07-28.md` | `937141AC382CA73E3A97C1B8943A3495F8B10A5A9E0377F5FFD3E282CE786D50` |
| `SHARED_DESIGN_SYSTEM_DIRECT_AUDIT_02_1_CLAUDE_2026-07-28.md` | `2B0FC9C9BF4626E9B1F7BAF41CCED76691B3E503906D2A208E43E1114A9C7566` |
| `SHARED_DESIGN_SYSTEM_DIRECT_AUDIT_02_2_CLAUDE_2026-07-28.md` | `651B2124BFEFE4819F8E58E54E76A97D2F8B5ED0A908EB71F5CA79C0FF55DB05` |

Los tres permanecen byte a byte intactos.

## 9. `git status -sb` final

```text
## master...origin/master [ahead 2]
 M AGENTS.md
 M CLAUDE.md
 M README.md
 M docs/ai/shared/AI_COLLABORATION.md
 M docs/architecture/ACTIVE_TRACKS.md
 M docs/architecture/BOUNDARY_RULES.md
 M docs/architecture/STRUCTURE_CANONICAL.md
 D platform_os/studio/channel/browser/shell/package-lock.json
 M platform_os/studio/channel/browser/shell/package.json
 M platform_os/studio/channel/browser/shell/src/app/authentication/LoginPage.jsx
 M platform_os/studio/channel/browser/shell/src/app/onboarding/ShortRegisterView.jsx
 M platform_os/studio/channel/browser/shell/src/app/shell/StudioShell.css
 M platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
 M platform_os/studio/channel/browser/shell/src/main.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/party/form/PartyForm.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/party/form/section/PartyIdentitySection.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/party/page/PartyListPage.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/tax/form/section/TaxProfileSection.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/workforce/employee/form/EmployeeForm.jsx
 M platform_os/studio/channel/browser/shell/src/renderer/module/workforce/employee/page/EmployeeTeamPage.jsx
 M platform_os/studio/channel/browser/shell/vite.alias.js
 M platform_os/studio/channel/browser/shell/vite.config.js
 D platform_os/studio/engine/framework/theme/base/reset.css
 D platform_os/studio/engine/framework/theme/base/typography.css
 D platform_os/studio/engine/framework/theme/base/variables.css
 D platform_os/studio/engine/framework/theme/dark/dark-theme.css
 D platform_os/studio/engine/framework/theme/light/light-theme.css
 D platform_os/studio/engine/framework/theme/print/print-theme.css
 D platform_os/studio/engine/framework/theme/style/runtime-theme.css
?? CHATGPT.md
?? design_system/
?? docs/ai/handoffs/codex-to-review/SHARED_DESIGN_SYSTEM_HARDENING_03_1_CODEX_2026-07-28.md
?? docs/ai/handoffs/codex-to-review/SHARED_DESIGN_SYSTEM_RECONCILIATION_01_1_CODEX_2026-07-28.md
?? docs/ai/reviews/accepted/SHARED_DESIGN_SYSTEM_DIRECT_AUDIT_02_1_CLAUDE_2026-07-28.md
?? docs/ai/reviews/accepted/SHARED_DESIGN_SYSTEM_DIRECT_AUDIT_02_2_CLAUDE_2026-07-28.md
?? docs/ai/shared/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0(1).md
?? docs/architecture/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md
?? docs/governance/
?? package-lock.json
?? package.json
```

No se ejecutó `git add`, `git commit` ni `git push`.

## 10. Veredicto

```text
REPO_VERIFIED=PASS
F1_ONSECONDARY=PASS
DEFAULT_THEME_ONSECONDARY=#06204D
DEFAULT_THEME_CONTRAST=5.9370097511034565
CUSTOM_SECONDARY_FOREGROUND=AUTOMATIC
CSS_STATIC_RUNTIME_CONSISTENCY=PASS
CSS_VARIABLE_EXPOSURE=PASS
TAILWIND_COLOR_TOKEN=PASS
F2_TEST_TS_EXCLUDED=PASS
F2_TEST_TSX_EXCLUDED=PASS
F2_PRODUCTIVE_TSX_VALIDATED=PASS
F2_FORBIDDEN_PRODUCTIVE_IMPORT_DETECTED=PASS
DESIGN_SYSTEM_TYPECHECK=PASS
DESIGN_SYSTEM_TESTS=PASS_11_OF_11
DESIGN_SYSTEM_BUILD=PASS
STUDIO_TESTS=PASS_187_OF_187
BROWSER_SHELL_BUILD=PASS_308_MODULES
ESLINT_EXISTING=PASS
SCOPED_DIFF_CHECK=PASS
TRACKED_NODE_MODULES_OR_DIST=ZERO
PRIOR_REPORTS_UNCHANGED=PASS
STAGING_EXECUTED=FALSE
COMMIT_EXECUTED=FALSE
PUSH_EXECUTED=FALSE
VERDICT=READY_FOR_CLAUDE_VERIFICATION
```

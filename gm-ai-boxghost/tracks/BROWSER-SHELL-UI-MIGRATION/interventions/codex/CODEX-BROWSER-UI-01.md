# CODEX-BROWSER-UI-01

## GYPPORT® PLATFORM OS

**Track:** Browser Shell UI Migration  
**Step:** BROWSER-UI-01 — Auditoría y reparación mínima de imports migrados  
**Mode:** Minimal Repair  
**Agent:** Codex  
**Status:** Ready for Execution  

---

# 1. CUMPLIMIENTO ARQUITECTÓNICO

Leer primero:

```text
gypport/AGENTS.md
gypport/Reglas.md
gypport/docs/architecture/ARCHITECTURE_GOVERNANCE.md
gypport/docs/architecture/PLATFORM_FOUNDATION.md
gypport/docs/architecture/STRUCTURE_CANONICAL.md
gypport/docs/architecture/BOUNDARY_RULES.md
gypport/docs/architecture/ACTIVE_TRACKS.md
```

Declarar:

```text
Track activo: Browser Shell UI Migration
Boundary autorizado: reparación de imports de JSX ya migrados
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. OBJETIVO

Verificar y corregir únicamente los imports rotos de los archivos JSX ya movidos dentro de:

```text
gypport/platform_os/studio/channel/browser/shell/src/app/
gypport/platform_os/studio/channel/browser/shell/src/renderer/module/
```

No mover más archivos.

No reorganizar carpetas.

No crear nueva arquitectura.

No conectar todavía todas las pantallas al `App.jsx`.

---

# 3. COMANDOS INICIALES

Ejecutar:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

Proteger todos los cambios preexistentes.

No ejecutar:

```text
git add
git commit
git push
git restore
git clean
git reset
git stash
```

---

# 4. ESTRUCTURA ESPERADA

Confirmar:

```text
src/app/authentication/
src/app/dashboard/
src/app/onboarding/

src/renderer/module/party/form/
src/renderer/module/party/form/section/
src/renderer/module/party/page/

src/renderer/module/tax/form/section/

src/renderer/module/workforce/employee/form/
src/renderer/module/workforce/employee/page/
```

Confirmar específicamente:

```text
EmployeeForm.jsx
    -> renderer/module/workforce/employee/form/

EmployeeTeamPage.jsx
    -> renderer/module/workforce/employee/page/
```

No moverlos nuevamente.

---

# 5. INSPECCIÓN OBLIGATORIA

Leer completos todos los `.jsx` bajo:

```text
gypport/platform_os/studio/channel/browser/shell/src/app/
gypport/platform_os/studio/channel/browser/shell/src/renderer/module/
```

Inspeccionar también:

```text
gypport/platform_os/studio/channel/browser/shell/src/App.jsx
gypport/platform_os/studio/channel/browser/shell/src/main.jsx
gypport/platform_os/studio/channel/browser/shell/vite.alias.js
gypport/platform_os/studio/engine/framework/theme/
```

Buscar en todo `src/`:

```text
@legacy
/src/legacy
../legacy
../../legacy
theme/index.css
theme/theme
services/authService
ListaParties
FormularioPartyIdentidad
FormularioParties
FormularioPartyTributario
FormularioEmpleado
ModuloEquipo
DashboardLayout
DashboardContent
menuConfig
menuEngine
breadcrumbs
```

---

# 6. ARCHIVOS AUTORIZADOS

Modificar únicamente archivos JSX o JS dentro de:

```text
gypport/platform_os/studio/channel/browser/shell/src/app/
gypport/platform_os/studio/channel/browser/shell/src/renderer/module/
```

También se permite modificar:

```text
gypport/platform_os/studio/channel/browser/shell/src/App.jsx
```

solo si hace falta corregir imports ya existentes.

No modificar:

```text
main.jsx
vite.alias.js
engine/**
module/**
journey/**
app/business-studio/**
contracts/**
developer_platform/toolchain/**
server/**
```

---

# 7. REGLAS DE REPARACIÓN

1. Eliminar toda referencia activa a `@legacy`.
2. Corregir imports relativos según la ubicación actual.
3. Usar aliases existentes; no crear aliases nuevos.
4. No copiar archivos.
5. No duplicar componentes.
6. No crear wrappers temporales.
7. No inventar servicios inexistentes.
8. Si una dependencia real no existe, detenerse y reportarla como blocker.
9. No conectar pantallas no activas solo para hacer que compile.
10. No cambiar comportamiento funcional.

---

# 8. DASHBOARD.JSX

Para:

```text
src/app/dashboard/Dashboard.jsx
```

Verificar:

- imports de layout;
- imports de navegación;
- imports de menú;
- imports de módulos visuales;
- ausencia de rutas hacia `legacy`.

Si algún owner requerido no existe en la estructura actual, no inventarlo.

Reportar el blocker exacto.

---

# 9. VALIDACIÓN

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

Después ejecutar búsqueda final:

```text
@legacy
src/legacy
```

Resultado esperado:

```text
Contracts PASS
Build PASS
Cero referencias activas a legacy
```

Si `build` pasa porque los componentes no están importados por el grafo activo, hacer además una verificación estática de resolución de imports de todos los JSX inspeccionados.

No modificar `App.jsx` solo para forzar que todos entren al bundle.

---

# 10. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Árbol final inspeccionado.
5. Archivos JSX inspeccionados.
6. Imports rotos encontrados.
7. Archivos modificados.
8. Diff exacto por archivo.
9. Referencias `@legacy` eliminadas.
10. Dependencias faltantes no corregibles.
11. Resultado de contracts.
12. Resultado de build.
13. Resultado de búsqueda final.
14. `git --no-pager diff --stat`.
15. `git status --short` final.
16. Confirmación de que no se movieron archivos.
17. Confirmación de que no se modificó Engine, Module, Journey ni Toolchain.
18. Confirmación de que nada fue staged, committed o pushed.

---

# 11. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
se requiere crear una nueva arquitectura

se necesita mover más archivos

falta un owner real para DashboardLayout, menú o navegación

se requiere crear aliases nuevos

se necesita modificar Engine o Module
```

No improvisar.

---

# 12. DETENERSE

Detenerse después de reparar imports y validar.

No hacer commit.

Finalizar con:

```text
git status --short
```

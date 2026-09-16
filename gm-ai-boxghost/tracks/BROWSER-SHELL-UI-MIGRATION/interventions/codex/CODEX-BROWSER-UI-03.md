# CODEX-BROWSER-UI-03

## GYPPORT® PLATFORM OS

**Track:** Browser Shell UI Migration  
**Step:** BROWSER-UI-03 — Reparación mecánica de imports existentes  
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
gypport/docs/architecture/BOUNDARY_RULES.md
gypport/docs/architecture/ACTIVE_TRACKS.md
gypport/docs/ai/codex/CODEX-BROWSER-UI-02.md
```

Declarar:

```text
Track activo: Browser Shell UI Migration
Boundary autorizado: reparación mecánica de imports ya existentes
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. OBJETIVO

Corregir únicamente imports cuya correspondencia ya fue confirmada.

No crear owners nuevos.

No activar pantallas.

No modificar layout, menú, autenticación, tema ni routing.

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

# 4. ARCHIVOS AUTORIZADOS

Modificar solamente:

```text
gypport/platform_os/studio/channel/browser/shell/src/renderer/module/workforce/employee/form/EmployeeForm.jsx

gypport/platform_os/studio/channel/browser/shell/src/renderer/module/workforce/employee/page/EmployeeTeamPage.jsx

gypport/platform_os/studio/channel/browser/shell/src/renderer/module/party/page/PartyListPage.jsx

gypport/platform_os/studio/channel/browser/shell/src/app/dashboard/Dashboard.jsx
```

No modificar ningún otro archivo.

---

# 5. CAMBIOS AUTORIZADOS

## EmployeeForm.jsx

Reemplazar el import Legacy de identidad Party por:

```javascript
@renderer/module/party/form/section/PartyIdentitySection.jsx
```

No modificar lógica ni JSX.

## EmployeeTeamPage.jsx

Reemplazar el import antiguo de `ListaParties` por:

```javascript
@renderer/module/party/page/PartyListPage.jsx
```

No modificar lógica ni JSX.

## PartyListPage.jsx

Eliminar únicamente el import CSS local redundante que apunta a:

```text
theme/index.css
```

El estilo global ya se carga desde `main.jsx`.

No agregar otro import CSS.

## Dashboard.jsx

Corregir únicamente estos imports visuales ya mapeados:

```text
ModuloEquipo
→ @renderer/module/workforce/employee/page/EmployeeTeamPage.jsx

FormularioEmpleado
→ @renderer/module/workforce/employee/form/EmployeeForm.jsx
```

No tocar todavía imports de:

```text
DashboardLayout
DashboardContent
menuConfig
menuEngine
buildBreadcrumb
```

Esos siguen fuera de scope.

---

# 6. PROHIBICIONES

No modificar:

```text
App.jsx
main.jsx
vite.alias.js
package.json
DashboardLayout
DashboardContent
NavigationEngine
Framework Navigation
authService
GYPPORT_THEME
react-router-dom
```

No tocar:

```text
engine/**
module/**
journey/**
app/business-studio/**
contracts/**
developer_platform/toolchain/**
server/**
```

No mover archivos.

No crear aliases.

No crear wrappers.

No restaurar Legacy.

---

# 7. VALIDACIÓN

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

Después ejecutar búsquedas:

```text
@legacy
ListaParties
FormularioPartyIdentidad
theme/index.css
```

Resultado esperado:

```text
Contracts PASS
Build PASS
Cero referencias activas en los cuatro archivos autorizados
```

No interpretar build verde como validación de los owners aún faltantes de Dashboard.

---

# 8. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Archivos modificados.
6. Diff exacto por archivo.
7. Confirmación de eliminación de `@legacy`.
8. Confirmación de corrección Workforce.
9. Confirmación de eliminación del CSS redundante.
10. Confirmación de que Dashboard solo corrigió imports visuales.
11. Resultado de contracts.
12. Resultado de build.
13. Resultado de búsquedas finales.
14. Blockers restantes de Dashboard.
15. `git --no-pager diff --stat`.
16. `git status --short` final.
17. Confirmación de que no se movieron archivos.
18. Confirmación de que Engine, Module, Journey y Toolchain no fueron modificados.
19. Confirmación de que nada fue staged, committed o pushed.

---

# 9. DETENERSE

Detenerse después de reparar y validar.

No continuar con layout, menú, autenticación, tema ni routing.

Finalizar con:

```text
git status --short
```

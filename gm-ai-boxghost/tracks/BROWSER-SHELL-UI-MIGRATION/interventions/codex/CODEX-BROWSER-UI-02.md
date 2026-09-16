# CODEX-BROWSER-UI-02

## GYPPORT® PLATFORM OS

**Track:** Browser Shell UI Migration  
**Step:** BROWSER-UI-02 — Reconnaissance de owners faltantes para UI migrada  
**Mode:** Solo lectura  
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
gypport/docs/architecture/ROOT_DIRECTORY_RESPONSIBILITIES.md
gypport/docs/architecture/STRUCTURE_CANONICAL.md
gypport/docs/architecture/BOUNDARY_RULES.md
gypport/docs/architecture/ACTIVE_TRACKS.md
gypport/docs/ai/codex/CODEX-BROWSER-UI-01.md
```

Declarar:

```text
Track activo: Browser Shell UI Migration
Boundary autorizado: owners faltantes de layout, menú, autenticación y tema
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. CONTEXTO CERRADO

La equivalencia Legacy → UI renombrada ya fue confirmada.

Mapa aceptado:

```text
FormularioParties.jsx
→ src/renderer/module/party/form/PartyForm.jsx

FormularioPartyIdentidad.jsx
→ src/renderer/module/party/form/section/PartyIdentitySection.jsx

FormularioPartyTributario.jsx
→ src/renderer/module/tax/form/section/TaxProfileSection.jsx

ListaParties.jsx
→ src/renderer/module/party/page/PartyListPage.jsx

FormularioEmpleado.jsx
→ src/renderer/module/workforce/employee/form/EmployeeForm.jsx

ModuloEquipo.jsx
→ src/renderer/module/workforce/employee/page/EmployeeTeamPage.jsx

Dashboard.jsx
→ src/app/dashboard/Dashboard.jsx

LoginPage.jsx
→ src/app/authentication/LoginPage.jsx

ShortRegisterView.jsx
→ src/app/onboarding/ShortRegisterView.jsx
```

No volver a discutir ni invertir estas correspondencias.

No mover nuevamente esos archivos.

---

# 3. OBJETIVO

Determinar, con evidencia del repositorio, el owner real o la ausencia real de owner para:

```text
DashboardLayout
DashboardContent
menuConfig
menuEngine
buildBreadcrumb
authService
GYPPORT_THEME
theme/index.css
```

Este STEP es solo lectura.

No modificar archivos.

No crear aliases.

No crear implementaciones temporales.

No restaurar Legacy.

---

# 4. COMANDOS INICIALES

Ejecutar:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

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

# 5. INSPECCIÓN OBLIGATORIA

Leer completos:

```text
gypport/platform_os/studio/channel/browser/shell/src/app/dashboard/Dashboard.jsx
gypport/platform_os/studio/channel/browser/shell/src/app/authentication/LoginPage.jsx
gypport/platform_os/studio/channel/browser/shell/src/app/onboarding/ShortRegisterView.jsx
gypport/platform_os/studio/channel/browser/shell/src/renderer/module/party/page/PartyListPage.jsx
gypport/platform_os/studio/channel/browser/shell/src/renderer/module/workforce/employee/form/EmployeeForm.jsx
gypport/platform_os/studio/channel/browser/shell/src/renderer/module/workforce/employee/page/EmployeeTeamPage.jsx
```

Inspeccionar además:

```text
gypport/platform_os/studio/channel/browser/shell/src/
gypport/platform_os/studio/engine/core/
gypport/platform_os/studio/engine/framework/theme/
gypport/platform_os/studio/engine/framework/navigation/
gypport/platform_os/studio/engine/core/platform/
gypport/platform_os/studio/module/
gypport/platform_os/studio/app/
```

Buscar en todo el repositorio, excluyendo `node_modules`, por:

```text
DashboardLayout
DashboardContent
DEFAULT_ACTIVE_MODULES
buildMenu
menuConfig
menuEngine
buildBreadcrumb
authService
GYPPORT_THEME
runtime-theme.css
input-gypport-form
fa-spin
```

---

# 6. PREGUNTAS OBLIGATORIAS

Responder con evidencia:

1. ¿Existe actualmente `DashboardLayout` bajo otro nombre?
2. ¿Existe actualmente `DashboardContent` bajo otro nombre?
3. ¿Existe un owner real de configuración de menú?
4. ¿Existe un motor de menú actual reutilizable?
5. ¿`buildBreadcrumb` debe consumirse desde `NavigationEngine.js`?
6. ¿Existe un servicio de autenticación actual bajo otra ubicación?
7. ¿Existe un sistema de tema vigente que reemplace `GYPPORT_THEME`?
8. ¿`runtime-theme.css` es el owner activo de estilos?
9. ¿`PartyListPage.jsx` debe importar CSS directamente o depender del import global de `main.jsx`?
10. ¿Qué imports pueden corregirse de forma mecánica?
11. ¿Qué dependencias requieren una nueva decisión arquitectónica?
12. ¿Qué archivos pueden quedar funcionales sin crear owners nuevos?
13. ¿Qué archivo debe repararse primero?
14. ¿Puede `Dashboard.jsx` funcionar hoy con owners existentes o necesita un STEP de diseño previo?

---

# 7. CLASIFICACIÓN OBLIGATORIA

Clasificar cada dependencia faltante como:

```text
EXISTE — RUTA INCORRECTA
EXISTE — NOMBRE DIFERENTE
NO EXISTE — REQUIERE DECISIÓN
LEGACY — NO DEBE RESTAURARSE
REDUNDANTE — DEBE ELIMINARSE
```

Tabla mínima:

```text
Dependencia
Archivo consumidor
Clasificación
Owner actual o ausencia
Ruta correcta propuesta
Riesgo
```

---

# 8. OPCIONES A EVALUAR

Para layout y menú evaluar:

```text
OPCIÓN A
Reutilizar owners existentes en Engine/Framework.

OPCIÓN B
Crear implementación Browser Shell específica.

OPCIÓN C
Eliminar dependencia porque el nuevo Runtime ya la reemplaza.

OPCIÓN D
Restaurar Legacy.
```

La opción D debe rechazarse salvo evidencia excepcional.

Para autenticación y tema evaluar:

```text
OPCIÓN A
Reutilizar owner existente.

OPCIÓN B
Crear owner mínimo en app/authentication o framework/theme.

OPCIÓN C
Eliminar dependencia antigua.
```

No implementar ninguna opción.

---

# 9. VALIDACIÓN PASIVA

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

Reportar conteos reales.

No asumir que build verde significa que JSX no enlazado está sano.

Hacer además verificación estática de resolución de imports para todos los JSX migrados.

---

# 10. PROHIBICIONES

No modificar ni crear archivos.

No:

```text
restaurar src/legacy
crear aliases
crear wrappers
crear owners ficticios
mover archivos
conectar App.jsx
cambiar Runtime
cambiar Engine
cambiar Module
cambiar Toolchain
```

---

# 11. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Resultados completos de búsqueda.
6. Tabla de clasificación de dependencias.
7. Owners existentes confirmados.
8. Owners inexistentes confirmados.
9. Imports corregibles mecánicamente.
10. Imports que requieren decisión arquitectónica.
11. Recomendación por cada blocker.
12. Orden exacto de reparación.
13. Superficie propuesta para `BROWSER-UI-03`.
14. Resultado de contracts.
15. Resultado de build.
16. Resultado de verificación estática.
17. `git status --short` final.
18. Confirmación de que no se modificó nada.

---

# 12. DETENERSE

Detenerse después del reporte.

No implementar reparaciones.

Finalizar con:

```text
git status --short
```

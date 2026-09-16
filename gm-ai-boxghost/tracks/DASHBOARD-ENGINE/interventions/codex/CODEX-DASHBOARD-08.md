# CODEX-DASHBOARD-08

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-08 — Contrato de API pública declarativa  
**Mode:** Contract First  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-07.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: contrato de API pública de Dashboard
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. OBJETIVO

Crear un contrato ejecutable que defina la API declarativa pública del Dashboard Engine disponible mediante:

```javascript
import * as DashboardPublicApi from "@core/ui";
```

No modificar barrels ni producción en este STEP.

---

# 3. DECISIÓN CERRADA

La API pública para módulos de negocio debe exponer:

```text
DashboardBuilder
createDashboardBuilder
createDashboardSchema
createDashboardWidget
createDashboardAction
DASHBOARD_TYPES
DASHBOARD_LAYOUTS
DASHBOARD_VISIBILITY
validateDashboardSchema
assertValidDashboardSchema
```

No debe exponer mediante `@core/ui`:

```text
resolveDashboardComposition
resolveDashboardForRender
resolveDashboardInstanceForRender
loadDashboard
createDashboardInstance
setDashboardLoading
setDashboardError
setDashboardEditable
setWidgetState
getWidgetState
refreshDashboard
getDashboardState
```

Estos símbolos pertenecen a implementación interna de Engine/Runtime.

---

# 4. COMANDOS INICIALES

Ejecutar:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

Proteger todos los cambios preexistentes.

No hacer stage, commit ni push.

---

# 5. INSPECCIÓN OBLIGATORIA

Leer completos:

```text
gypport/platform_os/studio/engine/core/ui/index.js
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardBuilder.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardSchema.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardTypes.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardValidator.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRuntime.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRenderer.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
```

No modificar archivos inspeccionados.

---

# 6. ÚNICO ARCHIVO AUTORIZADO

Crear solamente:

```text
gypport/platform_os/studio/contracts/dashboard/DashboardPublicApi.contract.mjs
```

---

# 7. CASOS OBLIGATORIOS

El contrato debe comprobar que `@core/ui` expone:

```text
DashboardBuilder
createDashboardBuilder
createDashboardSchema
createDashboardWidget
createDashboardAction
DASHBOARD_TYPES
DASHBOARD_LAYOUTS
DASHBOARD_VISIBILITY
validateDashboardSchema
assertValidDashboardSchema
```

También debe comprobar que `@core/ui` no expone:

```text
resolveDashboardComposition
resolveDashboardForRender
resolveDashboardInstanceForRender
loadDashboard
createDashboardInstance
setDashboardLoading
setDashboardError
setDashboardEditable
setWidgetState
getWidgetState
refreshDashboard
getDashboardState
```

No afirmar nada sobre exports de otros dominios de `@core/ui`.

---

# 8. ESTADO ROJO CONTROLADO

La API actual todavía expone Runtime, Renderer y CompositionResolver mediante `export *`.

Por tanto, el nuevo contrato debe quedar rojo únicamente porque esos símbolos internos siguen siendo públicos.

La línea base anterior debe permanecer verde:

```text
9 archivos
70 pruebas
PASS
```

No modificar producción para lograr PASS.

No usar `skip` ni `todo`.

---

# 9. VALIDACIÓN

Antes de crear el contrato:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Esperado:

```text
9 archivos
70 pruebas
PASS
```

Después de crear el contrato, ejecutar nuevamente.

Esperado:

```text
10 archivos descubiertos
contrato DashboardPublicApi falla únicamente por exports internos presentes
los 9 archivos anteriores permanecen verdes
```

---

# 10. PROHIBICIONES

No modificar:

```text
engine/core/ui/index.js
engine/core/ui/dashboard/index.js
DashboardRuntime.js
DashboardRenderer.js
DashboardCompositionResolver.js
```

No tocar Module, Journey, Channel, App, Toolchain ni Server.

No reorganizar barrels.

No integrar Runtime.

No resolver `installedPlugins`.

---

# 11. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Resultado de cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Ruta del contrato creado.
6. Símbolos públicos exigidos.
7. Símbolos internos prohibidos.
8. Contenido completo del contrato.
9. Resultado de línea base.
10. Resultado rojo controlado.
11. Causa exacta del fallo.
12. Confirmación de que los 9 contratos anteriores siguen verdes.
13. `git --no-pager diff --stat`.
14. `git status --short` final.
15. Confirmación de que no se modificó producción.
16. Confirmación de que nada fue staged, committed o pushed.

---

# 12. DETENERSE

No modificar barrels.

No ejecutar DASHBOARD-09.

Finalizar con:

```text
git status --short
```
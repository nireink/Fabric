# CODEX-DASHBOARD-09

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-09 — Implementación mínima de API pública declarativa  
**Mode:** Implementación mínima guiada por contrato  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-08.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: API pública declarativa del Dashboard Engine
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Hacer que:

```javascript
import * as DashboardPublicApi from "@core/ui";
```

exponga únicamente la API declarativa aprobada del Dashboard Engine y deje fuera los símbolos internos de Runtime, Renderer y CompositionResolver.

El contrato obligatorio es:

```text
gypport/platform_os/studio/contracts/dashboard/DashboardPublicApi.contract.mjs
```

No modificar dicho contrato.

---

# 3. API PÚBLICA APROBADA

`@core/ui` debe seguir exponiendo:

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

Los archivos internos siguen existiendo y pueden continuar siendo importados mediante rutas internas explícitas por componentes autorizados del Engine.

---

# 4. COMANDOS INICIALES

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

# 5. INSPECCIÓN Y BÚSQUEDA OBLIGATORIA

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
gypport/platform_os/studio/contracts/dashboard/DashboardPublicApi.contract.mjs
```

Buscar en `gypport/platform_os/studio/`, excluyendo `node_modules`, todos los consumidores de:

```text
@core/ui
@core/ui/dashboard
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

Clasificar cada consumidor como:

```text
DECLARATIVE CONSUMER
ENGINE INTERNAL CONSUMER
CHANNEL CONSUMER
CONTRACT
```

Si un consumidor activo depende de que los símbolos internos salgan por `@core/ui`, detenerse y reportar antes de modificar.

No corregir consumidores en este STEP.

---

# 6. ÚNICO ARCHIVO AUTORIZADO

Modificar solamente:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
```

No modificar:

```text
gypport/platform_os/studio/engine/core/ui/index.js
```

---

# 7. CAMBIO AUTORIZADO

Reemplazar los `export *` del barrel Dashboard por exportaciones explícitas que mantengan únicamente la API declarativa aprobada.

La forma exacta debe derivarse de los exports reales de cada archivo inspeccionado.

El resultado debe excluir del barrel público:

```text
DashboardCompositionResolver
DashboardRenderer
DashboardRuntime
```

No eliminar ni renombrar esos archivos.

No modificar su contenido.

No crear un nuevo barrel interno en este STEP.

---

# 8. REGLAS

La implementación debe:

1. Mantener todos los símbolos declarativos aprobados.
2. Ocultar los símbolos internos únicamente del barrel público.
3. No alterar comportamiento de Runtime, Renderer o Resolver.
4. No cambiar imports internos existentes.
5. No agregar nuevas dependencias.
6. No modificar otros dominios exportados por `@core/ui`.
7. No introducir aliases nuevos.

---

# 9. VALIDACIÓN DE CONTRATOS

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Resultado esperado:

```text
10 archivos de prueba
72 pruebas
PASS
exit code 0
```

Reportar el conteo real si difiere.

El contrato:

```text
DashboardPublicApi.contract.mjs
```

debe pasar sin modificaciones.

---

# 10. VALIDACIÓN DE BUILD

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

El build puede seguir fallando únicamente por:

```text
installedPlugins is not exported by module/index.js
```

No corregir ese blocker.

Confirmar que no aparezcan errores nuevos por exports faltantes del Dashboard Engine.

---

# 11. PROHIBICIONES

No modificar:

```text
gypport/platform_os/studio/engine/core/ui/index.js
DashboardBuilder.js
DashboardSchema.js
DashboardTypes.js
DashboardValidator.js
DashboardRuntime.js
DashboardRenderer.js
DashboardCompositionResolver.js
DashboardPublicApi.contract.mjs
```

No tocar:

```text
module/
journey/
app/
channel/browser/shell/src/
developer_platform/toolchain/
server/
```

No:

```text
integrar Runtime con CompositionResolver
integrar Renderer
resolver installedPlugins
crear nuevos barrels
cambiar aliases
crear UI
```

---

# 12. REPORTE FINAL

Entregar:

1. Root.
2. Branch.
3. `git status --short` inicial.
4. Cumplimiento arquitectónico.
5. Archivos inspeccionados.
6. Resultado de búsqueda de consumidores.
7. Clasificación de consumidores.
8. Archivo modificado.
9. Diff exacto de `dashboard/index.js`.
10. Símbolos públicos finales.
11. Símbolos internos eliminados del barrel público.
12. Salida completa de contracts.
13. Exit code y conteos.
14. Salida completa de build.
15. Exit code del build.
16. Próximo blocker exacto.
17. Confirmación de que no apareció error nuevo de Dashboard.
18. `git --no-pager diff --stat`.
19. `git status --short` final.
20. Confirmación de que Runtime, Renderer y Resolver no fueron modificados.
21. Confirmación de que Toolchain no fue tocado.
22. Confirmación de que nada fue staged, committed o pushed.

---

# 13. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
existe un consumidor activo que depende de símbolos internos desde @core/ui

se requiere modificar más de un archivo

algún símbolo declarativo aprobado no existe realmente

algún contrato anterior deja de pasar

aparece un nuevo error de build relacionado con Dashboard
```

No improvisar.

---

# 14. DETENERSE

Detenerse después de implementar y validar.

No ejecutar el siguiente STEP.

Finalizar con:

```text
git status --short
```

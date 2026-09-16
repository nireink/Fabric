# CODEX-DASHBOARD-13

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-13 — Implementación de resolveDashboardCompositionForRender  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-12.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: DashboardRenderer consumiendo composición resuelta
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Implementar únicamente:

```javascript
resolveDashboardCompositionForRender(code, options)
```

en:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRenderer.js
```

Debe satisfacer:

```text
gypport/platform_os/studio/contracts/dashboard/DashboardRendererComposition.contract.mjs
```

No modificar Runtime, Resolver, Registry ni contratos.

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

# 4. INSPECCIÓN OBLIGATORIA

Leer completos:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRenderer.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRuntime.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
gypport/platform_os/studio/contracts/dashboard/DashboardRendererComposition.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardRenderer.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardRuntimeComposition.contract.mjs
```

Verificar:

```text
loadDashboardComposition(code)
defaults actuales del Renderer
overrides actuales del Renderer
```

No modificar contratos.

---

# 5. ÚNICO ARCHIVO AUTORIZADO

Modificar solamente:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRenderer.js
```

No modificar ningún otro archivo.

---

# 6. API A IMPLEMENTAR

Agregar:

```javascript
export function resolveDashboardCompositionForRender(
  dashboardCode,
  options = {}
)
```

Responsabilidad:

1. Obtener composición mediante:

```javascript
loadDashboardComposition(dashboardCode)
```

2. Retornar:

```javascript
{
  schema,
  widgets,
  renderer,
  device,
  layout,
  readonly
}
```

3. Conservar referencias originales de:

```text
schema
widgets
binding
definition
```

4. Conservar el orden recibido.

5. Aplicar los defaults y overrides actuales del Renderer.

6. Propagar errores de Dashboard faltante y Widget faltante sin alterarlos.

---

# 7. REGLAS DE PAYLOAD

El resultado no debe incluir:

```text
runtime
instance
widgetsState
loading
error
editable
registry
dashboardRegistry
widgetRegistry
```

No resolver widgets nuevamente.

No consultar directamente:

```text
DashboardRegistry
WidgetRegistry
```

No crear instancia.

No mutar composición.

---

# 8. IMPLEMENTACIÓN MÍNIMA

La implementación debe delegar en:

```javascript
loadDashboardComposition(dashboardCode)
```

y limitarse a preparar metadata renderer-neutral.

No crear:

```text
clases
caché
estado global
adaptadores nuevos
factories nuevas
mocks
errores personalizados
```

---

# 9. PROHIBICIONES

No modificar:

```text
DashboardRuntime.js
DashboardCompositionResolver.js
DashboardRegistry.js
WidgetRegistry.js
dashboard/index.js
core/ui/index.js
contracts/**
StudioBootstrap.js
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

No resolver:

```text
installedPlugins
Commercial Dashboard
UI
React renderer
```

---

# 10. VALIDACIÓN DE CONTRATOS

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Resultado esperado:

```text
12 archivos de prueba
98 pruebas
PASS
exit code 0
```

Si el conteo real difiere, reportarlo.

No modificar contratos para obtener PASS.

---

# 11. VALIDACIÓN DE BUILD

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

El build puede seguir fallando únicamente por:

```text
installedPlugins is not exported by module/index.js
```

No corregir ese blocker.

Confirmar que no aparezca error nuevo relacionado con:

```text
resolveDashboardCompositionForRender
DashboardRenderer
DashboardRuntime
DashboardCompositionResolver
```

---

# 12. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Archivo modificado.
6. Diff exacto de `DashboardRenderer.js`.
7. Contenido de `resolveDashboardCompositionForRender`.
8. Confirmación de referencias preservadas.
9. Confirmación de metadata por default y override.
10. Confirmación de no consulta directa a registries.
11. Confirmación de no creación de instancia.
12. Salida completa de contracts.
13. Exit code y conteos.
14. Salida completa de build.
15. Exit code del build.
16. Próximo blocker exacto.
17. Confirmación de que no apareció error nuevo de Dashboard.
18. `git --no-pager diff --stat`.
19. `git status --short` final.
20. Confirmación de que Runtime, Resolver, Registry y contratos no fueron modificados.
21. Confirmación de que Toolchain no fue tocado.
22. Confirmación de que nada fue staged, committed o pushed.

---

# 13. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
se requiere modificar más de un archivo

algún contrato anterior deja de pasar

es necesario consultar Registry directamente

aparece un error nuevo de arquitectura
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

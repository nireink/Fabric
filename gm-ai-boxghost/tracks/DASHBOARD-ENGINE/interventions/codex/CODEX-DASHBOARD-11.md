# CODEX-DASHBOARD-11

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-11 — Implementación de loadDashboardComposition  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-10.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: DashboardRuntime → DashboardCompositionResolver
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Implementar únicamente la función interna:

```javascript
loadDashboardComposition(code)
```

en:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRuntime.js
```

Debe satisfacer:

```text
gypport/platform_os/studio/contracts/dashboard/DashboardRuntimeComposition.contract.mjs
```

No modificar Renderer, Registry ni API pública declarativa.

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
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRuntime.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
gypport/platform_os/studio/contracts/dashboard/DashboardRuntimeComposition.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardRuntime.contract.mjs
gypport/platform_os/studio/engine/core/registry/ui/DashboardRegistry.js
```

Verificar el comportamiento actual de:

```text
loadDashboard(code)
resolveDashboardComposition(dashboardSchema)
```

No modificar contratos.

---

# 5. ÚNICO ARCHIVO AUTORIZADO

Modificar solamente:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRuntime.js
```

No modificar ningún otro archivo.

---

# 6. API A IMPLEMENTAR

Agregar:

```javascript
export function loadDashboardComposition(code)
```

Comportamiento obligatorio:

1. Cargar el Dashboard mediante `loadDashboard(code)`.
2. Pasar el schema cargado a `resolveDashboardComposition(schema)`.
3. Retornar la composición resuelta.
4. Propagar sin alterar:
   - error de Dashboard inexistente;
   - error de Widget inexistente.
5. No crear instancia.
6. No modificar `widgetsState`.
7. No invocar Renderer.
8. No depender de React, DOM, Channel, Module ni Journey.

---

# 7. IMPLEMENTACIÓN MÍNIMA

La implementación esperada debe ser equivalente conceptualmente a:

```javascript
export function loadDashboardComposition(code) {
  const dashboardSchema = loadDashboard(code);
  return resolveDashboardComposition(dashboardSchema);
}
```

La forma exacta debe respetar imports y estilo actuales del archivo.

No duplicar lógica de Registry.

No resolver widgets directamente dentro de Runtime.

---

# 8. PROHIBICIONES

No modificar:

```text
DashboardCompositionResolver.js
DashboardRenderer.js
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
Renderer integration
Commercial Dashboard
UI
```

---

# 9. VALIDACIÓN DE CONTRATOS

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Resultado esperado:

```text
11 archivos de prueba
84 pruebas
PASS
exit code 0
```

Si el conteo real difiere, reportarlo.

No modificar contratos para obtener PASS.

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

Confirmar que no aparezca error nuevo relacionado con:

```text
loadDashboardComposition
DashboardRuntime
DashboardCompositionResolver
```

---

# 11. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Archivo modificado.
6. Diff exacto de `DashboardRuntime.js`.
7. Contenido de `loadDashboardComposition`.
8. Confirmación de propagación de errores.
9. Confirmación de no creación de instancia.
10. Confirmación de no mutación de estado.
11. Salida completa de contracts.
12. Exit code y conteos.
13. Salida completa de build.
14. Exit code del build.
15. Próximo blocker exacto.
16. Confirmación de que no apareció error nuevo de Dashboard.
17. `git --no-pager diff --stat`.
18. `git status --short` final.
19. Confirmación de que Resolver, Renderer, Registry y contratos no fueron modificados.
20. Confirmación de que Toolchain no fue tocado.
21. Confirmación de que nada fue staged, committed o pushed.

---

# 12. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
se requiere modificar más de un archivo

algún contrato anterior deja de pasar

la función requiere cambiar la API pública

aparece un error nuevo de arquitectura
```

No improvisar.

---

# 13. DETENERSE

Detenerse después de implementar y validar.

No ejecutar el siguiente STEP.

Finalizar con:

```text
git status --short
```

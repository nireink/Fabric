# CODEX-DASHBOARD-09B

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-09B — Cierre del barrel público declarativo  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-09.md
gypport/docs/ai/codex/CODEX-DASHBOARD-09A.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: barrel público declarativo del Dashboard Engine
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Modificar únicamente:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
```

para que `@core/ui` exponga solo la API declarativa aprobada del Dashboard Engine.

No modificar contratos ni otros archivos de producción.

---

# 3. API PÚBLICA QUE DEBE PERMANECER

Conservar públicamente:

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

---

# 4. API INTERNA QUE DEBE DEJAR DE SALIR POR EL BARREL

Excluir de `@core/ui`:

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

Los archivos internos deben seguir existiendo y continuar accesibles mediante rutas explícitas:

```text
@core/ui/dashboard/DashboardCompositionResolver
@core/ui/dashboard/DashboardRenderer
@core/ui/dashboard/DashboardRuntime
```

---

# 5. COMANDOS INICIALES

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

# 6. INSPECCIÓN OBLIGATORIA

Leer completos:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardBuilder.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardSchema.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardTypes.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardValidator.js
gypport/platform_os/studio/contracts/dashboard/DashboardPublicApi.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardRuntime.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardRenderer.contract.mjs
```

Confirmar que `DashboardRuntime.contract.mjs` y `DashboardRenderer.contract.mjs` ya usan rutas internas explícitas.

---

# 7. CAMBIO EXACTO

Reemplazar en:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
```

los `export *` actuales por exportaciones explícitas de la API declarativa aprobada.

No exportar desde este barrel:

```text
DashboardCompositionResolver
DashboardRenderer
DashboardRuntime
```

No modificar:

```text
gypport/platform_os/studio/engine/core/ui/index.js
```

No crear barrels nuevos.

---

# 8. VALIDACIÓN DE CONTRATOS

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

El contrato:

```text
DashboardPublicApi.contract.mjs
```

debe pasar sin modificaciones.

---

# 9. VALIDACIÓN DE BUILD

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

El build puede seguir fallando únicamente por:

```text
installedPlugins is not exported by module/index.js
```

No corregir ese blocker.

No debe aparecer error nuevo por exports faltantes del Dashboard Engine.

---

# 10. ARCHIVO AUTORIZADO

Modificar solamente:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
```

No modificar ningún otro archivo.

---

# 11. PROHIBICIONES

No modificar:

```text
DashboardRuntime.js
DashboardRenderer.js
DashboardCompositionResolver.js
DashboardBuilder.js
DashboardSchema.js
DashboardTypes.js
DashboardValidator.js
core/ui/index.js
contracts/**
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

No integrar todavía Runtime con CompositionResolver.

No resolver `installedPlugins`.

---

# 12. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Archivo modificado.
6. Diff exacto de `dashboard/index.js`.
7. Símbolos públicos finales.
8. Símbolos internos excluidos.
9. Salida completa de contracts.
10. Exit code y conteos.
11. Salida completa de build.
12. Exit code del build.
13. Próximo blocker exacto.
14. Confirmación de que no apareció error nuevo de Dashboard.
15. `git --no-pager diff --stat`.
16. `git status --short` final.
17. Confirmación de que Runtime, Renderer, Resolver y contratos no fueron modificados.
18. Confirmación de que Toolchain no fue tocado.
19. Confirmación de que nada fue staged, committed o pushed.

---

# 13. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
se requiere modificar más de un archivo

algún contrato anterior deja de pasar

algún símbolo declarativo aprobado deja de exportarse

aparece un error nuevo de build relacionado con Dashboard
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

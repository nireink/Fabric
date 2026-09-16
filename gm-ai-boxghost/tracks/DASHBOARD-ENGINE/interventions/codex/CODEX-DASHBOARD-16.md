# CODEX-DASHBOARD-16

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-16 — Contrato de instalación Plugin → Domain → Feature → Dashboard/Widget  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-15.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: PluginInstaller → Domain → FeatureManager → DashboardRegistry / WidgetRegistry
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Crear un contrato ejecutable que pruebe el flujo completo:

```text
CommercialPlugin
    ↓
PluginInstaller
    ↓
Domain
    ↓
Feature
    ↓
FeatureManager
    ↓
DashboardRegistry / WidgetRegistry
    ↓
resolveDashboardCompositionForRender
```

No modificar producción.

No tocar `StudioBootstrap` ni `installedPlugins`.

---

# 3. COMANDOS INICIALES

Ejecutar:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

Proteger todos los cambios preexistentes.

No ejecutar `git add`, `git commit`, `git push`, `git restore`, `git clean`, `git reset` ni `git stash`.

---

# 4. INSPECCIÓN OBLIGATORIA

Leer completos:

```text
gypport/platform_os/studio/engine/framework/plugin/runtime/PluginInstaller.js
gypport/platform_os/studio/engine/framework/feature/runtime/FeatureManager.js
gypport/platform_os/studio/module/commercial/CommercialPlugin.js
gypport/platform_os/studio/module/commercial/domain/
gypport/platform_os/studio/module/commercial/domain/business-partner/feature/BusinessPartnerProfileFeature.js
gypport/platform_os/studio/engine/core/registry/ui/DashboardRegistry.js
gypport/platform_os/studio/engine/core/registry/ui/WidgetRegistry.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRenderer.js
gypport/platform_os/studio/contracts/feature/FeatureManagerDashboardWidgetRouting.contract.mjs
```

Verificar la API pública real del instalador.

No inventar nombres de funciones.

---

# 5. ÚNICO ARCHIVO AUTORIZADO

Crear solamente:

```text
gypport/platform_os/studio/contracts/plugin/PluginDashboardWidgetInstallation.contract.mjs
```

Crear `contracts/plugin/` solo si no existe.

No modificar ningún otro archivo.

---

# 6. CASOS OBLIGATORIOS

El contrato debe probar, como mínimo:

1. El `CommercialPlugin` puede instalarse mediante la API real de `PluginInstaller`.
2. La instalación recorre sus Domains.
3. Los Domains instalan sus Features.
4. Las Features enrutan dashboards hacia `DashboardRegistry`.
5. Las Features enrutan widgets hacia `WidgetRegistry`.
6. `CommercialDashboard` queda registrado.
7. `CommercialTotalKpiWidget` queda registrado.
8. `CommercialMonthlyChartWidget` queda registrado.
9. No existe cruce de ownership entre registries.
10. Se preservan las referencias originales registradas.
11. Después de instalar el plugin, `resolveDashboardCompositionForRender("commercial-dashboard")` devuelve los dos widgets resueltos.
12. Se conserva el orden declarado.
13. Reinstalar según el comportamiento actual no debe inventar una política nueva.
14. El flujo no depende de `StudioBootstrap`.
15. El flujo no depende de `installedPlugins`.
16. El flujo permanece neutral respecto de React, DOM y Browser Shell.

---

# 7. POLÍTICA DE REINSTALACIÓN

Inspeccionar el comportamiento actual real.

El contrato debe fijar lo que ya ocurre hoy:

```text
retorno existente
no-op
duplicado silencioso
error
```

No cambiar ni reinterpretar esa política.

---

# 8. AISLAMIENTO

Usar `beforeEach/afterEach` para limpiar, mediante API pública:

```text
DashboardRegistry
WidgetRegistry
Plugin Registry, si el instalador lo utiliza y existe reset público
Feature Registry o Domain Registry, si corresponde
```

No acceder a Maps internos.

No depender del orden de ejecución.

No usar mocks si el flujo real puede ejecutarse.

---

# 9. VALIDACIÓN

Antes de crear el contrato:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Línea base esperada:

```text
14 archivos
121 pruebas
PASS
```

Después de crear el contrato, ejecutar nuevamente.

Resultado esperado:

```text
15 archivos
nuevos casos de instalación pasando
exit code 0
```

Reportar conteos reales.

---

# 10. PROHIBICIONES

No modificar:

```text
PluginInstaller.js
FeatureManager.js
module/commercial/**
DashboardRegistry.js
WidgetRegistry.js
DashboardRuntime.js
DashboardRenderer.js
DashboardCompositionResolver.js
StudioBootstrap.js
module/index.js
```

No resolver:

```text
installedPlugins
App composition
Browser Shell
React rendering
```

No tocar Toolchain ni Server.

---

# 11. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. API real de `PluginInstaller` utilizada.
6. Ruta exacta del contrato creado.
7. Casos definidos.
8. Política actual de reinstalación detectada.
9. Estrategia de aislamiento.
10. Contenido completo del contrato.
11. Resultado de línea base.
12. Resultado final.
13. Exit code y conteos.
14. Confirmación de instalación completa del Commercial Plugin.
15. Confirmación de registro de Dashboard y Widgets.
16. Confirmación de resolución end-to-end.
17. Confirmación de independencia de `StudioBootstrap` e `installedPlugins`.
18. `git --no-pager diff --stat`.
19. `git status --short` final.
20. Confirmación de que no se modificó producción.
21. Confirmación de que Toolchain no fue tocado.
22. Confirmación de que nada fue staged, committed o pushed.

---

# 12. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
la API real del instalador no permite ejecutar el flujo sin StudioBootstrap

se requiere modificar producción

algún contrato anterior deja de pasar

aparece dependencia obligatoria de installedPlugins
```

No improvisar.

---

# 13. DETENERSE

Detenerse después del contrato.

No corregir `installedPlugins`.

No ejecutar el siguiente STEP.

Finalizar con:

```text
git status --short
```

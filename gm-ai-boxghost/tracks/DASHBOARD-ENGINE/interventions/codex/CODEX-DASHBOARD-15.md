# CODEX-DASHBOARD-15

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-15 — Contrato de enrutamiento FeatureManager para Dashboards y Widgets  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-14.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: FeatureManager → DashboardRegistry / WidgetRegistry
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Crear un contrato ejecutable que pruebe que `FeatureManager` enruta correctamente capacidades declarativas de:

```text
dashboards
widgets
```

hacia:

```text
DashboardRegistry
WidgetRegistry
```

No modificar producción.

No tocar PluginInstaller, StudioBootstrap ni `installedPlugins`.

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
gypport/platform_os/studio/engine/framework/feature/runtime/FeatureManager.js
gypport/platform_os/studio/engine/core/registry/ui/DashboardRegistry.js
gypport/platform_os/studio/engine/core/registry/ui/WidgetRegistry.js
gypport/platform_os/studio/module/commercial/domain/business-partner/feature/BusinessPartnerProfileFeature.js
gypport/platform_os/studio/module/commercial/dashboard/CommercialDashboard.js
gypport/platform_os/studio/module/commercial/widget/CommercialTotalKpiWidget.js
gypport/platform_os/studio/module/commercial/widget/CommercialMonthlyChartWidget.js
gypport/platform_os/studio/contracts/dashboard/CommercialDashboardIntegration.contract.mjs
```

Verificar los nombres públicos reales de las funciones de instalación y registro.

No inventar APIs.

---

# 5. ÚNICO ARCHIVO AUTORIZADO

Crear solamente:

```text
gypport/platform_os/studio/contracts/feature/FeatureManagerDashboardWidgetRouting.contract.mjs
```

Crear el directorio `contracts/feature/` solo si no existe.

No modificar ningún otro archivo.

---

# 6. CASOS OBLIGATORIOS

El contrato debe probar como mínimo:

1. Una feature con `capabilities.dashboards` registra sus dashboards.
2. Una feature con `capabilities.widgets` registra sus widgets.
3. Dashboard y widgets quedan disponibles en sus registries correctos.
4. No existe cruce de ownership:
   - dashboard no termina en WidgetRegistry;
   - widget no termina en DashboardRegistry.
5. Se preservan las referencias registradas.
6. Se preserva el orden de capacidades declaradas.
7. Una feature con arrays vacíos no altera registries.
8. Una feature sin `capabilities.dashboards` no falla.
9. Una feature sin `capabilities.widgets` no falla.
10. El caso Commercial real registra:
    - `CommercialDashboard`;
    - `CommercialTotalKpiWidget`;
    - `CommercialMonthlyChartWidget`.
11. Después del routing, `resolveDashboardCompositionForRender("commercial-dashboard")` resuelve los dos widgets.
12. El flujo permanece neutral respecto de React, DOM y Browser Shell.

---

# 7. AISLAMIENTO

Usar:

```text
beforeEach
afterEach
```

para limpiar:

```text
DashboardRegistry
WidgetRegistry
```

No depender del orden de ejecución.

No usar mocks de implementación si la API real permite instalar capacidades directamente.

No probar PluginInstaller ni StudioBootstrap.

---

# 8. VALIDACIÓN

Antes de crear el contrato:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Línea base esperada:

```text
13 archivos
110 pruebas
PASS
```

Después de crear el contrato, ejecutar nuevamente.

Resultado esperado:

```text
14 archivos
nuevos casos de FeatureManager pasando
exit code 0
```

Reportar conteos reales.

---

# 9. PROHIBICIONES

No modificar:

```text
FeatureManager.js
DashboardRegistry.js
WidgetRegistry.js
module/commercial/**
DashboardRuntime.js
DashboardRenderer.js
DashboardCompositionResolver.js
PluginInstaller.js
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

# 10. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Ruta exacta del contrato creado.
6. API real de FeatureManager utilizada.
7. Casos definidos.
8. Estrategia de aislamiento.
9. Contenido completo del contrato.
10. Resultado de línea base.
11. Resultado final.
12. Exit code y conteos.
13. Confirmación del routing correcto.
14. Confirmación del caso Commercial real.
15. Confirmación de resolución end-to-end posterior al routing.
16. `git --no-pager diff --stat`.
17. `git status --short` final.
18. Confirmación de que no se modificó producción.
19. Confirmación de que Toolchain no fue tocado.
20. Confirmación de que nada fue staged, committed o pushed.

---

# 11. DETENERSE

Detenerse después del contrato.

No corregir `installedPlugins`.

No ejecutar el siguiente STEP.

Finalizar con:

```text
git status --short
```

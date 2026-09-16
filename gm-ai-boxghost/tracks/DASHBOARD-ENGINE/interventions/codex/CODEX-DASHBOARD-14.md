# CODEX-DASHBOARD-14

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-14 — Contrato end-to-end del Commercial Dashboard  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-13.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: primer consumidor Commercial del Dashboard Engine
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Crear un contrato end-to-end que demuestre que el Commercial Dashboard puede:

1. registrar su Dashboard;
2. registrar sus Widgets;
3. resolver `widgetCode`;
4. producir un payload renderer-neutral mediante:

```javascript
resolveDashboardCompositionForRender(code, options)
```

No modificar producción en este STEP.

---

# 3. COMANDOS INICIALES

Ejecutar:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

Proteger cambios preexistentes.

No ejecutar `git add`, `git commit`, `git push`, `git restore`, `git clean`, `git reset` ni `git stash`.

---

# 4. INSPECCIÓN OBLIGATORIA

Leer completos:

```text
gypport/platform_os/studio/module/commercial/dashboard/CommercialDashboard.js
gypport/platform_os/studio/module/commercial/widget/CommercialTotalKpiWidget.js
gypport/platform_os/studio/module/commercial/widget/CommercialMonthlyChartWidget.js
gypport/platform_os/studio/module/commercial/domain/business-partner/feature/BusinessPartnerProfileFeature.js

gypport/platform_os/studio/engine/framework/feature/runtime/FeatureManager.js

gypport/platform_os/studio/engine/core/registry/ui/DashboardRegistry.js
gypport/platform_os/studio/engine/core/registry/ui/WidgetRegistry.js

gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRenderer.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRuntime.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
```

Verificar exports públicos reales.

No modificar archivos inspeccionados.

---

# 5. ÚNICO ARCHIVO AUTORIZADO

Crear solamente:

```text
gypport/platform_os/studio/contracts/dashboard/CommercialDashboardIntegration.contract.mjs
```

No modificar ningún otro archivo.

---

# 6. CASOS OBLIGATORIOS

El contrato debe probar:

1. El Commercial Dashboard tiene código estable.
2. Sus bindings contienen los `widgetCode` esperados.
3. Los dos Widgets comerciales pueden registrarse.
4. El Dashboard comercial puede registrarse.
5. `resolveDashboardCompositionForRender` devuelve:
   - `schema`;
   - `widgets`;
   - `renderer`;
   - `device`;
   - `layout`;
   - `readonly`.
6. Cada binding se resuelve contra la definición correcta.
7. Se conserva el orden declarado.
8. Se conservan referencias de bindings y definiciones.
9. El payload no contiene estado de instancia.
10. El payload permanece neutral respecto de React y DOM.
11. Si se omite un Widget comercial, la resolución falla `FAIL CLOSED`.
12. El error identifica el `widgetCode` faltante y el Dashboard comercial.

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

No usar mocks de implementación.

---

# 8. DECISIÓN DE REGISTRO

El contrato puede registrar directamente las definiciones comerciales usando las APIs públicas de Registry.

No debe probar todavía:

```text
PluginInstaller
StudioBootstrap
installedPlugins
Browser Shell
```

Esos pertenecen a otro boundary.

---

# 9. VALIDACIÓN

Antes de crear el contrato:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Línea base esperada:

```text
12 archivos
98 pruebas
PASS
```

Después de crear el contrato, ejecutar nuevamente.

Resultado esperado:

```text
13 archivos
nuevos casos Commercial pasando
exit code 0
```

Reportar conteos reales.

---

# 10. PROHIBICIONES

No modificar:

```text
module/commercial/**
DashboardRuntime.js
DashboardRenderer.js
DashboardCompositionResolver.js
DashboardRegistry.js
WidgetRegistry.js
FeatureManager.js
StudioBootstrap.js
module/index.js
```

No resolver:

```text
installedPlugins
Browser Shell
App composition
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
5. Ruta del contrato creado.
6. Casos definidos.
7. Estrategia de registro y aislamiento.
8. Contenido completo del contrato.
9. Resultado de línea base.
10. Resultado final.
11. Exit code y conteos.
12. Confirmación de resolución correcta de Widgets.
13. Confirmación de orden y referencias.
14. Confirmación de `FAIL CLOSED`.
15. `git --no-pager diff --stat`.
16. `git status --short` final.
17. Confirmación de que no se modificó producción.
18. Confirmación de que Toolchain no fue tocado.
19. Confirmación de que nada fue staged, committed o pushed.

---

# 12. DETENERSE

Detenerse después del contrato.

No corregir `installedPlugins`.

No ejecutar el siguiente STEP.

Finalizar con:

```text
git status --short
```

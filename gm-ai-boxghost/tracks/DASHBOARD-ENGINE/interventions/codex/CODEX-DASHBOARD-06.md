# CODEX-DASHBOARD-06

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-06 — Implementación mínima de DashboardCompositionResolver  
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
gypport/docs/architecture/STRUCTURE_CANONICAL.md
gypport/docs/architecture/BOUNDARY_RULES.md
gypport/docs/architecture/ACTIVE_TRACKS.md
gypport/docs/ai/codex/CODEX-DASHBOARD-05.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: implementación mínima de DashboardCompositionResolver
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Implementar únicamente:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
```

La implementación debe satisfacer:

```text
gypport/platform_os/studio/contracts/dashboard/DashboardCompositionResolver.contract.mjs
```

No modificar Runtime, Renderer ni Registry.

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
gypport/platform_os/studio/contracts/dashboard/DashboardCompositionResolver.contract.mjs
gypport/platform_os/studio/engine/core/registry/ui/WidgetRegistry.js
gypport/platform_os/studio/engine/core/registry/ui/index.js
gypport/platform_os/studio/engine/core/registry/index.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardSchema.js
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
gypport/platform_os/studio/engine/core/ui/index.js
```

Verificar la API pública exacta disponible para resolver widgets.

No inventar nombres de exports.

---

# 5. ARCHIVOS AUTORIZADOS

Crear o modificar solamente:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
```

`index.js` solo puede modificarse para exportar públicamente el Resolver.

---

# 6. API OBLIGATORIA

Implementar:

```javascript
export function resolveDashboardComposition(dashboardSchema)
```

Debe:

1. Recibir un Dashboard Schema.
2. Recorrer `dashboardSchema.widgets`.
3. Resolver cada `binding.widgetCode` mediante WidgetRegistry.
4. Conservar el orden original.
5. Retornar:

```javascript
{
  schema: dashboardSchema,
  widgets: [
    {
      binding,
      definition
    }
  ]
}
```

---

# 7. REGLAS

Conservar referencias:

```text
composition.schema === dashboardSchema
composition.widgets[index].binding === dashboardSchema.widgets[index]
composition.widgets[index].definition === definición registrada
```

No ordenar por `order`, `widgetCode` ni Registry.

Dos bindings con el mismo `widgetCode` deben producir dos posiciones independientes.

No fusionar `binding` y `definition`.

La configuración del binding no debe sobrescribir la definición.

Política de widget inexistente:

```text
FAIL CLOSED
```

Mensaje exacto:

```text
Widget "<widgetCode>" is not registered for dashboard "<dashboardCode>".
```

No devolver composición parcial.

No importar React, DOM, Channel, Module ni Journey.

---

# 8. IMPLEMENTACIÓN MÍNIMA

No crear clases, caché, estado global, mocks, adaptadores, factories, errores personalizados, Frameworks ni Registries nuevos.

No agregar campos no exigidos por el contrato.

---

# 9. PROHIBICIONES

No modificar:

```text
DashboardRuntime.js
DashboardRenderer.js
DashboardSchema.js
DashboardBuilder.js
DashboardValidator.js
WidgetRegistry.js
WidgetRuntime.js
WidgetRenderer.js
StudioBootstrap.js
vitest.config.js
package.json
```

No tocar `module/`, `journey/`, `app/`, Browser Shell source, Toolchain ni Server.

No resolver `installedPlugins`.

No integrar todavía el Resolver con Runtime o Renderer.

---

# 10. VALIDACIÓN

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Resultado esperado:

```text
9 archivos de prueba
70 pruebas
PASS
exit code 0
```

Si el conteo real difiere, reportarlo.

No modificar el contrato.

---

# 11. BUILD

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

Puede seguir fallando únicamente por:

```text
installedPlugins is not exported by module/index.js
```

No corregirlo.

Confirmar que no exista error nuevo relacionado con DashboardCompositionResolver, WidgetRegistry o barrels.

---

# 12. REPORTE FINAL

Entregar:

1. Root.
2. Branch.
3. `git status --short` inicial.
4. Cumplimiento arquitectónico.
5. Archivos inspeccionados.
6. Archivos creados o modificados.
7. Contenido completo de `DashboardCompositionResolver.js`.
8. Diff exacto de `dashboard/index.js`, si cambia.
9. API de WidgetRegistry utilizada.
10. Confirmación de orden y referencias.
11. Confirmación fail-closed.
12. Salida completa de contracts.
13. Exit code y conteos.
14. Salida completa de build.
15. Exit code del build.
16. Próximo blocker exacto.
17. `git --no-pager diff --stat`.
18. `git status --short` final.
19. Confirmación de que Runtime, Renderer y WidgetRegistry no fueron modificados.
20. Confirmación de que Toolchain no fue tocado.
21. Confirmación de que nada fue staged, committed o pushed.

---

# 13. DETENERSE

Detenerse si se requiere modificar más de los dos archivos autorizados, si WidgetRegistry no ofrece API pública utilizable o si falla algún contrato anterior.

No ejecutar DASHBOARD-07.

Finalizar con:

```text
git status --short
```

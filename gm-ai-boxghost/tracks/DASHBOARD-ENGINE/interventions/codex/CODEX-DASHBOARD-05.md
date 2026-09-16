# CODEX-DASHBOARD-05

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-05 — Contrato de DashboardCompositionResolver  
**Mode:** Contract First  
**Agent:** Codex  
**Status:** Ready for Execution  

---

# 1. CUMPLIMIENTO ARQUITECTÓNICO

Leer primero:

```text
AGENTS.md
Reglas.md
docs/architecture/ARCHITECTURE_GOVERNANCE.md
docs/architecture/PLATFORM_FOUNDATION.md
docs/architecture/STRUCTURE_CANONICAL.md
docs/architecture/BOUNDARY_RULES.md
docs/architecture/ACTIVE_TRACKS.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: contrato de composición Dashboard → Widget
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Crear el contrato ejecutable que defina el comportamiento futuro de:

```text
DashboardCompositionResolver
```

El Resolver todavía no debe implementarse en este STEP.

No modificar código de producción.

---

# 3. DECISIÓN ARQUITECTÓNICA CERRADA

La composición será propiedad de:

```text
platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
```

Flujo aprobado:

```text
DashboardRuntime
        ↓
DashboardCompositionResolver
        ↓
WidgetRegistry
        ↓
Dashboard compuesto
        ↓
DashboardRenderer
```

Responsabilidades:

```text
DashboardRuntime
- ciclo de vida
- instancia
- estado

DashboardCompositionResolver
- resolver widgetCode
- consultar WidgetRegistry
- unir binding + definition
- conservar orden
- fallar si falta un widget

DashboardRenderer
- recibir composición resuelta
- no consultar Registry

Channel
- representar
- no resolver widgets
```

---

# 4. COMANDOS INICIALES OBLIGATORIOS

Ejecutar:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

Proteger todos los cambios preexistentes.

No hacer:

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
platform_os/studio/engine/core/ui/dashboard/DashboardSchema.js
platform_os/studio/engine/core/ui/dashboard/DashboardRuntime.js
platform_os/studio/engine/core/ui/dashboard/DashboardRenderer.js
platform_os/studio/engine/core/registry/ui/WidgetRegistry.js
platform_os/studio/engine/core/ui/widget/WidgetSchema.js

platform_os/studio/contracts/dashboard/DashboardRuntime.contract.mjs
platform_os/studio/contracts/dashboard/DashboardRenderer.contract.mjs
platform_os/studio/contracts/registry/ui/DashboardRegistry.contract.mjs

platform_os/studio/channel/browser/shell/vitest.config.js
platform_os/studio/channel/browser/shell/package.json
```

Inspeccionar también los barrels públicos aplicables.

No modificar archivos inspeccionados.

---

# 6. ÚNICO ARCHIVO AUTORIZADO

Crear solamente:

```text
platform_os/studio/contracts/dashboard/DashboardCompositionResolver.contract.mjs
```

No crear todavía:

```text
platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
```

No modificar ningún otro archivo.

---

# 7. API FUTURA A CONTRATAR

El contrato debe asumir esta función pública futura:

```javascript
resolveDashboardComposition(dashboardSchema)
```

La implementación futura deberá resolver cada:

```javascript
dashboardSchema.widgets[].widgetCode
```

mediante el `WidgetRegistry`.

---

# 8. SALIDA CONTRATADA

Salida conceptual:

```javascript
{
  schema: dashboardSchema,
  widgets: [
    {
      binding: dashboardWidgetBinding,
      definition: registeredWidgetDefinition
    }
  ]
}
```

Reglas:

```text
schema
- conserva la referencia original del DashboardSchema

binding
- conserva la referencia original del binding declarado en dashboard.widgets[]

definition
- conserva la referencia de la definición registrada en WidgetRegistry

widgets
- conserva el orden exacto de dashboardSchema.widgets
```

No fusionar destructivamente:

```text
binding
definition
```

Deben permanecer como objetos separados.

---

# 9. CASOS OBLIGATORIOS

El contrato debe definir, como mínimo:

## Caso 1

Dashboard sin widgets devuelve:

```javascript
{
  schema: dashboardSchema,
  widgets: []
}
```

## Caso 2

Un widget registrado se resuelve correctamente mediante `widgetCode`.

## Caso 3

Se conserva la referencia original de:

```javascript
composition.schema
```

## Caso 4

Se conserva la referencia original de:

```javascript
composition.widgets[index].binding
```

## Caso 5

Se conserva la referencia registrada de:

```javascript
composition.widgets[index].definition
```

## Caso 6

Se conserva exactamente el orden declarado en:

```javascript
dashboardSchema.widgets
```

## Caso 7

Dos bindings con el mismo `widgetCode` permanecen como dos posiciones independientes.

## Caso 8

La configuración del binding no sobrescribe campos de la definición registrada.

Ejemplo:

```javascript
binding.configuration
```

no debe mutar:

```javascript
definition.configuration
```

## Caso 9

Un widget inexistente falla de forma determinista.

## Caso 10

El error identifica:

```text
widgetCode
dashboardCode
```

## Caso 11

No se devuelve una composición parcial cuando falta un widget.

## Caso 12

El Resolver no depende de:

```text
React
DOM
Channel
Business Module
Journey
```

---

# 10. POLÍTICA DE WIDGET INEXISTENTE

Política cerrada:

```text
FAIL CLOSED
```

Mensaje conceptual esperado:

```text
Widget "<widgetCode>" is not registered for dashboard "<dashboardCode>".
```

No:

```text
omitir silenciosamente
devolver null
continuar parcialmente
reemplazar por placeholder
```

---

# 11. AISLAMIENTO DEL REGISTRY

`WidgetRegistry` usa estado compartido de módulo.

Usar:

```text
beforeEach
afterEach
```

para limpiar el Registry mediante su API pública.

Ningún caso puede depender del orden de ejecución.

No acceder directamente al `Map` interno.

---

# 12. ESTADO ROJO CONTROLADO

Como el Resolver todavía no existe, el nuevo contrato puede quedar rojo.

El fallo aceptable debe deberse únicamente a:

```text
módulo inexistente
export inexistente
DashboardCompositionResolver no implementado
```

Los contratos anteriores deben permanecer verdes.

No usar:

```text
skip
todo
mock de implementación
implementación dentro del contrato
```

No modificar producción para forzar PASS.

---

# 13. VALIDACIÓN DE LÍNEA BASE

Antes de crear el nuevo contrato, ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Línea base esperada:

```text
8 archivos
58 pruebas
PASS
```

Reportar resultado real.

---

# 14. VALIDACIÓN ROJA

Después de crear el contrato, ejecutar nuevamente:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Resultado esperado:

```text
el nuevo contrato falla únicamente porque DashboardCompositionResolver no existe

los 8 archivos anteriores continúan pasando

no aparecen otros fallos
```

Si el runner no puede descubrir parcialmente los demás contratos debido al error de importación, ejecutar además una validación explícita de los 8 contratos anteriores sin incluir el nuevo archivo y reportar ambos resultados.

No modificar `vitest.config.js`.

---

# 15. PROHIBICIONES ESTRICTAS

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
implementar el Resolver
integrarlo al Runtime
cambiar payloads
agregar campos especulativos
resolver installedPlugins
crear UI
crear widgets comerciales
```

---

# 16. REPORTE FINAL OBLIGATORIO

Entregar:

```text
1. Root del repositorio

2. Branch

3. git status --short inicial

4. Resultado de cumplimiento arquitectónico

5. Archivos inspeccionados

6. Ruta exacta del contrato creado

7. Casos de contrato definidos

8. Política de error definida

9. Estrategia de aislamiento de WidgetRegistry

10. Contenido completo de DashboardCompositionResolver.contract.mjs

11. Comando y salida completa de línea base

12. Exit code y conteos de línea base

13. Comando y salida completa del estado rojo

14. Exit code del estado rojo

15. Causa exacta del fallo

16. Confirmación de que los 8 contratos anteriores siguen verdes

17. git --no-pager diff --stat

18. git status --short final

19. Confirmación de que no se modificó producción

20. Confirmación de que DashboardRuntime y DashboardRenderer no fueron tocados

21. Confirmación de que Toolchain no fue tocado

22. Confirmación de que nada fue staged, committed o pushed
```

---

# 17. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
root o branch difieren

el contrato requiere modificar producción

el fallo no se limita al Resolver inexistente

algún contrato anterior deja de pasar

cambia un archivo fuera del único autorizado

WidgetRegistry no ofrece API pública suficiente para preparar el contrato
```

No improvisar.

---

# 18. DETENERSE

Detenerse después del contrato rojo controlado.

No ejecutar:

```text
DASHBOARD-06
```

No implementar:

```text
DashboardCompositionResolver.js
```

Finalizar con:

```text
git status --short
```
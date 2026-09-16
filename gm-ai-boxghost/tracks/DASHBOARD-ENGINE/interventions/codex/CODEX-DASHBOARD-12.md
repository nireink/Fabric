# CODEX-DASHBOARD-12

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-12 — Contrato de integración Renderer ← Composition  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-11.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: contrato DashboardRenderer consumiendo composición resuelta
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. OBJETIVO

Crear un contrato ejecutable para definir cómo `DashboardRenderer` debe consumir una composición ya resuelta.

No modificar producción.

No integrar todavía el Renderer.

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
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRenderer.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardRuntime.js
gypport/platform_os/studio/engine/core/ui/dashboard/DashboardCompositionResolver.js
gypport/platform_os/studio/contracts/dashboard/DashboardRenderer.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardRuntimeComposition.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardCompositionResolver.contract.mjs
```

No modificar archivos inspeccionados.

---

# 5. ÚNICO ARCHIVO AUTORIZADO

Crear solamente:

```text
gypport/platform_os/studio/contracts/dashboard/DashboardRendererComposition.contract.mjs
```

No modificar ningún otro archivo.

---

# 6. API FUTURA A CONTRATAR

La integración futura debe exponer desde:

```text
@core/ui/dashboard/DashboardRenderer
```

una función interna:

```javascript
resolveDashboardCompositionForRender(code, options)
```

Responsabilidad:

1. Obtener la composición mediante `loadDashboardComposition(code)`.
2. Devolver un payload renderer-neutral.
3. Conservar `schema`.
4. Conservar `widgets` ya resueltos.
5. Añadir únicamente metadata de render aprobada.
6. No consultar DashboardRegistry directamente.
7. No consultar WidgetRegistry directamente.
8. No resolver widgets nuevamente.
9. No crear una instancia de Dashboard.
10. No depender de React, DOM, Channel, Module ni Journey.

---

# 7. PAYLOAD ESPERADO

Salida conceptual:

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

Reglas:

```text
schema
- misma referencia recibida desde la composición

widgets
- mismo array de composición resuelta

renderer
- conserva default y override actuales del Renderer

device
- conserva default y override actuales

layout
- conserva default y override actuales

readonly
- conserva default y override actuales
```

No incluir:

```text
runtime instance
widgetsState
loading
error
editable
```

---

# 8. CASOS OBLIGATORIOS

Definir como mínimo:

1. Resuelve un Dashboard registrado y devuelve composición lista para render.
2. Conserva referencia de `schema`.
3. Conserva referencia del array `widgets`.
4. Conserva cada `binding`.
5. Conserva cada `definition`.
6. Conserva el orden de widgets.
7. Conserva defaults actuales de renderer metadata.
8. Conserva overrides actuales de renderer metadata.
9. Propaga error de Dashboard inexistente.
10. Propaga error de Widget inexistente.
11. No devuelve composición parcial.
12. No contiene estado de instancia.
13. No consulta Registry directamente desde el contrato.
14. Permanece renderer-neutral.

---

# 9. ESTADO ROJO CONTROLADO

La función:

```javascript
resolveDashboardCompositionForRender
```

todavía no existe.

El contrato debe quedar rojo únicamente por función/export inexistente.

Línea base esperada:

```text
11 archivos
84 pruebas
PASS
```

Después del nuevo contrato:

```text
12 archivos descubiertos
nuevo contrato rojo
11 contratos anteriores verdes
```

No usar `skip`, `todo` ni mocks de implementación.

---

# 10. VALIDACIÓN

Antes de crear el contrato:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Después de crearlo, ejecutar nuevamente el mismo comando.

Reportar conteos reales y causa exacta del rojo.

---

# 11. PROHIBICIONES

No modificar:

```text
DashboardRenderer.js
DashboardRuntime.js
DashboardCompositionResolver.js
DashboardRegistry.js
WidgetRegistry.js
dashboard/index.js
core/ui/index.js
contracts existentes
```

No tocar Module, Journey, App, Browser Shell source, Toolchain ni Server.

No resolver `installedPlugins`.

---

# 12. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Ruta del contrato creado.
6. Casos definidos.
7. Payload contratado.
8. Estrategia de aislamiento.
9. Contenido completo del contrato.
10. Resultado de línea base.
11. Resultado rojo controlado.
12. Exit code y conteos.
13. Causa exacta del fallo.
14. Confirmación de que los 11 contratos anteriores siguen verdes.
15. `git --no-pager diff --stat`.
16. `git status --short` final.
17. Confirmación de que no se modificó producción.
18. Confirmación de que Toolchain no fue tocado.
19. Confirmación de que nada fue staged, committed o pushed.

---

# 13. DETENERSE

Detenerse después del contrato rojo controlado.

No implementar todavía:

```text
resolveDashboardCompositionForRender
```

No ejecutar el siguiente STEP.

Finalizar con:

```text
git status --short
```

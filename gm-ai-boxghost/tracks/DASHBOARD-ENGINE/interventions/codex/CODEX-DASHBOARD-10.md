# CODEX-DASHBOARD-10

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-10 — Contrato de integración Runtime → CompositionResolver  
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
gypport/docs/ai/codex/CODEX-DASHBOARD-09B.md
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: contrato de integración DashboardRuntime → DashboardCompositionResolver
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Crear un contrato ejecutable que defina la futura integración entre:

```text
DashboardRuntime
        ↓
DashboardCompositionResolver
```

No modificar producción en este STEP.

No modificar Renderer.

No integrar todavía el Resolver.

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
gypport/platform_os/studio/engine/core/registry/ui/DashboardRegistry.js
gypport/platform_os/studio/engine/core/registry/ui/WidgetRegistry.js

gypport/platform_os/studio/contracts/dashboard/DashboardRuntime.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardCompositionResolver.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardRenderer.contract.mjs
```

Inspeccionar las rutas internas explícitas utilizadas por los contratos.

No modificar archivos inspeccionados.

---

# 5. ÚNICO ARCHIVO AUTORIZADO

Crear solamente:

```text
gypport/platform_os/studio/contracts/dashboard/DashboardRuntimeComposition.contract.mjs
```

No modificar ningún otro archivo.

---

# 6. API FUTURA A CONTRATAR

La integración futura debe exponer una función interna explícita desde:

```text
@core/ui/dashboard/DashboardRuntime
```

Nombre esperado:

```javascript
loadDashboardComposition(code)
```

Su responsabilidad será:

1. Cargar el Dashboard registrado mediante `DashboardRuntime`.
2. Pasar el schema cargado a `resolveDashboardComposition`.
3. Retornar la composición resuelta.
4. Propagar errores de Dashboard inexistente.
5. Propagar errores de Widget inexistente.
6. No modificar estado de instancia.
7. No invocar Renderer.
8. No depender de React, Channel ni módulos de negocio.

---

# 7. CASOS OBLIGATORIOS

Definir como mínimo:

1. Carga un Dashboard registrado y devuelve composición resuelta.
2. Conserva la referencia original del schema registrado.
3. Conserva referencias de bindings.
4. Conserva referencias de definiciones de widgets.
5. Conserva el orden declarado de widgets.
6. Propaga el error actual de Dashboard inexistente.
7. Propaga el error fail-closed de Widget inexistente.
8. No devuelve composición parcial.
9. No crea una instancia de Dashboard.
10. No muta el estado Runtime existente.
11. No invoca Renderer.
12. Permanece neutral respecto de React, DOM, Channel, Module y Journey.

No inventar comportamiento adicional.

---

# 8. AISLAMIENTO

Usar APIs públicas para limpiar:

```text
DashboardRegistry
WidgetRegistry
estado Runtime, cuando exista API pública aplicable
```

Usar:

```text
beforeEach
afterEach
```

Ningún test puede depender del orden de ejecución.

---

# 9. ESTADO ROJO CONTROLADO

La función:

```javascript
loadDashboardComposition
```

todavía no existe.

El nuevo contrato debe quedar rojo únicamente por:

```text
export inexistente
función inexistente
```

La línea base anterior debe permanecer verde:

```text
10 archivos
72 pruebas
PASS
```

No usar `skip`, `todo` ni mocks de implementación.

No modificar producción para forzar PASS.

---

# 10. VALIDACIÓN

Antes de crear el contrato:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Esperado:

```text
10 archivos
72 pruebas
PASS
```

Después de crear el contrato, ejecutar nuevamente.

Esperado:

```text
11 archivos descubiertos
nuevo contrato rojo únicamente por loadDashboardComposition inexistente
10 contratos anteriores verdes
```

Reportar conteos reales.

---

# 11. PROHIBICIONES

No modificar:

```text
DashboardRuntime.js
DashboardCompositionResolver.js
DashboardRenderer.js
DashboardRegistry.js
WidgetRegistry.js
dashboard/index.js
core/ui/index.js
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

No resolver `installedPlugins`.

No integrar Renderer.

No crear API pública adicional en `@core/ui`.

---

# 12. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Ruta exacta del contrato creado.
6. Casos definidos.
7. Estrategia de aislamiento.
8. Contenido completo del contrato.
9. Resultado de línea base.
10. Resultado rojo controlado.
11. Exit code y conteos.
12. Causa exacta del fallo.
13. Confirmación de que los 10 contratos anteriores siguen verdes.
14. `git --no-pager diff --stat`.
15. `git status --short` final.
16. Confirmación de que no se modificó producción.
17. Confirmación de que Toolchain no fue tocado.
18. Confirmación de que nada fue staged, committed o pushed.

---

# 13. DETENERSE

Detenerse después del contrato rojo controlado.

No implementar todavía:

```text
loadDashboardComposition
```

No ejecutar el siguiente STEP.

Finalizar con:

```text
git status --short
```

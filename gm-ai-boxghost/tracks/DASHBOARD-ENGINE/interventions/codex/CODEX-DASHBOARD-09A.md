# CODEX-DASHBOARD-09A

## GYPPORT® PLATFORM OS

**Track:** Dashboard Engine  
**Step:** DASHBOARD-09A — Alinear contratos internos con rutas explícitas  
**Mode:** Corrección mínima de contratos  
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
```

Declarar:

```text
Track activo: Dashboard Engine
Boundary autorizado: imports internos de contratos Runtime y Renderer
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Corregir únicamente los imports de contratos internos para que dejen de depender del barrel público:

```text
@core/ui
```

y consuman rutas internas explícitas:

```text
@core/ui/dashboard/DashboardRuntime
@core/ui/dashboard/DashboardRenderer
```

No cambiar comportamiento ni assertions.

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

# 4. ARCHIVOS AUTORIZADOS

Modificar solamente:

```text
gypport/platform_os/studio/contracts/dashboard/DashboardRuntime.contract.mjs
gypport/platform_os/studio/contracts/dashboard/DashboardRenderer.contract.mjs
```

No modificar ningún otro archivo.

---

# 5. CAMBIO EXACTO

## DashboardRuntime.contract.mjs

Mover únicamente los imports internos de Runtime desde:

```javascript
import {
  ...
} from "@core/ui";
```

hacia:

```javascript
import {
  ...
} from "@core/ui/dashboard/DashboardRuntime";
```

Mantener en `@core/ui` solamente factories, schemas, types o utilidades declarativas que realmente pertenezcan a la API pública.

## DashboardRenderer.contract.mjs

Mover únicamente los imports internos de Renderer desde:

```javascript
import {
  ...
} from "@core/ui";
```

hacia:

```javascript
import {
  ...
} from "@core/ui/dashboard/DashboardRenderer";
```

Si el contrato usa símbolos internos de Runtime, importarlos desde:

```javascript
@core/ui/dashboard/DashboardRuntime
```

Mantener en `@core/ui` únicamente la API declarativa pública.

---

# 6. REGLAS

No modificar:

```text
nombres de tests
assertions
fixtures
setup/teardown
semántica esperada
conteo de casos
```

No agregar tests nuevos.

No borrar tests.

No usar mocks nuevos.

No cambiar producción.

---

# 7. VALIDACIÓN

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Resultado esperado mientras el barrel público todavía no cambia:

```text
10 archivos descubiertos
1 contrato público rojo
9 contratos anteriores verdes
72 pruebas totales
```

El único fallo permitido sigue siendo:

```text
DashboardPublicApi.contract.mjs
```

Los contratos:

```text
DashboardRuntime.contract.mjs
DashboardRenderer.contract.mjs
```

deben permanecer verdes usando rutas internas explícitas.

---

# 8. BÚSQUEDA FINAL

Confirmar que estos dos contratos ya no importan símbolos internos desde:

```text
@core/ui
```

Reportar los imports finales exactos.

---

# 9. PROHIBICIONES

No modificar:

```text
gypport/platform_os/studio/engine/**
gypport/platform_os/studio/channel/**
gypport/platform_os/studio/contracts/dashboard/DashboardPublicApi.contract.mjs
```

No tocar Toolchain, Module, Journey, App ni Server.

No ocultar todavía exports del barrel.

No resolver `installedPlugins`.

---

# 10. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Archivos inspeccionados.
4. Archivos modificados.
5. Diff exacto de imports.
6. Confirmación de que no cambió ninguna assertion.
7. Salida completa de contracts.
8. Exit code y conteos.
9. Único fallo restante.
10. `git --no-pager diff --stat`.
11. `git status --short` final.
12. Confirmación de que no se modificó producción.
13. Confirmación de que Toolchain no fue tocado.
14. Confirmación de que nada fue staged, committed o pushed.

---

# 11. DETENERSE

Detenerse después de validar.

No modificar todavía:

```text
gypport/platform_os/studio/engine/core/ui/dashboard/index.js
```

Finalizar con:

```text
git status --short
```

# CODEX-BOOTSTRAP-02

## GYPPORT® PLATFORM OS

**Track:** Browser Bootstrap Recovery  
**Step:** BOOTSTRAP-02 — Implementación mínima de composición `installedPlugins`  
**Mode:** Implementación mínima guiada por arquitectura  
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
gypport/docs/architecture/ROOT_DIRECTORY_RESPONSIBILITIES.md
gypport/docs/architecture/STRUCTURE_CANONICAL.md
gypport/docs/architecture/BOUNDARY_RULES.md
gypport/docs/architecture/ACTIVE_TRACKS.md
gypport/docs/ai/codex/CODEX-BOOTSTRAP-01.md
```

Declarar:

```text
Track activo: Browser Bootstrap Recovery
Boundary autorizado: composición inicial de plugins de Business Studio
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si la decisión no es `PASS`, detenerse.

---

# 2. OBJETIVO

Crear el owner correcto de la composición inicial de plugins en:

```text
gypport/platform_os/studio/app/business-studio/
```

y corregir `StudioBootstrap.js` para importar `installedPlugins` desde esa app concreta.

No modificar `module/index.js`.

No descubrir plugins dinámicamente.

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
gypport/platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
gypport/platform_os/studio/module/commercial/index.js
gypport/platform_os/studio/module/commercial/CommercialPlugin.js
gypport/platform_os/studio/module/index.js
gypport/platform_os/studio/engine/framework/plugin/runtime/PluginManager.js
gypport/platform_os/studio/engine/framework/plugin/runtime/PluginInstaller.js
gypport/platform_os/studio/channel/browser/shell/vite.alias.js
```

Confirmar que:

```text
@app existe
CommercialPlugin es el único plugin real inicial
installedPlugins no existe como composición de producto
```

---

# 5. ARCHIVOS AUTORIZADOS

Crear:

```text
gypport/platform_os/studio/app/business-studio/installedPlugins.js
gypport/platform_os/studio/app/business-studio/index.js
```

Modificar:

```text
gypport/platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
```

No modificar ningún otro archivo.

---

# 6. IMPLEMENTACIÓN REQUERIDA

## `installedPlugins.js`

Debe importar `CommercialPlugin` desde su surface público real y exportar:

```javascript
export const installedPlugins = [
  CommercialPlugin
];
```

No duplicar ni transformar el plugin.

No incluir placeholders.

No incluir plugins inexistentes.

## `index.js`

Debe exportar:

```javascript
export * from "./installedPlugins";
```

## `StudioBootstrap.js`

Cambiar únicamente el origen del import:

```javascript
import { installedPlugins } from "@module";
```

por:

```javascript
import { installedPlugins } from "@app/business-studio";
```

No modificar ninguna otra línea de bootstrap.

---

# 7. REGLAS DE OWNERSHIP

```text
module/
- define capacidades y plugins de negocio

app/business-studio/
- decide qué plugins instala el producto

channel/browser/shell/
- ejecuta bootstrap tecnológico

engine/
- instala y registra plugins
```

No mover `CommercialPlugin`.

No exportar `installedPlugins` desde `module/index.js`.

---

# 8. VALIDACIÓN DE CONTRATOS

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Resultado esperado:

```text
15 archivos
133 pruebas
PASS
exit code 0
```

Reportar el conteo real.

---

# 9. VALIDACIÓN DE BUILD

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

El error de:

```text
installedPlugins is not exported by module/index.js
```

debe desaparecer.

Si aparece un nuevo blocker, reportarlo textualmente y detenerse.

No corregirlo en este STEP.

---

# 10. VALIDACIÓN DEV

Ejecutar de forma controlada:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run dev
```

Capturar:

```text
Vite ready
URL local
errores de compilación o linking
```

Detener el servidor después de obtener evidencia.

Confirmar que no quede proceso escuchando en el puerto.

No afirmar que la aplicación funciona visualmente si no se verificó en navegador real.

---

# 11. PROHIBICIONES

No modificar:

```text
gypport/platform_os/studio/module/index.js
gypport/platform_os/studio/module/commercial/**
gypport/platform_os/studio/engine/**
gypport/platform_os/studio/contracts/**
gypport/developer_platform/toolchain/**
gypport/platform_os/server/**
```

No resolver otros blockers.

No reorganizar Studio.

No crear más apps.

---

# 12. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Archivos creados y modificados.
6. Contenido completo de `installedPlugins.js`.
7. Contenido completo de `app/business-studio/index.js`.
8. Diff exacto de `StudioBootstrap.js`.
9. Confirmación de que `module/index.js` no fue modificado.
10. Salida completa de contracts.
11. Exit code y conteos.
12. Salida completa de build.
13. Exit code del build.
14. Confirmación de desaparición del blocker `installedPlugins`.
15. Próximo blocker exacto o build success.
16. Salida relevante de dev.
17. Confirmación de detención del servidor.
18. `git --no-pager diff --stat`.
19. `git status --short` final.
20. Confirmación de que Toolchain no fue tocado.
21. Confirmación de que nada fue staged, committed o pushed.

---

# 13. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
CommercialPlugin no es el único plugin inicial real

@app no resuelve correctamente

se requiere modificar más de los tres archivos autorizados

algún contrato anterior deja de pasar

aparece un blocker nuevo fuera del boundary
```

No improvisar.

---

# 14. DETENERSE

Detenerse después de contracts, build y dev controlado.

No ejecutar el siguiente STEP.

Finalizar con:

```text
git status --short
```

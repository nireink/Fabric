# CODEX-BOOTSTRAP-01

## GYPPORT® PLATFORM OS

**Track:** Browser Bootstrap Recovery  
**Step:** BOOTSTRAP-01 — Reconnaissance de `installedPlugins`  
**Mode:** Solo lectura  
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
```

Declarar:

```text
Track activo: Browser Bootstrap Recovery
Boundary autorizado: ownership y resolución de installedPlugins
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. OBJETIVO

Determinar el owner correcto de:

```javascript
installedPlugins
```

y explicar por qué `StudioBootstrap.js` lo importa desde `@module` aunque `module/index.js` no lo exporta.

Este STEP es solo de reconnaissance. No modificar código.

---

# 3. COMANDOS INICIALES

Ejecutar:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

No ejecutar `git add`, `git commit`, `git push`, `git restore`, `git clean`, `git reset` ni `git stash`.

---

# 4. INSPECCIÓN OBLIGATORIA

Leer completos:

```text
gypport/platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
gypport/platform_os/studio/module/index.js
gypport/platform_os/studio/module/commercial/index.js
gypport/platform_os/studio/module/commercial/CommercialPlugin.js
gypport/platform_os/studio/engine/framework/plugin/runtime/PluginInstaller.js
```

Inspeccionar si existen actualmente:

```text
gypport/platform_os/studio/app/
gypport/platform_os/studio/app/business-studio/
gypport/platform_os/studio/app/business-studio/index.js
gypport/platform_os/studio/app/business-studio/installedPlugins.js
```

Buscar en todo `gypport/platform_os/studio/`, excluyendo `node_modules`:

```text
installedPlugins
CommercialPlugin
installAndRegisterPlugins
bootstrapStudio
```

---

# 5. PREGUNTAS OBLIGATORIAS

Responder con evidencia:

1. ¿Existe hoy algún owner real de `installedPlugins`?
2. ¿`module/index.js` es un barrel de capacidades o un punto de composición de producto?
3. ¿La Foundation asigna la composición de producto a `app/`?
4. ¿`StudioBootstrap` debe importar composición desde `@module` o desde `@app`?
5. ¿Existe alias `@app`?
6. ¿Existe actualmente una app concreta como `business-studio`?
7. ¿El mínimo conjunto instalado hoy es únicamente `CommercialPlugin`?
8. ¿Hay otros plugins reales que deban formar parte de la composición inicial?
9. ¿Crear `installedPlugins` en `module/index.js` violaría ownership?
10. ¿Cuál es el cambio mínimo correcto para desbloquear build y localhost sin reorganizar Studio?

---

# 6. OPCIONES A EVALUAR

Evaluar solo:

```text
OPCIÓN A
Exportar installedPlugins desde module/index.js.

OPCIÓN B
Crear app/business-studio/installedPlugins.js y exportarlo desde @app.

OPCIÓN C
Definir la lista dentro de StudioBootstrap.js.

OPCIÓN D
Eliminar installedPlugins y descubrir plugins dinámicamente.
```

Para cada opción indicar:

```text
cumplimiento Foundation
riesgo de ownership
acoplamiento
impacto futuro
superficie mínima de cambio
```

No implementar ninguna.

---

# 7. VALIDACIÓN PASIVA

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

Esperado:

```text
Contracts: 15 archivos / 133 pruebas / PASS
Build: falla por installedPlugins
```

Reportar resultados reales. No corregir el blocker.

---

# 8. PROHIBICIONES

No modificar ni crear archivos.

No tocar Dashboard Engine, Toolchain, Kernel, Core Runtime, CommercialPlugin, `module/index.js`, `StudioBootstrap.js` ni `app/`.

No resolver otros blockers.

---

# 9. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Resultados de búsqueda.
6. Owner actual de `installedPlugins`.
7. Owner arquitectónico correcto.
8. Comparación de opciones A-D.
9. Recomendación final.
10. Superficie exacta del próximo STEP.
11. Archivos permitidos y prohibidos para la corrección.
12. Resultado de contracts.
13. Resultado de build.
14. `git status --short` final.
15. Confirmación de que no se modificó nada.

---

# 10. DETENERSE

Detenerse después del reporte.

No implementar la corrección.

Finalizar con:

```text
git status --short
```

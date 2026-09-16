# CODEX-AUTH-02A

## GYPPORT® PLATFORM OS

**Track:** Authentication Journey  
**Step:** AUTH-02A — Habilitar alias `@journey` para Vite y Vitest  
**Mode:** Minimal Infrastructure Fix  
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
gypport/docs/ai/codex/CODEX-AUTH-01.md
gypport/docs/ai/codex/CODEX-AUTH-02.md
```

Declarar:

```text
Track activo: Authentication Journey
Boundary autorizado: resolución del alias @journey
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. OBJETIVO

Habilitar el alias:

```text
@journey
```

para que Vite y Vitest resuelvan:

```text
gypport/platform_os/studio/journey/
```

No crear todavía `journey/authentication/`.

No implementar autenticación.

---

# 3. COMANDOS INICIALES

Ejecutar:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

Proteger cambios preexistentes.

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
gypport/platform_os/studio/channel/browser/shell/vite.alias.js
gypport/platform_os/studio/channel/browser/shell/vitest.config.js
```

Verificar cómo Vitest consume los aliases de Vite.

No inventar una segunda configuración si `vitest.config.js` ya reutiliza `vite.alias.js`.

---

# 5. ARCHIVOS AUTORIZADOS

Modificar solamente:

```text
gypport/platform_os/studio/channel/browser/shell/vite.alias.js
```

Modificar también:

```text
gypport/platform_os/studio/channel/browser/shell/vitest.config.js
```

únicamente si la inspección demuestra que no reutiliza el alias compartido.

No modificar ningún otro archivo.

---

# 6. CAMBIO REQUERIDO

Agregar:

```javascript
"@journey": path.resolve(rootDir, "../../../journey"),
```

siguiendo el estilo y orden existentes del archivo.

No crear:

```text
@authentication
@auth
@journeys
```

No cambiar aliases existentes.

---

# 7. VALIDACIÓN DE RESOLUCIÓN

Crear temporalmente solo mediante comando, sin dejar archivo persistente, una comprobación de resolución del path:

```text
gypport/platform_os/studio/journey
```

Si el directorio aún no existe, confirmar que el alias apunta exactamente al path canónico esperado.

No crear `journey/` en este STEP.

---

# 8. VALIDACIÓN

Ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

Esperado:

```text
15 archivos
133 pruebas
PASS
Build PASS
```

No debe aparecer regresión de aliases existentes.

---

# 9. PROHIBICIONES

No crear:

```text
journey/
AuthenticationRequest.js
contratos AUTH
authService
Login
Router
JWT
```

No tocar:

```text
engine/**
module/**
app/**
server/**
developer_platform/toolchain/**
```

No modificar `package.json`.

---

# 10. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos inspeccionados.
5. Archivo modificado.
6. Diff exacto.
7. Confirmación de ruta resuelta.
8. Confirmación de integración Vite/Vitest.
9. Resultado de contracts.
10. Resultado de build.
11. `git --no-pager diff --stat`.
12. `git status --short` final.
13. Confirmación de que no se creó `journey/`.
14. Confirmación de que nada fue staged, committed o pushed.

---

# 11. DETENERSE

Detenerse después de validar.

No reintentar AUTH-02 dentro de este STEP.

Finalizar con:

```text
git status --short
```

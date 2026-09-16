# CODEX-AUTH-02

## GYPPORT® PLATFORM OS

**Track:** Authentication Journey  
**Step:** AUTH-02 — Contrato y definición mínima de AuthenticationRequest  
**Mode:** Contract First + Minimum Definition  
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
```

Declarar:

```text
Track activo: Authentication Journey
Boundary autorizado: AuthenticationRequest neutral
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. DECISIÓN CERRADA

El primer contrato de autenticación será neutral y tendrá exactamente:

```javascript
{
  identifier,
  password
}
```

No incluir:

```text
email
username
tenant
workspace
token
refreshToken
rememberMe
device
metadata
```

`identifier` es una identidad adaptable. Su interpretación futura pertenece al backend.

---

# 3. OBJETIVO

Crear la definición mínima y su contrato ejecutable.

No implementar:

```text
fetch
login
logout
JWT
sesión
localStorage
React
Router
backend
```

---

# 4. COMANDOS INICIALES

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

# 5. ARCHIVOS AUTORIZADOS

Crear solamente:

```text
gypport/platform_os/studio/journey/authentication/definition/AuthenticationRequest.js
gypport/platform_os/studio/journey/authentication/definition/index.js
gypport/platform_os/studio/journey/authentication/index.js
gypport/platform_os/studio/contracts/journey/authentication/AuthenticationRequest.contract.mjs
```

No modificar ningún otro archivo.

---

# 6. API OBLIGATORIA

En `AuthenticationRequest.js` implementar:

```javascript
export function createAuthenticationRequest(input = {})
```

Debe retornar un objeto con exactamente:

```javascript
{
  identifier,
  password
}
```

Reglas:

```text
identifier:
- string
- trim en extremos
- default ""

password:
- string
- no trim
- default ""
```

No validar credenciales.

No inferir tipo de identificador.

No lanzar errores.

No mutar `input`.

No incluir campos extra.

---

# 7. BARRELS

`definition/index.js` debe exportar:

```javascript
export * from "./AuthenticationRequest";
```

`authentication/index.js` debe exportar:

```javascript
export * from "./definition";
```

No crear barrel global de `journey/` en este STEP.

---

# 8. CONTRATO OBLIGATORIO

Crear:

```text
gypport/platform_os/studio/contracts/journey/authentication/AuthenticationRequest.contract.mjs
```

Debe probar como mínimo:

1. Crea request con `identifier` y `password`.
2. Hace trim solo de `identifier`.
3. No hace trim de `password`.
4. Usa `""` como default de ambos.
5. Convierte valores no string a `""`.
6. Ignora campos extra.
7. Retorna exactamente dos keys.
8. No muta el input.
9. Cada llamada retorna un objeto nuevo.
10. Permanece neutral respecto de React, DOM, fetch, storage y tokens.

---

# 9. IMPORT DEL CONTRATO

Usar ruta interna explícita:

```javascript
import {
  createAuthenticationRequest
} from "@journey/authentication";
```

Si `@journey` no existe actualmente, detenerse.

No modificar aliases en este STEP.

Reportar el blocker exacto.

---

# 10. VALIDACIÓN

Antes de crear archivos:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
```

Línea base esperada:

```text
15 archivos
133 pruebas
PASS
```

Después de crear los cuatro archivos, ejecutar nuevamente.

Resultado esperado:

```text
16 archivos
143 pruebas
PASS
exit code 0
```

Si el conteo real difiere, reportarlo.

También ejecutar:

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

El build debe permanecer verde.

---

# 11. PROHIBICIONES

No modificar:

```text
LoginPage.jsx
ShortRegisterView.jsx
App.jsx
main.jsx
package.json
vite.alias.js
SecurityConfig
AuthController
backend
Runtime Session
```

No crear:

```text
AuthenticationService
AuthenticationSession
authService
Router
Guard
JWT
mocks
```

No tocar Dashboard Engine, Kernel, Module ni Toolchain.

---

# 12. REPORTE FINAL

Entregar:

1. Root y branch.
2. `git status --short` inicial.
3. Cumplimiento arquitectónico.
4. Archivos creados.
5. Contenido completo de `AuthenticationRequest.js`.
6. Contenido de ambos barrels.
7. Contenido completo del contrato.
8. Casos cubiertos.
9. Confirmación de neutralidad.
10. Resultado de línea base.
11. Resultado final de contracts.
12. Exit code y conteos.
13. Resultado de build.
14. `git --no-pager diff --stat`.
15. `git status --short` final.
16. Confirmación de que no se modificó UI ni backend.
17. Confirmación de que Toolchain no fue tocado.
18. Confirmación de que nada fue staged, committed o pushed.

---

# 13. CONDICIONES DE DETENCIÓN

Detenerse si:

```text
@journey no existe
se requiere modificar aliases
se requiere modificar más de los cuatro archivos autorizados
algún contrato anterior deja de pasar
aparece necesidad de inventar response o token
```

No improvisar.

---

# 14. DETENERSE

Detenerse después de contrato y build.

No implementar login.

Finalizar con:

```text
git status --short
```

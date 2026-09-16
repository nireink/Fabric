# CODEX-AUTH-03

## GYPPORT® PLATFORM OS

**Track:** Authentication Journey  
**Step:** AUTH-03 — Contrato neutral de AuthenticationResponse  
**Mode:** Contract First  
**Agent:** Codex

---

# 1. Objetivo

Definir el contrato neutral de respuesta de autenticación.

No implementar:

- Backend
- Login
- JWT
- Cookies
- Fetch
- Session Runtime
- React
- LocalStorage

---

# 2. Archivos autorizados

Crear únicamente:

```text
gypport/platform_os/studio/journey/authentication/definition/AuthenticationResponse.js
gypport/platform_os/studio/journey/authentication/definition/index.js   (actualizar barrel)
gypport/platform_os/studio/contracts/journey/authentication/AuthenticationResponse.contract.mjs
```

No modificar ningún otro archivo.

---

# 3. API requerida

Implementar:

```javascript
export function createAuthenticationResponse(input = {})
```

Debe retornar exactamente:

```javascript
{
  authenticated,
  session,
  actor,
  tenant,
  workspace,
  permissions,
  metadata
}
```

Reglas:

- `authenticated`: boolean (`false` por defecto).
- `session`, `actor`, `tenant`, `workspace`: objeto o `null`.
- `permissions`: arreglo (`[]` por defecto).
- `metadata`: objeto (`{}` por defecto).
- No inferir valores.
- No mutar `input`.
- Ignorar campos adicionales.

---

# 4. Contrato

Crear pruebas para verificar al menos:

1. Forma exacta del objeto.
2. Valores por defecto.
3. Conservación de referencias de objetos válidos.
4. `permissions` siempre arreglo.
5. `metadata` siempre objeto.
6. Ignora campos extra.
7. No muta input.
8. Devuelve un objeto nuevo.
9. Neutral respecto a React/DOM/fetch/storage/JWT.
10. Solo contiene las siete propiedades definidas.

---

# 5. Validación

Ejecutar:

```text
npm --prefix platform_os/studio/channel/browser/shell run contracts
npm --prefix platform_os/studio/channel/browser/shell run build
```

Esperado:

- Contracts PASS
- Build PASS

---

# 6. Prohibiciones

No crear:

- AuthenticationService
- Login
- Logout
- Refresh
- JWT
- Session Runtime
- Backend

Detenerse después de validar y reportar resultados.

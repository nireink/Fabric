# CODEX-AUTH-01

## GYPPORT® PLATFORM OS

**Track:** Authentication Journey  
**Step:** AUTH-01 — Reconnaissance de autenticación y frontera Journey / Browser UI  
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
Track activo: Authentication Journey
Boundary autorizado: reconnaissance de autenticación
Cambio arquitectónico: NO
Decisión: PASS / STOP
```

Si no es `PASS`, detenerse.

---

# 2. DECISIÓN ARQUITECTÓNICA CERRADA

```text
platform_os/studio/journey/authentication/
- definición del flujo
- contratos
- servicios
- sesión
- reglas
- sin React ni DOM

platform_os/studio/channel/browser/shell/src/app/authentication/
- LoginPage
- formularios React
- adaptación al Browser Shell
```

Regla:

```text
Journey no contiene JSX.
Browser Shell no contiene lógica de dominio de autenticación.
```

Modelo de credencial objetivo:

```text
identifier
password
```

`identifier` podrá representar correo, usuario, cédula, RUC, teléfono u otro identificador admitido.

Este STEP no implementa esa política.

---

# 3. OBJETIVO

Determinar el estado real de autenticación en frontend y backend antes de crear código.

Responder:

1. Qué endpoints existen.
2. Qué modelos request/response existen.
3. Qué seguridad está implementada.
4. Qué UI migrada existe.
5. Qué servicios frontend faltan.
6. Qué owner debe tener cada responsabilidad.
7. Cuál debe ser el primer contrato ejecutable.

No modificar archivos.

---

# 4. COMANDOS INICIALES

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

No ejecutar `git add`, `commit`, `push`, `restore`, `clean`, `reset` ni `stash`.

---

# 5. INSPECCIÓN BACKEND

Inspeccionar bajo:

```text
gypport/platform_os/server/src/main/java/
```

Buscar y leer archivos relacionados con:

```text
AuthController
SecurityConfig
login
logout
refresh
register-short
JWT
token
session
password
UserAccount
Tenant
Authentication
Authorization
```

Inspeccionar DTOs, services, repositories y filters relacionados.

No asumir endpoints.

---

# 6. INSPECCIÓN FRONTEND

Leer:

```text
gypport/platform_os/studio/channel/browser/shell/src/app/authentication/LoginPage.jsx
gypport/platform_os/studio/channel/browser/shell/src/app/onboarding/ShortRegisterView.jsx
gypport/platform_os/studio/channel/browser/shell/src/App.jsx
gypport/platform_os/studio/channel/browser/shell/src/main.jsx
gypport/platform_os/studio/channel/browser/shell/package.json
```

Buscar en `platform_os/studio/`, excluyendo `node_modules`:

```text
authService
AuthenticationService
login(
logout(
refresh(
registerShort(
token
jwt
session
localStorage
sessionStorage
Authorization
Bearer
react-router-dom
```

---

# 7. INSPECCIÓN DE OWNERS

Verificar si existen owners de:

```text
Authentication Journey
Authentication Service
Authentication Session
Tenant Selection
Workspace Selection
Route Guard
```

Inspeccionar:

```text
gypport/platform_os/studio/journey/
gypport/platform_os/studio/app/business-studio/
gypport/platform_os/studio/engine/core/runtime/
gypport/platform_os/studio/engine/framework/
```

---

# 8. PREGUNTAS OBLIGATORIAS

1. ¿Existe `POST /auth/login`?
2. ¿Existe `POST /auth/register-short`?
3. ¿Existe logout?
4. ¿Existe refresh token?
5. ¿Existe JWT u otro token?
6. ¿Cómo se almacenan contraseñas?
7. ¿Existe selección de Tenant?
8. ¿Existe selección de Workspace posterior al login?
9. ¿Existe sesión frontend?
10. ¿Existe router configurado?
11. ¿LoginPage está conectado al backend?
12. ¿ShortRegisterView está conectado al backend?
13. ¿Qué imports están rotos?
14. ¿Qué puede contratarse hoy sin inventar backend?
15. ¿Qué pertenece a Journey?
16. ¿Qué permanece en Browser Shell?
17. ¿Qué requiere primero trabajo backend?
18. ¿Cuál es el primer STEP seguro de implementación?

---

# 9. CLASIFICACIÓN

Clasificar:

```text
EXISTE Y FUNCIONA
EXISTE PARCIALMENTE
NO EXISTE
LEGACY / DESCONECTADA
REQUIERE DECISIÓN
BLOQUEADA POR BACKEND
```

Incluir:

```text
Login
Register Short
Logout
Refresh
JWT
Session
Tenant Selection
Workspace Selection
Route Guard
Password Recovery
MFA
```

---

# 10. OPCIONES

Evaluar:

```text
A. Comenzar por register-short porque el backend ya existe.
B. Crear contrato Journey neutral para login aunque backend login no exista.
C. Implementar primero backend login.
D. Conectar LoginPage con mocks temporales.
```

Rechazar D.

Comparar riesgo, dependencias, valor, Foundation y superficie.

---

# 11. VALIDACIÓN PASIVA

```text
npm --prefix gypport/platform_os/studio/channel/browser/shell run contracts
npm --prefix gypport/platform_os/studio/channel/browser/shell run build
```

---

# 12. PROHIBICIONES

No modificar ni crear archivos.

No crear Journey, authService, router, mocks, JWT ni endpoints.

No cambiar SecurityConfig ni conectar pantallas.

No tocar Dashboard Engine, Kernel, Toolchain ni Module.

---

# 13. REPORTE FINAL

Entregar:

1. Root y branch.
2. Git inicial.
3. Cumplimiento.
4. Archivos backend inspeccionados.
5. Archivos frontend inspeccionados.
6. Endpoints reales.
7. Modelos request/response.
8. Estado de seguridad.
9. Estado de LoginPage.
10. Estado de ShortRegisterView.
11. Tabla de capacidades.
12. Owners actuales y correctos.
13. Blockers.
14. Comparación A-D.
15. Recomendación.
16. Superficie exacta de AUTH-02.
17. Contracts.
18. Build.
19. Git final.
20. Confirmación de no modificación.

---

# 14. DETENERSE

Detenerse después del reporte.

Finalizar con:

```text
git status --short
```

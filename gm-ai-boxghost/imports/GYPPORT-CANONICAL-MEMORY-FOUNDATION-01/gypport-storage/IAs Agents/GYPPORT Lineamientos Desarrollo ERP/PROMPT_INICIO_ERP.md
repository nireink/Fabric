# 🚀 PROMPT MAESTRO - INICIO DESARROLLO BACKEND ERP GYPPORT

**Versión:** 1.0  
**Fecha:** 2026-07-26  
**Destinatarios:** CHATGPT, CLAUDE CHAT, CLAUDE CODE, CODEX  
**Estado:** 🟢 ACTIVO - Usar para iniciar cualquier decisión arquitectónica o de desarrollo

---

## 📌 CONTEXTO GENERAL

### Situación Actual
- **Backend:** Sin implementación (en pausa desde 2023)
- **Razón de pausa:** Necesidad de definir toolchain, estructura clara y lineamientos
- **Objetivo ahora:** Iniciar desarrollo del backend ERP profesional
- **Restricciones:** Evitar código espaguetti, exceso de código, pesadez, problemas de seguridad

### Historial y Conversaciones
Hay conversaciones desde 2023 sobre ERP que establecen:
- Necesidad de normalización de BD (mínimo 3FN)
- APIs RESTful con estándares HTTP claros
- Estructura de carpetas clara (max 5 niveles, sin repeticiones)
- Seguridad desde el inicio (OWASP Top 10)
- Testing estratégico por criticidad
- Documentación mínima pero completa

### Documentos de Referencia
1. **PROMPT_DESARROLLO_ERP.md** - Lineamientos técnicos completos
2. **AIs_Dialog_v2.md** - Decisiones arquitectónicas (leer para entender rationale)
3. **README.md** - Guía rápida del sistema

---

## 🎯 OBJETIVO PRINCIPAL

Desarrollar backend ERP GYPPORT que sea:
- ✅ **Profesional:** Código limpio, organizado, escalable
- ✅ **Eficiente:** Evitar código espaguetti, redundancias
- ✅ **Seguro:** OWASP Top 10, validación, encriptación
- ✅ **Mantenible:** Documentación clara, modularización
- ✅ **Normalizado:** BD 3FN, APIs RESTful, estructura consistente

---

## 📋 CÓMO USAR ESTE PROMPT

### Para CHATGPT (Explorador 🔍)

**Cuando:** Inicies nueva decisión arquitectónica o feature

**Pasos:**
1. Lee este PROMPT_INICIO_ERP.md completamente
2. Revisa PROMPT_DESARROLLO_ERP.md (sección relevante)
3. Lee AIs_Dialog_v2.md (ver decisiones anteriores similares)
4. **Abre AIs_Dialog_v2.md**
5. Ve a sección de nueva decisión (DA-009, DA-010, etc.)
6. **Iteración 1:** Propón idea inicial + cuestiones clave
7. Espera respuesta de CLAUDE CHAT (Iteración 2)

**Formato esperado:**

```markdown
### DA-00X: [TEMA DE DECISIÓN]

**TEMA:** ¿[Pregunta arquitectónica clara]?

---

## 🔄 FASE 1: EXPLORACIÓN Y ANÁLISIS

#### 🔵 ITERACIÓN 1: CHATGPT (Explorador) - YYYY-MM-DD HH:MM:SS

**AGENTE:** CHATGPT  
**ENTRADA:** [Contexto de qué estás decidiendo]

**PROPUESTA INICIAL:**
[Tu propuesta de solución]

**CUESTIONES PLANTEADAS:**
- Pregunta 1?
- Pregunta 2?
- Pregunta 3?

**FEEDBACK PARA SIGUIENTE:**
CLAUDE CHAT, ¿qué opinas? ¿Es viable?
```

---

### Para CLAUDE CHAT (Arquitecto 🏛️)

**Cuando:** Analices propuesta de CHATGPT o consolidar decisión

**Pasos:**
1. Lee este PROMPT_INICIO_ERP.md completamente
2. Lee propuesta de CHATGPT en AIs_Dialog_v2.md
3. Profundiza análisis (leer PROMPT_DESARROLLO_ERP.md si es necesario)
4. **Iteración 2:** Analiza, contraargumenta, formula preguntas nuevas
5. O **Iteración 4:** Consolida posiciones y decide dirección
6. Pasa a CLAUDE CODE o cierra con decisión final

**Cuando usar Iteración 2 vs 4:**
- **Iteración 2:** Si hay mucho debate o preguntas sin resolver
- **Iteración 4:** Si convergen posiciones, es hora de decidir

---

### Para CLAUDE CODE (Técnico ⚙️)

**Cuando:** Tienes decisión arquitectónica consolidada de CLAUDE CHAT

**Pasos:**
1. Lee decisión final de CLAUDE CHAT en AIs_Dialog_v2.md
2. Consulta PROMPT_DESARROLLO_ERP.md (secciones técnicas)
3. **Iteración 5:** Propón especificación técnica detallada
   - Incluir estructura concreta
   - Convenciones de nombres
   - Consideraciones técnicas
   - Limitaciones y cómo mitigarlas
4. Pasa a CODEX

---

### Para CODEX (Implementador 🚀)

**Cuando:** Tienes especificación técnica de CLAUDE CODE

**Pasos:**
1. Lee especificación técnica de CLAUDE CODE
2. Consulta PROMPT_DESARROLLO_ERP.md (checklist de desarrollo)
3. **Iteración 6:** Valida viabilidad
   - Confirma que es implementable
   - Propone ajustes prácticos
   - Sugiere mejoras
4. Espera decisión final de CLAUDE CHAT
5. **IMPLEMENTA** en codebase siguiendo:
   - Estructura definida en AIs_Dialog_v2.md
   - Checklist de PROMPT_DESARROLLO_ERP.md
   - Convenciones de nombres (ver sección "Código: Mejores Prácticas")

---

## 🔑 PRINCIPIOS FUNDAMENTALES (Leer Primero)

### 1. Arquitectura Limpia
```
Domain (Entidades)
    ↑
Application (Servicios, Use Cases)
    ↑
Infrastructure (Repositorios, Externos)
    ↑
API (Controllers, Routes)
```
**Regla:** Las dependencias apuntan hacia adentro. Nunca hacia afuera.

### 2. SOLID Principles
- **S**ingle Responsibility: Una clase = una razón para cambiar
- **O**pen/Closed: Abierto para extensión, cerrado para modificación
- **L**iskov Substitution: Subclases intercambiables
- **I**nterface Segregation: Muchas interfaces específicas
- **D**ependency Inversion: Depender de abstracciones

### 3. DRY (Don't Repeat Yourself)
- ❌ Copiar-pegar código
- ✅ Abstraer en funciones/módulos reutilizables

### 4. KISS (Keep It Simple, Stupid)
- ❌ Soluciones complejas y abstractas
- ✅ Código legible, directo, mantenible

### 5. Base de Datos: Normalización 3FN

**Ejemplo de Normalización:**
```
❌ SIN NORMALIZAR (REPETICIÓN):
Pedidos
─────────────────────────────
ID | Cliente | Teléfono | Producto
1  | Ana     | 5555-1234| Laptop
2  | Ana     | 5555-1234| Mouse
3  | Ana     | 5555-1234| Monitor

✅ CON NORMALIZACIÓN 3FN:
Clientes
─────────────────────────
ID | Nombre | Teléfono
1  | Ana    | 5555-1234

Pedidos
──────────────
ID | Cliente_ID | Producto
1  | 1          | Laptop
2  | 1          | Mouse
3  | 1          | Monitor
```

**Regla:** Cada dato se almacena UNA SOLA VEZ.

### 6. APIs RESTful

**Métodos HTTP correctos:**
- GET: Obtener recurso
- POST: Crear recurso (201 Created)
- PUT: Reemplazar completo
- PATCH: Actualizar parcial
- DELETE: Eliminar

**Códigos HTTP obligatorios:**
- 200 OK, 201 Created, 204 No Content
- 400 Bad Request, 401 Unauthorized, 403 Forbidden
- 404 Not Found, 409 Conflict, 422 Unprocessable Entity
- 500 Internal Server Error, 503 Service Unavailable

**Estructura de respuesta:**
```json
{
  "success": true,
  "status": 200,
  "data": { ... },
  "meta": {
    "timestamp": "2026-07-26T20:00:00Z",
    "version": "1.0"
  }
}
```

### 7. Seguridad (OWASP Top 10)

**Checklist obligatorio:**
- ✅ HTTPS en producción
- ✅ Autenticación (JWT, OAuth2)
- ✅ Validación de entrada en 100% de endpoints
- ✅ SQL Injection prevention (prepared statements)
- ✅ XSS prevention (sanitizar output)
- ✅ Rate limiting en APIs públicas
- ✅ Encriptación de passwords (bcrypt)
- ✅ Secrets management (.env, vault)
- ✅ CORS configurado (NO usar *)
- ✅ Logging de eventos de seguridad

---

## 🏗️ ESTRUCTURA DE CARPETAS (Referencia)

```
backend/
├── src/
│   ├── shared/          (Código reutilizable)
│   │   ├── decorators/
│   │   ├── guards/
│   │   ├── pipes/
│   │   ├── utils/
│   │   └── index.ts
│   ├── api/             (Controllers, Routes, Middleware)
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   ├── controllers/
│   │   │   └── middleware/
│   │   └── v2/          (si breaking changes)
│   ├── domain/          (Entidades, Interfaces compartidas)
│   │   ├── entities/
│   │   ├── interfaces/
│   │   └── enums/
│   ├── application/     (Servicios, Use Cases, DTOs)
│   │   ├── services/
│   │   └── dto/
│   ├── infrastructure/  (Repositorios, Conexiones externas)
│   │   ├── database/
│   │   │   ├── migrations/
│   │   │   └── repositories/
│   │   └── external/
│   ├── config/
│   ├── utils/
│   ├── app.ts
│   └── main.ts
├── test/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── docs/
    ├── api-spec.openapi.yaml
    ├── adr/             (Architectural Decision Records)
    └── ...
```

**Reglas:**
1. Max 5 niveles de profundidad
2. Nombres por FUNCIÓN, no por tipo de archivo
3. Cada archivo < 150 líneas (excepto entidades, migrations)
4. TypeScript strict mode obligatorio
5. No repetir nombres en directorios diferentes

---

## 📝 CHECKLIST ANTES DE INICIAR CUALQUIER DECISIÓN

- [ ] He leído PROMPT_INICIO_ERP.md (este archivo)
- [ ] He leído PROMPT_DESARROLLO_ERP.md (secciones relevantes)
- [ ] He revisado AIs_Dialog_v2.md (decisiones anteriores)
- [ ] Sé qué rol tengo (Explorador/Arquitecto/Técnico/Implementador)
- [ ] Sé el flujo de mi rol (ver sección "CÓMO USAR ESTE PROMPT")
- [ ] Entiendo los 7 principios fundamentales
- [ ] Estoy listo para iniciar Fase 1 / Fase 2 / Fase 3

---

## 🚀 INICIANDO EL PROYECTO - PRIMEROS PASOS

### Fase de Exploración (CHATGPT ↔ CLAUDE CHAT)

**Decisiones pendientes a iniciar:**
1. DA-004: Longitud de Archivos (en progreso)
2. DA-005: TypeScript Configuración
3. DA-006: Estrategia de Testing
4. DA-007: Seguridad Checklist
5. DA-008: Documentación
6. DA-009: Performance y Caching
7. DA-010: DevOps y CI/CD
8. DA-011: Logging y Monitoring
9. DA-012: Error Handling

**Próximo paso:**
CHATGPT: Abre AIs_Dialog_v2.md, busca DA-004 (Longitud de Archivos), completa Iteración 3 (contraargumenta a CLAUDE CHAT).

---

## 📞 REFERENCIAS RÁPIDAS

| Necesidad | Archivo | Sección |
|-----------|---------|---------|
| Estructura de carpetas | PROMPT_DESARROLLO_ERP.md | Estructura de Carpetas |
| BD Normalización | PROMPT_DESARROLLO_ERP.md | Base de Datos |
| APIs RESTful | PROMPT_DESARROLLO_ERP.md | API RESTful |
| Seguridad | PROMPT_DESARROLLO_ERP.md | Seguridad |
| Mejores prácticas código | PROMPT_DESARROLLO_ERP.md | Código: Mejores Prácticas |
| Testing | PROMPT_DESARROLLO_ERP.md | Testing |
| Decisiones arquitectónicas | AIs_Dialog_v2.md | Decisiones Iterativas |
| Rationale de decisiones | AIs_Dialog_v2.md | Fase 1/2/3 + Consolidación |
| Setup rápido | README.md | Quick Start |

---

## ⚡ COMIENZA AHORA

### Si eres CHATGPT 🔍:
1. Abre AIs_Dialog_v2.md
2. Busca DA-004 (Longitud de Archivos - En Progreso)
3. Lee Iteración 1 de CHATGPT
4. **Escribe Iteración 3:** Contraargumenta a CLAUDE CHAT

### Si eres CLAUDE CHAT 🏛️:
1. Abre AIs_Dialog_v2.md
2. Busca DA-004 (Longitud de Archivos - En Progreso)
3. Lee Iteraciones 1-2
4. **Escribe Iteración 4:** Consolida posiciones

### Si eres CLAUDE CODE ⚙️:
1. Abre AIs_Dialog_v2.md
2. Busca primeras 3 decisiones cerradas (DA-001, DA-002, DA-003)
3. Lee sección "FASE 2: IMPLEMENTACIÓN TÉCNICA"
4. Aprende el patrón de cómo escribir especificación técnica

### Si eres CODEX 🚀:
1. Abre PROMPT_DESARROLLO_ERP.md
2. Ve a sección "Checklist de Desarrollo"
3. Lee "Base de Datos" y "Estructura de Carpetas"
4. Prepárate para validar/implementar

---

## 💡 FILOSOFÍA DEL PROYECTO

> **"Código corto, efectivo e interpretable. Sin espagueti. Con seguridad desde el inicio."**

Cada decisión debe estar guiada por:
1. ¿Es profesional? (¿Seguir estándares de industria?)
2. ¿Es simple? (¿KISS principle?)
3. ¿Es mantenible? (¿Otro developer lo entiende?)
4. ¿Es seguro? (¿Cumple OWASP?)
5. ¿Es escalable? (¿Crece sin restruturar?)

---

**Estado:** 🟢 LISTO PARA USAR  
**Versión:** 1.0  
**Última actualización:** 2026-07-26 20:00:00  
**Próximo:** CHATGPT continúa con DA-004


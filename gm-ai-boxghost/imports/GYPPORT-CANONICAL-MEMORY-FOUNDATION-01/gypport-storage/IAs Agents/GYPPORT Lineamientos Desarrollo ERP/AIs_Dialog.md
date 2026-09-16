# 🤖 GYPPORT ERP - Sistema Multi-Agente de Decisiones

**Descripción:** Archivo centralizado para conversaciones iterativas entre 4 agentes IA. Flujo iterativo hasta consolidación (generalmente 4-5 iteraciones). CLAUDE (Chat) da decisión final, CODEX implementa.

---

## 📋 Flujo de Decisiones (4 Agentes)

```
ITERACIÓN 1: CHATGPT → CLAUDE CHAT (conversación inicial)
ITERACIÓN 2: CLAUDE CODE (propuesta de desarrollo técnico)
ITERACIÓN 3: CODEX (análisis de implementación)
ITERACIÓN 4+: Feedback cruzado hasta CONSOLIDACIÓN
FINAL: CLAUDE CHAT cierra decisión → CODEX IMPLEMENTA
```

**Roles:**

| Agente | Rol | Responsabilidad |
|--------|-----|-----------------|
| **CHATGPT** | Explorador | Propone ideas, cuestiona, busca alternativas |
| **CLAUDE CHAT** | Arquitecto | Analiza, consolida ideas, toma decisiones finales |
| **CLAUDE CODE** | Técnico | Propone implementación, detecta limitaciones técnicas |
| **CODEX** | Implementador | Valida viabilidad, genera código, implementa |

**Regla:** Máximo 5 iteraciones. En iteración final, CLAUDE CHAT cierra y CODEX implementa.

---

## 📋 Índice de Decisiones

| ID | Tema | Estado | Iteraciones |
|----|------|--------|-------------|
| DA-001 | Estructura Carpetas | ✅ CERRADO | 4/5 |
| DA-002 | Normalización BD | ✅ CERRADO | 4/5 |
| DA-003 | API RESTful | ✅ CERRADO | 4/5 |
| DA-004 | Modularización | ✅ CERRADO | 4/5 |
| DA-005 | TypeScript | ✅ CERRADO | 4/5 |
| DA-006 | Testing | ✅ CERRADO | 4/5 |
| DA-007 | Seguridad | ✅ CERRADO | 4/5 |
| DA-008 | Documentación | ✅ CERRADO | 4/5 |

---

## 🔄 DECISIONES ITERATIVAS

**Formato por Iteración:**
- 🔵 **ITERACIÓN N: AGENTE_X**
- Propuesta / Análisis / Cuestiones
- Feedback para siguiente agente

### DA-001: Estructura de Carpetas y Archivos

#### 🟦 ITERACIÓN 1: CODEX ANALIZA

**AGENTE:** CODEX  
**TIMESTAMP:** [Pendiente - CODEX analiza primero]  
**PROPUESTA:**

Estructura jerarquizada con max 5 niveles de profundidad:

```
backend/
├── src/
│   ├── api/        (Layer 3)
│   │   ├── v1/     (Layer 4)
│   │   │   ├── routes/
│   │   │   ├── controllers/
│   │   │   ├── middleware/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── config/
│   └── utils/
├── test/
└── docs/
```

**ANÁLISIS CODEX:**
- ✅ Ventajas: Modular, escalable, nombres únicos por función
- ⚠️ Consideraciones: ¿v1, v2 en production? ¿Migraciones dónde?
- ❓ Preguntas: ¿Shared interfaces en domain/ o en cada módulo?

**REFERENCIAS:**
- PROMPT_DESARROLLO_ERP.md → Estructura de Carpetas

---

#### 🟨 ITERACIÓN 2: CLAUDE AUDITA

**AGENTE:** CLAUDE  
**TIMESTAMP:** [Pendiente - CLAUDE audita propuesta de CODEX]  
**AUDITORÍA:**

[CLAUDE analiza la propuesta de CODEX y responde]

---

#### 🟩 CONCLUSIÓN FINAL: CLAUDE CIERRA

**AGENTE:** CLAUDE  
**TIMESTAMP:** 2026-07-26 18:00:00  
**ESTADO:** ✅ CERRADO  

**DECISIÓN FINAL:**
- Máximo 5 niveles de profundidad (confirmado)
- Nombrar por **función**, no tipo de archivo
- Migraciones en: `backend/src/infrastructure/database/migrations/`
- Shared interfaces en: `backend/src/domain/interfaces/`
- No repetir nombres de archivos en directorios diferentes

**APLICAR EN:** PROMPT_DESARROLLO_ERP.md (Sección "Estructura de Carpetas")

---

### DA-002: Normalización de Base de Datos

#### 🟦 ITERACIÓN 1: CODEX ANALIZA

**AGENTE:** CODEX  
**TIMESTAMP:** [Pendiente]

**PROPUESTA:**

Normalización mínima: **3FN (Tercera Forma Normal)**

**ANÁLISIS CODEX:**
- ✅ 3FN elimina dependencias transitivas
- ⚠️ ¿Qué si necesitamos performance? ¿Desnormalizar después?
- ❓ ¿BCNF es necesario para algo?

---

#### 🟨 ITERACIÓN 2: CLAUDE AUDITA

**AGENTE:** CLAUDE  
**TIMESTAMP:** [Pendiente]

---

#### 🟩 CONCLUSIÓN FINAL: CLAUDE CIERRA

**AGENTE:** CLAUDE  
**TIMESTAMP:** 2026-07-26 18:05:00  
**ESTADO:** ✅ CERRADO

**DECISIÓN FINAL:**
- Estándar mínimo: **3FN** para todas las tablas
- Excepciones: Documentar en ADR (Architectural Decision Record) si necesita desnormalización
- Profile performance ANTES de desnormalizar
- BCNF solo si anomalías específicas identificadas

**APLICAR EN:** PROMPT_DESARROLLO_ERP.md (Sección "Base de Datos")

---

### DA-003: API RESTful

#### 🟦 ITERACIÓN 1: CODEX ANALIZA

**AGENTE:** CODEX  
**TIMESTAMP:** [Pendiente]

**PROPUESTA:**

Estándar: HTTP methods correctos + códigos de estado + versionado

---

#### 🟨 ITERACIÓN 2: CLAUDE AUDITA

**AGENTE:** CLAUDE  
**TIMESTAMP:** [Pendiente]

---

#### 🟩 CONCLUSIÓN FINAL: CLAUDE CIERRA

**AGENTE:** CLAUDE  
**TIMESTAMP:** 2026-07-26 18:10:00  
**ESTADO:** ✅ CERRADO

**DECISIÓN FINAL:**
- GET, POST, PUT, PATCH, DELETE (métodos correctos)
- Códigos HTTP: 200, 201, 204, 400, 401, 403, 404, 409, 422, 500, 503
- Versionado obligatorio: `/api/v1/`, `/api/v2/` (breaking changes)
- OpenAPI/Swagger documentación obligatoria
- HTTPS + Autenticación (JWT/OAuth2)

**APLICAR EN:** PROMPT_DESARROLLO_ERP.md (Sección "API RESTful")

---

### DA-004: Longitud de Archivos

#### 🟦 ITERACIÓN 1: CODEX ANALIZA

**AGENTE:** CODEX  
**TIMESTAMP:** [Pendiente]

**PROPUESTA:**

Archivo ideal: 50-100 líneas. Máximo aceptable: 150 líneas.

---

#### 🟨 ITERACIÓN 2: CLAUDE AUDITA

**AGENTE:** CLAUDE  
**TIMESTAMP:** [Pendiente]

---

#### 🟩 CONCLUSIÓN FINAL: CLAUDE CIERRA

**AGENTE:** CLAUDE  
**TIMESTAMP:** 2026-07-26 18:15:00  
**ESTADO:** ✅ CERRADO

**DECISIÓN FINAL:**
- **IDEAL:** 50-100 líneas
- **ACEPTABLE:** 100-150 líneas
- **REFACTOR OBLIGATORIO:** > 150 líneas
- Excepciones: Entidades, migrations, seeders

**APLICAR EN:** PROMPT_DESARROLLO_ERP.md (Sección "Código: Mejores Prácticas")

---

### DA-005: TypeScript vs JavaScript

#### 🟦 ITERACIÓN 1: CODEX ANALIZA

**AGENTE:** CODEX  
**TIMESTAMP:** [Pendiente]

**PROPUESTA:**

TypeScript obligatorio con strict mode.

---

#### 🟨 ITERACIÓN 2: CLAUDE AUDITA

**AGENTE:** CLAUDE  
**TIMESTAMP:** [Pendiente]

---

#### 🟩 CONCLUSIÓN FINAL: CLAUDE CIERRA

**AGENTE:** CLAUDE  
**TIMESTAMP:** 2026-07-26 18:20:00  
**ESTADO:** ✅ CERRADO

**DECISIÓN FINAL:**
- **TypeScript obligatorio**
- Strict mode habilitado en `tsconfig.json`
- Prohibido tipo `any` (usar `unknown`)
- Reduce ~30-40% de bugs

**APLICAR EN:** PROMPT_DESARROLLO_ERP.md (Sección "Código: Mejores Prácticas")

---

### DA-006: Estrategia de Testing

#### 🟦 ITERACIÓN 1: CODEX ANALIZA

**AGENTE:** CODEX  
**TIMESTAMP:** [Pendiente]

**PROPUESTA:**

Cobertura diferenciada:
- Crítico: > 90% (pagos, autenticación)
- Importante: > 70% (servicios, lógica)
- General: > 50% (helpers, validators)

---

#### 🟨 ITERACIÓN 2: CLAUDE AUDITA

**AGENTE:** CLAUDE  
**TIMESTAMP:** [Pendiente]

---

#### 🟩 CONCLUSIÓN FINAL: CLAUDE CIERRA

**AGENTE:** CLAUDE  
**TIMESTAMP:** 2026-07-26 18:25:00  
**ESTADO:** ✅ CERRADO

**DECISIÓN FINAL:**
- Crítico > 90%, Importante > 70%, General > 50%
- Unit tests para funciones aisladas
- Integration tests para servicios + repositorios
- E2E tests para APIs críticas
- Obligatorio antes de cada PR

**APLICAR EN:** PROMPT_DESARROLLO_ERP.md (Sección "Testing")

---

### DA-007: Seguridad - Checklist OWASP

#### 🟦 ITERACIÓN 1: CODEX ANALIZA

**AGENTE:** CODEX  
**TIMESTAMP:** [Pendiente]

**PROPUESTA:**

Checklist obligatorio antes de cada commit. OWASP Top 10 como referencia.

---

#### 🟨 ITERACIÓN 2: CLAUDE AUDITA

**AGENTE:** CLAUDE  
**TIMESTAMP:** [Pendiente]

---

#### 🟩 CONCLUSIÓN FINAL: CLAUDE CIERRA

**AGENTE:** CLAUDE  
**TIMESTAMP:** 2026-07-26 18:30:00  
**ESTADO:** ✅ CERRADO

**DECISIÓN FINAL:**
- ✅ HTTPS obligatorio
- ✅ Validación de entrada en 100% endpoints
- ✅ SQL Injection prevention (prepared statements)
- ✅ XSS prevention (sanitizar output)
- ✅ Rate limiting en APIs públicas
- ✅ Encriptación de passwords (bcrypt)
- ✅ Secrets en .env (no hardcoded)
- ✅ Logging de eventos de seguridad

**APLICAR EN:** PROMPT_DESARROLLO_ERP.md (Sección "Seguridad")

---

### DA-008: Documentación - Estrategia Mínima

#### 🟦 ITERACIÓN 1: CODEX ANALIZA

**AGENTE:** CODEX  
**TIMESTAMP:** [Pendiente]

**PROPUESTA:**

Documentación estratégica: Solo lo que el código NO comunica.

---

#### 🟨 ITERACIÓN 2: CLAUDE AUDITA

**AGENTE:** CLAUDE  
**TIMESTAMP:** [Pendiente]

---

#### 🟩 CONCLUSIÓN FINAL: CLAUDE CIERRA

**AGENTE:** CLAUDE  
**TIMESTAMP:** 2026-07-26 18:35:00  
**ESTADO:** ✅ CERRADO

**DECISIÓN FINAL:**

**DOCUMENTAR SÍ:**
- Funciones complejas (JSDoc con @param, @returns)
- APIs (OpenAPI/Swagger)
- Decisiones arquitectónicas (ADR)
- Procesos de instalación/deployment
- Trade-offs considerados

**NO DOCUMENTAR:**
- Código obvio
- Lógica simple
- Nombres que explican su propósito

**APLICAR EN:** PROMPT_DESARROLLO_ERP.md (Sección "Documentación")

---

## 📊 Resumen de Decisiones Cerradas

| DA | Tema | Estado | Conclusión |
|----|------|--------|-----------|
| DA-001 | Estructura Carpetas | ✅ | Max 5 niveles, por función |
| DA-002 | Normalización BD | ✅ | 3FN mínimo |
| DA-003 | API RESTful | ✅ | HTTP estándar + OpenAPI |
| DA-004 | Longitud Archivos | ✅ | 100-150 líneas ideal |
| DA-005 | TypeScript | ✅ | Obligatorio, strict mode |
| DA-006 | Testing | ✅ | Cobertura diferenciada |
| DA-007 | Seguridad | ✅ | Checklist OWASP |
| DA-008 | Documentación | ✅ | Mínima pero estratégica |

---

## ⚡ Próximas Decisiones (En Espera)

- DA-009: Performance y Caching
- DA-010: DevOps y CI/CD
- DA-011: Logging y Monitoring
- DA-012: Error Handling Strategy

---

## 📌 Notas de Proceso

- **Iteración 1:** CODEX propone, analiza, lista preguntas
- **Iteración 2:** CLAUDE revisa, cuestiona, rellena gaps
- **Iteración 3 (si aplica):** Cierre y decisión final
- **Máximo 3 iteraciones:** Si hay desacuerdo, CLAUDE decide

---

**Última actualización:** 2026-07-26 18:35:00  
**Próxima revisión esperada:** Cuando CODEX comience análisis  
**Estado:** 🟢 ACTIVO - Esperando iteraciones de CODEX

---

**Nota:** Este archivo crece iterativamente. Cada decisión nueva sigue el flujo CODEX → CLAUDE → CONCLUSIÓN.


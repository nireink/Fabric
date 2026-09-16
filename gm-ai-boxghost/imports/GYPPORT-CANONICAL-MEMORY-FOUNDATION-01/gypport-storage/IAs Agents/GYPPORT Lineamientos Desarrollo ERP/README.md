# 📘 GYPPORT ERP - Lineamientos de Desarrollo

**Versión:** 1.0  
**Fecha:** 2026-07-26  
**Estado:** 🟢 ACTIVO (Esperando validación CODEX)  
**Destinatarios:** Developers, IAs, Tech Leads

---

## 📚 Índice Rápido

### 🎯 PARA INICIAR EL PROYECTO

1. **[PROMPT_INICIO_ERP.md](./PROMPT_INICIO_ERP.md)** ⭐ **LEER PRIMERO**
   - Prompt maestro para CHATGPT, CLAUDE CHAT, CLAUDE CODE, CODEX
   - Cómo usar este sistema
   - Principios fundamentales (7 core concepts)
   - Estructura de carpetas y checklist
   - Próximos pasos específicos por rol
   - **COMIENZA AQUÍ si eres nuevo**

### 📖 REFERENCIAS TÉCNICAS

2. **[PROMPT_DESARROLLO_ERP.md](./PROMPT_DESARROLLO_ERP.md)** - Lineamientos Técnicos
   - Mejores prácticas de código
   - Normalización de BD (3FN)
   - API RESTful (métodos, códigos, respuestas)
   - Seguridad (OWASP Top 10 checklist)
   - Testing (estrategia diferenciada)
   - Documentación
   - **Consulta por sección según necesidad**

3. **[AIs_Dialog_v2.md](./AIs_Dialog_v2.md)** - Decisiones Arquitectónicas
   - Flujo multi-agente: CHATGPT → CLAUDE CHAT → CLAUDE CODE → CODEX
   - Ejemplos completos (DA-001 con 6 iteraciones)
   - En progreso (DA-004)
   - Pendientes (DA-005 a DA-008)
   - **Ver rationale de decisiones anteriores**

---

## 🚀 Quick Start

### Paso 1: Leer PROMPT_INICIO_ERP.md (20 min) ⭐
**Qué te dice:**
- Contexto del proyecto ERP
- Por qué este sistema
- Los 7 principios fundamentales
- Cómo usar este sistema según tu rol
- Próximos pasos específicos

### Paso 2: Consultar por necesidad

**Si necesitas:**
- Estructura de carpetas → PROMPT_DESARROLLO_ERP.md Sección "Estructura"
- BD Normalización → PROMPT_DESARROLLO_ERP.md Sección "Base de Datos"
- APIs RESTful → PROMPT_DESARROLLO_ERP.md Sección "API RESTful"
- Seguridad → PROMPT_DESARROLLO_ERP.md Sección "Seguridad"
- Mejores prácticas código → PROMPT_DESARROLLO_ERP.md Sección "Código"

### Paso 3: Participar en decisiones

**Si eres:**
- **CHATGPT 🔍** → Lee PROMPT_INICIO_ERP.md Sección "Para CHATGPT"
- **CLAUDE CHAT 🏛️** → Lee PROMPT_INICIO_ERP.md Sección "Para CLAUDE CHAT"
- **CLAUDE CODE ⚙️** → Lee PROMPT_INICIO_ERP.md Sección "Para CLAUDE CODE"
- **CODEX 🚀** → Lee PROMPT_INICIO_ERP.md Sección "Para CODEX"

### Paso 4: Checklist antes de cada commit
```
PROMPT_DESARROLLO_ERP.md → Sección: Checklist de Desarrollo
```

---

## 📋 Decisiones Clave

| Decisión | Lineamiento | Referencia |
|----------|-----------|-----------|
| 🗄️ Normalización | **3FN mínimo** | Claude/Decisiones.md #4 |
| 📁 Carpetas | **Max 5 niveles, por función** | Claude/Decisiones.md #5 |
| 📄 Archivos | **100-150 líneas ideal** | Claude/Decisiones.md #6 |
| 🔤 Lenguaje | **TypeScript obligatorio** | Claude/Decisiones.md #7 |
| 🧪 Testing | **Cobertura diferenciada** | Claude/Decisiones.md #8 |
| 🔐 Seguridad | **Checklist OWASP** | Claude/Decisiones.md #9 |
| 📚 Documentación | **Mínima pero completa** | Claude/Decisiones.md #10 |

---

## 🎯 Objetivos del ERP

Este prompt fue diseñado para:

✅ **Evitar Código Espaguetti**
- Estructura clara y consistente
- SRP (Single Responsibility)
- Módulos pequeños

✅ **Reducir Bugs**
- TypeScript con tipos
- Testing prioritizado
- Validación de entrada

✅ **Acelerar Desarrollo**
- Lineamientos claros (no decisiones ad-hoc)
- Estructura escalable
- Documentación estratégica

✅ **Mejorar Seguridad**
- Checklist obligatorio
- Validación en 100% endpoints
- HTTPS + autenticación

✅ **Facilitar Mantenimiento**
- Código limpio y legible
- Documentación completa
- Decisiones arquitectónicas registradas

---

## 📞 Sistema de Diálogo entre Agentes

```
FLUJO:
1. CLAUDE establece lineamientos en:
   - PROMPT_DESARROLLO_ERP.md
   - Claude/Decisiones.md
   
2. CODEX valida y comenta en:
   - Codex/Respuestas.md
   - AIs_Dialog.md (decisiones finales)

3. EQUIPO recibe lineamientos validados
   - Implementan según PROMPT_DESARROLLO_ERP.md
   - Consultan decisiones en AIs_Dialog.md
   - Referencia técnica en Claude/Decisiones.md
```

**Estructura de carpetas:**
```
Lineamientos Desarrollo ERP/
├── README.md (estás aquí)
├── PROMPT_DESARROLLO_ERP.md ⭐ (guía principal)
├── AIs_Dialog.md (decisiones finales)
├── Claude/
│   └── Decisiones.md (análisis detallado)
└── Codex/
    └── Respuestas.md (validaciones)
```

---

## ✨ Uso Recomendado

### Para Developers en Proyecto
```
1. Descarga/Sync: PROMPT_DESARROLLO_ERP.md
2. Referencia durante desarrollo:
   - BD Queries → Ver "Base de Datos"
   - Endpoints → Ver "API RESTful"
   - Validación → Ver "Seguridad"
   - Estructura → Ver "Estructura de Carpetas"
3. Antes de PR → Checklist de Desarrollo
```

### Para Tech Leads / Architects
```
1. Entiende rationale → Claude/Decisiones.md
2. Valida con equipo → Refiere a PROMPT_DESARROLLO_ERP.md
3. Monitorea cumplimiento → Checklist en cada PR
4. Feedback → Agrega en AIs_Dialog.md
```

### Para IAs / Code Assistants

#### FASE 1: CONVERSACIÓN PROFUNDA

**CHATGPT** 🔍 (Iteraciones 1 + 3):
- Lee PROMPT_DESARROLLO_ERP.md completo
- Para nueva decisión: Inicia en AIs_Dialog_v2.md
- **Iteración 1:** Propón idea inicial, plantea cuestiones clave
- **Iteración 3:** Contraargumenta a CLAUDE CHAT, propone ajustes
- Responde análisis de CLAUDE CHAT

**CLAUDE CHAT** 🏛️ (Iteraciones 2 + 4):
- Recibe propuesta de CHATGPT
- **Iteración 2:** Analiza profundamente, contraargumenta, formula preguntas nuevas
- **Iteración 4:** Consolida posiciones, decide dirección arquitectónica
- Pasa decisión consolidada a CLAUDE CODE

#### FASE 2: IMPLEMENTACIÓN TÉCNICA

**CLAUDE CODE** ⚙️ (Iteración 5):
- Recibe **decisión arquitectónica consolidada** de CLAUDE CHAT
- Propone **implementación técnica detallada** (no arquitectura, sino cómo)
- Detecta limitaciones técnicas prácticas
- Pasa especificación a CODEX

#### FASE 3: VALIDACIÓN

**CODEX** 🚀 (Iteración 6):
- Recibe especificación técnica de CLAUDE CODE
- **Valida viabilidad** de implementación
- Propone ajustes prácticos
- Prepara para ejecutar

#### CIERRE Y EJECUCIÓN

**CLAUDE CHAT:** Cierra decisión final (consolida todo feedback)  
**CODEX:** **IMPLEMENTA** decisión en codebase

**Cuando generen código:**
- Sigue estructura (AIs_Dialog_v2.md DA-001)
- Max 150 líneas (AIs_Dialog_v2.md DA-004)
- Aplica SRP
- Agrega tests según cobertura
- Valida seguridad OWASP
- Referencia PROMPT_DESARROLLO_ERP.md

---

## 🔄 Proceso de Actualización

Si necesitas **cambiar algo** en los lineamientos:

1. **Propuesta:** CODEX analiza y propone en AIs_Dialog.md
2. **Auditoría:** CLAUDE revisa y cuestiona
3. **Conclusión:** CLAUDE cierra decisión final
4. **Aplicación:** Actualizar PROMPT_DESARROLLO_ERP.md
5. **Comunicación:** Equipo consulta AIs_Dialog.md + PROMPT

---

## 📊 Métricas de Éxito

Esperamos que con estos lineamientos:

| Métrica | Antes | Después | Meta |
|---------|-------|---------|------|
| Bugs por release | 8-12 | 3-5 | < 5 |
| Code review time | 30-45 min | 10-15 min | < 15 min |
| Onboarding nuevo dev | 2-3 semanas | 3-5 días | < 1 semana |
| Code coverage crítico | 60% | 85% | > 90% |
| Security issues | 2-3/quarter | 0-1/quarter | 0 |
| Tech debt (bugs) | Alto | Bajo | Muy bajo |

---

## 🤝 Proceso de Decisiones Iterativas (4 Agentes)

**Flujo con Conversación Profunda:**

### FASE 1: EXPLORACIÓN (CHATGPT ↔ CLAUDE CHAT) - 4 iteraciones
```
Iteración 1: CHATGPT propone idea inicial + cuestiones
             ↓
Iteración 2: CLAUDE CHAT analiza + contraargumenta + profundiza
             ↓
Iteración 3: CHATGPT contraargumenta + propone ajustes
             ↓
Iteración 4: CLAUDE CHAT consolida posiciones → DECISIÓN ARQUITECTÓNICA
```

### FASE 2: TÉCNICA (CLAUDE CODE) - 1 iteración
```
Iteración 5: CLAUDE CODE propone implementación técnica detallada
```

### FASE 3: VALIDACIÓN (CODEX) - 1 iteración
```
Iteración 6: CODEX valida viabilidad, propone ajustes prácticos
```

### CIERRE Y EJECUCIÓN
```
CLAUDE CHAT cierra decisión final (consolida todo) → CODEX IMPLEMENTA
```

**Máximo 6 iteraciones típicamente** (4 conversación + 1 técnica + 1 validación)

Ver sección "Flujo de Decisiones" en **AIs_Dialog_v2.md** para detalles exactos.

---

## 📌 Checklist de Onboarding

- [ ] He leído PROMPT_DESARROLLO_ERP.md
- [ ] Entiendo la estructura de carpetas (max 5 niveles)
- [ ] Sé cuál es la normalización mínima (3FN)
- [ ] Conozco el checklist de desarrollo
- [ ] Sé dónde encontrar respuestas (este README)
- [ ] Estoy listo para empezar a programar

---

## 🎓 Recursos Adicionales

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **OpenAPI 3.0:** https://spec.openapis.org/oas/v3.0.3
- **TypeScript Handbook:** https://www.typescriptlang.org/docs/
- **Express Best Practices:** https://expressjs.com/en/advanced/best-practice-security.html
- **Fabric/Knowledge/Books/Databases/:** PDFs de fundamentos de BD

---

## 📈 Versión y Cambios

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-07-26 | Versión inicial - CLAUDE establece lineamientos |
| 1.1 | [Pendiente] | CODEX valida y agrega feedback |
| 2.0 | [Futuro] | Incorporar learnings de fase backend |

---

**Estado Actual:** 🟢 ACTIVO  
**Próxima Actualización Esperada:** 2026-07-27 (Validación CODEX)  
**Creado por:** CLAUDE (IA Agent)  
**Validación Pendiente:** CODEX (IA Agent)

---

**¡Bienvenido al desarrollo profesional de GYPPORT ERP!** 🚀


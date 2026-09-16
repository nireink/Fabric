# DOCUMENTO DE APOYO A LA DECISIÓN
## Resolución de Bloqueadores UNR-000001, 002, 003 de GYPPORT®

**Fecha:** 2026-08-01  
**Origen:** Análisis FASE 1 - Base de Conocimiento  
**Propósito:** Presentar opciones, análisis y recomendaciones para que Eduardo resuelva tres asuntos críticos de persistencia  
**Destinatario:** Eduardo (Propietario de GYPPORT®)  
**Clasificación:** Apoyo a decisión (NO es recomendación impuesta; son opciones con análisis)

---

## RESUMEN EJECUTIVO

Se han identificado **3 asuntos bloqueadores críticos** que impiden importación de corpus funcional e inicio de Fase 2:

| UNR ID | Asunto | Impacto | Urgencia |
|--------|--------|--------|----------|
| **UNR-000001** | Ruta física definitiva de Fabric | CRÍTICO - Persistencia | INMEDIATA |
| **UNR-000002** | Política de versionado y repositorio privado | ALTO - Historial | INMEDIATA |
| **UNR-000003** | Dispositivo secundario de respaldo (QNAP/Cloud) | CRÍTICO - Recuperación | INMEDIATA |

**Recomendación:** Resolver en orden UNR-001 → UNR-003 → UNR-002 antes de recibir corpus.

---

## UNR-000001: RUTA FÍSICA DEFINITIVA DE FABRIC {#unr-001}

### Situación Actual

Fabric se creó en:  
`D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\`

**Preguntas sin respuesta:**
- ¿Es esta la ubicación DEFINITIVA o es temporal?
- ¿Se moverá a otra ruta/partición/disco cuando esté en producción?
- ¿Hay restricciones de acceso (red, permisos, sincronización)?

**Por qué importa:**
- Todas las rutas en .chatgpt/ asumen que Fabric está en D:\
- Todos los scripts de respaldo referenciaran esta ruta
- Un cambio posterior requeriría actualizar decenas de referencias

---

### OPCIÓN 1: Mantener en D:\ (LOCAL PC)

**Descripción:** Fabric permanece en disco local D: del equipo de desarrollo.

**Ventajas:**
- ✅ Rápido acceso (no hay latencia de red)
- ✅ Bajo costo (usa espacio existente)
- ✅ Independencia de infraestructura corporativa
- ✅ Control total sobre cambios

**Desventajas:**
- ❌ Riesgo si D: falla (depende de COPIA_2 y COPIA_3)
- ❌ No hay acceso remoto desde otros equipos
- ❌ Difícil colaboración si hay múltiples usuarios
- ❌ Si equipo se daña, recuperación es lenta

**Recomendación:** Adecuada si Fabric es personal/única instancia. Requiere respaldos robustos.

---

### OPCIÓN 2: Mover a Servidor Corporativo (SMB/NAS)

**Descripción:** Fabric reside en compartición de red (QNAP, servidor SMB, o equivalente).

**Ventajas:**
- ✅ Acceso desde múltiples equipos
- ✅ Centralización física
- ✅ Facilita respaldos automáticos
- ✅ Mejor recuperación ante fallo de PC local
- ✅ Control corporativo sobre permisos/auditoría

**Desventajas:**
- ❌ Latencia de red (más lento que disco local)
- ❌ Depende de infraestructura corporativa
- ❌ Requiere configuración de comparticiones SMB
- ❌ Riesgo si servidor principal falla

**Recomendación:** Ideal para equipos de trabajo. Requiere servidor confiable.

---

### OPCIÓN 3: Ruta Híbrida (Local + Sincronización a Servidor)

**Descripción:** Fabric vive en D:\ (local) pero se sincroniza automáticamente a servidor corporativo usando herramienta como Syncthing, rsync, o cloud.

**Ventajas:**
- ✅ Rápido acceso local
- ✅ Respaldo automático en servidor
- ✅ Recuperación rápida si D: falla
- ✅ Control local sin sacrificar sincronización

**Desventajas:**
- ❌ Complejidad de sincronización
- ❌ Posibles conflictos si cambios en paralelo
- ❌ Requiere herramienta de sincronización

**Recomendación:** Balance entre velocidad y seguridad. Requiere política de sincronización clara.

---

### DECISIÓN REQUERIDA

**Pregunta para Eduardo:**
> ¿Cuál será la ruta física DEFINITIVA de Fabric?  
> - (A) D:\ local (Opción 1)  
> - (B) \\SERVIDOR\comparticion (Opción 2)  
> - (C) D:\ con sincronización a SERVIDOR (Opción 3)  
> - (D) Otra:___

**Una vez decidido:**
1. Registrar decisión en DECISION_REGISTER.md como DEC-000002
2. Actualizar todas las referencias de rutas en Fabric/
3. Configurar permanentemente esa ubicación

---

## UNR-000003: DISPOSITIVO SECUNDARIO DE RESPALDO (COPIA_2) {#unr-003}

### Situación Actual

La estrategia de respaldo propuesta es de **3 copias:**

```
COPIA_1 = PC_LOCAL (D:\)
COPIA_2 = ??? (QNAP, Cloud, Disco externo)  ← PENDIENTE
COPIA_3 = REPOSITORIO_PRIVADO_O_BACKUP_CIFRADO (Git, OneDrive, etc.)  ← PENDIENTE
```

**Por qué importa:**
- COPIA_2 es tu **respaldo corporativo rápido** (recuperación en minutos)
- Sin COPIA_2, solo tienes COPIA_1 (local) y COPIA_3 (remoto lento)
- Ante fallo de D:\, recuperación es lenta sin COPIA_2

---

### OPCIÓN A: QNAP NAS (Recommended)

**Descripción:** Dispositivo NAS (Network Attached Storage) dedicado en oficina/servidor.

**Ventajas:**
- ✅ Respaldo rápido (está en red corporativa)
- ✅ Almacenamiento redundante (RAID interno)
- ✅ Bajo mantenimiento
- ✅ Acceso desde múltiples equipos
- ✅ Integración con herramientas de sincronización

**Desventajas:**
- ❌ Costo inicial (equipo NAS)
- ❌ Requiere configuración y mantenimiento
- ❌ Depende de red corporativa
- ❌ Si oficina cae, no hay acceso

**Estimado:** $200-500 USD para NAS pequeño (4 bahías)  
**Recomendación:** Ideal para persistencia corporativa confiable.

---

### OPCIÓN B: Disco Externo USB (Budget)

**Descripción:** Disco externo conectado a PC o servidor central.

**Ventajas:**
- ✅ Bajo costo ($30-100)
- ✅ Fácil de conectar/desconectar
- ✅ Portabilidad
- ✅ No requiere configuración compleja

**Desventajas:**
- ❌ No es redundante (fallo = pérdida total)
- ❌ Requiere conexión física
- ❌ Difícil automatizar respaldos
- ❌ No está disponible si se desconecta
- ❌ Lento para recuperación en caso de fallo crítico

**Recomendación:** Solución temporal/adicional, no suficiente como COPIA_2 única.

---

### OPCIÓN C: Cloud Storage (Google Drive, OneDrive, AWS S3)

**Descripción:** Usar servicio cloud como respaldo secundario.

**Ventajas:**
- ✅ Disponible desde cualquier lugar
- ✅ Redundancia automática (proveedores)
- ✅ Escalable (paga por uso)
- ✅ Integración con Fabric posible (rclone, etc.)

**Desventajas:**
- ❌ Dependencia de conexión a internet
- ❌ Costo recurrente
- ❌ Privacidad/cumplimiento normativo (datos en servidores de terceros)
- ❌ Más lento que NAS local
- ❌ Posible latencia significativa

**Estimado:** $10-50/mes (OneDrive, Google)  
**Recomendación:** Válido como COPIA_3, pero menos ideal para COPIA_2 (requiere QNAP o similar).

---

### OPCIÓN D: Servidor Corporativo con Respaldo Automático

**Descripción:** Integrar Fabric en servidor central corporativo con políticas de respaldo.

**Ventajas:**
- ✅ Respaldo automático integrado
- ✅ Redundancia RAID del servidor
- ✅ Acceso remoto y local
- ✅ Auditoría centralizada

**Desventajas:**
- ❌ Requiere infraestructura corporativa dedicada
- ❌ Depende de disponibilidad del servidor
- ❌ Complejidad de configuración

**Recomendación:** Ideal si existe servidor corporativo robusto ya en lugar.

---

### DECISIÓN REQUERIDA

**Pregunta para Eduardo:**
> ¿Cuál será el dispositivo de COPIA_2 (respaldo secundario)?  
> - (A) QNAP NAS (4+ bahías, RAID 5/6)  
> - (B) Disco Externo USB + Script de sincronización manual  
> - (C) Cloud Storage (OneDrive, Google, AWS) + herramienta sync  
> - (D) Servidor corporativo existente  
> - (E) Combinación de los anteriores  
> - (F) Otro:___

**Una vez decidido:**
1. Registrar en DECISION_REGISTER.md como DEC-000003
2. Especificar modelo/ubicación exacta
3. Provisionar espacio (calcular: tamaño_Fabric × 1.2)
4. Configurar script de respaldo automático

---

## UNR-000002: POLÍTICA DE VERSIONADO Y REPOSITORIO PRIVADO {#unr-002}

### Situación Actual

**Tres capas de persistencia necesitan versioning:**

1. **Markdown canónico** (.chatgpt/, Governance/, documentación)
2. **Corpus procesado** (Knowledge/Processing/, matrices, KN)
3. **Derivados** (reportes, presentaciones, documentos especializados)

**Preguntas sin respuesta:**
- ¿Usar Git, o almacenamiento simple con timestamps?
- ¿Repositorio privado (GitHub, GitLab, Gitea) o local?
- ¿Política de branching? ¿Releases? ¿Tags?
- ¿Frecuencia de commits? ¿Quién autoriza?

**Por qué importa:**
- Sin versionado, no puedes recuperar versiones anteriores
- Sin repositorio, pierdes historial si disco falla
- Sin política clara, cambios se mezclan sin auditoría

---

### OPCIÓN 1: Git Privado en GitHub/GitLab (Recomendado)

**Descripción:** Usar GitHub/GitLab con repositorio privado. Commit frecuentes, historial completo.

**Ventajas:**
- ✅ Versionado profesional (historial completo)
- ✅ Recuperación granular (cualquier versión anterior)
- ✅ Auditoría integrada (quién, cuándo, por qué)
- ✅ Colaboración (branches, pull requests)
- ✅ Integración con CI/CD futuro
- ✅ Respaldo remoto (COPIA_3)

**Desventajas:**
- ❌ Costo ($4-21/mes si usas organizaciones privadas)
- ❌ Depende de conexión a internet
- ❌ Privacidad: datos en servidores de GitHub/GitLab
- ❌ Curva de aprendizaje (Git)

**Estimado:** $0-21/mes  
**Recomendación:** Ideal para equipos, profesionalismo, auditoría.

---

### OPCIÓN 2: Gitea Auto-hospedado (Self-hosted)

**Descripción:** Instalar Gitea (Git auto-hospedado) en servidor local.

**Ventajas:**
- ✅ Git completo sin depender de GitHub/GitLab
- ✅ Control total sobre datos
- ✅ Privacidad máxima (on-premises)
- ✅ Sin costos recurrentes (solo hardware)
- ✅ Integración personalizable

**Desventajas:**
- ❌ Requiere servidor dedicado
- ❌ Mantenimiento/parches propios
- ❌ Si servidor falla, Git falla
- ❌ Backup de Gitea requiere proceso adicional

**Recomendación:** Para máxima privacidad y control. Requiere capacidad técnica.

---

### OPCIÓN 3: Sistema Simple (Sin Git)

**Descripción:** Carpetas con timestamps + script de respaldo manual/automático.

**Ventajas:**
- ✅ Bajo costo
- ✅ Sin curva de aprendizaje
- ✅ Directa (archivos simples)

**Desventajas:**
- ❌ Sin auditoría (no se sabe quién cambió qué)
- ❌ Sin versionado granular
- ❌ Recuperación lenta (carpetas completas, no cambios)
- ❌ Sin colaboración
- ❌ Difícil de respaldar consistentemente

**Recomendación:** Solución temporal. No recomendado para producción.

---

### POLÍTICA DE BRANCHING (si se elige Git)

**Recomendación:** Git Flow simplificado

```
main/          ← Versiones estables (tags semánticos v1.0, v1.1, etc.)
  ↑ (PR merge only)
develop/       ← Integración de cambios (HEAD del trabajo activo)
  ↑ (PR de feature branches)
feature/*      ← Cambios individuales (PROTOCOLO_FASE2, Corpus_Import, etc.)
hotfix/*       ← Fixes urgentes
```

**Frecuencia de commits:**
- Por cada KN procesada: 1 commit
- Por cada decisión registrada: 1 commit
- Por cada checkpoint completado: 1 commit
- Mínimo: semanal (evitar cambios sin versionar)

---

### DECISIÓN REQUERIDA

**Pregunta para Eduardo:**
> ¿Cuál será el sistema de versionado y repositorio privado?  
> - (A) GitHub/GitLab privado (Git Flow) — Recomendado  
> - (B) Gitea auto-hospedado en servidor corporativo  
> - (C) Sistema simple con timestamps + script respaldo  
> - (D) Otro:___

**Una vez decidido:**
1. Registrar en DECISION_REGISTER.md como DEC-000004
2. Crear repositorio / configurar sistema
3. Hacer commit inicial de Fabric tal como existe hoy
4. Establecer política de commits (responsable, frecuencia)

---

## ORDEN RECOMENDADO DE DECISIONES

```
PASO 1: Resolver UNR-000001 (Ruta física)
        ↓
        Ubicación confirmada → Scripts de respaldo apuntan correctamente
        
PASO 2: Resolver UNR-000003 (Dispositivo COPIA_2)
        ↓
        QNAP/Disco/Cloud confirmado → Configurar sincronización
        
PASO 3: Resolver UNR-000002 (Versionado)
        ↓
        Git/Gitea/Simple → Primer commit de Fabric
        
PASO 4: Validar que 3 copias funcionan
        ↓
        Test: Simular pérdida de D:\ → Recuperar desde COPIA_2
        
PASO 5: Importar corpus funcional de GYPPORT®
        ↓
        Comienza FASE 2 (Modelado de Dominio)
```

---

## TEMPLATE DE DECISIÓN PARA EDUARDO

**Una vez que Eduardo haya decidido, él completa este template y lo pega en DECISION_REGISTER.md:**

```markdown
| DEC-000002 | 2026-08-XX | Ruta física definitiva de Fabric = [OPCIÓN ELEGIDA] | Eduardo | [Referencia] | APPROVED |
| DEC-000003 | 2026-08-XX | Dispositivo COPIA_2 = [OPCIÓN ELEGIDA] | Eduardo | [Referencia] | APPROVED |
| DEC-000004 | 2026-08-XX | Versionado = [OPCIÓN ELEGIDA] | Eduardo | [Referencia] | APPROVED |
```

Una vez registradas como APPROVED, desbloquean:
- Configuración de scripts de respaldo
- Inicio de Fase 2
- Importación de corpus

---

## CRONOGRAMA SUGERIDO

| Semana | Hito | Responsable |
|--------|------|-------------|
| Semana 1 (Hoy) | Análisis FASE 1 completado; este documento presentado a Eduardo | Claude |
| Semana 2 | Eduardo revisa opciones y toma decisiones UNR-001, 003, 002 | Eduardo |
| Semana 3 | Provisionar/configurar COPIA_2, Git, respaldos | IT/DevOps |
| Semana 4 | Validar 3 copias; preparar estructura de ingesta de corpus | Claude |
| Semana 5+ | Recibir corpus funcional de GYPPORT®; ejecutar FASE 2 | Eduardo + Claude |

---

## CONTACTO Y SIGUIENTES PASOS

Este documento es un **apoyo a la decisión**, no un mandato. Eduardo es libre de:
- ✓ Elegir cualquiera de las opciones presentadas
- ✓ Combinar opciones
- ✓ Proponer alternativas no listadas
- ✓ Diferir decisiones si aún no está listo

**Una vez Eduardo decida:**
1. Registre decisiones en DECISION_REGISTER.md
2. Comunique a Claude los detalles de UNR-001, 003, 002
3. Claude configura estructura correspondiente
4. Se habilita Fase 2

**No hay prisa.** El protocolo está diseñado para ser incremental y flexible.

---

**Fin del Documento de Apoyo a la Decisión**

Versión: 1.0  
Fecha: 2026-08-01  
Estado: DISPONIBLE PARA REVISIÓN DE EDUARDO

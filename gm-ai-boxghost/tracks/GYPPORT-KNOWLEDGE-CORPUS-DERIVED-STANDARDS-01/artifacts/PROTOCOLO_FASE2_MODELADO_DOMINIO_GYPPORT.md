# PROTOCOLO FASE 2: MODELADO DEL DOMINIO
## Formalización del Conocimiento Consolidado en Modelos Conceptuales

**Versión:** 1.0 PLANTILLA  
**Fecha de disponibilidad:** Cuando Fase 1 esté completada + Corpus importado + UNR resueltos  
**Estado:** DISEÑO — No es ejecutable hasta que prerequisitos se cumplan  
**Organización:** ISAGRUB CORPORACIÓN C.L. / GYPPORT®  

---

## PROPÓSITO DE ESTA FASE

**Fase 1** consolidó el conocimiento EN TEXTO (Unidades de Conocimiento, decisiones, políticas).

**Fase 2** formaliza ese conocimiento EN MODELOS (diagramas, esquemas, relaciones formales).

**Resultado esperado:** Modelos de dominio verificables que sirvan de puente entre negocio (Fase 1) y especialización técnica (Fase 3).

---

## DIFERENCIA CLAVE: FASE 1 vs FASE 2

| Aspecto | FASE 1 | FASE 2 |
|--------|--------|--------|
| **Input** | Documentación fuente (PDFs, DOCX, wikis) | Base de Conocimiento SSOT (KN) |
| **Procesamiento** | Lectura, extracción, consolidación | Modelado, formalización, diagrama |
| **Output** | 15-100 Unidades de Conocimiento | Diagramas UML, BPMN, C4, ER, Matrices |
| **Enfoque** | "¿Qué dice la documentación?" | "¿Cómo se relacionan los conceptos?" |
| **Audiencia** | Arquitectos, analistas, auditores | Diseñadores, DBAs, arquitectos técnicos |
| **Herramientas** | Lectura, trazabilidad, búsqueda | UML, BPMN, diagrama ER, matrices |

---

## PREREQUISITOS (DEBEN ESTAR CUMPLIDOS ANTES DE INICIAR)

- ✅ FASE 1 completada (Base de Conocimiento con 15+ KN)
- ✅ Corpus funcional de GYPPORT® importado (especificación, procesos, datos)
- ✅ UNR-000001, 002, 003 resueltos (decisiones registradas)
- ✅ REGISTRO_FUENTES.md completo (corpus registrado y validado)
- ✅ Respaldos configurados (COPIA_1, COPIA_2, COPIA_3)

**Si alguno falta:** Detener e informar a Eduardo.

---

## OBJETIVO GENERAL DE FASE 2

Transformar la Base de Conocimiento (SSOT) de GYPPORT® en **modelos formales de dominio** que:

1. Capturen la estructura conceptual de GYPPORT®
2. Muestren relaciones entre actores, procesos, datos
3. Identifiquen ambigüedades restantes en la especificación
4. Preparen la arquitectura para Fase 3 (especialización técnica)
5. Sean verificables y trazables (cada modelo referencia KN de Fase 1)

---

## ALCANCE EXPLÍCITO DE FASE 2

### ✓ INCLUYE:

1. **Modelado de Procesos de Negocio** (BPMN 2.0)
   - Diagramas de flujos de transacciones
   - Decisiones, excepciones, ciclos
   - Responsables y sistemas involucrados

2. **Modelado de Dominio** (UML Class Diagram)
   - Entidades de negocio (Cliente, Producto, Transacción)
   - Atributos y relaciones
   - Cardinalidades
   - Herencia y asociaciones

3. **Modelado de Datos Conceptual** (ER Diagram)
   - Entidades, atributos, llaves
   - Relaciones entre entidades
   - Reglas de integridad

4. **Modelado Arquitectónico de Alto Nivel** (C4 Level 1-2)
   - Sistemas principales
   - Fronteras de módulos
   - Flujos de datos entre módulos

5. **Matriz de Trazabilidad Fase 2** (Modelo ↔ KN)
   - Qué KN de Fase 1 sustenta cada modelo
   - Cobertura: ¿Todos los KN están representados en algún modelo?

6. **Catálogo de Términos Formalizados** (Glosario + Ontología)
   - Definiciones precisas (no solo equivalencias)
   - Restricciones (un Cliente siempre tiene RUC o Pasaporte)
   - Opcionalidad (un Producto puede no tener lote)

7. **Matriz de Decisiones de Diseño Conceptual**
   - Por qué se eligió un modelo sobre otro
   - Trade-offs considerados
   - Alternativas rechazadas y razones

### ✗ NO INCLUYE (Fase 3):

- Esquema de base de datos físico (tablas, índices, particiones)
- Diseño de APIs (endpoints, métodos, autenticación)
- Interfaz de usuario (wireframes, mockups)
- Arquitectura técnica detallada (servidores, deployment)
- Código fuente
- Especificaciones de seguridad implementadas
- Procedimientos de backup/recovery

---

## METODOLOGÍA: ETAPAS DE FASE 2

### ETAPA 1: ANÁLISIS COMPARATIVO (1-2 semanas)

**Objetivo:** Reconciliar múltiples fuentes de verdad en el corpus.

**Actividades:**
1. Leer corpus completo (especificación, procesos, datos, normas)
2. Comparar: ¿La especificación coincide con los procesos? ¿Los datos?
3. Documentar discrepancias: "La especificación dice X, pero el proceso hace Y"
4. Crear matriz de DISCREPANCIAS_ENCONTRADAS.md

**Entregable:**
- Matriz: Documento vs Documento, diferencias detectadas
- Lista de preguntas para Eduardo (ambigüedades a resolver)
- Propuesta de "fuente canónica" cuando hay conflicto

**Nota:** Si hay conflictos, se resuelven CON Eduardo. Claude no decide.

---

### ETAPA 2: EXTRACCIÓN DE CONCEPTOS DE DOMINIO (2-3 semanas)

**Objetivo:** Identificar todas las entidades, procesos, reglas del dominio.

**Actividades:**
1. Lectura de corpus línea por línea
2. Extraer: "Cliente, Producto, Transacción, Factura, Retención, Asiento"
3. Para cada concepto: atributos, relaciones, restricciones
4. Crear "Diccionario de Conceptos de Dominio"

**Diccionario de Conceptos (plantilla):**

```markdown
## Concepto: CLIENTE

**Definición (de Fase 1/corpus):**  
Una empresa o persona que realiza transacciones comerciales con GYPPORT®.

**Atributos:**
- ID_Cliente (único, generado por sistema)
- RUC (texto, 13 caracteres, único, CRITICO)
- Pasaporte (texto, opcional si tiene RUC)
- Razón Social (texto, obligatorio)
- Email (texto, opcional)
- Teléfono (texto, opcional)
- Dirección Fiscal (texto, obligatorio)
- Límite Crédito (número, >= 0, opcional)

**Relaciones:**
- Crea → Muchas transacciones (Pedidos, Facturas)
- Tiene → Una o más direcciones de entrega
- Pertenece A → Una categoría de cliente (Mayorista, Minorista)

**Restricciones:**
- RUC y Pasaporte no pueden ambos estar vacíos
- Si tipo cliente = "Extranjero", debe tener pasaporte válido
- No se puede eliminar un Cliente que tiene facturas activas

**Ejemplos de Fase 1/Corpus:**
- KN-000045 (Cliente comercial definición)
- Especificación v2.5, página 23

**Preguntas abiertas:**
- ¿Puede un Cliente tener múltiples RUCs (sucursales)?
- ¿Qué pasa con clientes "dados de baja" en el SRI?
```

**Entregable:**
- Diccionario de Conceptos (20-50 conceptos clave)
- Cada concepto completamente documentado
- Referencias a KN de Fase 1 y corpus

---

### ETAPA 3: MODELADO DE PROCESOS DE NEGOCIO (2-3 semanas)

**Objetivo:** Diagramar CÓMO fluyen las transacciones a través de GYPPORT®.

**Actividades:**
1. Tomar procesos documentados en corpus
2. Crear o mejorar diagramas BPMN 2.0
3. Incluir: actividades, decisiones, excepciones, responsables
4. Para cada proceso, documentar: inicio, fin, precondiciones, excepciones

**Procesos esperados en GYPPORT®:**

```
1. Gestión de Clientes
   - Crear Cliente → Validar RUC SRI → Asignar Límite → Cliente Activo

2. Ciclo de Venta (Pedido a Factura)
   - Crear Pedido → Reservar Stock → Confirmar → Generar Factura → Pago

3. Gestión de Facturación Electrónica
   - Generar XML Factura → Firmar digitalmente → Enviar SRI → Obtener autorización

4. Gestión de Retenciones
   - Identificar transacción sujeta a retención → Calcular % → Generar comprobante de retención

5. Asientos Contables Automáticos
   - Transacción de venta → Generar asiento (Cxc, Ingresos) → Registrar en GL

6. Reportes y Auditoría
   - Generar reporte de ventas → Reconciliar con GL → Auditoría de comprobantes
```

**Entregable:**
- Diagrama BPMN para cada proceso principal
- Matriz: Proceso ↔ Actores involucrados ↔ Sistemas
- Documento: Excepciones detectadas y cómo se manejan

---

### ETAPA 4: MODELADO DE DATOS CONCEPTUAL (1-2 semanas)

**Objetivo:** Diagrama ER (Entity-Relationship) a nivel conceptual.

**Actividades:**
1. Tomar diccionario de conceptos (Etapa 2)
2. Crear diagrama ER con todas las entidades
3. Mostrar relaciones: 1:1, 1:N, M:N
4. Anotar atributos clave, llaves, restricciones

**Ejemplo simplificado (GYPPORT®):**

```
CLIENTE (1) ──────→ (N) TRANSACCIÓN
  ├─ ID_Cliente
  ├─ RUC
  ├─ Razón Social
  └─ Email

TRANSACCIÓN (1) ──→ (N) LINEA_TRANSACCION
  ├─ ID_Transacción
  ├─ Fecha
  ├─ Tipo (Pedido, Factura, Nota Crédito)
  └─ Total

LINEA_TRANSACCION (N) ← (1) PRODUCTO
  ├─ ID_Línea
  ├─ Cantidad
  ├─ Precio Unitario
  └─ Total Línea

TRANSACCIÓN (1) ──→ (N) ASIENTO_CONTABLE
  ├─ ID_Asiento
  ├─ Cuenta_GL
  ├─ Débito/Crédito
  └─ Monto

TRANSACCIÓN (0..1) ← (1) RETENCIÓN
  ├─ ID_Retención
  ├─ Tipo_Retención
  ├─ Porcentaje
  └─ Monto
```

**Entregable:**
- Diagrama ER conceptual completo
- Documento: Definición de cada relación y cardinalidad
- Notas sobre restricciones de integridad

---

### ETAPA 5: MODELADO DE ARQUITECTURA CONCEPTUAL (1-2 semanas)

**Objetivo:** Diagrama de módulos y flujos de datos (C4 Level 1-2).

**Actividades:**
1. Identificar módulos principales (Facturación, Inventario, Contabilidad, etc.)
2. Mostrar cómo se comunican
3. Identificar sistemas externos (SRI, Bancos)

**Ejemplo simplificado:**

```
┌─────────────────────────────────────────────────────────┐
│                      GYPPORT®                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────┐    ┌────────────┐    ┌──────────────┐ │
│  │Facturación │───→│Contabilidad│←───│Facturación   │ │
│  │e Ing.      │    │            │    │Electrónica   │ │
│  └─┬──────────┘    └──────┬─────┘    └────┬─────────┘ │
│    │                      │               │            │
│    ↓                      ↓               ↓            │
│  ┌──────────┐    ┌─────────────┐    ┌──────────┐      │
│  │Inventario│    │ Reportes &  │    │Integ.    │      │
│  │          │    │ Auditoría   │    │ Bancaria │      │
│  └──────────┘    └─────────────┘    └──────────┘      │
│        ↑                                   ↑            │
└────────┼───────────────────────────────────┼───────────┘
         │                                   │
         ↓                                   ↓
    ┌─────────┐                      ┌──────────────┐
    │BD       │                      │SRI / Bancos  │
    │GYPPORT  │                      │Sistemas Ext  │
    └─────────┘                      └──────────────┘
```

**Entregable:**
- Diagrama C4 Nivel 1 (Sistemas externos)
- Diagrama C4 Nivel 2 (Módulos internos)
- Matriz de flujos: Módulo A → Módulo B, datos intercambiados

---

### ETAPA 6: VALIDACIÓN Y REVISIÓN (1-2 semanas)

**Objetivo:** Verificar que los modelos son correctos y completos.

**Actividades:**

1. **Revisión de completitud:**
   - ¿Todos los conceptos de corpus están representados en los modelos?
   - ¿Todos los procesos tienen diagrama BPMN?
   - ¿Todos los datos tienen entidad en ER?

2. **Revisión de consistencia:**
   - ¿El diagrama BPMN coincide con el ER? (mismo flujo de datos)
   - ¿Los atributos en ER coinciden con los campos mencionados en procesos?
   - ¿Las relaciones en ER coinciden con las dependencias en BPMN?

3. **Revisión de ambigüedad:**
   - ¿Hay conceptos "vagos" que necesitan clarificación?
   - ¿Hay procesos que terminan sin resultado claro?
   - ¿Hay excepciones documentadas pero no modeladas?

4. **Revisión con Eduardo:**
   - Presentar modelos
   - Recopilar feedback: "¿Es esto correcto?"
   - Incorporar cambios

**Entregable:**
- Documento de "Hallazgos de Validación"
- Lista de "Cambios implementados por feedback"
- Versión final de modelos (aprobada por Eduardo)

---

### ETAPA 7: DOCUMENTACIÓN FINAL (1 semana)

**Objetivo:** Producir documento maestro de Fase 2.

**Contenido:**

```
DOCUMENTO_MAESTRO_FASE2_MODELADO_DOMINIO_GYPPORT.md
│
├── Portada + Metadatos
├── Introducción
├── Prerequisitos (qué se necesitó de Fase 1)
├── Discrepancias Encontradas en Corpus (si las hay)
├── Diccionario Completo de Conceptos de Dominio
├── Diagramas BPMN (Procesos de Negocio)
├── Diagrama ER (Datos Conceptual)
├── Diagrama C4 (Arquitectura Conceptual)
├── Matriz de Trazabilidad (Modelo ↔ KN Fase 1)
├── Matriz de Trazabilidad (Modelo ↔ Corpus)
├── Glosario Formalizado (Ontología)
├── Decisiones de Diseño Conceptual
├── Preguntas Abiertas (para futuro)
├── Conclusiones
└── Apéndices (diagramas adicionales, matrices)
```

**Entregable:** 
- DOCUMENTO_MAESTRO_FASE2_MODELADO_DOMINIO_GYPPORT.md (80-150 páginas)
- Archivos de diagramas (*.bpmn, *.xml, *.json para ER, *.png para visualizaciones)

---

## CRONOGRAMA ESPERADO DE FASE 2

| Semana | Etapa | Hito | Entregable |
|--------|-------|------|-----------|
| 1-2 | Análisis Comparativo | Reconciliar fuentes | DISCREPANCIAS.md |
| 3-5 | Extracción de Conceptos | Diccionario | Conceptos_Dominio.md |
| 6-8 | BPMN de Procesos | Diagramas | BPMN_*.bpmn |
| 9-10 | Modelo ER Conceptual | Diagrama | ER_Conceptual.png |
| 11-12 | Arquitectura C4 | Diagramas | C4_*.png |
| 13-14 | Validación y Revisión | Feedback → Cambios | Modelos_Finales |
| 15 | Documento Maestro | Consolidación | DOCUMENTO_MAESTRO_FASE2.md |

**Duración total:** ~15 semanas (3-4 meses) con 1 recurso dedicado

---

## HERRAMIENTAS RECOMENDADAS (NO MANDATORIAS)

- **BPMN:** draw.io, Lucidchart, Camunda Modeler
- **ER Diagram:** Lucidchart, dbdiagram.io, MySQL Workbench
- **C4:** draw.io, Structurizr
- **Versionado:** GitHub (DECISION_REGISTER DEC-000004)

---

## ENTRADAS ESPERADAS (DE FASE 1 + CORPUS)

- ✅ Base de Conocimiento SSOT (15-100 KN)
- ✅ Corpus completo de GYPPORT® (especificaciones, procesos, datos, normas)
- ✅ Decisiones aprobadas (DEC-000001 a DEC-000004)
- ✅ Preguntas abiertas de Fase 1 (resueltas o documentadas)

## SALIDAS ESPERADAS (PARA FASE 3)

- ✅ Modelos de dominio formales (BPMN, ER, C4)
- ✅ Diccionario de conceptos
- ✅ Matriz de trazabilidad (Modelo ↔ KN ↔ Corpus)
- ✅ Documento maestro Fase 2
- ✅ Preguntas de diseño resueltas o documentadas

---

## REGLAS OPERATIVAS FASE 2

1. **No inventar conceptos:** Todo debe estar en Fase 1 o Corpus
2. **Mantener trazabilidad:** Cada modelo referencia sus orígenes
3. **Documentar excepciones:** "Lo que no sabemos" es tan importante como "lo que sabemos"
4. **Validar con Eduardo:** Los modelos representan su negocio; él valida
5. **No avanzar a Fase 3 sin aprobación:** Fase 3 depende de estos modelos

---

## CÓMO COMIENZA FASE 2

1. Eduardo confirma que corpus está listo (REGISTRO_FUENTES.md completo)
2. Claude iniciará Análisis Comparativo (Etapa 1)
3. Cada 2-3 semanas, checkpoint con Eduardo
4. Cambios por feedback se incorporan inmediatamente
5. Cuando Etapa 7 (Documento Maestro) esté completa, Fase 2 termina

---

**Fin de Protocolo Fase 2**

Versión: 1.0 PLANTILLA  
Fecha: 2026-08-01  
Estado: DISEÑO (No ejecutable hasta que prerequisitos se cumplan)  
Siguiente: Fase 3 (Documentación Especializada)

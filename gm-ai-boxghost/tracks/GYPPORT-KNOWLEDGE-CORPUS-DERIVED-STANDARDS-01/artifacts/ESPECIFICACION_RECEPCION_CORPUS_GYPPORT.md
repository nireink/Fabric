# ESPECIFICACIÓN DE RECEPCIÓN DE CORPUS FUNCIONAL GYPPORT®

**Documento:** Preparación para importación de documentación funcional  
**Fecha:** 2026-08-01  
**Versión:** 1.0 PLANTILLA  
**Estado:** LISTO PARA USO (Cuando Eduardo haya resuelto UNR-001, 002, 003)  
**Propósito:** Guía paso a paso para recibir, registrar y preparar corpus funcional de GYPPORT®

---

## RESUMEN

Cuando Eduardo esté listo para traer documentación funcional de GYPPORT® a Fabric, este documento especifica:

1. **Tipos de fuentes esperadas** (qué documentos son críticos)
2. **Ubicaciones de recepción** (dónde guardarlas en Fabric)
3. **Registro formal** (cómo documentar cada fuente)
4. **Antes de procesar** (validaciones previas)
5. **Checklist de recepción** (verificación completa)

**NO es un protocolo de análisis.** Solo prepara los archivos para que FASE 2 pueda procesarlos.

---

## PARTE 1: TIPOS DE FUENTES ESPERADAS

### Categoría A: FUENTES FUNCIONALES (CRÍTICA)

Estas son el corazón del negocio GYPPORT®. **Sin ellas, Fase 2 no puede proceder.**

#### A1. Especificación Funcional del ERP GYPPORT®

**Qué es:** Documento(s) que describen qué hace GYPPORT® funcionalmente.

**Incluye típicamente:**
- Módulos: Facturación, Inventario, Contabilidad, RH, Reportes, Integraciones
- Procesos de negocio: Cómo fluye una orden de compra → factura → asiento contable
- Reglas de negocio: Descuentos, retenciones, validaciones
- Usuarios y roles: Quién puede hacer qué
- Datos clave: Clientes, productos, transacciones, saldos

**Formatos esperados:** PDF, DOCX, Confluence, Wiki

**Ejemplos:**
- "Especificación Funcional GYPPORT® v2.5.pdf" (80 páginas)
- "Manual de Procesos Facturación.docx"
- "Guía de Configuración Básica.pdf"

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/[NOMBRE_DOCUMENTO.pdf|.docx]`

**Criticidad:** 🔴 CRÍTICA — Sin esto, no hay Fase 2

---

#### A2. Procesos de Negocio GYPPORT®

**Qué es:** Diagramas, tablas, textos que describen CÓMO se hacen las cosas.

**Incluye típicamente:**
- BPMN o flowcharts de procesos
- Descripción paso a paso de procedimientos
- Responsables, tiempos, excepciones
- Integración entre módulos

**Ejemplos:**
- "Proceso Pedido a Factura (BPMN).pdf"
- "Procedimiento Retenciones.docx"
- "Flujo Conciliación Bancaria.png" (diagrama)

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/Procesos/[NOMBRE.pdf|.pptx|.png]`

**Criticidad:** 🔴 CRÍTICA — Base para modelado de dominio

---

#### A3. Catálogo de Entidades y Datos

**Qué es:** Lista de qué datos maneja GYPPORT® (campos, tipos, relaciones).

**Incluye típicamente:**
- Clientes (RUC, razón social, contactos, direcciones)
- Productos (códigos, precios, categorías, almacenes)
- Transacciones (órdenes, facturas, retenciones, asientos)
- Configuración (parámetros, tasas impositivas, períodos)

**Formatos esperados:** XLSX, PDF tabla, DOCX lista, diagrama ER

**Ejemplos:**
- "Catálogo de Entidades GYPPORT®.xlsx" (diccionario de datos)
- "Modelo Conceptual (ER Diagram).pdf"

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/Datos/[NOMBRE.xlsx|.pdf]`

**Criticidad:** 🔴 CRÍTICA — Necesario para Fase 3 (BD, APIs)

---

#### A4. Normas y Reglas de Negocio GYPPORT®

**Qué es:** Políticas, restricciones y decisiones de negocio que GYPPORT® debe respetar.

**Incluye típicamente:**
- Reglas tributarias (retenciones, IVA, bases imponibles)
- Políticas de crédito (plazos, intereses, límites)
- Validaciones (no vender sin stock, facturación con documentos vigentes)
- Estándares (numeración de comprobantes, formato de reportes)

**Formatos esperados:** PDF, DOCX, Hoja de cálculo

**Ejemplos:**
- "Normas Tributarias Vigentes Ecuador 2026.pdf"
- "Políticas de Crédito GYPPORT®.docx"
- "Validaciones Críticas.xlsx"

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/Normas/[NOMBRE.pdf|.docx]`

**Criticidad:** 🟠 ALTA — Crítica para Fase 3 (gobernanza, seguridad)

---

#### A5. Manuales de Usuario GYPPORT®

**Qué es:** Guías de cómo usar GYPPORT® (no para IAs, sino como referencia de negocio).

**Incluye típicamente:**
- Pasos para registrar una transacción
- Pasos para emitir reportes
- Pasos para ejecutar auditorías
- Resolución de problemas comunes

**Formatos esperados:** PDF, DOCX

**Ejemplos:**
- "Manual de Usuario - Facturación.pdf"
- "Guía de Reportes Disponibles.docx"

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/Manuales/[NOMBRE.pdf|.docx]`

**Criticidad:** 🟡 MEDIA — Contexto útil para IAs

---

### Categoría B: FUENTES REGULATORIAS Y CONTEXTUALES (ALTA)

Documentos que enmarcan GYPPORT® dentro del contexto ecuatoriano y tributario.

#### B1. Normas Tributarias Ecuador (NIIF, Códigos Tributarios, SRI)

**Qué es:** Regulaciones oficiales que GYPPORT® debe cumplir.

**Incluye:**
- NIIF (Normas Internacionales de Información Financiera)
- Código Tributario Ecuatoriano
- Resoluciones del SRI (Servicio de Rentas Internas)
- RUC, facturas, retenciones, regímenes tributarios
- Cambios normativos recientes (2026)

**Formatos esperados:** PDF

**Ubicación en Fabric:**  
`Knowledge/Sources/Ecuador/Normas_Tributarias/[NOMBRE.pdf]`

**Criticidad:** 🟠 ALTA — Obligatorio para compliance

---

#### B2. Documentación de Integraciones Externas

**Qué es:** Especificaciones de sistemas con los que GYPPORT® se conecta.

**Incluye:**
- APIs de bancos ecuatorianos (consulta saldos, transferencias)
- Catastro SRI (validación RUC)
- Aduanas (si hay movimiento de importación)
- Sistemas de terceros (contabilidad, payroll, e-commerce)

**Formatos esperados:** PDF, especificación técnica, YAML/JSON

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/Integraciones/[NOMBRE.pdf|.yaml]`

**Criticidad:** 🟠 ALTA — Necesario para Fase 3 (APIs)

---

### Categoría C: FUENTES DE SOPORTE (MEDIA)

Documentos que ayudan pero no son críticos para comenzar.

#### C1. Diagramas Arquitectónicos Existentes

**Qué es:** Diagramas UML, C4, arquitectura técnica de GYPPORT®.

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/Arquitectura/[NOMBRE.png|.pdf]`

**Criticidad:** 🟡 MEDIA

---

#### C2. Actas de Decisiones Anteriores

**Qué es:** Reuniones, decisiones de diseño, trade-offs considerados.

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/Decisiones/[NOMBRE.pdf|.md]`

**Criticidad:** 🟡 MEDIA

---

#### C3. Correos o Chats Relevantes (Exportados)

**Qué es:** Conversaciones históricas que documentan decisiones o aclaraciones.

**Ubicación en Fabric:**  
`Knowledge/Sources/Internal/Conversaciones/[FECHA_ASUNTO.txt|.md]`

**Criticidad:** 🟢 BAJA (contextual)

---

## PARTE 2: ESTRUCTURA DE DIRECTORIOS PARA INGESTA

```
D:\...\Fabric\Knowledge\Sources\Internal\
│
├── README_INGESTA.md
│   └── [Este archivo se genera con instrucciones de importación actual]
│
├── Especificacion_Funcional\
│   ├── GYPPORT_Especificacion_Funcional_v2.5.pdf
│   ├── GYPPORT_Especificacion_Funcional_v2.4.pdf (histórico)
│   └── README_VERSIONES.md
│
├── Procesos\
│   ├── Facturacion\
│   │   ├── Proceso_Pedido_a_Factura.pdf
│   │   ├── Flujo_Retenciones.bpmn
│   │   └── Excepciones_Facturacion.docx
│   │
│   ├── Inventario\
│   │   ├── Proceso_Movimiento_Inventario.pdf
│   │   ├── Ajustes_Stock.docx
│   │   └── Kardex_Valorizado.pdf
│   │
│   ├── Contabilidad\
│   │   ├── Proceso_Asientos_Automaticos.pdf
│   │   ├── Proceso_Conciliacion.pdf
│   │   └── Cierre_Periodo.docx
│   │
│   └── [Otros módulos]
│
├── Datos\
│   ├── Catalogo_Entidades_GYPPORT.xlsx
│   ├── Diccionario_Campos.xlsx
│   ├── Diagrama_ER_Logico.pdf
│   └── Diagrama_ER_Fisico.pdf
│
├── Normas\
│   ├── Politicas_Credito.docx
│   ├── Reglas_Negocio_Facturacion.xlsx
│   ├── Validaciones_Criticas.xlsx
│   └── Estandares_Numeracion.docx
│
├── Manuales\
│   ├── Manual_Usuario_Facturacion.pdf
│   ├── Manual_Usuario_Inventario.pdf
│   ├── Guia_Reportes.pdf
│   └── FAQ_Usuario.docx
│
├── Arquitectura\
│   ├── Diagrama_C4_Nivel_1.png
│   ├── Diagrama_Modulos.pdf
│   ├── Decisiones_Arquitectonicas.md
│   └── Trade_offs_Considerados.md
│
├── Integraciones\
│   ├── SRI_API_Specification.pdf
│   ├── Banco_XYZ_API.yaml
│   ├── Integracion_Contabilidad_Externa.pdf
│   └── Webhook_Configuracion.docx
│
├── Decisiones\
│   ├── Acta_Reunion_2026_07_15.md
│   ├── Decision_Tecnologia_Base_Datos.pdf
│   └── Decision_Arquitectura_Modular.md
│
├── Conversaciones\
│   ├── Email_Cambios_SRI_2026.txt
│   ├── Chat_Retenciones_Actualizacion.md
│   └── Llamada_Clarificacion_Facturacion.txt
│
└── [REGISTRO_FUENTES.md] ← Archivo clave (ver Parte 3)
```

---

## PARTE 3: REGISTRO FORMAL DE FUENTES

Cada documento que entra a Fabric DEBE registrarse en un archivo central:

**Ubicación:** `Knowledge/Sources/Internal/REGISTRO_FUENTES.md`

**Formato:**

```markdown
# Registro de Fuentes Importadas a Fabric

| ID | Fecha | Documento | Tipo | Ruta | Tamaño | Autor/Fuente | Versión | Estado | Validado |
|----|-------|-----------|------|------|--------|--------------|---------|--------|----------|
| SRC-001 | 2026-08-XX | Especificación Funcional GYPPORT® v2.5 | PDF | Internal/Especificacion_Funcional/... | 45 MB | Producto Team | 2.5 | VIGENTE | ✓ |
| SRC-002 | 2026-08-XX | Proceso Pedido a Factura | PDF | Internal/Procesos/Facturacion/... | 3 MB | BPM Analyst | 1.0 | VIGENTE | ✓ |
| SRC-003 | 2026-08-XX | Catálogo de Entidades | XLSX | Internal/Datos/... | 500 KB | Data Team | 3.2 | VIGENTE | ✓ |
```

**Campos obligatorios:**
- **ID:** Identificador único (SRC-001, SRC-002, etc.)
- **Fecha:** Cuándo se importó
- **Documento:** Nombre descriptivo
- **Tipo:** PDF, DOCX, XLSX, BPMN, etc.
- **Ruta:** Ubicación exacta en Fabric
- **Tamaño:** Para auditoría de almacenamiento
- **Autor/Fuente:** De dónde vino (producto team, equipo, etc.)
- **Versión:** Versión del documento (2.5, 1.0, etc.)
- **Estado:** VIGENTE, OBSOLETO, PENDIENTE_REVISION
- **Validado:** ✓ Si fue revisado, ✗ Si aún pendiente

---

## PARTE 4: VALIDACIONES ANTES DE PROCESAR

Antes de que Fase 2 procese un corpus, hacer estas validaciones:

### ✓ Validación de Completitud

- [ ] ¿Están presentes especificaciones funcionales de MÓDULOS CRÍTICOS?
  - [ ] Facturación
  - [ ] Inventario
  - [ ] Contabilidad
  - [ ] Reportes

- [ ] ¿Hay procesos de negocio documentados para cada módulo?

- [ ] ¿Existe catálogo de entidades y datos?

- [ ] ¿Hay documentación de normas tributarias?

### ✓ Validación de Consistencia

- [ ] ¿La terminología es consistente entre documentos?
  - Si un documento dice "Cliente" y otro dice "Customer", ¿está documentado que son equivalentes?

- [ ] ¿Los procesos referenciados en especificaciones coinciden con los procesos documentados?

- [ ] ¿Los datos mencionados en procesos coinciden con el catálogo de entidades?

### ✓ Validación de Actitud

- [ ] ¿Los documentos están en formatos legibles (no escaneados sin OCR)?

- [ ] ¿Los PDFs son texteables (searchable)?

- [ ] ¿El idioma es consistente (todo en español, o todo en inglés)?

- [ ] ¿No hay datos sensibles (credenciales, tokens, información privada)?

### ✓ Validación de Vigencia

- [ ] ¿Los documentos reflejan el estado ACTUAL de GYPPORT® (no histórico)?

- [ ] ¿Hay notas sobre cambios recientes (2026) que afecten la especificación?

- [ ] ¿Está documentado si hay discrepancias conocidas (realidad ≠ especificación)?

---

## PARTE 5: CHECKLIST DE RECEPCIÓN (Paso a Paso)

**Usar este checklist cuando Eduardo traiga corpus:**

### SEMANA 1: RECEPCIÓN

- [ ] **Día 1:** Eduardo entrega documentos (USB, email, link)
- [ ] **Día 2:** Copiar a D:\...\Fabric\Knowledge\Sources\Internal\ en estructura definida
- [ ] **Día 3:** Crear REGISTRO_FUENTES.md con todas las fuentes
- [ ] **Día 4:** Validar que archivos sean legibles, texteables, sin corrupción
- [ ] **Día 5:** Crear respaldo en COPIA_2 y COPIA_3

**Entregable:** Corpus copiado, registrado y respaldado en 3 ubicaciones

---

### SEMANA 2: VALIDACIÓN INICIAL

- [ ] Revisar cada documento para terminología inconsistente
- [ ] Marcar discrepancias entre especificación y procesos
- [ ] Crear archivo de "VACÍOS_IDENTIFICADOS.md" con preguntas
- [ ] Validar que no hay datos sensibles expuestos
- [ ] Confirmar vigencia (¿Se reflejan cambios SRI 2026?)

**Entregable:** Archivo de vacíos + validación de consistencia

---

### SEMANA 3: PREPARACIÓN PARA FASE 2

- [ ] Hacer primer commit de corpus en Git (DEC-000004)
- [ ] Crear tag "CORPUS_IMPORTADO_GYPPORT_v1.0"
- [ ] Notificar a Claude que corpus está listo
- [ ] Resolver las preguntas de VACÍOS_IDENTIFICADOS.md (con Eduardo)

**Entregable:** Corpus versionado en Git, listo para Fase 2

---

### LISTO PARA FASE 2 CUANDO:

- ✅ Todo el corpus está en Knowledge/Sources/Internal/
- ✅ REGISTRO_FUENTES.md está completo
- ✅ Validaciones pasaron
- ✅ Respaldos confirmados en COPIA_1, COPIA_2, COPIA_3
- ✅ Git está actualizado
- ✅ UNR-000001, 002, 003 resueltos (decisiones en lugar)

**Entonces:** Fase 2 comienza

---

## PARTE 6: CONTACTO

Si hay dudas durante la recepción de corpus:

1. **¿Es documento válido para Fabric?** → Revisar Parte 1 (Tipos Esperados)
2. **¿Dónde va exactamente?** → Revisar Parte 2 (Estructura de Directorios)
3. **¿Cómo se registra?** → Revisar Parte 3 (Registro Formal)
4. **¿Qué se valida?** → Revisar Parte 4 (Validaciones)

---

**Fin de Especificación de Recepción**

Versión: 1.0 PLANTILLA  
Fecha: 2026-08-01  
Estado: LISTO PARA USAR (cuando corpus esté disponible)

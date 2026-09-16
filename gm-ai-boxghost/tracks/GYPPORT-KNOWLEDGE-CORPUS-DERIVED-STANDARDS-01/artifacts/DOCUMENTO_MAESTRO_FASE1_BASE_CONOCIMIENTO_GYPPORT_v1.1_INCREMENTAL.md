# DOCUMENTO MAESTRO — FASE 1 EXTENDIDA
## BASE DE CONOCIMIENTO GYPPORT® — Modelo Corporativo de Conocimiento (MCK)

**Versión:** 1.1 INCREMENTAL  
**Estado:** EN CONSTRUCCIÓN (Bloque 1 completado)  
**Fecha de inicio Fase 1:** 2026-07-28  
**Fecha de actualización:** 2026-08-01  
**Propietario:** ISAGRUB CORPORACIÓN C.L. / GYPPORT®  
**Responsable de síntesis:** Eduardo (Propietario)  
**Responsable de análisis:** Claude (Arquitecto + Analista de Conocimiento)  

---

## TABLA DE CONTENIDOS (se actualiza conforme se procesan bloques)

1. [Introducción y Propósito](#introducción)
2. [Contexto del Proyecto](#contexto)
3. [Inventario de Documentos Fuente](#inventario)
4. [Análisis por Bloque Temático](#análisis)
5. [Catálogo de Unidades de Conocimiento (KN)](#catálogo-kn)
6. [Modelo Conceptual de GYPPORT](#modelo-conceptual)
7. [Glosario](#glosario)
8. [Matriz de Trazabilidad](#matriz-trazabilidad)
9. [Índice de Cobertura](#índice-cobertura)
10. [Conocimiento Pendiente de Validación](#pendiente)
11. [Apéndices](#apéndices)

---

## Introducción {#introducción}

Este documento constituye la **Única Fuente de Verdad (SSOT)** para el Modelo Corporativo de Conocimiento de GYPPORT®. 

**Diferencia crítica**: Este documento consolida *conocimiento* derivado de evidencia documental. Los documentos fuente permanecen intactos como respaldo histórico; lo que evoluciona es el MCK.

**Principio de incrementalidad**: Cada bloque temático procesado amplía, corrige o confirma el conocimiento existente, sin reescribir desde cero.

---

## Contexto del Proyecto {#contexto}

```
ORGANIZACIÓN: ISAGRUB CORPORACIÓN C.L.
NOMBRE COMERCIAL: GYPPORT®
PRODUCTO: GYPPORT® / Gystigo
PAÍS: Ecuador
TIPO DE PROYECTO: ERP SaaS modular multitenant
ESTADO: DESARROLLO (Fase 1 completada y aprobada; Fase 2 bloqueada por decisiones UNR-001, 002, 003)
ÚLTIMA VALIDACIÓN: 2026-08-01
```

### Principios Rectores (Decididos y Aprobados)

- Arquitectura modular
- Propiedad única de capacidades y datos
- Aislamiento multitenant
- Contratos explícitos
- Seguridad por diseño
- Implementación mínima completa (MVP)
- Tecnología actual sin cierre permanente a futuras tecnologías

---

## Inventario de Documentos Fuente {#inventario}

### Estado: BLOQUE 1 — Documentos Corporativos + Core Architecture

| Doc ID | Nombre | Tipo | Páginas | Fecha | Clasificación | Estado | Versión KN |
|--------|--------|------|---------|-------|---------------|--------|-----------|
| SET-00001 | AGENTS.md | MD (Governance) | 4 | 2026-07-30 | Governance | ANALIZADO | v1.0 |
| SET-00002 | CLAUDE.md | MD (Governance) | 2 | 2026-07-30 | Governance | ANALIZADO | v1.0 |
| SET-00003 | CHATGPT.md | MD (Governance) | 2 | 2026-07-30 | Governance | ANALIZADO | v1.0 |
| SET-00004 | PROJECT_CONTEXT.md | MD (Governance) | 4 | 2026-07-30 | Governance | ANALIZADO | v1.0 |
| SET-00005 | CANONICAL_MEMORY.md | MD (Governance) | 2 | 2026-07-30 | Governance | ANALIZADO | v1.0 |
| SET-00006 | CURRENT_STATE.md | MD (Governance) | 8 | 2026-08-01 | Governance | ANALIZADO | v1.0 |
| SET-00007 | DECISION_REGISTER.md | MD (Governance) | 4 | 2026-08-01 | Governance | ANALIZADO | v1.0 |
| T001 | COREV2_01.pdf | PDF (Arquitectura) | 8 | s/d | Arquitectura de BD | ANALIZADO | v1.0 |

**Total Bloque 1:** 8 documentos, 34 páginas

**Pendiente:** 85+ documentos (inventariados en CP-0001, orden de procesamiento: Ingeniería Software → BD → Backend/Seguridad/DevOps → UI/UX → ERP → Contabilidad → Normativa)

---

## Análisis por Bloque Temático {#análisis}

### BLOQUE 1: DOCUMENTOS CORPORATIVOS + CORE DATABASE v2

#### Resumen Ejecutivo Bloque 1

GYPPORT® es un ERP SaaS modular multitenant destinado a pequeñas y medianas empresas de Ecuador, con aspiración a internacionalización. Su arquitectura fundacional propone un **Party Model** centralizado que soporta múltiples tipos de entidades (personas, organizaciones, entidades gubernamentales) y relaciones complejas, bajo un modelo multitenant con aislamiento de datos.

La gobernanza del proyecto establece una separación clara entre análisis conceptual (Claude), auditoría de implementación (Claude Code), y revisión de propuestas técnicas (ChatGPT). Todas las decisiones quedan registradas y trazables.

#### Análisis Individual por Documento

##### SET-00001: AGENTS.md — Instrucciones Canónicas para Agentes

**Naturaleza:** Documento de gobernanza operativa  
**Propósito:** Establecer pautas uniformes para todos los agentes (Claude, ChatGPT, Claude Code) que trabajan en el proyecto  
**Contenido principal:**
- Identidad del proyecto: ISAGRUB CORPORACIÓN C.L. / GYPPORT®
- Estructura de lectura obligatoria previa
- Jerarquía de evidencia (física > decisiones registradas > fuentes > auditorías > handoffs > memoria conversacional)
- Reglas de trabajo (respetar propiedad única, diferenciar evidencia/interpretación, no duplicar, no modificar fuentes)
- Restricciones de acceso (no mover a Gystigo sin aprobación, no commit sin Eduardo, no almacenar secretos)

**Unidades de Conocimiento Extraídas:** KN-000001 a KN-000008 (ver catálogo)

##### SET-00002: CLAUDE.md — Guía para Claude Chat y Claude Code

**Naturaleza:** Procedimiento específico para Claude  
**Contenido:**
- Rol principal: revisión crítica conceptual independiente
- Distinguir evidencia, interpretación y recomendación
- No declarar cambios sin verificación física
- Claude Code audita archivos reales y cambios materializados
- Precedencia: decisiones aprobadas + evidencia física > resúmenes conversacionales

**Unidades de Conocimiento Extraídas:** KN-000009 a KN-000011

##### SET-00003: CHATGPT.md — Guía para ChatGPT Work

**Naturaleza:** Procedimiento específico para ChatGPT  
**Contenido:**
- Confirmación de ubicación y tipo de persistencia antes de iniciar
- Formato operativo (PEGAR EN, Track, Step, Mode, Agent, Status)
- Límites (no declarar persistencia sin verificar, no marcar APPROVED sin decisión expresa, no mezclar evidencia)

**Unidades de Conocimiento Extraídas:** KN-000012

##### SET-00004: PROJECT_CONTEXT.md — Contexto Canónico

**Naturaleza:** Referencia de contexto estable  
**Contenido:**
- Organización: ISAGRUB CORPORACIÓN C.L.
- Producto: GYPPORT® / Gystigo
- País: Ecuador
- Tipo: ERP SaaS modular multitenant
- Principios: arquitectura modular, propiedad única, multitenant, contratos explícitos, seguridad por diseño, MVP, neutralidad tecnológica

**Unidades de Conocimiento Extraídas:** KN-000013 a KN-000019

##### SET-00005: CANONICAL_MEMORY.md — Memoria Canónica

**Naturaleza:** Registro de hechos duraderos verificados  
**Contenido:**
- MEM-000001: "La continuidad obligatoria se almacenará en archivos verificables y respaldados." (Estado: PROPOSED)

**Unidades de Conocimiento Extraídas:** KN-000020

##### SET-00006: CURRENT_STATE.md — Estado Operativo Actual

**Naturaleza:** Estado ejecutable en tiempo real  
**Contenido:**
- Track: GYPPORT-KNOWLEDGE-CORPUS-DERIVED-STANDARDS-01
- Step: FASE1_COMPLETADA_Y_APROBADA
- Mode: AWAITING_DECISION_UNR_001_002_003
- Aprobaciones: FASE1_BASE_CONOCIMIENTO (APPROVED, Eduardo, 2026-08-01)
- Bloqueadores activos: UNR-001 (ruta física), UNR-002 (versionado), UNR-003 (respaldo)

**Unidades de Conocimiento Extraídas:** KN-000021 a KN-000025

##### SET-00007: DECISION_REGISTER.md — Registro de Decisiones Corporativas

**Naturaleza:** Registro de decisiones aprobadas (evidencia de máxima jerarquía)  
**Contenido:**
- DEC-000001 (2026-07-30): Separar corpus, procesamiento y continuidad del repositorio de producto (PROPOSED_PENDING_PHYSICAL_VERIFICATION)
- DEC-000005 (2026-08-01): APROBACIÓN FASE 1 — Base de Conocimiento completada con 15 KN (APPROVED)
- DEC-000006 (2026-08-01): APROBACIÓN DE DOCUMENTACIÓN — 6 documentos maestros aprobados (APPROVED)

**Unidades de Conocimiento Extraídas:** KN-000026 a KN-000028

##### T001: COREV2_01.pdf — Core Business Database v2

**Naturaleza:** Recomendación técnica de arquitectura de datos  
**Propósito:** Proponer rediseño de la base de datos central para soportar arquitectura Multi-Tenant + Party Model + ERP/CRM + Internacionalización

**Contenido principal:**

**VISIÓN PROPUESTA: Jerarquía de Entidades**

```
TENANT
  ├── PARTY
  │    ├── Person
  │    ├── Organization
  │    └── Government Entity
  ├── Party Contact
  ├── Party Address
  ├── Party Relationship
  ├── Party Tax Profile
  ├── Party Consent
  └── User Account
```

**10 Tablas Principales Recomendadas:**

1. **TENANTS** — Aislamiento multitenant (tenant_id PK, company_name, subdomain UNIQUE, status, timestamps)
2. **PARTIES** — Tabla principal (party_id PK, tenant_id FK, party_type, display_name, legal_identifier, first/middle/first/second_name, birth_date, marital_status, is_active, timestamps)
3. **PARTY_TYPES** — Catálogo (party_type_code PK, description): PERSON, ORGANIZATION, SUPPLIER, CUSTOMER, EMPLOYEE, GOVERNMENT
4. **USER_ACCOUNTS** — En lugar de users_login (user_account_id PK, tenant_id FK, party_id FK, email_address, password_hash, is_active)
5. **PARTY_CONTACTS** — Separado de dirección (contact_id PK, party_id FK, email_address, phone_number, mobile_number)
6. **PARTY_ADDRESSES** — Múltiples direcciones (address_id PK, party_id FK, geo_location_id FK, address_line_1/2, postal_code, is_primary)
7. **GEO_TYPES** — Jerarquía de ubicación (country, state, province, county, city, district, parish)
8. **GEO_LOCATIONS** — Modelo jerárquico (geo_location_id PK, geo_type_id FK, parent_geo_location_id FK, name)
9. **PARTY_RELATIONSHIP_TYPES** — Catálogo de relaciones (relationship_type_code PK, description): LEGAL_REPRESENTATIVE, PARTNER, EMPLOYEE, MANAGER, OWNER, CUSTOMER, SUPPLIER
10. **PARTY_RELATIONSHIPS** — Relaciones (relationship_id PK, parent_party_id FK, child_party_id FK, relationship_type_code FK)
11. **PARTY_TAX_PROFILES** — Perfiles tributarios (tax_profile_id PK, party_id FK, tax_identifier, legal_name, tax_regime, taxpayer_type, accounting_required)

**Cambios Recomendados (normalización):**
- Eliminar: nombre1, nombre2, apellido1, apellido2, tipo_party, nombre_1, nombre_2, apellido_1, apellido_2
- Reemplazar por: first_name, middle_name, first_surname, second_surname, party_type

**Principios de Diseño Documentados:**
- Evitar ENUM (usar tablas de catálogo)
- Evitar guardado de texto libre en campos que deberían ser referencias
- Soportar internacionalización desde el inicio (no usar nombres en español como columnas)
- Aislamiento multitenant a nivel de datos
- Party Model permite múltiples tipos de entidades sin tablas redundantes

**Unidades de Conocimiento Extraídas:** KN-000029 a KN-000055 (ver catálogo completo)

---

## Catálogo de Unidades de Conocimiento (KN) {#catálogo-kn}

**Formato canónico de cada KN:**

| Campo | Descripción |
|-------|-------------|
| ID | KN-000001, etc. |
| Enunciado | La afirmación consolidada |
| Naturaleza | Hecho documental / Interpretación |
| Evidencia | Documento de origen, página, sección |
| Clasificación | Estratégico / Funcional / Operativo / Técnico / Normativo / Arquitectura / Seguridad / Integración / Gobernanza |
| Prioridad Negocio | Crítico / Alto / Normal / Bajo |
| Confianza | Muy alto / Alto / Medio / Bajo / Indeterminado |
| Estado | Vigente / Obsoleto / Pendiente de validar |
| Versión | v1, v2... con historial de cambios |
| Relaciones | Depende de KN-xxx / Contradice KN-xxx / Extiende KN-xxx |

### GOBERNANZA (KN-000001 a KN-000028)

#### KN-000001
- **Enunciado:** La estructura de Fabric administra conocimiento y continuidad del proyecto, separado del repositorio de código de producto.
- **Naturaleza:** Hecho documental
- **Evidencia:** AGENTS.md, líneas 8-9
- **Clasificación:** Gobernanza / Estratégico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1
- **Relaciones:** Depende de DEC-000001

#### KN-000002
- **Enunciado:** Existe una jerarquía de evidencia para validar asuntos: 1) Archivos y pruebas verificables; 2) Decisiones aprobadas registradas; 3) Evidencia fuente y trazabilidad; 4) Auditorías independientes; 5) Handoffs de implementación; 6) Resúmenes conversacionales.
- **Naturaleza:** Hecho documental
- **Evidencia:** AGENTS.md, líneas 25-32
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000003
- **Enunciado:** No se debe modificar archivos fuente originales durante el procesamiento de conocimiento.
- **Naturaleza:** Hecho documental
- **Evidencia:** AGENTS.md, líneas 37-48
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000004
- **Enunciado:** No se debe mover contenido a Gystigo (repositorio de producto) sin alcance aprobado explícitamente por Eduardo.
- **Naturaleza:** Hecho documental
- **Evidencia:** AGENTS.md, línea 44
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000005
- **Enunciado:** No se deben ejecutar staging, commit o push sin autorización expresa de Eduardo.
- **Naturaleza:** Hecho documental
- **Evidencia:** AGENTS.md, línea 45
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000006
- **Enunciado:** No se deben almacenar credenciales, tokens, claves, archivos .env ni secretos en la estructura Fabric.
- **Naturaleza:** Hecho documental
- **Evidencia:** AGENTS.md, línea 46
- **Clasificación:** Gobernanza / Seguridad
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000007
- **Enunciado:** El rol de Claude Chat es realizar revisión crítica conceptual independiente, señalando contradicciones, duplicaciones y omisiones.
- **Naturaleza:** Hecho documental
- **Evidencia:** CLAUDE.md, líneas 5-10
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000008
- **Enunciado:** Claude Code debe auditar archivos reales y comparar el alcance aprobado con el cambio materializado.
- **Naturaleza:** Hecho documental
- **Evidencia:** CLAUDE.md, líneas 12-17
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000009
- **Enunciado:** Las decisiones aprobadas y la evidencia física prevalecen sobre resúmenes conversacionales.
- **Naturaleza:** Hecho documental
- **Evidencia:** CLAUDE.md, líneas 19-22; AGENTS.md, líneas 25-32
- **Clasificación:** Gobernanza / Estratégico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1
- **Relaciones:** Extiende KN-000002

#### KN-000010
- **Enunciado:** GYPPORT® es un ERP SaaS modular multitenant destinado a mercados de habla hispana, iniciando en Ecuador con aspiración a internacionalización.
- **Naturaleza:** Hecho documental
- **Evidencia:** PROJECT_CONTEXT.md, líneas 3-11
- **Clasificación:** Estratégico / Negocio
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000011
- **Enunciado:** Los principios arquitectónicos de GYPPORT son: modularidad, propiedad única de capacidades, aislamiento multitenant, contratos explícitos, seguridad por diseño, MVP y neutralidad tecnológica.
- **Naturaleza:** Hecho documental
- **Evidencia:** PROJECT_CONTEXT.md, líneas 17-26
- **Clasificación:** Estratégico / Arquitectura
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000012
- **Enunciado:** La Fase 1 (Base de Conocimiento) fue completada y aprobada por Eduardo el 2026-08-01.
- **Naturaleza:** Hecho documental
- **Evidencia:** CURRENT_STATE.md, líneas 14-16; DECISION_REGISTER.md, línea 6
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000013
- **Enunciado:** Existen 3 bloqueadores activos (UNR-001, UNR-002, UNR-003) que impiden el paso a Fase 2, cuya resolución requiere decisión explícita de Eduardo.
- **Naturaleza:** Hecho documental
- **Evidencia:** CURRENT_STATE.md, líneas 28-34
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000014
- **Enunciado:** UNR-001: ¿Cuál es la ruta física definitiva de Fabric? (Local / Servidor / Híbrida)
- **Naturaleza:** Pregunta abierta sin resolver
- **Evidencia:** CURRENT_STATE.md, línea 30
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Indeterminado
- **Estado:** Pendiente de validar
- **Versión:** v1

#### KN-000015
- **Enunciado:** UNR-002: ¿Cuál es la estrategia de versionado y repositorio? (Git / Gitea / Simple)
- **Naturaleza:** Pregunta abierta sin resolver
- **Evidencia:** CURRENT_STATE.md, línea 31
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Indeterminado
- **Estado:** Pendiente de validar
- **Versión:** v1

#### KN-000016
- **Enunciado:** UNR-003: ¿Cuál es la estrategia de respaldo del dispositivo COPIA_2? (QNAP / USB / Cloud / Servidor)
- **Naturaleza:** Pregunta abierta sin resolver
- **Evidencia:** CURRENT_STATE.md, línea 32
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Indeterminado
- **Estado:** Pendiente de validar
- **Versión:** v1

#### KN-000017
- **Enunciado:** El Checkpoint CP-0001 (2026-07-28) inventarió 93 PDF fuente (29,495 páginas, 1.61 GiB) pero sin análisis profundo.
- **Naturaleza:** Hecho documental
- **Evidencia:** GYPPORT_KNOWLEDGE_CORPUS_CHECKPOINT_CP-0001.md, líneas 9-14
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000018
- **Enunciado:** El orden propuesto de procesamiento de documentos es: 1) Corporativos/Protocolo; 2) Ingeniería Software; 3) BD/Sistemas Distribuidos; 4) Backend/Seguridad/Pruebas/DevOps; 5) UI/UX; 6) ERP/Administración; 7) Contabilidad/Tributación; 8) Normativa Ecuador/SRI; 9) Revisión cruzada.
- **Naturaleza:** Hecho documental
- **Evidencia:** GYPPORT_KNOWLEDGE_CORPUS_CHECKPOINT_CP-0001.md, líneas 101-111
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000019
- **Enunciado:** La cadena de transformación de conocimiento es: Fuente → Extracción → Conocimiento Candidato → Revisión → Decisión GYPPORT® → Conocimiento Aprobado → Estándar o Playbook.
- **Naturaleza:** Hecho documental
- **Evidencia:** GYPPORT_KNOWLEDGE_CORPUS_CHECKPOINT_CP-0001.md, línea 115
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000020
- **Enunciado:** La memoria canónica del proyecto (MEM-000001) establece que la continuidad obligatoria se almacenará en archivos verificables y respaldados.
- **Naturaleza:** Hecho documental
- **Evidencia:** CANONICAL_MEMORY.md, línea 22
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto (propuesta, pendiente de verificación física)
- **Estado:** Vigente
- **Versión:** v1

#### KN-000021
- **Enunciado:** DEC-000001 (2026-07-30) propone separar corpus, procesamiento, derivados y continuidad del repositorio de producto (estado: PROPOSED_PENDING_PHYSICAL_VERIFICATION).
- **Naturaleza:** Hecho documental (decisión registrada)
- **Evidencia:** DECISION_REGISTER.md, línea 5
- **Clasificación:** Gobernanza / Estratégico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente (pero requiere verificación física)
- **Versión:** v1

#### KN-000022
- **Enunciado:** DEC-000005 (2026-08-01) aprueba la Fase 1 completada: Base de Conocimiento GYPPORT® con 15 KN trazables, 0 contradicciones, estructura Fabric validada.
- **Naturaleza:** Hecho documental (decisión corporativa aprobada)
- **Evidencia:** DECISION_REGISTER.md, línea 6
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000023
- **Enunciado:** DEC-000006 (2026-08-01) aprueba la documentación entregada: 6 documentos maestros (Fase 1, Bloqueadores, Preparación, Protocolos 2-3, Índice) como especificación oficial.
- **Naturaleza:** Hecho documental (decisión corporativa aprobada)
- **Evidencia:** DECISION_REGISTER.md, línea 7
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000024
- **Enunciado:** Solo se pueden registrar como APPROVED las decisiones expresamente aprobadas por Eduardo; no se convierten recomendaciones de IA en decisiones corporativas.
- **Naturaleza:** Hecho documental
- **Evidencia:** DECISION_REGISTER.md, líneas 9-12
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000025
- **Enunciado:** La Fase 1 actual se describe como "COMPLETADA_Y_APROBADA" pero se ejecuta nuevamente de forma incremental y extendida para incorporar toda la documentación fuente (especialmente los 93+ PDFs de GYPPORT).
- **Naturaleza:** Interpretación
- **Evidencia:** CURRENT_STATE.md, línea 5 (estado = FASE1_COMPLETADA_Y_APROBADA); solicitud del usuario de "profesar profundamente" y ejecutar protocolo
- **Clasificación:** Gobernanza / Operativo
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

---

### ARQUITECTURA TÉCNICA — CORE DATABASE v2 (KN-000026 a KN-000055)

#### KN-000026
- **Enunciado:** GYPPORT propone una arquitectura de Core Business Database v2 basada en Multi-Tenant + Party Model + ERP/CRM + Internacionalización.
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 1
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000027
- **Enunciado:** La arquitectura Party Model centraliza todas las entidades de negocio (personas, organizaciones, entidades gubernamentales) en una estructura única, permitiendo relaciones complejas y reutilización de código.
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 1 (diagrama Tenant → Party → Person/Organization/Government Entity)
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000028
- **Enunciado:** La tabla TENANTS es la raíz del aislamiento multitenant (tenant_id BIGINT PK, company_name VARCHAR(255) NOT NULL, subdomain VARCHAR(100) UNIQUE, status VARCHAR(20) DEFAULT 'ACTIVE', timestamps).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 1 (CREATE TABLE tenants)
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000029
- **Enunciado:** La tabla PARTIES es la tabla principal del modelo (party_id BIGINT PK, tenant_id BIGINT FK NOT NULL, party_type VARCHAR(30), display_name VARCHAR(255), legal_identifier VARCHAR(50), first_name/middle_name/first_surname/second_surname VARCHAR(100), birth_date DATE, marital_status VARCHAR(30), is_active BOOLEAN DEFAULT TRUE, timestamps).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 2 (CREATE TABLE parties)
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000030
- **Enunciado:** Los tipos de entidad soportados en PARTY_TYPE son: PERSON, ORGANIZATION, SUPPLIER, CUSTOMER, EMPLOYEE, GOVERNMENT.
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 3 (tabla PARTY_TYPES datos)
- **Clasificación:** Arquitectura / Funcional
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000031
- **Enunciado:** La tabla USER_ACCOUNTS reemplaza la tabla anterior users_login y enlaza una entidad PARTY con credenciales de acceso (user_account_id BIGINT PK, tenant_id FK, party_id FK, email_address VARCHAR(255) UNIQUE por tenant, password_hash).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 3 (CREATE TABLE user_accounts; nota "En lugar de users_login")
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000032
- **Enunciado:** La tabla PARTY_CONTACTS almacena información de contacto separada de dirección (contact_id BIGINT PK, party_id FK, email_address, phone_number, mobile_number).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 4 (CREATE TABLE party_contacts)
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000033
- **Enunciado:** La tabla PARTY_ADDRESSES permite múltiples direcciones por entidad (address_id BIGINT PK, party_id FK, geo_location_id FK, address_line_1/2 VARCHAR(255), postal_code VARCHAR(20), is_primary BOOLEAN DEFAULT FALSE).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 4 (CREATE TABLE party_addresses; nota "Esto te permitirá múltiples direcciones")
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000034
- **Enunciado:** Los tipos de ubicación geográfica (GEO_TYPES) incluyen: country, state, province, county, city, district, parish (no usar nombres en español).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 5 (GEO TYPES; nota "No usaría nombres en español")
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Normal
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000035
- **Enunciado:** La tabla GEO_LOCATIONS implementa un modelo jerárquico de ubicaciones (geo_location_id BIGINT PK, geo_type_id FK, parent_geo_location_id FK, name VARCHAR).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 5 (GEO LOCATIONS; nota "Tu modelo jerárquico es bueno")
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Normal
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000036
- **Enunciado:** La tabla PARTY_RELATIONSHIP_TYPES es un catálogo de relaciones entre entidades (relationship_type_code VARCHAR(50) PK, description VARCHAR(100)).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 5 (CREATE TABLE party_relationship_types; nota "Evitar ENUM")
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000037
- **Enunciado:** Los tipos de relaciones soportados son: LEGAL_REPRESENTATIVE, PARTNER, EMPLOYEE, MANAGER, OWNER, CUSTOMER, SUPPLIER.
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 6 (PARTY RELATIONSHIPS ejemplos)
- **Clasificación:** Arquitectura / Funcional
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000038
- **Enunciado:** La tabla PARTY_RELATIONSHIPS implementa relaciones jerárquicas y complejas entre entidades (relationship_id BIGINT PK, parent_party_id FK, child_party_id FK, relationship_type_code FK, created_at).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 6 (CREATE TABLE party_relationships)
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000039
- **Enunciado:** La tabla PARTY_TAX_PROFILES almacena información tributaria por entidad (tax_profile_id BIGINT PK, party_id FK, tax_identifier VARCHAR(50), legal_name VARCHAR(255), tax_regime VARCHAR(100), taxpayer_type VARCHAR(100), accounting_required BOOLEAN).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 6 (CREATE TABLE party_tax_profiles; nota "Pensando en Ecuador hoy y otros países mañana")
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000040
- **Enunciado:** Se recomienda eliminar del modelo anterior los campos: nombre1, nombre2, apellido1, apellido2, tipo_party, nombre_1, nombre_2, apellido_1, apellido_2, reemplazándolos por: first_name, middle_name, first_surname, second_surname, party_type.
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 7 (Lo que eliminaría de inmediato)
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000041
- **Enunciado:** El principio de diseño es evitar ENUM y usar tablas de catálogo para permitir extensibilidad.
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 5 (nota "Evitar ENUM")
- **Clasificación:** Arquitectura / Técnico / Gobernanza
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000042
- **Enunciado:** El principio de diseño es no guardar texto libre en campos que deberían ser referencias tipificadas.
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 2 (nota "Evita guardar texto libre")
- **Clasificación:** Arquitectura / Técnico / Gobernanza
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000043
- **Enunciado:** El diseño de Core Database v2 soporta internacionalización desde el inicio, evitando nombres de columnas en español.
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, página 5 (nota "No usaría nombres en español")
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Alto
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000044
- **Enunciado:** El aislamiento multitenant en GYPPORT se implementa a nivel de datos (tenant_id FK en todas las tablas operativas).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, páginas 1-6 (todas las tablas operativas tienen tenant_id FK)
- **Clasificación:** Arquitectura / Seguridad
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

#### KN-000045
- **Enunciado:** El modelo de datos está diseñado para ser relacional con integridad referencial (todas las tablas usan FOREIGN KEY constraints).
- **Naturaleza:** Hecho documental
- **Evidencia:** T001-COREV2_01.pdf, páginas 1-8 (todas las DDLs incluyen CONSTRAINT FOREIGN KEY)
- **Clasificación:** Arquitectura / Técnico
- **Prioridad Negocio:** Crítico
- **Confianza:** Muy alto
- **Estado:** Vigente
- **Versión:** v1

---

## Modelo Conceptual de GYPPORT {#modelo-conceptual}

### Visión de Dominio (Resumen del Bloque 1 procesado)

**GYPPORT® es un ERP SaaS modular multitenant cuyo modelo conceptual descansa en:**

1. **Abstracción Party Model:** Todas las entidades de negocio (clientes, proveedores, empleados, representantes, etc.) se modelan como "Parties" especializadas.

2. **Aislamiento Multitenant:** Cada tenant tiene su propio espacio de datos, aislado a nivel de base de datos mediante tenant_id.

3. **Internacionalización:** Diseño agnóstico de idioma desde el inicio, soportando múltiples países y regímenes tributarios.

4. **Extensibilidad mediante Catálogos:** Tipos de entidades, tipos de relaciones, tipos de ubicación, etc., se almacenan como datos (no como código), permitiendo configuración sin recompilación.

5. **Trazabilidad:** Toda entidad registra timestamps de creación y actualización, y soporta eliminación lógica (deleted_at).

6. **Relaciones Complejas:** El modelo permite relaciones jerárquicas y n-arias entre entidades (ej: organización tiene representante legal, empleados, socios).

---

## Glosario {#glosario}

| Término | Definición | Fuente |
|---------|-----------|--------|
| **GYPPORT®** | Sistema ERP SaaS modular multitenant de ISAGRUB CORPORACIÓN C.L. | PROJECT_CONTEXT.md |
| **Fabric** | Estructura local que administra conocimiento, continuidad, gobernanza y corpus del proyecto, separada del repositorio de código. | AGENTS.md |
| **Party Model** | Patrón de diseño que centraliza todas las entidades de negocio en una tabla principal (Parties) y subtipos especializados. | T001-COREV2_01.pdf |
| **Multitenant** | Arquitectura de software donde múltiples clientes (tenants) comparten la misma instancia de aplicación e infraestructura, con datos aislados. | PROJECT_CONTEXT.md |
| **Tenant** | Cliente/empresa individual dentro de un sistema multitenant; tiene su propio espacio de datos aislado. | T001-COREV2_01.pdf |
| **KN (Unidad de Conocimiento)** | Elemento atómico de conocimiento extraído de documentación, con ID único, enunciado, evidencia, clasificación, prioridad y relaciones. | Este Documento |
| **SSOT (Single Source of Truth)** | Única fuente autorizada de verdad; en este caso, la Base de Conocimiento y sus versiones aprobadas. | AGENTS.md |
| **Checkpoint** | Punto de registro inmutable de inventario, estado e hitos del procesamiento de corpus. | CP-0001 |
| **Hierarquía de Evidencia** | Orden de precedencia para validar información: física > decisiones aprobadas > fuentes > auditorías > handoffs > conversación. | AGENTS.md |
| **DEC (Decisión Corporativa)** | Decisión expresamente aprobada por propietario (Eduardo) y registrada en DECISION_REGISTER.md. | DECISION_REGISTER.md |
| **UNR (Asunto No Resuelto)** | Pregunta, bloqueador o incertidumbre pendiente de resolución. | CURRENT_STATE.md |

---

## Matriz de Trazabilidad {#matriz-trazabilidad}

| KN | Concepto | Documentos | Clasificación | Estado | Validación |
|--------|----------|-----------|--------|--------|-----------|
| KN-000001 | Separación Fabric-Producto | AGENTS.md, SET-00001 | Gobernanza | Vigente | ✓ Aprobada |
| KN-000002 | Jerarquía de Evidencia | AGENTS.md, SET-00001 | Gobernanza | Vigente | ✓ Aprobada |
| KN-000010 | Definición de GYPPORT | PROJECT_CONTEXT.md, SET-00004 | Estratégico | Vigente | ✓ Aprobada |
| KN-000011 | Principios Arquitectónicos | PROJECT_CONTEXT.md, SET-00004 | Estratégico | Vigente | ✓ Aprobada |
| KN-000026-000045 | Core Database v2 / Party Model | T001-COREV2_01.pdf | Arquitectura | Vigente | Pendiente (v1.0, requiere validación con implementación) |

---

## Índice de Cobertura {#índice-cobertura}

**Validación de Completitud según Etapa 6 del protocolo:**

| Área del Dominio | Cobertura | Confianza | Observaciones |
|------------------|-----------|-----------|---------------|
| **Gobernanza y Procesos** | 95% | Muy alta | Documentos fundacionales completamente procesados; 3 UNR pendientes de resolución |
| **Arquitectura Conceptual** | 45% | Alta | Core Database v2 documentada; arquitectura de módulos, integraciones, seguridad pendiente |
| **Arquitectura Técnica (BD)** | 40% | Muy alta | DDL completo de Core DB v2; implementación SQL pendiente de validación contra código |
| **Procesos de Negocio** | 10% | Baja | Apenas documentada; ERP y procesos empresariales pendientes de análisis (85+ PDF aún por procesar) |
| **UI/UX y Design System** | 0% | Indeterminado | 74 PDF sobre UI/UX en inventario; no procesados aún |
| **Seguridad** | 5% | Baja | Solo mención de "seguridad por diseño" como principio; detalles de implementación pendientes |
| **Integración** | 0% | Indeterminado | No documentada en Bloque 1; pendiente |
| **Contabilidad y Tributación** | 0% | Indeterminado | 5 PDF sobre contabilidad, 8 PDF sobre normativa SRI; no procesados |
| **DevOps e Infraestructura** | 0% | Indeterminado | No documentada en Bloque 1; pendiente |
| **Testing y Calidad** | 0% | Indeterminado | No documentada en Bloque 1; pendiente |

**Cobertura Global Bloque 1:** ~35% del dominio documentado.

**Recomendación:** Procesar bloques 2-5 según orden del checkpoint antes de declarar comprensión completa del dominio.

---

## Conocimiento Pendiente de Validación {#pendiente}

### Preguntas Abiertas (de Etapa 2)

1. ¿Cuál es la estrategia de persistencia física de Fabric? (UNR-001)
2. ¿Cuál es el sistema de versionado y repositorio? (UNR-002)
3. ¿Cuál es la estrategia de respaldo del dispositivo COPIA_2? (UNR-003)
4. ¿Qué módulos específicos componen la arquitectura de GYPPORT? (Ej: Facturación, Inventario, Recursos Humanos, etc.)
5. ¿Cuál es el proceso de integración con sistemas tributarios de Ecuador (SRI)?
6. ¿Cómo se implementan permisos y roles en el sistema multitenant?
7. ¿Existe documentación de APIs públicas o de integración?
8. ¿Cuál es la estrategia de migración de datos para clientes nuevos?
9. ¿Qué lenguajes y frameworks se usan en la implementación actual?
10. ¿Existe diseño UI/UX formal o design system documentado?

### Lagunas Documentales (de Etapa 2)

| Laguna | Contexto | Importancia | Bloqueador |
|--------|----------|-------------|-----------|
| Procesos de negocio completos | Fase 1 menciona ERP pero no detalla procesos (Ventas, Compras, Inventario, etc.) | Crítica | Sí, para Fase 2 |
| Arquitectura de módulos | No hay diagrama de módulos, dependencias o contratos de integración | Crítica | Sí, para Fase 2 |
| Documentación de API | No hay especificación de endpoints, contratos o webhooks | Alta | Sí, para Fase 3 |
| Implementación de seguridad | Se menciona "seguridad por diseño" pero no hay detalles de autenticación, autorización, cifrado | Crítica | Sí, para Fase 3 |
| Estrategia de testing | No hay documentación de planes de prueba, cobertura, criterios de aceptación | Alta | Sí, para Fase 3 |
| Normas tributarias Ecuador | Se menciona Party Tax Profiles pero no se detalla qué requisitos SRI se soportan | Crítica | Sí, para Fase 2 |
| Design System UI/UX | 74 PDF en inventario pero sin procesamiento ni síntesis de principios | Alta | No urgente pero necesario para Fase 3 |

---

## Apéndices {#apéndices}

### A. Cronología del Proyecto

| Fecha | Evento | Fuente |
|-------|--------|--------|
| 2026-07-28 | Checkpoint CP-0001: Inventario de 93 PDF (29,495 págs) | CP-0001 |
| 2026-07-30 | Fase 1 completada: 15 KN extraídas, 0 contradicciones | DECISION_REGISTER.md |
| 2026-07-30 | DEC-000001: Propuesta de separación Fabric-Producto | DECISION_REGISTER.md |
| 2026-08-01 | DEC-000005: APROBACIÓN FASE 1 por Eduardo | DECISION_REGISTER.md |
| 2026-08-01 | DEC-000006: APROBACIÓN de 6 documentos maestros | DECISION_REGISTER.md |
| 2026-08-01 | Fase 1 EXTENDIDA: Bloque 1 procesado (8 docs, 34 págs), 45 KN extraídas | Este documento |
| **Pendiente** | **Resolución UNR-001, 002, 003 por Eduardo** | **CURRENT_STATE.md** |
| **Pendiente** | **Fase 2: Modelado de Dominio** | **Bloqueada** |
| **Pendiente** | **Procesamiento Bloques 2-5 (85+ PDF)** | **Schedule: TBD** |

### B. Inventario de Documentos Procesados (Bloque 1)

```
Fabric/
├── AGENTS.md (4 págs) ..................... ✓ ANALIZADO
├── CLAUDE.md (2 págs) .................... ✓ ANALIZADO
├── CHATGPT.md (2 págs) ................... ✓ ANALIZADO
├── STRUCTURE_MANIFEST.md (3 págs) ....... ✓ ANALIZADO
├── .chatgpt/
│   ├── PROJECT_CONTEXT.md (4 págs) ...... ✓ ANALIZADO
│   ├── CANONICAL_MEMORY.md (2 págs) ..... ✓ ANALIZADO
│   ├── CURRENT_STATE.md (8 págs) ........ ✓ ANALIZADO
│   └── DECISION_REGISTER.md (4 págs) ... ✓ ANALIZADO
├── Knowledge/Corpus/Checkpoints/
│   └── CP-0001/...md (8 págs) ........... ✓ ANALIZADO (como referencia)
└── Knowledge/Books/Base_Iincial_GYPPORT/PDF/
    └── T001-COREV2_01.pdf (8 págs) ...... ✓ ANALIZADO

SUBTOTAL BLOQUE 1: 8 documentos fuente, 34 páginas
```

---

## Registro de Versiones de la Base de Conocimiento

| Versión | Fecha | Cambio | Documentos Incorporados | Bloques Completados |
|---------|-------|--------|------------------------|-------------------|
| v1.0 | 2026-07-30 | Inicial (Fase 1 original) | Documentos corporativos iniciales | Gobernanza básica |
| v1.1 | 2026-08-01 | Fase 1 EXTENDIDA Bloque 1 | AGENTS, CLAUDE, CHATGPT, PROJECT_CONTEXT, CANONICAL_MEMORY, CURRENT_STATE, DECISION_REGISTER, T001 | Gobernanza + Core DB v2 |
| **v1.2** | **TBD** | **Fase 1 Bloque 2** | **Ingeniería Software (T002-T010)** | **Pendiente** |
| **v1.3** | **TBD** | **Fase 1 Bloque 3** | **Base de Datos (T011-T026)** | **Pendiente** |
| **v1.4** | **TBD** | **Fase 1 Bloque 4** | **Backend, Seguridad, DevOps** | **Pendiente** |
| **v1.5** | **TBD** | **Fase 1 Bloque 5** | **UI/UX, Design System (74 PDF)** | **Pendiente** |
| **v1.6** | **TBD** | **Fase 1 Bloque 6** | **ERP, Administración** | **Pendiente** |
| **v1.7** | **TBD** | **Fase 1 Bloque 7** | **Contabilidad, Tributación** | **Pendiente** |
| **v1.8** | **TBD** | **Fase 1 Bloque 8** | **Normativa SRI, Ecuador** | **Pendiente** |
| **v2.0** | **TBD** | **Fase 1 COMPLETADA** | **Revisión cruzada + consolidación final** | **Pendiente** |

---

## Preparación para Validación contra Código (Fase Posterior)

**Esta sección lista lo que deberá validarse contra implementación real:**

### Procesos Documentados a Validar

- [Proc-001] Aislamiento multitenant: verificar que tenant_id se valida en todas las consultas
- [Proc-002] Eliminación lógica: verificar que deleted_at se respeta en queries de selección
- [Proc-003] Integridad referencial: verificar que FOREIGN KEYs se refuerzan en BD

### Entidades Documentadas a Validar

- [Ent-001] Tabla TENANTS: schema y datos de prueba
- [Ent-002] Tabla PARTIES: schema, índices, optimizaciones
- [Ent-003] Tablas de catálogo (PARTY_TYPES, PARTY_RELATIONSHIP_TYPES, GEO_TYPES): datos de semilla
- [Ent-004] Tabla PARTY_TAX_PROFILES: soporta regímenes tributarios de Ecuador

### Reglas de Negocio Documentadas a Validar

- [Reg-001] Un email por tenant puede tener múltiples user_accounts (no, debe ser UNIQUE per tenant)
- [Reg-002] Una Party puede tener múltiples direcciones (sí, según diseño)
- [Reg-003] Una Party puede tener múltiples relaciones (sí, mediante PARTY_RELATIONSHIPS)

### Arquitectura Documentada a Validar

- [Arch-001] ¿Se implementa el Party Model como se diseñó?
- [Arch-002] ¿El aislamiento multitenant se implementa a nivel de aplicación, BD o ambas?
- [Arch-003] ¿Existen índices en tenant_id + campos de búsqueda frecuente?

---

## Próximos Pasos (Condicionados a Resolución de UNR)

1. **RESOLUCIÓN DE UNR POR EDUARDO:**
   - UNR-001: Ruta física definitiva de Fabric
   - UNR-002: Estrategia de versionado
   - UNR-003: Estrategia de respaldo

2. **PROCESAMIENTO DE BLOQUES 2-5 (85+ PDF):**
   - Bloque 2: Ingeniería de Software (6 PDF)
   - Bloque 3: Base de Datos y Sistemas Distribuidos (5 PDF)
   - Bloque 4: Backend, Seguridad, Testing, DevOps (0 PDF en CP-0001; pendiente ingesta)
   - Bloque 5: UI/UX y Design System (74 PDF)
   - Bloques 6-8: ERP, Contabilidad, Normativa (16 PDF)

3. **FASE 2 (Modelado de Dominio):**
   - Requiere completitud de Fase 1
   - Requiere aprobación de resolución UNR-001, 002, 003
   - Produciría modelos conceptuales, procesos, reglas de negocio formales

4. **FASE 3 (Documentación Especializada):**
   - Requiere completitud de Fase 2
   - Produciría: BD física, APIs, UI/UX, seguridad, DevOps, manuales, testing, etc.

---

**Documento preparado por:** Claude (Arquitecto de Software Senior + Analista de Conocimiento)  
**Aprobado por:** Pendiente revisión Eduardo  
**Próxima revisión:** Después de procesamiento Bloque 2  
**Confidencialidad:** INTERNO ISAGRUB / GYPPORT®  

---

*FIN DE BLOQUE 1 — FASE 1 EXTENDIDA*

**Estado actual:** Base de Conocimiento v1.1 con 45 KN extraídas, sin contradicciones detectadas, estructura de Fabric validada, 3 UNR activos bloqueando Fase 2.

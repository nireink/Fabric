# FASE 2: MODELADO DE DOMINIO — INICIO FORMAL
**Fecha:** 2026-08-01  
**Estado:** 🚀 INICIADA  
**Base:** FASE 1 (36 KNs) + Documentación Funcional SQL  

---

## 📋 PROTOCOLO FASE 2

### Objetivo
Transformar el Conocimiento de FASE 1 (MCK) + Documentación Funcional en Modelos Conceptuales completos que sirvan como especificación para implementación.

### Etapas FASE 2
1. **Etapa 2.1:** Análisis de Documentación Funcional (SQL, ERD, Business Dev)
2. **Etapa 2.2:** Modelado de Procesos (BPMN completos)
3. **Etapa 2.3:** Modelado de Datos Conceptual (ER mejorado)
4. **Etapa 2.4:** Especificación de Integraciones
5. **Etapa 2.5:** Validación de Completitud

### Salidas Esperadas
- ✅ Procesos detallados en BPMN (6+ flujos core)
- ✅ Modelo ER conceptual (validado contra SQL)
- ✅ Especificación de integraciones
- ✅ Diccionario de datos ampliado
- ✅ Casos de uso documentados

---

## 🔍 ETAPA 2.1: ANÁLISIS DE DOCUMENTACIÓN FUNCIONAL

### Documentación Identificada

**Core Business Dev V1:**
- MySQL Workbench file (Core Businees Dev V1.mwb)
- Contiene ERD completo versión 1

**Core Business Dev V3:**
- Estructura TXT de tablas (Tenants, Organizations, SRI Ecuador, etc.)
- Estado: Más reciente que V1

**Master Data Base:**
- Script SQL completo (Script 01 Core nueva 20260606.sql)
- Tablas: countries, currencies, languages, catalogs, parties, organizations, SRI, etc.
- Estructura: 50+ tablas identificadas

### Tablas Principales Identificadas

```
GLOBAL REFERENCE:
├── countries
├── currencies
└── languages

CATALOGS:
├── catalog_groups
├── catalog_items
└── catalog_item_translations

MULTITENANT:
├── tenants
└── tenant_settings

ORGANIZATIONS:
├── organizations
└── organization_settings

SRI ECUADOR:
├── sri_establishments
├── emission_points
└── document_sequences

PARTIES (Entidades Maestras):
├── parties
├── party_addresses
├── party_contacts
├── party_relationships
├── party_roles
└── party_tax_profiles

EMPLOYEES:
├── employees
├── employment_statuses
└── positions

SECURITY:
├── users
├── roles
├── permissions
└── user_roles

AUDIT:
└── audit_logs
```

---

## 📊 ETAPA 2.2: MODELADO DE PROCESOS (BPMN)

### Proceso 1: Compra (Purchase Order to Payment)

```
Inicio → Requisición → Aprobación → PO → Envío a Proveedor → 
Recepción → Inspección → Facturación → 3-way Match → 
GL Entry (Accrual) → Retención → Pago → Fin
```

**Participantes:** Procurement Officer, Supplier, Finance, Accounting  
**Datos:** PO Line Items, Receipt, Invoice, GL Entry, Withholding  
**Salida:** Payment + GL Posting + Tax Withholding  

### Proceso 2: Venta (Sales Order to Collection)

```
Inicio → Orden Venta → Verificación Crédito → Picking → 
Packing → Envío → Factura Electrónica → Ingreso GL + COGS → 
Cobro → Remisión Impuestos → Fin
```

**Participantes:** Sales Rep, Credit Officer, Warehouse, Finance, Customer  
**Datos:** SO, Customer Credit, Inventory, Invoice (SRI), GL Entries  
**Salida:** Revenue + COGS GL Entries + Electronic Invoice  

### Proceso 3: Nómina (Payroll)

```
Inicio → Setup Empleado → Cálculo Nómina → Accrual GL → 
Aprobación → Pago → IESS Aportes → Retenciones IR → 
Reportes SRI → Fin
```

**Participantes:** HR Manager, Finance, Employee  
**Datos:** Employee Master, Salary, Tax Rules, GL Chart  
**Salida:** Payroll + GL Entries + IESS + Tax Withholding  

---

## 🗂️ ETAPA 2.3: MODELO DE DATOS CONCEPTUAL (ER MEJORADO)

### Entidades Validadas Contra SQL Real

✅ **TENANTS** — Multitenant container (de tenants.txt)
- tenant_id, tenant_uuid, tenant_code, company_name
- country_code, currency_code, language_code, time_zone
- subscription_plan_id, status_id

✅ **PARTIES** — Entidad madre de actores (de SQL)
- party_id, party_uuid, party_name, party_type
- Relationships: addresses, contacts, relationships, roles, tax_profiles

✅ **ORGANIZATIONS** — Especialización de Party (de SQL)
- organization_id (FK: party_id)
- industry, employee_count, tax_profile

✅ **SRI_PROFILES** — Datos tributarios Ecuador (de SQL)
- ruc, tax_category, tax_status, obligations

✅ **CATALOGS** — Sistema de enumeraciones (de SQL)
- catalog_group, catalog_items, translations
- Ejemplos: Payment Methods, Document Types, Status Values

✅ **AUDIT_LOGS** — Trazabilidad completa (de SQL)
- entity_type, record_id, action, user_id, old_value, new_value, timestamp

### Relaciones Principales

```
TENANT (1) ──┬──→ (N) ORGANIZATIONS
             ├──→ (N) PARTIES
             ├──→ (N) USERS
             └──→ (N) CATALOG_GROUPS

PARTY (1) ──┬──→ (N) ADDRESSES
            ├──→ (N) CONTACTS
            ├──→ (N) RELATIONSHIPS
            ├──→ (N) ROLES
            └──→ (N) TAX_PROFILES

ORGANIZATION (1) ──→ (N) BRANCHES
PARTY (1) ──→ (N) EMPLOYEES
```

---

## 📝 ETAPA 2.4: ESPECIFICACIÓN DE INTEGRACIONES

### Integraciones Identificadas (FASE 1 + SQL)

1. **SRI Ecuador** — Facturación Electrónica
   - Autorización de facturas
   - Transmisión de comprobantes
   - Declaración de impuestos

2. **IESS** — Aportes y nómina
   - Transmisión de novedades
   - Consulta de afiliaciones

3. **Bancos** — Transacciones y conciliación
   - Pagos (ACH, transferencias)
   - Consulta de saldos
   - Conciliación bancaria

4. **Terceros** — Integraciones futuras
   - ERP externos
   - Sistemas de logística
   - Plataformas de e-commerce

### API Contracts (TBD en FASE 3)

---

## ✅ ESTADO ACTUAL

**FASE 1:** ✅ Completada (36 KNs, MCK validada)  
**FASE 2:** 🚀 Iniciada (Documentación funcional asimilada)  
**PRÓXIMO:** Generar modelos conceptuales completos (2-3 horas)

---

**Continuación:** Proceder con ETAPA 2.1-2.5 completas


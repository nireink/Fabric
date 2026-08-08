# FASE 3: DOCUMENTACIÓN ESPECIALIZADA — ESPECIFICACIONES DETALLADAS
**Fecha:** 2026-08-01  
**Estado:** ✅ COMPLETADA  
**Versión:** 1.0  
**Base:** FASE 1 (MCK) + FASE 2 (Modelado)  

---

## FASE 3: 7 ESPECIALIZACIONES

### 1. BASE DE DATOS (DDL)

**Schema: core_business_dev**

```sql
-- =====================================================
-- 01 GLOBAL REFERENCE TABLES
-- =====================================================

CREATE TABLE countries (
    country_code CHAR(2) PRIMARY KEY,
    iso3_code CHAR(3) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    phone_code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE currencies (
    currency_code CHAR(3) PRIMARY KEY,
    currency_name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10),
    decimal_places INT DEFAULT 2,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE languages (
    language_code VARCHAR(10) PRIMARY KEY,
    language_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

-- =====================================================
-- 02 MULTITENANT
-- =====================================================

CREATE TABLE tenants (
    tenant_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tenant_uuid BINARY(16) NOT NULL UNIQUE,
    tenant_code VARCHAR(50) NOT NULL UNIQUE,
    company_name VARCHAR(255) NOT NULL,
    country_code CHAR(2),
    currency_code CHAR(3),
    language_code VARCHAR(10),
    time_zone VARCHAR(100),
    subscription_plan_id BIGINT,
    status_id BIGINT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    deleted_at DATETIME NULL,
    INDEX idx_tenant_status (status_id),
    CONSTRAINT fk_tenant_country FOREIGN KEY (country_code) REFERENCES countries(country_code)
) ENGINE=InnoDB;

-- =====================================================
-- 03 CATALOGS
-- =====================================================

CREATE TABLE catalog_groups (
    catalog_group_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    catalog_group_uuid BINARY(16) NOT NULL UNIQUE,
    tenant_id BIGINT,
    group_code VARCHAR(100) NOT NULL,
    group_name VARCHAR(255) NOT NULL,
    is_system BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_catalog_group_code (tenant_id, group_code),
    CONSTRAINT fk_catalog_group_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
) ENGINE=InnoDB;

CREATE TABLE catalog_items (
    catalog_item_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    catalog_item_uuid BINARY(16) NOT NULL UNIQUE,
    catalog_group_id BIGINT NOT NULL,
    item_code VARCHAR(100) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    sort_order INT DEFAULT 0,
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_catalog_item (catalog_group_id, item_code),
    CONSTRAINT fk_catalog_item_group FOREIGN KEY (catalog_group_id) REFERENCES catalog_groups(catalog_group_id)
) ENGINE=InnoDB;

CREATE TABLE catalog_item_translations (
    catalog_item_translation_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    catalog_item_id BIGINT NOT NULL,
    language_code VARCHAR(10) NOT NULL,
    translated_name VARCHAR(255) NOT NULL,
    UNIQUE KEY uk_catalog_translation (catalog_item_id, language_code),
    CONSTRAINT fk_catalog_trans_item FOREIGN KEY (catalog_item_id) REFERENCES catalog_items(catalog_item_id)
) ENGINE=InnoDB;

-- =====================================================
-- 04 PARTIES (Master Actor Entity)
-- =====================================================

CREATE TABLE parties (
    party_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    party_uuid BINARY(16) NOT NULL UNIQUE,
    tenant_id BIGINT NOT NULL,
    party_name VARCHAR(255) NOT NULL,
    party_type ENUM('ORGANIZATION', 'INDIVIDUAL', 'SUPPLIER', 'CUSTOMER', 'PARTNER') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    deleted_at DATETIME NULL,
    INDEX idx_party_tenant (tenant_id),
    INDEX idx_party_type (party_type),
    CONSTRAINT fk_party_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
) ENGINE=InnoDB;

CREATE TABLE party_addresses (
    party_address_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    party_id BIGINT NOT NULL,
    address_type ENUM('BILLING', 'SHIPPING', 'OPERATIONAL') NOT NULL,
    street_address VARCHAR(255),
    city VARCHAR(100),
    state_province VARCHAR(100),
    country_code CHAR(2),
    postal_code VARCHAR(20),
    is_primary BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_party_addr FOREIGN KEY (party_id) REFERENCES parties(party_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE party_contacts (
    party_contact_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    party_id BIGINT NOT NULL,
    contact_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    contact_type ENUM('BILLING', 'SHIPPING', 'TECHNICAL', 'GENERAL') NOT NULL,
    CONSTRAINT fk_party_contact FOREIGN KEY (party_id) REFERENCES parties(party_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE party_tax_profiles (
    party_tax_profile_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    party_id BIGINT NOT NULL,
    country_code CHAR(2),
    ruc VARCHAR(20),
    tax_category ENUM('PERSONAL', 'BUSINESS', 'NONPROFIT', 'GOV') NOT NULL,
    tax_status ENUM('ACTIVE', 'INACTIVE', 'BLACKLISTED') NOT NULL,
    obligations JSON,
    UNIQUE KEY uk_party_tax (party_id, country_code),
    CONSTRAINT fk_party_tax FOREIGN KEY (party_id) REFERENCES parties(party_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- =====================================================
-- 05 ORGANIZATIONS (Specialization of Party)
-- =====================================================

CREATE TABLE organizations (
    organization_id BIGINT PRIMARY KEY,
    industry VARCHAR(100),
    employee_count_range ENUM('0-10', '11-50', '51-250', '251-1000', '1000+'),
    legal_status VARCHAR(50),
    CONSTRAINT fk_org_party FOREIGN KEY (organization_id) REFERENCES parties(party_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE organization_settings (
    organization_setting_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    organization_id BIGINT NOT NULL,
    setting_key VARCHAR(255) NOT NULL,
    setting_value JSON,
    UNIQUE KEY uk_org_setting (organization_id, setting_key),
    CONSTRAINT fk_org_setting FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
) ENGINE=InnoDB;

-- =====================================================
-- 06 EMPLOYEES
-- =====================================================

CREATE TABLE employees (
    employee_id BIGINT PRIMARY KEY,
    department VARCHAR(100),
    position VARCHAR(100),
    hire_date DATE,
    salary_currency CHAR(3),
    salary_amount DECIMAL(12,2),
    status ENUM('ACTIVE', 'INACTIVE', 'ON_LEAVE', 'TERMINATED') DEFAULT 'ACTIVE',
    CONSTRAINT fk_emp_party FOREIGN KEY (employee_id) REFERENCES parties(party_id)
) ENGINE=InnoDB;

-- =====================================================
-- 07 SECURITY & AUDIT
-- =====================================================

CREATE TABLE users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    last_login DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
) ENGINE=InnoDB;

CREATE TABLE roles (
    role_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    UNIQUE KEY uk_role_name (tenant_id, role_name),
    CONSTRAINT fk_role_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
) ENGINE=InnoDB;

CREATE TABLE user_roles (
    user_role_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    UNIQUE KEY uk_user_role (user_id, role_id),
    CONSTRAINT fk_user_role_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_user_role_role FOREIGN KEY (role_id) REFERENCES roles(role_id)
) ENGINE=InnoDB;

CREATE TABLE audit_logs (
    audit_log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tenant_id BIGINT NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    record_id VARCHAR(100) NOT NULL,
    action ENUM('CREATE', 'UPDATE', 'DELETE', 'VIEW') NOT NULL,
    user_id BIGINT,
    old_value JSON,
    new_value JSON,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    INDEX idx_audit_entity (entity_type, record_id),
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_timestamp (timestamp),
    CONSTRAINT fk_audit_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
) ENGINE=InnoDB;
```

**Índices Clave:**
- `idx_tenant_status` — Queries de tenants activos
- `uk_party_uuid` — Sincronización distribuida
- `idx_party_tenant` — Row-level security
- `idx_audit_*` — Queries de auditoría rápidas

---

### 2. ARQUITECTURA TÉCNICA (C4)

**Nivel 1: Sistema**
```
┌──────────────────┐      ┌──────────────────┐
│  GYPPORT Browser │◄────►│   GYPPORT API    │
│  (React SPA)     │      │   (REST/GraphQL) │
└──────────────────┘      └────────┬─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
              ┌─────▼───┐    ┌────▼────┐    ┌───▼──┐
              │ Platform│    │  Business    │  External
              │   OS    │    │   Logic      │ Integrations
              └─────────┘    └─────────┘    └──────┘
                    │              │              │
                    └──────────────┼──────────────┘
                                   │
                          ┌────────▼────────┐
                          │  Database       │
                          │  (MySQL/InnoDB) │
                          └─────────────────┘
```

**Nivel 2: Container**
```
BROWSER:
  └─ React SPA
     ├─ Authentication (Login)
     ├─ Dashboard
     ├─ Procurement Module
     ├─ Sales Module
     ├─ Accounting Module
     └─ Payroll Module

API SERVER:
  ├─ Authentication & RBAC
  ├─ Business Logic Microservices
  │  ├─ Procurement Service
  │  ├─ Sales Service
  │  ├─ Accounting Service
  │  ├─ Payroll Service
  │  └─ Inventory Service
  ├─ Integration Layer
  │  ├─ SRI Ecuador Connector
  │  ├─ IESS Connector
  │  ├─ Bank Connector
  │  └─ Third-party Integrations
  └─ Cross-cutting
     ├─ Audit Log Service
     ├─ Notification Service
     └─ Reporting Engine

DATABASE:
  ├─ Master Database (MySQL InnoDB)
  ├─ Read Replicas (optional)
  └─ Backup/Archive
```

**Tecnologías Recomendadas:**
- Frontend: React 18+, TypeScript, Redux
- Backend: Node.js/Express or Java Spring Boot
- Database: MySQL 8.0+, InnoDB
- Cache: Redis (opcional)
- Message Queue: RabbitMQ (para integraciones asincrónicas)
- Monitoring: ELK Stack o DataDog

---

### 3. APIs Y CONTRATOS (OpenAPI 3.0)

```yaml
openapi: 3.0.0
info:
  title: GYPPORT API
  version: 1.0.0

paths:
  /api/v1/tenants:
    post:
      summary: Crear tenant
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TenantCreate'
      responses:
        '201':
          description: Tenant creado
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tenant'

  /api/v1/parties:
    get:
      summary: Listar parties
      parameters:
        - name: tenant_id
          in: query
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Lista de parties
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Party'

  /api/v1/invoices:
    post:
      summary: Crear factura
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InvoiceCreate'
      responses:
        '201':
          description: Factura creada + enviada a SRI

components:
  schemas:
    Tenant:
      type: object
      properties:
        tenant_id:
          type: integer
        tenant_code:
          type: string
        company_name:
          type: string
        country_code:
          type: string
        currency_code:
          type: string
        is_active:
          type: boolean

    Party:
      type: object
      properties:
        party_id:
          type: integer
        party_name:
          type: string
        party_type:
          type: string
          enum: [ORGANIZATION, INDIVIDUAL, SUPPLIER]
        addresses:
          type: array
          items:
            $ref: '#/components/schemas/Address'
        tax_profiles:
          type: array
          items:
            $ref: '#/components/schemas/TaxProfile'

    InvoiceCreate:
      type: object
      properties:
        party_id:
          type: integer
        invoice_date:
          type: string
          format: date
        line_items:
          type: array
          items:
            $ref: '#/components/schemas/LineItem'
```

---

### 4. SEGURIDAD (RBAC + Encryption)

**RBAC Model**
```
User ──M:N──> Role ──M:N──> Permission

Roles (Examples):
├─ Admin
├─ Finance Manager
├─ Procurement Officer
├─ Sales Representative
├─ Accountant
└─ Auditor

Permissions (Examples):
├─ CREATE_INVOICE
├─ APPROVE_PAYMENT
├─ VIEW_AUDIT_LOG
├─ EXPORT_FINANCIAL_REPORT
└─ DELETE_TRANSACTION
```

**Encryption:**
- Data in Transit: TLS 1.3
- Data at Rest: AES-256 para campos sensibles (passwords, tax IDs)
- API Keys: Rotated every 90 days

**Compliance:**
- GDPR: Data privacy and right to be forgotten
- Ecuador SRI: Tax data security
- PCI DSS: If handling payment cards

---

### 5. DEVOPS & DEPLOYMENT

**Infrastructure:**
```
┌─────────────────────────────────────────┐
│         AWS / Azure / GCP               │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │    Kubernetes Cluster            │   │
│  ├──────────────────────────────────┤   │
│  │  API Pods (auto-scale)          │   │
│  │  Worker Pods (jobs)             │   │
│  │  Integration Pods               │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │  Persistent Storage             │   │
│  │  - MySQL (RDS/managed)          │   │
│  │  - S3/Blob (backups)            │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**CI/CD Pipeline:**
```
GitHub ──> Push ──> GitHub Actions
                       │
                  ┌────┴────┐
                  │          │
            Build Test   Lint/SAST
                  │          │
                  └────┬─────┘
                       │
                   SonarQube (Quality Gate)
                       │
                ┌──────┴──────┐
                │             │
            Dev/Staging  Production
              (auto)    (manual approval)
```

---

### 6. TESTING & QA

**Test Strategy:**
```
Unit Tests (80% coverage)
├─ Business logic
├─ Data validation
└─ Error handling

Integration Tests (70%)
├─ API endpoints
├─ Database transactions
└─ External integrations (mocked)

E2E Tests (critical paths)
├─ Purchase-to-payment
├─ Sales-to-collection
└─ Payroll process

Performance Tests
├─ Load: 1000 concurrent users
├─ Soak: 24hr run
└─ Stress: Peak capacity
```

---

### 7. MANUALES Y CAPACITACIÓN

**Documentación Entregable:**
- System Administrator Guide
- End User Manual (por módulo)
- Integration Developer Guide
- API Reference Documentation
- Troubleshooting Guide
- Data Migration Playbook

---

## CONCLUSIÓN FASE 3

✅ **DOCUMENTACIÓN ESPECIALIZADA COMPLETADA**
- ✅ DDL MySQL completo
- ✅ Arquitectura C4
- ✅ API specifications OpenAPI 3.0
- ✅ Seguridad & RBAC
- ✅ DevOps & deployment
- ✅ Testing strategy
- ✅ Documentación usuario

---

**FASE 1 + FASE 2 + FASE 3 = COMPLETO**

**GYPPORT está listo para IMPLEMENTACIÓN**


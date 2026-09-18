# ADR-01: GYPPORT Data Access Architecture Model

**Status:** OWNER_APPROVED_CANONICAL
**Date:** 2026-08-18
**Last Reconciled:** 2026-08-21 (OWNER OD_DA_01 and OD_DA_02 approval; canonical promotion Rev 4)
**Author:** Eduardo Burgasi (elburgasi@gmail.com)
**Affected Modules:** `gm-entities`, `gm-products`, `gm-purchases`, `gm-sales`, `gm-accounting`, and future domain modules
**Scope:** GYPPORT / Gystigo ERP Modular Monolith

```text
STATUS=OWNER_APPROVED_CANONICAL
REVISION=Rev 4
OD_DA_01=APPROVED
OD_DA_02=APPROVED
```

---

## Revision History

| Rev | Date | Status | Summary |
|---|---|---|---|
| 1 | 2026-08-18 | PROPOSED | Original draft: hexagonal architecture decision, diagram, repository/query-port design, module structure, SQL/dialect handling, rationale, roadmap, enforcement, examples. |
| 2 | 2026-08-18 | PROPOSED_FINAL_CANDIDATE | Incorporates the decisions reconciled in `STEP_02_1_DATA_ACCESS_ARCHITECTURE_RECONCILIATION`, informed by evidence from `STEP_02_CURRENT_IMPLEMENTATION_AUDIT` and `STEP_02_DEEP_REAUDIT_BEFORE_RECONCILIATION` (findings `DAA-001`…`DAA-015`, cited here only as rationale — not as part of the canonical model). Key changes: split Domain/Application as distinct layers in the diagram; **corrected** the dependency rules to prohibit `controller → repository-interface` (the Rev 1 draft allowed this, which contradicted the reconciled decision); added explicit Tenant Isolation, Transaction Ownership, Exception Translation, and Legacy Convergence policies (absent from Rev 1); added the numbered `DA-RULE-XXX` canonical rule list; added a concise Alternatives Considered section; added a Consequences section; marked `ports/persistence`, standalone `RowMapper` classes, and dialect-abstraction interfaces (`SqlDialect`, `UpsertStrategy`, `MySqlDialect`, …) as conditional/on-demand rather than mandatory Phase-1 deliverables; softened SQL-storage guidance to a pragmatic choice rather than one mandated form; clarified that `NamedParameterJdbcTemplate` is a clarity/maintainability preference and does **not** address schema-alignment defects. |
| 3 | 2026-08-18 | PROPOSED_FINAL_CANDIDATE | Minor technical clarification pass (`STEP_02_3`), architecture not reopened: clarified Spring JDBC API dependency vs runtime ownership (a `gm-*` module's JDBC adapters may depend on the Spring JDBC API without owning the DataSource/driver/pool); clarified TransactionManager ownership (`TRANSACTION_MANAGER_OWNER=GYSTIGO_HOST`, distinct from where the transaction boundary is declared); refined expected vs. unexpected persistence exception translation. |
| 4 | 2026-08-21 | OWNER_APPROVED_CANONICAL | Owner decisions `OD_DA_01` and `OD_DA_02` granted. Promotes Rev 3 without erasing its reasoning; closes exception-boundary ambiguity through revised `DA-RULE-010` and new `DA-RULE-017`; formalizes host/module ownership, testing ownership, flexible aggregate-cluster structure, and `gm-entities` Phase E as the first concrete consumer. |

---

## Problem

GYPPORT modules currently exhibit tight coupling to `JdbcTemplate`, MySQL-specific idioms, and persistence concerns scattered across domain logic, application services, and infrastructure. This creates:

1. **Technology Lock-in**: Changing the persistence technology (JDBC → ORM → alternative DB) requires changes across all modules
2. **Business Logic Contamination**: Services and repositories mix transactional operations with SQL-specific implementation details
3. **Lack of Testability**: Domain logic cannot be tested without a database or complex mocking of JDBC artifacts
4. **Maintenance Friction**: SQL dialects, driver-specific types, and configuration details bleed into business modules
5. **Unclear Boundaries**: No explicit architectural rule defines what a module can depend on

Additionally, there is a legal/contractual aspect (potential database licensing), but the fundamental issue is architectural hygiene: **a modular monolith's durability depends on clean separation between domain, application, ports, and infrastructure**.

This problem statement is independent of, and not blocked by, any specific defect found in the existing Gystigo host backend. Audit evidence (`STEP_02`/`STEP_02_DEEP_REAUDIT`) confirmed real correctness defects in legacy repository SQL (`DAA-010`, `DAA-011`, `DAA-012`) and layering gaps (`DAA-001`–`DAA-009`, `DAA-013`–`DAA-015`), but per this ADR's governing decision, **the legacy backend is a known input, not the reference implementation, and does not define or block the canonical standard below.**

---

## Decision

We adopt **Hexagonal Architecture (Ports & Adapters)** as the canonical model for GYPPORT data access, with explicit rules and layers.

```text
DECISION_SUMMARY = OWNER_APPROVED_CANONICAL (OD_DA_01=APPROVED, OD_DA_02=APPROVED)
```

### Architecture Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                    GYPPORT / GYSTIGO                          │
│                  MODULAR MONOLITH HOST                        │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                          DOMAIN                                │
│                                                               │
│   gm-entities   gm-products   gm-sales   gm-purchases ...     │
│                                                               │
│   ✓ Entity definitions, value objects, invariants            │
│   ✓ Business rules                                           │
│   ✓ Persistence Port interfaces (aggregate-owned)             │
│                                                               │
│   ✗ NO JdbcTemplate                                          │
│   ✗ NO MySQL types / com.mysql.*                             │
│   ✗ NO SQL-specific code                                     │
│   ✗ NO DataSource                                            │
└───────────────────────────┬───────────────────────────────────┘
                            │ used by
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                        APPLICATION                             │
│                                                               │
│   ✓ Use cases / application services                         │
│   ✓ Transaction demarcation (@Transactional on use cases)    │
│   ✓ Tenant context resolution → explicit tenantId to ports   │
│   ✓ Coordination across multiple ports/aggregates            │
│                                                               │
│   ✗ NO JdbcTemplate                                          │
│   ✗ NO MySQL types / com.mysql.*                             │
│   ✗ NO SQL-specific code                                     │
│   ✗ NO DataSource                                            │
│   ✗ NO direct dependency on the concrete JDBC adapter class   │
└───────────────────────────┬───────────────────────────────────┘
                            │ depends on (interface only)
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                    DATA ACCESS PORTS                          │
│                 (GYPPORT-defined contracts)                  │
│                                                               │
│   CustomerRepository                                         │
│   ProductRepository                                          │
│   InvoiceRepository                                          │
│   PurchaseOrderRepository                                    │
│   JournalEntryRepository                                     │
│   PartyRepository                                            │
│                                                               │
│   + Query Ports (CQRS-lite) — CONDITIONAL, see Query Ports §: │
│   CustomerQueryPort                                          │
│   InvoiceQueryPort                                           │
│                                                               │
│   ✓ Interface definitions, domain-owned (Repository) or       │
│     application/ports-owned (Query Port, cross-aggregate)     │
│   ✓ No SQL, no driver knowledge, tenantId explicit param      │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            │ implemented by
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                  PERSISTENCE ADAPTER                          │
│              (infrastructure/persistence/jdbc)                │
│                                                               │
│   JdbcCustomerRepository                                     │
│   JdbcProductRepository                                      │
│   JdbcInvoiceRepository                                      │
│   JdbcPurchaseOrderRepository                                │
│                                                               │
│   + Query Adapters (mirrors Query Ports, CONDITIONAL):        │
│   JdbcCustomerQueryAdapter                                   │
│   JdbcInvoiceQueryAdapter                                    │
│                                                               │
│   + Support (OPTIONAL — inline lambda mapping is acceptable): │
│   CustomerRowMapper                                          │
│   ProductRowMapper                                           │
│                                                               │
│   ✓ SQL execution (JdbcTemplate / NamedParameterJdbcTemplate) │
│   ✓ Row mapping (ResultSet → domain / read model directly)   │
│   ✓ Exception translation (DataAccessException → outcome)     │
│   ✓ Tenant-scoping enforcement on every tenant-owned query     │
│   ✓ JDBC-specific logic                                      │
└───────────────────────────┬───────────────────────────────────┘
                            │
                    ┌───────┴─────────┐
                    ▼                 ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│   SQL DIALECT ABSTRACTION      │ │   DATABASE CAPABILITIES      │
│   (ON-DEMAND ONLY — see §)     │ │   (ON-DEMAND ONLY — see §)   │
│                              │ │                              │
│ SqlDialect                   │ │ SequenceStrategy             │
│ PaginationStrategy           │ │ LockingStrategy              │
│ UpsertStrategy               │ │ JsonStrategy                 │
│ IdentifierQuoting            │ │ TimestampPrecisionStrategy   │
│                              │ │                              │
│ NOT built speculatively.     │ │ Introduced only when a real   │
│ Introduced only when a real  │ │ engine-specific behavior       │
│ second-engine difference     │ │ actually needs to vary.       │
│ must actually be varied.     │ │                              │
└───────────────────┬──────────┘ └───────────────┬──────────────┘
                    │                            │
        ┌───────────┴────────────┐               │
        │  (illustrative only —   │               │
        │   not required Phase-1  │               │
        │   deliverables)         │               │
        ▼                        ▼               ▼
 MySqlDialect          MySqlLockingStrategy   motor-specific
        │                        │
        └─────────────┬──────────┘
                      ▼
┌───────────────────────────────────────────────────────────────┐
│              DATASOURCE & JDBC DRIVER CONFIG                  │
│         (Gystigo Host Configuration — HOST-OWNED, exclusive)   │
│                                                               │
│    HikariCP DataSource                                       │
│             ↓                                                │
│    spring.datasource.url                                    │
│    spring.datasource.driver-class-name                      │
│    spring.datasource.hikari.*                              │
│             ↓                                                │
│    JDBC Standard API                                        │
│             ↓                                                │
│    mysql-connector-j (MySQL 8.4)                           │
└──────────────┬────────────────────────────────────────────────┘
               ▼
        ┌──────────────┐
        │   MySQL 8.4  │
        └──────────────┘
```

```text
PRIMARY_DATABASE=MYSQL_8_4
PORTABILITY_READY=YES        (Domain/Application code has no MySQL dependency)
MULTI_DATABASE_IMPLEMENTED=NO (no second engine is built, supported, or promised)
```

This ADR does not present, and must not be read as presenting, current support for PostgreSQL, MariaDB, SQL Server, or any engine other than MySQL 8.4. The dialect-abstraction boundary exists so that *if* a second engine is ever required, Domain/Application code will not need to change — it does not mean a second engine is being built now.

### Dependency Rules (Enforceable)

**Allowed dependencies:**

```
application-service → repository-interface ✓
application-service → query-port-interface ✓
jdbc-adapter → repository-interface (implements) ✓
jdbc-adapter → JdbcTemplate / NamedParameterJdbcTemplate ✓
jdbc-adapter → RowMapper (inline or standalone) ✓
jdbc-adapter → SQL execution ✓
jdbc-adapter → SqlDialect (only when introduced, see Dialect §) ✓
controller → application-service (use case) ✓
host → DataSource configuration ✓
host → JDBC driver config ✓
```

**Prohibited dependencies:**

```
domain → JdbcTemplate ✗
domain → DataSource ✗
domain → com.mysql.* ✗
domain → java.sql.* (except in adapter) ✗
application → JdbcTemplate ✗
application → MySQL-specific types ✗
application → concrete JDBC adapter class ✗
controller → SQL ✗
controller → repository-interface ✗   (corrected in Rev 2 — see note below)
controller → query-port-interface ✗   (corrected in Rev 2 — see note below)
controller → jdbc-adapter ✗
repository-interface → JDBC types ✗
any-module (gm-*) → own DataSource / JDBC URL / driver config ✗
```

> **Rev 2 correction:** Rev 1 of this ADR listed `controller → repository-interface ✓` as an allowed dependency. This contradicted the reconciled decision from `STEP_02_1`: controllers depend on **Application use cases only**; they must not reach past Application into a Persistence Port, Query Port, or JDBC Adapter directly. This has been corrected above. See **Controllers** § and `DA-RULE-011`.

**Spring JDBC API vs. runtime ownership matrix (Rev 3):** the table below makes explicit a distinction folded into the prose above — a module may depend on the Spring JDBC *API* to compile its own JDBC adapters without that meaning it owns any runtime persistence infrastructure. See **Primary Database & Driver** § for the full clarification.

| From | To | Allowed |
|---|---|---|
| Domain | Spring JDBC (any form) | NO |
| Application | Spring JDBC (any form) | NO |
| JDBC Adapter | Spring JDBC API (`JdbcTemplate`/`NamedParameterJdbcTemplate`/`JdbcClient`) | YES |
| `gm-*` module infrastructure | Spring JDBC API | YES |
| `gm-*` module (any layer) | MySQL Connector/J (`mysql-connector-j`) | NO |
| `gm-*` module (any layer) | own `DataSource` | NO |
| `gm-*` module (any layer) | own JDBC URL / DB credentials | NO |
| `gm-*` module (any layer) | own connection pool / Flyway runtime config | NO |
| Host | Spring JDBC runtime (auto-configuration) | YES |
| Host | `DataSource` | YES |
| Host | Transaction Manager | YES |
| Host | MySQL Connector/J | YES |

---

## Repository Design

### 1. Transactional Repositories (Commands)

Each domain module defines **specific, named** repositories for write operations, declared in `domain/` alongside the aggregate they serve (a repository interface is part of its aggregate's contract — see **Canonical Package Model**):

```java
// In gm-entities domain/
public interface CustomerRepository {

    Customer save(Customer customer);

    Optional<Customer> findById(
        TenantId tenantId,
        CustomerId customerId
    );

    boolean existsByIdentification(
        TenantId tenantId,
        Identification identification
    );

    void delete(TenantId tenantId, CustomerId customerId);
}
```

**Rules:**
- One repository per aggregate root
- Method names reflect business intent, not SQL structure
- No pagination/sorting in transactional repos
- Parameters are domain objects (`TenantId`, `CustomerId`), not primitives
- Every method touching tenant-owned data takes `TenantId` explicitly as a parameter (see **Tenant Isolation**)
- No `GenericRepository<T, ID>` abstraction (see **Rationale**)

### 2. Query Ports (CQRS-Lite)

```text
QueryPort = MANDATORY_FOR_COMPLEX_READS
QueryPort = OPTIONAL for simple, single-aggregate reads
```

A read is **mandatory** to model as a Query Port when it meets any of:
- it joins/spans more than one aggregate;
- it returns a projection or read-model shape rather than the aggregate itself;
- it exists specifically to serve a UI grid, dashboard, or report;
- it is a complex analytical/search query.

A read that is none of the above (a simple, single-aggregate lookup) **may** live as an ordinary finder method on the `Repository` port instead — a Query Port is not required for every read.

```java
// In gm-entities application/ports/ (or domain/ if it is aggregate-scoped — see note)
public interface CustomerQueryPort {

    Page<CustomerListItem> search(
        TenantId tenantId,
        CustomerSearchCriteria criteria,
        Pageable pageable
    );

    Optional<CustomerDetailItem> getForDisplay(
        TenantId tenantId,
        CustomerId customerId
    );

    List<CustomerBalance> getAccountBalances(
        TenantId tenantId
    );
}
```

**Rules:**
- Read-only, optimized for UI/reporting
- Return DTOs or view models (not domain entities)
- Pagination and sorting allowed here
- No mutation
- Separate from transactional repositories
- `TenantId` explicit on every method touching tenant-owned data (same rule as Repositories)

---

## Tenant Isolation

```text
TENANT_ID_EXPLICIT_IN_TENANT_OWNED_PORT_METHODS=REQUIRED
```

GYPPORT uses **shared-schema multitenancy** (`tenant_id` column, not database-per-tenant or schema-per-tenant). Persistence access must preserve tenant isolation structurally, not by convention alone.

- Every `Repository` or `QueryPort` method that reads or writes tenant-owned data **MUST** receive `tenantId` (or a `TenantId` value object) as an explicit parameter in its signature.
- A `TenantContext` (thread-local or request-scoped, populated once per request after authentication) **may** exist at the Application/web boundary to resolve "which tenant is this request for" — but Application **MUST** pass the resolved `tenantId` explicitly to the Port; it must not be re-resolved silently inside the JDBC Adapter as an implicit fallback for a missing parameter.
- A JDBC Adapter **MUST NOT** silently omit the `tenant_id` predicate on a tenant-scoped query when the corresponding port method received a `tenantId` parameter — the parameter existing and the SQL using it are both required.
- A tenant-agnostic (global) lookup is permitted **only** when the underlying column has a genuine, deliberate, DB-enforced global-uniqueness constraint — and that must be a documented decision per method, not an accidental omission.

**Rationale (evidence, not part of the canonical model itself):** the legacy audit (`STEP_02_DEEP_REAUDIT`, findings `DAA-001`/`DAA-014`) found a confirmed mechanism where a tenant-owned lookup omitted a `tenant_id` predicate because nothing in the method signature carried one to omit in the first place — two tenants could share a `username` (tenant-scoped unique only, not global), while `email_address` happened to also carry a global unique constraint. This rule exists specifically so that a future adapter cannot repeat that omission silently; it does not retroactively fix the legacy code, which converges separately (see **Legacy Convergence**).

---

## Transaction Ownership

```text
TRANSACTION_BOUNDARY=APPLICATION_USE_CASE
TRANSACTION_MANAGER_OWNER=GYSTIGO_HOST
```

- The transaction boundary for any use case is owned by the **Application layer**, not by an individual repository or adapter method.
- For the current stack (Spring Boot + `JdbcTemplate`), `@Transactional` **is** permitted directly on Application Service / use-case methods. This is a pragmatic choice: Spring's declarative transaction management, backed by the auto-configured `DataSourceTransactionManager`/`JdbcTransactionManager` that ships with `spring-boot-starter-jdbc`, already provides the needed guarantee without a separate `TransactionTemplate`-wrapping abstraction, which would be ceremony without benefit at this stack's current scale.

**Boundary declaration vs. runtime ownership (clarification, Rev 3):** placing `@Transactional` on a use case declares transactional *intent* — it does not mean the module owns the transactional *infrastructure*. The effective `TransactionManager`, `DataSource`, and connection pool that fulfill that boundary remain owned exclusively by the Gystigo host (consistent with `DATASOURCE_OWNER`/`CONNECTION_POOL_OWNER=GYSTIGO_HOST` above) — a module never configures or instantiates its own `TransactionManager`.

```text
Application Use Case
      │
      │ @Transactional  (module declares intent here)
      ▼
Persistence Ports
      ▼
JDBC Adapters
      ▼
JdbcTemplate
      ▼
DataSource ──────────── Transaction Manager   (both host-owned runtime infrastructure)
      │
      ▼
    MySQL
```
- A use case that coordinates writes across multiple ports/aggregates (e.g. "register tenant, then register the founding party") owns a **single** transaction boundary spanning both port calls. Individual `Repository`/`Adapter` methods do not declare their own `@Transactional` for what is really a multi-aggregate business operation — doing so would allow a partial commit if a later step in the use case fails.
- Repositories/adapters remain free to rely on the ambient transaction for their own single-statement work; they are not required to manage transactions themselves.
- JDBC Adapters participate in the external Host-managed transaction. They MUST NOT create or configure a competing module-owned transaction manager.

---

## Exception Translation

```text
INFRASTRUCTURE_EXCEPTION ↓ translate ↓ APPLICATION/DOMAIN MEANING
```

Infrastructure (the JDBC Adapter) may know about `DataAccessException` and its subtypes (`DuplicateKeyException`, `EmptyResultDataAccessException`, `BadSqlGrammarException`, etc.) and `SQLException`. These types **must not** become part of the contract that Application/Domain code depends on.

**Not every infrastructure exception should be forced into a domain/business exception. Every infrastructure exception must nevertheless cross the Adapter boundary only as a technology-neutral module-owned outcome or exception (canonical clarification, Rev 4).** The policy distinguishes two categories:

```text
EXPECTED_PERSISTENCE_OUTCOME
→ translate to a semantic application/domain outcome

UNEXPECTED_INFRASTRUCTURE_FAILURE
→ module-owned technology-neutral persistence exception
→ handled at host-level exception handling
→ generic 5xx externally
```

- **Expected persistence outcomes** — conditions the use case genuinely anticipates as part of normal business flow:
  - Expected absence → `Optional.empty()` / an empty collection (no exception at all).
  - `DuplicateKeyException`, when it represents an expected business conflict (e.g. a duplicate within a tenant) → a small, intention-revealing domain/application outcome (e.g. `DuplicateEntityException`).
  - A real concurrency conflict (e.g. optimistic-locking failure) → a concurrency/application conflict outcome.
  These are the **only** cases translated into a domain-meaningful type, and the set stays deliberately small — not a large 1:1 exception hierarchy.
- **Unexpected infrastructure failures** — conditions the use case does not anticipate and cannot meaningfully react to differently: `BadSqlGrammarException`, database unavailability, driver failures, or any other `DataAccessException` that isn't one of the expected outcomes above. These:
  - **MUST** be translated by the JDBC Adapter to a module-owned, technology-neutral persistence exception before leaving Infrastructure;
  - **MUST NOT** expose `DataAccessException`, any Spring/JDBC type, `java.sql` type, or database-vendor type through Domain, Application, or Port interfaces;
  - **MUST NOT** be falsely repackaged as a domain/business error either — an unexpected infrastructure failure is not a business outcome, and disguising it as one would be as misleading as leaking it raw;
  - **SHOULD** preserve the original infrastructure exception as the cause where appropriate for diagnostics;
  - are rendered by thin host-level exception handling (e.g. a single `@ControllerAdvice`) as a generic technical failure (5xx) externally. Host handling may depend on the neutral module exception contract, but MUST NOT depend on receiving raw `DataAccessException` from modules.

The standard does not prescribe one shared exception class name for every module. Each module owns its neutral persistence exception vocabulary. For the first reference implementation, `gm-entities` uses:

```text
com.gypport.business.entities.persistence.RepositoryAccessException
```

That name is a reference implementation, not a universal class-name mandate.

### Persistence Testing Ownership

```text
MODULE_UNIT_TESTS=DOMAIN_APPLICATION_ADAPTER_CONTRACTS
HOST_BACKED_INTEGRATION_TESTS=REAL_PERSISTENCE_RUNTIME
```

Module unit tests may verify:

- Domain behavior and invariants;
- Application orchestration and transaction declarations;
- adapter guards and tenant-context propagation;
- codecs and row-mapping helpers;
- exception translation;
- adapter contracts with test doubles where no real runtime claim is made.

Host-backed integration tests verify:

- the real JDBC driver and host-owned `DataSource`;
- the real connection pool and SQL;
- generated-key behavior and foreign-key constraints;
- the canonical Flyway schema and canonical seed data;
- real transaction participation and rollback.

A `gm-*` module MUST NOT introduce its own JDBC driver, `DataSource`, connection pool, JDBC URL, credentials, or transaction manager merely to close an integration-test gap when an approved Host-backed mechanism exists. `gm-entities` Phase E1/E2 is the first reference evidence for this split; it does not change runtime ownership.

### First Concrete Consumer: gm-entities Phase E

```text
Domain
  -> Application
  -> Repository Ports
  -> JDBC Adapters
  -> Host-provided Spring JDBC
  -> Host DataSource
  -> Host Driver
  -> MySQL 8.4

DataAccessException
  -> Adapter translation
  -> RepositoryAccessException
  -> Application
```

This is an architectural reference only. Rev 4 does not implement Java, adapters, SQL, schema, or host wiring.

---

## Module Structure

Each business module follows this layout. **Not every folder is mandatory** — see the table below.

```
gm-entities/
│
├── domain/
│   ├── entity/
│   │   ├── Customer.java
│   │   └── Address.java
│   ├── value/
│   │   ├── CustomerId.java
│   │   ├── Identification.java
│   │   └── TenantId.java
│   ├── error/
│   │   └── CustomerNotFoundException.java
│   └── CustomerRepository.java          ← aggregate-owned Persistence Port, lives here
│
├── application/
│   ├── service/
│   │   ├── CreateCustomerService.java
│   │   ├── UpdateCustomerService.java
│   │   └── GetCustomerService.java
│   ├── dto/
│   │   ├── CreateCustomerRequest.java
│   │   └── CustomerResponse.java
│   └── ports/
│       └── CustomerQueryPort.java       ← cross-aggregate Query Port, if needed (CONDITIONAL)
│
└── infrastructure/
    └── persistence/
        └── jdbc/
            ├── JdbcCustomerRepository.java
            ├── JdbcCustomerQueryAdapter.java   (CONDITIONAL — mirrors Query Ports)
            ├── CustomerRowMapper.java          (OPTIONAL — inline lambda acceptable)
            └── CustomerSql.java                (OPTIONAL — see SQL Ownership §)
```

| Folder | Requirement |
|---|---|
| `domain/` | **MANDATORY** once the module has any persisted aggregate |
| `application/` | **MANDATORY** |
| `infrastructure/persistence/jdbc/` | **MANDATORY** once any persistence exists |
| `application/ports/` (Query Ports) | **CONDITIONAL** — only when a cross-aggregate/read-model query actually exists (see Query Ports §) |
| Standalone `RowMapper` class | **OPTIONAL** — an inline lambda `RowMapper` inside the adapter method is fully acceptable for simple mappings; extract only when reused or genuinely complex |
| `sql/` holder classes, dialect packages | **OPTIONAL / ON-DEMAND** — see SQL Ownership and Dialect §§ |

No module is required to pre-create empty folders for capabilities it doesn't yet use.

Modules with multiple aggregate clusters may keep feature ownership visible, for example:

```text
identity/domain
identity/infrastructure

party/domain
party/infrastructure
```

Module-root packages remain available for genuinely cross-cutting module concerns:

```text
application
persistence
infrastructure
```

This elaboration is optional. A simpler module or aggregate MUST NOT be forced into extra packages when the structure adds no real ownership clarity.

---

## SQL Ownership

```text
SQL_MUST_NOT_EXIST_IN_DOMAIN=YES
SQL_MUST_NOT_EXIST_IN_APPLICATION=YES
```

SQL text lives exclusively inside the infrastructure/persistence/jdbc layer. **No single form is mandated** — choose pragmatically per adapter:

- **Default:** a `private static final String` constant (or an inline literal for a genuinely one-off simple statement) inside the JDBC adapter class.
- **Escalate to a dedicated `XxxSql` holder class** only once a single adapter accumulates enough SQL that the adapter class itself becomes hard to navigate — a judgment call at review time, not a fixed line-count rule.
- **`.sql` resource files** are reserved for genuinely large, DBA-authored SQL (complex reporting queries) where a `.sql` file materially helps readability/tooling — an escape hatch, not a default.

```java
// Example (Option B — escalate only if warranted): infrastructure/persistence/jdbc/CustomerSql.java
public class CustomerSql {

    public static final String CUSTOMER_BASE_SELECT = """
        SELECT c.id, c.tenant_id, c.name, c.identification_type,
               c.identification_value, c.email, c.phone
        FROM customers c
        WHERE c.tenant_id = ?
        """;

    public static final String CUSTOMER_INSERT = """
        INSERT INTO customers
        (tenant_id, name, identification_type, identification_value, email, phone)
        VALUES (?, ?, ?, ?, ?, ?)
        """;
}
```

### JdbcTemplate Policy

```text
JdbcTemplate=ALLOWED_IN_INFRASTRUCTURE_ONLY
NamedParameterJdbcTemplate=SHOULD_BE_PREFERRED_FOR_NEW_COMPLEX_STATEMENTS
```

- `JdbcTemplate` and `NamedParameterJdbcTemplate` are allowed exclusively inside the JDBC Adapter layer — never in Domain, Application, or controllers.
- `NamedParameterJdbcTemplate` **should** be preferred for new, multi-parameter statements going forward, purely for **clarity and maintainability** (named parameters are easier to review than a long run of positional `?` placeholders, especially on multi-column inserts/updates).
- **This preference does not claim to prevent schema-alignment defects.** The legacy audit's most serious findings (`DAA-010`, `DAA-011`) were SQL statements referencing columns that do not exist in the schema at all — a mismatch between the SQL text and the actual DDL, unrelated to whether the statement used positional or named parameters. Named parameters would not have caught, and are not a substitute for catching, that class of error. Preventing it requires reviewing/testing adapter SQL against the real schema, not a parameter-binding style choice.
- Plain `JdbcTemplate` remains fully acceptable for simple, single-parameter statements — this is a style recommendation for new complex statements, not a mandatory rewrite of existing simple ones.
- `JdbcClient` (Spring's newer fluent API) is allowed for new adapters at a team's discretion; it is not required.

### RowMapper

```text
ROWMAPPER=INFRASTRUCTURE_ONLY
Standalone RowMapper=OPTIONAL
```

- `RowMapper` performs `ResultSet → domain object` (or `ResultSet → read-model projection`, for Query Ports) directly. It must not contain business rules.
- Mapping directly to the domain/read-model type is the default — no separate intermediate "persistence representation" struct is required by default (avoiding an unnecessary `ResultSet → PersistenceDTO → Entity → Domain` chain).
- An inline lambda `RowMapper` inside the adapter method is fully acceptable when the mapping is simple. Extract to a standalone class only when it is reused across more than one adapter method or becomes complex enough to warrant its own test.

---

## SQL Dialect Handling

```text
DIALECT_ABSTRACTION=ON_DEMAND_ONLY
```

No `MySqlDialect`, `PostgreSqlDialect`, or `MariaDbDialect` abstraction is created speculatively. A dialect abstraction is introduced **only when** a second database engine is actually being supported **and** a concrete vendor-behavior difference needs to vary — for example:

```text
UPSERT syntax
Pagination (LIMIT/OFFSET vs. an alternative)
Row locking
Generated-key retrieval
JSON operations
Identifier quoting
```

The interface shapes below are kept in this ADR as an **illustration of the escape hatch**, not as a required Phase-1 deliverable — nothing in `gm-entities` or any other module needs to implement `SqlDialect`/`UpsertStrategy` until an actual second-engine need arises:

```java
// infrastructure/persistence/jdbc/dialect/SqlDialect.java — ON-DEMAND, not required today
public interface SqlDialect {
    String currentTimestampExpression();
    String quoteIdentifier(String identifier);
    String limitOffsetClause(long limit, long offset);
    String jsonExtractValue(String jsonColumn, String path);
}
```

```java
// Illustration only — MySQL 8.4, would only be written once the interface above is actually needed
public class MySqlDialect implements SqlDialect {
    @Override
    public String currentTimestampExpression() { return "CURRENT_TIMESTAMP(6)"; }
    @Override
    public String quoteIdentifier(String identifier) { return "`" + identifier + "`"; }
    @Override
    public String limitOffsetClause(long limit, long offset) { return "LIMIT " + limit + " OFFSET " + offset; }
    @Override
    public String jsonExtractValue(String jsonColumn, String path) { return String.format("JSON_EXTRACT(%s, '%s')", jsonColumn, path); }
}
```

```java
// Also illustration only — an UPSERT is real, concrete MySQL-dialect syntax; encapsulate it behind
// an interface only once a second engine's different UPSERT syntax must actually be supported.
public interface UpsertStrategy {
    String customerExternalCodeUpsertSql();
}

public class MySqlUpsertStrategy implements UpsertStrategy {
    @Override
    public String customerExternalCodeUpsertSql() {
        return """
            INSERT INTO customer_external_codes
            (customer_id, system_code, external_code, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP(6))
            ON DUPLICATE KEY UPDATE
                external_code = VALUES(external_code),
                updated_at = CURRENT_TIMESTAMP(6)
            """;
    }
}
```

Until a second engine is real, an adapter may simply write `ON DUPLICATE KEY UPDATE` (or any other MySQL-specific SQL) directly in its SQL — that is expected infrastructure coupling, not a violation, per **SQL Ownership** above.

---

## Primary Database & Driver

```text
PRIMARY_DATABASE=MYSQL_8_4
DATASOURCE_OWNER=GYSTIGO_HOST
JDBC_DRIVER_OWNER=GYSTIGO_HOST
CONNECTION_POOL_OWNER=GYSTIGO_HOST
TRANSACTION_MANAGER_OWNER=GYSTIGO_HOST
DATABASE_RUNTIME_CONFIGURATION_OWNER=GYSTIGO_HOST

GM_MODULE_MYSQL_CONNECTOR_ALLOWED=NO
GM_MODULE_DATASOURCE_ALLOWED=NO
GM_MODULE_CONNECTION_POOL_ALLOWED=NO
GM_MODULE_TRANSACTION_MANAGER_ALLOWED=NO
GM_MODULE_JDBC_URL_ALLOWED=NO
GM_MODULE_DATABASE_CREDENTIALS_ALLOWED=NO

GM_MODULE_SPRING_JDBC_INFRASTRUCTURE_ADAPTER_ALLOWED=YES
DOMAIN_SPRING_JDBC_ALLOWED=NO
APPLICATION_SPRING_JDBC_ALLOWED=NO
PORT_SPRING_JDBC_ALLOWED=NO
```

- Motor: **MySQL 8.4**
- Connector: **mysql-connector-j**
- `DataSource` (HikariCP), connection pool, and JDBC driver configuration are owned **exclusively** by the Gystigo host — centralized in the host's `application.yml`/`application.yaml`.
- Internal modules (`gm-entities`, `gm-products`, `gm-purchases`, `gm-sales`, `gm-accounting`, and future modules):

```text
MUST_NOT_DEFINE_OWN_DATASOURCE
MUST_NOT_DEFINE_JDBC_URL
MUST_NOT_DECLARE_MYSQL_DRIVER (no mysql-connector-j dependency in a module's own pom.xml)
```

- A module's JDBC Adapters receive the host-provided `JdbcTemplate`/`NamedParameterJdbcTemplate` bean via ordinary Spring dependency injection — they never construct or configure their own.

**Technology API dependency vs. runtime infrastructure ownership (clarification, Rev 3):** these are two different things and must not be conflated.

```text
SPRING_JDBC_API=MODULE_ADAPTER_ALLOWED
MYSQL_DRIVER=HOST_RUNTIME_ONLY
DATASOURCE=HOST_OWNED
CONNECTION_POOL=HOST_OWNED
```

A `gm-*` module that contains a JDBC Adapter necessarily compiles against the Spring JDBC API (`JdbcTemplate`, `NamedParameterJdbcTemplate`, `JdbcClient`) — that is an unavoidable, allowed **technology API dependency**, not a runtime-ownership violation. What remains prohibited is the module owning the **runtime infrastructure** behind that API:

When the Host supplies the Spring runtime, an API dependency such as `spring-jdbc` MAY use Maven `provided` scope. This ADR intentionally does not make today's concrete Spring version a permanent architecture rule; version compatibility remains governed by the Host integration baseline.

```text
gm-* MAY depend on the Spring JDBC API when the module contains JDBC adapters.
gm-* MUST NOT declare mysql-connector-j.
gm-* MUST NOT configure or instantiate its own DataSource.
gm-* MUST NOT define its own JDBC URL or DB credentials.
gm-* MUST NOT configure its own connection pool or Flyway runtime configuration.
```

"The module uses the `JdbcTemplate` API" and "the module controls the datasource/driver" are not the same claim — only the second is prohibited by `DATASOURCE_OWNER=GYSTIGO_HOST` / `JDBC_DRIVER_OWNER=GYSTIGO_HOST` above. This does not change those ownership decisions; it only removes an ambiguity about what a module's `pom.xml` is allowed to compile against. The exact `pom.xml` shape is not designed here — that is a Phase 3 concern.

- This is confirmed compatible with the current modular-monolith host: the existing Gystigo backend already has exactly one `DataSource` (Hikari, auto-configured), one `application.yaml`, and the MySQL driver dependency declared only once, runtime-scoped, in the host's own `pom.xml` — no structural change to the host is implied by this rule.

**Future Portability:** The architecture *permits* future migration to a different engine without changing Domain/Application code. We do **not** implement a second engine today. We design the boundary cleanly and leave the implementation for when it is actually needed — see **Dialect Handling**, `PORTABILITY_READY=YES` / `MULTI_DATABASE_IMPLEMENTED=NO`.

---

## Flyway / Schema Portability Boundary

```text
APPLICATION_PORTABILITY  ≠  SCHEMA_PORTABILITY
FLYWAY_MAY_USE_MYSQL_SPECIFIC_DDL=YES
```

- This ADR governs **application-code portability** (Domain/Application/Ports have no MySQL dependency). It does **not** require or imply that Flyway migrations become multi-engine.
- Migrations are permitted to remain MySQL-idiomatic DDL (`ENGINE=InnoDB`, `AUTO_INCREMENT`, `TINYINT(1)` booleans, JSON columns, etc.) as a conscious, contained decision — that is schema portability, a separate axis this ADR does not decide.
- Flyway configuration remains centralized in the host, not per module.
- **Migration location is not changed by this ADR.** Audit evidence noted the current legacy host's migrations physically live at `database/core/migration` (outside the `platform_os/server` Maven module, copied onto the classpath at build time) rather than under a module's own `src/main/resources/db/migration/`. Whether that location is the deliberate canonical shared-schema location or should move is an open item tracked separately (outside this step's authorization) — this ADR neither mandates nor changes it.

---

## Controllers

```text
CONTROLLER_TO_APPLICATION=YES
CONTROLLER_TO_PERSISTENCE_PORT=NO
CONTROLLER_TO_JDBC_ADAPTER=NO
```

Controllers depend on Application-layer use cases only. They must not inject or call a `Repository`, `QueryPort`, or JDBC Adapter directly, and must not construct SQL. This corrects the Rev 1 draft's dependency-rules table, which incorrectly allowed `controller → repository-interface` (see the correction note under **Dependency Rules**).

---

## Legacy Convergence

```text
NEW_CODE_MUST_FOLLOW_STANDARD=YES
LEGACY_CODE_MAY_CONVERGE_INCREMENTALLY=YES
BIG_BANG_REFACTOR_REQUIRED=NO
```

- All new persistence code — starting with `gm-entities` — follows this standard from first implementation. No exceptions for net-new code.
- The existing Gystigo host backend is **not** required to be restructured into ports/adapters as a prerequisite for anything, including fixing already-identified correctness defects (`DAA-010`, `DAA-011`, `DAA-012`). Those are bugs to be fixed on their own schedule, independent of this ADR.
- **Convergence strategy:** when an existing legacy repository is touched for an unrelated reason (bug fix, new method, feature work), that touch is a natural, low-risk opportunity to extract a port interface for that one aggregate and turn the existing class into its `Jdbc*` adapter implementation. This is opportunistic, not scheduled as a dedicated migration project.
- The legacy audit findings `DAA-001` through `DAA-015` are **evidence that motivated specific rules in this ADR** (Tenant Isolation, Transaction Ownership, Controllers, Exception Translation) — they are not themselves part of the canonical model, and fixing them is not a prerequisite for this ADR's acceptance or for `gm-entities` proceeding to reference templates.
- A shared, non-generic infrastructure base class (comparable to the legacy `BaseJdbcRepository`, which only shares a `JdbcTemplate` field, not business methods) is compatible with this ADR and may continue to exist or be introduced for new adapters — it is not the `GenericRepository<T, ID>` pattern this ADR prohibits (see **Rationale**).

---

## Rationale

### Why Not a Single GenericRepository<T, ID>?

```text
GenericRepository<T, ID> = PROHIBITED_AS_CANONICAL_DOMAIN_ABSTRACTION
```

A generic repository obscures important business semantics:

```java
// ❌ BAD: Loses meaning
interface GenericRepository<T, ID> {
    T save(T entity);
    Optional<T> findById(ID id);
    List<T> findAll();
}
```

For an ERP, different aggregates have fundamentally different operations:

```java
// ✓ GOOD: Clear intent
interface CustomerRepository {
    Customer save(Customer customer);
    Optional<Customer> findById(TenantId tenantId, CustomerId id);
    boolean existsByIdentification(TenantId tenantId, Identification id);
}

interface InvoiceRepository {
    InvoiceNumber reserveNextNumber(TenantId tenantId);
    void insertDraft(Invoice invoice);
    void freeze(InvoiceId invoiceId);
    void markIssued(InvoiceId invoiceId, String accessKey);
    Optional<Invoice> findForUpdate(TenantId tenantId, InvoiceId id);
}
```

Each repository speaks the language of its domain. A generic `save(T)` also cannot express aggregate-specific invariants (e.g. a party creation that requires a linked master-data record first) the way a purpose-built method signature can.

### Why Separate Query Ports?

Transactional repositories optimize for command consistency; queries optimize for read performance. Mixing them forces compromises:

```java
// ❌ BAD: Transactional repo forced to support read-heavy queries
repository.search(criteria, pageable); // Awkward for a command repository
repository.getTopCustomersByBalance(); // Not a transaction

// ✓ GOOD: Separate concerns
invoiceRepository.save(invoice);  // transactional
invoiceQueryPort.search(criteria, pageable); // read-optimized
```

### Why Not Multi-Motor SQL Today?

Attempting to write "universal" SQL adds complexity without benefit:

```java
// ❌ This sounds good but adds overhead and hidden bugs:
if (dialect.supportsJson()) { ... }
if (dialect.needsSequenceForId()) { ... }
String pagination = dialect.limitOffsetClause(...);
```

Instead, we:
1. **Design the boundary** (the `SqlDialect` interface shape exists as an illustration)
2. **Implement only MySQL**, and only when a real second-engine need forces the boundary to be built
3. **Make migration explicit** (when a second engine is needed, add its `Dialect` implementation then — not before)

---

## Alternatives Considered

Kept brief and architectural — not a full comparative study.

| Alternative | Verdict | Why |
|---|---|---|
| **JdbcTemplate directly from Application/services** | Rejected | Collapses Application and Adapter; makes use cases untestable without a real datasource; exactly the pattern the legacy audit flagged when a controller reached a repository directly. |
| **Concrete repositories, no interfaces** | Rejected as canonical (the legacy backend's current shape) | Compiles and works, but couples Application code directly to `JdbcTemplate`-shaped classes and blocks swapping infrastructure or using a test double. |
| **`GenericRepository<T, ID>`** | Rejected | See **Rationale** — erases domain-specific operations and invariants. |
| **JPA / Hibernate** | Rejected for now | Not currently used anywhere in the stack (no dependency, no annotations). A real option in principle, but adopting an ORM is a larger technology decision than this ADR's scope, and the current schema's ID strategy and master-data-linked party model need real modeling work before a straightforward JPA mapping exists. Not precluded permanently — out of scope here. |
| **jOOQ** | Rejected for now | Would give compile-time-checked SQL against generated schema metadata — a genuinely attractive property that could have prevented column-name defects like those found in the legacy audit. Not adopted now because it introduces a new build-time codegen dependency the team hasn't evaluated; worth a dedicated future evaluation. |
| **MyBatis** | Rejected for now | A real alternative to hand-written `JdbcTemplate` SQL; would still sit behind the same Port/Adapter boundary this ADR defines, so adopting it later would not require revisiting this decision, only the Adapter's internals. |
| **Repository Ports + JdbcTemplate Adapters** | **Selected** | Matches the existing technology exactly (zero new dependencies), fits the modular monolith's single-`DataSource` reality, and delivers the properties GYPPORT needs today — testability via port mocking, replaceable infrastructure, MySQL isolation — without the modeling cost of an ORM or the tooling cost of a codegen SQL builder. |
| **Multi-engine implementation from now** | Rejected | Out of scope per `MULTI_DATABASE_SUPPORT_NOW=NO` — would mean building and maintaining dialect abstractions for a second engine nobody is running. |

---

## Canonical Rules

```text
DA-RULE-001  (MUST NOT)
Domain and Application code MUST NOT depend directly on JdbcTemplate, NamedParameterJdbcTemplate, JdbcClient, DataSource, java.sql.*, or com.mysql.*.

DA-RULE-002  (MUST)
Persistence capabilities MUST be exposed to Application code exclusively through domain-specific Persistence Port or Query Port interfaces.

DA-RULE-003  (MAY / SHOULD)
JDBC Adapters MAY use JdbcTemplate, NamedParameterJdbcTemplate, or JdbcClient. NamedParameterJdbcTemplate SHOULD be preferred for new, complex/multi-parameter statements for clarity and maintainability — this preference does not address, and MUST NOT be presented as addressing, schema-alignment defects (SQL referencing columns that don't exist), which are a review/testing concern, not a parameter-binding-style concern.

DA-RULE-004  (MUST / MAY — refined Rev 3)
The Gystigo host owns DataSource, connection pool, and JDBC driver (mysql-connector-j) configuration exclusively. Internal modules (gm-*) MUST NOT declare their own datasource, JDBC URL, DB credentials, driver dependency, connection pool, or Flyway runtime configuration. This does NOT prohibit a module from depending on the Spring JDBC API itself: a gm-* module MAY depend on JdbcTemplate/NamedParameterJdbcTemplate/JdbcClient when it contains JDBC adapters — that is a technology API dependency, not a claim of runtime infrastructure ownership.

DA-RULE-005  (MUST NOT)
GenericRepository<T, ID> or any CRUD-generic persistence abstraction MUST NOT be used as the canonical domain repository shape. Repositories MUST be named and shaped per aggregate.

DA-RULE-006  (MUST)
Every Persistence Port or Query Port method that reads or writes tenant-owned data MUST take tenantId (or an equivalent value object) as an explicit parameter.

DA-RULE-007  (MUST NOT)
A JDBC Adapter MUST NOT silently omit a tenant_id predicate on a tenant-scoped query when the corresponding port method received a tenantId parameter.

DA-RULE-008  (SHOULD)
A read operation SHOULD be modeled as a Query Port instead of a Repository method when it spans more than one aggregate, returns a projection rather than the aggregate itself, or exists to serve a dashboard/report/grid.

DA-RULE-009  (MUST)
The transaction boundary for any use case touching more than one Persistence Port MUST be owned by the Application-layer use case (e.g. via @Transactional on the use-case method), never by an individual repository/adapter method.

DA-RULE-010  (MUST — revised Rev 4)
JDBC Adapters MUST distinguish EXPECTED_PERSISTENCE_OUTCOME from UNEXPECTED_INFRASTRUCTURE_FAILURE. Expected outcomes (absence, expected duplicate/uniqueness conflicts, real concurrency conflicts) MUST be translated into Optional.empty() or a small set of intention-revealing domain/application outcomes before crossing into Application/Domain code. Unexpected failures (BadSqlGrammarException, DB unavailability, driver failures, or any other unmapped DataAccessException) MUST be translated before leaving the Adapter into a module-owned, technology-neutral persistence exception. Neither category may expose raw Spring, JDBC, java.sql, or database-vendor types through Application, Domain, or Port contracts. Host-level handling may render the neutral exception as a generic technical failure, but MUST NOT depend on receiving raw DataAccessException from a module.

DA-RULE-011  (MUST NOT)
Controllers MUST NOT depend on Persistence Ports, Query Ports, or JDBC Adapters directly — only on Application use cases.

DA-RULE-012  (MAY)
SQL text MAY live as adapter-local constants, a dedicated XxxSql holder class, or an external .sql resource file, chosen pragmatically per adapter; it MUST NOT appear in Domain or Application packages under any option.

DA-RULE-013  (MUST NOT / MAY)
No dialect-abstraction interface (e.g. MySqlDialect) MUST be introduced speculatively; such an abstraction MAY be introduced only when a second database engine is actually being supported and a concrete vendor behavior difference (UPSERT, pagination, locking, generated keys, JSON ops, identifier quoting) requires it.

DA-RULE-014  (MAY)
Flyway migrations MAY use MySQL-specific DDL; schema portability is a decision independent of this ADR's application-portability scope.

DA-RULE-015  (SHOULD)
New persistence code SHOULD follow this standard from first implementation; existing legacy Gystigo host repositories MAY converge to it incrementally, opportunistically, when touched for another reason — convergence is never a prerequisite for unrelated bug fixes.

DA-RULE-016  (MUST — added Rev 3)
The Gystigo host owns the TransactionManager runtime exclusively, distinct from where a transaction boundary is declared (DA-RULE-009). An Application use case declaring @Transactional expresses transactional intent only; it MUST NOT configure, instantiate, or own its own TransactionManager, DataSource, or connection pool.

DA-RULE-017  (MUST — added Rev 4)
SPRING_DATA_ACCESS_EXCEPTION_MUST_NOT_ESCAPE_ADAPTER_BOUNDARY=YES
EXCEPTION_TRANSLATION_REQUIRED=YES
Domain, Application, and Port interfaces MUST NOT depend on org.springframework.dao.DataAccessException or its subtypes. Every JDBC Adapter MUST translate Spring DataAccessException before the exception leaves Infrastructure. The translated exception MUST be module-owned and technology-neutral; MUST import no Spring, JDBC, java.sql, or database-vendor type; and SHOULD preserve the original exception as cause where appropriate. This rule does not force every module to use one shared exception class name. `com.gypport.business.entities.persistence.RepositoryAccessException` is the first reference implementation, not a universal class name.
```

---

## Consequences

```text
DATABASE_CHANGE_AUTOMATIC=NO
```

**Positive**
- Domain/Application code is decoupled from `JdbcTemplate`/MySQL, made explicit and enforceable rather than incidental.
- Use cases become unit-testable against a mocked port, without a real database.
- Infrastructure (the JDBC adapter, even the DB engine boundary) becomes structurally replaceable without touching Domain/Application.
- Uniform, predictable module shape across `gm-entities`, `gm-products`, `gm-purchases`, `gm-sales`, `gm-accounting`, and future modules, without forcing identical repository/query-port method sets across unrelated domains.
- A named, reviewable boundary (the JDBC Adapter) is exactly where SQL-vs-schema alignment must be checked — concentrating that review responsibility in one place rather than spreading it across controllers/services.

**Negative / Cost**
- More interfaces and classes per aggregate than a single repository class (a Port + an Adapter, possibly a Query Port) — real ceremony, bounded by making Query Ports, standalone RowMappers, and dialect abstractions conditional/on-demand rather than mandatory.
- Requires sustained architectural discipline (Controllers→Application only, no `JdbcTemplate` outside adapters) enforced by review — nothing in the build currently checks these boundaries automatically; adding that (e.g. ArchUnit rules) is future work, not delivered by this ADR alone.
- This ADR reduces Application/Domain coupling to the persistence *technology*. It does **not** reduce or eliminate the cost of:
  - schema migrations and DDL design;
  - SQL that is genuinely specific to MySQL where a real vendor difference exists;
  - writing and maintaining tests for the persistence layer (currently near-zero coverage on the legacy host, per audit evidence — a separate, unaddressed cost this ADR does not itself pay down);
  - database operations and performance tuning.
- Changing the database engine is **not** made automatic by this ADR — only Application/Domain code's dependency on the current engine is removed. The schema, and any adapter SQL that legitimately needs to stay engine-specific, are unaffected.

---

## Implementation Roadmap

### Phase 1: Canonical ADR (Current)
- ✓ Document decision
- ✓ Define rules and layers
- ✓ Establish naming conventions
- ✓ Reconcile against audit evidence (`STEP_02_1`) and finalize as candidate (`STEP_02_2`, this revision)
- ✓ Owner approval and canonical promotion (`OD_DA_01=APPROVED`, `OD_DA_02=APPROVED`, Rev 4)

### Phase 2: Current Implementation Audit
- ✓ Scan legacy host for JDBC coupling (`STEP_02`, `STEP_02_DEEP_REAUDIT`)
- ✓ Identify violations and correctness defects (`DAA-001`…`DAA-015`)
- ✓ Reconcile findings against the canonical model (`STEP_02_1`) — legacy findings do not define the standard
- [ ] Separate, explicitly authorized track to address legacy correctness defects (`DAA-010`/`DAA-011`/`DAA-012`) on their own schedule

### Phase 3: Reference Templates & Patterns (not authorized by this document)
- [ ] Create `RepositoryTemplate.java` for copy-paste
- [ ] Create `RowMapperTemplate.java` (optional pattern, per RowMapper §)
- [ ] Create `SqlTemplate.java` (one of the pragmatic SQL-ownership options, per SQL Ownership §)
- [ ] Document integration with Spring Configuration
- [ ] Apply to `gm-entities` as the first reference module

### Phase 4: Incremental Refactoring (not authorized by this document)
- [ ] Apply templates to existing modules
- [ ] Add linting/enforcement (Checkstyle, ArchUnit) for `DA-RULE-001`/`002`/`011`
- [ ] Update CI to verify rule compliance
- [ ] Document in GYPPORT Developer Handbook
- [ ] Opportunistic legacy convergence per **Legacy Convergence** §

---

## Enforcement

To keep the architecture intact:

1. **Code Review Checklist**: Does this PR introduce `JdbcTemplate`/`DataSource`/`com.mysql.*` in domain/application layers? Does a controller depend on a port or adapter directly? Does a tenant-owned port method omit `tenantId`?
2. **ArchUnit Rules** (in CI, future work — not delivered by this ADR):
   ```
   classes in domain should not depend on JdbcTemplate
   classes in application should not depend on com.mysql
   classes in application should not depend on infrastructure.persistence.jdbc..
   controllers should not depend on ..persistence..
   ```
3. **Package Structure Validation**: Repository ports live in `domain/` (aggregate-owned) or `application/ports/` (cross-aggregate Query Ports); adapters live in `infrastructure/persistence/jdbc/`.

---

## Examples

### Example 1: Customer Service with Repository

```java
@Service
public class CreateCustomerService {

    private final CustomerRepository customerRepository;
    private final TenantContext tenantContext;

    public CreateCustomerService(
            CustomerRepository customerRepository,
            TenantContext tenantContext) {
        this.customerRepository = customerRepository;
        this.tenantContext = tenantContext;
    }

    @Transactional
    public CustomerId execute(CreateCustomerRequest request) {
        TenantId tenantId = tenantContext.getCurrentTenantId(); // resolved once here

        Customer customer = Customer.create(
            tenantId,
            request.getName(),
            request.getIdentification()
        );

        customerRepository.save(customer); // tenantId flows explicitly via the domain object / port params
        return customer.getId();
    }
}
```

**Note:** No `JdbcTemplate`, no MySQL, no SQL visible. Transaction boundary owned here (`@Transactional` on the use case), per **Transaction Ownership**.

### Example 2: JDBC Adapter

```java
@Repository
public class JdbcCustomerRepository implements CustomerRepository {

    private final NamedParameterJdbcTemplate jdbcTemplate;

    public JdbcCustomerRepository(NamedParameterJdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public Customer save(Customer customer) {
        try {
            return customer.isNew() ? insertNew(customer) : updateExisting(customer);
        } catch (DataAccessException e) {
            throw translate(e); // Exception Translation §
        }
    }

    private Customer insertNew(Customer customer) {
        var params = new MapSqlParameterSource()
            .addValue("tenantId", customer.getTenantId().getValue())
            .addValue("name", customer.getName().getValue())
            .addValue("email", customer.getEmail().getValue());

        int rows = jdbcTemplate.update(CustomerSql.CUSTOMER_INSERT, params);
        if (rows != 1) {
            throw new PersistenceException("Insert failed");
        }
        return customer;
    }

    @Override
    public Optional<Customer> findById(TenantId tenantId, CustomerId customerId) {
        var params = new MapSqlParameterSource()
            .addValue("tenantId", tenantId.getValue())
            .addValue("customerId", customerId.getValue());

        List<Customer> results = jdbcTemplate.query(
            CustomerSql.CUSTOMER_BASE_SELECT + " AND c.id = :customerId",
            params,
            (rs, rowNum) -> CustomerRowMapping.fromRow(rs) // inline or standalone mapping, RowMapper §
        );
        return results.stream().findFirst();
    }
}
```

**Note:** All JDBC concerns are here, including exception translation and explicit `tenantId` handling. Domain never sees this.

### Example 3: Query Port

```java
public interface CustomerQueryPort {
    Page<CustomerListItem> search(
        TenantId tenantId,
        CustomerSearchCriteria criteria,
        Pageable pageable
    );
}

@Component
public class JdbcCustomerQueryAdapter implements CustomerQueryPort {

    private final NamedParameterJdbcTemplate jdbcTemplate;

    @Override
    public Page<CustomerListItem> search(
            TenantId tenantId,
            CustomerSearchCriteria criteria,
            Pageable pageable) {

        // Dialect abstraction only introduced here if/when a second engine forces it — see Dialect §
        String sql = """
            SELECT c.id, c.name, c.email, COUNT(i.id) as invoice_count
            FROM customers c
            LEFT JOIN invoices i ON c.id = i.customer_id
            WHERE c.tenant_id = :tenantId
            """ + criteria.toWhereClause() + """
            GROUP BY c.id, c.name, c.email
            ORDER BY """ + criteria.getSortBy() +
            " LIMIT :limit OFFSET :offset";

        var params = new MapSqlParameterSource()
            .addValue("tenantId", tenantId.getValue())
            .addValue("limit", pageable.getPageSize())
            .addValue("offset", pageable.getOffset());

        List<CustomerListItem> items = jdbcTemplate.query(sql, params, new CustomerListItemRowMapper());
        long total = countTotal(tenantId, criteria);

        return new PageImpl<>(items, pageable, total);
    }
}
```

---

## Related Documents

- **GYPPORT Modular Monolith Architecture** (reference ADR for module boundaries)
- `STEP_02_CURRENT_IMPLEMENTATION_AUDIT` / `STEP_02_DEEP_REAUDIT_BEFORE_RECONCILIATION` — evidence base (`DAA-001`…`DAA-015`), cited here as rationale only
- `STEP_02_1_DATA_ACCESS_ARCHITECTURE_RECONCILIATION` — the reconciliation this revision incorporates
- **Persistence Testing Ownership** (formalized in Rev 4 of this document)

---

## Approval & Supersedes

- **Proposed by:** Eduardo Burgasi
- **Status:** OWNER_APPROVED_CANONICAL
- **Owner decisions:** `OD_DA_01=APPROVED`; `OD_DA_02=APPROVED`
- **Supersedes:** Any prior undocumented assumptions about data access coupling
- **Reconciliation input:** `STEP_02_1_DATA_ACCESS_ARCHITECTURE_RECONCILIATION` (`ACCEPT_WITH_REFINEMENT`)

---

## Appendix: Quick Reference

| Artifact | Location | Purpose |
|----------|----------|---------|
| Domain Entities | `domain/entity/` | Business state |
| Use Cases | `application/service/` | Business operations, transaction boundary |
| Repository Interface | `domain/` (aggregate-owned) | Data access contract, MANDATORY |
| Query Port | `application/ports/` | Complex/cross-aggregate read port, CONDITIONAL |
| JDBC Implementation | `infrastructure/persistence/jdbc/` | SQL execution, exception translation, tenant scoping |
| Row Mapper | `infrastructure/persistence/jdbc/` | Result conversion, OPTIONAL as standalone class |
| SQL | adapter-local constant / `XxxSql` / `.sql` resource | Pragmatic choice, never in Domain/Application |
| SQL Dialect | `infrastructure/persistence/jdbc/dialect/` | ON-DEMAND ONLY — not built until a second engine needs it |

---

**End of ADR-01 (Rev 4 — OWNER_APPROVED_CANONICAL)**

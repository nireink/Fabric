# STEP 02: Current Implementation Audit — Template & Execution Plan

**Status:** TEMPLATE READY FOR EXECUTION  
**Date:** 2026-08-18  
**Based on:** ADR-01: GYPPORT Data Access Architecture Model

---

## Overview

This document is a **reusable checklist** for auditing GYPPORT modules against the architecture defined in ADR-01. It includes:

1. Search patterns for each coupling type
2. A scoring matrix for severity assessment
3. Instructions for running the audit across modules
4. Template for documenting findings

## Phase 2 Execution: Coupling Audit

### Module List

- **gm-entities**
- **gm-products**
- **gm-purchases**
- **gm-sales**
- **gm-service-management**
- **gm-e-documents**
- **Gystigo** (host)

### Audit Categories

#### 1. JdbcTemplate in Wrong Layers

**What to look for:** `JdbcTemplate` appearing in domain, application, or controller classes.

**Search patterns:**

```bash
# In each module, search for JdbcTemplate usage:
grep -r "JdbcTemplate" src/ --include="*.java" | grep -v "infrastructure/persistence"

# Check for @Autowired JdbcTemplate in services:
grep -r "@Autowired" src/ --include="*.java" | grep -A2 "JdbcTemplate"

# Check for constructor injection in wrong places:
grep -r "this.jdbcTemplate\|this\.template" src/ --include="*.java" | grep -v "infrastructure"
```

**Red flags:**
- `@Service` or `@Component` with injected `JdbcTemplate`
- `JdbcTemplate` in any file under `domain/` or `application/`
- Direct `JdbcTemplate` calls in business logic

**Example violation:**
```java
@Service
public class CustomerService {
    @Autowired
    private JdbcTemplate jdbcTemplate;  // ❌ VIOLATION
    
    public void createCustomer(String name) {
        jdbcTemplate.update("INSERT INTO customers...");  // ❌ VIOLATION
    }
}
```

**Correct pattern:**
```java
@Service
public class CustomerService {
    private final CustomerRepository customerRepository;  // ✓ Port
    
    public CustomerService(CustomerRepository repository) {
        this.customerRepository = repository;
    }
}
```

---

#### 2. MySQL-Specific Imports

**What to look for:** Direct imports of MySQL classes outside the JDBC adapter.

**Search patterns:**

```bash
# Find all com.mysql imports:
grep -r "import com\.mysql\." src/ --include="*.java"

# Check for mysql-specific drivers:
grep -r "com\.mysql\.cj\.jdbc\|org\.mysql\.jdbc" src/ --include="*.java"

# Find DataSource configuration in modules:
grep -r "@Bean.*DataSource\|DataSource.*@Bean" src/ --include="*.java"
grep -r "spring\.datasource\." src/ --include="*.properties" --include="*.yml" --include="*.yaml"
```

**Red flags:**
- `import com.mysql.cj.*;` in domain, application, or service classes
- `spring.datasource.*` config in module-level files (should only be in host)
- `@Bean` defining DataSource anywhere except host

**Example violation:**
```java
// gm-entities/src/main/java/com/gypport/entity/service/CustomerService.java
import com.mysql.cj.jdbc.Driver;  // ❌ VIOLATION: MySQL-specific

@Service
public class CustomerService {
    // ...
}
```

**Correct pattern:**
```java
// Gystigo/src/main/java/com/gypport/host/config/DatasourceConfig.java
import com.mysql.cj.jdbc.Driver;  // ✓ OK: Only in host config
```

---

#### 3. Raw SQL in Services & Controllers

**What to look for:** SQL strings embedded in business logic or controllers.

**Search patterns:**

```bash
# Find SQL strings in services:
grep -r "SELECT\|INSERT\|UPDATE\|DELETE" src/ --include="*.java" | grep -E "(\".*SELECT|'.*SELECT)"

# Find SQL in controllers specifically:
grep -r "class.*Controller" src/ --include="*.java" -l | xargs grep -l "SELECT\|INSERT\|UPDATE"

# Find raw SQL that isn't in SQL constant classes:
grep -r "\"SELECT.*FROM\|\"INSERT INTO\|\"UPDATE.*SET" src/ --include="*.java" | grep -v "sql/.*\.java" | grep -v "adapter/.*\.java"
```

**Red flags:**
- SQL in `@RestController` or `@Controller` classes
- Raw SQL strings in `@Service` classes (not going through repository)
- SQL passed directly to methods instead of using abstraction

**Example violation:**
```java
@RestController
@RequestMapping("/api/customers")
public class CustomerController {
    
    @GetMapping("/{id}")
    public ResponseEntity<?> getCustomer(@PathVariable String id) {
        // ❌ VIOLATION: Raw SQL in controller
        String sql = "SELECT * FROM customers WHERE id = ?";
        return ResponseEntity.ok(someJdbcService.query(sql, id));
    }
}
```

**Correct pattern:**
```java
@RestController
@RequestMapping("/api/customers")
public class CustomerController {
    private final CustomerRepository repository;  // ✓ Port
    
    @GetMapping("/{id}")
    public ResponseEntity<Customer> getCustomer(@PathVariable String id) {
        return repository.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}
```

---

#### 4. SQL Dialect Specific Code Scattered

**What to look for:** Motor-specific SQL (MySQL) appearing outside the dialect layer.

**Search patterns:**

```bash
# Find ON DUPLICATE KEY UPDATE (MySQL-specific):
grep -r "ON DUPLICATE KEY UPDATE" src/ --include="*.java" | grep -v "infrastructure"

# Find AUTO_INCREMENT (MySQL-specific):
grep -r "AUTO_INCREMENT\|AUTOINCREMENT" src/ --include="*.java" | grep -v "infrastructure"

# Find MySQL JSON functions:
grep -r "JSON_EXTRACT\|JSON_SET\|JSON_ARRAY" src/ --include="*.java" | grep -v "infrastructure"

# Find MySQL-specific functions:
grep -r "CURRENT_TIMESTAMP(6)\|UUID()\|LAST_INSERT_ID()" src/ --include="*.java" | grep -v "infrastructure"

# Find LIMIT/OFFSET without abstraction:
grep -r "LIMIT.*OFFSET" src/ --include="*.java" | grep -v "infrastructure" | grep -v "dialect"
```

**Red flags:**
- SQL dialect keywords in services or repositories outside `infrastructure/persistence/jdbc/dialect/`
- Multiple implementations of the same pattern with different SQL syntax
- Hardcoded pagination SQL instead of using `SqlDialect`

**Example violation:**
```java
@Repository
public class ProductRepository {
    @Query("SELECT * FROM products LIMIT ? OFFSET ?")  // ❌ Motor-specific
    Page<Product> search(Pageable page) { ... }
}
```

**Correct pattern:**
```java
@Repository
public class JdbcProductRepository {
    private final SqlDialect dialect;
    
    public Page<Product> search(Pageable page) {
        String sql = ProductSql.BASE_SELECT 
            + " " + dialect.limitOffsetClause(page.getPageSize(), page.getOffset());
        // ✓ Dialect abstraction
    }
}
```

---

#### 5. Repository Architecture Issues

**What to look for:** Generic repositories, mixed read/write, missing transactional repos.

**Search patterns:**

```bash
# Find GenericRepository usage:
grep -r "extends.*GenericRepository\|extends.*JpaRepository.*<T" src/ --include="*.java"

# Find repositories mixing queries:
grep -r "interface.*Repository" src/ --include="*.java" -A 10 | grep -E "findBy|search|list" | wc -l

# Check for repositories doing write ops alongside complex reads:
grep -r "interface.*Repository" src/ --include="*.java" -A 20 | grep -E "save|update|delete|search|findBy"

# Find QueryPort implementations:
grep -r "interface.*QueryPort\|interface.*Query" src/ --include="*.java"
```

**Red flags:**
- `extends GenericRepository<T, ID>` pattern (should be specific per aggregate)
- Single repository mixing transactional saves with complex queries
- No separation between `*Repository` (commands) and `*QueryPort` (queries)
- Repository methods with complex pagination/filtering logic

**Example violation:**
```java
// ❌ VIOLATION: Generic + mixed concerns
interface CustomerRepository extends GenericRepository<Customer, Long> {
    
    Customer save(Customer customer);  // Write
    
    Page<Customer> search(String name, Integer page);  // Complex read
    
    List<CustomerDTO> getAllBalances();  // Read-heavy DTO query
}
```

**Correct pattern:**
```java
// ✓ Separated concerns
interface CustomerRepository {
    Customer save(Customer customer);
    Optional<Customer> findById(TenantId tenantId, CustomerId id);
}

interface CustomerQueryPort {
    Page<CustomerSearchResult> search(TenantId tenantId, String name, Pageable page);
    List<CustomerBalance> getAccountBalances(TenantId tenantId);
}
```

---

#### 6. DataSource & Configuration Scattered

**What to look for:** Database configuration and driver setup in individual modules.

**Search patterns:**

```bash
# Find DataSource beans outside host:
grep -r "@Bean" src/ --include="*.java" -B2 | grep -A2 "DataSource"

# Find datasource config in module properties:
find src/ -name "application*.properties" -o -name "application*.yml" | \
  xargs grep -l "spring.datasource"

# Find JDBC driver config outside host:
grep -r "jdbc:mysql\|jdbc:postgresql" src/ --include="*.properties" --include="*.yml"

# Find Flyway configuration in modules:
grep -r "spring.flyway" src/ --include="*.properties" --include="*.yml" | grep -v "gystigo-host\|host"
```

**Red flags:**
- `DataSource` `@Bean` in module-level config classes
- `spring.datasource.*` properties in individual modules
- Flyway migrations defined at module level (should be centralized)
- JDBC driver configuration outside of host

**Example violation:**
```yaml
# gm-entities/src/main/resources/application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/gypport  # ❌ VIOLATION: Module config
    driver-class-name: com.mysql.cj.jdbc.Driver  # ❌ VIOLATION
```

**Correct pattern:**
```yaml
# Gystigo/src/main/resources/application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/gypport  # ✓ Only in host
    driver-class-name: com.mysql.cj.jdbc.Driver  # ✓ Only in host
```

---

### Audit Scoring Matrix

Create a matrix for each module to assess coupling:

```
| Module              | JdbcTemplate | MySQL Imports | Raw SQL | Scattered Config | Repository Issues | Dialect Code | **Severity** | **Priority** |
|---------------------|:------------:|:-------------:|:-------:|:----------------:|:-----------------:|:------------:|:------------:|:------------:|
| gm-entities         | 0            | 0             | 2       | 1                | 1                 | 0            | **LOW**      | P2           |
| gm-products         | 3            | 2             | 5       | 2                | 3                 | 1            | **HIGH**     | P0           |
| gm-purchases        | 5            | 1             | 8       | 1                | 2                 | 2            | **CRITICAL** | P0           |
| gm-sales            | 2            | 0             | 3       | 0                | 1                 | 0            | **LOW**      | P2           |
| gm-service-mgmt     | 1            | 0             | 1       | 0                | 0                 | 0            | **LOW**      | P2           |
| Gystigo (host)      | 5            | 10            | 20      | 10               | 0                 | 3            | **EXPECTED** | —            |
```

**Scoring:**
- 0 = None detected
- 1-3 = Few violations, low impact
- 4-10 = Multiple violations, medium impact
- 11+ = Pervasive coupling, high refactoring cost

**Severity Levels:**
- **CRITICAL:** >15 points. Immediate refactoring required. Cannot evolve without risk.
- **HIGH:** 10-15 points. Refactoring strongly recommended. Blocks multi-motor support.
- **MEDIUM:** 5-10 points. Refactoring recommended but not blocking. Clean-up work.
- **LOW:** <5 points. Minimal coupling. Can be refactored incrementally with new features.
- **EXPECTED:** Gystigo host. Should contain all JDBC, MySQL, DataSource concerns. Not a violation.

**Priority Mapping:**
- **P0:** CRITICAL + HIGH (do first)
- **P1:** MEDIUM (do after P0)
- **P2:** LOW (do last, can defer)

---

### Execution Instructions

**For each module:**

1. Run all search patterns listed above
2. Count violations in each category
3. Score severity based on matrix
4. Document findings in the template below

**Time estimate:** 15-30 minutes per module if manual; 5 minutes if using CI integration (SonarQube rules, custom linting).

**Recommended tool:**
```bash
# Run once for all modules:
./scripts/audit-db-coupling.sh
```

(See Appendix A for script)

---

## Finding Template

Use this template to record each finding:

```markdown
### Module: [MODULE_NAME]

**Overall Coupling Score:** [n] / 50

#### JdbcTemplate Violations
- [ ] `@Autowired JdbcTemplate` in services (Count: [n])
  - Files: [list]
  - Severity: LOW / MEDIUM / HIGH
  
#### MySQL-Specific Imports
- [ ] `import com.mysql.*` outside adapter (Count: [n])
  - Files: [list]
  - Severity: LOW / MEDIUM / HIGH

#### Raw SQL Scattered
- [ ] SQL strings in service/controller classes (Count: [n])
  - Files: [list]
  - Severity: LOW / MEDIUM / HIGH

#### Configuration Coupling
- [ ] DataSource beans in module (Count: [n])
- [ ] Datasource config in properties (Count: [n])
  - Files: [list]
  - Severity: LOW / MEDIUM / HIGH

#### Repository Architecture
- [ ] GenericRepository usage (Count: [n])
- [ ] Repositories mixing read/write (Count: [n])
- [ ] No QueryPort separation (Count: [n])
  - Severity: LOW / MEDIUM / HIGH

#### SQL Dialect Leakage
- [ ] Motor-specific SQL in business code (Count: [n])
  - Examples: [list]
  - Severity: LOW / MEDIUM / HIGH

#### Summary
- **Total Violations:** [n]
- **Estimated Refactoring Effort:** [days]
- **Blocking Issues:** [list or "None"]
- **Recommended Actions:** [list]
```

---

## Appendix A: Automated Audit Script

If you have scripting access, use this to automate:

```bash
#!/bin/bash
# scripts/audit-db-coupling.sh

MODULES="gm-entities gm-products gm-purchases gm-sales gm-service-management"
HOST="Gystigo"

for MODULE in $MODULES; do
    echo "=== Auditing $MODULE ==="
    
    echo "1. JdbcTemplate in wrong layers:"
    grep -r "JdbcTemplate" "$MODULE/src/" --include="*.java" | grep -v "infrastructure/persistence" | wc -l
    
    echo "2. MySQL imports:"
    grep -r "import com\.mysql\." "$MODULE/src/" --include="*.java" | wc -l
    
    echo "3. Raw SQL:"
    grep -r "\"SELECT\|\"INSERT\|\"UPDATE\|\"DELETE" "$MODULE/src/" --include="*.java" | grep -v "sql/.*\.java" | wc -l
    
    echo "4. DataSource config:"
    grep -r "spring\.datasource" "$MODULE/src/" --include="*.properties" --include="*.yml" | wc -l
    
    echo "5. GenericRepository:"
    grep -r "GenericRepository\|JpaRepository" "$MODULE/src/" --include="*.java" | wc -l
    
    echo ""
done
```

---

## Next Steps After Audit

Once findings are documented:

1. **Aggregate into coupling matrix**
2. **Prioritize modules:** CRITICAL → HIGH → MEDIUM → LOW
3. **Create refactoring roadmap:** Start with P0 modules
4. **Move to Phase 3:** Create reference templates for new code
5. **Incremental refactoring:** Apply templates to highest-priority modules first

---

## Appendix B: Quick Reference — What Should Live Where

| Pattern | Domain | Application | Ports | Adapter (JDBC) | Host |
|---------|:------:|:-----------:|:-----:|:--------------:|:----:|
| Entity definitions | ✓ | | | | |
| Value objects | ✓ | | | | |
| Business logic | ✓ | | | | |
| Services | | ✓ | | | |
| Repository interfaces | | | ✓ | | |
| `JdbcTemplate` | | | | ✓ | |
| RowMapper | | | | ✓ | |
| SQL strings | | | | ✓ | |
| `SqlDialect` | | | | ✓ | |
| `DataSource` config | | | | | ✓ |
| MySQL driver config | | | | | ✓ |
| Flyway migrations | | | | | ✓ |

---

**End of STEP 02 Template**

---

## Appendix C: Common Findings & Quick Fixes

### Finding: JdbcTemplate in CustomerService

**Before (❌):**
```java
@Service
public class CustomerService {
    @Autowired private JdbcTemplate jdbcTemplate;
    
    public void save(Customer c) {
        jdbcTemplate.update("INSERT...", c.getName());
    }
}
```

**After (✓):**
```java
@Service
public class CustomerService {
    private final CustomerRepository repository;
    
    public CustomerService(CustomerRepository repository) {
        this.repository = repository;
    }
    
    public void save(Customer c) {
        repository.save(c);
    }
}
```

**Refactoring effort:** 30 min per service

---

### Finding: DataSource in Module Config

**Before (❌):**
```yaml
# gm-entities/src/main/resources/application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/gypport
    username: root
```

**After (✓):**
```yaml
# Move to Gystigo/src/main/resources/application.yml
# gm-entities: Remove datasource config entirely
```

**Refactoring effort:** 15 min per module

---

### Finding: GenericRepository Mixed with Queries

**Before (❌):**
```java
interface CustomerRepository extends GenericRepository<Customer, Long> {
    Page<Customer> search(String name, Pageable page);
    List<CustomerDTO> getTopBalances();
}
```

**After (✓):**
```java
interface CustomerRepository {
    Customer save(Customer c);
    Optional<Customer> findById(Long id);
}

interface CustomerQueryPort {
    Page<CustomerSearchItem> search(String name, Pageable page);
    List<CustomerBalance> getTopBalances();
}
```

**Refactoring effort:** 1-2 hours per repository

---

**End of ADR-02 Implementation Audit Template**

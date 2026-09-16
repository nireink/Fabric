# GYPPORT® SaaS Deployment, Distribution and Dependency Governance Standard v1.0

**Document ID:** GYPPORT-SAAS-DEPLOYMENT-DISTRIBUTION-DEPENDENCY-GOVERNANCE-01  
**Version:** 1.0  
**Status:** PROPOSED_CANONICAL_STANDARD  
**Scope:** GYPPORT® Platform OS, Gystigo host, all `gm-*` modules, build/runtime infrastructure, third-party dependencies  
**Product model:** `SAAS_ONLY`  
**Implementation authorization:** NO — governance/documentation only

---

## 1. Purpose

This standard defines the canonical deployment and software-distribution model for GYPPORT®, establishes the boundary between SaaS operation and software distribution, and sets the governance rules for third-party dependencies, database engines, containers, licensing reviews, and future software-compliance artifacts.

The intent is to prevent future architecture, licensing, or implementation reviews from incorrectly treating GYPPORT® as an installable/on-premise product when the approved product model is SaaS-only.

---

## 2. Canonical product model

```text
GYPPORT_PRODUCT_MODEL=SAAS_ONLY

CUSTOMER_LOCAL_INSTALLATION=NO
CUSTOMER_ON_PREMISE_EDITION=NO
CUSTOMER_EXECUTABLE_BINARY_DELIVERY=NO
CUSTOMER_DOCKER_IMAGE_DELIVERY=NO
CUSTOMER_DOCKER_COMPOSE_DELIVERY=NO
CUSTOMER_DATABASE_ENGINE_DISTRIBUTION=NO
CUSTOMER_JDBC_DRIVER_DISTRIBUTION=NO
CUSTOMER_CONTROLLED_RUNTIME_INSTALLATION=NO
```

### Canonical rule

> GYPPORT® SaaS maintains operational control of the executable copies of GYPPORT® and its infrastructure components. Customers receive access to the service, not a distribution of the software.

The customer consumes GYPPORT® through approved remote interfaces such as HTTPS/API.

The customer does not receive an installable copy of the GYPPORT® application, database engine, JDBC driver, Docker image, Docker Compose stack, or packaged runtime.

---

## 3. Hosting model

The SaaS classification is not determined by whether the infrastructure is physically located in a public cloud, private datacenter, colocation facility, or GYPPORT®-owned server room.

The following hosting models are compatible with the canonical SaaS model when GYPPORT® retains operational control:

```text
GYPPORT_MANAGED_PUBLIC_CLOUD=ALLOWED
GYPPORT_OWNED_PHYSICAL_SERVERS=ALLOWED
GYPPORT_MANAGED_COLOCATION=ALLOWED
GYPPORT_MANAGED_PRIVATE_CLOUD=ALLOWED
GYPPORT_MANAGED_MULTI_DATACENTER=ALLOWED
```

Examples include:

- cloud infrastructure contracted and administered by GYPPORT®;
- dedicated servers owned by GYPPORT®;
- servers hosted in colocation facilities but administered by GYPPORT®;
- future multi-region or multi-datacenter infrastructure managed by GYPPORT®.

The physical location of the hardware does not by itself redefine the product as on-premise.

---

## 4. Customer boundary

Under the approved SaaS-only model, a customer:

- does not receive GYPPORT® binaries for installation;
- does not receive the Gystigo backend JAR for installation;
- does not receive `gm-*` modules as installable runtime packages;
- does not receive MySQL Server as part of a GYPPORT® product package;
- does not receive MySQL Connector/J as part of a GYPPORT® product package;
- does not receive Docker images containing the GYPPORT® runtime;
- does not receive a GYPPORT® Docker Compose stack;
- does not administer the production application runtime;
- does not operate a customer-controlled copy of the complete GYPPORT® software stack.

Customers may receive their own authorized business data exports, reports, XML files, documents, backups, or other data artifacts where contractually and technically appropriate. A customer-data export must not be treated as equivalent to distribution of the GYPPORT® software runtime.

---

## 5. Docker governance

Docker is an internal engineering and infrastructure tool unless a separate Owner decision explicitly changes this rule.

```text
DOCKER_ROLE_DEVELOPMENT=YES
DOCKER_ROLE_TESTING=YES
DOCKER_ROLE_REPRODUCIBILITY=YES
DOCKER_ROLE_VERSION_FREEZE=YES
DOCKER_ROLE_CI_CD=ALLOWED_SUBJECT_TO_SEPARATE_DESIGN
DOCKER_CUSTOMER_DISTRIBUTION=NO
```

Approved current uses include:

- local development;
- integration testing;
- reproducible environments;
- dependency/runtime version freezing;
- build verification;
- future internal CI/CD or infrastructure automation after separate authorization.

A Docker image used internally by GYPPORT® does not become a customer-distributed product merely because it contains third-party components.

---

## 6. Database engine governance

### Current candidate

```text
DATABASE_ENGINE_CURRENT_CANDIDATE=MYSQL_8_4
```

MySQL may remain the canonical database candidate for the GYPPORT® MVP.

A licensing or redistribution observation must not by itself trigger a migration away from MySQL when the identified concern only applies to a distribution model that GYPPORT® does not use.

### PostgreSQL and MariaDB

PostgreSQL and MariaDB remain valid technical alternatives but are not required solely because of a hypothetical software-distribution scenario.

They must be compared only when justified by one or more of the following:

- technical capability;
- operational reliability;
- performance;
- scalability;
- managed-service availability;
- backup and disaster-recovery requirements;
- replication;
- observability;
- data architecture;
- reporting/analytics needs;
- cost;
- long-term maintainability;
- security;
- verified licensing/compliance advantage that actually applies to the approved deployment model.

```text
MIGRATE_FROM_MYSQL_DUE_TO_HYPOTHETICAL_REDISTRIBUTION_ONLY=NO
MULTI_DATABASE_SUPPORT_REQUIRED_FOR_MVP=NO
```

---

## 7. Repository/Port architecture rule

The domain and application layers must not depend directly on database-specific SQL or database vendor APIs.

Canonical direction:

```text
Domain / Application
        |
        v
Repository Port / Interface
        |
        v
Infrastructure Adapter
        |
        v
JdbcTemplate / JDBC
        |
        v
Canonical Database Engine
```

### Required rules

- Repository interfaces express business intent, not SQL syntax.
- Database-specific SQL remains inside infrastructure/adapters.
- Controllers and business services must not contain SQL.
- Raw SQL fragments must not be passed between architectural layers.
- Vendor-specific operations such as upsert, JSON operators, locking hints, collations, date functions, or pagination syntax must remain isolated.
- Flyway migrations may contain engine-specific DDL where justified, but such dependencies must be identifiable.
- GYPPORT® is not required to support MySQL, PostgreSQL and MariaDB simultaneously.

The objective is not premature multi-engine support. The objective is to avoid contaminating the business domain with database-vendor details.

---

## 8. Third-party dependency governance

Every third-party dependency included in the GYPPORT® build or runtime must be inventoried and classified.

The classification model is:

```text
OK_COMMERCIAL
REQUIRES_NOTICES
COPYLEFT_REVIEW
PROPRIETARY_OR_RESTRICTED_REVIEW
UNKNOWN_REQUIRES_RESEARCH
```

A dependency may also receive operational qualifiers such as:

```text
SAAS_USE_OK
DISTRIBUTION_REVIEW_REQUIRED
SECURITY_REVIEW_REQUIRED
VERSION_REVIEW_REQUIRED
TRANSITIVE_DEPENDENCY
DIRECT_DEPENDENCY
BUILD_ONLY
TEST_ONLY
RUNTIME
```

A classification is not permanent. It applies to a specific component, version, license, usage mode, and product/deployment model.

---

## 9. Required stack audit

A dedicated dependency/license audit must review the actual GYPPORT® technology stack and resolved dependency tree.

At minimum, the audit should cover:

- Java / OpenJDK distribution actually used;
- Spring Boot;
- Spring Framework;
- Spring Security;
- Spring JDBC;
- MySQL Server;
- MySQL Connector/J;
- Flyway;
- Logback;
- SLF4J;
- Log4j API or bridges when present;
- Jackson;
- JSpecify;
- Maven;
- Maven plugins;
- React;
- React DOM;
- TypeScript;
- Vite;
- Tailwind CSS;
- Node.js runtime used for build;
- npm/pnpm/yarn tooling actually used;
- frontend transitive dependencies;
- test libraries;
- code-quality tools;
- vulnerability scanners;
- reporting libraries;
- PDF/XML/signature libraries;
- SRI electronic-document dependencies;
- all future `gm-*` module dependencies.

The audit must use the versions actually resolved by the project rather than relying only on top-level declared versions.

---

## 10. Required classification record

Each dependency should be recorded with at least:

```text
COMPONENT=
GROUP_OR_PACKAGE=
VERSION=
DIRECT_OR_TRANSITIVE=
SCOPE=
LICENSE=
LICENSE_SOURCE=
COPYRIGHT_NOTICE_REQUIRED=
SOURCE_DISCLOSURE_REQUIRED=
MODIFICATION_OBLIGATIONS=
SAAS_USE_CLASSIFICATION=
DISTRIBUTION_CLASSIFICATION=
SECURITY_STATUS=
KNOWN_CVE_STATUS=
OWNER=
REVIEW_DATE=
EVIDENCE=
FINAL_CLASSIFICATION=
NOTES=
```

The legal/compliance classification should use primary license sources whenever possible.

---

## 11. Licensing review boundary

Technical architecture review may identify licensing risks and establish compliance gates, but it must not fabricate a final legal opinion.

```text
TECHNICAL_LICENSE_REVIEW=ALLOWED
LEGAL_INTERPRETATION_FINALITY=NO
```

Before commercial launch, GYPPORT® should perform a formal OSS/license compliance review of the actual production dependency inventory.

This review is a release/compliance control and is not automatically an architecture or MVP-development blocker unless a concrete dependency issue affects the approved SaaS model.

---

## 12. Re-evaluation triggers

The SaaS distribution analysis must be reopened if a future Owner decision introduces any of the following:

```text
ON_PREMISE_EDITION
CUSTOMER_LOCAL_INSTALLATION
CUSTOMER_CONTROLLED_CLOUD_INSTALLATION
CUSTOMER_CONTROLLED_SERVER_RUNTIME
DOWNLOADABLE_APPLIANCE
DOWNLOADABLE_VM_IMAGE
DOWNLOADABLE_DOCKER_IMAGE
WHITE_LABEL_INSTALLABLE_EDITION
TRIAL_WITH_PACKAGED_RUNTIME
CUSTOMER_DISTRIBUTION_OF_DATABASE_ENGINE
CUSTOMER_DISTRIBUTION_OF_JDBC_DRIVER
OTHER_TRANSFER_OF_EXECUTABLE_RUNTIME_TO_CUSTOMER_CONTROL
```

These are re-evaluation triggers, not currently approved GYPPORT® product modes.

---

## 13. Security and licensing are separate gates

A dependency may be legally usable and still be blocked because of a vulnerability.

Likewise, a dependency may be secure at a given version but require licensing/compliance review.

Therefore:

```text
SECURITY_GATE != LICENSE_GATE
LICENSE_GATE != ARCHITECTURE_GATE
ARCHITECTURE_GATE != IMPLEMENTATION_AUTHORIZATION
```

No security finding should be dismissed merely because SaaS distribution is permitted, and no hypothetical distribution concern should be converted into an MVP security blocker.

---

## 14. Required follow-on governance artifacts

This standard should be complemented by separate documents rather than mixing all concerns into one file.

Recommended artifacts:

### 14.1 Third-party license inventory

```text
GYPPORT_THIRD_PARTY_LICENSE_INVENTORY_v1.0.md
```

Purpose:

- inventory direct and transitive dependencies;
- record official licenses;
- classify commercial/SaaS use;
- record required notices;
- identify copyleft or proprietary review.

### 14.2 OSS compliance standard

```text
GYPPORT_OSS_LICENSE_COMPLIANCE_STANDARD_v1.0.md
```

Purpose:

- define license-review workflow;
- define evidence requirements;
- define NOTICE/LICENSE retention rules;
- define approval gates;
- define escalation to qualified legal review.

### 14.3 Dependency governance register

```text
GYPPORT_DEPENDENCY_GOVERNANCE_REGISTER_v1.0.md
```

Purpose:

- dependency ownership;
- direct vs transitive status;
- BOM/version-management source;
- security status;
- approved/rejected/deferred decisions.

### 14.4 Security vulnerability register

```text
GYPPORT_DEPENDENCY_SECURITY_REGISTER_v1.0.md
```

Purpose:

- CVEs;
- affected versions;
- mitigation;
- verification evidence;
- acceptance/rejection of risk;
- implementation/release gates.

### 14.5 Third-party notices artifact

```text
THIRD_PARTY_NOTICES.md
```

Purpose:

- collect notices required for the production/release artifact when applicable.

### 14.6 Software Bill of Materials

A machine-readable SBOM should be generated from the actual resolved build when the build/release process is ready.

Preferred formats should be evaluated separately, such as CycloneDX or SPDX.

---

## 15. Document authority

This document defines the GYPPORT® SaaS deployment/distribution baseline.

It does not:

- approve a specific third-party dependency version;
- replace a dependency security audit;
- replace a formal legal opinion;
- authorize implementation;
- authorize production release;
- authorize on-premise distribution;
- authorize customer-controlled runtime installations.

Any future document that assumes GYPPORT® is an on-premise or customer-installable product conflicts with this standard unless supported by a later explicit Owner decision that supersedes this rule.

---

## 16. Canonical summary

```text
GYPPORT_PRODUCT_MODEL=SAAS_ONLY

GYPPORT_CONTROLS_EXECUTABLE_RUNTIME=YES
CUSTOMER_RECEIVES_SERVICE_ACCESS_ONLY=YES

CUSTOMER_INSTALLABLE_GYPPORT=NO
CUSTOMER_MYSQL_DISTRIBUTION=NO
CUSTOMER_CONNECTOR_J_DISTRIBUTION=NO
CUSTOMER_DOCKER_DISTRIBUTION=NO

DOCKER=INTERNAL_ENGINEERING_AND_INFRASTRUCTURE_TOOL

MYSQL_8_4=VALID_CURRENT_DATABASE_CANDIDATE
MYSQL_MIGRATION_REQUIRED_BY_CURRENT_DISTRIBUTION_FINDING=NO

POSTGRESQL=TECHNICAL_ALTERNATIVE
MARIADB=TECHNICAL_ALTERNATIVE
DATABASE_SELECTION_MUST_BE_BASED_ON_ACTUAL_TECHNICAL_OPERATIONAL_STRATEGIC_REQUIREMENTS=YES

REPOSITORY_PORT_BOUNDARY=REQUIRED
MULTI_DATABASE_MVP_SUPPORT=NOT_REQUIRED

THIRD_PARTY_DEPENDENCY_INVENTORY=REQUIRED
OSS_LICENSE_COMPLIANCE_REVIEW=REQUIRED_BEFORE_COMMERCIAL_LAUNCH
SECURITY_REVIEW=SEPARATE_REQUIRED_GATE

FUTURE_CUSTOMER_CONTROLLED_INSTALLATION=REOPEN_LICENSE_AND_DISTRIBUTION_ANALYSIS
```

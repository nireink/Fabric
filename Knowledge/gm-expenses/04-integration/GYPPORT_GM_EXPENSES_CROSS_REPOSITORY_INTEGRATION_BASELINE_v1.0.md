# GYPPORT gm-expenses — Cross-Repository Integration Baseline v1.0

```text
HISTORICAL INITIAL-DEVELOPMENT BASELINE

This document describes the initial design stage and is not the
current authoritative MVP baseline.

Current authority:
GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
```

```text
TRACK=GM-EXPENSES-INITIAL-DEVELOPMENT-01
PHASE_D_STATUS=OWNER_ACCEPTED
```

This document distinguishes the **approved target model** from **currently
verified platform state**. Where a Host contract is still work-in-progress,
this document says so explicitly — it does not present WIP as stable.

## 1. Security / tenant context

### Approved target

```text
TENANT_ID_FROM_AUTH_CONTEXT=YES
ACTOR_FROM_AUTH_CONTEXT=YES
```

Client-supplied tenant or actor identity is never authoritative. An
organization selected by the client is only a *selection* — the Host
verifies actual access.

### Currently verified state (as of this baseline)

```text
AUTH_CONTEXT_CONTRACT_FOUND=NO
TENANT_CONTEXT_CONTRACT_FOUND=NO
```

Gystigo's `AuthController` (`POST /auth/login`) performs real credential
verification and returns `{actor, tenant, permissions}` in the response
body, but its own documentation states this explicitly does not yet issue a
JWT or create a persistent session (tracked as `AUTH-05.2`, pending). No
`SecurityContextHolder` population, request-scoped principal, or equivalent
mechanism was found anywhere in the Host for propagating tenant/actor
identity into a *subsequent* request.

```text
BLOCKS_DOMAIN=NO
BLOCKS_APPLICATION=NO
BLOCKS_REAL_AUTHENTICATED_HTTP_INTEGRATION=YES
```

`gm-expenses` must **not** invent its own authentication mechanism to work
around this gap. It is a Host integration prerequisite, tracked outside this
module.

## 2. Cross-repository integration state

| Repository | Verified state | gm-expenses relationship |
|---|---|---|
| **Gystigo (Host)** | Owns DataSource, connection pool, MySQL driver, transaction manager, Flyway runtime | Composition point — see §3 |
| **gm-entities** | Implemented (`feat/entities-initial-development`); provides the canonical Party precedent (`MdmParty`, `TenantParty`) and the verified feature-first package/JDBC/exception-translation style this baseline follows | No direct dependency |
| **gm-organizations** | Implemented (`feat/organizations-initial-development`); owns the `Organization` aggregate | No direct dependency |
| **Organization Access** (who may access which organization) | Implemented natively inside Gystigo Host as `com.gypport.server.module.access` (`OrganizationAccessQueryPort`, JDBC adapters, wired via `OrganizationAccessConfig`) — **work-in-progress, not yet committed at the time of this baseline** | Do not duplicate. Treat as informational precedent only until it stabilizes; do not build a hard dependency on its current shape |
| **gm-fleet** | Bootstrap-only — no `pom.xml`, no `src/`, no canonical vehicle master exists anywhere | `gm-expenses`' local `VehicleReference` is required for the current MVP, not an optional fallback |
| **Document / object storage** | No platform storage contract exists anywhere on the platform | `DocumentStoragePort` is defined in Application now; the concrete storage adapter is deferred integration work |

### Dependency rules (non-negotiable)

```text
gm-expenses MUST NOT compile-depend directly on:
- gm-entities
- gm-organizations
- gm-fleet
```

Cross-module orchestration belongs to Gystigo Host. There are no
cross-module physical database foreign keys.

## 3. Document command trust boundary

The client must never supply an authoritative `storage_reference`.

```text
client upload handle/content
  → DocumentStoragePort
  → StoredDocumentDescriptor
  → immutable internal storageReference
  → ExpenseDocument persistence
```

No distributed MySQL/object-storage transaction is assumed — the storage
write and the database write are not coupled by a two-phase commit.

## 4. Category scope

```text
ExpenseCategory scope: GLOBAL | TENANT
```

`ExpenseCategory` is **not** organization-scoped. Tenant users may
create/modify `TENANT` categories only. `GLOBAL` categories are
platform-seeded reference data.

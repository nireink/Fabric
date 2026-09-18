# GYPPORT gm-expenses — Implementation Constraints v1.0

```text
HISTORICAL INITIAL-DEVELOPMENT BASELINE

This document describes the initial design stage and is not the
current authoritative MVP baseline.

Current authority:
GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
```

```text
TRACK=GM-EXPENSES-INITIAL-DEVELOPMENT-01
```

Non-negotiable rules any implementation agent (human or AI) must obey. These
summarize, but do not replace, the four preceding baseline documents.

## Platform

- Java 25.
- Canonical package root: `com.gypport.business.expenses`, in the final
  hybrid feature-domain + structured-application shape (see the Application
  Architecture Baseline).

## Module boundaries

- No direct compile-time dependency on `gm-entities`, `gm-organizations`, or
  `gm-fleet`.
- No database foreign keys across modules.
- Gystigo Host owns the DataSource, connection pool, MySQL driver,
  transaction manager, and Flyway runtime — `gm-expenses` owns none of
  these.

## Domain purity

- No Spring, no JDBC, no SQL, no persistence annotations anywhere under a
  `domain` package.
- Spring's `DataAccessException` must never escape the Infrastructure
  adapter boundary — translate it to `persistence.RepositoryAccessException`
  before it does.

## Persistence discipline

- No generic `save()` repository method — use explicit, named insert/update
  operations per the actual write being performed.
- Optimistic locking via `version` columns. No `SELECT ... FOR UPDATE`
  unless separately approved.
- Internal `BIGINT` identifiers never escape persistence. Where a record has
  a public identifier, it is UUID-based — but not every table has one:
  `ExpenseCategory` is addressed by `CategoryScope + CategoryCode` instead
  (see the Persistence Baseline, §2).
- No physical `DELETE`. No soft-delete. Append-only history tables where
  defined.
- `expense.advance_reference_frozen` is monotonic (`FALSE → TRUE` only,
  never the reverse) and is physically guarded by a dedicated trigger, not
  just a `CHECK` constraint (see the Persistence Baseline, §9).
- `expense_advance.delivery_method_code` is nullable at rest but
  conditionally required: `NULL` while undelivered, `NOT NULL` once
  `delivered_at` is set — enforced by extending the existing
  `chk_advance_delivered_snapshot` CHECK, the same physical mechanism as
  its sibling delivery-snapshot fields (see the Persistence Baseline,
  §12), not left as an Application-only rule. It is an open,
  pattern-validated code (`^[A-Z][A-Z0-9_]{0,29}$`) — no closed SQL enum,
  no native `ENUM`; the admissible code list is an Application/
  configuration concern, matching `expense_command_receipt.command_type`'s
  existing precedent. It is immutable once set (frozen at delivery, same
  as the other delivery snapshots).

## Transactions and idempotency

- One external command maps to exactly one business transaction.
- Every external write command is idempotent via a UUIDv7 `operationId` and
  a command receipt, per the Application Architecture Baseline.

## API surface

- No generic `UpdateExpense` or `UpdateExpenseStatus` — every mutation is an
  explicit, named Command.

## Explicitly out of scope for this baseline

- No Domain Event Bus. Not event-sourced.
- No Java implementation is authorized by WP-00.
- No schema implementation is authorized by WP-00.

## Provenance discipline

- Chat history with any AI agent is not an implementation source of truth —
  the five documents in this `Fabric/Knowledge/gm-expenses` folder are.
- Do not treat a Host contract documented as work-in-progress (see the
  Cross-Repository Integration Baseline, §Organization Access) as stable
  until a future baseline update says otherwise.

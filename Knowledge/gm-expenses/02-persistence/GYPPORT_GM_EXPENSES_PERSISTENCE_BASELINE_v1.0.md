# GYPPORT gm-expenses — Persistence Baseline v1.0

```text
TRACK=GM-EXPENSES-INITIAL-DEVELOPMENT-01
PHASE_C_STATUS=OWNER_ACCEPTED
```

This document is the final physical persistence design. **No SQL is created
by this document or by WP-00.** It exists so WP-SCHEMA-01 has an unambiguous
target to implement against.

## 1. Engine

```text
ENGINE=MySQL 8.4+
STORAGE_ENGINE=InnoDB
CHARSET=utf8mb4
COLLATION=utf8mb4_0900_ai_ci
```

## 2. Identifiers

| Kind | Representation |
|---|---|
| Internal DB primary key | `BIGINT` signed, `AUTO_INCREMENT` |
| Public ID | `BINARY(16)`, UUIDv7 semantics, generated **outside Domain** by a generator port |

Internal `BIGINT` identifiers must never be exposed to Application or API
layers — where a public identifier is needed, it is the UUID that crosses
that boundary.

```text
PUBLIC_UUID_REQUIRED_FOR_ALL_TABLES=NO

PUBLIC_UUIDS=required for aggregates and externally addressable records
             where explicitly defined
```

Public UUID: `ResponsibleReference`, `VehicleReference`, `ExpenseAdvance`,
`Expense`, `AdvanceSettlement`, `ExpenseDocument`, `ExpenseAdjustment`, and
the reversible settlement financial events (`settlement_adjustment_event`,
`settlement_balance_event`).

**Exception — `ExpenseCategory`**: no public UUID. `ExpenseCategory` is
classification/catalog data, not a record addressed individually — its
business selector is `CategoryScope (GLOBAL | TENANT) + CategoryCode`. Its
`expense_category_id BIGINT` stays persistence-internal, same as any other
internal PK.

## 3. Money

```text
PHYSICAL_TYPE=DECIMAL(19,4)
USD_BUSINESS_SCALE=2
```

## 4. Enumerations

```text
REPRESENTATION=VARCHAR + CHECK constraint
NATIVE_MYSQL_ENUM=NOT USED
```

## 5. Time

```text
TYPE=DATETIME(3)
TIMEZONE=UTC
```

## 6. Optimistic version

```text
TYPE=INT
CONSTRAINT= >= 0
```

## 7. Multitenancy

- `tenant_id` is mandatory on every operational row.
- `organization_scope = COALESCE(organization_id, 0)` — NULL organization
  scope is represented by a generated sentinel scope value, never a bare
  NULL, so that scope-partitioned uniqueness/FK constraints behave
  consistently for PERSONAL-mode rows.
- This sentinel substitution applies **only** to the scope/partition
  dimension. Genuinely optional relationships (e.g. an Expense with no
  Advance) keep real `NULL` — they are not sentinel-substituted.
- Intra-module foreign keys are tenant/scope aware.
- Cross-module database foreign keys are **forbidden**.
  *Amended 2026-09-10 (STEP GYPPORT_DATABASE_CANONICAL_FOUNDATION_RECONCILIATION_09; Gystigo ADR-0014):*
  this was gm-expenses' own MVP design choice. It stays valid for the existing gm-expenses schema, with no
  retrofit. As a general GYPPORT rule it is superseded: a module may reference stable canonical identities
  (tenant, organization, party, user account, shared reference data) through tenant-safe foreign keys when
  its relationship genuinely depends on them.

## 8. Delete policy

```text
PHYSICAL_DELETE=NO
SOFT_DELETE=NO
APPEND_ONLY_HISTORY=YES (where defined)
FK_POLICY=RESTRICT
```

## 9. Physical records (final set)

```text
responsible_reference
vehicle_reference
expense_category
expense_advance
expense
advance_settlement
expense_advance_assignment_event
expense_review_event
expense_revision_event
settlement_adjustment_event
settlement_balance_event
expense_adjustment
expense_document
expense_command_receipt
```

### Expected conceptual counts after all design deltas are consolidated

```text
TABLE_COUNT=14
TRIGGER_COUNT=23
FOREIGN_KEY_COUNT=24
```

`TRIGGER_COUNT` was revised from 22 to 23 after the independent WP-SCHEMA-01
audit of the V11 candidate: the original candidate only guarded
`expense.advance_reference_frozen` with a `CHECK (... IN (0,1))`, which
cannot compare old vs. new row values and therefore cannot prevent a
`TRUE → FALSE` reversal of this monotonic flag (already stated as a rule in
the Domain Baseline, §4). The Owner accepted this finding and added one
`BEFORE UPDATE` trigger on `expense` as a local-row physical guard —
Application still decides *when* the legitimate `FALSE → TRUE` transition
happens; the trigger only makes the reverse transition impossible.

## 10. Audit / event semantics

| Table | Records |
|---|---|
| `expense_advance_assignment_event` | Expense↔Advance `LINKED` / `UNLINKED` / `REASSIGNED` only — **not** advance delivery |
| `expense_review_event` | Expense review lifecycle transitions, plus `EXCLUSION_REASON_AMENDED` |
| `expense_revision_event` | Material Expense field changes (not review transitions) |
| `settlement_adjustment_event` | Authorized shortfall adjustment, and its reversal |
| `settlement_balance_event` | Return / reimbursement registration, and their reversal |
| `expense_adjustment` | Immutable post-terminal financial correction record |
| `expense_document` | Immutable evidence record; replacement is a new record in a replacement chain, never a mutation |
| `expense_command_receipt` | Idempotency ledger for successful external-write commands |

`expense_command_receipt` contract:

```text
result_snapshot: required, JSON object — the authoritative replay response
payload_hash:    SHA-256, BINARY(32)
```

### 10.1 Two complementary audit layers (Owner rule, GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14)

GYPPORT reuses its existing audit infrastructure. No parallel audit architecture,
audit table, generic `updated_by` column or migration is added for it.

- **Domain history** — the semantic, append-only tables above (every one has
  BEFORE UPDATE and BEFORE DELETE refusal triggers). They answer the business
  questions: who decided, when, why and, for material changes, the previous and new
  snapshots. Review transitions go to `expense_review_event`; material field changes to
  `expense_revision_event` (see the domain baseline §4); command execution (actor, time,
  target, committed version) to `expense_command_receipt`.
- **Global / transversal audit** — `audit_logs` (created by core V1; its actor key
  points at the global `user_accounts` since V58) with the action catalog
  `audit_action_types`. It records administrative or system operations: tenant
  context, actor, action code, entity (`entity_name`, `entity_id`, `entity_uuid`,
  `entity_version`), `old_values` / `new_values` JSON, `request_id` /
  `correlation_id`, `ip_address`, `user_agent` and `created_at` (database clock).
  - The actor is the global UserAccount of the execution context. `tenant_id` and
    `user_account_id` are nullable: a `NULL` actor is the canonical system-event
    semantics (GYPPORT_FINAL_CANONICAL_FOUNDATION_REGISTER_v1.0 §6.4), never a
    fabricated account and never a business participant (responsible, supervisor,
    employee, receiver).
  - Domain events are not duplicated into `audit_logs`.
  - State on 2026-09-17: no application port, service or adapter writes `audit_logs`
    yet (ADR-0010 is PROPOSED), and the table has no append-only triggers. Neither
    blocks the MVP: every business audit question is answered by the domain history.
    The first record is the audit of the DEV test-data cleanup of
    GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13, on the local 3310 copy only
    (action `LEGACY_DEV_TEST_DATA_REGULARIZATION`, actor `NULL`).

## 11. Migration decision (final)

The design-evolution artifacts previously referred to as `C5`, `V2`, `V3`,
`V4`, `V5`, `V6` were **design deltas**, not six production Flyway
migrations. No `gm-expenses` migration has been applied to the real
canonical database at any point.

```text
DESIGN_DELTAS_C5_V2_V3_V4_V5_V6=SQUASH_INTO_FIRST_CANONICAL_MIGRATION
```

Verified current Gystigo core Flyway range: `V1..V10` (all foundation/core —
party, RBAC, organization structure, employee, legal verification; none
expense-related).

```text
FLYWAY_INITIAL_GM_EXPENSES_MIGRATION=V11__gm_expenses_initial_schema.sql
```

`V12..V16` are **not** currently reserved or created.

### Rules

```text
BEFORE_FIRST_DEPLOYMENT:
  approved design corrections may be consolidated into V11 freely.

AFTER_A_FLYWAY_MIGRATION_HAS_BEEN_APPLIED:
  never rewrite it; future changes use the next global Flyway version.

FLYWAY_VERSION_NAMESPACE=GLOBAL_MONOTONIC
```

`gm-expenses` uses the **same** GYPPORT multitenant database as every other
module. `SEPARATE_DATABASE_FOR_GM_EXPENSES=NO`.

### Ownership split

```text
schema/domain design owner:   gm-expenses
runtime migration executor:   Gystigo Host
```

### Verified mechanics (why the ownership split works this way)

Gystigo's Flyway configuration (`platform_os/server/src/main/resources/application.yaml`)
scans a single classpath location: `classpath:db/migration`. That folder is
empty in source control — it is populated at Maven build time by an
explicit `<resource>` copy in `platform_os/server/pom.xml`, which currently
copies only `Gystigo/database/core/migration/*.sql` into it.

Final module migration folder:

```text
Gystigo/database/modules/gm-expenses/migration/V11__gm_expenses_initial_schema.sql
```

```text
CORE_REMAINS_FOUNDATION_ONLY=YES
GM_EXPENSES_MIGRATIONS_IN_CORE_MIGRATION=NEVER
```

This location is compatible with the existing mechanism **only after** a
matching `<resource>` block is added to `platform_os/server/pom.xml` (a
Gystigo-repo change, scheduled for WP-SCHEMA-01 implementation, not made by
this document, by WP-00, or by this reconciliation).

**Why this is stated this firmly**: the independently-audited V11 candidate
was found sitting directly inside `Gystigo/database/core/migration/` —
technically loadable with zero pom.xml change only because that folder is
already copied to the classpath, but mixing gm-expenses schema into the
foundation/core migration lineage. The Owner rejected that placement and
confirmed the module-owned folder above as final.

**Open point carried forward, not resolved here**: because both the core
and (future) gm-expenses resource blocks would copy into the same merged
`db/migration` classpath folder feeding one shared Flyway schema-history
table, migration version numbers must stay globally unique across every
module, not just within `gm-expenses`. `V11` is confirmed clear of the
existing `V1..V10` core range at the time of writing; nothing beyond that
one number has been reserved or coordinated.

## 12. Pending post-V11 changes

`V11` is applied and immutable (§11). Anything discovered afterward lands
in a new, forward-only migration under the same global monotonic
namespace — never a rewrite of `V11`.

### Advance delivery method (expected `V12`)

Discovered by reconciling the approved UX against the already-applied
`V11` schema: `expense_advance` has no column recording *how* delivered
funds were handed over. Final decision:

```text
COLUMN=delivery_method_code
TYPE=VARCHAR(30)
PATTERN=^[A-Z][A-Z0-9_]{0,29}$
CLOSED_ENUM=NO
NATIVE_MYSQL_ENUM=NO
```

This reuses two idioms already present in `V11` rather than inventing a
new one: the open-code shape (no closed `CHECK IN (...)` enum) matches
`expense_command_receipt.command_type`, whose own comment states the
admissible values are deliberately left to Application/configuration; the
regex shape matches `expense_category.category_code`'s existing
constraint, just scaled to a 30-character column.

Delivery-state invariant — extends the existing
`chk_advance_delivered_snapshot` group on `expense_advance` (the same
physical mechanism already guarding `responsible_snapshot_name`,
`rendition_due_at`, and the vehicle snapshot fields), rather than being
left as an Application-only rule:

```text
delivered_at IS NULL     → delivery_method_code MUST be NULL
delivered_at IS NOT NULL → delivery_method_code MUST NOT be NULL
```

```text
V11_REWRITE_ALLOWED=NO
NEXT_EXPECTED_FLYWAY_VERSION=V12
EXPECTED_FILE=V12__gm_expenses_add_advance_delivery_method.sql
```

`V12` adds this column and extends/recreates the delivered-snapshot
`CHECK`; it must not alter any other `V11` structure. Not created by this
document — schema implementation is a separate, later work package.

### Advance planned delivery (`V62`)

GM_EXPENSES_FINAL_ADJUSTMENT_V62_04 (Owner-approved option A of
IMPLEMENTATION_02 §32). A `BORRADOR` stores the delivery plan chosen when it
is registered, without relaxing the `V12` delivered-snapshot invariant:

```text
COLUMN=planned_delivery_method_code  TYPE=VARCHAR(30) NULL  PATTERN=^[A-Z][A-Z0-9_]{0,29}$
COLUMN=planned_rendition_days        TYPE=SMALLINT NULL     RANGE=1..365
CHECK=chk_advance_planned_delivery_method_code
CHECK=chk_advance_planned_rendition_days
CHECK=chk_advance_planned_delivery_pair (both NULL or both NOT NULL)
EXISTING_ROWS=NULL (no plan recorded; no data rewrite)
FILE=V62__gm_expenses_advance_planned_delivery.sql
```

`delivery_method_code` and `rendition_due_at` keep meaning what actually
happened at `DELIVER`; the plan columns are written with the draft and never
rewritten.

### Unified settlement reconciliation (`V63`)

GM_EXPENSES_UNIFIED_RECONCILIATION_V63_05 (Owner-approved option A; Domain
Baseline RN-001). A real return and a later reimbursement may both be positive
on one `advance_settlement`, and a `RECONCILED` row satisfies one equation:

```text
DROPPED=chk_settlement_return_reimburse
RECREATED=chk_settlement_reconciled_equation
  reconciliation_result <> 'RECONCILED'
  OR advance_amount_snapshot + reimbursement_amount
     = justified_expense_total + returned_amount + authorized_adjustment_total
UNCHANGED=chk_settlement_adjustment_shortfall_only (reimbursement_amount = 0 OR authorized_adjustment_total = 0)
DATA_REWRITE=NONE (every V11 branch is a special case of the unified equation)
FILE=V63__gm_expenses_unified_settlement_reconciliation.sql
```

Both CHECK changes run in one `ALTER TABLE`. The fresh baseline `B17` carries
the same V11 constraint names, so both migration lineages reach the same
schema.

### ExpenseCase business number (`V64`)

*Owner decision of GM_EXPENSES_FINAL_MVP_CLOSURE_22. Additive; no existing column, constraint, trigger or row value is
altered and no financial table is touched.*

```text
expense_case.case_business_date  DATE NOT NULL          - the persisted business day
expense_case.case_sequence       SMALLINT UNSIGNED NOT NULL - 1..9999 within tenant and that day
expense_case.case_number         CHAR(12) ascii, STORED generated from the two columns above
UNIQUE (tenant_id, case_number)              UNIQUE (tenant_id, case_business_date, case_sequence)
CHECK case_sequence BETWEEN 1 AND 9999       CHECK (case_business_date IS NULL) = (case_sequence IS NULL)
expense_case_number_sequence (tenant_id, case_business_date, last_sequence, updated_at), PK (tenant_id, case_business_date)
  CHECK last_sequence BETWEEN 1 AND 9999     no FK to tenants: the module references the tenant by value
TRIGGER trg_expense_case_business_number_immutable  BEFORE UPDATE - the number is history
TRIGGER trg_case_number_sequence_no_delete          BEFORE DELETE - the counter is never removed
```

The number is generated, not written by the application: `case_number` is a stored generated column, so its parts and
its visible value cannot drift apart. The application only allocates the sequence, with one statement that both locks
and advances the counter row (`INSERT ... ON DUPLICATE KEY UPDATE last_sequence = LAST_INSERT_ID(last_sequence + 1)`)
inside the creating transaction.

Backfill: every existing Case took the UTC day of its `created_at` - the day its users already saw - ordered by
`created_at`, then `expense_case_id`. Rehearsed on a disposable copy of Shared DEV V63: 30 of 30 Cases numbered, 0
duplicates, the six financial tables byte-identical before and after (CHECKSUM TABLE), the counter seeded with no gap.

### ExpenseCase permanent sequence (`V65`)

*Owner decision of GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25. Additive; V64 and everything before it are
untouched, and no financial table is read or written.*

```text
expense_case.expense_sequence       INT UNSIGNED NOT NULL - the permanent number inside the tenant ("EXP. NN")
UNIQUE (tenant_id, expense_sequence)          CHECK expense_sequence >= 1
expense_case_permanent_sequence (tenant_id, last_sequence, updated_at), PK (tenant_id)
  CHECK last_sequence >= 1                     no FK to tenants, as V64's counter
TRIGGER trg_expense_case_expense_sequence_immutable  BEFORE UPDATE - the number is history
TRIGGER trg_case_permanent_sequence_no_delete       BEFORE DELETE - the counter is never removed
```

Two counters, never one: `expense_case_number_sequence` (V64) is keyed by tenant and business date and restarts every
day to compose `case_number`; `expense_case_permanent_sequence` (V65) is keyed by the tenant alone and never restarts.
Both are advanced with the same one-statement pattern (`INSERT ... ON DUPLICATE KEY UPDATE last_sequence =
LAST_INSERT_ID(last_sequence + 1)`) inside the creating transaction; the permanent row is taken first, so two creations
never wait on each other's rows in opposite orders. A creation that rolls back rolls its counter back with it, so the
committed numbers run without holes.

Backfill: every existing Case was numbered within its tenant by `created_at`, then `expense_case_id` - its real creation
order - with the business date, the daily sequence, the business number and `created_at` read and never written.

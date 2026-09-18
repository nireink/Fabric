# GYPPORT gm-expenses — Application Architecture Baseline v1.0

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

## 1. Canonical Java root

```text
com.gypport.business.expenses
```

## 2. Final package model

```text
FINAL_PACKAGE_MODEL=HYBRID_FEATURE_DOMAIN_PLUS_STRUCTURED_APPLICATION
```

This supersedes an earlier layer-first proposal (top-level `domain` with a
subpackage per feature). It is final.

```text
com.gypport.business.expenses
├── advance
│   └── domain
├── expense
│   └── domain
├── settlement
│   └── domain
├── reference
│   └── domain
├── catalog
│   └── domain
├── adjustment
│   └── domain
├── document
│   └── domain
├── common
│   └── domain
├── application
│   ├── advance
│   ├── expense
│   ├── settlement
│   ├── reference
│   ├── catalog
│   ├── adjustment
│   ├── document
│   ├── idempotency
│   ├── port
│   │   ├── query
│   │   ├── security
│   │   ├── policy
│   │   └── storage
│   └── exception
├── persistence
│   └── RepositoryAccessException
└── infrastructure
    └── persistence
        └── jdbc
```

### Why this shape

- The only verified multi-aggregate precedent on the platform (`gm-entities`)
  uses feature-first packaging (`<feature>.domain`), not a top-level `domain`
  with feature subpackages. This baseline follows that precedent.
- Repository ports representing an aggregate's own persistence belong beside
  that aggregate's `domain` package (matching `gm-entities` and
  `gm-organizations`, where `OrganizationRepository` / `OrganizationQueryPort`
  live in `domain`, not in `application.port`).
- Cross-row / cross-aggregate query ports (queries that don't belong to a
  single feature's own repository) belong under `application.port`.
- `RepositoryAccessException` belongs in a top-level `persistence` package,
  sibling to `domain`/`application`/`infrastructure` — this exact shape is
  unanimous across every real implementation checked (`gm-entities`,
  `gm-organizations`, and Gystigo's own native `organization access` code).

### Layer rules

**Domain** (each `<feature>.domain` and `common.domain`):
- Java standard library only.
- No Spring. No JDBC. No SQL. No DataSource. No MySQL classes. No
  persistence annotations.

**Application**:
- Orchestrates use cases.
- Coordinates ports (repository, query, security, policy, storage).
- Owns cross-aggregate transaction logic and declares transaction
  boundaries.

**Infrastructure**:
- JDBC adapters. Spring JDBC is allowed here only.
- `DataAccessException` is translated to `persistence.RepositoryAccessException`
  before it leaves the adapter boundary — it must never reach Application or
  Domain.

## 3. Transaction model

```text
ONE_EXTERNAL_COMMAND_ONE_BUSINESS_TRANSACTION=YES
TRANSACTION_MANAGER_OWNER=GYSTIGO_HOST
FINANCIAL_REQUIRES_NEW_ALLOWED=NO
```

Concurrency is optimistic locking only. `SELECT ... FOR UPDATE` is not used
unless separately approved.

```text
PRE_SETTLEMENT_COORDINATOR:  ExpenseAdvance.version
POST_SETTLEMENT_COORDINATOR: AdvanceSettlement.version
Expense changes:             Expense.version, where applicable
```

### Cross-resource coordination order

```text
TYPE_RANK:
  0 = SETTLEMENT
  1 = ADVANCE
  2 = EXPENSE

then: ascending canonical public UUID bytes
```

Internal `BIGINT` identifiers are never used by Application for
coordination ordering.

### Reconciliation invalidation

Any financial input mutation invalidates reconciliation atomically —
`reconciliation_result` reverts to `PENDING`. Triggers include: Expense
approval/reopen, amount correction, link/unlink/reassign, return,
reimbursement, authorized adjustment, and any of their reversals.

`CLOSE_SETTLEMENT`:
1. Recalculates current inputs.
2. Re-evaluates RN-001.
3. Verifies every linked Expense is `APROBADO` or `EXCLUIDO`.
4. Closes the Settlement and the Advance atomically, in one transaction.

```text
PERSISTED_FINANCIAL_FINGERPRINT=NO
```

Reason: `version` plus atomic reconciliation invalidation plus full
transactional recalculation already make a persisted fingerprint redundant.

## 4. Idempotency model

Every external write command requires an `operationId` (UUIDv7).

```text
Outer: IdempotentCommandExecutor
Inner: TransactionalHandler
```

- The receipt is inserted in the **same** transaction as the successful
  business command. A failed command leaves no receipt.
- Same `operationId` + same command/payload → return the stored original
  `result_snapshot`.
- Same `operationId` + different command/payload → `IdempotencyConflictException`.
- Concurrent duplicates: one transaction wins the UNIQUE key; the loser
  rolls back; the outer executor reloads the committed receipt and returns
  the same result.

```text
CommandResultCodec payload hash contract: byte[32], SHA-256
```

## 5. Command coverage (final — exhaustive, not an estimate)

```text
ADVANCE:        Create, EditDraft, Deliver, Cancel

EXPENSE:        Register, Link, Unlink, Reassign, SubmitForReview, Accept,
                Observe, Reject, RemoveFromReview, Exclude, Reinstate,
                ReopenApproved, AmendExclusionReason, EditRegistered,
                CorrectObserved, CorrectRejected

DOCUMENT:       Attach, RegisterUnavailable, Replace

SETTLEMENT:     Start, RegisterReturn, ReverseReturn, RegisterReimbursement,
                ReverseReimbursement, RegisterAuthorizedAdjustment,
                ReverseAuthorizedAdjustment, Reconcile, Close

EXPENSE
ADJUSTMENT:     Increase, Decrease, Void

RESPONSIBLE:    Create, Update, Activate, Deactivate, LinkCanonicalParty

VEHICLE:        Create, Update, Activate, Deactivate, LinkCanonicalFleetVehicle

CATEGORY:       CreateTenantCategory, Rename, ChangePolicies, Activate, Deactivate
```

No generic `UpdateExpense` or `UpdateExpenseStatus` exists or is planned —
every mutation is an explicit, named Command.

## 6. Evidence query responsibility

```text
ExpenseEvidenceQueryPort
PACKAGE=com.gypport.business.expenses.application.port.query
LAYER=APPLICATION
```

`ExpenseEvidenceQueryPort` is the Application-layer port through which
Application determines the *effective evidence state* of an `Expense`. It is
not a Domain repository, not `DocumentStoragePort`, not a JDBC adapter, and
not an `Expense` or `ExpenseDocument` responsibility.

Its future responsibility includes resolving, for a given Expense,
information such as:

- whether any evidence exists at all
- whether the current effective evidence is stored evidence (`FACTURA` /
  `TICKET` / `RECIBO`) or a `NO_DISPONIBLE` declaration
- whether a document has been superseded by its replacement in the
  replacement chain
- whether the effective evidence satisfies the review prerequisite implied
  by `ExpenseCategoryPolicySnapshot.requiresReceipt`

The exact interface methods are intentionally not frozen here, matching the
granularity of the rest of this document — they belong to the Application
work package that implements this port. Only the type name, package, and
layer ownership are canonical as of this reconciliation.

```text
Expense.requiresReceipt
        +
ExpenseEvidenceQueryPort
        v
Application review policy
```

`ExpenseCategoryPolicySnapshot.requiresReceipt` does **not** block
`Expense.register()` or any other Domain mutation — confirmed by the
already-implemented `Expense` aggregate, which contains no document-related
check anywhere. `Expense` Domain never queries documents, and
`ExpenseDocument` Domain never decides Expense review eligibility. Evidence
sufficiency is exclusively an Application review-policy decision, made
through `ExpenseEvidenceQueryPort`.

`ExpenseEvidenceQueryPort` and `DocumentStoragePort` are distinct concerns
and must not be merged:

| Port | Boundary | Responsibility |
|---|---|---|
| `DocumentStoragePort` | Application storage boundary | Obtains the authoritative `StoredDocumentDescriptor` / storage reference before an `ExpenseDocument` is persisted. The client never supplies an authoritative `storageReference` (see the Cross-Repository Integration Baseline, §3, for the full trust-boundary flow). |
| `ExpenseEvidenceQueryPort` | Application query boundary | Reads the effective evidence state already persisted via `ExpenseDocument`. |

# GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14
MODE=AUDIT_EXISTING_ARCHITECTURE_THEN_TARGETED_FINALIZATION
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
REVIEWS=GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13 (two indicators correct; placement changes; audit reuse correction)
OWNER_DECISIONS=reuse the existing global audit infrastructure plus semantic domain histories (no parallel audit architecture, no V64, no new audit table or columns); audit the STEP 13 DEV cleanup through the existing global audit mechanism without fabricating an actor or timestamp; tracked permanent safe local launcher; Conciliado = Case lifecycle indicator above the divider, Uso = Finanzas metric
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FINAL_12_BASELINE_REUSED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — FINAL PRE-COMMIT AUDIT REUSE + LOCAL SAFETY + CASE CARD LAYOUT

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14

MODE=
AUDIT_EXISTING_ARCHITECTURE_THEN_TARGETED_FINALIZATION

OWNER_AUTHORIZED=YES

PURPOSE=

Close the remaining pre-commit items without creating duplicate architecture:

A. Reuse the EXISTING GYPPORT audit infrastructure correctly.
B. Make the safe LOCAL launcher permanent/tracked.
C. Place Conciliado and Uso in their correct semantic areas.
D. Freeze the already-proven OBSERVADO history integrity behavior.

Do NOT migrate Shared DEV.
Do NOT commit.
Do NOT push.

============================================================
0. IMPORTANT CORRECTION — AUDIT ALREADY EXISTS
============================================================

Do NOT design a new audit architecture.

Do NOT add audit columns merely because fields such as updated_by are absent.

Do NOT create a new audit table.

GYPPORT already has an audit/history architecture.

Previous gm-expenses design includes, among the existing mechanisms:

    ExpenseAuditTrailPort

and semantic append-only histories including:

    expense_review_event
    expense_revision_event
    expense_advance_assignment_event
    settlement_adjustment_event
    settlement_balance_event

The current implementation also proves that review events already preserve:

    tenant
    expense
    event type
    actor
    occurred_at
    reason
    notes

with append-only protections.

FIRST locate and document the ACTUAL current implementations in the repository.

Do not assume names from this prompt are still exact if the code has since
been renamed.

============================================================
1. LOCATE THE EXISTING GLOBAL AUDIT TABLE / PORT
============================================================

The Owner confirms GYPPORT already has a transversal/general audit table.

Locate the ACTUAL implementation before editing.

Audit:

- physical table name;
- migration that created it;
- domain/application port;
- JDBC adapter;
- Host/service used to write it;
- required actor fields;
- tenant / organization context;
- operation/action code;
- timestamp source;
- entity/resource reference;
- before/after or metadata payload support;
- operationId/correlationId support if present;
- append-only/delete protections.

DO NOT invent:

    audit_log
    audit_event
    audit_trail

as a physical name.

Use the REAL existing object.

Return its exact identity in the report.

============================================================
2. AUDIT RESPONSIBILITY SPLIT
============================================================

Preserve two complementary layers.

A. DOMAIN HISTORY

Used when the event itself is part of Expenses business meaning.

Examples:

    SUBMITTED
    OBSERVED
    CORRECTION_SUBMITTED
    ACCEPTED
    REJECTED

and existing Expense revision / settlement / assignment histories.

These remain in their existing semantic history tables.

B. GLOBAL / TRANSVERSAL AUDIT

Used to answer:

    who performed an administrative/system operation;
    when;
    against which tenant/entity;
    which action;
    relevant before/after metadata;
    correlation / operation context.

Do NOT duplicate every domain event into a second parallel event model unless
the existing audit contract already intentionally does that.

Follow the established GYPPORT audit architecture.

============================================================
3. ACTOR SEMANTICS
============================================================

Audit actor is always the canonical GLOBAL UserAccount / execution actor.

Use the existing:

    ExecutionContext / CommandContext / authenticated principal

semantics.

Do NOT use:

- Responsible Party
- Supervisor Party
- Employee Party
- Receiver Party

as audit actor merely because they appear in the business record.

Business participants and audit actor remain distinct.

============================================================
4. KNOWN LEGACY TEST EXPENSE
============================================================

Known local test Expense was:

    state = OBSERVADO
    review history = missing

It has already been classified:

    LEGACY_DEV_TEST_DATA

Current modern code has proven:

    CURRENT_CODE_CAN_CREATE_OBSERVED_WITHOUT_HISTORY=NO

and:

    OBSERVE_TRANSACTION_ATOMIC=YES

The local copy on 3310 was changed to:

    RECHAZADO

through a guarded DEV cleanup.

Do NOT invent an OBSERVED event.

Do NOT invent a historical reviewer.

Do NOT invent a historical rejection date.

============================================================
5. AUDIT THE ALREADY-PERFORMED DEV CLEANUP
============================================================

Because this administrative cleanup changed a record, it must use the EXISTING
global GYPPORT audit mechanism.

First inspect the evidence already captured for the cleanup:

- Expense id
- tenant
- before state / version
- after state / version
- actual cleanup timestamp
- actual execution context
- reason

Use only FACTUAL evidence.

Required audit semantic:

    action =
        LEGACY_DEV_TEST_DATA_REGULARIZATION

or the closest EXISTING canonical audit action/code.

Entity:

    Expense

Before:

    OBSERVADO
    version 2

After:

    RECHAZADO
    version 3

Reason:

    Test record created before canonical review-history persistence.

IMPORTANT:

If the existing global audit table requires a UserAccount actor and the actual
cleanup did NOT have a valid canonical UserAccount actor:

    DO NOT fabricate one.

Use the existing SYSTEM/MAINTENANCE actor semantics if GYPPORT already
supports them.

If no such canonical semantics exist:

    STOP this one audit insertion and report the exact gap.

Do not invent an actor just to fill a NOT NULL column.

============================================================
6. NO NEW LEGACY PRODUCT FEATURE
============================================================

Do NOT add:

    LEGACY_OBSERVED_REGULARIZED

as a permanent normal Expense workflow event.

Do NOT introduce a new normal UI flow.

This was DEV/test-data cleanup.

The permanent product guarantee is instead:

    OBSERVADO state
    +
    OBSERVED event

written atomically.

============================================================
7. FREEZE MODERN REVIEW INTEGRITY
============================================================

Preserve the proven current flow:

ObserveExpenseReviewUseCase
    ↓
same transaction
    ├── Expense state → OBSERVADO
    └── review history → OBSERVED

Actor:
    authenticated global UserAccount

Time:
    canonical server clock

If history persistence fails:

    whole transaction rolls back.

Keep the real-DB regression test that proves this.

============================================================
8. EXPENSE REVISION AUDIT
============================================================

Re-audit the existing Expense revision mechanism.

Previous design already uses:

    ExpenseRevisionChange

with previous/new ExpenseDetails snapshots.

Ensure corrections/edits continue to use that existing mechanism.

Do NOT create:

- another changes table;
- another event-sourcing model;
- free mutable fields without revision evidence.

Canonical principle:

    edit/correction
        → preserve previous state
        → preserve new state
        → actor/context
        → immutable history

using the EXISTING implementation.

============================================================
9. AUDIT GAPS — DO NOT AUTOMATICALLY CREATE V64
============================================================

The previous report noted:

    expense has no generic updated_by
    review_event has no second DB insertion timestamp beside occurred_at

These facts alone DO NOT justify schema changes.

If existing global audit + semantic history already answer:

    who
    when
    what
    why
    before/after where required

then:

    AUDIT_GAP=NONE_FOR_MVP

Do NOT create V64.

Only report a blocking gap if there is an actual business/audit question that
cannot be answered by the existing architecture.

============================================================
PART B — PERSISTENT SAFE LOCAL LAUNCHER
============================================================

10. CURRENT PROBLEM
============================================================

The hardened safe launcher currently exists only under:

    target/

That directory is ephemeral and may be removed by:

    mvn clean

The safety control must be tracked and permanent.

============================================================
11. LOCATE CANONICAL SCRIPT HOME
============================================================

Audit Gystigo for the existing tracked scripts/tooling structure.

Use the existing canonical location.

Do NOT invent a parallel scripts hierarchy.

Create/move the final local launcher there.

Conceptually:

    Start-GypportLocal.ps1

but follow actual repository naming conventions.

There must be ONE obvious canonical LOCAL launcher.

============================================================
12. LOCAL LAUNCHER CONTRACT
============================================================

The tracked launcher must explicitly resolve:

    ENV=LOCAL_EDUARDO
    DB_HOST=127.0.0.1
    DB_PORT=3310
    DB_NAME=gypport_runtime_local

Credentials:

    use existing safe local/gitignored source.

Never hardcode secrets into tracked files.

Never depend on global Windows User datasource variables.

============================================================
13. SHARED DEV FAIL-CLOSED GUARD
============================================================

Before Java starts, abort if resolved datasource identifies Shared DEV.

At minimum refuse:

    :3308
    gypport-mysql-dev
    core_business_dev

Message:

    "Local runtime refused to start because the datasource points to Shared DEV."

Verify Java never starts after refusal.

============================================================
14. CLEAN-SURVIVAL TEST
============================================================

Prove:

    mvn clean

does NOT delete the canonical launcher.

target/ may contain:

- PID
- logs
- generated jar
- scratch

but not the only copy of the safety launcher.

============================================================
PART C — FINAL CASE CARD SEMANTIC LAYOUT
============================================================

15. OWNER VISUAL DECISION
============================================================

The two independent indicators are correct.

Their current placement must change.

OWNER WANTS:

CASE HEADER / CONTEXT:

                                      Cerrado

                                      Conciliado
                                      100%   │BAR│

-----------------------------------------------------------
DIVIDER

Finanzas

Entregado          Usado          Justificado          Uso
USD ...            USD ...        USD ...              87% │BAR│

Devuelto           Reembolsado    Pendiente...

============================================================
16. CONCILIADO BELONGS TO CASE HEADER
============================================================

Conciliado is a CASE-LIFECYCLE indicator.

Place it ABOVE the horizontal divider.

Visually associate it with:

    Abierto / Cerrado

For CLOSED + financially resolved:

    Conciliado
    100%
    full independent bar

For OPEN:

    Conciliado
    Pendiente
    empty independent bar

Do NOT invent an intermediate percentage.

============================================================
17. USO BELONGS TO FINANZAS
============================================================

Uso is a FINANCIAL metric.

Place it BELOW the divider inside:

    Finanzas

It retains its own independent progress bar.

Calculation:

    used / delivered

Examples:

    29%
    87%
    110%

Numeric text may exceed 100%.

Visual fill:

    clamp to 100%.

No delivered Advance:

    Uso 0%
    empty bar.

============================================================
18. DO NOT STACK BOTH TOGETHER
============================================================

Do NOT render:

    Conciliado
    [bar]
    Uso
    [bar]

as one combined right-side block crossing the semantic divider.

They are independent indicators in different semantic regions.

============================================================
19. RESPONSIVE
============================================================

Verify:

    1280
    768
    375
    320

At narrow widths:

- layout may wrap;
- Conciliado remains associated with the Case header/status;
- Uso remains within Finanzas;
- neither disappears;
- bars remain independent;
- no horizontal overflow.

============================================================
20. EXPECTED REAL EXAMPLES
============================================================

Compra Teléfono CLOSED:

HEADER:
    Cerrado
    Conciliado 100%
    full bar

FINANZAS:
    Entregado USD 300
    Usado USD 260
    Justificado USD 260
    Devuelto USD 40
    Reembolsado USD 0
    Pendiente USD 0
    Uso 87%
    87% bar

Viaje Loja CLOSED:

HEADER:
    Cerrado
    Conciliado 100%

FINANZAS:
    Uso 29%
    own bar

Open overuse:

HEADER:
    Abierto
    Conciliado Pendiente
    empty bar

FINANZAS:
    Uso 110%
    text = 110%
    visual fill = 100%

============================================================
21. BASELINE REUSE
============================================================

No financial/domain/migration behavior should change.

Reuse:

    FINAL_12 migration + financial baseline.

Do NOT rerun V43→V63.

Run only:

- audit architecture verification;
- existing/new audit-focused tests if needed;
- affected Studio contracts;
- Studio full contracts if inexpensive;
- ESLint;
- responsive fixtures;
- launcher safety tests;
- local runtime health.

============================================================
22. CANONICAL DOCUMENTATION
============================================================

Update Fabric to explicitly state:

AUDIT:
    GYPPORT reuses the existing global audit infrastructure plus domain
    semantic histories; no parallel audit architecture.

EXPENSE REVIEW:
    OBSERVADO + OBSERVED are atomic.

EXPENSE REVISION:
    existing revision snapshots remain canonical.

ENV:
    LOCAL must never inherit Shared DEV globally.

UI:
    Conciliado = Case lifecycle indicator.
    Uso = Finanzas metric.

Reglas.md:

append only if these decisions are not already captured by the previous
entries.

Do NOT duplicate equivalent rules unnecessarily.

============================================================
23. SCOPE
============================================================

No V64.

No new audit table.

No new generic updated_by columns unless a proven blocker requires them and
Owner separately approves.

No Shared DEV write.

No migration.

No staging.
No commit.
No push.

============================================================
24. REQUIRED REPORT
============================================================

Return:

STATUS=
READY_FOR_OWNER_FINAL_PRECOMMIT_REVIEW

AUDIT:
GLOBAL_AUDIT_TABLE_EXACT_NAME=
GLOBAL_AUDIT_PORT_OR_SERVICE=
GLOBAL_AUDIT_ACTOR_SOURCE=
GLOBAL_AUDIT_TIMESTAMP_SOURCE=
GLOBAL_AUDIT_BEFORE_AFTER_SUPPORT=

EXPENSE_AUDIT_TRAIL_PORT_FOUND=
EXPENSE_REVIEW_HISTORY_MODEL=
EXPENSE_REVISION_HISTORY_MODEL=

PARALLEL_AUDIT_ARCHITECTURE_CREATED=NO
NEW_AUDIT_TABLE_CREATED=NO
NEW_AUDIT_COLUMNS_CREATED=NO
V64_CREATED=NO

KNOWN_TEST_DATA_CLEANUP_AUDITED=
CLEANUP_AUDIT_ACTION=
CLEANUP_ACTOR_FABRICATED=NO
CLEANUP_HISTORICAL_TIMESTAMP_FABRICATED=NO

OBSERVED_ATOMICITY_PRESERVED=
AUDIT_GAPS_BLOCKING_MVP=

ENVIRONMENT:
TRACKED_LOCAL_LAUNCHER=
LAUNCHER_SURVIVES_MVN_CLEAN=
LOCAL_DB_TARGET=3310
SHARED_DEV_GUARD=
BACKEND_CONNECTIONS_3308=0

UI:
CASE_HEADER_CONCILIATED_INDICATOR=
FINANCE_BODY_USAGE_INDICATOR=
DUAL_BARS_INDEPENDENT=
OPEN_CASE_CONCILIATED=PENDIENTE
CLOSED_CASE_CONCILIATED=100%
USAGE_OVER_100=TEXT_REAL_BAR_CLAMPED

RESPONSIVE_RESULTS=

TEST_RESULTS=

FINAL_12_BASELINE_REUSED=YES

SHARED_DEV_VERSION=V43
SHARED_DEV_MODIFIED=NO

FILES_STAGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

READY_FOR_CONTROLLED_COMMIT_GATE=YES/NO

STOP_FOR_OWNER_REVIEW=YES

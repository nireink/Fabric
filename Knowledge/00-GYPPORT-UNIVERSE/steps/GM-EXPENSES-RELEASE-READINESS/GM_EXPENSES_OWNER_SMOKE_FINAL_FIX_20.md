# GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20
MODE=AUDIT_CONFIRM_THEN_IMPLEMENT_THEN_VERIFY
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner decisions after GM_EXPENSES_OWNER_SMOKE_FINDINGS_19
ACCEPTED_BASELINE=gm-expenses 545eae0, Gystigo bcb9591, Fabric bbdd66a, Shared DEV V63
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES OWNER SMOKE FINAL CORRECTIONS

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20

MODE=
AUDIT_CONFIRM → IMPLEMENT → VERIFY

OWNER_AUTHORIZED=YES

PURPOSE=

Implement the final functional corrections discovered during the real Owner
smoke of gm-expenses before freezing the MVP.

This STEP contains TWO Owner-approved corrections:

A. Financial reconciliation semantics and real Return/Reimbursement movements.
B. Persistent ExpenseCase business numbering ("ID Gasto") with tenant and
   establishment traceability.

These decisions supersede any earlier interpretation that treats a rejected
expense as a Return, Advance, reimbursement or other cash movement.

============================================================
0. ACCEPTED BASELINE / CONTINUITY
============================================================

Current accepted/deployed baseline:

GM_EXPENSES_COMMIT=
545eae0fb287f8e04f7f1b4ac73780304ec53f22

GYSTIGO_COMMIT=
bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f

FABRIC_COMMIT=
bbdd66a0c5a1c9cbb21293beb74c3e5e61cc5de0

Shared DEV:
    V63

Official DEV backend:
    rebuilt from accepted commits

Automated Shared DEV smoke:
    37/37 PASS

Owner smoke Case:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0
    "Compra Filtro"

STEP 19 established read-only that the current Case contains:

    delivered = USD 320
    approved/justified = USD 400
    stored Return = USD 300
    reimbursed = USD 0

The stored USD 300 Return was NOT a real cash return according to the Owner.

Do NOT preserve that mistaken business interpretation as canonical.

============================================================
1. OWNER CANONICAL FINANCIAL RULE
============================================================

The reconciliation model must clearly separate:

1. FUNDING
2. EXPENSES
3. REAL CASH CLOSING MOVEMENTS

Canonical definitions:

TOTAL_ADVANCES =
    SUM(all DELIVERED Advances for the Case/currency)

TOTAL_EXPENSES =
    SUM(all APROBADO Expenses for the Case/currency)

REJECTED_EXPENSE_FINANCIAL_EFFECT =
    ZERO

OBSERVED_EXPENSE_FINANCIAL_EFFECT =
    ZERO until approved

PENDING_REVIEW_EXPENSE_FINANCIAL_EFFECT =
    ZERO until approved

REGISTERED_EXPENSE_FINANCIAL_EFFECT =
    ZERO until approved

A rejected/cancelled expense:

- remains in immutable history;
- is visible operationally where appropriate;
- contributes ZERO to reconciliation;
- does NOT become an Advance;
- does NOT create a Return;
- does NOT create a Reimbursement;
- does NOT create an Adjustment merely because it was rejected.

============================================================
2. IMPORTANT — DO NOT DOUBLE SUBTRACT REJECTED EXPENSES
============================================================

Do NOT implement:

    Total Gastos = Approved - Rejected

if Approved already means the APROBADO set.

Correct:

    Total Gastos = SUM(APROBADO)

Rejected Expenses are already excluded.

Example:

Expenses:
    200 RECHAZADO
     30 APROBADO
     90 APROBADO
     80 APROBADO
    200 APROBADO

TOTAL_EXPENSES =
    30 + 90 + 80 + 200
    = 400

The rejected 200 has financial effect 0.

============================================================
3. BASE RECONCILIATION
============================================================

Introduce/standardize the explicit derived concept:

    BASE_RECONCILIATION_BALANCE

Formula:

    BASE_RECONCILIATION_BALANCE =
        TOTAL_ADVANCES - TOTAL_EXPENSES

Owner-facing concept:

    Total a conciliar

Direction:

If > 0:
    POR_DEVOLVER

If < 0:
    POR_REEMBOLSAR

If = 0:
    BALANCEADO

For the Owner smoke Case after correcting the false Return:

    Total anticipos = 320
    Total gastos    = 400

    320 - 400 = -80

Therefore:

    POR_REEMBOLSAR = USD 80.00

============================================================
4. REAL CASH MOVEMENTS ARE SEPARATE
============================================================

Return and Reimbursement represent REAL movement of money.

RETURN means:

    the responsible person actually returned money to the company.

REIMBURSEMENT means:

    the company actually paid the responsible person additional money.

They are NOT derived automatically from:

- Rejecting an Expense;
- Observing an Expense;
- Correcting an Expense;
- Approving/Rejecting review;
- cancelling an Expense.

They require an explicit user operation.

The final pending balance may continue to follow the existing conservation
equation:

    FINAL_BALANCE =
        TOTAL_ADVANCES
        + TOTAL_REIMBURSED
        - TOTAL_EXPENSES
        - TOTAL_RETURNED
        - TOTAL_ADJUSTMENTS

But expose separately:

    BASE_RECONCILIATION_BALANCE =
        TOTAL_ADVANCES - TOTAL_EXPENSES

This separation is important.

============================================================
5. OWNER SMOKE NUMERIC PROOFS
============================================================

Require tests for:

CASE A

    Advances:
        200 + 100 + 20 = 320

    Approved Expenses:
        30 + 90 + 80 + 200 = 400

    Rejected:
        200

Expected:

    Total anticipos = 320
    Total gastos = 400
    Rejected impact = 0
    Total a conciliar = -80
    Direction = POR_REEMBOLSAR
    Amount = 80

CASE B

    Advances = 320
    Approved Expenses = 200
    Rejected Expenses = 200

Expected:

    Total gastos = 200
    Total a conciliar = +120
    Direction = POR_DEVOLVER
    Amount = 120

CASE C

    Advances = 320
    Approved Expenses = 400
    Real Return = 0
    Real Reimbursement = 80

Expected:

    Final balance = 0

CASE D

    Advances = 320
    Approved Expenses = 400
    Real Return = 100

Expected before reimbursement:

    Base balance = -80

    Final balance =
        320 - 400 - 100
        = -180

Therefore:

    Por reembolsar = 180

This proves a Return is a REAL movement and cannot be confused with a rejected
Expense.

============================================================
6. "USADO" REMAINS OPERATIONAL
============================================================

Preserve:

    Usado
    Uso %

as operational/statistical metrics if currently useful.

But:

    USADO MUST NOT DECIDE RECONCILIATION.

Only APROBADO Expenses enter:

    TOTAL_EXPENSES

and the reconciliation equations.

For usage > 100%:

    real text may exceed 100%
    visual progress remains clamped to 100%

============================================================
7. RETURN UX SAFETY
============================================================

The current Return form must not silently pre-fill the entire pending amount
and submit it without an explicit consequence confirmation.

Implement:

- amount entered explicitly;
- no automatic full-balance prefill;
- reason required;
- explicit confirmation before recording;
- clear wording that this records a REAL movement of money.

If unresolved Expenses exist, show a warning such as:

    "Este expediente todavía tiene gastos pendientes de resolución.
     La devolución se registrará como un movimiento real de dinero y
     los gastos aprobados posteriormente pueden modificar el saldo."

Do NOT prohibit a legitimate early Return merely because Expenses are pending.

Backend remains authoritative.

============================================================
8. RETURN / REIMBURSEMENT REVERSAL
============================================================

Complete the existing reversal capability.

STEP 19 established that V11/schema already anticipated reversals through:

    reverses_balance_event_id

Do NOT delete or update the original movement.

Reversal is compensating, append-only.

Canonical rules:

- original movement remains immutable;
- reversal references the original event;
- reversal amount equals original amount exactly;
- an event may be reversed at most once;
- reversal requires a reason;
- closed Case cannot receive a new reversal;
- actor = authenticated global UserAccount;
- timestamp = server/database authoritative time;
- idempotency preserved;
- resulting Case must be reconciled again if balance changes.

Use the existing canonical permission that currently authorizes settlement /
Return / Reimbursement operations.

Do NOT invent a parallel permission unless the existing model makes this
impossible.

============================================================
9. CURRENT OWNER CASE — NO CASH WAS RETURNED
============================================================

Owner has now explicitly confirmed:

    NO real cash Return occurred.

The stored return events:

    event 29 = USD 200
    event 30 = USD 100

are therefore incorrect business movements from the Owner smoke.

DO NOT delete them.

DO NOT rewrite their history.

After the new reversal functionality is deployed, the correct repair is:

    reverse event 29 in full
    reverse event 30 in full

Then the Case must calculate:

    Total anticipos = 320
    Total gastos = 400
    Total devuelto efectivo = 0
    Total reembolsado = 0
    Por reembolsar = 80

IMPORTANT:

Do NOT perform this Shared DEV data correction automatically in this source
implementation STEP.

The Owner should execute the reversal through the real authenticated product
flow after deployment, so the real actor is recorded.

============================================================
10. FINANCE CARD — OWNER SEMANTICS
============================================================

Make the finance summary clearly expose:

    Total anticipos
    Total gastos
    Total a conciliar

and preserve real movement information:

    Devuelto
    Reembolsado
    Pendiente / direction

Suggested conceptual layout:

    Finanzas

    Total anticipos       Total gastos        Total a conciliar
    USD 320.00            USD 400.00          USD 80.00
                                              Por reembolsar

    Devuelto              Reembolsado         Pendiente
    USD 0.00              USD 0.00            USD 80.00

    Uso
    125%                  [bar clamped visually]

Do not use a negative currency display if the existing design convention
prefers positive money + direction.

Internally the signed balance may remain -80.

============================================================
11. DO NOT BREAK ACCEPTED CASE CARD
============================================================

Preserve the accepted STEP 15 structure:

- EXP. NN title;
- Fecha;
- Responsable;
- Supervisor;
- Recurso asignado;
- Cerrado / Abierto;
- Conciliado above divider;
- Uso inside Finanzas;
- responsive layout.

The new ID Gasto will be inserted under Fecha.

============================================================
12. OWNER-APPROVED EXPENSE CASE BUSINESS IDENTIFIER
============================================================

The ExpenseCase needs a persistent, immutable business number.

Visible normal UI:

    ID Gasto: 202609170001

Example card:

    EXP. 01: Compra Filtro
    Fecha: 2026-09-17
    ID Gasto: 202609170001

    Responsable: ...
    Supervisor: ...
    Recurso asignado: ...

Do NOT expose the UUID as the normal user identifier.

Do NOT derive this from:

- list position;
- EXP. 01;
- database bigint id.

============================================================
13. THREE IDENTIFIER LEVELS
============================================================

Preserve these separate concepts:

A. TECHNICAL ID

    public UUID

Used internally/API where appropriate.

B. VISIBLE BUSINESS CASE NUMBER

    caseNumber

Example:

    202609170001

This is what normal UI displays as:

    ID Gasto: 202609170001

C. FULL BUSINESS REFERENCE

For Ecuador:

    RUC - ESTABLISHMENT_NUMBER - CASE_NUMBER

Example:

    1191771814001-001-202609170001

This full reference establishes business traceability.

It is NOT normally displayed on the Case card.

Use it where full traceability is useful:

- export;
- audit;
- report;
- integration;
- support/admin lookup.

============================================================
14. RUC IS NOT TENANT_ID
============================================================

DO NOT use RUC as GYPPORT's structural tenant key.

Internal relationship remains:

    tenant_id

RUC is a tax identifier belonging to the organization's canonical tax profile.

Likewise:

    establishment_id

is the internal canonical establishment reference.

The full Ecuador reference is derived from:

    canonical tax identifier (RUC)
    +
    canonical establishment business number/code
    +
    caseNumber

Do NOT duplicate RUC into gm-expenses merely for convenience.

Do NOT create a second Establishment catalog.

Do NOT cross-module JDBC.

============================================================
15. EXPENSE CASE ESTABLISHMENT LINK
============================================================

Audit the current ExpenseCase organization/establishment context before
editing.

If ExpenseCase already carries a canonical establishment reference:

    reuse it.

If the current Case model lacks establishment_id but creation context already
contains a canonical establishment:

    add an opaque/canonical establishment reference using existing modular
    architecture.

Do NOT copy establishment master data into gm-expenses.

If an existing historical Case cannot be deterministically associated with an
Establishment:

    STOP and report the exact affected rows.

Do NOT invent Establishment 001 simply to complete a backfill.

============================================================
16. CASE NUMBER FORMAT
============================================================

Visible case number:

    YYYYMMDD####

Example:

    202609170001

Components:

    YYYYMMDD = business date
    ####     = daily sequence, zero-padded

Sequence scope:

    TENANT
    + ESTABLISHMENT
    + BUSINESS_DATE

Therefore Establishment 001 may have:

    202609170001
    202609170002

and Establishment 002 may independently have:

    202609170001

The full business references remain distinct:

    1191771814001-001-202609170001
    1191771814001-002-202609170001

============================================================
17. BUSINESS DATE
============================================================

The date used by:

    Fecha
and
    caseNumber YYYYMMDD

must be the SAME business date.

Do not use UI date from one timezone and case number date from another.

Use the canonical tenant/organization business timezone resolution if it
exists.

For Ecuador, the effective country timezone is:

    America/Guayaquil

Do NOT silently use UTC for an Ecuador business date.

If current platform timezone configuration is absent/null:

- audit the canonical country/tenant context;
- implement the smallest reusable timezone-resolution mechanism consistent
  with the existing platform;
- do not hardcode Ecuador inside gm-expenses domain logic.

If a globally safe timezone cannot be resolved without opening a new platform
foundation:

    STOP and report before inventing architecture.

============================================================
18. PERSISTENCE DESIGN
============================================================

Expected persisted ExpenseCase concepts:

    tenant_id
    establishment_id / canonical establishment reference
    case_business_date
    case_sequence
    case_number
    public UUID

Do NOT store the concatenated Ecuador full reference as the source of truth.

Full reference is derived.

Recommended uniqueness:

    UNIQUE(
        tenant_id,
        establishment_id,
        case_business_date,
        case_sequence
    )

and/or equivalent canonical uniqueness for:

    tenant_id,
    establishment_id,
    case_number

Case number is immutable after creation.

============================================================
19. CONCURRENCY-SAFE SEQUENCE
============================================================

Sequence generation must be:

- server-side;
- transaction-safe;
- concurrency-safe;
- scoped per tenant + establishment + business date;
- never process-memory only.

A failed Case creation must not accidentally assign duplicate numbers.

Use a dedicated sequence/counter persistence mechanism appropriate to current
JdbcTemplate architecture.

Do NOT reuse:

    document_sequences

because that belongs to SRI/fiscal-document numbering.

============================================================
20. V64
============================================================

V63 is the current deployed migration head.

This STEP is authorized to create:

    V64

ONLY for the minimum schema necessary for the final Owner-smoke corrections.

Expected V64 scope may include:

- ExpenseCase business-number fields;
- establishment link if truly absent/required;
- sequence/counter table;
- deterministic historical backfill;
- uniqueness/check constraints;
- immutability protection where consistent with current DB conventions.

Reversal support should reuse the existing V11 reversal schema wherever
possible.

Do NOT create a second reversal architecture.

Do NOT create V65 in this STEP unless a proven technical blocker makes one
migration impossible; STOP first.

============================================================
21. HISTORICAL BACKFILL
============================================================

Backfill existing ExpenseCases deterministically.

Use:

    tenant
    establishment
    business date
    created_at
    stable id tie-breaker

to assign sequences.

Example ordering:

    ORDER BY created_at, id

Do not derive sequence from current UI list order.

Do not fabricate an establishment.

Before applying to Shared DEV, rehearse V64 on a disposable copy.

Report:

    number of Cases backfilled
    duplicates = 0
    unresolved establishment references

If unresolved references > 0:

    STOP_FOR_OWNER_REVIEW.

============================================================
22. API
============================================================

Expose at minimum:

    caseNumber

on Case list/detail APIs.

Where architecturally appropriate expose:

    fullBusinessReference

through Host composition, not by making gm-expenses query tax/organization
tables directly.

Preserve UUID compatibility for existing routes.

Do NOT replace UUID URLs in this STEP.

============================================================
23. UI
============================================================

Card:

    EXP. 01: Compra Filtro
    Fecha: 2026-09-17
    ID Gasto: 202609170001

Normal card does NOT need to show:

    1191771814001-001-202609170001

Full reference may appear later/detail/export/support surfaces where useful.

Preserve accepted typography and left-column structure.

Do not let ID Gasto deform:

    Responsable
    Supervisor
    Recurso asignado

Conciliado stays aligned near Responsable.

============================================================
24. RESPONSIVE
============================================================

Verify:

    1280
    768
    375
    320

Require:

- ID Gasto readable;
- no horizontal overflow;
- no deformation of accepted text;
- Conciliado remains header lifecycle indicator;
- Uso remains finance metric;
- finance summary remains readable.

============================================================
25. TEST MATRIX — FINANCIAL
============================================================

Add/adjust tests proving:

A.
Rejected Expense contributes zero.

B.
Observed Expense contributes zero.

C.
Pending Review contributes zero.

D.
Approved Expense contributes its full amount.

E.
Multiple delivered Advances sum correctly.

F.
320 Advances + 400 approved Expenses:
    base balance = -80
    Por reembolsar = 80.

G.
Rejecting a 200 Expense does not create:
    Advance
    Return
    Reimbursement
    Adjustment.

H.
Real Return changes final balance exactly once.

I.
Real Reimbursement changes final balance exactly once.

J.
Reversing Return restores its financial effect exactly.

K.
Original movement remains immutable.

L.
Double reversal refused.

M.
Closed Case reversal refused.

============================================================
26. TEST MATRIX — BUSINESS NUMBER
============================================================

Prove:

A.
First Case for:

    tenant A
    establishment 001
    2026-09-17

gets:

    202609170001

B.
Second gets:

    202609170002

C.
Establishment 002 may independently get:

    202609170001

D.
Another tenant may independently get:

    202609170001

E.
Concurrent Case creation cannot duplicate a number.

F.
Failed transaction does not leave an invalid Case.

G.
Case number cannot be modified.

H.
Full Ecuador reference resolves:

    <RUC>-<establishment number>-<caseNumber>

without copying RUC into gm-expenses.

============================================================
27. V64 REHEARSAL
============================================================

Before any Shared DEV migration:

- create a fresh disposable copy of current Shared DEV V63;
- apply V64;
- verify deterministic backfill;
- verify all existing data preserved;
- verify constraints;
- run real concurrency sequence test;
- run rollback/failure transaction test.

Do NOT modify actual Shared DEV in this implementation STEP.

============================================================
28. TEST SCOPE
============================================================

Run affected suites:

gm-expenses:
    full module suite

Host:
    affected unit/API tests
    real-DB gm-expenses suite

Studio:
    full contracts

Migration:
    V63 → V64 disposable rehearsal

Do not rerun unrelated PKG-2D or other module matrices unless a changed shared
file triggers them.

Use incremental baseline rules.

============================================================
29. DOCUMENTATION
============================================================

Update canonical gm-expenses domain/persistence documentation.

Append Owner decisions to:

    Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md

Append-only.

Record clearly:

- rejected Expense financial impact = zero;
- reconciliation uses delivered Advances vs APROBADO Expenses;
- real Return/Reimbursement are independent cash movements;
- business Case number semantics;
- full business reference semantics;
- RUC is not tenant_id;
- establishment is canonical organizational data;
- sequence scope.

Store this STEP prompt and evidence.

Refresh CURRENT_STEP through the continuity mechanism.

Also promote/store the accepted STEP 18 deployment record if the canonical
release track requires it.

============================================================
30. HARD SAFETY
============================================================

Do NOT:

- delete financial history;
- rewrite event history;
- mutate STEP 19 Owner Case;
- migrate Shared DEV;
- repair its false Return automatically;
- push;
- stage unrelated WIP;
- change PKG-2D architecture;
- introduce cross-module JDBC;
- duplicate RUC or Establishment masters;
- reuse SRI document sequences.

============================================================
31. COMMIT POLICY
============================================================

This is an implementation + verification STEP.

Do NOT commit yet.

Do NOT push.

Stop for Owner review after all tests are green.

The next closure gate will perform:

    controlled commits
    → deploy V64 to Shared DEV
    → Owner reverses the false Return through the product
    → verify USD 80 Por reembolsar
    → final Owner smoke
    → freeze MVP

============================================================
32. REQUIRED FINAL REPORT
============================================================

Return:

STEP=
GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20

STATUS=
READY_FOR_OWNER_FINAL_FIX_REVIEW
or
BLOCKED

FINANCIAL_MODEL:

TOTAL_ADVANCES_RULE=
SUM_DELIVERED_ADVANCES

TOTAL_EXPENSES_RULE=
SUM_APPROVED_EXPENSES

REJECTED_FINANCIAL_EFFECT=
ZERO

BASE_RECONCILIATION_FORMULA=
TOTAL_ADVANCES - TOTAL_EXPENSES

OWNER_CASE_EXPECTED_AFTER_REVERSAL=
TOTAL_ADVANCES=320
TOTAL_EXPENSES=400
TOTAL_RETURNED=0
TOTAL_REIMBURSED=0
POR_REEMBOLSAR=80

RETURN_AUTOCREATED_BY_REJECTION=
NO

RETURN_FORM_PREFILLS_FULL_BALANCE=
NO

RETURN_CONFIRMATION_REQUIRED=
YES

RETURN_REVERSAL_IMPLEMENTED=
YES/NO

REVERSAL_APPEND_ONLY=
YES/NO

DOUBLE_REVERSAL_BLOCKED=
YES/NO

BUSINESS_IDENTIFIER:

TECHNICAL_CASE_ID=
UUID

VISIBLE_CASE_NUMBER=
YYYYMMDD####

VISIBLE_EXAMPLE=
202609170001

NORMAL_CARD_DISPLAY=
ID Gasto: 202609170001

SEQUENCE_SCOPE=
TENANT + ESTABLISHMENT + BUSINESS_DATE

FULL_BUSINESS_REFERENCE_EC=
RUC-ESTABLISHMENT_NUMBER-CASE_NUMBER

FULL_EXAMPLE=
1191771814001-001-202609170001

RUC_USED_AS_TENANT_KEY=
NO

ESTABLISHMENT_MASTER_DUPLICATED=
NO

SRI_SEQUENCE_REUSED=
NO

BUSINESS_DATE_TIMEZONE_RULE=

V64:

MIGRATION_CREATED=
YES/NO

BACKFILLED_CASES=

UNRESOLVED_ESTABLISHMENTS=

DUPLICATE_CASE_NUMBERS=
0

V63_TO_V64_REHEARSAL=
PASS/FAIL

CONCURRENT_SEQUENCE_TEST=
PASS/FAIL

UI:

ID_GASTO_CARD=
YES/NO

CONCILIADO_POSITION_PRESERVED=
YES/NO

USAGE_POSITION_PRESERVED=
YES/NO

RESPONSIVE_RESULTS=
1280:
768:
375:
320:

TEST_RESULTS:

GM_EXPENSES=
HOST_REAL_DB=
HOST_TARGETED=
STUDIO=

SHARED_DEV_VERSION=
V63

SHARED_DEV_MODIFIED=
NO

OWNER_CASE_MODIFIED=
NO

FILES_STAGED=
0

COMMITS_CREATED=
0

PUSH_PERFORMED=
NO

READY_FOR_CONTROLLED_COMMIT_AND_V64_DEPLOYMENT=
YES/NO

STOP_FOR_OWNER_REVIEW=
YES

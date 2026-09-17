# GM_EXPENSES_OWNER_SMOKE_FINDINGS_19 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_SMOKE_FINDINGS_19
MODE=AUDIT_FIRST_THEN_PROPOSE_FIX
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner real-login smoke on Shared DEV V63 after GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18
TARGET_CASE=437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES OWNER SMOKE FINDINGS
CASE BUSINESS ID + RETURN/REIMBURSEMENT AUDIT

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_OWNER_SMOKE_FINDINGS_19

MODE=
AUDIT_FIRST_THEN_PROPOSE_FIX

OWNER_AUTHORIZED=YES

TARGET_CASE=
437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0

IMPORTANT:

This finding came from the Owner real-login smoke on Shared DEV V63.

DO NOT modify source code yet.
DO NOT modify the database yet.
DO NOT reverse any financial movement yet.
DO NOT create V64 yet.
DO NOT commit.
DO NOT push.

First establish the exact facts.

============================================================
1. OWNER OBSERVED FINANCIAL STATE
============================================================

Current UI shows approximately:

Entregado:
    USD 320.00

Usado:
    USD 400.00

Justificado:
    USD 400.00

Devuelto:
    USD 300.00

Reembolsado:
    USD 0.00

Displayed:
    Por reembolsar USD 380.00

Owner initially expected:

    USD 80.00

Audit whether current result follows the canonical equation:

    balance =
        totalDelivered
        + totalReimbursed
        - totalJustified
        - totalReturned
        - totalAdjustments

Expected mathematical audit:

    320 + 0 - 400 - 300 = -380

Therefore:

    Por reembolsar = USD 380

IF AND ONLY IF the USD 300 return was a real financial movement.

Without that return:

    320 - 400 = -80

Therefore:

    Por reembolsar = USD 80

DO NOT change the canonical equation merely to produce USD 80.

============================================================
2. AUDIT THE EXACT CASE
============================================================

Read-only inspect Case:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0

Identify:

- all Advances;
- amount of each Advance;
- state of each Advance;
- delivery timestamp;
- total delivered;
- all Expenses;
- amount/state of each Expense;
- total Used;
- total Approved/Justified;
- all Return movements;
- all Reimbursement movements;
- all Adjustments;
- rendition/reconciliation state.

Return the complete financial chronology.

Especially identify the exact origin of:

    Devuelto USD 300.00

Record:

- movement id;
- amount;
- timestamp;
- actor;
- source endpoint/use case;
- immutable history/event if present.

Do not print secrets.

============================================================
3. DETERMINE WHETHER THERE IS AN ARITHMETIC BUG
============================================================

Return exactly:

ARITHMETIC_FORMULA_CORRECT=YES/NO

FINANCIAL_INPUTS_CORRECTLY_AGGREGATED=YES/NO

DISPLAYED_REIMBURSEMENT_EXPECTED_FROM_STORED_MOVEMENTS=
<amount>

If USD 380 follows faithfully from stored movements:

    CALCULATION_BUG=NO

Do not classify a mistaken business movement as a formula bug.

============================================================
4. RETURN REVERSAL CAPABILITY
============================================================

Audit current gm-expenses code and schema for an existing supported mechanism
to reverse/cancel/correct a previously registered Return.

Search actual current implementation for:

- Return reversal;
- settlement adjustment;
- compensating movement;
- balance event;
- immutable correction/reversal event.

Do not assume one exists.

Determine:

RETURN_REVERSAL_SUPPORTED_NOW=YES/NO

If YES:
    document exact supported workflow.

If NO:
    classify whether this Owner smoke exposed an MVP functional gap.

Canonical rule:

A real Return must never be silently deleted merely because later Expense
approval creates a reimbursement obligation.

If the Return did NOT actually happen, correction must preserve history and
must not fabricate past facts.

============================================================
5. UX SAFETY AUDIT
============================================================

Audit whether the current UI allows:

    Registrar devolución

while the Case still has:

- REGISTRADO expenses;
- PENDIENTE_REVISION expenses;
- OBSERVADO expenses;
- expenses that may later become APROBADO.

Do NOT automatically decide this should be forbidden.

A real return before final expense approval can be legitimate.

Instead determine whether the UI should warn clearly that:

    "Esta devolución se registrará como un movimiento real.
     Si posteriormente se aprueban más gastos, podría generarse
     un importe por reembolsar."

Report recommendation only.

No implementation yet.

============================================================
6. NEW OWNER REQUIREMENT — BUSINESS ID
============================================================

Owner wants the Case card to display:

    EXP. 01: Compra Filtro
    Fecha: 2026-09-17
    ID Gasto: 202609170001

Audit the current ExpenseCase persistence/model first.

Determine whether there is already:

- business number;
- case number;
- sequence;
- document number;
- human-readable id;

that can be reused.

DO NOT reuse:

- database UUID;
- UI list position;
- derived EXP. 01 index;

as the persistent business identifier.

============================================================
7. BUSINESS ID SEMANTICS
============================================================

If no existing identifier exists, propose:

DISPLAY LABEL:

    ID Gasto

OWNER EXAMPLE:

    202609170001

Concept:

    YYYYMMDD + 4-digit sequence

Example:

    20260917 + 0001
    = 202609170001

Audit and propose the safest persistence semantics.

Preferred characteristics:

- immutable after creation;
- generated server-side;
- concurrency-safe;
- tenant-aware;
- not derived from list ordering;
- stable across UI/report/API;
- unique according to an explicit DB constraint.

Because GYPPORT is multitenant, evaluate:

    sequence per tenant + business date

rather than a process-memory counter.

Do NOT implement until the audit confirms the correct design.

============================================================
8. TERMINOLOGY CHECK
============================================================

The target object is ExpenseCase.

Owner requested UI label:

    ID Gasto

Do not silently rename it.

But report whether the internal model should use a precise name such as:

    caseNumber
    expenseCaseNumber
    businessId

while UI displays:

    ID Gasto

Do not expose technical UUIDs to the user.

============================================================
9. PLACEMENT
============================================================

Desired card header:

    EXP. 01: Compra Filtro
    Fecha: 2026-09-17
    ID Gasto: 202609170001

    Responsable: ...
    Supervisor: ...
    Recurso asignado: ...

Do not alter:

- Conciliado placement;
- Responsable;
- Supervisor;
- Recurso asignado;
- Finanzas;
- Uso;
- card responsive behavior.

============================================================
10. MIGRATION DECISION
============================================================

Do not create V64 in this audit.

Determine whether adding the persistent Case business identifier requires a
migration.

If YES:

    MIGRATION_REQUIRED=YES

and propose what V64 would need to contain.

Consider existing ExpenseCases already present.

Do NOT invent identifiers for historical rows without defining a deterministic
backfill policy.

============================================================
11. SCOPE SAFETY
============================================================

Do not reopen:

- V62;
- V63;
- Case-level rendition;
- multiple Advances;
- FIFO removal;
- audit architecture;
- PKG-2D;
- Docker architecture.

Shared DEV may be queried read-only for this exact Owner smoke case.

No writes.

============================================================
12. REQUIRED REPORT
============================================================

Return:

STEP=
GM_EXPENSES_OWNER_SMOKE_FINDINGS_19

STATUS=
AUDIT_COMPLETE_WAITING_OWNER_DECISION

CASE_ID=
437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0

FINANCIAL_CHRONOLOGY=

TOTAL_DELIVERED=
TOTAL_USED=
TOTAL_JUSTIFIED=
TOTAL_RETURNED=
TOTAL_REIMBURSED=
TOTAL_ADJUSTMENTS=

CANONICAL_BALANCE=

ARITHMETIC_FORMULA_CORRECT=
FINANCIAL_INPUTS_CORRECTLY_AGGREGATED=
CALCULATION_BUG=

RETURN_300_MOVEMENT=
RETURN_ACTOR=
RETURN_TIMESTAMP=

RETURN_REVERSAL_SUPPORTED_NOW=
RETURN_REVERSAL_GAP=

UX_RETURN_WARNING_RECOMMENDED=

BUSINESS_ID_ALREADY_EXISTS=
CURRENT_IDENTIFIER_MODEL=

OWNER_REQUESTED_DISPLAY=
ID Gasto: 202609170001

PROPOSED_INTERNAL_FIELD=
PROPOSED_GENERATION_RULE=
PROPOSED_UNIQUENESS_SCOPE=

MIGRATION_REQUIRED=
PROPOSED_V64_SCOPE=

SOURCE_FILES_CHANGED=0
DATABASE_ROWS_CHANGED=0
FILES_STAGED=0
COMMITS_CREATED=0
PUSH_PERFORMED=NO

STOP_FOR_OWNER_REVIEW=YES

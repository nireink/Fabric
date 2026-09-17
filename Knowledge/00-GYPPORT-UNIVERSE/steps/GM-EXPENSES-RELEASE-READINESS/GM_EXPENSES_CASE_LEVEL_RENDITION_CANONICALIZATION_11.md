# GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11
MODE=AUDIT_FIRST_THEN_TARGETED_IMPLEMENTATION
OWNER_AUTHORIZATION=YES
DATE=2026-09-16
SUPERSEDES_DECISION=CASE_LEVEL_JUSTIFIED_TOTAL shared across a Case's delivered advances in delivery order (FIFO) and the per-advance rendition commands on the ExpenseCase
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES CASE-LEVEL RENDITION CANONICALIZATION

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11

MODE=
AUDIT_FIRST_THEN_TARGETED_IMPLEMENTATION

OWNER_AUTHORIZED=YES

============================================================
0. OWNER ACCEPTANCE
============================================================

The following STEPs are Owner-accepted:

GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07
GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10

Accepted:

- multiple Advances per ExpenseCase = YES
- multiple Advances in same currency = YES
- one-active-Advance restriction = REMOVED
- draft Advances still block Case closure
- closed Case bar = Conciliado 100%
- open Case bar = Uso
- V62 preserved
- V63 preserved
- Shared DEV untouched

Do NOT reopen those decisions.

============================================================
1. OWNER DECISION — ZERO USAGE STATE
============================================================

Resolve the remaining presentation conflict.

OWNER CHOICE=OPTION_B

When an ExpenseCase has no delivered Advance:

    Uso
    0%

and render an empty usage bar.

Do NOT show:

    Uso —
    No aplica

for this numeric progress metric.

Example:

    Entregado
    USD 0.00

    Usado
    USD 260.00

    Justificado
    USD 0.00

    Devuelto
    USD 0.00

    Reembolsado
    USD 0.00

    Pendiente de conciliar
    USD 0.00

    Uso
    0%

The bar track remains visible with 0% fill.

============================================================
2. IMPORTANT REMAINING FUNCTIONAL CONFLICT
============================================================

The current implementation still allocates approved Expense amounts among
individual Advances using earliest-delivered-first / FIFO.

Current report states:

    each Advance rendition reconciles using its individual share
    of Case-approved Expenses, split in delivery order.

This is NOT the Owner's canonical business model.

FIFO may remain only as temporary technical compatibility while this STEP is
being changed.

It must NOT remain the authoritative rendition rule.

============================================================
3. CANONICAL MODEL
============================================================

ExpenseCase is the rendition / funding center.

Advances are funding tranches.

Expenses belong to the ExpenseCase.

Canonical structure:

    ExpenseCase
        ├── Advance 1
        ├── Advance 2
        ├── Advance 3
        ├── ...
        ├── Expenses
        └── Case-level rendition

Example:

    Construcción Casa A

    Advance 1     USD 30,000
    Advance 2     USD  2,000
    Advance 3     USD    300
    Advance 4     USD  5,000

    Total entregado
    USD 37,300

Expenses are NOT assigned to those Advances through FIFO.

============================================================
4. CANONICAL CASE-LEVEL FINANCIAL EQUATION
============================================================

For one ExpenseCase + currency:

    totalDelivered
        = SUM(delivered Advances)

Canonical balance:

    caseBalance =
        totalDelivered
        + totalReimbursed
        - totalJustified
        - totalReturned
        - totalAdjustments

Canonical reconciliation equation:

    totalDelivered
    + totalReimbursed
    =
    totalJustified
    + totalReturned
    + totalAdjustments

Interpretation:

    caseBalance > 0
        → Por justificar o devolver

    caseBalance < 0
        → Por reembolsar

    caseBalance == 0
        → Pendiente de conciliar USD 0.00
          / financially balanced

Existing Expense workflow blockers still apply.

============================================================
5. AUDIT CURRENT SETTLEMENT ARCHITECTURE FIRST
============================================================

Before implementing:

Audit exactly how the current per-Advance AdvanceSettlement model is used.

Return:

- tables involved;
- foreign keys;
- CloseSettlementUseCase behavior;
- how CaseRenditionService currently chooses settlements;
- how returns are persisted;
- how reimbursements are persisted;
- how Case closure currently closes each Advance;
- how FIFO share enters those calculations;
- which read models depend on per-Advance justified allocation.

Determine whether Case-level rendition can be implemented using the existing
schema.

Preferred:

NO migration if current settlement/event storage can safely support Case-level
orchestration.

If a new Case-level aggregate/table is truly unavoidable:

STOP.

Report exact schema need and wait for Owner approval.

Do NOT invent V64 automatically.

============================================================
6. REMOVE FIFO AS AUTHORITATIVE FINANCIAL ALLOCATION
============================================================

The class/mechanism currently used for:

    CaseJustifiedTotalAllocation

or equivalent FIFO distribution must no longer determine the authoritative
financial truth of the Case.

Do NOT allocate:

    Expense A → Advance 1
    Expense B → Advance 1
    Expense C → Advance 2

merely because of delivery order.

Approved Expenses contribute to:

    ExpenseCase justified total.

FIFO may only remain temporarily where required to read historical legacy
records, clearly marked compatibility-only.

============================================================
7. ADVANCE SEMANTICS
============================================================

Each Advance keeps its own history:

- amount
- currency
- activity
- planned delivery
- delivery method
- deliveredAt
- deliveredBy
- responsible/reviewer context
- state

But it is a funding tranche.

Preferred individual Advance presentation:

    Anticipo USD 5,000.00

    Fecha entrega
    ...

    Método
    ...

    Estado
    Entregado

    Rendición
    Se gestiona desde el expediente

Do not display a fabricated FIFO "Justificado" amount per Advance as if it were
a business allocation.

============================================================
8. RETURN / REIMBURSEMENT SEMANTICS
============================================================

Returns and reimbursements belong to the Case rendition business flow.

Users should not have to decide which funding tranche a return/reimbursement
belongs to unless the existing persistence requires an internal technical
reference.

If an internal Advance/Settlement reference is still necessary:

- keep it invisible as implementation detail;
- it must not determine Case-level financial truth;
- it must not recreate FIFO semantics in Studio.

Preserve V63:

Return + Reimbursement may coexist.

============================================================
9. CASE-LEVEL RENDITION UX
============================================================

ExpenseCase detail is the single operational place for rendition.

Show:

    Resumen financiero

    Entregado
    SUM Advances

    Usado

    Justificado
    SUM approved Expenses

    Devuelto
    total Case returns

    Reembolsado
    total Case reimbursements

    Por justificar o devolver
    OR
    Por reembolsar
    OR
    Pendiente de conciliar USD 0.00

Actions:

    Registrar devolución
    Registrar reembolso
    Conciliar
    Cerrar expediente

according to current valid rules.

Do NOT require the user to conciliate each Advance independently.

============================================================
10. CASE CLOSURE
============================================================

Canonical close flow:

ExpenseCase
    ↓
all Expense workflow blockers resolved
    ↓
all BORRADOR Advances resolved
    ↓
Case financial equation balanced
    ↓
explicit Conciliar
    ↓
Cerrar expediente

Closing the Case must leave all funding Advances in the correct terminal state
through the existing technical closure chain.

Do NOT require multiple repetitive user-facing settlement closes.

============================================================
11. DRAFT ADVANCES
============================================================

Multiple Advances are allowed.

Multiple BORRADOR Advances are also allowed while the Case is open.

However:

    Case closure
    → blocked while any BORRADOR remains.

Message remains specific:

Singular:
    Hay 1 anticipo en borrador por USD X.XX.
    Confirma su entrega o cancélalo antes de cerrar el expediente.

Plural:
    Hay N anticipos en borrador por un total de USD X.XX.
    Confirma su entrega o cancélalos antes de cerrar el expediente.

This closure rule must NOT prevent adding another Advance.

============================================================
12. PROGRESS INDICATORS
============================================================

Preserve STEP 10:

OPEN Case:

    Uso
    actual percentage

CLOSED Case:

    Conciliado
    100%

    Uso
    actual percentage as secondary metric

Usage percentage may exceed 100%.

Example:

    delivered 1000
    used 1100

    Uso 110%

Visual fill:
    clamp at 100%

Numeric text:
    preserve 110%

No delivered Advance:

    Uso 0%

with empty bar.

============================================================
13. MULTIPLE ADVANCE EXAMPLE
============================================================

Prove this canonical scenario:

Case:
    Construcción

Advances:
    30,000
     2,000
       300
     5,000

Total delivered:
    37,300

Approved Expenses:
    35,000

Returned:
     2,300

Reimbursed:
         0

Case balance:
         0

No FIFO allocation is required.

Conciliar:
    enabled when all other prerequisites pass.

Case closes successfully.

============================================================
14. ADDITIONAL ADVANCE AFTER EXPENSES
============================================================

Also prove:

Case initially:

    Delivered 30,000
    Justified 29,500

Then another Advance:

    +2,000

New total delivered:

    32,000

Case balance updates naturally.

No previously approved Expense is reassigned among Advances.

No FIFO recalculation is exposed as financial policy.

============================================================
15. REPORTS
============================================================

Reports must use Case-level totals.

Per Case first calculate:

    delivered
    used
    justified
    returned
    reimbursed
    caseBalance

Then aggregate directions.

Do not aggregate artificial per-Advance FIFO positions.

Preserve:

Case A:
    +30 por justificar/devolver

Case B:
    -20 por reembolsar

Report:
    30 and 20 separately

not net 10.

============================================================
16. CANONICAL DOCUMENTATION
============================================================

Update Fabric in the same STEP.

Canonical documentation must now state:

- multiple Advances per Case are valid;
- same-currency multiple Advances are valid;
- Advances are funding tranches;
- Expenses belong to ExpenseCase;
- rendition is Case-level;
- FIFO is NOT canonical;
- individual Advance justified allocation is not business truth;
- V63 cash-conservation principle is evaluated at Case level;
- closure remains Case-centered.

Reglas.md:

append a superseding decision if previous entries still imply:
    one active Advance
or
    FIFO allocation.

Do NOT rewrite historical entries.

============================================================
17. TESTS — DOMAIN / APPLICATION
============================================================

Required:

1.
Multiple Advances same Case/currency allowed.

2.
Total delivered = sum of delivered Advances.

3.
Approved Expense total belongs to Case.

4.
No FIFO required for Case balance.

5.
Return changes Case balance.

6.
Reimbursement changes Case balance.

7.
Return + reimbursement coexist according to V63.

8.
Additional Advance after Expenses updates total delivered only.

9.
Drafts block Case closure.

10.
Balanced Case reconciles.

11.
Closing Case resolves/closes funding Advances correctly.

12.
Tenant isolation preserved.

============================================================
18. TESTS — STUDIO
============================================================

Verify:

A.
Multiple Advances listed.

B.
No "one active Advance" refusal.

C.
No fake per-Advance justified allocation presented as business truth.

D.
Case-level summary correct.

E.
Open bar:
    Uso.

F.
Closed bar:
    Conciliado 100%
    Uso secondary.

G.
No delivered Advance:
    Uso 0%
    empty bar.

H.
Uso 110%:
    text 110%
    visual fill <=100%.

I.
Draft closure blocker count/amount correct.

============================================================
19. REHEARSAL IMPACT
============================================================

This STEP changes authoritative backend financial behavior.

Therefore:

REHEARSAL_03 runtime/business smoke is invalidated for final release evidence.

Migration evidence V43→V63 remains reusable if migration bytes do not change.

After this STEP is Owner-accepted:

run:

    GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12

using an exact disposable copy of Shared DEV.

Do not migrate Shared DEV before that final rehearsal.

============================================================
20. ENVIRONMENT
============================================================

Local only:

Studio:
    localhost:5173

Backend:
    localhost:8080

MySQL:
    localhost:3310

Shared DEV:
    localhost:3308
    READ ONLY

No commit.
No push.

============================================================
21. REQUIRED REPORT
============================================================

Return:

STATUS=
READY_FOR_OWNER_CASE_LEVEL_RENDITION_REVIEW

STEP=
GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11

ZERO_USAGE_OPTION=
B_0_PERCENT

MULTIPLE_ADVANCES_PER_CASE=YES
MULTIPLE_ADVANCES_SAME_CURRENCY=YES

CASE_LEVEL_RENDITION_IMPLEMENTED=

FIFO_AUTHORITATIVE=NO

FIFO_COMPATIBILITY_REMAINING=

CASE_LEVEL_DELIVERED_TOTAL=

CASE_LEVEL_JUSTIFIED_TOTAL=

CASE_LEVEL_RETURN_TOTAL=

CASE_LEVEL_REIMBURSEMENT_TOTAL=

PER_ADVANCE_JUSTIFIED_ALLOCATION_EXPOSED=NO

CASE_CLOSURE_FLOW=

V62_PRESERVED=
V63_PRESERVED=

MIGRATION_REQUIRED=

FABRIC_UPDATED=
REGLAS_SUPERSEDING_ENTRY_APPENDED=

TEST_RESULTS=
- gm-expenses:
- Host real DB:
- Studio:
- local runtime:

REHEARSAL_MIGRATION_EVIDENCE_REUSABLE=
FINAL_RUNTIME_REHEARSAL_REQUIRED=YES

SHARED_DEV_MODIFIED=NO
FILES_STAGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

STOP_FOR_OWNER_REVIEW=YES

# GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10
MODE=TARGETED_OWNER_CORRECTION_BEFORE_COMMIT
OWNER_AUTHORIZATION=YES
DATE=2026-09-16
SUPERSEDES_DECISION=GM_EXPENSES_ONE_ACTIVE_ADVANCE_PER_CASE_CURRENCY_06 (one financially active advance per ExpenseCase and currency)
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES CLOSED CASE PROGRESS BAR + MULTIPLE ADVANCES FIX

STEP=
GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10

MODE=
TARGETED_OWNER_CORRECTION_BEFORE_COMMIT

OWNER_AUTHORIZED=YES

IMPORTANT:

Do NOT reopen V62 or V63.
Do NOT migrate Shared DEV.
Do NOT commit.
Do NOT push.

============================================================
1. OWNER FINDING — CLOSED CASE BAR IS MISLEADING
============================================================

Current closed ExpenseCase example:

    Entregado   USD 300.00
    Usado       USD 260.00
    Devuelto    USD 40.00
    Reembolsado USD 0.00
    Pendiente de conciliar USD 0.00
    Estado      Cerrado

The current visual bar still shows:

    Uso 87%

because:

    260 / 300 = 87%

That arithmetic is correct for usage, but visually misleading for a CLOSED
Case because the financial lifecycle is already fully resolved.

Canonical understanding:

    300 delivered
    260 used
     40 returned
    ---
    300 resolved

Therefore, for a CLOSED Case, the visual progress bar should represent
financial resolution/conciliation completeness, not only raw usage.

============================================================
2. OWNER DECISION — SEPARATE "USO" FROM "CONCILIADO"
============================================================

Two concepts must be kept separate:

A. Uso
    = how much of delivered money became expense/use

    usagePercent =
        used / delivered
        when delivered > 0

B. Conciliado / Resolución financiera
    = whether the Case's financial lifecycle is fully resolved

For a CLOSED Case with:

    pending reconciliation = 0

conciliation progress must be:

    100%

============================================================
3. OPEN CASE PRESENTATION
============================================================

For OPEN Cases:

keep the current operational bar concept:

    Uso
    X%

Example:

    delivered 300
    used 260

    Uso 87%
    progress bar = 87%

This is useful while the Case remains active.

============================================================
4. CLOSED CASE PRESENTATION
============================================================

For CLOSED Cases:

do NOT keep the main visual bar as:

    Uso 87%

Replace the bar meaning with:

    Conciliado
    100%

Show the bar filled at 100%.

Keep "Uso 87%" as a normal numeric metric inside the financial summary, but
not as the final progress bar that visually suggests incomplete state.

Preferred closed presentation:

    Entregado                USD 300.00
    Usado                    USD 260.00
    Justificado              USD 260.00
    Devuelto                 USD 40.00
    Reembolsado              USD 0.00
    Pendiente de conciliar   USD 0.00
    Uso                      87%
    Conciliado               100%

If the layout only supports one bar, the single bar for CLOSED Cases must be:

    Conciliado 100%

not "Uso 87%".

============================================================
5. BAR RULES
============================================================

OPEN case:
    main bar = Uso

CLOSED case:
    main bar = Conciliado

Conciliation percentage logic:

If:
    case status = CLOSED
    and pending reconciliation = 0

Then:
    conciliationPercent = 100

If in the future a non-closed state needs progress:
    use only if explicitly modeled.
For now CLOSED = 100%.

============================================================
6. DO NOT CHANGE FINANCIAL MODEL
============================================================

Do NOT change:

- delivered amount
- used amount
- justified amount
- returned amount
- reimbursed amount
- pending reconciliation amount
- V63 cash equation

This is only presentation semantics.

============================================================
7. MULTIPLE ADVANCES — OWNER CONFIRMATION
============================================================

Reaffirm Owner decision:

Multiple Advances in the same ExpenseCase are VALID.

Examples:

    30,000
     2,000
       300
     5,000

All may belong to the same open Case.

Therefore:

DO NOT reintroduce any "one active Advance per Case + currency" restriction.

Remove any refusal like:

    "Este expediente ya tiene un anticipo activo en USD.
     Resuelve el anticipo actual antes de registrar otro."

Creating another Advance in the same Case/currency must remain allowed.

============================================================
8. CASE-LEVEL FUNDING MODEL
============================================================

Keep the canonical model:

ExpenseCase
    = funding/rendition center

Advances
    = funding tranches

Expenses
    = belong to the Case

Do NOT force per-Advance FIFO allocation as business policy.

Do NOT make multiple Advances appear invalid.

============================================================
9. DRAFT ADVANCE CLOSURE BLOCKER
============================================================

Preserve the accepted rule:

A Case cannot close while it still has BORRADOR Advances.

But this rule applies only to closure.

It must NOT prevent creating another valid Advance.

Improve copy if needed, but preserve business behavior.

============================================================
10. TARGETED UI EXPECTATIONS
============================================================

A. OPEN case with delivered=300 and used=260:

    Uso 87%
    progress bar at 87%

B. CLOSED case with delivered=300, used=260, returned=40, pending=0:

    financial summary still shows Uso 87%
    main bar shows Conciliado 100%
    bar visually full

C. No delivered Advance:

    Uso 0%
    bar empty
    numeric zero states preserved

============================================================
11. TARGETED TESTS
============================================================

Add/update tests for:

A.
Open Case:
    delivered=300
    used=260
    status=OPEN
    → bar label "Uso"
    → 87%

B.
Closed Case:
    delivered=300
    used=260
    returned=40
    reimbursed=0
    pending=0
    status=CLOSED
    → summary shows Uso 87%
    → main bar shows Conciliado 100%
    → full fill

C.
Closed Case with Viaje Loja-like data:
    delivered=679
    used=200
    justified=200
    returned=499
    reimbursed=20
    pending=0
    → main bar 100%

D.
Multiple Advances in one Case:
    second/third/fourth Advance creation allowed

E.
No "one active Advance" refusal rendered.

F.
Draft Advance blocker still prevents closing.

============================================================
12. SCOPE
============================================================

Prefer Studio-only changes unless the API lacks a required Case status/value.

No migration.

No backend financial write changes unless strictly necessary.

Do not touch Shared DEV.

============================================================
13. RETURN
============================================================

STATUS=
READY_FOR_OWNER_CLOSED_BAR_AND_MULTIPLE_ADVANCE_REVIEW

CLOSED_CASE_MAIN_BAR=
CONCILIATED_100

OPEN_CASE_MAIN_BAR=
USAGE_PERCENT

USAGE_METRIC_PRESERVED=YES

MULTIPLE_ADVANCES_ALLOWED=YES

ONE_ACTIVE_ADVANCE_RULE_PRESENT=NO

DRAFT_ADVANCE_CLOSURE_BLOCKER_PRESERVED=YES

BACKEND_FINANCIAL_RULES_CHANGED=NO
MIGRATION_CREATED=NO

TEST_RESULTS=

SHARED_DEV_MODIFIED=NO
FILES_STAGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

STOP_FOR_OWNER_REVIEW=YES

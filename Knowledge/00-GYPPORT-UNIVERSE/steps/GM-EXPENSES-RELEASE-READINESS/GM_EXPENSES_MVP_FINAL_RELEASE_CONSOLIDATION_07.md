# GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07
MODE=TARGETED_FINAL_CONSOLIDATION_BEFORE_COMMIT_AND_SHARED_DEV
OWNER_AUTHORIZATION=YES
DATE=2026-09-16
ACCEPTED_BASELINE_NOT_TO_REOPEN=GM_EXPENSES_FINAL_ADJUSTMENT_V62_04,GM_EXPENSES_UNIFIED_RECONCILIATION_V63_05,GM_EXPENSES_ONE_ACTIVE_ADVANCE_PER_CASE_CURRENCY_06,GM_EXPENSES_RUNTIME_REHEARSAL_03
FINAL_MIGRATION_HEAD=V63
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES MVP FINAL RELEASE CONSOLIDATION

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07

MODE=
TARGETED_FINAL_CONSOLIDATION_BEFORE_COMMIT_AND_SHARED_DEV

OWNER_AUTHORIZED=
YES

IMPORTANT:

This STEP is the final consolidation of the gm-expenses MVP before the
controlled commit gate and the real Shared DEV migration.

DO NOT migrate Shared DEV in this STEP.

DO NOT commit.
DO NOT push.

============================================================
0. ACCEPTED BASELINE
============================================================

The following STEPs are Owner-accepted and MUST NOT be reopened:

GM_EXPENSES_FINAL_ADJUSTMENT_V62_04
GM_EXPENSES_UNIFIED_RECONCILIATION_V63_05
GM_EXPENSES_ONE_ACTIVE_ADVANCE_PER_CASE_CURRENCY_06
GM_EXPENSES_RUNTIME_REHEARSAL_03

FINAL_MIGRATION_HEAD=V63

Accepted migration evidence:

    Shared DEV source:
        V43

    Disposable rehearsal:
        V43 → V63

    migrations:
        V44..V63
        20 migrations
        0 failures

    gm-expenses tables:
        19/19 content-identical across shared columns

    workflow smoke:
        14/14 PASS

    old /settlement calls:
        0

    server 5xx:
        0

    tenant isolation:
        PASS

Shared DEV itself remains:

    V43
    UNMODIFIED

============================================================
1. CURRENT LOCAL RUNTIME
============================================================

Use ONLY the current aligned local environment:

Studio:
    http://localhost:5173

Backend:
    http://127.0.0.1:8080

Local isolated MySQL:
    127.0.0.1:3310

Expected local DB version:
    V63

Shared DEV:

    127.0.0.1:3308
    V43

Shared DEV is READ-ONLY for this STEP.

============================================================
2. FINAL OWNER UX FINDING — EXPENSE CASE CARD
============================================================

Owner found a financial clarity problem on:

    EXP. 01: Viaje Loja
    CLOSED

Current Case card shows approximately:

    Finanzas

    Entregado
    USD 679.00

    Usado
    USD 200.00

    Diferencia
    USD 0.00

    Uso
    29%

This presentation is misleading.

A user naturally reads:

    679 - 200 = 479

and therefore:

    Diferencia USD 0.00

appears mathematically wrong.

The financial model is NOT wrong.

The card hides the financial movements that explain the reconciliation.

For the Case, the complete financial history includes:

    Entregado
    Justificado / Usado
    Devuelto
    Reembolsado
    canonical rendition balance

============================================================
3. DO NOT CHANGE V63
============================================================

The canonical V63 equation remains:

    advanceAmount
    + reimbursementAmount
    =
    justifiedTotal
    + returnedAmount
    + adjustments

Canonical balance remains:

    balance =
        advanceAmount
        + reimbursementAmount
        - justifiedTotal
        - returnedAmount
        - adjustments

Do NOT modify:

- V63;
- RN-001;
- Return + Reimbursement coexistence;
- financial caps;
- reconciliation behavior.

This STEP is presentation/read-model clarity only unless a missing aggregate
read value is proven.

============================================================
4. CASE CARD — REQUIRED FINANCIAL PRESENTATION
============================================================

The Case card must show enough information for the user to understand why a
Case is financially balanced.

Preferred financial information:

    Entregado
    USD 679.00

    Usado
    USD 200.00

    Justificado
    USD 200.00

    Devuelto
    USD 499.00

    Reembolsado
    USD 20.00

    Pendiente de conciliar
    USD 0.00

    Uso
    29%

IMPORTANT:

"Usado" remains an operational metric.

"Justificado" is the approved amount used by rendition.

Do NOT silently merge these two concepts if they can differ.

============================================================
5. CARD DIRECTION LABEL
============================================================

Remove the ambiguous plain label:

    Diferencia

from the Case card.

Use the canonical direction.

If Case canonical balance > 0:

    Por justificar o devolver
    USD X.XX

If Case canonical balance < 0:

    Por reembolsar
    USD X.XX

If Case canonical balance == 0:

    Pendiente de conciliar
    USD 0.00

For a CLOSED Case:

    Pendiente de conciliar
    USD 0.00

clearly communicates that the financial position has been resolved.

Do NOT calculate this field as:

    delivered - used

============================================================
6. CLOSED CASE EXPLANATION
============================================================

For a closed Case like Viaje Loja, the visible values should make the
reconciliation understandable.

Conceptually:

    Entregado      679
    Reembolsado     20
                   ---
                   699

    Justificado    200
    Devuelto       499
                   ---
                   699

Therefore:

    Pendiente de conciliar
    USD 0.00

The UI does not need to render this equation literally unless it improves the
existing design.

But the individual numbers required to understand it must be visible.

============================================================
7. RESPONSIVE PRESENTATION
============================================================

Keep the GYPPORT Executive Technology visual language.

Do not make the Case card excessively tall or visually noisy.

Desktop may use a compact grid.

Example conceptual arrangement:

    Entregado   Usado   Justificado   Uso

    Devuelto    Reembolsado    Pendiente de conciliar

At narrower widths:

    wrap naturally into 2 or 1 column arrangements.

Require no horizontal overflow at:

    375px

Do not reduce the font until readability suffers.

============================================================
8. CASE DETAIL / RENDITION CONSISTENCY
============================================================

The Case card, Case detail and Reports must use consistent vocabulary.

Canonical financial presentation vocabulary:

    Entregado
    Usado
    Justificado
    Devuelto
    Reembolsado
    Por justificar o devolver
    Por reembolsar
    Pendiente de conciliar

Avoid reintroducing:

    Exceso gastado

as a rendition obligation.

Avoid ambiguous:

    Diferencia

without context.

============================================================
9. CASE WITH NO DELIVERED ADVANCE
============================================================

Preserve the accepted rule:

If there is no delivered Advance:

    rendition/funding direction = NO APLICA

Expenses may still contribute to:

    Usado
    categories
    period totals
    operational analytics

But do not invent a return/reimbursement obligation.

============================================================
10. MULTI-ADVANCE LEGACY CASES
============================================================

Preserve current compatibility behavior.

The Case card may show the Case-level net direction.

Each individual Advance/rendition block must continue to show its own
direction.

Do NOT expand FIFO.

Do NOT make FIFO canonical.

Prospective rule remains:

    at most one financially active Advance
    per ExpenseCase + currency.

============================================================
11. ONE ACTIVE ADVANCE COPY
============================================================

Preserve the Owner-approved wording:

Creation refusal:

    "Este expediente ya tiene un anticipo activo en USD.
     Resuelve el anticipo actual antes de registrar otro."

Delivery refusal:

    "Este expediente ya tiene otro anticipo activo en USD.
     Resuelve ese anticipo antes de confirmar esta entrega."

Do not introduce a separate "Finalizar anticipo" Studio command.

============================================================
12. CLOSURE UX — PRESERVE
============================================================

Do not regress the accepted Case closure blockers.

REGISTRADO:

    "El expediente tiene gastos registrados sin enviar a revisión."

PENDIENTE_REVISION:

    "El expediente tiene gastos pendientes de aprobación."

OBSERVADO:

    "El expediente tiene gastos observados pendientes de corrección."

Draft Advances:

    "El expediente tiene anticipos en borrador; confirma su entrega o cancélalos."

Financial difference:

    explain the affected Advance/rendition.

RECHAZADO remains resolved/terminal.

============================================================
13. CONCILIAR UX — PRESERVE
============================================================

Do not regress:

If financial position is unresolved:

    Conciliar disabled

Positive direction:

    "Faltan USD X.XX por justificar o devolver."

Negative direction:

    "Faltan USD X.XX por reembolsar."

Zero difference + valid workflow state:

    Conciliar enabled.

No repeated active reconcile button that only returns the same state.

============================================================
14. READ MODEL AUDIT FIRST
============================================================

Before changing backend code, inspect the current Case card response.

Determine whether the existing API already exposes:

    delivered
    used
    justified
    returned
    reimbursed
    pendingReturn
    pendingReimbursement

or equivalent values.

If all required values already exist:

    Studio-only correction.

If one presentation value is missing:

    add only the minimum read-model field.

Do NOT change financial write behavior.

Do NOT create a migration.

============================================================
15. STUDIO TARGETED TESTS
============================================================

Add/update contracts proving:

A. Closed Case:

    delivered=679
    used=200
    justified=200
    returned=499
    reimbursed=20

renders:

    Entregado USD 679.00
    Usado USD 200.00
    Justificado USD 200.00
    Devuelto USD 499.00
    Reembolsado USD 20.00
    Pendiente de conciliar USD 0.00
    Uso 29%

B. Positive Case balance:

    shows "Por justificar o devolver"

C. Negative Case balance:

    shows "Por reembolsar"

D. Zero open Case:

    shows "Pendiente de conciliar USD 0.00"

E. No delivered Advance:

    financial direction = No aplica

F. Existing multi-advance compatibility remains visible correctly.

G. No horizontal overflow at 375px.

============================================================
16. OWNER MANUAL LOCAL SMOKE PREPARATION
============================================================

After automated verification, leave local runtime ready for Owner testing.

Owner must be able to open:

    EXP. 01: Viaje Loja

and visually verify the corrected financial summary.

Do NOT modify its financial history merely to create the visual state.

Use existing data.

============================================================
17. REHEARSAL_03 — OWNER ACCEPTANCE
============================================================

Record:

GM_EXPENSES_RUNTIME_REHEARSAL_03=
OWNER_ACCEPTED

Accepted evidence:

    V43 → V63 = PASS
    20 migrations = PASS
    0 failures
    gm-expenses row integrity = PASS
    real workflow smoke = 14/14
    reports = PASS
    tenant isolation = PASS
    old settlement calls = 0
    5xx = 0
    Shared DEV modified = NO

Do NOT rerun the entire rehearsal merely for this Studio clarity adjustment
unless backend/migration bytes relevant to rehearsal change.

Apply VERIFIED_BASELINE_REUSE.

============================================================
18. LEGACY SHARED DEV DATA
============================================================

DO NOT clean legacy Shared DEV data in this STEP.

Known legacy conditions from REHEARSAL_03 remain separate:

- 1 OBSERVADO Expense without OBSERVED history;
- 3 CERRADO settlements whose Advances remain EN_RENDICION;
- 16 BORRADOR Advances;
- existing legacy multi-advance Cases;
- 3 standalone Advances without a Case;
- 4 Expenses without a Case.

Do NOT:

- silently backfill review history;
- silently update Advance states;
- silently cancel drafts;
- delete legacy records.

Legacy cleanup is a separate Owner-controlled STEP.

============================================================
19. UNKNOWN TENANTS
============================================================

Tenants 33 and 70 remain:

    UNKNOWN

Do not classify them as test or real data without Owner evidence.

Do not clean their records.

============================================================
20. BOXGHOST EVIDENCE
============================================================

REHEARSAL_03 evidence currently exists only in session scratchpad.

Before the release commit gate:

1. inspect the existing BoxGhost evidence structure;
2. determine the canonical location for gm-expenses evidence;
3. run a secret/sensitive-data check on scripts and results;
4. promote only safe evidence.

Do NOT invent duplicate evidence structures.

If no canonical gm-expenses BoxGhost track exists and naming is ambiguous:

    STOP and report the recommended path.

Do not move dumps, credentials, session cookies, passwords or secrets into
source repositories.

============================================================
21. CANONICAL DOCUMENTATION SYNC
============================================================

Verify Fabric includes the final accepted decisions:

- V62 planned delivery;
- V63 unified RN-001;
- Return + Reimbursement coexistence;
- one active Advance per Case + currency;
- FIFO compatibility-only;
- Case-centered closure;
- canonical financial presentation vocabulary.

Append any new transversal Owner decision to:

    Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md

using the established append-only policy.

Do NOT rewrite or renumber previous rules.

Update:

    active-work/CURRENT_STEP.md

to reflect:

    GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07

and the next release gate.

============================================================
22. DO NOT MIGRATE SHARED DEV YET
============================================================

Although REHEARSAL_03 technically confirms:

    READY_FOR_SHARED_DEV_MIGRATION=YES

the real migration is NOT authorized in this STEP.

Do not:

- migrate 3308;
- rebuild official DEV backend;
- restart stale DEV backend;
- commit;
- push.

============================================================
23. PREPARE REAL SHARED DEV MIGRATION PLAN
============================================================

Prepare only.

The future controlled migration must require:

1. controlled commits of the exact rehearsed/final bytes;
2. fresh Shared DEV backup immediately before migration;
3. re-check Shared DEV Flyway/version/counts;
4. compare against the rehearsal source fingerprint;
5. build backend FROM THE ACCEPTED COMMIT;
6. verify packaged hashes;
7. migrate Shared DEV V43 → V63;
8. rebuild/recreate official DEV backend;
9. Owner real-login smoke;
10. only then declare Shared DEV aligned.

Do not execute this plan now.

============================================================
24. TARGETED VERIFICATION
============================================================

Use VERIFIED_BASELINE_REUSE.

If this STEP remains Studio/read-model only:

Run:

- affected Studio contracts;
- full Studio contracts if inexpensive;
- ESLint changed files;
- fixture smoke;
- 375px responsive smoke.

If a Host read-model field changes:

also run:

- affected Host test;
- only the smallest required real-DB gate.

Do NOT rerun:

- PKG-2D;
- V43→V63 full rehearsal;
- unrelated gm-expenses matrices

unless relevant bytes are invalidated.

============================================================
25. REQUIRED FINAL REPORT
============================================================

Return:

STATUS=
READY_FOR_OWNER_FINAL_MVP_UI_REVIEW

STEP=
GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07

REHEARSAL_03_OWNER_ACCEPTED=YES

FINAL_MIGRATION_HEAD=V63

CASE_CARD_FINANCIAL_CLARITY_FIXED=

CASE_CARD_DELIVERED=
CASE_CARD_USED=
CASE_CARD_JUSTIFIED=
CASE_CARD_RETURNED=
CASE_CARD_REIMBURSED=

PLAIN_DIFFERENCE_LABEL_REMOVED=

CANONICAL_DIRECTION_LABELS_PRESERVED=

CLOSED_CASE_PENDING_RECONCILIATION_ZERO=

CASE_DETAIL_REGRESSION=NO
REPORTS_REGRESSION=NO
CONCILIATION_REGRESSION=NO
CLOSURE_REGRESSION=NO
ONE_ACTIVE_ADVANCE_REGRESSION=NO

BACKEND_FINANCIAL_RULES_CHANGED=NO
MIGRATION_CREATED=NO

FABRIC_SYNCED=
REGLAS_MD_APPENDED=
CURRENT_STEP_UPDATED=

BOXGHOST_EVIDENCE_STATUS=

LEGACY_DEV_DATA_MODIFIED=NO
UNKNOWN_TENANTS_MODIFIED=NO

TEST_RESULTS=
- Studio targeted:
- Studio full:
- ESLint:
- fixture:
- 375px:
- Host targeted (if applicable):

SHARED_DEV_VERSION=V43
SHARED_DEV_MODIFIED=NO

FILES_STAGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

READY_FOR_CONTROLLED_COMMIT_GATE=YES/NO
READY_FOR_SHARED_DEV_MIGRATION_AFTER_COMMIT=YES/NO

STOP_FOR_OWNER_REVIEW=YES

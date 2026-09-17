# GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12
MODE=FINAL_DISPOSABLE_RELEASE_REHEARSAL
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ACCEPTS=GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11
OWNER_DECISION=report zero state uses numeric zeros (no "No aplica" for numeric funding fields without a delivered advance)
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES FINAL RUNTIME REHEARSAL

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12

MODE=
FINAL_DISPOSABLE_RELEASE_REHEARSAL

OWNER_AUTHORIZED=YES

============================================================
0. OWNER ACCEPTANCE
============================================================

The following STEP is now Owner-accepted:

    GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11

Accepted canonical model:

- ExpenseCase is the rendition/funding center.
- Multiple Advances per Case are valid.
- Multiple same-currency Advances are valid.
- Advances are funding tranches.
- Expenses belong to the Case.
- FIFO allocation is removed completely.
- No per-Advance justified allocation is business truth.
- Return/Reimbursement/Conciliar operate at Case + currency level.
- Case close resolves/closes all Advances.
- V62 preserved.
- V63 preserved.
- No new migration was required.

Accepted verification:

    gm-expenses        748/748
    Host real DB       99/99
    Host permission     6/6
    Studio             628/628
    runtime smoke       16/16

============================================================
1. OWNER DECISION — REPORT ZERO STATE
============================================================

Resolve the final presentation inconsistency.

Reports must NOT show:

    No aplica

for numeric funding fields when there is no delivered Advance.

Use numeric zeroes consistently with Case card and detail.

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

Important:

Usado remains the real Expense amount.

Do NOT zero Usado merely because no Advance exists.

This is a presentation/read-model normalization only.

Do not change financial write behavior.

============================================================
2. PURPOSE
============================================================

This is the FINAL runtime rehearsal before:

    controlled commit gate
    → Shared DEV migration
    → official DEV backend rebuild
    → Owner real-login smoke

Do NOT implement new functionality in this STEP.

Do NOT migrate Shared DEV.

============================================================
3. SOURCE AND TARGET
============================================================

SOURCE:

    Shared DEV
    127.0.0.1:3308

Expected source:

    Flyway V43

TARGET:

    disposable exact copy

Final migration head:

    V63

Rehearsal:

    V43 → V63

============================================================
4. READ-ONLY SOURCE SAFETY
============================================================

Shared DEV must remain read-only.

Allowed:

- SELECT
- metadata queries
- mysqldump --single-transaction

Not allowed:

- migration
- UPDATE
- INSERT
- DELETE
- schema changes
- Flyway writes
- backend startup against 3308

Before creating the copy record:

- Flyway version
- Flyway failed rows
- table count
- total row count
- gm-expenses table counts
- relevant legacy data counts

============================================================
5. FRESH SOURCE COPY
============================================================

Create a fresh disposable MySQL 8.4.10 instance.

Do NOT reuse 3310.

Do NOT use 3308.

Use a new temporary port/container.

Copy current Shared DEV read-only.

Do NOT rely only on the previous REHEARSAL_03 dump.

The earlier migration evidence is reusable, but this final rehearsal must use
the current Shared DEV bytes.

Verify copy equality before migration:

- table counts
- row counts
- relevant trigger definitions
- gm-expenses counts
- canonical source fingerprints where practical

If current Shared DEV has materially changed from the accepted rehearsal
source in ways relevant to Expenses:

STOP and report.

============================================================
6. MIGRATION
============================================================

Run the current WORKING TREE backend / accepted migration set against the
disposable copy.

Expected:

    V43 → V63

Reuse the accepted migration evidence only where bytes are still identical.

Verify:

- 0 failed migrations
- V61 identity/security invariants
- V62 planned Advance delivery fields
- V63 unified Return + Reimbursement constraints
- no migration beyond V63
- no business row loss
- no silent rewrite of gm-expenses historical rows

============================================================
7. BUILD EXACT CURRENT WORKING TREE
============================================================

Build current:

    Modules/gm-expenses
    Gystigo Host

Do NOT build from stale committed HEAD.

Record:

- gm-expenses jar SHA-256
- Host jar SHA-256
- build timestamps
- migration head packaged

Prove packaged backend contains:

- Case-level rendition service
- no FIFO allocation class/code
- multiple Advances allowed
- Case-level return endpoint
- Case-level reimbursement endpoint
- Case-level reconcile endpoint
- Case-centered close behavior
- V62 planned delivery behavior
- V63 unified financial behavior

============================================================
8. FINAL CANONICAL FINANCIAL MODEL
============================================================

For one Case + currency:

    totalDelivered
        = SUM(delivered Advances)

    totalJustified
        = SUM(APROBADO Expenses in the Case)

Canonical balance:

    totalDelivered
    + totalReimbursed
    - totalJustified
    - totalReturned
    - totalAdjustments

Reconciliation equation:

    totalDelivered
    + totalReimbursed
    =
    totalJustified
    + totalReturned
    + totalAdjustments

No FIFO.

No per-Advance Expense allocation.

============================================================
9. FINAL MULTIPLE-ADVANCE SCENARIO
============================================================

Execute a real API/runtime scenario equivalent to:

Case:
    Construcción

Advances:
    USD 30,000
    USD  2,000
    USD    300
    USD  5,000

All must be allowed in the same Case and currency.

Total delivered:

    USD 37,300

Approved Expenses:

    USD 35,000

Return:

    USD 2,300

Expected:

    balance = 0

Conciliar:
    succeeds

Cerrar expediente:
    succeeds

All funding Advances must end in the correct terminal state through the
Case-centered closure flow.

No user-facing per-Advance reconciliation steps.

============================================================
10. ADDITIONAL-ADVANCE SCENARIO
============================================================

Prove:

Initial:

    delivered 30,000
    approved  29,500

Then add another Advance:

    +2,000

Expected:

    total delivered = 32,000

No already-approved Expense is reassigned.

No FIFO behavior appears.

Case balance changes only because funding changed.

============================================================
11. RETURN + LATER APPROVAL + REIMBURSEMENT
============================================================

Preserve V63 semantics.

Scenario:

    Advance funding total
    justified
    real Return
    later Expense approval
    reimbursement required

Return and Reimbursement may both exist.

Prove:

- later approval allowed
- reimbursement calculated at Case level
- reimbursement accepted
- final Case balance reaches zero
- Conciliar succeeds
- close succeeds

============================================================
12. DRAFT ADVANCES
============================================================

Multiple drafts are allowed while Case is open.

Creating another Advance must NOT be blocked merely because another Advance
exists.

However:

    unresolved BORRADOR Advance
    → Case closure blocked

Test:

- multiple BORRADOR allowed
- delivery allowed beside other Advances
- closure refused while one BORRADOR remains
- after deliver/cancel, blocker disappears

Use exact singular/plural closure UX semantics where applicable.

============================================================
13. EXPENSE WORKFLOW
============================================================

Run at least one complete Expense lifecycle:

    REGISTRADO
    → PENDIENTE_REVISION
    → APROBADO

and one:

    REGISTRADO
    → PENDIENTE_REVISION
    → OBSERVADO
    → CORRECTION
    → PENDIENTE_REVISION
    → APROBADO

Also prove:

    RECHAZADO

remains terminal/resolved.

Justified total must include APROBADO only.

============================================================
14. CLOSURE BLOCKERS
============================================================

Prove Case cannot close when:

A.
REGISTRADO Expense exists

B.
PENDIENTE_REVISION exists

C.
OBSERVADO exists

D.
BORRADOR Advance exists

E.
financial balance != 0

F.
Case is balanced but not explicitly reconciled

And prove closure succeeds after all blockers are resolved.

============================================================
15. CASE CARD / DETAIL FINANCIAL PRESENTATION
============================================================

Verify final presentation.

Example closed Case:

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

    Conciliado
    100%

    Uso
    29%

Open overuse example:

    Entregado 1,000
    Usado     1,100

Show:

    Uso 110%

Numeric value remains 110%.

Visual usage bar is clamped to 100%.

============================================================
16. ZERO ADVANCE PRESENTATION
============================================================

Verify Owner decision:

No delivered Advance:

    Entregado USD 0.00
    Justificado USD 0.00
    Devuelto USD 0.00
    Reembolsado USD 0.00
    Pendiente de conciliar USD 0.00
    Uso 0%

Usado may still show its real amount.

Reports must use the same numeric zero vocabulary.

Do NOT show:

    No aplica
    —

for these numeric fields.

============================================================
17. REPORTS
============================================================

Verify:

- period summary
- categories
- resources/vehicles as applicable
- related Cases
- delivered
- used
- justified
- returned
- reimbursed
- Por justificar o devolver
- Por reembolsar

Financial direction must be calculated per ExpenseCase first.

Do not net opposite obligations across Cases.

No FIFO-dependent totals.

============================================================
18. ADVANCE DETAIL
============================================================

Each Advance remains individually visible for history.

Advance detail should show operational information only.

Expected rendition wording:

    Rendición:
    Se gestiona desde el expediente

Do NOT expose:

- fake per-Advance Justificado
- fake FIFO balance
- individual Conciliar action

============================================================
19. TENANT ISOLATION
============================================================

Use a second synthetic tenant.

Prove it cannot:

- read Case
- read Advances
- read Expenses
- register movement
- view report data
- mutate any record

Expected:
    404 / empty according to canonical endpoint behavior.

============================================================
20. LEGACY DATA
============================================================

Do NOT repair legacy Shared DEV data.

Only classify/report.

Re-check known shapes:

- OBSERVADO without history
- closed settlements with stale Advance states
- old drafts
- standalone Advances
- Expenses without Case
- multi-Advance Cases

IMPORTANT:

Multiple Advances alone are NO LONGER a legacy defect.

Do not classify them as invalid merely for being multiple.

Only report actual inconsistent states.

============================================================
21. OLD SETTLEMENT API
============================================================

Prove Studio sends no old per-Advance settlement operations for Case Advances.

The old API may remain compatibility-protected internally.

Expected Studio calls:

    /api/expense-cases/{id}/rendition/...

No:

    operational /api/settlements/{id}/...
    or advance-level reconciliation calls

for normal Case workflow.

============================================================
22. CONSOLE / SERVER ERRORS
============================================================

During final smoke:

Require:

    0 application 5xx
    0 unexpected Studio application errors

Known deferred behavior:

    unmapped route may appear as 401

Do not fix it here.

Classify known fixture `/auth/me` 401 separately.

============================================================
23. RESPONSIVE UI
============================================================

Verify at least:

Desktop
375px
320px

Require:

- no horizontal overflow
- financial grid readable
- closed bar shows Conciliado 100%
- Uso still visible
- multiple Advances list remains readable
- closure blocker remains understandable

============================================================
24. DOCUMENTATION / EVIDENCE
============================================================

Verify Fabric contains final canonical model:

- multiple Advances
- funding tranches
- Case-level rendition
- no FIFO
- V62
- V63
- Case-centered closure
- final zero-state vocabulary
- progress indicator semantics

Reglas.md:

append-only history preserved.

CURRENT_STEP:

must point to FINAL_12 during this STEP.

Promote safe final rehearsal evidence to existing:

    GM-EXPENSES-RELEASE-READINESS

BoxGhost track.

Secret scan before promotion.

Do NOT promote:

- passwords
- generated security passwords
- dumps
- cookies
- tokens
- session secrets

============================================================
25. CLEANUP
============================================================

After final rehearsal:

- stop temporary backend
- remove disposable MySQL/container/volume
- free rehearsal ports
- preserve local 8080/3310 Owner environment
- do not touch Shared DEV

============================================================
26. NO COMMIT / NO SHARED DEV
============================================================

Do NOT:

- stage
- commit
- push
- migrate 3308
- rebuild official DEV backend

This STEP ends at Owner review.

============================================================
27. REQUIRED REPORT
============================================================

Return:

STATUS=
READY_FOR_OWNER_FINAL_RUNTIME_REHEARSAL_REVIEW

STEP=
GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12

SOURCE_DB_VERSION=

TARGET_DB_VERSION=V63

SOURCE_COPY_MATCH=

MIGRATION_RESULT=

GM_EXPENSES_JAR_HASH=

HOST_JAR_HASH=

MULTIPLE_ADVANCES_SAME_CURRENCY=

FIFO_CALLERS_FOUND=

CASE_LEVEL_RENDITION_CONFIRMED=

CASE_LEVEL_RETURN_CONFIRMED=

CASE_LEVEL_REIMBURSEMENT_CONFIRMED=

CASE_LEVEL_RECONCILE_CONFIRMED=

CASE_LEVEL_CLOSE_CONFIRMED=

DRAFT_CLOSURE_BLOCKER=

EXPENSE_WORKFLOW_SMOKE=

RETURN_PLUS_REIMBURSEMENT_SMOKE=

ZERO_ADVANCE_REPORT_VALUES=

USAGE_OVER_100_SMOKE=

CLOSED_CONCILIATED_100=

REPORTS_SMOKE=

TENANT_ISOLATION_SMOKE=

OLD_SETTLEMENT_STUDIO_CALLS=

SERVER_5XX=

UNEXPECTED_CONSOLE_ERRORS=

LEGACY_INCONSISTENCIES=

MULTIPLE_ADVANCES_CLASSIFIED_AS_DEFECT=NO

FABRIC_FINAL_MODEL_CONFIRMED=

BOXGHOST_FINAL_EVIDENCE=

REHEARSAL_ENVIRONMENT_REMOVED=

SHARED_DEV_VERSION=V43
SHARED_DEV_MODIFIED=NO

FILES_STAGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

READY_FOR_CONTROLLED_COMMIT_GATE=YES/NO

READY_FOR_SHARED_DEV_MIGRATION_AFTER_COMMIT=YES/NO

STOP_FOR_OWNER_REVIEW=YES

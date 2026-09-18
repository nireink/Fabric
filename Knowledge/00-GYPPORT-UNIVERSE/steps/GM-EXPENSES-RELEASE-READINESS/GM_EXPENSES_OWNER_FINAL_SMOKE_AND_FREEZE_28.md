# GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28
MODE=OWNER_RUNTIME_VERIFICATION_THEN_AUTHENTICATED_CORRECTION_THEN_FREEZE
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner final smoke, authenticated correction of the USD 300 return and MVP freeze
ACCEPTED_BASELINE=gm-expenses 39a2adf, Gystigo 5eed5d6, Fabric 1f5bed8, Shared DEV V65
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES OWNER FINAL SMOKE + MVP FREEZE

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28

MODE=
OWNER_RUNTIME_VERIFICATION
→ AUTHENTICATED_CORRECTION
→ FINAL_SMOKE
→ EVIDENCE_CLOSURE
→ MVP_FREEZE

OWNER_AUTHORIZED=YES

PUSH_AUTHORIZED=NO


============================================================
0. PURPOSE
============================================================

V65 is already deployed successfully.

Current runtime:

    Shared DEV = V65

gm-expenses source:

    39a2adf4dfff0196208a1f80719be1c12c047ac2

Gystigo source:

    5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc

Fabric source baseline:

    1f5bed831c54d01efe74444f02ee2b2d947df549


This STEP performs the final Owner smoke and closes gm-expenses MVP.

No redesign.

No new feature.

No migration.

No financial rule change.

No numbering change.


============================================================
1. FINAL NUMBERING MODEL — FREEZE
============================================================

Canonical forever for this MVP:

UUID
    = technical resource identifier

expense_sequence
    = permanent tenant-scoped expediente sequence
    = EXP. NN
    = does NOT reset daily

case_sequence
    = daily sequence
    = TENANT + BUSINESS_DATE
    = used for ID only

case_number
    = YYYYMMDD####
    = visible ID


Examples from real Shared DEV:

    EXP. 08: Compra Filtro
    ID: 202609170001

    EXP. 09: VIAJE QUITO
    ID: 202609170002


Do not reinterpret these concepts.


============================================================
2. OWNER VISUAL ACCEPTANCE
============================================================

Owner must verify in the REAL app:

    http://localhost:5173


Confirm:

    Compra Filtro:
        EXP. 08
        Fecha: 2026-09-17
        ID: 202609170001

    VIAJE QUITO:
        EXP. 09
        Fecha: 2026-09-17
        ID: 202609170002


Also visually confirm hierarchy:

    EXP / Fecha / ID

    divider

    Responsable
    Supervisor
    Recurso asignado
    Conciliado

    divider

    Finanzas


Record:

    OWNER_NUMBERING_VISUAL_ACCEPTED=
    YES/NO

    OWNER_LAYOUT_VISUAL_ACCEPTED=
    YES/NO


============================================================
3. OWNER CASE — PRE-CORRECTION STATE
============================================================

Target:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0
    Compra Filtro


Expected before reversal:

    Total anticipos = USD 320.00
    Total gastos = USD 400.00

    Total a conciliar =
    USD 80.00
    Por reembolsar

    Devuelto =
    USD 300.00

    Reembolsado =
    USD 0.00

    Pendiente =
    USD 380.00
    Por reembolsar

    Usado =
    USD 400.00

    Uso =
    125%


Confirm exact values before correction.


============================================================
4. AUTHENTICATED REVERSAL
============================================================

The two historical Return events:

    USD 200
    USD 100

are grouped by the product as one visible movement:

    Devolución USD 300.00


The Owner confirmed no real cash Return occurred.

Use the REAL authenticated product workflow to reverse that movement.


Do NOT:

- direct-update DB;
- delete events;
- modify immutable history;
- fabricate actor;
- run SQL correction.


Use:

    Reverse / Reversar devolución


Reason:

    Corrección de devolución registrada durante prueba del MVP;
    no existió devolución real de efectivo.


or equivalent Owner-entered reason.


The operation must record:

    authenticated global UserAccount
    server timestamp
    original movement reference
    reversal relationship


============================================================
5. REVERSAL AUDIT PROOF
============================================================

After Owner reversal, prove:

Original events remain:

    RETURN_REGISTERED 200
    RETURN_REGISTERED 100


Reversal event(s) appended:

    RETURN_REVERSED


Require:

    originals unchanged
    reversal references original movement(s)
    actor populated
    timestamp populated
    reason populated
    duplicate reversal refused


No direct data mutation.


============================================================
6. EXPECTED POST-REVERSAL FINANCIAL STATE
============================================================

After reversal:

    Total anticipos
    USD 320.00

    Total gastos
    USD 400.00

    Total a conciliar
    USD 80.00
    Por reembolsar

    Devuelto
    USD 0.00

    Reembolsado
    USD 0.00

    Pendiente
    USD 80.00
    Por reembolsar

    Usado
    USD 400.00

    Uso
    125%


Require BOTH:

    Case Card
    Case Detail

to show the same result.


============================================================
7. REJECTED EXPENSE
============================================================

Verify the rejected USD 200 Expense remains:

    RECHAZADO

and visible in history.


Financial effect must remain:

    ZERO


It must NOT alter:

    Total gastos
    Devuelto
    Reembolsado
    Pendiente


============================================================
8. FINAL ACTION STATE
============================================================

After the reversal the Case should correctly offer:

    Registrar reembolso

for:

    USD 80.00


Do NOT register the reimbursement unless the Owner explicitly wants to test
the complete settlement-to-zero flow now.


The MVP may be accepted while the real Case legitimately remains:

    Pendiente USD 80.00 Por reembolsar


because that represents the actual business position.


============================================================
9. CROSS-SURFACE CONSISTENCY
============================================================

Verify:

CARD:

    EXP. 08
    ID: 202609170001
    Total anticipos 320
    Total gastos 400
    Total a conciliar 80 Por reembolsar
    Devuelto 0
    Reembolsado 0
    Pendiente 80 Por reembolsar
    Usado 400
    Uso 125%


DETAIL:

same business identifier and same financial summary.


Require:

    CARD_DETAIL_NUMBERING_CONSISTENCY=YES

    CARD_DETAIL_FINANCIAL_CONSISTENCY=YES


============================================================
10. NARROW FINAL SMOKE
============================================================

Run only the final affected smoke.

Verify:

- backend health;
- Shared DEV V65;
- ExpenseCase list;
- ExpenseCase detail;
- expenseSequence;
- caseNumber;
- businessDate;
- UUID route;
- financial summary;
- rejected Expense effect zero;
- reversal history;
- duplicate reversal rejection;
- tenant isolation;
- HTTP 5xx = 0.


Do NOT rerun unrelated platform suites.


============================================================
11. NO SOURCE CHANGES
============================================================

This STEP should not require code modifications.

Expected:

    SOURCE_CODE_CHANGED=NO


If a defect is found:

    STOP.

Do not repair it inside the freeze STEP.

Report exact blocker.


============================================================
12. STEP 27 EVIDENCE
============================================================

STEP 27 deployment evidence is currently uncommitted in Fabric.

Include it in the final Fabric closure commit together with:

- this STEP 28 prompt;
- final Owner-smoke evidence;
- reversal evidence;
- final baseline record;
- CURRENT_STEP;
- append-only canonical rule if needed.


Do NOT alter historical evidence.


============================================================
13. SYNTHETIC DEV DATA
============================================================

STEP 18/24/27 smoke may have left synthetic:

    @example.test

tenants/accounts/data in Shared DEV.


Audit them.

Do NOT automatically delete unless the existing evidence clearly marks them
as disposable and cleanup is safe.


If cleanup is straightforward and audit-preserving:

report exact cleanup proposal.

Do not let synthetic cleanup block MVP freeze unless it materially affects
product behavior.


============================================================
14. FINAL BASELINE
============================================================

If all Owner smoke checks pass, create the final baseline:

    GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17


Record exact:

GM_EXPENSES_HEAD=
39a2adf4dfff0196208a1f80719be1c12c047ac2

GYSTIGO_HEAD=
5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc

SHARED_DEV_FLYWAY=
65


Fabric HEAD will become the final closure commit.


Record:

- test evidence;
- deployment evidence;
- final numbering model;
- final financial semantics;
- known accepted technical debt;
- unrelated WIP exclusions;
- push status.


============================================================
15. FINAL FABRIC COMMIT
============================================================

After all Owner-smoke gates pass:

stage ONLY accepted Fabric closure paths.


Do NOT stage unrelated Fabric WIP.


Create ONE local Fabric commit for:

- STEP 27 deployment evidence;
- STEP 28 final smoke;
- reversal evidence;
- final MVP baseline;
- CURRENT_STEP closure.


Suggested intent:

    fabric: freeze gm-expenses MVP baseline


No gm-expenses code commit expected.

No Gystigo code commit expected.


============================================================
16. MVP FREEZE
============================================================

If everything passes:

    GM_EXPENSES_MVP_STATUS=
    FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL


From this point:

no more MVP architecture/UI changes without a new explicit track.


New ideas become:

    backlog
    post-MVP
    next release


============================================================
17. PUSH
============================================================

Do NOT push yet.

Expected:

    PUSH_PERFORMED=NO


Owner authorizes push separately after reviewing the freeze report.


============================================================
18. REQUIRED FINAL REPORT
============================================================

Return:


STEP=
GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28


STATUS=
FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL
or
BLOCKED


OWNER_VISUAL:

COMPRA_FILTRO_EXP_DISPLAY=
EXP. 08

COMPRA_FILTRO_ID=
202609170001

VIAJE_QUITO_EXP_DISPLAY=
EXP. 09

VIAJE_QUITO_ID=
202609170002

OWNER_NUMBERING_VISUAL_ACCEPTED=
YES/NO

OWNER_LAYOUT_VISUAL_ACCEPTED=
YES/NO


PRE_REVERSAL:

TOTAL_ADVANCES=
320

TOTAL_EXPENSES=
400

TOTAL_TO_RECONCILE=
80 POR_REEMBOLSAR

RETURNED=
300

REIMBURSED=
0

PENDING=
380 POR_REEMBOLSAR


REVERSAL:

REVERSAL_EXECUTED_BY_OWNER=
YES/NO

REVERSAL_REASON=

ORIGINAL_EVENTS_PRESERVED=
YES/NO

REVERSAL_EVENT_APPENDED=
YES/NO

AUTHENTICATED_ACTOR_RECORDED=
YES/NO

DUPLICATE_REVERSAL_BLOCKED=
YES/NO


POST_REVERSAL:

TOTAL_ADVANCES=
320

TOTAL_EXPENSES=
400

TOTAL_TO_RECONCILE=
80 POR_REEMBOLSAR

RETURNED=
0

REIMBURSED=
0

PENDING=
80 POR_REEMBOLSAR

USED=
400

USAGE=
125%


REJECTED_EXPENSE:

REJECTED_AMOUNT=
200

FINANCIAL_EFFECT=
0


CONSISTENCY:

CARD_DETAIL_NUMBERING_CONSISTENCY=
YES/NO

CARD_DETAIL_FINANCIAL_CONSISTENCY=
YES/NO


RUNTIME:

SHARED_DEV_VERSION=
65

BACKEND_HEALTH=
PASS/FAIL

HTTP_5XX_COUNT=

TENANT_ISOLATION=
PASS/FAIL


SMOKE:

SMOKE_CHECKS=
SMOKE_FAILURES=


SOURCE:

GM_EXPENSES_HEAD=
39a2adf4dfff0196208a1f80719be1c12c047ac2

GYSTIGO_HEAD=
5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc

SOURCE_CODE_CHANGED=
NO


FABRIC:

FINAL_FABRIC_COMMIT_CREATED=
YES/NO

FINAL_FABRIC_HEAD=

STEP27_EVIDENCE_COMMITTED=
YES/NO

STEP28_EVIDENCE_COMMITTED=
YES/NO


BASELINE:

BASELINE_NAME=
GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17

GM_EXPENSES_MVP_STATUS=
FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL


SYNTHETIC_DEV_DATA:

SYNTHETIC_TENANTS_FOUND=

CLEANUP_REQUIRED=
YES/NO

CLEANUP_PROPOSAL=


OPERATIONS:

PUSH_PERFORMED=
NO

UNRELATED_WIP_PRESERVED=
YES/NO


NEXT_ACTION=

Owner authorizes final push when desired.


STOP=
YES

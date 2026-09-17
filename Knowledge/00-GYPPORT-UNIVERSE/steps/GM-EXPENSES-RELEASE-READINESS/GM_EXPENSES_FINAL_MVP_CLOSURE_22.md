# GM_EXPENSES_FINAL_MVP_CLOSURE_22 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_FINAL_MVP_CLOSURE_22
MODE=AUDIT_CURRENT_WIP_THEN_IMPLEMENT_THEN_VERIFY_THEN_REHEARSE
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner consolidated closure of the gm-expenses MVP after STEPs 19, 20, 20A and 21
ACCEPTED_BASELINE=gm-expenses 545eae0, Gystigo bcb9591, Fabric bbdd66a, Shared DEV V63
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES FINAL MVP CLOSURE
OWNER SMOKE FINANCIAL CONSISTENCY + ID GASTO + HEADER HIERARCHY + WIP CONSOLIDATION

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_FINAL_MVP_CLOSURE_22

MODE=
AUDIT_CURRENT_WIP
→ IMPLEMENT_FINAL_REQUIREMENTS
→ VERIFY
→ V64_REHEARSAL
→ PREPARE_CONTROLLED_COMMIT_GATE

OWNER_AUTHORIZED=YES

IMPORTANT:

This is ONE consolidated STEP.

Do NOT split this into separate implementation STEPs unless a real technical
blocker makes the implementation unsafe.

Do NOT push.

Do NOT modify live Shared DEV in this STEP.

Do NOT automatically correct the Owner's live financial movements.

Do NOT commit yet.

At the end, all accepted work must be classified and ready for ONE controlled
commit gate after Owner visual acceptance.


======================================================================
0. CURRENT ACCEPTED CONTEXT
======================================================================

Accepted/deployed baseline before Owner-smoke fixes:

gm-expenses:
    545eae0fb287f8e04f7f1b4ac73780304ec53f22

Gystigo:
    bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f

Fabric:
    bbdd66a0c5a1c9cbb21293beb74c3e5e61cc5de0

Shared DEV:
    V63

Official DEV backend:
    STEP 18 image / accepted pre-owner-smoke commit

Known accepted later working-tree work:

- STEP 19 audit/evidence
- STEP 20 financial semantics + movement reversal
- STEP 20A card alignment/base-balance fix
- STEP 21 financial consistency/addendum work
- header grouping work
- Studio/Host/domain tests and evidence
- Fabric documentation/evidence

Nothing from these later STEPs is committed yet.

The Owner currently sees approximately 32+ source-control changes.

Those changes MUST be inventoried and preserved.

Do not lose accepted work.


======================================================================
1. OWNER FINAL BUSINESS FACTS — AUTHORITATIVE
======================================================================

Target real Owner Case:

    UUID:
    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0

    Name:
    Compra Filtro


ADVANCES:

    USD 200.00    EN_RENDICION
    USD 100.00    EN_RENDICION
    USD  20.00    ENTREGADO


All three represent money that was actually delivered.

Therefore:

    TOTAL_ADVANCES = USD 320.00


EXPENSES:

    USD 200.00    APROBADO
    USD  80.00    APROBADO
    USD  90.00    APROBADO
    USD  30.00    APROBADO

    USD 200.00    RECHAZADO


Therefore:

    TOTAL_APPROVED_EXPENSES = USD 400.00

The rejected USD 200 has:

    FINANCIAL_EFFECT = ZERO


OWNER BUSINESS REALITY:

    REAL_RETURN = USD 0.00
    REAL_REIMBURSEMENT = USD 0.00


Base result:

    320 - 400 = -80

Display:

    USD 80.00
    Por reembolsar


======================================================================
2. CANONICAL ADVANCE RULE
======================================================================

TOTAL_ADVANCES means:

    SUM of Advances for which money was ACTUALLY DELIVERED.


Lifecycle state does not erase historical funding.

A delivered Advance remains part of Total anticipos when later state is:

    ENTREGADO
    EN_RENDICION
    RENDIDO
    CERRADO

if its delivery actually occurred.


A Draft/Cancelled Advance that was never delivered contributes:

    ZERO


Do NOT infer funding from current state name alone.

Use actual delivery semantics.


======================================================================
3. CANONICAL EXPENSE RULE
======================================================================

TOTAL_EXPENSES_FOR_RECONCILIATION =

    SUM(EXPENSES WHERE STATE = APROBADO)


Financial effect:

    REGISTRADO          = 0
    PENDIENTE_REVISION  = 0
    OBSERVADO           = 0
    RECHAZADO           = 0
    APROBADO            = full amount


IMPORTANT:

Do NOT implement:

    approved - rejected

because rejected Expenses are already outside the approved set.


A rejected Expense:

- stays in immutable history;
- remains visible/auditable;
- does NOT become an Advance;
- does NOT become a Return;
- does NOT become a Reimbursement;
- does NOT become an Adjustment;
- is NOT subtracted a second time.


======================================================================
4. BASE RECONCILIATION
======================================================================

Canonical base balance:

    BASE_BALANCE =
        TOTAL_ADVANCES
        - TOTAL_APPROVED_EXPENSES


For Owner fixture:

    320 - 400 = -80


UI:

    Total a conciliar
    USD 80.00
    Por reembolsar


Use positive amount + direction in normal UI.

Internal signed value may remain:

    -80


======================================================================
5. REAL MONEY MOVEMENTS
======================================================================

RETURN means:

    responsible person actually returned real money to the company.


REIMBURSEMENT means:

    company actually paid additional real money to the responsible person.


They must only originate from explicit money-movement operations.


Rejecting/observing/correcting an Expense MUST NOT automatically create:

    Return
    Reimbursement
    Advance
    Adjustment


======================================================================
6. FINAL POSITION
======================================================================

Canonical final balance:

    FINAL_BALANCE =
        TOTAL_ADVANCES
        + TOTAL_REIMBURSED
        - TOTAL_APPROVED_EXPENSES
        - TOTAL_RETURNED
        - TOTAL_ADJUSTMENTS


For the real business facts:

    320 + 0 - 400 - 0 - 0
    = -80


Therefore expected final state:

    Devuelto
    USD 0.00

    Reembolsado
    USD 0.00

    Pendiente
    USD 80.00
    Por reembolsar


======================================================================
7. STORED USD 300 HISTORY — DO NOT HIDE IT
======================================================================

Previous audit found two stored Return events:

    USD 200
    USD 100

total:

    USD 300


Owner confirms:

    NO real cash Return happened.


The earlier audit proved these events came from an explicit old
"Registrar devolución" action and NOT from Expense rejection.


Do NOT:

- delete them;
- update them;
- hide them in Studio;
- subtract them using a UI-only workaround;
- fabricate correction history;
- fabricate an actor.


Preserve immutable history.


The STEP 20 append-only reversal mechanism remains canonical.


Required historical correction model:

    Original RETURN USD 200
    Reversal        USD 200

    Original RETURN USD 100
    Reversal        USD 100


NET RETURN:

    USD 0.00


======================================================================
8. DO NOT MODIFY OWNER LIVE CASE DURING THIS STEP
======================================================================

This STEP implements/verifies the correct product behavior.

Do NOT mutate the real Shared DEV Owner Case.


After commit + deployment, the real correction must happen through:

    authenticated product reversal workflow

so the real global UserAccount actor and server timestamp are recorded.


Until deployment/reversal, the current Shared DEV Case may still show:

    Devuelto = 300
    Pendiente = 380


That does NOT authorize hiding those values in Studio.


======================================================================
9. RETURN REVERSAL — FREEZE ACCEPTED DESIGN
======================================================================

Preserve STEP 20 behavior:

- append-only compensating event;
- original event remains immutable;
- reversal references original event;
- reversal amount = original amount;
- one reversal maximum per original movement;
- reason required;
- actor = authenticated global UserAccount;
- authoritative timestamp;
- closed Case cannot receive reversal;
- double reversal refused;
- idempotency preserved;
- Case requires reconciliation again after balance-changing reversal.


Do NOT create a second reversal architecture.

Reuse the existing V11-compatible mechanism.


======================================================================
10. BOTH FINANCIAL SURFACES ARE IN SCOPE
======================================================================

The same canonical financial information must appear in:

A.
ExpenseCase Card/List

B.
ExpenseCase Detail:
    Resumen financiero
    Rendición del expediente


Do NOT consider the STEP complete if only one surface is correct.


======================================================================
11. FINAL FINANCE CARD — OWNER ACCEPTED STRUCTURE
======================================================================

Required semantic hierarchy:

    Finanzas

    Total anticipos     Total gastos       Total a conciliar       Uso
    USD 320.00          USD 400.00         USD 80.00               125% │BAR│
                                            Por reembolsar

    Devuelto            Reembolsado        Pendiente
    USD 0.00            USD 0.00           USD 80.00
                                            Por reembolsar

    Usado
    USD 400.00


Uso:

    text may exceed 100%

Example:

    125%


Visual bar:

    clamp fill to 100%


Usado remains operational/statistical.

It does NOT determine reconciliation.


======================================================================
12. DETAIL PAGE — OWNER ACCEPTED RESULT
======================================================================

Resumen financiero
Rendición del expediente


Expected:

    Total anticipos
    USD 320.00

    Total gastos
    USD 400.00

    Total a conciliar
    USD 80.00 · Por reembolsar

    Devuelto
    USD 0.00

    Reembolsado
    USD 0.00

    Pendiente
    USD 80.00 · Por reembolsar

    Usado
    USD 400.00


Message:

    Faltan USD 80.00 por reembolsar.


NOT:

    Faltan USD 380.00 por reembolsar.


Available action:

    Registrar reembolso


After a real reimbursement of USD 80:

    Reembolsado = USD 80.00
    Pendiente = USD 0.00


Then reconciliation may proceed subject to other blockers.


======================================================================
13. CARD ↔ DETAIL CONSISTENCY
======================================================================

Add/retain a contract proving both surfaces receive/display the same canonical
summary.


Fixture:

    advances delivered = 320
    approved expenses = 400
    rejected expense = 200
    net returned = 0
    reimbursed = 0


Both surfaces:

    Total anticipos = 320
    Total gastos = 400
    Total a conciliar = 80 POR_REEMBOLSAR
    Devuelto = 0
    Reembolsado = 0
    Pendiente = 80 POR_REEMBOLSAR
    Usado = 400


Card additionally:

    Uso = 125%


Rejected USD 200 changes none of those financial totals.


======================================================================
14. ID GASTO — FINAL OWNER DECISION
======================================================================

ID Gasto is REQUIRED for MVP closure.


The earlier rule:

    TENANT
    + ESTABLISHMENT
    + BUSINESS_DATE

for the visible caseNumber sequence is SUPERSEDED.


Canonical sequence scope is now:

    TENANT
    + BUSINESS_DATE


Establishment is NOT required to generate ID Gasto.


Therefore:

absence of fiscal Establishment data MUST NOT block caseNumber generation.


======================================================================
15. IDENTIFIER LEVELS
======================================================================

A. TECHNICAL RESOURCE ID

    UUID


Example:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0


UUID remains the API routing identifier.


B. VISIBLE BUSINESS CASE NUMBER

    caseNumber


Format:

    YYYYMMDD####


Example:

    202609170001


Normal UI:

    ID Gasto: 202609170001


C. FULL BUSINESS REFERENCE

When fiscal/establishment information exists:

    RUC-ESTABLISHMENT_NUMBER-CASE_NUMBER


Example:

    1191771814001-001-202609170001


The full reference is NOT required to generate caseNumber.

It is NOT normally displayed on the standard Case card.


======================================================================
16. FULL REFERENCE SEMANTICS
======================================================================

Internal tenant relationship remains:

    tenant_id


RUC is NOT tenant_id.


Establishment is optional context for:

    fullBusinessReference


Do NOT duplicate inside gm-expenses:

- RUC master;
- Organization master;
- Establishment master.


Do NOT fabricate:

    establishment 001


Do NOT create cross-module JDBC.


If full reference cannot currently be composed:

    fullBusinessReference = unavailable/null


But:

    caseNumber remains fully valid.


======================================================================
17. CASE NUMBER FORMAT
======================================================================

Format:

    YYYYMMDD####


Example:

    202609170001


Components:

    YYYYMMDD = persisted business date

    #### = tenant-daily sequence


Sequence range:

    0001 → 9999


If a tenant genuinely exceeds 9999 Cases in one business day:

    reject creation with a clear domain error

for this MVP.


Do NOT silently expand the format without Owner approval.


======================================================================
18. CASE NUMBER UNIQUENESS
======================================================================

Canonical uniqueness:

    tenant_id
    + case_business_date
    + case_sequence


Also enforce:

    UNIQUE (tenant_id, case_number)


Example Tenant A:

    202609170001
    202609170002
    202609170003


Tenant B may independently have:

    202609170001


No global collision problem exists because tenant ownership remains explicit.


======================================================================
19. BUSINESS DATE
======================================================================

Persist:

    case_business_date


The visible:

    Fecha

and:

    YYYYMMDD

inside ID Gasto must use the SAME persisted business date.


Required:

    Fecha: 2026-09-17
    ID Gasto: 202609170001


For NEW Cases:

resolve business date through:

1.
tenant.time_zone when configured;

else

2.
a Host/platform configurable default business timezone.


Do NOT hardcode:

    America/Guayaquil

inside gm-expenses domain logic.


For DEV/Ecuador configuration the Host/platform property may resolve to:

    America/Guayaquil


Use a generic configuration concept such as:

    gypport.business.default-zone


or the existing equivalent if one already exists.


Do not open a broad timezone redesign.


======================================================================
20. HISTORICAL DATE BACKFILL
======================================================================

Do NOT retroactively re-date historical Cases based on a new timezone rule.


For existing Cases:

preserve the date semantics that users historically saw.

Backfill historical:

    case_business_date

using the current historical visible-date basis for those records.


Then assign sequence deterministically per:

    tenant
    case_business_date


Ordering:

    created_at
    stable internal id


This keeps historical Fecha and new ID Gasto consistent without rewriting
history.


======================================================================
21. V64 — AUTHORIZED
======================================================================

Current migration head:

    V63


Create:

    V64


V64 scope ONLY:

- expense_case.case_business_date
- expense_case.case_sequence
- expense_case.case_number
- persistent sequence/counter infrastructure if required
- deterministic historical backfill
- uniqueness constraints
- immutability protection


Do NOT add:

- RUC;
- Establishment master;
- Return cleanup;
- Reimbursement cleanup;
- unrelated schema work.


======================================================================
22. CONCURRENCY-SAFE NUMBER GENERATION
======================================================================

Generation must be:

- server-side;
- persistent;
- transactional;
- concurrency-safe;
- tenant + business-date scoped.


Do NOT use:

    SELECT MAX(...) + 1

without real locking/concurrency guarantees.


Do NOT use:

- frontend generation;
- process-memory counters;
- UI list count;
- EXP. NN;
- UUID transformation;
- SRI document_sequences.


Use a dedicated sequence/counter persistence mechanism appropriate to the
current JdbcTemplate architecture.


======================================================================
23. FAILED CREATION SEMANTICS
======================================================================

A failed Case creation must NOT create:

- duplicate caseNumber;
- corrupt sequence state;
- partially-created Case.


Prefer sequence allocation inside the same database transaction.


If gaps can occur only due to transaction semantics, document the exact
behavior.

Never reuse a caseNumber already committed.


======================================================================
24. CASE NUMBER IMMUTABILITY
======================================================================

Once created:

    case_business_date
    case_sequence
    case_number

must never change.


Later timezone configuration changes MUST NOT renumber old Cases.


Add domain/persistence/database protection consistent with existing project
conventions.


======================================================================
25. API
======================================================================

Expose in Case list/detail:

    businessDate
    caseNumber


Preserve all existing:

    UUID routes


Do NOT replace technical routing with caseNumber.


Host may later compose:

    fullBusinessReference

when tax identity and establishment are available.


gm-expenses must not directly query fiscal tables.


======================================================================
26. NEW HEADER VISUAL HIERARCHY
======================================================================

The Owner wants three clearly readable regions:

1.
CASE IDENTITY

2.
ASSIGNMENT

3.
FINANCE


Do NOT use visually heavy nested cards.


Use spacing + subtle hairline dividers consistent with GYPPORT.


======================================================================
27. HEADER — CASE IDENTITY SECTION
======================================================================

Required:

    EXP. 01: VIAJE QUITO
    Fecha: 2026-09-17
    ID Gasto: 202609170001


This forms the first visual group.


Do NOT display the technical UUID.


Do NOT display the full RUC-establishment-case reference here.


======================================================================
28. HEADER — ASSIGNMENT SECTION
======================================================================

After a subtle divider/spacing:

    Responsable:       Eduardo Burgasí
    Supervisor:        Eduardo Burgasí
    Recurso asignado:  Sin recurso


Preserve:

- label/value same row on desktop;
- current label width;
- typography;
- line heights;
- resource readability.


Do NOT deform these fields to make room for ID Gasto.


======================================================================
29. CONCILIADO POSITION
======================================================================

Keep status:

    Abierto / Cerrado

top-right.


Keep:

    Conciliado

in the Assignment region.


Its vertical top should remain approximately aligned with:

    Responsable


Do NOT move Conciliado into the Case Identity region.


Preserve the STEP 15 structural alignment contract.


No margin hack.


======================================================================
30. FINANCE DIVIDER
======================================================================

After Assignment:

    subtle horizontal divider


Then:

    Finanzas


Keep the accepted financial hierarchy from sections 11–13.


======================================================================
31. CARD HEADER TARGET
======================================================================

Conceptual desktop result:


    EXP. 01: VIAJE QUITO                              Cerrado
    Fecha: 2026-09-17
    ID Gasto: 202609170001


    ------------------------------------------------------------


    Responsable:       Eduardo Burgasí                Conciliado
    Supervisor:        Eduardo Burgasí                100% │BAR│
    Recurso asignado:  Sin recurso


    ------------------------------------------------------------


    Finanzas


    Total anticipos     Total gastos       Total a conciliar       Uso
    USD 200.00          USD 200.00         USD 0.00                100% │BAR│
                                            Balanceado


    Devuelto            Reembolsado        Pendiente
    USD 0.00            USD 0.00           USD 0.00


    Usado
    USD 200.00


======================================================================
32. DETAIL HEADER
======================================================================

Where the ExpenseCase detail has an equivalent identity header, it must also
show:

    Fecha
    ID Gasto


Require:

    CARD_CASE_NUMBER == DETAIL_CASE_NUMBER == API_CASE_NUMBER


Do not implement ID Gasto only on the list card.


======================================================================
33. RESPONSIVE
======================================================================

Verify the card itself at:

    1280
    768
    375
    320


Do not let the application shell/sidebar invalidate the measurement.

If necessary use the existing forced-width card fixture.


Require:

1280:
    full desktop hierarchy

768:
    readable hierarchy, no overflow

375:
    natural stacking / 2-column finance where accepted

320:
    no overlap
    no horizontal overflow
    all labels readable


Identity / Assignment / Finance grouping must remain visually understandable
at every width.


======================================================================
34. OWNER FINANCIAL REGRESSION FIXTURE
======================================================================

Fixture:

ADVANCES:

    200 delivered
    100 delivered
     20 delivered


APPROVED EXPENSES:

    200
     80
     90
     30


REJECTED:

    200


NET REAL RETURN:

    0


REAL REIMBURSEMENT:

    0


Expected:

    TOTAL_ADVANCES = 320
    TOTAL_EXPENSES = 400

    REJECTED_FINANCIAL_EFFECT = 0

    TOTAL_TO_RECONCILE = 80
    DIRECTION = POR_REEMBOLSAR

    RETURNED = 0
    REIMBURSED = 0

    FINAL_PENDING = 80
    DIRECTION = POR_REEMBOLSAR

    USED = 400
    USAGE = 125%


======================================================================
35. REQUIRED FINANCIAL TESTS
======================================================================

Prove:

A.
Delivered Advance counts exactly once.

B.
EN_RENDICION Advance remains delivered funding.

C.
RENDIDO/CERRADO delivered funding remains historical funding.

D.
Draft not delivered = zero.

E.
Rejected Expense = zero.

F.
Observed Expense = zero.

G.
Pending Review Expense = zero.

H.
Approved Expense counts exactly once.

I.
Rejection creates no financial movement.

J.
Return only from explicit Return command.

K.
Reimbursement only from explicit Reimbursement command.

L.
Reversal restores the original movement's financial effect.

M.
Original event remains immutable.

N.
Double reversal blocked.


======================================================================
36. REQUIRED ID GASTO TESTS
======================================================================

A.

Tenant A / 2026-09-17
first Case:

    202609170001


B.

second Case:

    202609170002


C.

Tenant B / same date:

    202609170001


D.

Next business date:

    202609180001


E.

Concurrent creation:
    no duplicates.


F.

Failed transaction:
    no corrupt sequence state.


G.

caseNumber immutable.


H.

businessDate immutable.


I.

Fecha and YYYYMMDD always match.


J.

UUID routes unchanged.


K.

No Establishment required.


L.

No RUC copied into gm-expenses.


M.

SRI sequence not reused.


======================================================================
37. V64 DISPOSABLE REHEARSAL
======================================================================

Before any live Shared DEV migration:

create a fresh disposable copy of current V63 Shared DEV.


Apply V64.


Verify:

- all existing ExpenseCases backfilled;
- deterministic values;
- duplicate caseNumbers = 0;
- historical financial rows unchanged;
- settlement_balance_event unchanged;
- review history unchanged;
- no Establishment fabricated;
- uniqueness works;
- immutability works;
- real concurrent number generation works.


Do NOT modify actual Shared DEV.


======================================================================
38. CURRENT API VERSION MISMATCH
======================================================================

The running official DEV backend may still be the STEP 18 image.


Current Studio may be working-tree/newer code.


Do NOT confuse:

    new Studio + old API

with final deployed behavior.


Report:

    WORKING_TREE_API_VERSION
    RUNNING_DEV_API_VERSION


Before deployment it is expected that:

    WORKING_TREE_API_SUPPORTS_CASE_NUMBER=YES
    RUNNING_DEV_API_SUPPORTS_CASE_NUMBER=NO


Do NOT create a fake Studio-only caseNumber fallback.


======================================================================
39. CURRENT DIRTY WORKTREE — MANDATORY AUDIT
======================================================================

There are approximately 32+ pending source-control changes.


Before finalizing this STEP, inventory exact paths in:

    Modules/gm-expenses
    Gystigo
    Fabric


Classify EVERY dirty path as:

A.
accepted financial/domain implementation

B.
accepted Host/API work

C.
accepted Studio/UI work

D.
ID Gasto/V64 work

E.
Fabric documentation/evidence

F.
unrelated pre-existing WIP

G.
generated/runtime

H.
unknown


Require:

    UNKNOWN=0


Do NOT stage.


Do NOT commit.


Do NOT push.


======================================================================
40. PRESERVE EXCLUDED WIP
======================================================================

Continue excluding all unrelated paths identified by the prior commit-readiness
audits.


Do not absorb old:

- onboarding work;
- branding experiments;
- unrelated Fabric Knowledge;
- other module work;
- arbitrary README changes.


If the dirty set differs from the previously known exclusions:

report exact difference.


======================================================================
41. TEST STRATEGY
======================================================================

Run only affected suites plus the required final proof.


gm-expenses:
    full suite


Host:
    affected targeted tests
    real-DB expenses suite


Studio:
    full contracts
    ESLint


Responsive:
    1280
    768
    375
    320


Migration:
    V63 → V64 disposable rehearsal


Concurrency:
    real DB sequence race


Do NOT rerun unrelated PKG-2D/full platform matrices unless an actual shared
byte change invalidates their baseline.


======================================================================
42. DOCUMENTATION
======================================================================

Update canonical gm-expenses domain/persistence documentation.


Append to:

    Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md


Append-only.


Record the Owner supersession explicitly:


SUPERSEDED:

    caseNumber sequence scope =
    tenant + establishment + business date


CANONICAL:

    caseNumber sequence scope =
    tenant + business date


Also record:

    establishment participates only in the full business reference when
    available.


Record financial semantics:

    Total anticipos = actually delivered Advances
    Total gastos = APROBADO Expenses
    Rejected financial effect = zero
    real Return/Reimbursement are explicit money movements


Record visual hierarchy:

    Case Identity
    Assignment
    Finance


Store:

- this STEP prompt;
- evidence;
- V64 rehearsal proof;
- test results.


Refresh CURRENT_STEP using the canonical continuity mechanism.


======================================================================
43. STEP 18 / 19 / 20 / 20A / 21 RECORD CONSOLIDATION
======================================================================

Ensure the release evidence chain contains the accepted relevant records from:

    STEP 18
    STEP 19
    STEP 20
    STEP 20A
    STEP 21
    STEP 22


Do NOT rewrite history.


Do not duplicate evidence unnecessarily.


If STEP 18 deployment evidence still exists only in Restricted storage:

record that accurately.

Do not fabricate Fabric evidence from unavailable raw files.


======================================================================
44. NO COMMIT YET
======================================================================

Even if all tests pass:

    FILES_STAGED=0
    COMMITS_CREATED=0
    PUSH_PERFORMED=NO


The Owner must first visually approve:

1.
new Identity / Assignment / Finance hierarchy;

2.
ID Gasto on card;

3.
ID Gasto on detail;

4.
financial Card fixture;

5.
financial Detail fixture.


Then ONE controlled commit gate will consolidate the accumulated dirty paths.


======================================================================
45. REQUIRED FINAL REPORT
======================================================================

Return:


STEP=
GM_EXPENSES_FINAL_MVP_CLOSURE_22


STATUS=
READY_FOR_OWNER_FINAL_VISUAL_REVIEW
or
BLOCKED


--------------------------------------------------
DIRTY WORKTREE
--------------------------------------------------

GM_EXPENSES_DIRTY_PATHS=
GYSTIGO_DIRTY_PATHS=
FABRIC_DIRTY_PATHS=

ACCEPTED_DIRTY_PATHS=
UNRELATED_DIRTY_PATHS=
UNKNOWN_PATHS=


--------------------------------------------------
FINANCIAL MODEL
--------------------------------------------------

TOTAL_ADVANCES_RULE=
SUM_ACTUALLY_DELIVERED_ADVANCES

TOTAL_EXPENSES_RULE=
SUM_APROBADO

REJECTED_FINANCIAL_EFFECT=
ZERO

OWNER_FIXTURE_TOTAL_ADVANCES=
320

OWNER_FIXTURE_TOTAL_EXPENSES=
400

OWNER_FIXTURE_BASE_BALANCE=
80 POR_REEMBOLSAR

OWNER_FIXTURE_NET_RETURN=
0

OWNER_FIXTURE_REIMBURSED=
0

OWNER_FIXTURE_FINAL_PENDING=
80 POR_REEMBOLSAR

OWNER_FIXTURE_USED=
400

OWNER_FIXTURE_USAGE=
125%


--------------------------------------------------
CURRENT LIVE OWNER CASE
--------------------------------------------------

LIVE_OWNER_CASE_AUTOMATICALLY_MODIFIED=
NO

LIVE_STORED_RETURN_TOTAL=

LIVE_NET_RETURN_AFTER_NO_CORRECTION=

LIVE_CASE_REQUIRES_AUTHENTICATED_REVERSAL=
YES/NO


--------------------------------------------------
CARD / DETAIL CONSISTENCY
--------------------------------------------------

CARD_FINANCIAL_SUMMARY=

DETAIL_FINANCIAL_SUMMARY=

CARD_DETAIL_FINANCIAL_CONSISTENCY=
YES/NO

CARD_TOTAL_RETURNED=
DETAIL_TOTAL_RETURNED=

CARD_FINAL_PENDING=
DETAIL_FINAL_PENDING=


--------------------------------------------------
ID GASTO
--------------------------------------------------

ID_GASTO_IMPLEMENTED=
YES/NO

CASE_NUMBER_FORMAT=
YYYYMMDD####

SEQUENCE_SCOPE=
TENANT + BUSINESS_DATE

ESTABLISHMENT_REQUIRED_FOR_CASE_NUMBER=
NO

VISIBLE_CASE_NUMBER_EXAMPLE=
202609170001

API_CASE_NUMBER=
YES/NO

CARD_ID_GASTO_VISIBLE=
YES/NO

DETAIL_ID_GASTO_VISIBLE=
YES/NO

CARD_CASE_NUMBER=
DETAIL_CASE_NUMBER=

CARD_DETAIL_CASE_NUMBER_CONSISTENCY=
YES/NO

UUID_ROUTES_PRESERVED=
YES/NO


--------------------------------------------------
FULL BUSINESS REFERENCE
--------------------------------------------------

FULL_REFERENCE_DEPENDS_ON_ESTABLISHMENT=
YES

FULL_REFERENCE_REQUIRED_FOR_CASE_NUMBER=
NO

FULL_REFERENCE_EXAMPLE=
1191771814001-001-202609170001

RUC_USED_AS_TENANT_KEY=
NO

ESTABLISHMENT_FABRICATED=
NO

SRI_SEQUENCE_REUSED=
NO


--------------------------------------------------
BUSINESS DATE
--------------------------------------------------

BUSINESS_DATE_RULE=

DEFAULT_BUSINESS_ZONE_SOURCE=

HISTORICAL_BACKFILL_DATE_RULE=

FECHA_CASE_NUMBER_DATE_CONSISTENT=
YES/NO


--------------------------------------------------
V64
--------------------------------------------------

V64_CREATED=
YES/NO

BACKFILLED_CASES=

DUPLICATES=

V63_TO_V64_REHEARSAL=
PASS/FAIL

CONCURRENT_SEQUENCE_TEST=
PASS/FAIL

IMMUTABILITY_TEST=
PASS/FAIL

FINANCIAL_HISTORY_UNCHANGED_BY_V64=
YES/NO


--------------------------------------------------
UI HEADER
--------------------------------------------------

IDENTITY_SECTION=
YES/NO

ASSIGNMENT_SECTION=
YES/NO

FINANCE_SECTION=
YES/NO

IDENTITY_ASSIGNMENT_DIVIDER=
YES/NO

ASSIGNMENT_FINANCE_DIVIDER=
YES/NO

RESPONSIBLE_LAYOUT_PRESERVED=
YES/NO

SUPERVISOR_LAYOUT_PRESERVED=
YES/NO

RESOURCE_LAYOUT_PRESERVED=
YES/NO

CONCILIADO_POSITION_PRESERVED=
YES/NO

USAGE_POSITION_PRESERVED=
YES/NO


--------------------------------------------------
RESPONSIVE
--------------------------------------------------

RESPONSIVE_1280=
RESPONSIVE_768=
RESPONSIVE_375=
RESPONSIVE_320=


--------------------------------------------------
TESTS
--------------------------------------------------

GM_EXPENSES=
HOST_REAL_DB=
HOST_TARGETED=
STUDIO=
ESLINT=


--------------------------------------------------
RUNTIME
--------------------------------------------------

WORKING_TREE_API_SUPPORTS_CASE_NUMBER=
YES/NO

RUNNING_DEV_API_SUPPORTS_CASE_NUMBER=
YES/NO

SHARED_DEV_VERSION=
V63

SHARED_DEV_MODIFIED=
NO


--------------------------------------------------
SOURCE CONTROL
--------------------------------------------------

FILES_STAGED=
0

COMMITS_CREATED=
0

PUSH_PERFORMED=
NO

READY_FOR_CONTROLLED_COMMIT_GATE=
YES/NO


STOP_FOR_OWNER_REVIEW=
YES

# GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21
MODE=AUDIT_FIRST_THEN_IMPLEMENT_THEN_VERIFY
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ORIGIN=Owner business facts after the visual smoke of GM_EXPENSES_OWNER_SMOKE_CARD_ALIGNMENT_FIX_20A
ACCEPTED_BASELINE=gm-expenses 545eae0, Gystigo bcb9591, Fabric bbdd66a, Shared DEV V63
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16,GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — GM-EXPENSES FINAL OWNER SMOKE CORRECTION
FINANCIAL RECONCILIATION + ID GASTO

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21

MODE=
AUDIT_FIRST → IMPLEMENT → VERIFY

OWNER_AUTHORIZED=YES


============================================================
0. PURPOSE
============================================================

This is the final Owner-smoke correction before the gm-expenses MVP can be
frozen.

There are TWO required deliverables:

A. Correct the final ExpenseCase financial semantics/UI using the real Owner
   business facts.

B. Implement the persistent ExpenseCase business number shown as:

       ID Gasto: 202609170001

Do not defer either silently.

If B cannot be implemented safely because a real platform foundation is
missing, STOP with the exact missing foundation and the smallest required
follow-up STEP.

No commit.
No push.
No Shared DEV migration in this STEP.


============================================================
1. OWNER BUSINESS FACTS — AUTHORITATIVE
============================================================

Target Case:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0
    Compra Filtro

The Owner confirms the business reality is:

ADVANCES:

    USD 200.00   EN_RENDICION
    USD 100.00   EN_RENDICION
    USD  20.00   ENTREGADO

All three were actually delivered.

Therefore:

    TOTAL_ADVANCES = USD 320.00


EXPENSES:

    USD 200.00   APROBADO
    USD  80.00   APROBADO
    USD  90.00   APROBADO
    USD  30.00   APROBADO

    USD 200.00   RECHAZADO

Therefore:

    TOTAL_APPROVED_EXPENSES = USD 400.00

The rejected USD 200.00 has:

    FINANCIAL_EFFECT = ZERO


REAL CASH MOVEMENTS:

    RETURNED = USD 0.00
    REIMBURSED = USD 0.00

No real cash was returned by the responsible person.

No reimbursement has yet been paid by the company.


============================================================
2. CANONICAL ADVANCE RULE
============================================================

An Advance counts in Total anticipos when money was actually delivered.

Therefore:

    ENTREGADO        = included
    EN_RENDICION     = included
    RENDIDO          = included if it represents delivered funding
    CERRADO          = included historically as delivered funding

A state transition after delivery MUST NOT remove the Advance from the
original funding total.

Draft/cancelled Advance with no delivery:

    financial effect = zero

Do not confuse:

    Advance lifecycle state

with:

    whether money was actually delivered.


============================================================
3. CANONICAL EXPENSE RULE
============================================================

TOTAL_EXPENSES_FOR_RECONCILIATION =

    SUM(EXPENSES WHERE STATE = APROBADO)

Do NOT calculate:

    approved - rejected

because rejected Expenses are already excluded from the approved set.

Financial effect:

    REGISTRADO          = 0
    PENDIENTE_REVISION  = 0
    OBSERVADO           = 0
    RECHAZADO           = 0
    APROBADO            = full amount

A rejected Expense:

- remains visible in history;
- remains auditable;
- does not become an Advance;
- does not become a Return;
- does not become a Reimbursement;
- does not become an Adjustment;
- is not subtracted again.


============================================================
4. BASE RECONCILIATION
============================================================

Canonical formula:

    TOTAL_TO_RECONCILE =
        TOTAL_ADVANCES
        - TOTAL_APPROVED_EXPENSES

For this Owner Case:

    320 - 400 = -80

Therefore:

    AMOUNT = USD 80.00
    DIRECTION = POR_REEMBOLSAR

Normal UI should display positive money + direction:

    Total a conciliar
    USD 80.00
    Por reembolsar

Do not display:

    USD -80.00

unless an existing technical/internal API uses signed values.


============================================================
5. REAL RETURN / REIMBURSEMENT
============================================================

Return and Reimbursement are REAL cash movements only.

RETURN:

    responsible person actually gives money back to the company.

REIMBURSEMENT:

    company actually pays additional money to the responsible person.

They must only originate from explicit money-movement operations.

Expense rejection must NEVER create either movement.


============================================================
6. AUDIT ANY STORED RETURN FOR THIS CASE
============================================================

STEP 19 previously reported stored Return events totalling USD 300.

The Owner now confirms:

    NO REAL CASH RETURN OCCURRED.

Therefore, before changing anything, audit exactly why those stored movements
exist.

Determine:

- exact originating command;
- API operation;
- UI operation;
- event ids;
- whether they were generated manually, automatically or by previous legacy
  semantics;
- whether Expense rejection ever caused or contributed to them;
- whether current production code can reproduce the incorrect state.

Return:

    STORED_RETURN_TOTAL=
    OWNER_REAL_RETURN_TOTAL=0

Do NOT simply ignore stored history.

Do NOT delete immutable events.

If these events are legacy/incorrect business data:

design the audit-preserving correction using the existing reversal /
compensating-event model.

But do NOT automatically mutate the Owner Case in this implementation STEP.

Owner data correction will happen only after deployment through an
authenticated product operation or an explicitly authorized data-fix STEP.


============================================================
7. FINAL PENDING FORMULA
============================================================

Keep base reconciliation separate from real cash movements.

BASE:

    BASE_BALANCE =
        TOTAL_ADVANCES
        - TOTAL_APPROVED_EXPENSES

FINAL:

    FINAL_BALANCE =
        TOTAL_ADVANCES
        + TOTAL_REIMBURSED
        - TOTAL_APPROVED_EXPENSES
        - TOTAL_RETURNED
        - TOTAL_ADJUSTMENTS

When real movements are zero:

    TOTAL_ADVANCES = 320
    TOTAL_EXPENSES = 400
    RETURNED = 0
    REIMBURSED = 0
    ADJUSTMENTS = 0

Final:

    -80

Display:

    Pendiente
    USD 80.00
    Por reembolsar


============================================================
8. OWNER-EXPECTED FINANCIAL CARD
============================================================

Final desired semantic layout:

    Finanzas

    Total anticipos     Total gastos       Total a conciliar       Uso
    USD 320.00          USD 400.00         USD 80.00               125% │BAR│
                                            Por reembolsar

    Devuelto            Reembolsado        Pendiente
    USD 0.00            USD 0.00           USD 80.00
                                            Por reembolsar

    Usado
    USD 400.00


USO:

    operational metric

USADO:

    operational/statistical metric

Neither determines reconciliation.

Only APROBADO Expenses determine Total gastos.


============================================================
9. USAGE BAR
============================================================

Keep:

    Uso 125%
    [vertical bar]

as one visual unit.

Text may exceed 100%.

Visual fill:

    clamp to 100%.

Do not separate the percentage from its bar.

Do not allow another metric to occupy the Uso rail.


============================================================
10. HEADER — PRESERVE ACCEPTED DESIGN
============================================================

Do NOT distort:

    EXP. 01: Compra Filtro
    Fecha
    Responsable
    Supervisor
    Recurso asignado
    Abierto / Cerrado
    Conciliado
    Conciliado bar

Preserve STEP 15/20A accepted visual composition.


============================================================
11. ID GASTO — REQUIRED MVP FEATURE
============================================================

The ExpenseCase requires a persistent business number.

Normal UI:

    EXP. 01: Compra Filtro
    Fecha: 2026-09-17
    ID Gasto: 202609170001

Then:

    Responsable: ...
    Supervisor: ...
    Recurso asignado: ...

ID Gasto is NOT:

- the UUID;
- database bigint id;
- EXP. 01;
- UI list position.

It is a persistent immutable business number.


============================================================
12. IDENTIFIER LEVELS
============================================================

Preserve three different concepts.


A. TECHNICAL ID

    UUID

Example:

    437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0


B. VISIBLE EXPENSE CASE NUMBER

    YYYYMMDD####

Example:

    202609170001

Normal UI label:

    ID Gasto: 202609170001


C. FULL BUSINESS REFERENCE

For Ecuador:

    RUC-ESTABLISHMENT_NUMBER-CASE_NUMBER

Example:

    1191771814001-001-202609170001

This full reference is for:

- traceability;
- support;
- export;
- reports;
- integrations;
- audit.

It is NOT normally shown on the ExpenseCase card.


============================================================
13. TENANT RELATIONSHIP
============================================================

The real platform relationship remains:

    tenant_id

Do NOT use RUC as tenant_id.

RUC is tax/business identity.

Internally:

    ExpenseCase
        tenant_id
        establishment_id
        case_number

Tax/organization context provides:

    RUC
    establishment business number

Derived full reference:

    RUC
    + "-"
    + establishment_number
    + "-"
    + case_number


============================================================
14. DO NOT DUPLICATE MASTER DATA
============================================================

gm-expenses must NOT create:

- its own RUC master;
- its own Establishment master;
- its own Organization master.

Reuse canonical platform data.

No cross-module JDBC.

If Host composition is needed:

    use ports/services/adapters according to existing architecture.


============================================================
15. ESTABLISHMENT REQUIREMENT
============================================================

Before implementation, audit the real current architecture again.

STEP 20 found:

- ExpenseCase creation currently has no establishment reference;
- Shared DEV has no usable configured establishments;
- historical Cases cannot currently be resolved to establishments.

Do NOT invent:

    establishment = 001

Do NOT fabricate historical ownership.

Determine whether:

A.
the canonical Establishment model already exists and only needs wiring;

or

B.
a minimal Establishment foundation must be implemented first.

If A:

    implement the reuse/wiring in this STEP.

If B:

    STOP before inventing architecture and report the exact minimal
    prerequisite foundation.

Do NOT silently change the sequence scope to tenant-only without Owner
approval.


============================================================
16. BUSINESS NUMBER FORMAT
============================================================

Visible number:

    YYYYMMDD####

Example:

    202609170001

Where:

    YYYYMMDD = business date
    #### = daily sequence

Sequence scope:

    TENANT
    + ESTABLISHMENT
    + BUSINESS_DATE

Example:

Tenant A / Establishment 001:

    202609170001
    202609170002
    202609170003

Same Tenant / Establishment 002:

    202609170001

This is valid because full references differ:

    <RUC>-001-202609170001
    <RUC>-002-202609170001


============================================================
17. BUSINESS DATE
============================================================

The visible:

    Fecha

and the YYYYMMDD part of:

    ID Gasto

must use the SAME business date.

Do not allow:

    Fecha = 2026-09-17
    ID Gasto = 202609180001

Resolve a canonical business timezone.

For Ecuador the expected effective timezone is:

    America/Guayaquil

But do NOT hardcode Ecuador in gm-expenses domain logic.

Audit existing tenant / organization / country timezone capability.

If the platform genuinely lacks a safe timezone resolver:

    STOP and identify the exact missing foundation.

Do not silently use UTC if it contradicts business date semantics.


============================================================
18. V64
============================================================

Current migration head:

    V63

V64 is authorized ONLY if the required architecture is safely resolvable.

Expected V64 scope:

- ExpenseCase establishment reference;
- case_business_date;
- case_sequence;
- case_number;
- concurrency-safe sequence persistence;
- uniqueness constraints;
- immutability protection;
- deterministic legacy backfill where facts are resolvable.

Do NOT include unrelated schema changes.


============================================================
19. HISTORICAL CASES
============================================================

Existing Cases must not receive fabricated establishment values.

Classify:

    RESOLVABLE
    NOT_RESOLVABLE

For resolvable Cases:

    backfill canonical establishment context.

For unresolved Cases:

    do NOT invent 001.

Report exact count.

If visible case numbers can safely be backfilled without fabricating
establishment data, explain the model and prove uniqueness.

If doing that would violate the Owner-approved identifier semantics:

    STOP.


============================================================
20. SEQUENCE GENERATION
============================================================

Must be:

- server-side;
- transactional;
- concurrency-safe;
- persistent;
- scoped by tenant + establishment + business date.

Do not use:

- Java process-memory counter;
- Studio-generated counter;
- current list count;
- MAX()+1 without locking/concurrency protection.

Do NOT reuse SRI:

    document_sequences

because ExpenseCase is not a fiscal document.


============================================================
21. CASE NUMBER IMMUTABILITY
============================================================

Once assigned:

    case_number MUST NEVER CHANGE.

Business date MUST NEVER CHANGE merely because timezone/configuration changes
later.

Persist the resolved date at creation.

The full reference must remain historically stable.


============================================================
22. API
============================================================

Expose:

    caseNumber
    businessDate

Preserve:

    UUID-based routes.

Do not replace existing URLs.

Where appropriate Host may compose:

    fullBusinessReference

using canonical tax/establishment data.

gm-expenses must not query tax tables directly.


============================================================
23. UI
============================================================

Required card:

    EXP. 01: Compra Filtro
    Fecha: 2026-09-17
    ID Gasto: 202609170001

    Responsable:       Eduardo Burgasí
    Supervisor:        Sofia Salinas
    Recurso asignado:  Vehículo · ...

Do not display the full RUC-establishment-case reference in this card.

Preserve:

- spacing;
- label/value relationship;
- typography;
- Conciliado alignment;
- Finanzas layout;
- Uso rail.


============================================================
24. RESPONSIVE
============================================================

Verify:

    1280
    768
    375
    320

Require:

- no horizontal overflow;
- ID Gasto readable;
- no text deformation;
- header remains stable;
- Conciliado remains in header;
- Uso stays in Finanzas;
- finance totals retain semantic grouping.


============================================================
25. REQUIRED FINANCIAL TEST — OWNER CASE
============================================================

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

REAL RETURNS:

    0

REAL REIMBURSEMENTS:

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


============================================================
26. REQUIRED FINANCIAL INVARIANT TESTS
============================================================

Prove:

A.
Rejecting Expense creates no financial movement.

B.
Rejected Expense contributes zero.

C.
Observed Expense contributes zero.

D.
Pending Expense contributes zero.

E.
Approved Expense contributes exactly once.

F.
Delivered Advances sum exactly once.

G.
Advance EN_RENDICION remains part of delivered funding.

H.
Real Return only comes from explicit Return operation.

I.
Real Reimbursement only comes from explicit Reimbursement operation.

J.
No rejected Expense is converted into Advance/Return/Reimbursement/Adjustment.


============================================================
27. REQUIRED ID TESTS
============================================================

If architecture gate passes, prove:

A.

Tenant A
Establishment 001
2026-09-17

first Case:

    202609170001


B.

second Case:

    202609170002


C.

Establishment 002:

    202609170001


D.

Another tenant:

    202609170001


E.

Concurrent Case creations:
    no duplicates.


F.

Failed creation:
    no corrupt identifier state.


G.

Case number immutable.


H.

Fecha and ID Gasto date always match.


I.

Full EC reference:

    <RUC>-<establishment>-<caseNumber>


J.

RUC not used as tenant key.


K.

SRI sequence not reused.


============================================================
28. V64 REHEARSAL
============================================================

If V64 is created:

Do NOT apply it to Shared DEV yet.

Use a disposable V63 copy.

Verify:

- migration PASS;
- historical data preserved;
- deterministic backfill;
- zero fabricated establishments;
- uniqueness;
- immutability;
- concurrent sequence generation;
- financial rows unchanged.

Return:

    BACKFILLED_CASES
    UNRESOLVED_ESTABLISHMENTS
    DUPLICATES
    REHEARSAL_STATUS


============================================================
29. TEST SCOPE
============================================================

Run affected tests.

Expected minimum:

gm-expenses:
    full suite

Host:
    affected unit/API
    real-DB expenses suite

Studio:
    full contracts

Responsive:
    1280
    768
    375
    320

Migration:
    V63→V64 disposable rehearsal if V64 exists

Do not rerun unrelated platform matrices.


============================================================
30. DOCUMENTATION
============================================================

Update canonical gm-expenses documentation.

Append Owner rules to:

    Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md

Append-only.

Record explicitly:

FINANCE:

    Total anticipos = delivered Advances
    Total gastos = APROBADO Expenses
    Rejected financial effect = zero
    Reconciliation = advances - approved expenses

IDENTIFIER:

    technical id = UUID
    visible ID Gasto = YYYYMMDD####
    full business reference =
        RUC-establishment-caseNumber
    RUC != tenant_id
    establishment != establishment_id
    sequence scope =
        tenant + establishment + business date

Store STEP prompt/evidence.

Refresh CURRENT_STEP through canonical continuity mechanism.


============================================================
31. SAFETY
============================================================

DO NOT:

- mutate Shared DEV;
- repair Owner Case automatically;
- delete financial history;
- fabricate Return/Reimbursement;
- fabricate establishment;
- use RUC as tenant PK;
- duplicate master data;
- create cross-module JDBC;
- push;
- stage unrelated WIP.


============================================================
32. COMMIT POLICY
============================================================

This STEP is implementation + verification only.

No commit yet.

No push.

Stop for Owner visual/functional review.


============================================================
33. REQUIRED FINAL REPORT
============================================================

Return:

STEP=
GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21

STATUS=
READY_FOR_OWNER_FINAL_REVIEW
or
BLOCKED


FINANCIAL:

OWNER_CASE_FACTS=
ADVANCES=200+100+20
APPROVED_EXPENSES=200+80+90+30
REJECTED_EXPENSE=200
REAL_RETURN=0
REAL_REIMBURSEMENT=0

TOTAL_ADVANCES=
320

TOTAL_EXPENSES=
400

REJECTED_FINANCIAL_EFFECT=
0

TOTAL_TO_RECONCILE=
80

TOTAL_TO_RECONCILE_DIRECTION=
POR_REEMBOLSAR

RETURNED=
0

REIMBURSED=
0

FINAL_PENDING=
80

FINAL_PENDING_DIRECTION=
POR_REEMBOLSAR

USED=
400

USAGE=
125%

REJECTION_CREATES_FINANCIAL_MOVEMENT=
NO


STORED_RETURN_AUDIT:

STORED_RETURN_TOTAL=
OWNER_CONFIRMED_REAL_RETURN_TOTAL=
0

ROOT_CAUSE_IF_DIFFERENT=

OWNER_CASE_AUTOMATICALLY_MUTATED=
NO


BUSINESS_IDENTIFIER:

ID_GASTO_IMPLEMENTED=
YES/NO

VISIBLE_CASE_NUMBER=
202609170001

NORMAL_CARD_DISPLAY=
ID Gasto: 202609170001

TECHNICAL_ID=
UUID

SEQUENCE_SCOPE=
TENANT + ESTABLISHMENT + BUSINESS_DATE

FULL_BUSINESS_REFERENCE_EC=
RUC-ESTABLISHMENT-CASE_NUMBER

FULL_REFERENCE_EXAMPLE=
1191771814001-001-202609170001

RUC_USED_AS_TENANT_KEY=
NO

ESTABLISHMENT_MASTER_DUPLICATED=
NO

SRI_SEQUENCE_REUSED=
NO

BUSINESS_TIMEZONE_RULE=

V64_CREATED=
YES/NO

BACKFILLED_CASES=

UNRESOLVED_ESTABLISHMENTS=

V63_TO_V64_REHEARSAL=
PASS/NOT_RUN/BLOCKED

CONCURRENT_SEQUENCE_TEST=
PASS/NOT_RUN/BLOCKED


UI:

ID_GASTO_VISIBLE=
YES/NO

FINANCE_GRID=
ACCEPTED/NOT_ACCEPTED

CONCILIADO_PRESERVED=
YES/NO

USAGE_BAR_PRESERVED=
YES/NO

RESPONSIVE=
1280:
768:
375:
320:


TEST_RESULTS:

GM_EXPENSES=
HOST_REAL_DB=
HOST_TARGETED=
STUDIO=


ARCHITECTURE_BLOCKER=

IF_BLOCKED:

EXACT_FOUNDATION_MISSING=
MINIMUM_REQUIRED_STEP=
WHY_UNSAFE_TO_IMPLEMENT_NOW=


SHARED_DEV_VERSION=
V63

SHARED_DEV_MODIFIED=
NO

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

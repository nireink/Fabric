# GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15
MODE=READ_ONLY_VISUAL_AUDIT_THEN_TARGETED_STUDIO_FIX
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
ACCEPTS=GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14 (do not repeat it)
OWNER_DECISION=Conciliado starts approximately at the Responsable row in the Case header right rail; the status badge stays top-right; the left information block is preserved; Uso stays in Finanzas
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FINAL_12_BASELINE_REUSED=YES
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — FINAL EXPENSE CASE HEADER ALIGNMENT
AUDIT FIRST → IMPLEMENT ONLY IF REQUIRED

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15

MODE=
READ_ONLY_VISUAL_AUDIT_THEN_TARGETED_STUDIO_FIX

OWNER_AUTHORIZED=YES

============================================================
0. CONTINUITY / IMPORTANT
============================================================

The previous accepted work is:

    STEP 14
    GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14

DO NOT repeat STEP 14.

DO NOT re-audit or modify:

- audit_logs;
- expense audit/history architecture;
- OBSERVADO integrity;
- Windows environment variables;
- local runtime launcher;
- Docker configuration;
- V62;
- V63;
- gm-expenses backend;
- Case-level rendition;
- multiple Advances;
- FIFO removal;
- financial formulas;
- reports;
- migrations.

Those areas are already Owner-reviewed.

This STEP concerns ONLY:

    ExpenseCase card header/layout.

No backend change.
No financial change.
No audit change.
No environment change.
No launcher change.
No migration.
No Shared DEV write.
No commit.
No push.

============================================================
PHASE 1 — READ-ONLY VISUAL AUDIT
============================================================

1. VERIFY ACTUAL CURRENT FILES
============================================================

Before editing anything, inspect the current production Studio implementation:

- ExpenseCaseCard.jsx
- caseRules.js if relevant
- ExpenseCases.css
- related card fixture
- related contracts

Confirm current git diff for these files.

Do NOT modify yet.

============================================================
2. VERIFY CURRENT OWNER-ACCEPTED LEFT BLOCK
============================================================

The following desktop presentation is OWNER-ACCEPTED:

    Responsable:       Eduardo Burgasí
    Supervisor:        Eduardo Burgasí
    Recurso asignado:  Vehículo · PCH5159 — KIA - RIO R EX 1.4 4P 4X2 TM

Audit whether the current implementation preserves:

- label/value on same visual row;
- current label width;
- current value alignment;
- font sizes;
- font weights;
- line heights;
- vertical spacing;
- full resource text where normal desktop width permits it.

This block MUST NOT be modified merely to accommodate the right rail.

============================================================
3. VERIFY CURRENT RIGHT-SIDE POSITION
============================================================

Inspect the actual rendered Case header.

Determine whether:

    Conciliado

already begins approximately at the vertical height of:

    Responsable

Desired semantic structure:

    EXP. 01: Compra Telefono                         Cerrado
    Fecha: 2026-09-17

    Responsable:       Eduardo Burgasí               Conciliado
                                                     100%   │BAR│

    Supervisor:        Eduardo Burgasí

    Recurso asignado:  Vehículo · PCH5159 — KIA ...

    ---------------------------------------------------------

    Finanzas

If it already satisfies this requirement:

    DO NOT CHANGE CSS.

Proceed directly to verification and report:

    IMPLEMENTATION_REQUIRED=NO

If it does NOT:

    continue to PHASE 2.

============================================================
4. AUDIT LAYOUT MECHANISM
============================================================

Before implementing, identify whether the Case header currently uses:

- CSS Grid;
- Flexbox;
- absolute positioning;
- margins/padding;
- another layout mechanism.

Determine the smallest structural change needed.

Preferred model:

    Case header
    ├── left information region
    └── compact right rail

LEFT owns:

    title
    date
    Responsable
    Supervisor
    Recurso asignado

RIGHT owns:

    status badge
    Conciliado

IMPORTANT:

Do NOT place Conciliado into a width calculation that unnecessarily reduces
the left information region.

============================================================
PHASE 1 GATE
============================================================

Continue automatically to PHASE 2 ONLY if:

    CONCILIATED_ALIGNMENT_CORRECTION_REQUIRED=YES

If correcting it would require changing:

- left label widths;
- left typography;
- financial layout;
- backend data;
- global design-system behavior;

STOP and report instead.

Do not broaden scope.

============================================================
PHASE 2 — TARGETED IMPLEMENTATION
============================================================

5. EXACT OWNER CHANGE
============================================================

Move ONLY the Conciliado visual block slightly lower.

Target:

    Conciliado top position
    ≈ Responsable row vertical position

Do NOT move:

    Cerrado / Abierto badge.

The badge remains in its existing top-right location.

Only Conciliado moves.

============================================================
6. PRESERVE LEFT INFORMATION BLOCK
============================================================

ABSOLUTE PRIORITY:

Do NOT change:

    Responsable:
    Supervisor:
    Recurso asignado:

or their values.

Moving Conciliado must NOT cause:

- label/value pairs to split on desktop;
- names to wrap unnecessarily;
- label column to shrink;
- value column to shift;
- resource text to truncate prematurely;
- font size reduction;
- line-height compression;
- ellipsis introduced merely to create room;
- new text deformation.

If space is needed:

    adjust the RIGHT rail.

Do NOT sacrifice the LEFT information block.

============================================================
7. STRUCTURAL ALIGNMENT, NOT MAGIC SPACING
============================================================

Prefer structural CSS/Grid/Flex alignment.

Avoid a fragile solution such as:

    margin-top: 47px

if a grid row / right rail placement can express the intended layout.

Preferred conceptual desktop arrangement:

    LEFT                         RIGHT

    Title                        Status
    Date
    Responsable                  Conciliado + bar
    Supervisor
    Recurso asignado

Use the actual existing DOM/CSS structure and make the smallest safe change.

============================================================
8. CONCILIADO MUST REMAIN ABOVE DIVIDER
============================================================

Conciliado is a CASE-LIFECYCLE indicator.

It MUST stay:

    ABOVE the horizontal divider.

Do NOT move it into Finanzas.

Closed:

    Cerrado

    Conciliado
    100%
    [bar]

Open:

    Abierto

    Conciliado
    Pendiente
    [empty bar]

Do NOT invent intermediate percentages.

============================================================
9. USO REMAINS IN FINANZAS
============================================================

Uso is a FINANCIAL metric.

It remains:

    BELOW the divider
    inside Finanzas

Example:

    Finanzas

    Entregado       Usado        Justificado       Uso
    USD 300.00      USD 260.00   USD 260.00        87% │BAR│

    Devuelto        Reembolsado  Pendiente...

Do NOT move Uso.

Do NOT merge the Conciliado and Uso indicators.

============================================================
10. DUAL BAR SEMANTICS — FREEZE
============================================================

Preserve current accepted behavior:

Conciliado:
    CLOSED + financially resolved
        → 100%, full bar

    OPEN
        → Pendiente, empty bar

Uso:
    used / delivered

Examples:

    29%
    87%
    110%

For:

    Uso 110%

preserve:

    text = 110%
    visual fill = max 100%

No delivered Advance:

    Uso 0%
    empty usage bar

============================================================
11. RESOURCE TEXT PROTECTION
============================================================

On normal desktop widths preserve:

    Vehículo · PCH5159 — KIA - RIO R EX 1.4 4P 4X2 TM

whenever the existing width can display it.

Do NOT truncate it because Conciliado moved.

At narrower widths:

    natural semantic wrapping is allowed.

Do not break identifiers or words awkwardly.

============================================================
PHASE 3 — VERIFICATION
============================================================

12. DESKTOP VISUAL ACCEPTANCE
============================================================

At 1280px require:

    EXP. 01: Compra Telefono                         Cerrado
    Fecha: ...

    Responsable:       Eduardo Burgasí               Conciliado
                                                     100%  │BAR│

    Supervisor:        Eduardo Burgasí

    Recurso asignado:  Vehículo · PCH5159 — KIA - RIO R EX 1.4 4P 4X2 TM

    ---------------------------------------------------------

    Finanzas

The visual target is approximate vertical alignment with Responsable,
not pixel-perfect alignment at the expense of layout quality.

============================================================
13. RESPONSIVE
============================================================

Verify:

    1280px
    768px
    375px
    320px

At 1280:

- Responsable label/value same row;
- Supervisor label/value same row;
- Recurso retains accepted presentation;
- Conciliado aligns near Responsable.

At 768:

- preserve horizontal label/value structure where space permits;
- resource may wrap naturally only if necessary.

At 375 / 320:

responsive reflow is allowed.

But preserve:

- semantic pairing of labels and values;
- Conciliado in Case header;
- Uso in Finanzas;
- no overlap;
- no hidden indicators;
- no horizontal overflow.

============================================================
14. REQUIRED REGRESSION PROOFS
============================================================

Require:

RESPONSABLE_LAYOUT_PRESERVED=YES
SUPERVISOR_LAYOUT_PRESERVED=YES
RESOURCE_LAYOUT_PRESERVED=YES

CASE_STATUS_POSITION_UNCHANGED=YES

CONCILIATED_ALIGNED_NEAR_RESPONSIBLE=YES
CONCILIATED_ABOVE_DIVIDER=YES

USAGE_INSIDE_FINANCE=YES

DUAL_BARS_INDEPENDENT=YES

TEXT_DEFORMED=NO
NEW_TEXT_TRUNCATION=NO
INDICATOR_OVERLAP=NO
TEXT_OVERLAP=NO
HORIZONTAL_OVERFLOW=NO

============================================================
15. TEST SCOPE
============================================================

This STEP is Studio-only.

Reuse accepted evidence from:

    FINAL_12
    STEP 13
    STEP 14

Do NOT rerun:

- Host real-DB suite;
- gm-expenses module suite;
- V43→V63 migration rehearsal;
- audit tests;
- launcher tests.

Run only:

- targeted ExpenseCaseCard contracts;
- full Studio contracts if inexpensive;
- ESLint on changed Studio files;
- responsive card fixture at:
    1280
    768
    375
    320

============================================================
16. BEFORE / AFTER PROOF
============================================================

Return the actual changed files.

Report:

    FILES_CHANGED_BY_STEP15

and summarize the exact CSS/markup change.

Do not merely state that it was fixed.

Confirm whether the implementation used:

    grid
    flex
    row placement
    minimal spacing adjustment

and why.

============================================================
17. HARD SCOPE FREEZE
============================================================

BACKEND_CHANGED=NO
AUDIT_CHANGED=NO
ENVIRONMENT_CHANGED=NO
LAUNCHER_CHANGED=NO
FINANCIAL_MODEL_CHANGED=NO
MIGRATION_CREATED=NO

Shared DEV:

    DO NOT MODIFY

No stage.
No commit.
No push.

============================================================
18. REQUIRED FINAL REPORT
============================================================

Return exactly:

STEP=
GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15

STATUS=
READY_FOR_OWNER_FINAL_VISUAL_ACCEPTANCE

PHASE1_AUDIT_COMPLETED=YES

IMPLEMENTATION_REQUIRED=YES/NO

FILES_CHANGED_BY_STEP15=

DIFF_SUMMARY=

LAYOUT_MECHANISM_BEFORE=
LAYOUT_MECHANISM_AFTER=

RESPONSIBLE_LAYOUT_PRESERVED=YES
SUPERVISOR_LAYOUT_PRESERVED=YES
RESOURCE_LAYOUT_PRESERVED=YES

CASE_STATUS_POSITION_UNCHANGED=YES

CONCILIATED_POSITION=
ALIGNED_APPROXIMATELY_WITH_RESPONSIBLE

CONCILIATED_ABOVE_DIVIDER=YES

USAGE_INSIDE_FINANCE=YES

DUAL_BARS_INDEPENDENT=YES

TEXT_DEFORMED=NO
NEW_TEXT_TRUNCATION=NO

RESPONSIVE_RESULTS=
- 1280:
- 768:
- 375:
- 320:

STUDIO_TEST_RESULTS=
ESLINT_RESULT=

BACKEND_CHANGED=NO
AUDIT_CHANGED=NO
ENVIRONMENT_CHANGED=NO
LAUNCHER_CHANGED=NO
MIGRATION_CREATED=NO

FINAL_12_BASELINE_REUSED=YES

SHARED_DEV_VERSION=V43
SHARED_DEV_MODIFIED=NO

FILES_STAGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

READY_FOR_CONTROLLED_COMMIT_GATE=YES/NO

STOP_FOR_OWNER_REVIEW=YES

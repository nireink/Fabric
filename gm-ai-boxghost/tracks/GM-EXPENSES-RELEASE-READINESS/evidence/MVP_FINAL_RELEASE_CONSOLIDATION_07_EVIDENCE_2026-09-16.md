# GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07 — evidence

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07.md
DATE=2026-09-16 (local, UTC-5)
STATUS=READY_FOR_OWNER_FINAL_MVP_UI_REVIEW
COMMIT_STATUS=NONE
PUSH_STATUS=NONE
SHARED_DEV_STATUS=V43, not modified (read-only Flyway query only)
REPOSITORY_HEADS=Gystigo d9f3dde; Modules/gm-expenses ab74610; Fabric 70fd250 (all uncommitted work on top)
```

## Read model audit (§14)

The Case list and detail already return, per currency, `delivered`, `spent`, `justified`, `returned`,
`reimbursed`, `authorizedAdjustments`, `pendingReturn`, `pendingReimbursement` and `hasDeliveredAdvance`
(`ExpenseCaseController.format`, `financialSummary`). The detail's `renditionSummary` and every
rendition, and the report funding rows, carry the same movements. No read value was missing.

```text
CORRECTION_SCOPE=STUDIO_ONLY
BACKEND_FINANCIAL_RULES_CHANGED=NO
HOST_READ_MODEL_CHANGED=NO
MIGRATION_CREATED=NO
```

## The Owner's Case in the local runtime (read-only, 127.0.0.1:3310, V63)

`Viaje Loja` (expense_case 318, uuid 2075C587…, tenant 1, CERRADO at 2026-09-17T00:22:20Z) is a legacy
Case with several advances: 12 delivered advances, all CERRADO, and 5 CANCELADO; 6 APROBADO expenses
(200.00) and 1 RECHAZADO (20.00, outside Usado and Justificado); no authorized adjustment.

```text
Entregado 679.00 + Reembolsado 20.00 = Justificado 200.00 + Devuelto 499.00   -> Pendiente de conciliar USD 0.00
Usado 200.00, Uso 29%
```

Its history was not modified. In Shared DEV (V43) the same Case identity still holds 2 EN_RENDICION
advances and 10 BORRADOR drafts, recorded as legacy data in RUNTIME-REHEARSAL-03-2026-09-16.

## Studio changes

```text
cases/renditionRules.js      zero direction = Pendiente de conciliar; adjustmentRows; no-advance label
cases/caseRules.js           summarizeCaseBalance: Entregado, Usado, Justificado, Devuelto, Reembolsado,
                             Ajuste autorizado (only when > 0), direction; No aplica without delivered advance
cases/ExpenseCaseCard.jsx    Entregado · Usado · Justificado · Uso / Devuelto · Reembolsado · direction
cases/ExpenseCases.css       4-column grid, direction spans 2 columns; <=600px 2 columns, direction full row
cases/ExpenseCaseDetailPage.jsx  per-advance rendition shows Ajuste autorizado when one exists
reportRules.js               Pendiente de conciliar; Devuelto/Reembolsado in the period summary and the
                             related-Cases line; "Gastado (todo el expediente)" -> "Usado (todo el expediente)"
ExpenseReportsPage.jsx       Devuelto (CUR), Reembolsado (CUR), Ajuste autorizado (CUR) when one exists
fixtures/ExpenseCaseCardsFixture.jsx  RN-001-consistent financial helper; Viaje Loja and adjustment scenarios
contracts                    ExpenseCaseCard, ExpenseCases, AdvanceRenditionFlow, ExpenseReportHome,
                             ExpenseResourceAssignmentFlow
```

## Verification

```text
VERIFIED_BASELINE_CHECK
BASELINE_FOUND=YES (PKG-2D; no registered gm-expenses baseline yet)
BASELINE_ID=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
ACCEPTED_COMMITS_PRESENT=YES (gm-security d3fa0b4, Gystigo d9f3dde, Fabric cc194e4 are ancestors of HEAD)
RELEVANT_CONTRACT_DRIFT=NO (Studio expenses presentation only)
BASELINE_REUSE_DECISION=REUSE
REHEARSAL_03_REUSE=REUSE (Owner-accepted, uncommitted): 0 files under server/src, database or
                   Modules/gm-expenses/src newer than Host jar CC028B88…; runtime jar still CC028B88…,
                   gm-expenses jar still FDDAB6CF…
FULL_HISTORICAL_REGRESSION_RERUN=NO

Studio targeted contracts (5 suites)   111/111
Studio full contracts                  620/620 (53 files; 612 before + 8 new)
ESLint (7 changed shell files)         0 problems (contracts sit outside the shell ESLint config)
Card fixture 1024px                    20 cards, Viaje Loja 679/200/200/29%/499/20/Pendiente 0.00, no "Diferencia"
Card fixture 375px / 320px             no horizontal overflow, 0 clipped cells, 2 columns, amounts at 14px
Card fixture console (fresh tab)       0 errors
UIX fixture Case detail (legacy c8)    net Por reembolsar 20.00, per-advance own directions; after the reimbursement:
                                       Pendiente de conciliar USD 0.00 and Conciliar enabled
UIX fixture reports                    Devuelto / Reembolsado shown, no "Diferencia", no "Gastado"
UIX fixture 375px                      reports and Case detail without horizontal overflow
UIX fixture console                    6 known 401 from the harness /auth/me, no application error
Owner Studio 5173                      serves the updated modules
Local backend 127.0.0.1:8080           PID 48044, jar cc028b886c4d, unchanged
```

## Documentation and continuity

```text
Fabric domain baseline       RN-001 zero label, FIFO named, "Financial presentation vocabulary" section
Reglas.md                    +2 entries appended (gm-expenses rules; Shared DEV controlled migration and legacy data),
                             first 33,150 bytes unchanged
CURRENT_STEP.md              generated by Fabric/tools/continuity/Set-GypportCurrentStep.ps1 (GENERATE_ONLY)
BoxGhost                     evidence/RUNTIME-REHEARSAL-03-2026-09-16/ (14 byte-exact files + evidence document),
                             handoffs/SHARED_DEV_MIGRATION_V43_V63_PLAN_2026-09-16.md
```

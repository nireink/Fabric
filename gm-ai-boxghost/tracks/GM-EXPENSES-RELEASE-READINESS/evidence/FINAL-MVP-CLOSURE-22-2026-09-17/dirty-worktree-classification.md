# GM_EXPENSES_FINAL_MVP_CLOSURE_22 §39 - dirty worktree classification (2026-09-17)

Every uncommitted path in the three worktrees, with the STEP that produced it. Nothing is staged, nothing is
committed and nothing is pushed. PRE_EXISTING_WIP is work of other tracks that this STEP series never opened:
it is listed so that it is excluded deliberately, and it stays exactly as it was.

## Modules/gm-expenses - master at 545eae0 (18 paths)

| git | path | origin |
|---|---|---|
| _M | src/test/java/com/gypport/business/expenses/casefile/application/CaseRenditionServiceTest.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | src/main/java/com/gypport/business/expenses/casefile/application/CaseRenditionLedger.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | src/main/java/com/gypport/business/expenses/casefile/application/CaseRenditionService.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseCaseFinancialSummary.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | src/main/java/com/gypport/business/expenses/settlement/application/SettlementBalanceEventRepository.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | src/main/java/com/gypport/business/expenses/settlement/domain/AdvanceSettlement.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | src/main/java/com/gypport/business/expenses/settlement/domain/SettlementBalanceChange.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| ?? | src/main/java/com/gypport/business/expenses/settlement/domain/SettlementBalanceEvent.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | src/main/java/com/gypport/business/expenses/settlement/infrastructure/persistence/jdbc/JdbcSettlementBalanceEventRepository.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | src/test/java/com/gypport/business/expenses/settlement/domain/AdvanceSettlementTest.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| ?? | src/main/java/com/gypport/business/expenses/casefile/application/BusinessDatePort.java | STEP_22 - ID Gasto (business date, sequence, number) |
| ?? | src/main/java/com/gypport/business/expenses/casefile/application/CaseNumberSequencePort.java | STEP_22 - ID Gasto (business date, sequence, number) |
| _M | src/main/java/com/gypport/business/expenses/casefile/application/ExpenseCaseService.java | STEP_22 - ID Gasto (business date, sequence, number) |
| ?? | src/main/java/com/gypport/business/expenses/casefile/domain/CaseNumber.java | STEP_22 - ID Gasto (business date, sequence, number) |
| _M | src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseCase.java | STEP_22 - ID Gasto (business date, sequence, number) |
| ?? | src/main/java/com/gypport/business/expenses/casefile/infrastructure/persistence/jdbc/JdbcCaseNumberSequenceRepository.java | STEP_22 - ID Gasto (business date, sequence, number) |
| _M | src/main/java/com/gypport/business/expenses/casefile/infrastructure/persistence/jdbc/JdbcExpenseCaseRepository.java | STEP_22 - ID Gasto (business date, sequence, number) |
| ?? | src/test/java/com/gypport/business/expenses/casefile/domain/ | STEP_22 - ID Gasto (business date, sequence, number) |

## Gystigo - feature/gm-fleets-minimum-vehicle-master-01 at bcb9591 (25 paths)

| git | path | origin |
|---|---|---|
| ?? | platform_os/studio/channel/browser/shell/fixtures/HeaderBrandingFixture.jsx | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (branding fixture, 2026-08-30) |
| ?? | platform_os/studio/channel/browser/shell/fixtures/header-branding.html | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (branding fixture, 2026-08-30) |
| _D | README.md | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (deleted in the working tree before this track; last commit 54bdacd, 2026-07-28) |
| _M | platform_os/studio/channel/browser/shell/src/application/AuthPage.css | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (onboarding, modified 2026-08-29) |
| _M | platform_os/studio/channel/browser/shell/src/application/onboarding/ShortRegisterPage.jsx | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (onboarding, modified 2026-08-29) |
| _M | platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseCaseController.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensesResponseFormatting.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseCaseHttpApiTest.java | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/studio/channel/browser/shell/fixtures/ExpenseCaseCardsFixture.jsx | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseCard.jsx | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseDetailPage.jsx | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCases.css | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/studio/verification/contracts/browser/AdvanceRenditionFlow.contract.mjs | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/studio/verification/contracts/browser/ExpenseCaseCard.contract.mjs | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail + STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/cases/caseRules.js | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/cases/renditionRules.js | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/expenseService.js | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | platform_os/studio/verification/contracts/browser/ExpenseCases.contract.mjs | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| _M | platform_os/studio/verification/contracts/browser/ExpenseOperationIdBoundary.contract.mjs | STEP_20/20A/21 - financial semantics, movement UX, reverso, card and detail |
| ?? | database/modules/gm-expenses/migration/V64__gm_expenses_case_business_number.sql | STEP_22 - ID Gasto (business date, sequence, number) |
| ?? | platform_os/server/src/main/java/com/gypport/server/module/expenses/TenantBusinessDateResolver.java | STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/server/src/main/java/com/gypport/server/shared/config/ExpenseCaseConfig.java | STEP_22 - ID Gasto (business date, sequence, number) |
| _M | platform_os/server/src/main/resources/application.yaml | STEP_22 - ID Gasto (business date, sequence, number) |
| ?? | platform_os/studio/channel/browser/shell/fixtures/ExpenseCaseDetailFixture.jsx | STEP_22 - ID Gasto (business date, sequence, number) |
| ?? | platform_os/studio/channel/browser/shell/fixtures/expense-case-detail.html | STEP_22 - ID Gasto (business date, sequence, number) |

## Fabric - main at bbdd66a (22 paths)

| git | path | origin |
|---|---|---|
| ?? | Knowledge/Derived/ | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-08-07) |
| ?? | Knowledge/gm-accounting/ | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-08-13) |
| ?? | Knowledge/gm-expenses/04-integration/ | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-08-26) |
| ?? | Knowledge/gm-expenses/05-implementation/ | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-08-27) |
| ?? | Knowledge/gm-expenses/03-application/ | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-08-28) |
| ?? | Knowledge/gm-expenses/README.md | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-08-28) |
| ?? | Knowledge/AI/ | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-09-08) |
| ?? | Knowledge/Security/ | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-09-08) |
| ?? | Knowledge/Architecture/GYPPORT_REGLAS_CANONICAS_ARQUITECTURA_DOMINIO_UIX.md | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-09-10) |
| ?? | Knowledge/UIX/ | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (knowledge WIP, 2026-09-10) |
| _M | Knowledge/00-GYPPORT-UNIVERSE/Reglas.md | STEP_19/20/21/22 - Fabric canonical records and evidence |
| _M | Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md | STEP_19/20/21/22 - Fabric canonical records and evidence |
| ?? | Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_FINAL_MVP_CLOSURE_22.md | STEP_19/20/21/22 - Fabric canonical records and evidence |
| ?? | Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21.md | STEP_19/20/21/22 - Fabric canonical records and evidence |
| ?? | Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20.md | STEP_19/20/21/22 - Fabric canonical records and evidence |
| ?? | Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_OWNER_SMOKE_FINDINGS_19.md | STEP_19/20/21/22 - Fabric canonical records and evidence |
| _M | Knowledge/gm-expenses/01-domain/GYPPORT_GM_EXPENSES_DOMAIN_BASELINE_v1.0.md | STEP_19/20/21/22 - Fabric canonical records and evidence |
| _M | Knowledge/gm-expenses/02-persistence/GYPPORT_GM_EXPENSES_PERSISTENCE_BASELINE_v1.0.md | STEP_19/20/21/22 - Fabric canonical records and evidence |
| ?? | gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/FINAL-MVP-CLOSURE-22-2026-09-17/ | STEP_19/20/21/22 - Fabric canonical records and evidence |
| ?? | gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/OWNER-SMOKE-FINAL-CORRECTION-21-2026-09-17/ | STEP_19/20/21/22 - Fabric canonical records and evidence |
| ?? | gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/OWNER-SMOKE-FINAL-FIX-20-2026-09-17/ | STEP_19/20/21/22 - Fabric canonical records and evidence |
| ?? | gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/OWNER-SMOKE-FINDINGS-19-2026-09-17/ | STEP_19/20/21/22 - Fabric canonical records and evidence |

## Totals

```text
PRE_EXISTING_WIP=15
STEP_19_20_21_22=12
STEP_20_20A_21=24
STEP_22=14
TOTAL_DIRTY_PATHS=65
UNKNOWN=0
FILES_STAGED=0
COMMITS_CREATED=0
PUSH_PERFORMED=NO
```

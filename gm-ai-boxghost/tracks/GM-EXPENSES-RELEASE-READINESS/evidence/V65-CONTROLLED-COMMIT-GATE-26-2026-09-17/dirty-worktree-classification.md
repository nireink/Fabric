# GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26 - dirty worktree classification (2026-09-17)

Every uncommitted path in the three worktrees, with the STEP that produced it. Nothing is staged, nothing is
committed and nothing is pushed. PRE_EXISTING_WIP is work of other tracks that this STEP series never opened:
it is listed so that it is excluded deliberately, and it stays exactly as it was.

## Modules/gm-expenses - master at 874a3e5 (9 paths)

| git | path | origin |
|---|---|---|
| _M | src/main/java/com/gypport/business/expenses/casefile/application/ExpenseCaseService.java | STEP_25 - permanent expediente sequence (V65) |
| ?? | src/main/java/com/gypport/business/expenses/casefile/application/ExpenseSequencePort.java | STEP_25 - permanent expediente sequence (V65) |
| _M | src/main/java/com/gypport/business/expenses/casefile/domain/CaseNumber.java | STEP_25 - permanent expediente sequence (V65) |
| _M | src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseCase.java | STEP_25 - permanent expediente sequence (V65) |
| ?? | src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseSequence.java | STEP_25 - permanent expediente sequence (V65) |
| _M | src/main/java/com/gypport/business/expenses/casefile/infrastructure/persistence/jdbc/JdbcExpenseCaseRepository.java | STEP_25 - permanent expediente sequence (V65) |
| ?? | src/main/java/com/gypport/business/expenses/casefile/infrastructure/persistence/jdbc/JdbcExpenseSequenceRepository.java | STEP_25 - permanent expediente sequence (V65) |
| _M | src/test/java/com/gypport/business/expenses/casefile/application/CaseRenditionServiceTest.java | STEP_25 - permanent expediente sequence (V65) |
| ?? | src/test/java/com/gypport/business/expenses/casefile/domain/ExpenseSequenceTest.java | STEP_25 - permanent expediente sequence (V65) |

## Gystigo - feature/gm-fleets-minimum-vehicle-master-01 at 0293ff4 (17 paths)

| git | path | origin |
|---|---|---|
| ?? | platform_os/studio/channel/browser/shell/fixtures/HeaderBrandingFixture.jsx | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (branding fixture, 2026-08-30) |
| ?? | platform_os/studio/channel/browser/shell/fixtures/header-branding.html | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (branding fixture, 2026-08-30) |
| _D | README.md | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (deleted in the working tree before this track; last commit 54bdacd, 2026-07-28) |
| _M | platform_os/studio/channel/browser/shell/src/application/AuthPage.css | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (onboarding, modified 2026-08-29) |
| _M | platform_os/studio/channel/browser/shell/src/application/onboarding/ShortRegisterPage.jsx | PRE_EXISTING_WIP - other tracks, untouched by this STEP series (onboarding, modified 2026-08-29) |
| _M | platform_os/studio/channel/browser/shell/fixtures/ExpenseCaseCardsFixture.jsx | STEP_25 - permanent expediente sequence (V65) + STEP_25A - EXP display from expenseSequence on card and detail |
| _M | platform_os/studio/channel/browser/shell/fixtures/ExpenseCaseDetailFixture.jsx | STEP_25 - permanent expediente sequence (V65) + STEP_25A - EXP display from expenseSequence on card and detail |
| _M | platform_os/studio/verification/contracts/browser/AdvanceRenditionFlow.contract.mjs | STEP_25 - permanent expediente sequence (V65) + STEP_25A - EXP display from expenseSequence on card and detail |
| _M | platform_os/studio/verification/contracts/browser/ExpenseCaseCard.contract.mjs | STEP_25 - permanent expediente sequence (V65) + STEP_25A - EXP display from expenseSequence on card and detail |
| ?? | database/modules/gm-expenses/migration/V65__gm_expenses_case_permanent_sequence.sql | STEP_25 - permanent expediente sequence (V65) |
| _M | platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseCaseController.java | STEP_25 - permanent expediente sequence (V65) |
| _M | platform_os/server/src/main/java/com/gypport/server/shared/config/ExpenseCaseConfig.java | STEP_25 - permanent expediente sequence (V65) |
| _M | platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseCaseHttpApiTest.java | STEP_25 - permanent expediente sequence (V65) |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseCard.jsx | STEP_25 - permanent expediente sequence (V65) |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/cases/caseRules.js | STEP_25 - permanent expediente sequence (V65) |
| _M | platform_os/studio/verification/contracts/browser/ExpenseCaseListNumbering.contract.mjs | STEP_25 - permanent expediente sequence (V65) |
| _M | platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseDetailPage.jsx | STEP_25A - EXP display from expenseSequence on card and detail |

## Fabric - main at 018ea84 (20 paths)

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
| _M | Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md | STEP_24 - Shared DEV V64 deployment evidence (uncommitted, awaiting Owner authorization) + STEP_25 - permanent expediente sequence (V65) |
| ?? | Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24.md | STEP_24 - Shared DEV V64 deployment evidence (uncommitted, awaiting Owner authorization) |
| ?? | gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/SHARED-DEV-V64-DEPLOYMENT-24-2026-09-17/ | STEP_24 - Shared DEV V64 deployment evidence (uncommitted, awaiting Owner authorization) |
| _M | Knowledge/00-GYPPORT-UNIVERSE/Reglas.md | STEP_25 - permanent expediente sequence (V65) |
| ?? | Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25.md | STEP_25 - permanent expediente sequence (V65) |
| _M | Knowledge/gm-expenses/01-domain/GYPPORT_GM_EXPENSES_DOMAIN_BASELINE_v1.0.md | STEP_25 - permanent expediente sequence (V65) |
| _M | Knowledge/gm-expenses/02-persistence/GYPPORT_GM_EXPENSES_PERSISTENCE_BASELINE_v1.0.md | STEP_25 - permanent expediente sequence (V65) |
| ?? | gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/PERMANENT-EXPEDIENTE-SEQUENCE-V65-25-2026-09-17/ | STEP_25 - permanent expediente sequence (V65) |
| ?? | Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A.md | STEP_25A - EXP display from expenseSequence on card and detail |
| ?? | gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/V65-EXP-DISPLAY-CORRECTION-25A-2026-09-17/ | STEP_25A - EXP display from expenseSequence on card and detail |

## Totals

```text
PRE_EXISTING_WIP=15
STEP_24=3
STEP_25=25
STEP_25A=3
TOTAL_DIRTY_PATHS=46
UNKNOWN=0
FILES_STAGED=0
COMMITS_CREATED=0
PUSH_PERFORMED=NO
```

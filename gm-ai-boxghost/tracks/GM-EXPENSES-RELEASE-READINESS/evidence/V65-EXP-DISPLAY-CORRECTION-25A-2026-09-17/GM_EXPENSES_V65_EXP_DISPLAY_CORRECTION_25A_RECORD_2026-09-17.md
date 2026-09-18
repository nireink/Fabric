# GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A
MODE=TARGETED_FIX_AND_VERIFY
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A.md
STATUS=READY_FOR_OWNER_REVIEW
BACKEND_CHANGED=NO  V65_CHANGED=NO  FILES_STAGED=0  COMMITS_CREATED=0  PUSH_PERFORMED=NO  DEPLOYMENT_PERFORMED=NO
```

## 1. Why the Owner's screen showed "VIAJE QUITO" without EXP

```text
STUDIO_ON_5173=the current working tree, whose card reads EXP only from expenseSequence (STEP 25)
BACKEND_ON_8080=gystigo-backend:4.1.0-java25-gm-expenses-v64-0293ff4 - V64, which sends no expenseSequence
RESULT=the card could not show an EXP without inventing one from the daily sequence, which STEP 25 §23 forbids
```

That is the transitional state §4 of this STEP allows: the real screen shows EXP once V65 is deployed. What this STEP
corrects is everything that does carry V65: the card and the detail must always show `EXP. NN:` once expenseSequence
exists, and the acceptance fixtures must prove it with the Owner's exact numbers.

## 2. What changed

```text
ExpenseCaseDetailPage.jsx   the heading is caseTitle(detail): "EXP. 02: Compra Filtro", the same title as the card
ExpenseCaseCardsFixture.jsx the Owner's acceptance pair with their exact numbers, every other Case numbered around them
                            - Fixture A: VIAJE QUITO, expenseSequence 1, 2026-09-17, caseSequence 2, 202609170002
                            - Fixture B: Compra Filtro, expenseSequence 2, 2026-09-17, caseSequence 1, 202609170001
ExpenseCaseDetailFixture    Compra Filtro carries expenseSequence 2 (Fixture B)
ExpenseCaseCard.contract    25A EXP_DISPLAY (1, 2, 9, 10, 99, 100), 25A ACCEPTANCE_FIXTURES, 25A EXP_SOURCE
AdvanceRenditionFlow        the detail's heading is "EXP. 01: Viaje Loja", the card's heading
```

No backend, domain, schema, allocation, financial or Finance-layout byte changed.

## 3. Proof

```text
EXP_SEQUENCE_1_DISPLAY=EXP. 01   EXP_SEQUENCE_2_DISPLAY=EXP. 02   EXP_SEQUENCE_9_DISPLAY=EXP. 09
EXP_SEQUENCE_10_DISPLAY=EXP. 10  EXP_SEQUENCE_99_DISPLAY=EXP. 99  EXP_SEQUENCE_100_DISPLAY=EXP. 100
SORTING_DOES_NOT_RENUMBER_EXP=PASS           FILTERING_DOES_NOT_RENUMBER_EXP=PASS
BUSINESS_DATE_CHANGE_DOES_NOT_RENUMBER_EXP=PASS
CASE_SEQUENCE_DOES_NOT_CONTROL_EXP=PASS      CASE_NUMBER_DOES_NOT_CONTROL_EXP=PASS
CARD_EXPENSE_SEQUENCE == DETAIL_EXPENSE_SEQUENCE == API_EXPENSE_SEQUENCE (AdvanceRenditionFlow §32)
STUDIO=652/652 in 53 files   ESLINT=PASS
```

In the browser, on the acceptance fixtures:

```text
CARD    EXP. 01: VIAJE QUITO | Fecha: 2026-09-17 | ID: 202609170002 | Cerrado | Conciliado 100% | 200 / 200, Uso 100%
CARD    EXP. 02: Compra Filtro | Fecha: 2026-09-17 | ID: 202609170001 | Abierto | 320 / 400, 80 Por reembolsar, Uso 125%
CARDS   every title carries "EXP. NN:" with at least two digits; the others run 31 .. 03 in creation order
DETAIL  EXP. 02: Compra Filtro | Fecha: 2026-09-17 | ID: 202609170001
WIDTHS  1280 / 768 / 375 / 320 - no horizontal overflow on either surface; the title wraps naturally at 320
```

## 4. What the real screen will read after V65 is deployed

The fixtures carry the Owner's illustrative numbers. The real tenant is numbered by real creation order (STEP 25
rehearsal on today's Shared DEV copy): Compra Filtro becomes EXP. 08 and VIAJE QUITO EXP. 09, with their IDs
202609170001 and 202609170002 unchanged.

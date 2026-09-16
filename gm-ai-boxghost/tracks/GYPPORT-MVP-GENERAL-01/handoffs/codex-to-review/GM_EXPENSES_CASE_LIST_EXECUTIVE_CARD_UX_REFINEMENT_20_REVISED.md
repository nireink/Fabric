# Expense Case list executive cards — STEP 20 revised

Date: 2026-09-13. Track: GYPPORT-MVP-GENERAL-01.

The list cards now show the Case name/status, UTC creation date, responsible,
supervisor, all active assignment labels and currency-separated finances. The
native title link covers the card and retains keyboard navigation and visible
focus. Changes are confined to Studio presentation and verification.

## Read model audit before implementation

Gystigo checkout: `D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo`.
Branch: `feature/gm-fleets-minimum-vehicle-master-01`.
Initial HEAD: `dc14e0d539d17a9f72159e5ca7640d733b1b765b`.
The initial Documents/ChatGPT/gm-expenses repository has no commits or product
source. The module checkout is `Modules/gm-expenses`, clean on `master` at
`ab74610094dcdbdbb93564fc7b9fe05b51c7b8c2`; it was inspected only.

`expenseService.listCases` consumes `GET /api/expense-cases`. The controller's
list method uses the same `format(service.detail(...))` representation as detail.
This audit is source-backed; no authenticated live list response was obtained.

| Requested display datum | Current list representation |
| --- | --- |
| CASE_NAME | `name`; no business-facing Case sequence/code exists |
| CASE_DATE | `createdAt`; no separate Case business date |
| CASE_STATUS | `status`, ABIERTO/CERRADO |
| RESPONSIBLE_DISPLAY_NAME | `responsibleName`, required by ExpenseCase |
| REVIEWER_DISPLAY_NAME | `reviewerName`, nullable |
| CASE_RESOURCE_TYPE | `resources[].resourceType` |
| CASE_RESOURCE_DISPLAY_LABEL | `resources[].displaySnapshot` |
| ALLOCATION_TYPE | No Case-level allocation dimension is exposed/enabled |
| ALLOCATION_DISPLAY_LABEL | No Case-level allocation dimension is exposed/enabled |
| VEHICLE_PLATE | Included in resource displaySnapshot, not a separate list field |
| VEHICLE_BRAND | Included in resource displaySnapshot, not a separate list field |
| VEHICLE_MODEL | Included when available in resource displaySnapshot, not a separate list field |
| FINANCIAL_SUMMARY | `financialSummary[]`: delivered, spent, balance, excess, returned, reimbursed, authorizedAdjustments, hasDeliveredAdvance, hasClosedSettlement |

CURRENT_CASE_CARD_READ_MODEL=Name/status/createdAt/resolved people/resource snapshots/canonical financial summary.
ASSIGNMENT_INFORMATION_AVAILABLE=resources[].displaySnapshot for all active resources.
BACKEND_CHANGE_REQUIRED=NO.
READ_MODEL_GAP=NONE for currently enabled Case contexts.

Sources: `ExpenseCaseController.java` list/format, `FleetExpenseCaseResourceResolver.java`,
`ExpenseCase.java`, `ExpenseCaseResource.java`, `ExpenseCaseService.java`, and the
existing `caseRules.js` summary adapter. The Universe baseline, Expense Case
foundation/participants handoffs, MVP freeze and current UIX guide were reviewed.

The Host resolver currently enables VEHICLE only, producing plate plus
`FleetVehicleLabel.brandAndModel`. Department, Cost Center and Project examples
are not implemented Case contexts. Per-Expense allocation is a separate concept;
the no-verifier allocation adapter fails closed. No other module was expanded.

The Case resource model permits multiple active resources. Presentation joins
every active displaySnapshot with ` · `, preserving order and labels without a
vehicle preference or type filter. No resource means `Asignado a: Ninguno`.
Historical snapshots are preserved without fetching or fabricating newer labels.

## Presentation decisions

- Keep `name`; no `EXP. xx` sequence is manufactured and no technical ID is visible.
- CASE_DATE_SOURCE=createdAt. Display its UTC calendar date, YYYY-MM-DD, using the
  existing Instant string; never an Expense date or a new business date.
- Responsible remains required. Optional supervisor uses `Sin asignar`.
- Reuse `summarizeCaseBalance` unchanged. It selects authoritative delivered/spent/
  balance/excess values and drives `Sin anticipo` / `No aplica` through the backend
  `hasDeliveredAdvance` flag. Amount grouping/formatting is card-local.
- Only the requested presentation ratio is calculated: spent / delivered * 100,
  rounded to an integer. It is uncapped; no delivered money produces `—`.
- One native link per card, expanded with a CSS pseudo-element. Tab/Enter work;
  focus outlines the full card. No nested interactive controls, synthetic click
  handler, role substitution or route change.
- Scoped CSS uses the existing Card component and navy/cyan/surface tokens.
  Detail, forms, Rapid Capture, Reports, shared summary rules and shell are untouched.

## Verification and limits

Directed contracts: 41 PASS in 2 files, including 13 new card tests. Coverage
includes full vehicle labels, multiple resources, no assignment, optional reviewer,
name/date/status, canonical finance values, no Advance, 0%, 100%, 117%, zero
delivery, currency separation and native detail navigation. Department coverage
was intentionally not fabricated for an unavailable context.

Final Studio suite: 522 PASS in 47 files. Initial sandbox execution could not
write Vite's cache; the same authorized command passed with execution permission.
An initial full-suite attempt overlapped the design-system build, which regenerated
its package entry and caused one import failure. The sequential full run after
the build passed. No product/configuration repair was made for these execution issues.

Production build: PASS, including design-system build/type generation. The final
build includes the final title/focus CSS. Vite reports its existing >500 kB chunk
size advisory; no code-splitting scope was added. Targeted ESLint: PASS for both
production JSX files and the fixture. Exact-path whitespace review: PASS.

Browser verification used the actual ExpenseCaseListPage/ExpenseCaseCard with
the current shell CSS in a dedicated fixture, with simulated response values and
no backend calls. It is not evidence of real DEV records or a live detail response.
The fixture is outside the production entry and adds no product route.

| Viewport | Document client/scroll width | Card width | Card heights | Overflow |
| --- | --- | --- | --- | --- |
| 1440x900 | 1425 / 1425 | 568.5 | 280 | None |
| 1366x768 | 1351 / 1351 | 531.5 | 280 | None |
| 390x844 | 375 / 375 | 351 | 315.89–374.39 | None |

Measurements above were captured after viewport transitions settled. The long
vehicle label wraps naturally; at 390 its label is 317px wide / 39px high and
the two-resource label is 58.5px high. No label is truncated. Header/status share
a desktop row and stack on mobile; finances retain alignment and show 117%.

Keyboard: Tab reaches the next native link, with a 2px navy outline around its
card; Enter resolves `/expenses/cases/fixture-general`. Clicking the card body
resolves the same route. Every card has exactly one interactive element.
Computed contrast: context text #667085 on white 4.97:1; navy title 15.89:1.
The temporary viewport override was reset.

LIVE_DEV_DATA_ACCEPTANCE=NOT_VERIFIED_SESSION_REQUIRED. Local Studio at
`http://localhost:5173/expenses` redirects to login. An authenticated session was
requested; none was available during verification. No accounts or financial
records were created. The prompt requires live data verification where possible;
fixture validation is complete and Owner manual retest remains explicitly pending.
The locally started Vite preview is left available for that retest; backend and
database were not started/restarted or modified.

Evidence outside the repository:
`C:/Users/elbur/.codex/visualizations/2026/09/13/01a09aba-39bd-7ab3-a407-bc06d863cfe3/`

- `case-cards-fixture-1440.png`
- `case-cards-fixture-1366.png`
- `case-cards-fixture-390.png`
- `case-cards-keyboard-focus-390.png`
- `case-cards-responsive-evidence.json`

## Controlled local commit

The seven-file allowlist is this report, ExpenseCaseCard.jsx, ExpenseCaseListPage.jsx,
ExpenseCases.css, ExpenseCaseCard.contract.mjs, ExpenseCaseCardsFixture.jsx and
expense-case-cards.html. Sixteen preexisting WIP files were recorded by SHA-256
and checked separately. The initial index was empty. No WIP path is staged.
LOCAL_COMMIT=the single commit containing this report, with subject
`feat(expenses): refine case list cards`; the final response records its hash.

## Completion fields

PASS below means verified by source/contracts and/or the browser fixture described
above. It does not assert authenticated live DEV acceptance.

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=GM_EXPENSES_CASE_LIST_EXECUTIVE_CARD_UX_REFINEMENT_20_REVISED
STATUS=COMPLETED
CASE_CARD_TITLE=PASS
CASE_CARD_STATUS=PASS
CASE_CARD_DATE=PASS
CASE_DATE_SOURCE=createdAt
CASE_CARD_RESPONSIBLE=PASS
CASE_CARD_SUPERVISOR=PASS
CASE_CONTEXT_LABEL=Asignado a
VEHICLE_ASSIGNMENT_DISPLAY=PASS
NON_VEHICLE_ASSIGNMENT_DISPLAY=NOT_AVAILABLE_IN_CURRENT_READ_MODEL
NO_ASSIGNMENT_DISPLAY=PASS
NO_ASSIGNMENT_LABEL=Ninguno
CASE_CARD_FINANCIAL_SUMMARY=PASS
CASE_CARD_NO_ADVANCE=PASS
CASE_CARD_USAGE_INDICATOR=PASS
CASE_CARD_OVER_100=PASS
CASE_CARD_NAVIGATION=PASS
LONG_ASSIGNMENT_WRAP=PASS
RESPONSIVE_1440=PASS
RESPONSIVE_1366=PASS
RESPONSIVE_390=PASS
READ_MODEL_GAP=NONE
STUDIO_TESTS=522_PASS_47_FILES
STUDIO_BUILD=PASS
LIVE_DEV_DATA_ACCEPTANCE=NOT_VERIFIED_SESSION_REQUIRED
BACKEND_CHANGED=NO
DATABASE_CHANGED=NO
MIGRATIONS=NONE
FILES_CHANGED=7_EXACT_PATHS_LISTED_ABOVE
PREEXISTING_WIP_PRESERVED=YES
PUSH=NO
VPS=NO
NEXT_EXACT_ACTION=OWNER_MANUAL_RETEST
```

STOP. No push. No VPS.

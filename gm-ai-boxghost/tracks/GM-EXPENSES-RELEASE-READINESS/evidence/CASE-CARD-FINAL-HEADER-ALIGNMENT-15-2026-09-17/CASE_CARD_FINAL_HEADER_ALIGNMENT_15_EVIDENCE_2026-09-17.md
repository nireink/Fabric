# GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15 — evidence (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15
MODE=READ_ONLY_VISUAL_AUDIT_THEN_TARGETED_STUDIO_FIX
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15.md
EXECUTED_BY=Claude (Opus 5) in the Claude desktop app, on the Owner's instruction
STATUS=READY_FOR_OWNER_FINAL_VISUAL_ACCEPTANCE
```

Studio-only. No backend, audit, environment, launcher, financial or migration change. Shared DEV was not touched (V43). Nothing was staged, committed or pushed. Repository heads are unchanged.

## Phase 1 — read-only audit (before any edit)

- **Files (STEP 14 end state, SHA-256):** `ExpenseCaseCard.jsx` 9e733820…, `caseRules.js` c2158cab…, `ExpenseCases.css` bbb9b747…, `fixtures/ExpenseCaseCardsFixture.jsx` 9d6f2ca2…, `ExpenseCaseCard.contract.mjs` 3af6a825…, `ExpenseCases.contract.mjs` 3f7e2d81….
  - `git diff --stat` against HEAD d9f3dde covers these 6 files (+531 / −126). All of it is earlier uncommitted STEPs.
- **Layout mechanism before:**
  - `.expense-case-card__header` is a CSS Grid: columns `minmax(0, 1fr) auto`, areas "title lifecycle" "date lifecycle" "context lifecycle".
  - The right rail `.expense-case-card__lifecycle` spans all three rows as a nested grid (auto rows, `align-content: start`, `gap: 10px`), so Conciliado was placed at status height + 10px, independent of the left rows.
  - ≤600px: areas "title lifecycle" "date lifecycle" "context context".
- **Fixture measurements before** (card-relative px; fixture `gypport-expense-case-cards-fixture`, 20 cards):

| Width | Status | Title / date | Conciliado top | Responsable / Supervisor / Recurso rows | Label column / value x / value width | Conciliado − Responsable | Divider |
|---|---|---|---|---|---|---|---|
| 1280 | x=909 y=17 63×24 | y=17 / y=41.4 | y=51 | 69.4 / 90.9 / 112.4 (one line each, labels and values on the same row) | 103.8 / 134.8 / 717.2 | −18.4 (all 20 cards −18) | 143.9 |
| 768 | x=613 y=17 | y=17 / y=41.4 | y=51 | 69.4 / 90.9 / 112.4 (the SINOTRUK resource wraps to 2 lines) | 103.8 / 134.8 / 421.2 | −18.4 (range −41…−18 with wrapped titles) | 143.9 (163.4 SINOTRUK) |
| 375 | x=271 y=15 | y=15 / y=57 | y=49 | 104 / 125.5 / 147 (KIA 2 lines, SINOTRUK 3) | 103.8 / 130.8 / 203.2 | −55 | 198 / 217.5 / 178.5 |
| 320 | x=216 y=15 | y=15 (2 lines) / y=67.5 | y=49 | 104 / 125.5 / 147 (KIA 3 lines, SINOTRUK 4) | 103.8 / 130.8 / 148.2 | −55 | 217.5 / 237 / 178.5 |

- **Left block typography:** labels 13px / 400 / 19.5px; values 13px / 500 / 19.5px. At 1280 the KIA resource "Vehículo · PCH5159 — KIA - RIO R EX 1.4 4P 4X2 TM" and even the SINOTRUK label show in full on one line.
- **Other checks:** no overlaps, Conciliado above the divider, 0 overflow at every width.
- **Gate:** `CONCILIATED_ALIGNMENT_CORRECTION_REQUIRED=YES` (Conciliado started beside the date line, 18.4px above Responsable). The fix needed no change to label widths, typography, Finanzas, backend data or the design system, so Phase 2 continued.

## Phase 2 — the change (CSS only, row placement)

`Gystigo/platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCases.css` (now 3b506477…):

```css
/* desktop and tablet */
.expense-case-card__lifecycle { grid-area: lifecycle; display: grid; grid-template-rows: subgrid; justify-items: end; margin-bottom: 12px; }
.expense-case-card__lifecycle > .expense-case-card__status { grid-row: 1 / 3; align-self: start; }
.expense-case-card__conciliation { grid-row: 3; align-self: start; min-width: 6.5rem; margin: 0; }
/* @media (max-width: 600px): the context takes the whole width, so the rail keeps its stacked rows */
.expense-case-card__lifecycle { grid-template-rows: none; align-content: start; gap: 10px; }
.expense-case-card__lifecycle > .expense-case-card__status, .expense-case-card__conciliation { grid-row: auto; }
```

- **Replaced:** the rail's `align-content: start; gap: 10px` (moved into the narrow query); `.expense-case-card__conciliation { min-width: 6.5rem; margin: 0; }` gained the row placement.
- **Mechanism after:** the same header grid. The rail is now a CSS subgrid of the header's three rows. The status spans the title and date rows, keeping its top-right place without growing row 1. Conciliado is placed in the context row, whose first line is Responsable.
- **Why:** it is pure row placement, with no margin or offset, and no markup, width or typography change. The right column is still `auto` (the same 104px rail), so the left region is not narrowed.
- **Narrow screens:** they keep the previous stacked rail exactly, because an aligned rail there would squeeze the full-width label/value pairs.
- **Fallback:** without subgrid support the rail falls back to its own rows (status, then Conciliado).
- **Contract:** `ExpenseCaseCard.contract.mjs` (now e3260c2f…) gained `CONCILIADO_ON_RESPONSABLE_ROW`. It pins the subgrid rail, the status in rows 1–2, Conciliado in row 3 with no margin, padding or position offset, the untouched left-block rules (label column, 13px, 1.5 line height, no clipping) and the narrow stacked rail.
- **Unchanged:** `ExpenseCaseCard.jsx`, `caseRules.js`, the fixture and `ExpenseCases.contract.mjs` (same hashes).

## Phase 3 — verification after

| Width | Status | Title / date | Conciliado top | Rows | Label column / value x / value width | Conciliado − Responsable | Divider | Overflow / overlap |
|---|---|---|---|---|---|---|---|---|
| 1280 | x=909 y=17 63×24 (unchanged) | 17 / 41.4 (unchanged) | 69.4 | 69.4 / 90.9 / 112.4, one line each (unchanged) | 103.8 / 134.8 / 717.2 (unchanged) | 0 (all 20 cards) | 143.9 (unchanged) | 0 / none |
| 768 | x=613 y=17 (unchanged) | unchanged | 69.4 | unchanged (SINOTRUK 2 lines as before) | 103.8 / 134.8 / 421.2 (unchanged) | 0 (all cards) | unchanged | 0 / none |
| 375 | unchanged | unchanged | 49 (unchanged) | unchanged | unchanged | −55 (unchanged; stacked reflow) | unchanged | 0 / none |
| 320 | unchanged | unchanged | 49 (unchanged) | unchanged | unchanged | −55 (unchanged; stacked reflow) | unchanged | 0 / none |

- **Every width:** Conciliado sits in the header above the divider (20/20), Uso sits inside Finanzas (21/21 currency rows), no text or indicator overlaps, no horizontal overflow, and `CSS.supports('grid-template-rows', 'subgrid')` is true.
- **Screenshot at 800px (desktop layout; seen during the STEP, not stored):**
  - Compra repuestos shows Abierto at the top right and Conciliado Pendiente (empty bar) on the Responsable row. The KIA resource is complete on one line, and Uso 87% with its bar is in Finanzas.
  - Compra Teléfono shows Cerrado with Conciliado 100% (full bar) on the Responsable row.
- **Tests:** targeted contracts 63/63; full Studio suite 631/631; ESLint on `ExpenseCaseCard.jsx`, `caseRules.js` and the fixture: exit 0. The changed CSS and contract files are outside the shell ESLint configuration.
- **Reused, not rerun:** Host real-DB, gm-expenses module, the V43→V63 rehearsal, audit and launcher tests (FINAL_12, STEP 13 and STEP 14 evidence).

## Documentation

- **gm-expenses domain baseline §5:** Conciliado sits in the header's right rail, level with the Responsable row on desktop and tablet, without narrowing the left block.
- **Reglas.md:** unchanged. The STEP 14 placement rule already covers the semantics, and this is a visual alignment within it.

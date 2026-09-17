# GM_EXPENSES_OWNER_SMOKE_CARD_ALIGNMENT_FIX_20A — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_SMOKE_CARD_ALIGNMENT_FIX_20A
MODE=AUDIT_FIRST_THEN_TARGETED_FIX
STATUS=READY_FOR_OWNER_VISUAL_REVIEW
SCOPE=Case card composition and the Total a conciliar value. No domain, API, migration or Shared DEV change.
SHARED_DEV_MODIFIED=NO  FILES_STAGED=0  COMMITS_CREATED=0  PUSH_PERFORMED=NO
```

## 1. Root cause of "Total a conciliar USD 0.00 · Balanceado"

Neither a wrong Studio binding nor a wrong Host mapping: the Owner's browser reads the **deployed** backend, which
predates STEP 20 and does not send the field at all.

```text
BASE_BALANCE_BACKEND_VALUE=80.00 Por reembolsar (working tree: CaseRenditionLedger.baseBalance -> baseToReimburse)
BASE_BALANCE_API_VALUE=ABSENT on the running API; 80.00 on the working-tree API
BASE_BALANCE_STUDIO_VALUE=0.00 "Balanceado" (the absent pair was read as zero)
```

Evidence, read-only:

- The container `gypport-backend-dev` runs `gystigo-backend:4.1.0-java25-gm-expenses-mvp-bcb9591` (image id
  sha256:9e3ff62f…, built 2026-09-17T16:20Z by STEP 18), whose labels carry gm-expenses 545eae0 and Gystigo bcb9591.
- Its `/app/app.jar` was copied out and inspected: `ExpenseCaseController.class` contains `financialSummary` and
  `pendingReturn` but **not** `baseToReturn`, `baseToReimburse`, `movements` or `movement-reversals`; the nested
  `gm-expenses` jar's `ExpenseCaseFinancialSummary.class` has neither base field.
- The STEP 20 work is uncommitted, so no built image can contain it. The Studio dev server serves the new UI against
  that older API.
- The working-tree API is proven correct by the STEP 20 Host test, which asserts
  `$.financialSummary[0].baseToReimburse.amount = 80` for exactly this Case and passed (104/104).

## 2. Fix (smallest correct layer: Studio presentation)

`baseReconciliationRow` now prefers the backend's pair and, when a backend does not state it, applies the canonical
subtraction over the two totals it did send (Total anticipos − Total gastos). It is the canonical formula, not a second
opinion: whenever the backend states the pair, its values win. The domain equation, the API mapping and RN-001 are
untouched.

## 3. Card composition restored (§4–§6)

```text
Row 1  Total anticipos | Total gastos | Total a conciliar (+ direction caption) | Uso + its bar (far-right rail)
Row 2  Devuelto | Reembolsado | position (Por justificar o devolver / Por reembolsar / Pendiente de conciliar)
Row 3  Usado (operational metric, below the totals, never a column of the reconciliation)
```

The Uso bar is inside the Uso cell, so it can no longer appear between two amounts. The header (EXP. NN, Fecha,
Responsable, Supervisor, Recurso asignado, Abierto/Cerrado, Conciliado and its bar) was not touched. The Case detail's
Resumen financiero follows the same order, with Usado last.

## 4. Measured rendering — the Owner's own Case (fixture: 320 delivered, 400 approved, 300 returned)

```text
Total anticipos   USD 320.00      Total gastos   USD 400.00
Total a conciliar USD 80.00 · Por reembolsar     Uso 125% (bar fill clamped to 100%)
Devuelto          USD 300.00      Reembolsado    USD 0.00      Por reembolsar USD 380.00
Usado             USD 400.00
```

Base and position stay different values and neither is collapsed into the other. After the Owner reverses the false
return both read 80.

```text
RESPONSIVE (Case card fixture, own Vite dev server on 5189)
1280: 4 columns, rows at y=385 / 456 / 509, Uso in the right rail with its meter, 0 px overflow
768 : 4 columns, same grouping, 0 px overflow
375 : wraps to 2 columns, Uso stays paired with its bar, direction caption visible, 0 px overflow
320 : wraps to 2 columns, no overlap between any two cells, every value present, 0 px overflow
```

## 5. Verification

```text
STUDIO_CONTRACTS=639/639 PASS (636 before; +3: the §10 numeric contract, the absent-pair card case and the same case in caseRules)
STUDIO_LINT=PASS
GM_EXPENSES / HOST=not rerun: no backend file changed in this STEP (STEP 20 left them at 763/763 and 104/104)
MIGRATION_HEAD=V63 (untouched)
```

## 6. Consequence for the Owner's environment

The card is now correct against both backends. Everything else STEP 20 added to the API — the movements list and the
reverso endpoint — still needs a backend built from the STEP 20 code, which is a separate, Owner-authorized deployment.

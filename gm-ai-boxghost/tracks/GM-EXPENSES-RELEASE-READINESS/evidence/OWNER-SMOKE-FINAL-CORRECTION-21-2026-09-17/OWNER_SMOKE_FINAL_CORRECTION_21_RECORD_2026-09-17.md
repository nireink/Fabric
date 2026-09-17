# GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21 — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21
MODE=AUDIT_FIRST -> IMPLEMENT -> VERIFY
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21.md
STATUS=READY_FOR_OWNER_FINAL_REVIEW (A, financial) + BLOCKED (B, ID Gasto: no fiscal identity exists to reuse)
SHARED_DEV_MODIFIED=NO   OWNER_CASE_MODIFIED=NO   V64_CREATED=NO   MIGRATION_HEAD=V63
FILES_STAGED=0  COMMITS_CREATED=0  PUSH_PERFORMED=NO
```

## 1. Stored return audit (§6) — read-only

```text
STORED_RETURN_TOTAL=USD 300.00  (events 29 = 200.00 and 30 = 100.00, both RETURN_REGISTERED, reverses = NULL)
OWNER_CONFIRMED_REAL_RETURN_TOTAL=USD 0.00
ORIGINATING_COMMAND=expense_command_receipt 2817 CaseRenditionReturn, actor 1, 2026-09-17T16:40:29.559Z
API=POST /api/expense-cases/{id}/rendition/returns   UI=Registrar devolución (Case detail)
REASON_TEXT="100" on both events
FIRST_REJECTION_OF_THE_CASE=2026-09-17T16:41:55.882Z, 86 seconds AFTER the return
REJECTION_COULD_HAVE_CAUSED_IT=NO
```

Why a rejection cannot have contributed: `RejectExpenseReviewUseCase` only changes the expense and appends a review
event — it touches no settlement, advance or balance event. Exactly five places in production write
`settlement_balance_event`, and every one is an explicit money-movement command: the two legacy per-advance use cases
(guarded for Cases), the Case return, the Case reimbursement and the Case reverso. The return also predates every
rejection in this Case, so the sequence itself rules it out.

Reproducible today only through an explicit return command — and STEP 20 removed the two conditions that made the
mistake easy (the full-balance pre-fill and the optional motive), while adding an explicit confirmation.

The events are left exactly as recorded. The Owner corrects them after deployment through the reverso, so the real actor
and instant are recorded.

## 2. Financial semantics (A) — verified against the Owner's facts

```text
TOTAL_ADVANCES=320.00   (200 EN_RENDICION + 100 EN_RENDICION + 20 ENTREGADO, all delivered)
TOTAL_EXPENSES=400.00   (200 + 80 + 90 + 30 APROBADO)
REJECTED_FINANCIAL_EFFECT=0  (the 200 RECHAZADO)
TOTAL_TO_RECONCILE=80.00 POR_REEMBOLSAR      RETURNED=0  REIMBURSED=0
FINAL_PENDING=80.00 POR_REEMBOLSAR           USED=400.00  USAGE=125%
```

Advance rule confirmed in code and by test: the ledger counts an advance once its delivery exists and skips only
BORRADOR/CANCELADO or a missing delivery, so EN_RENDICION, RENDIDO and CERRADO all remain part of the funding.

Card composition (§8), measured in the fixture: row 1 Total anticipos · Total gastos · Total a conciliar · Uso with its
bar; row 2 Devuelto · Reembolsado · Pendiente; row 3 Usado. Pendiente now reads like Total a conciliar — the amount with
its direction as the caption — so the two comparable values sit in the same column.

## 3. ID Gasto (B) — BLOCKED, and this time the reason is sharper

The canonical model exists (`sri_establishments`, re-parented to `tax_subjects` by V48), so the question was whether it
only needs wiring. It does not: **there is no fiscal identity anywhere to wire to.**

```text
sri_establishments=0   tax_subjects=0   emission_points=0   user_establishments=0   organization_tax_profiles=0
mdm_party_identifiers of type RUC=0      organizations=4     branches=0
expense_case rows=29 across 7 tenants, 1 with an organization
tenants=15, with time_zone=0, with country_code=0, tenant_settings rows=0, countries catalog has no time zone
```

There is not a single RUC recorded in the platform, so neither component of `RUC-ESTABLISHMENT-CASE_NUMBER` has real
data to reuse, and no Case can be resolved to an establishment. Creating either would fabricate the Owner's tax identity
and the Cases' fiscal ownership, which §14, §15 and §19 forbid. Sequence scope was not silently changed to tenant-only
(§15), so V64 was not created.

## 4. Verification

```text
GM_EXPENSES=767/767 PASS (763 before; +4: the Owner Case, rejection through the review, delivered funding after a state
  change, and movements only from their own commands)
HOST_REAL_DB=104/104 PASS (run 1341d0fc, disposable core_business_expenses_test at Flyway 63)
STUDIO=640/640 contracts PASS (639 before; +1: the Owner facts card)
STUDIO_LINT=PASS
RESPONSIVE=1280 and 768 measured at real viewports: 4 columns, 0 px overflow, Uso in its rail.
  375 and 320 measured with the card in a container of that width, because the preview pane would not emulate below
  ~372 px and kept a 216 px sidebar that squeezed every card equally: 2 columns, 0 px overflow, no overlap, all eight
  values readable, Conciliado in the header, Uso in Finanzas.
```

## 5. Addendum §15A-§15E, §19B, §24A, §28A

**Both surfaces (§15A, §15E).** The Case card and the Expediente detail read the same backend
`ExpenseCaseFinancialSummary`, so they cannot diverge by construction. A contract now proves it by rendering both with
the Owner's acceptance fixture and comparing term by term: Total anticipos 320.00, Total gastos 400.00, Total a
conciliar 80.00 Por reembolsar, Devuelto 0.00, Reembolsado 0.00, Pendiente 80.00 Por reembolsar, Usado 400.00 (Uso 125%
is the card's own indicator, asserted in the card contract). The fixture includes the 200 RECHAZADO expense, which moves
none of those numbers.

**No UI-only correction (§15B).** Nothing in Studio subtracts, hides or recomputes a stored movement: both surfaces
print what the backend reports. The path from 300/380 to 0/80 is the reverso and nothing else. The STEP 20 Host test
proves the historical result end to end on a real database: RETURN_REGISTERED 200 + RETURN_REVERSED 200 and
RETURN_REGISTERED 100 + RETURN_REVERSED 100, four events kept, net returned 0.00, pendingReimbursement 80.00, with the
registered events untouched (`reverses_balance_event_id` still NULL on them).

**Detail actions (§15D).** With the corrected data the detail shows "Faltan USD 80.00 por reembolsar." and offers
Registrar reembolso, never Registrar devolución; the contract asserts the message and both button states, and that
neither USD 380.00 nor USD 300.00 appears.

**Data safety (§15C).** The real Case was not touched: it still holds exactly its 2 original events. The correction runs
through the authenticated product workflow after deployment, or through a separately authorized data-correction STEP.

**Header grouping (§19B).** The card header now separates identity (EXP. NN and Fecha, where ID Gasto will sit) from
assignment (Responsable, Supervisor, Recurso asignado) with the same hairline Finanzas already uses. The room comes from
the identity row itself, so the header grid moves both columns together: Conciliado keeps its subgrid row and stays
level with Responsable (measured: both at the same y at 1280 and 768), and the accepted STEP 15 contract - which forbids
nudging the rail with margin, padding or positioning - still passes.

**Owner acceptance fixture (§24A).** Rendered and measured on the card; asserted on both surfaces by contract.
`ID Gasto` is absent because it is blocked (§28A below), so `Fecha: 2026-09-17` is the only identity line today.

```text
CARD_TOTAL_RETURNED=0        DETAIL_TOTAL_RETURNED=0
CARD_PENDING=80              DETAIL_PENDING=80
CARD_ID_GASTO_VISIBLE=NO     DETAIL_ID_GASTO_VISIBLE=NO   (blocked: no fiscal identity exists)
WORKING_TREE_FIX_VERIFIED=YES
SHARED_DEV_STILL_OLD_DATA_OR_RUNTIME=YES (the deployed image predates STEP 20 and the Case still holds the 300)
READY_FOR_CONTROLLED_COMMIT_GATE=NO, by §28A, only because ID Gasto is not visible
RESPONSIVE=1280: 0 px overflow, Conciliado level | 768: 0 px, Conciliado level | 375: 0 px, no overlap, divider spans
  the card | 320: 0 px, no overlap, divider spans the card
STUDIO=641/641 contracts PASS   STUDIO_LINT=PASS
```

## 6. Not done

No migration, no Shared DEV change, no data repair, no commit, no push, no fabricated establishment, no RUC as a tenant
key, no duplicated master data, no cross-module JDBC, no reuse of the SRI document sequences.

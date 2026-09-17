# GM_EXPENSES_OWNER_SMOKE_FINDINGS_19 — audit evidence (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_SMOKE_FINDINGS_19
MODE=AUDIT_FIRST_THEN_PROPOSE_FIX
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_OWNER_SMOKE_FINDINGS_19.md
STATUS=AUDIT_COMPLETE_WAITING_OWNER_DECISION
TARGET_CASE=437a92bf-bd12-4ab4-9d0d-13dcd6f1fae0 (tenant 1, "Compra Filtro", ABIERTO)
SHARED_DEV=V63, read only (SET SESSION TRANSACTION READ ONLY + START TRANSACTION READ ONLY ... ROLLBACK)
CODE_READ=gm-expenses 545eae0, Gystigo bcb9591 (the deployed commits)
SOURCE_FILES_CHANGED=0 DATABASE_ROWS_CHANGED=0 FILES_STAGED=0 COMMITS_CREATED=0 PUSH_PERFORMED=NO
```

Raw query output is in `case-audit-result.txt` (person names and usernames removed) and `business-id-simulation.txt`;
the queries are in `case-audit.sql`. Actor account 1 is the Owner's own DEV account. Times are UTC (MySQL runs in UTC).

## 1. Financial chronology of the Case

| UTC | Command (expense_command_receipt) | Effect |
|---|---|---|
| 16:37:30.991 | 2803 CreateExpenseCase | Case 330 created; its first advance 106 (USD 200, OTRO, no delivery plan) created with it |
| 16:37:46.605 | 2804 CreateCaseAdvance | advance 107, USD 100, COMPRA, plan TRANSFERENCIA / 7 days |
| 16:37:50.090 | 2805 DeliverCaseAdvance | advance 107 delivered (TRANSFERENCIA) |
| 16:37:58.696 | 2806 DeliverCaseAdvance | advance 106 delivered (TRANSFERENCIA): delivered total USD 300 |
| 16:38:29.969–.973 | 2807–2814 RegisterExpense + RegisterCaseExpense ×4 | expenses 545 (200), 546 (30), 547 (90), 548 (80), all REGISTRADO |
| 16:40:29.559 | 2815, 2816 OpenSettlement + **2817 CaseRenditionReturn** | rendition rows 61 (advance 106) and 62 (advance 107) opened; **RETURN_REGISTERED 200.00 (event 29, row 61) + 100.00 (event 30, row 62) = USD 300**, reason text "100", actor account 1. No expense was APROBADO yet (justified 0), so the Case's pending return was exactly 300 |
| 16:40:31.714 | 2818 CaseRenditionReconcile | rows 61 and 62 RECONCILED / CONCILIADO (Case balance 300 + 0 − 0 − 300 = 0) while the 4 expenses were still REGISTRADO |
| 16:40:46–16:41:37 | 2819–2826 Submit / Accept; Observe → Correct → Accept | 548 (80) APROBADO; 547 (90) OBSERVADO (FALTA_COMPROBANTE) → corrected (revision 39) → APROBADO; 546 (30) APROBADO |
| 16:41:43–16:41:55 | 2827–2828 Submit / Reject | 545 (200) RECHAZADO (INFORMACION_INCONSISTENTE) |
| 16:42:27–16:42:38 | 2829–2832 Register / Submit / Accept | new expense 549 (200) APROBADO |
| 16:44:17.668–16:44:19.549 | 2833 CreateCaseAdvance + 2834 DeliverCaseAdvance | advance 108, USD 20, ENTREGA, EFECTIVO, ENTREGADO (no rendition row yet) |

No reimbursement, settlement adjustment, expense adjustment or reversal exists for the Case.

## 2. Totals and the canonical equation

```text
TOTAL_DELIVERED   = 200 + 100 + 20 = 320.00       (advances 106, 107, 108: delivery present, not BORRADOR/CANCELADO)
TOTAL_USED        = 30 + 90 + 80 + 200 = 400.00   (not RECHAZADO/EXCLUIDO; 545 RECHAZADO excluded)
TOTAL_JUSTIFIED   = 400.00                        (APROBADO, counted once the Case has a delivered advance)
TOTAL_RETURNED    = 300.00                        (row 61 200 + row 62 100; events 29 and 30)
TOTAL_REIMBURSED  = 0.00
TOTAL_ADJUSTMENTS = 0.00
BALANCE = 320 + 0 − 400 − 300 − 0 = −380  →  Por reembolsar USD 380.00 (the Owner's screen)
Without the USD 300 return: 320 − 400 = −80 → Por reembolsar USD 80.00
```

Code: `SettlementBalance.of` computes `advance + reimbursed − justified − returned − adjustments`; `CaseRenditionLedger`
feeds it the Case's delivered advances, APROBADO expenses and the rows' returned, reimbursed and adjustment totals.
`ARITHMETIC_FORMULA_CORRECT=YES`, `FINANCIAL_INPUTS_CORRECTLY_AGGREGATED=YES`, `CALCULATION_BUG=NO`.

## 3. Origin of "Devuelto USD 300.00"

- One Case command, receipt 2817 `CaseRenditionReturn` (POST /api/expense-cases/{reference}/rendition/returns →
  `CaseRenditionService.registerReturn`), at 2026-09-17T16:40:29.559Z by account 1. It is stored as two immutable
  `settlement_balance_event` rows: 29 (RETURN_REGISTERED 200.00, row 61) and 30 (RETURN_REGISTERED 100.00, row 62).
- `registerReturn` accepts any amount up to the Case's pending return at that moment (300). It opens a row for every
  delivered advance, then carries the amount on the open rows holding the most money first (`heldAmount` descending).
  REGISTRADO, PENDIENTE_REVISION and OBSERVADO expenses play no part in that check.
- Studio (`ExpenseCaseDetailPage.jsx`, `RenditionMovementForm`) pre-fills "Monto" with the full pending amount
  (`pendingMovement` gave 300.00). "Motivo (opcional)" is free text, and submitting records the movement with no
  confirmation or warning; `window.confirm` exists only for Cerrar expediente. The stored reason is "100".
- INFERENCE (the data cannot prove it): the Owner typed 100 into "Motivo" while the pre-filled Monto of 300.00 was
  submitted, or registered the return before the expenses were reviewed. Only the Owner can say whether any cash was
  returned.

## 4. Return reversal capability

| Layer | State |
|---|---|
| Schema (V11) | Supported. Event types RETURN_REVERSED / REIMBURSEMENT_REVERSED. `reverses_balance_event_id` with `fk_set_balance_reversal` (same tenant, scope, row and currency as the original event). `uq_set_balance_single_reversal` (one reversal per event). `chk_set_balance_shape`: a reversal needs the reference, a registration must not have one. `chk_set_balance_reversal_reason` (reason required). Append-only BEFORE UPDATE/DELETE triggers. V11 leaves three invariants to Application: RETURN_REVERSED reverses only RETURN_REGISTERED, REIMBURSEMENT_REVERSED only REIMBURSEMENT_REGISTERED, and the reversal amount equals the original amount |
| Domain | Partial. `AdvanceSettlement.reverseReturn(amount, reason)` and `reverseReimbursement(amount, reason)` exist and refuse CERRADO rows, but neither references the original event nor checks the amount against it. Only `reverseReturn` has a domain unit test (`AdvanceSettlementTest.reverseReturnDecreasesReturnedAmount`) |
| Persistence | Not supported. `SettlementBalanceChange` carries no reversed-event reference, and `JdbcSettlementBalanceEventRepository` never writes `reverses_balance_event_id`, so a reversal row would violate `chk_set_balance_shape` |
| Application / Case | None. No use case exists, and nothing reverses a Case return that was split across rows (receipt 2817 = events 29 + 30) |
| API / Studio | None. The Case controller has returns, reimbursements, reconcile and close only; the legacy settlement API has no reversal; Studio has no action |

`RETURN_REVERSAL_SUPPORTED_NOW=NO`. `RETURN_REVERSAL_GAP=YES`: an MVP functional gap exposed by the Owner smoke. A mistaken
return can be neither corrected nor reversed in the product.

Nothing durable ties events 29 and 30 to the one Case command that produced them:
- `settlement_balance_event` has no command or movement-group column, and no migration after V11 alters that table.
- Receipt 2817's result snapshot names only the Case.
- The two events share `occurred_at`, actor and reason, but that combination is not a guaranteed key.

Per-event reversal fits V11 as it is. Reversing "the Case return" as one unit would need either a grouping reference (a
schema change) or a rule that lists the Case's return events for selection.

Consequence for this Case: closing requires a balanced, reconciled Case rendition. The only in-product way to balance −380
today is a USD 380 reimbursement. If the return was not real, that would record a USD 300 payment nobody owes, so it is not
a valid workaround.

Under the V11 design, a correction reverses the whole original movement and never edits it:
- If no money was returned: RETURN_REVERSED 200.00 → event 29 and RETURN_REVERSED 100.00 → event 30, each with a reason,
  in one Case command. The balance becomes −80.
- If USD 100 was really returned: the same two reversals, then a new RETURN_REGISTERED 100.00. The balance becomes −180.

## 5. UX safety

- "Registrar devolución" is offered when `canRegisterReturn` is true. That requires all of: the Case takes rendition
  commands, it has a delivered advance, its rendition is not CERRADO, and the pending return is above 0.
- Non-final expenses (REGISTRADO, PENDIENTE_REVISION, OBSERVADO) do not affect that button. Only closing the Case refuses
  them (`ExpenseCaseService.close`).
- Conciliar was admitted at 16:40:31 while all four expenses were still REGISTRADO, because the Case balanced then.
  - Rows 61 and 62 are still stored as RECONCILED / CONCILIADO with `justified_expense_total` 0.0000.
  - The Case rendition status is computed live (`CaseRenditionLedger.status`) and is ABIERTO now: the balance is −380 and
    advance 108 has no row.
  - This is the accepted Case-level rule, not a defect.
- Recommendation only:
  - Warn before registering a return while non-final expenses exist, showing their count and amount.
  - Confirm the amount and its consequence ("Esta devolución se registrará como un movimiento real. Si posteriormente se
    aprueban más gastos, podría generarse un importe por reembolsar.").
  - Reconsider pre-filling the full pending amount.

## 6. Case business identifier

- `expense_case` has no business number, sequence or human-readable identifier. It was created by V24; V25 added
  `reviewer_snapshot_name`; V35 added closure.
- Keys: PK `expense_case_id`, `uq_case_tenant_uuid (tenant_id, expense_case_uuid)`,
  `uq_case_scope_id (tenant_id, organization_scope, expense_case_id)` and the index
  `ix_case_context_created (tenant_id, organization_scope, created_at, expense_case_id)`. There are no triggers.
- The domain `ExpenseCase` carries publicId (UUID), name, participants, status, createdAt/createdBy and closure fields. The
  API path `{reference}` accepts only the UUID.
- Studio: "EXP. NN" is the list position (`caseListTitle`, STEP 20 FINAL, never persisted), and "Fecha" is the UTC day of
  `createdAt` (`createdAt.slice(0, 10)`).
- Platform: the only numbering table is `document_sequences`. It is for SRI fiscal numbering (establishment, emission
  point, document type), has no Java writer and holds 0 rows in Shared DEV, so it is not reusable for an internal Case number.
- Time zone: `tenants.time_zone` exists (VARCHAR(100)) but is NULL for all tenants, and no code reads it. MySQL runs in UTC.
- Read-only backfill simulation: order per tenant by business date, `created_at`, then `expense_case_id`. No duplicates
  occur under either day rule across all tenants.
  - "Compra Filtro" gets `202609170001` under both the UTC day and the Ecuador day.
  - In tenant 1, one of 8 Cases changes day: "PRUEBA20260909" (created 2026-09-10 03:25 UTC, which is 2026-09-09 22:25 in
    Ecuador) gets `202609100001` (UTC) vs `202609090001` (Ecuador).

Proposal (not implemented):
- Internal `caseNumber` (column `case_number`), with "ID Gasto" as the UI label, as requested.
- Generated server-side in the Case-creation transaction from a per-tenant, per-business-date counter row
  (`INSERT … ON DUPLICATE KEY UPDATE last_value = LAST_INSERT_ID(last_value + 1)`).
- Immutable and unique on `(tenant_id, case_number)`.
- `MIGRATION_REQUIRED=YES`. V64 would add the columns and the counter table, run a deterministic backfill, and enforce
  uniqueness and immutability.
- Owner decisions: the business-date time zone, the overflow policy and the label.

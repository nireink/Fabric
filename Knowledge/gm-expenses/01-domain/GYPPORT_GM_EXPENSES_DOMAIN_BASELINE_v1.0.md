# GYPPORT gm-expenses — Domain Baseline v1.0

```text
TRACK=GM-EXPENSES-INITIAL-DEVELOPMENT-01
PHASE_A_STATUS=OWNER_ACCEPTED
PHASE_B_STATUS=OWNER_ACCEPTED
```

This document is the final domain model. It does not reproduce discarded
intermediate alternatives (e.g. an Advance lifecycle with a `VENCIDO` state)
— only the accepted outcome.

## 1. Expense modes

```text
MODES:
- PERSONAL
- ORGANIZATION
```

| Mode | organization_id | Notes |
|---|---|---|
| PERSONAL | absent | `BUSINESS_PROFILE_REQUIRED_FOR_PERSONAL_EXPENSE=NO`; `RUC_REQUIRED_FOR_PERSONAL_EXPENSE=NO` |
| ORGANIZATION | required | Must later be access-validated by the Host (see integration baseline, §Security/Context) — client-selected organization is never itself authoritative |

## 2. Aggregate / domain models

- `ExpenseAdvance`
- `Expense`
- `AdvanceSettlement`
- `ResponsibleReference`
- `VehicleReference`
- `ExpenseCategory`
- `ExpenseAdjustment`
- `ExpenseDocument`
- `ExpenseCase` (with its business number, `CaseNumber`)

## 3. ExpenseAdvance

### Lifecycle (final)

```text
BORRADOR
ENTREGADO
EN_RENDICION
OBSERVADO
RENDIDO
CERRADO
CANCELADO
```

`VENCIDO_IS_LIFECYCLE_STATE=NO`. Overdue is a **derived** condition, never a
persisted state:

```text
overdue = rendition_due_at < now()
```

Overdue derivation excludes advances in `RENDIDO`, `CERRADO`, or `CANCELADO`
— an advance that has already been settled, closed, or cancelled cannot be
"overdue" regardless of `rendition_due_at`.

### Rules

- Only an advance in `BORRADOR` may be cancelled.
- `DELIVER` (BORRADOR → ENTREGADO) freezes financial/identity/activity
  snapshots at the moment of delivery.
- Once delivered, an advance's core financial and activity identity is
  immutable — it cannot be cancelled to erase delivered money.
- Delivered money must be financially resolved through `AdvanceSettlement`,
  never by reverting the Advance's own state.
- `DELIVER` requires an `AdvanceDeliveryMethodCode` (nonblank, canonical
  uppercase code — see the Persistence Baseline, §12, and the
  Implementation Constraints) describing how the funds were handed over
  (e.g. cash, bank transfer). It is absent while in `BORRADOR` and
  mandatory from `DELIVER` onward, frozen together with the other
  delivery snapshots (responsible name, vehicle plate, `deliveredAt`,
  `renditionDueAt`). No operation changes it after delivery — it is part
  of the delivered Advance's frozen identity, same as the other snapshot
  fields.
- A `BORRADOR` may carry an `AdvanceDeliveryPlan` — the planned delivery
  method and planned rendition days (1–365) chosen when the advance is
  registered (V62, GM_EXPENSES_FINAL_ADJUSTMENT_V62_04). The plan is not a
  delivery snapshot: the `AdvanceDeliveryMethodCode` above stays absent
  while in `BORRADOR`. `DELIVER` of a planned draft copies the plan into the
  frozen delivery snapshot (`renditionDueAt = deliveredAt + planned days`)
  and refuses a different method or number of days; a draft registered
  without a plan names both at `DELIVER`.
- **Several advances per ExpenseCase** (Owner decision,
  GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10). The ExpenseCase
  is the funding and rendition center; its advances are funding tranches
  (for example 30,000, 2,000, 300 and 5,000 in one open Case), valid in any
  number and currency, and its expenses belong to the Case, never to an
  advance. Registering an advance and delivering a draft never depend on the
  Case's other advances. The only advance rule on the Case lifecycle is the
  closure blocker: a Case does not close while it holds a `BORRADOR` advance.
  Since GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11 the blocker names
  how many drafts there are and how much they add up to: "Hay 1 anticipo en
  borrador por USD X.XX. Confirma su entrega o cancélalo antes de cerrar el
  expediente." / "Hay N anticipos en borrador por un total de USD X.XX.
  Confirma su entrega o cancélalos antes de cerrar el expediente." A draft
  never prevents adding another advance. The rendition is the Case's own
  (§5, Case-level rendition): no approved expense is ever distributed to an
  advance.
  *Superseded wording of FIX_10 (kept for history): the blocker copy "El
  expediente tiene anticipos en borrador; confirma su entrega o cancélalos.",
  and "Distributing the Case's approved total across the renditions of its
  advances in delivery order is only the mechanism that lets each rendition
  reconcile; it is not business policy." FIFO stopped being used at all with
  GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11.*
  *Supersedes the invariant "one financially active advance per ExpenseCase
  and currency" of GM_EXPENSES_ONE_ACTIVE_ADVANCE_PER_CASE_CURRENCY_06
  (2026-09-16), with its registration and delivery refusals ("Resuelve el
  anticipo actual antes de registrar otro.", "Resuelve ese anticipo antes de
  confirmar esta entrega.") and its rule that only one legacy draft may
  continue toward delivery. It never had a database constraint.*
- **MVP closure policy** (Owner decision of
  GM_EXPENSES_ONE_ACTIVE_ADVANCE_PER_CASE_CURRENCY_06, still in force). The
  ExpenseCase remains the operational center of rendition; Studio has no
  independent "Cerrar anticipo", "Cerrar rendición" or "Finalizar anticipo"
  workflow. A draft is delivered or cancelled. The Case then goes expenses →
  review → the Case's return / reimbursement → Conciliar on the Case → Cerrar
  expediente, where the existing closure chain closes every reconciled
  rendition row and every funding advance (`CERRADO`). No command renders,
  reconciles or closes one advance on its own
  (GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11).

### UX field mapping

The approved UX ("Información general") maps onto existing Domain
concepts — none of the fields below introduce a new aggregate:

| UX field | Domain concept |
|---|---|
| Conductor | `ResponsibleReference` / its delivery snapshot |
| Vehículo | `VehicleReference` / its delivery snapshot |
| Fecha entrega | `deliveredAt` |
| Motivo | `ActivityType` (presentation label) |
| Entrega realizada por | `deliveredByUserAccountId` |
| Método de entrega | `AdvanceDeliveryMethodCode` |
| Observación | `activityDescription` |

"Conductor" is a UI role label for `ResponsibleReference`, not a new
aggregate. A UX screen titled "Mi viaje" does not imply a `Trip`
aggregate — `ActivityType`/`activityDescription` already cover it.

**Not yet decided**: the UX also shows a human-friendly reference such as
`ANT-000001`. This is **not** approved as a persisted sequential business
number. `INTERNAL_ADVANCE_ID_EXPOSED=NO` remains the rule — no
`advance_number` or `advance_sequence` column exists or is planned here.
Whether `ANT-000001` becomes a derived presentation value (from the
public UUID) or a real persisted business sequence is a separate,
not-yet-made Owner decision for later API/UX work.

## 4. Expense

### Lifecycle (final)

```text
REGISTRADO
PENDIENTE_REVISION
OBSERVADO
APROBADO
RECHAZADO
EXCLUIDO
```

### Review operations (explicit only — no generic update)

```text
SUBMIT
ACCEPT
OBSERVE
REJECT
REMOVE_FROM_REVIEW
EXCLUDE
REINSTATE
REOPEN_APPROVED
AMEND_EXCLUSION_REASON
```

`AMEND_EXCLUSION_REASON`: `EXCLUIDO → EXCLUIDO` — status does not change; the
operation only appends an audit fact recording the new reason. It is not a
status transition.

### Review history integrity (Owner rule, GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13)

- A modern `OBSERVADO` always carries its immutable `OBSERVED` event in
  `expense_review_event`. The status change and the event insert happen in the
  same transaction; if either fails, the whole review decision rolls back and
  the expense keeps its previous status and version (no idempotency receipt is
  kept either).
- The event's actor is the authenticated global UserAccount of the session
  (`performed_by_user_account_id`), never the Case's responsible or any Person.
  Its time (`occurred_at`) is the server's system clock at the request, never a
  client value. The motive code is stored in `reason` and the optional detail in
  `notes`.
- The history is append-only: database triggers refuse UPDATE and DELETE.
- Today the only production path into `OBSERVADO` is OBSERVE
  (`PENDIENTE_REVISION → OBSERVADO`). `REOPEN_APPROVED` exists in the domain model
  but has no production caller; wiring it later must write its own event in the
  same transaction.
- `RECHAZADO` stays final. There is no `OBSERVADO → RECHAZADO` transition: an
  observed expense is corrected (back to `PENDIENTE_REVISION`) and then decided.
- An `OBSERVADO` expense without its `OBSERVED` event can only be legacy data
  written before the review history existed (before 2026-09-03). The correction
  refuses it, and its history is never fabricated. Cleaning such data up is a
  controlled, Owner-authorized DEV data operation recorded as evidence (and in the
  global audit table `audit_logs`), not a product state-machine rule.

### Expense revision history (Owner rule, GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14)

- Material field changes keep using the existing revision mechanism: the domain
  returns `ExpenseRevisionChange(previous, newDetails)` from `editRegistered` and
  `correctObserved`, and the use case writes one `expense_revision_event` in the same
  transaction as the expense update.
- Each revision row keeps a sequential `revision_number`, its `revision_type`
  (`EDITED_BEFORE_REVIEW`, `CORRECTED_AFTER_OBSERVATION`), the `reason`, the full
  `previous_snapshot` and `new_snapshot` (category, amount, currency, date,
  description), the actor (`performed_by_user_account_id`, the authenticated global
  UserAccount), `occurred_at` (server clock) and, for a correction, the review events
  it answers (`triggering_review_event_id` = OBSERVED) and produces
  (`resulting_review_event_id` = CORRECTION_SUBMITTED).
- The history is append-only: database triggers refuse UPDATE and DELETE.
- No other changes table, event-sourcing model or free mutable field without revision
  evidence is introduced. Status transitions are recorded in `expense_review_event`;
  material field changes in `expense_revision_event`.

### Expense ↔ Advance relationship

- One `Expense` references at most one `ExpenseAdvance`.
- One `ExpenseAdvance` may contain many `Expense`s.
- A standalone `Expense` with no advance reference is allowed.
- `advance_reference_frozen` is **monotonic**: once set `TRUE` (at first
  settlement-context review), it can never return to `FALSE`.

## 5. AdvanceSettlement

### Statuses (final)

```text
ABIERTO
EN_CONCILIACION
CONCILIADO
CON_DIFERENCIA
CERRADO
```

### Reconciliation

```text
PENDING
RECONCILED
NOT_RECONCILED
```

### RN-001 — settlement balance

*Amended 2026-09-16 by GM_EXPENSES_UNIFIED_RECONCILIATION_V63_05 (Owner decision
OWNER_DECISIONS_COMPLETE of GM_EXPENSES_RENDITION_DIFFERENCE_SEMANTICS_FIX_02, option A;
schema `V63`).*

A return and a reimbursement are real cash movements that may happen at
different moments of one rendition. One equation governs every settlement:

```text
advanceAmount + reimbursementAmount
    = justifiedTotal + returnedAmount + authorizedAdjustmentTotal
```

`justifiedTotal` is the approved expense total the settlement holds
(`approvedExpenseTotal`). The rendition balance is:

```text
balance = advanceAmount + reimbursementAmount
          - justifiedTotal - returnedAmount - authorizedAdjustmentTotal
```

| Balance | Meaning | Label |
|---|---|---|
| greater than 0 | still to justify or to return | Por justificar o devolver |
| less than 0 | still to reimburse | Por reembolsar |
| equal to 0 | the equation holds | Pendiente de conciliar USD 0.00 |

Superseded label (V63_05, kept for history): "Diferencia USD 0.00". It stopped being
canonical with GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07, because a bare
"Diferencia" beside Entregado and Usado reads as Entregado − Usado.

The former separate equations — normal / shortfall
(`advanceAmount = approvedExpenseTotal + returnedAmount + authorizedAdjustmentTotal`)
and overspend (`advanceAmount + reimbursementAmount = approvedExpenseTotal`) —
are special cases of this one.

Rules:
- A valid return followed by later approved expenses may legitimately turn the
  balance negative and create a reimbursement obligation. That is valid
  financial history: the return is never reversed automatically, no
  reimbursement is created automatically, and approving an expense is never
  blocked because a return exists.
- A movement registered by mistake is corrected by a **reverso**, never by an edit or a
  deletion (Owner decision GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20 §8, on the reversal shape V11
  anticipated). The reverso is a new compensating event that names the movement it reverses
  (`reverses_balance_event_id`), for exactly that movement's amount, with a required motive,
  at most once per movement, and only while the Case and its rendition are open. The
  rendition goes back to pending, so the Case must be reconciled again. A partial correction
  is a reverso followed by a new, correct movement. The actor is the authenticated global
  UserAccount and the instant is the server's.
- A Case movement stored across several rendition rows is reversed as the one movement the
  Owner registered: the Case's movements are grouped by type, instant, actor and motive, and
  every event of the movement is compensated in the same transaction.
- A new return is capped at `max(balance, 0)` and a new reimbursement at
  `max(-balance, 0)`, measured after the justified total is refreshed.
- `RETURN_REVERSED` corrects a return entered wrongly or never physically
  made; it is never used because later approvals changed the balance.
- Reconciliation readiness: `balance = 0`, plus the existing workflow
  prerequisites. Nothing reconciles automatically; the user presses Conciliar.
- `authorizedAdjustmentTotal` keeps its shortfall-only meaning: it never
  coexists with a reimbursement.
- A `CERRADO` (closed) settlement is immutable.

Superseded wording (V11, kept for history): "`returnedAmount` and
`reimbursementAmount` can never both be positive at the same time." It stopped
being canonical with `V63`.

Rendition position of an ExpenseCase (same Owner decision): the Case card,
its Resumen financiero and the reports read JUSTIFIED amounts. "Usado" stays an
independent operational metric and never decides whether the employee or the
organization owes money. The direction is decided per ExpenseCase before any
aggregation — one Case still to justify or return never nets against another
Case still to reimburse. An ExpenseCase with no delivered advance has no
rendition yet, although its expenses still count as used.
A Case may hold several advances (§3, GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10).

*Superseded wording (kept for history): "Sharing the Case's approved expenses across
their renditions in delivery order (FIFO) only lets each rendition reconcile; it is
not business policy, and the Case's own position never depends on it. For such Cases
the Resumen financiero shows the Case's net position while every advance keeps showing
its own direction (Owner acceptance of GM_EXPENSES_UNIFIED_RECONCILIATION_V63_05)." It
stopped being canonical with GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11: the
rendition is the Case's own and no advance shows a direction or a justified total.*

### Case-level rendition

*Owner decision of GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11 (2026-09-16). No
schema change: V62 and V63 are unchanged.*

The ExpenseCase is the funding and rendition center. Its delivered advances are
funding tranches (several, in the same currency too), its expenses belong to it, and
its rendition is one per currency. RN-001 holds for the Case as a whole:

```text
caseBalance = totalDelivered + totalReimbursed
              - totalJustified - totalReturned - totalAuthorizedAdjustments
```

| Case total | Definition |
|---|---|
| totalDelivered | the Case's delivered advances (delivered, neither `BORRADOR` nor `CANCELADO`) |
| totalJustified | the Case's `APROBADO` expenses, once it has a delivered advance in that currency; 0 before |
| totalReturned / totalReimbursed / totalAuthorizedAdjustments | the movements its rendition rows hold |

The direction follows the RN-001 table above: greater than 0 is Por justificar o
devolver, less than 0 Por reembolsar, equal to 0 Pendiente de conciliar USD 0.00.

Rules:
- **FIFO is not canonical.** No approved expense is allocated to an advance, in
  delivery order or any other, and no per-advance justified total is business truth.
  No FIFO compatibility code remains: a legacy `CERRADO` rendition row keeps its frozen
  totals, which are read as they are and never re-allocated.
- **Commands on the Case.** Registrar devolución, Registrar reembolso and Conciliar are
  commands on the ExpenseCase in one currency, guarded by the version of the Case's
  rendition the user saw. None names an advance or a settlement row. A return is capped
  at `max(caseBalance, 0)`, a reimbursement at `max(-caseBalance, 0)`, and a Case holding
  an authorized adjustment takes no reimbursement.
- **Conciliar** is offered and admitted only while the Case balances. It never reconciles
  one advance on its own.
- **Technical carriers.** `advance_settlement` stays one row per delivered advance, as a
  carrier of the Case's movements and of the existing closure chain; it is never shown
  and never authoritative. The first rendition command opens the rows of every delivered
  advance that has none (moving those advances to `EN_RENDICION`). A return is stored on
  the open rows holding the most money first, split only when one row is not enough; a
  reimbursement on the open row of the largest advance; every stored part keeps its own
  `settlement_balance_event`. Conciliar sets each open row's justified total to exactly
  the money the row holds (`advance + reimbursed − returned − adjustments`), so every
  row satisfies V63 `chk_settlement_reconciled_equation` on its own while the Case
  balances as a whole. Those row totals exist only to reconcile and close; an approval of
  a Case expense resets them, which reopens a reconciled Case.
- **V63 at Case level.** The Case equation is evaluated on the Case totals; V63 keeps
  holding every `RECONCILED` row, which the carrier rule above guarantees.
- **Per-advance API.** The per-advance settlement endpoints (`/api/settlements/*` and
  `/api/expense-advances/{id}/settlement`, reads included) refuse an advance of an
  ExpenseCase: "La rendición de este anticipo se gestiona desde su expediente." They stay
  for an advance outside any Case.
- **Rendition status** (derived, never stored): `SIN_INICIAR` before any row opens;
  `CONCILIADO` once every delivered advance has a row, the open rows are reconciled and
  the Case balances; `CERRADO` once every row is closed; `ABIERTO` otherwise.
- **An additional advance** delivered after expenses were approved only adds to
  totalDelivered: no expense moves, no row is rewritten, and a view of the older
  rendition is stale.
- **Closure** (Cerrar expediente), in the order the user acts on it: expenses awaiting
  submission, approval or correction; flagged documents; drafts (the Owner copy of §3);
  observed advances; then, per currency, an unbalanced Case ("La rendición del
  expediente tiene saldo pendiente; registra la devolución o el reembolso y vuelve a
  conciliar.") and a Case not yet reconciled ("Concilia la rendición del expediente antes
  de cerrarlo."). Closing then closes every open rendition row and every funding advance
  through the existing chain, in the same transaction. A legacy `CERRADO` row whose
  advance is still open keeps blocking with its regularization message.
- **The Advance page** keeps the advance's own history and reads "Rendición: Se gestiona
  desde el expediente"; it shows no justified, returned or reimbursed amount of its own.
- **Reports** decide each Case's direction on its own totals first, then add Cases up per
  currency, so a Case at +30 and another at −20 stay 30 to justify or return and 20 to
  reimburse, never a net 10.
- **Before any delivered advance** (option B): the Case card, the Case detail and the
  reports show plain zeros — Entregado USD 0.00, Usado as used, Justificado USD 0.00,
  Devuelto USD 0.00, Reembolsado USD 0.00, Pendiente de conciliar USD 0.00 — and the card
  reads Uso 0% on an empty bar. No obligation is invented. The reports joined this
  vocabulary with the Owner decision of GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 (2026-09-17);
  it is a presentation normalization only.

### Financial presentation vocabulary

*Owner decision of GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07, amended 2026-09-17 by
GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20 §3/§10 (Total anticipos, Total gastos, Total a conciliar).
Presentation only: RN-001, the caps and the reconciliation behavior above are unchanged.*

The Case card and the Case detail (its Resumen financiero; since
GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11 no advance has a rendition of its own)
use one vocabulary:

| Term | Meaning |
|---|---|
| Total anticipos | money delivered by the Case's advances. An advance counts once its delivery exists, and a later state (EN_RENDICION, RENDIDO, CERRADO) never removes it from the funding; a draft or cancelled advance with no delivery counts zero (GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21 §2) |
| Total gastos | the Case's approved expenses (APROBADO), never approved minus rejected |
| Total a conciliar | Total anticipos − Total gastos, before the real cash movements, with its direction: Por devolver, Por reembolsar or Balanceado |
| Usado | operational metric: the Case's expenses that are neither rejected nor excluded; it never decides the reconciliation |
| Devuelto | returns registered on the Case |
| Reembolsado | reimbursements registered on the Case |
| Ajuste autorizado | an authorized adjustment, shown only when one exists |
| Pendiente | the position the real movements land on, shown like Total a conciliar: the amount with its direction as the caption (GM_EXPENSES_OWNER_SMOKE_FINAL_CORRECTION_21 §8) |
| Por justificar o devolver | balance greater than 0 |
| Por reembolsar | balance less than 0 |
| Pendiente de conciliar | balance equal to 0 (USD 0.00), also USD 0.00 before any advance is delivered (card, Case detail and reports) |

*Superseded (kept for history): "Entregado" is now Total anticipos and "Justificado" is now
Total gastos on the card and in the Case detail (MVP_FINAL_RELEASE_CONSOLIDATION_07 wording).
The reports keep Entregado / Usado (todo el expediente) / Justificado until the Owner decides
whether their vocabulary follows.*

A rejected, observed, registered or unreviewed expense weighs zero in Total gastos, in Total a
conciliar and in the balance, and rejecting one creates no advance, return, reimbursement or
adjustment (GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20 §1/§2). Total a conciliar and the position
differ exactly by what really moved, which is why both are shown.

Rules:
- A surface that shows a direction also shows the movements that explain it, so
  the visible numbers add up: Entregado + Reembolsado = Justificado + Devuelto
  (+ Ajuste autorizado) + the position. The Case card shows Entregado, Usado,
  Justificado, Uso, Devuelto, Reembolsado and the direction; a closed Case such
  as 679 delivered, 200 used and justified, 499 returned and 20 reimbursed reads
  Pendiente de conciliar USD 0.00.
- The direction is always the backend's balance. It is never calculated as
  Entregado − Usado, and "Usado" and "Justificado" are never merged, because they
  can differ.
- Never a bare "Diferencia", never "Saldo", and never "Exceso gastado" as a
  rendition obligation. Sentences that name the difference in context, such as
  "Faltan USD X.XX por justificar o devolver." or "Conciliar estará disponible
  cuando la diferencia sea USD 0.00.", remain.
- Without a delivered advance no return or reimbursement obligation is shown:
  expenses still count as Usado, categories and period totals. The Case card, the Case
  detail and the reports read plain zeros for every funding field (option B of
  GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11, extended to the reports by the
  Owner decision of GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12), never "No aplica" or "—";
  Usado keeps its real amount.
  *Superseded (kept for history): "Without a delivered advance the direction is No aplica"
  with "Sin anticipo" (card and Case detail, until STEP 11), and "the reports keep No aplica"
  (until FINAL_12).*
- A Case with several advances shows its own direction on the card and in the
  Resumen financiero, and no advance shows a direction of its own.
  *Superseded (kept for history): "and every advance keeps its own direction."*
- The card shows two independent indicators, each with its own compact track, for open
  and closed Cases alike (Owner decisions of GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13
  and, for their placement, GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14). They live
  in different semantic regions and are never rendered as one combined block.
  - **Conciliado** is a Case-lifecycle indicator, one per Case. It sits in the card
    header's right rail, above the Finanzas divider: the Abierto / Cerrado status keeps
    the top right, and Conciliado starts level with the Responsable row on desktop and
    tablet widths (GM_EXPENSES_CASE_CARD_FINAL_HEADER_ALIGNMENT_15), without narrowing
    the Responsable / Supervisor / Recurso asignado block. It reads
    100% on a full track only when the Case is closed and nothing is left to justify,
    return or reimburse in any currency. An open Case has no canonical intermediate
    percentage, so it reads **Pendiente** on an empty track: no invented ratio and never
    a false 100%. A closed Case that still shows a pending amount (legacy data only)
    also reads Pendiente.
  - **Uso** is a Finanzas metric, one per currency, inside Finanzas beside Entregado,
    Usado and Justificado. It is Usado / Entregado (e.g. 260 of 300 = 87%) and keeps its
    real value past 100% (for example 110%): only the fill stops at the track. Without a
    delivered advance Uso reads 0% on an empty track whose outline stays visible (option B
    of GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11), never "Uso —" or No aplica.
  - On narrow screens the layout wraps: Conciliado stays under the status in the header,
    Uso stays within Finanzas, both stay visible and nothing overflows horizontally.
  *Superseded (kept for history): FIX_10 "The card has one progress bar: Uso while the Case
  is open; Conciliado 100% once closed, with Uso as a plain figure beside it."; HARDENING_13
  "two indicators per currency in a column beside the amounts, side by side below them on
  narrow screens".*

### ExpenseCase business number — "ID Gasto" (Owner decision, GM_EXPENSES_FINAL_MVP_CLOSURE_22, schema `V64`)

A Case carries three separate identities, and they never do each other's work:

| Level | What it is | Where it is used |
|---|---|---|
| Technical id | the public UUID | every API route, unchanged |
| Business number | `caseNumber`, format `YYYYMMDD####` (for example `202609170001`) | shown as "ID Gasto" wherever a person reads or quotes the Case |
| Full business reference | `RUC-ESTABLISHMENT_NUMBER-CASE_NUMBER`, derived | traceability, export, reports, support; never on the Case card |

Rules:
- The sequence runs per **tenant and business date** and needs nothing else. An establishment and a RUC take part only in
  the full reference, when that fiscal data exists; their absence never stops a Case from getting its number.
  *Superseded (kept for history): the sequence scope "tenant + establishment + business date", which blocked the number
  behind a fiscal foundation that holds no data.*
- `case_business_date` is resolved once, when the Case is created - the tenant's configured zone, otherwise the
  platform's `gypport.business.default-zone` - and then persisted. The Case's "Fecha" and the `YYYYMMDD` of its number
  are that same stored day, so they can never disagree, and a later timezone configuration never renumbers or re-dates
  anything.
- Historical Cases keep the day their users already saw (the UTC day of `created_at`) and were numbered deterministically
  within tenant and day by `created_at`, then the internal id.
- 1..9999 per tenant and day. Passing it refuses the creation with a domain error rather than widening the format.
- The number is allocated server-side by a persistent counter inside the creating transaction, so concurrent creations
  cannot collide and a rolled-back creation keeps no number. Never `MAX()+1`, a process counter, the UI, "EXP. NN", a
  transformation of the UUID, or the SRI `document_sequences`.
- `case_business_date`, `case_sequence` and `case_number` are immutable once assigned, enforced in the database.
- **Two numbers, two purposes** (Owner decision, GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25, schema `V65`).
  A Case carries four identities, and none does another's work:

  | Concept | Field | Scope | Example | Shown as |
  |---|---|---|---|---|
  | Technical id | the public UUID | global | `437a92bf-...` | routes only, never shown |
  | Permanent expediente number | `expense_sequence` (`ExpenseSequence`, API `expenseSequence`) | tenant | 2 | `EXP. 02` |
  | Daily case sequence | `case_sequence` (API `caseSequence`) | tenant + business date | 1 | composes the ID |
  | Business number | `case_number` (`CaseNumber`, API `caseNumber`) | tenant | `202609170001` | `ID: 202609170001` |

  `EXP. NN` counts the tenant's Cases in the order they were created - 1, 2, 3 ... 99, 100 - and never restarts: a new
  business day resets only `case_sequence`. Creation order decides EXP and the business date decides the ID, so a Case
  created today for an earlier business date still takes the next EXP while its ID reads that earlier day. The permanent
  number is allocated server-side from its own counter (one row per tenant) inside the creating transaction, is unique
  per tenant, is immutable once assigned and never takes part in `case_number`; the daily sequence never decides EXP.
  The display keeps a minimum of two digits and is never truncated: 1 -> `EXP. 01`, 9 -> `EXP. 09`, 100 -> `EXP. 100`.
  A payload without `expenseSequence` carries no EXP rather than a daily count dressed as a permanent one.
  Historical Cases were numbered within their tenant by `created_at`, then the technical id.
  *Superseded (kept for history): "EXP. NN" derived from `case_sequence` (GM_EXPENSES_FINAL_CASE_CARD_NUMBERING_ALIGNMENT_22A,
  2026-09-17), under which the first Case of every business day read EXP. 01 again; and before it "EXP. NN" as the
  card's position in the backend's newest-first list (STEP 20 FINAL). A Case's number never depends on the page, the
  order, a sort or a filter.*
  The visible label of the complete business number is `ID:` (it was `ID Gasto:` while the feature was being built).

## 6. Money

- Conceptual representation: `BigDecimal`.
- `amount >= 0` always.
- Operations that require a genuine financial entry validate `amount > 0`.
- Negative `Money` is never valid.
- Same-currency invariants apply to any operation combining two `Money`
  values.

## 7. Vehicle boundary

```text
GM_FLEET OWNS:
- canonical vehicle master
- technical vehicle data
- odometer history
- maintenance history
- oil / tire technical records

GM_EXPENSES OWNS:
- financial Expense records
- ExpenseAdvance
- AdvanceSettlement
- expense evidence/documents
- local operational VehicleReference
```

There is no dependency on `gm-service-management`.

**Current reality**: `gm-fleet` is bootstrap-only today (no `pom.xml`, no
`src/`, no vehicle master implemented anywhere). This is not an edge case to
plan around — it is the current, unconditional state. `gm-expenses`' local
`VehicleReference` is therefore the operational model for the initial MVP,
not a fallback.

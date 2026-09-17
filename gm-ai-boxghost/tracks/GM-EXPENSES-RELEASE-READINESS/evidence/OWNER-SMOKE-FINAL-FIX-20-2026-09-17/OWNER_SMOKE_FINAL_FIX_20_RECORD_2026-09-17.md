# GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20 — implementation record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20
MODE=AUDIT_CONFIRM -> IMPLEMENT -> VERIFY
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_OWNER_SMOKE_FINAL_FIX_20.md
STATUS=READY_FOR_OWNER_FINAL_FIX_REVIEW (part A) + BLOCKED_FOR_ARCHITECTURE_REVIEW (part B, business identifier)
ACCEPTED_BASELINE=gm-expenses 545eae0, Gystigo bcb9591, Fabric bbdd66a, Shared DEV V63
MIGRATION_CREATED=NONE (V63 remains the head)
SHARED_DEV_MODIFIED=NO (read-only transactions only)   OWNER_CASE_MODIFIED=NO
FILES_STAGED=0 COMMITS_CREATED=0 PUSH_PERFORMED=NO
```

## 1. Environment precondition

No `SPRING_DATASOURCE_*`, `SPRING_FLYWAY_*`, `MYSQL*` or `GYPPORT_*` variable exists in the Process, User or Machine
scope, so nothing inherits Shared DEV. Repository heads matched the accepted baseline before any edit, with only the
5 known excluded WIP files in Gystigo and the 31 in Fabric.

## 2. Part A — financial semantics, movement UX and reverso (implemented)

### Canonical totals (§1–§3, §6)

- `Total anticipos` = delivered advances; `Total gastos` = APROBADO expenses only, never approved minus rejected.
- New derived value `Total a conciliar` = Total anticipos − Total gastos, exposed by the backend as `baseToReturn` /
  `baseToReimburse` (at most one positive) with the direction Por devolver / Por reembolsar / Balanceado.
- RN-001 is unchanged: the position stays `delivered + reimbursed − justified − returned − adjustments`.
- `Usado` and `Uso` stay operational metrics; Uso keeps its real percentage past 100% with the fill clamped.
- Verified in code: only four call sites can create a balance movement (the two legacy per-settlement use cases and the
  two Case-level ones), all explicit user commands. Rejecting an expense creates no advance, return, reimbursement or
  adjustment.

### Movement UX (§7)

- The amount is never pre-filled: `movementMaximum` only reports the ceiling the backend enforces.
- The motive is required by the backend (`MovementCommand`), not only by the form.
- An explicit confirmation names it as a real movement of money before anything is sent.
- A warning counts the expenses still undecided (REGISTRADO, PENDIENTE_REVISION, OBSERVADO) with their total. It never
  blocks a legitimate early return.

### Reverso (§8), reusing V11

- New Case command `POST /api/expense-cases/{id}/rendition/movement-reversals` with the movement, the rendition version
  and a required motive; new read `movements` on the Case detail.
- Each reverso is appended and names the event it compensates (`reverses_balance_event_id`), for exactly that event's
  amount. The original is never edited or deleted.
- Refused: a movement already reversed, a closed Case, a closed rendition row, an amount beyond what the row carries, a
  blank motive, a stale rendition version.
- The rendition reopens (EN_CONCILIACION), so the Case must be reconciled again.
- A Case movement split across rendition rows is shown and reversed as the one movement the Owner registered; the events
  of one command are grouped by type, instant, actor and motive.
- Persistence: the ledger port gained reads (no update, no delete), and the JDBC writer now stores the reversal
  reference, resolved inside the same settlement and currency the composite FK requires.

### Owner's Case (§9)

Not touched. After deployment the Owner reverses the USD 300 movement through the product, so the real actor is
recorded, and the Case then reads Total anticipos 320, Total gastos 400, Devuelto 0, Reembolsado 0, Por reembolsar 80.

## 3. Part B — business identifier (BLOCKED, no V64)

The STEP's own §15 and §17 order a stop before inventing architecture. Both conditions are met.

| Question | Evidence |
|---|---|
| Canonical establishment | `sri_establishments` (core migrations), re-parented to `tax_subjects` by V48. Owned by the Host capability `GYSTIGO_HOST_FISCAL_CONFIGURATION`, documented as `OUT_OF_FIRST_MVP; DEFERRED_FISCAL_CONFIGURATION` |
| Rows in Shared DEV (read-only) | sri_establishments 0, tax_subjects 0, emission_points 0, document_sequences 0, user_establishments 0, organization_tax_profiles 0 |
| Readers / writers in production code | none: no repository, port, adapter, use case, endpoint or Studio screen |
| Establishment in the Case creation path | absent: the context carries tenant, scope, organization, actor, operation id and instant only, and `expense_case` has no column |
| Historical Cases resolvable to an establishment | 0 of 29 (7 tenants). Inventing establishment 001 is forbidden by §15 |
| Business-date time zone | not resolvable: `tenants.time_zone` NULL in 15/15, `country_code` NULL in 15/15, the countries catalog has no zone, there is no injectable Clock and no zone reaches the frontend |
| Day divergence | 4 of 29 Cases fall on a different day under UTC than under America/Guayaquil |

`document_sequences` is SRI fiscal numbering and was not reused. RUC stays in `mdm_party_identifiers` (gm-entities is its
only writer) and is never a tenant key. Nothing was duplicated into gm-expenses.

## 4. Verification

```text
GM_EXPENSES_MODULE=763/763 PASS (748 before; +15 for §5 CASE A-D and §25 A-M)
STUDIO_CONTRACTS=636/636 PASS (631 before; +5)
STUDIO_LINT=PASS
HOST_EXPENSES_REAL_DB=104/104 PASS, 0 failures, 0 errors (run 96e3c1ac, disposable core_business_expenses_test at
  Flyway 63, container and evidence disposed) - host-expenses-realdb-result.json beside this record
MIGRATION_HEAD=V63 (unchanged, no V64)
RESPONSIVE=1280/768/375/320 all 0 px horizontal overflow (Case card fixture on its own Vite dev server, port 5189)
```

The Case card fixture renders the Owner's own smoke Case: Total anticipos USD 320.00, Total gastos USD 400.00,
Total a conciliar USD 80.00 · Por reembolsar, Usado USD 400.00, Uso 125%, Devuelto USD 300.00, Reembolsado USD 0.00 and
the position Por reembolsar USD 380.00. Conciliado stays in the header beside Abierto / Cerrado and Uso stays in
Finanzas; the four-column grid wraps to two at 375 and 320 with every label readable. The Case detail's movement form,
its warning, its confirmation and the reverso are covered by the Studio contracts; seeing them live needs the deployed
backend, which is the Owner's own smoke.

The Host suites run on a disposable `core_business_expenses_test` database through the project runner; the raw runner log
is not promoted here because it prints Spring's generated development password.

## 5. Not done in this STEP

No migration, no Shared DEV change, no data repair, no commit, no push, no PKG-2D or Docker change, no cross-module JDBC,
no duplicated RUC or establishment master, and no reuse of the SRI document sequences.

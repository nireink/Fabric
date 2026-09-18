# GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28 — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28
MODE=OWNER_RUNTIME_VERIFICATION -> AUTHENTICATED_CORRECTION -> FINAL_SMOKE -> EVIDENCE_CLOSURE -> MVP_FREEZE
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_OWNER_FINAL_SMOKE_AND_FREEZE_28.md
STATUS=FROZEN_OWNER_ACCEPTED_COMMITTED_LOCAL
BASELINE=GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
SOURCE_CODE_CHANGED=NO   SHARED_DEV_WRITTEN_BY_CLAUDE=NO   PUSH_PERFORMED=NO
```

## 1. The Owner's part (§2, §4, §8, §13)

The first pass stopped at BLOCKED_WAITING_OWNER_ACTION, which was not a defect: the acceptance and the reverso belong
in the Owner's authenticated session, Claude does not sign in as the Owner, and §4 forbids a SQL correction. The Owner
then did both in the real application at http://localhost:5173 and returned:

```text
OWNER_NUMBERING_VISUAL_ACCEPTED=YES   (EXP. 08: Compra Filtro, ID 202609170001; EXP. 09: VIAJE QUITO, ID 202609170002)
OWNER_LAYOUT_VISUAL_ACCEPTED=YES      (EXP / Fecha / ID, divider, Responsable / Supervisor / Recurso asignado / Conciliado, divider, Finanzas)
REVERSAL_EXECUTED_BY_OWNER=YES
REVERSAL_RESULT=SUCCESS
REIMBURSEMENT_TEST=DEFERRED
SYNTHETIC_DEV_DATA_DECISION=KEEP
```

## 2. Runtime and source

```text
gm-expenses 39a2adf4dfff0196208a1f80719be1c12c047ac2 (clean)   Gystigo 5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc (5 unrelated WIP)
Fabric 1f5bed831c54d01efe74444f02ee2b2d947df549 before this STEP's closure commit (10 unrelated WIP)
official backend gypport-backend-dev 445046e2801e, image gystigo-backend:4.1.0-java25-gm-expenses-v65-5eed5d6
  (sha256:f44f598a5a78...), started 2026-09-18T03:31:46Z, 0 restarts, healthy   Shared DEV Flyway 65, 0 failed
```

## 3. The Owner Case before the correction (§3) — `pre-reversal-state.txt`

Read twice, the second time just before the first stop, with the same bytes:

```text
CASE Compra Filtro | ABIERTO | EXP. 08 | ID 202609170001 | Fecha 2026-09-17
EVENT 29 RETURN_REGISTERED 200.00 | reverses NULL | actor 1 | 2026-09-17 16:40:29.559 | reason "100"
EVENT 30 RETURN_REGISTERED 100.00 | reverses NULL | actor 1 | 2026-09-17 16:40:29.559 | reason "100"
REVERSALS=0   settlement rows 61 and 62 CONCILIADO / RECONCILED, returned 200 and 100, reimbursed 0
=> Total anticipos 320.00 | Total gastos 400.00 | Total a conciliar 80.00 Por reembolsar | Devuelto 300.00 |
   Reembolsado 0.00 | Pendiente 380.00 Por reembolsar | Usado 400.00 | Uso 125%
```

Events 29 and 30 share instant, actor and reason, so the product showed them as one movement, "Devolución USD 300.00".

## 4. The Owner's reverso (§4, §5) — `post-reversal-state.txt`

```text
EVENT 29 RETURN_REGISTERED 200.00 | reverses NULL | actor 1 | 2026-09-17 16:40:29.559 | reason "100"          unchanged
EVENT 30 RETURN_REGISTERED 100.00 | reverses NULL | actor 1 | 2026-09-17 16:40:29.559 | reason "100"          unchanged
EVENT 35 RETURN_REVERSED   200.00 | reverses 29   | actor 1 | 2026-09-18 04:04:03.129 | reason "Actulizacion" appended
EVENT 36 RETURN_REVERSED   100.00 | reverses 30   | actor 1 | 2026-09-18 04:04:03.129 | reason "Actulizacion" appended
ORIGINALS_UNCHANGED=YES   REVERSALS=2, total 300.00, each equal to its original, on the original's row
ACTOR=user_account 1, a global UserAccount that exists - the account that created the Case and registered the returns
TIMESTAMP=server instant as stored (the database runs in UTC)   REASON=populated, the Owner's own text
ROWS 61 and 62: CONCILIADO / RECONCILED -> EN_CONCILIACION / PENDING, returned 0.00, adjustments 0.00, version 4
```

Duplicate reversal is refused twice over: the database holds `UNIQUE uq_set_balance_single_reversal
(reverses_balance_event_id)`, and `CaseRenditionService.reverseMovement` refuses a movement whose events already have a
reverso ("Este movimiento ya fue reversado.", proved through the API in STEP 27). The movement now reads `reversed=true`,
`canReverse=false`, so the product no longer offers Revertir on it.

The reverso wrote no `audit_logs` row, and that is the design: `settlement_balance_event` is the append-only audit ledger
of every movement and reverso (actor, instant, reason, the event it reverses), while `audit_logs` has no application
writer yet (ADR-0010 PROPOSED, a known debt). The reason stays as the Owner typed it - history is append-only; the
business context (no real cash return, both events recorded while testing the MVP) is in the STEP 28 prompt §4 and in
Reglas.md.

## 5. The Case after the reverso (§6, §7, §9)

| | Before | After |
|---|---|---|
| Total anticipos | 320.00 | 320.00 |
| Total gastos | 400.00 | 400.00 |
| Total a conciliar | 80.00 Por reembolsar | 80.00 Por reembolsar |
| Devuelto | 300.00 | 0.00 |
| Reembolsado | 0.00 | 0.00 |
| Pendiente | 380.00 Por reembolsar | 80.00 Por reembolsar |
| Usado | 400.00 | 400.00 |
| Uso | 125% | 125% |

Inputs: advances 106 (EN_RENDICION, 200), 107 (EN_RENDICION, 100) and 108 (ENTREGADO, 20) deliver 320.00; expenses
546-549 are APROBADO for 30 + 90 + 80 + 200 = 400.00; expense 545 stays RECHAZADO for 200.00 and weighs zero in Total
gastos, Usado, Devuelto, Reembolsado and Pendiente. Pendiente = 320 + 0 - 400 - 0 - 0 = -80, shown as 80.00 Por
reembolsar.

The card and the detail cannot disagree: `ExpenseCaseController` builds every list item with the same
`format(service.detail(...))` call as the detail endpoint, so both receive the same `financialSummary`, and Studio labels
it on the card (`summarizeCaseBalance`) and in the detail (`financialSummaryRows`) with the same helpers
(`baseReconciliationRow`, `differenceRows`, `adjustmentRows`). Uso is the card's metric, Usado / Total anticipos.

```text
CARD_DETAIL_NUMBERING_CONSISTENCY=YES   (same expenseSequence and caseNumber, same caseTitle; accepted by the Owner on screen)
CARD_DETAIL_FINANCIAL_CONSISTENCY=YES   (one server summary, the same label helpers)
```

## 6. Final action state (§8)

`CaseRenditionLedger` offers Registrar reembolso on an open Case with a delivered advance, a rendition that is not
CERRADO, a positive pending reimbursement and no authorized adjustment - all true here - with a ceiling of USD 80.00.
Nothing was registered (REIMBURSEMENT_TEST=DEFERRED): the Case legitimately stays Pendiente 80.00 Por reembolsar, the
real business position.

## 7. Narrow final smoke (§10) — `final-smoke-results.txt`, run by `final-smoke.sh`

```text
FINAL_SMOKE_CHECKS=29 FAILURES=0 WRITES=0
runtime   container unchanged since STEP 27; healthy; unauthenticated list and UUID route refused with 401; backend log
          since start: 0 ERROR lines, 0 exceptions
database  Flyway 65 / 0 failed; EXP. 08 and EXP. 09 with their IDs and business dates; the Owner tenant numbered 1..9,
          counter at 9; one currency; the eight financial values above; the rejected expense's zero effect; originals
          kept; reversals appended with actor, instant and reason; at most one reversal per original and the unique
          key; ledger equal to the rows; rendition reopened; Registrar reembolso conditions; no synthetic Case in the
          Owner tenant
```

The authenticated API checks - list, detail, expenseSequence, caseNumber, businessDate, the UUID route, tenant isolation
(404, the Owner Case included), the duplicate reverso refused (400) and 0 HTTP 5xx - ran in STEP 27 (27/27 and 12/12)
against this same container: created 2026-09-18T03:31:46Z, smoke at 03:32Z, the Owner's reverso at 04:04Z, 0 restarts
since. They are reused; no new synthetic account or tenant was created for this STEP. Both scripts are read-only: SQL
inside a READ ONLY transaction that is rolled back, HTTP probes without credentials.

## 8. Synthetic DEV data (§13) — the Owner decided KEEP

```text
SYNTHETIC_ACCOUNTS=19 (@example.test) in 18 tenants: STEP 18 deploy-smoke 3, s24-probe 2, s24-smoke 3, s24-rev 1,
  s27-smoke 2, s27-rev 1, and earlier QA (expense-fleet, fleet-ui, nav-qa, rbac-contador, rbac-verify, report-qa,
  ui-audit, 1 each)
DATA=26 Cases, 23 advances, 33 expenses, 13 balance events   SHARED_WITH_A_REAL_USER=0   IN_THE_OWNER_TENANT=0
CLEANUP_REQUIRED=NO   CLEANUP_PERFORMED=NO
```

## 9. The closure commit (§12, §15)

One local Fabric commit, staged by explicit path:

```text
STEP 27  its stored prompt and its evidence folder (record, smoke, reversal capability, artifact proof, migration log,
         backup and pre-flight), unchanged since STEP 27 apart from Git's line-ending normalization below
STEP 28  its stored prompt and this folder: this record, pre-reversal-state.txt, post-reversal-state.txt,
         final-smoke-results.txt, verify-owner-reversal.sh, final-smoke.sh
BASELINE Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_GM_EXPENSES_MVP_FROZEN_OWNER_ACCEPTED_2026-09-17.md
RULES    Reglas.md, append-only: the MVP freeze and the registration of its baseline (49 lines added, 0 changed)
POINTER  CURRENT_STEP.md, closed on this STEP
NOT STAGED  the 10 unrelated Fabric Knowledge paths; nothing in gm-expenses or Gystigo
```

Three STEP 27 files were written by PowerShell with CRLF; Git normalizes them to LF on staging (`text=auto eol=lf`),
which the canonical rule accepts:

```text
FILE=V65-SHARED-DEV-DEPLOYMENT-27-2026-09-17/artifact-proof.txt
  PRE_STAGE_WORKTREE_SHA256=e0ec382bf0b16b1209a3b7891b0df06f5bd39bf8e6e527ed8dccd3a9ea70c76d
  STAGED_BLOB_SHA256=7a5c6651103336656b00c6d339d6d51ae1386d0442c85932072e2d7939f848ff
  NORMALIZATION=CRLF_TO_LF
FILE=V65-SHARED-DEV-DEPLOYMENT-27-2026-09-17/reversal-capability-results.txt
  PRE_STAGE_WORKTREE_SHA256=1f200b5aab82f9bf6a64b2dd8a4dba9c37228932163d92a22734254af234882f
  STAGED_BLOB_SHA256=d1aa910664d9b64074df4bbcf91f0a8c844a56a706224321b65eb54a5377c8cf
  NORMALIZATION=CRLF_TO_LF
FILE=V65-SHARED-DEV-DEPLOYMENT-27-2026-09-17/smoke-results.txt
  PRE_STAGE_WORKTREE_SHA256=f4d8da2867a6b51fba386141846b893ce558b48d1b1b191fb7e0b48bd1c9f9cd
  STAGED_BLOB_SHA256=8088148505a0b2842bd50ed194604744736ce2869b1078e2ee12c3bd2121809b
  NORMALIZATION=CRLF_TO_LF
```

Before staging, every file of the commit was scanned for credential patterns (0 matches). The two promoted migration
logs, STEP 24's and STEP 27's, carry Spring's development-password notice without the password line: 0 UUID-shaped
tokens in either.

## 10. For the Owner - found while closing, not changed here

```text
BACKUPS  the Shared DEV backups (pre-V64 0f5fbd0e..., pre-V65 ffd4abb7..., both hashed again and unchanged) live under
         %LOCALAPPDATA%\Temp\gypport\shared-dev-backups, outside every repository. The placement rule sends raw dumps to
         GYPPORT_STORAGE, and a dump of Shared DEV holds accounts and personal data, so Restricted/ is its area; the
         move is the Owner's decision
STEP_18  Shared DEV V43 -> V63 has no stored prompt or evidence folder in Fabric; its outputs are still in the session
         scratchpad (s18) and its facts survive in the STEP 19 prompt and the 20A and 22B records
HOST     Spring's UserDetailsServiceAutoConfiguration prints a generated development password at every Host start -
         platform security configuration to settle before production, outside this MVP
```

## 11. Not done

```text
PUSH_PERFORMED=NO   REIMBURSEMENT_REGISTERED=NO   SOURCE_CODE_CHANGED=NO   SQL_WRITES=0   DATA_CLEANUP=NO
NEW_SYNTHETIC_TENANTS=0   HISTORICAL_EVIDENCE_ALTERED=NO
```

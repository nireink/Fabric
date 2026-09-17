# GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10 — evidence

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10.md
DATE=2026-09-16 (local, UTC-5); run 2026-09-17T02:48Z-03:05Z
STATUS=READY_FOR_OWNER_CLOSED_BAR_AND_MULTIPLE_ADVANCE_REVIEW
COMMIT_STATUS=NONE
PUSH_STATUS=NONE
SHARED_DEV_STATUS=V43, not modified (read-only Flyway query only)
REPOSITORY_HEADS=Gystigo d9f3dde; Modules/gm-expenses ab74610; Fabric 70fd250 (uncommitted work on top)
```

## Owner decisions applied

```text
CLOSED_CASE_MAIN_BAR=Conciliado (100% with nothing pending)
OPEN_CASE_MAIN_BAR=Uso (used / delivered)
USAGE_ON_CLOSED_CASE=plain figure, no bar
MULTIPLE_ADVANCES_PER_CASE=VALID in any number and currency
SUPERSEDED=GM_EXPENSES_ONE_ACTIVE_ADVANCE_PER_CASE_CURRENCY_06 invariant, its two refusals and its legacy-draft rule
DRAFT_BLOCKS=closing the Case only
FIFO_AS_BUSINESS_POLICY=NO (delivery-order sharing only lets each rendition reconcile)
```

## Changes

```text
gm-expenses main    OneActiveAdvancePerCaseCurrency deleted (untracked S06 file); its calls removed from
                    ExpenseCaseService.createAdvance and CaseAdvanceDeliveryService.deliver; AdvanceStatus restored
                    to HEAD (financiallyActive removed); CaseJustifiedTotalAllocation / CaseRenditionService comments
gm-expenses tests   OneActiveAdvancePerCaseCurrencyTest deleted; AdvanceStatusTest restored to HEAD;
                    CaseAdvanceDeliveryServiceTest: every draft of a Case is delivered beside its other advances
Host tests          ExpenseCaseHttpApiTest: several advances in any currency, only drafts block the close; delivered
                    tranches reconcile and the Case keeps taking advances; tenant isolation; unplanned draft in the
                    same Case; SQL helper moveAdvanceIntoCase removed
Studio              caseRules.caseCardProgress + row.settled; ExpenseCaseCard: one bar (Uso open / Conciliado closed),
                    plain Uso on closed cards; CSS .expense-case-card__progress and closed-row layout
Studio contracts    ExpenseCaseCard (A open, B closed, C Viaje Loja, no invented progress), ExpenseCases
                    (caseCardProgress), AdvanceRenditionFlow (D several advances offered and registered, E no refusal text)
Fixtures            UIX fixture no longer refuses a second advance; card fixture adds the Owner's open/closed 300/260 example
Fabric              domain baseline §3 (several advances, supersession note), RN-001 note, card progress bar rule;
                    Reglas.md +1 superseding entry; CURRENT_STEP.md via Set-GypportCurrentStep.ps1; STEP prompt stored
```

No migration, no Host main change, no change to delivered, used, justified, returned, reimbursed or pending
amounts, and no change to the V63 equation.

## Verification

```text
gm-expenses module (install)         740/740 (748 - 9 S06 tests + 1), jar 8AE3DF47FB9F3D551774352C536916376480BD665950E79CDD67072309E3944E
Host expenses real-DB runner         98/98 (99 - 5 S06 tests + 4), flywayMax 63, delete guards 17, canonical categories 8,
                                     container and evidence disposed (s10-host-realdb-result.json)
Host jar                             325D716A927262565DC7A6DC294FB745E48281E3B8DFC12B5B958E923A082B99, nested gm-expenses = installed jar,
                                     0 OneActiveAdvancePerCaseCurrency classes, highest migration V63, 0 migration files changed
Studio affected contracts            116/116 (5 suites)
Studio full contracts                625/625 (53 files)
ESLint (changed shell files)         0 problems
Local runtime redeploy               127.0.0.1:8080 PID 40008, jar 325d716a9272, Flyway validated, no migration (3310 at V63)
Live smoke (synthetic account)       6/6: four USD tranches (30000, 2000, 300, 5000) and one EUR tranche registered; drafts
                                     delivered beside drafts and delivered advances; no refusal text; drafts block the close
                                     with "El expediente tiene anticipos en borrador; confirma su entrega o cancélalos."
                                     A first run reported F as FAIL only because the BOM-less script mis-decoded "cancélalos";
                                     the backend already answered 400 with the exact message. Saved with a BOM, 6/6.
Access log / backend log             0 5xx; 0 ERROR lines
Card fixture 1024px                  Viaje Loja and Viaje Guayaquil (closed): Conciliado 100% full bar, Uso 29% / 87% plain;
                                     Compra repuestos (open): Uso 87% bar; closed without advance: Conciliado 100%, Uso —
Card fixture 375px                   no horizontal overflow, 0 clipped cells; closed rows Entregado|Usado, Justificado|Conciliado,
                                     Devuelto|Reembolsado, Pendiente de conciliar|Uso
UIX fixture                          c8 (already two advances): a third advance of USD 5000 registered and delivered without
                                     refusal; Case summary net Por justificar o devolver 4980, each advance its own direction;
                                     console only the harness /auth/me 401s
```

```text
VERIFIED_BASELINE_CHECK
PKG2D_BASELINE=REUSE (accepted commits are ancestors of HEAD; no identity or membership path touched)
REHEARSAL_03=PARTIAL_INVALIDATION: runtime check 4 (one-active-advance refusal) is superseded by this Owner decision;
             the migration evidence stays valid (V44..V63 files unchanged, no migration added)
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

## Open Owner decision

§10 C expects "No delivered Advance: Uso 0%, bar empty". The accepted STEP 20 FINAL contract
(USAGE_NOT_APPLICABLE) shows "—" with an empty inactive capsule and never an invented 0%, because such a
Case can still have used money (e.g. Usado USD 18.75 with nothing delivered). The presentation was left
unchanged pending the Owner's choice.

## Sensitivity check before promotion

```text
SECRET_SCAN=PASS for the promoted files
WITHHELD=s10-host-realdb.log (76,828 bytes, SHA-256 95c3f9be0ee6979bd3cbd1efb952ceb78b560db2c48c0f89052869fba79d39d1):
         it prints 4 Spring Boot "generated security password" lines of disposable test contexts. Its structured
         result is promoted instead (s10-host-realdb-result.json).
SYNTHETIC_DATA=two runtime-smoke-s10-*@example.test accounts and their Cases in the isolated copy 3310 (TEST_DATA)
```

## Manifest (byte-exact copies)

| File | Bytes | SHA-256 |
|---|---:|---|
| s10-runtime-smoke.ps1 | 7548 | 6626c1a9f973b7696be72f75767fafbabb5236ec3e2f6741611e5ead679111e7 |
| s10-runtime-smoke-results.txt | 837 | b439d50c220fe4c2166a6eaf9031185e032692dae953ed76cbdc6835c04c43f8 |
| s10-module-install.log | 23537 | d05b95563854aaaf8bdb39c3f07d6236cde7c16280eb9e12214da78484038c5a |
| s10-host-package.log | 2459 | 613f6cfb655e4761f58e5231e6b184da4ae1bacbdb58d143cd89f20d928aec05 |
| s10-host-realdb-result.json | 1691 | a7bd06a7d3dc28537a5d173030dc4d65cc18786939a47870fa80b7cb294eefcb |

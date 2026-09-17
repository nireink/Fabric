# GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11 — evidence

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11.md
DATE=2026-09-16 (local, UTC-5); run 2026-09-17T03:20Z-04:20Z
STATUS=READY_FOR_OWNER_CASE_LEVEL_RENDITION_REVIEW
COMMIT_STATUS=NONE
PUSH_STATUS=NONE
SHARED_DEV_STATUS=V43, not modified (read-only SELECT queries only)
REPOSITORY_HEADS=Gystigo d9f3dde; Modules/gm-expenses ab74610; Fabric 70fd250 (uncommitted work on top)
```

## Owner decisions applied

```text
ZERO_USAGE_OPTION=B_0_PERCENT (numeric zeros, Uso 0%, empty bar with a visible track)
CANONICAL_MODEL=ExpenseCase = funding and rendition center; advances = funding tranches; expenses belong to the Case
CASE_EQUATION=caseBalance = delivered + reimbursed - justified - returned - adjustments
FIFO_AUTHORITATIVE=NO
PER_ADVANCE_JUSTIFIED_ALLOCATION=not business truth, never exposed
RETURN_REIMBURSEMENT_CONCILIAR=Case commands per currency
DRAFT_BLOCKER_COPY=Hay 1 anticipo en borrador por USD X.XX... / Hay N anticipos en borrador por un total de USD X.XX...
ADVANCE_PAGE=Rendición: Se gestiona desde el expediente
MIGRATION=NONE (V62 and V63 unchanged)
```

## Audit (read-only, before implementation)

```text
advance_settlement            1:1 with an advance (uq_settlement_advance); V63 chk_settlement_reconciled_equation holds every
                              RECONCILED row to advance + reimbursed = justified + returned + adjustments; no-delete trigger
settlement_balance_event      append-only ledger per settlement row
settlement_adjustment_event   no application caller; 0 rows
expense_review_event          settlement_id always NULL
FIFO entry point              CaseJustifiedTotalAllocation (delivery-order sharing) used by JdbcApprovedExpenseTotalQueryPort,
                              ExpenseCaseService.financialSummary and JdbcExpenseReportPort
per-advance commands          CaseRenditionService addressed one advanceId; per-advance endpoints on the Case and the Advance
closure                       ExpenseCaseService.close -> CloseSettlementUseCase per CONCILIADO row (row CERRADO, advance RENDIDO -> CERRADO)
SCHEMA_CHANGE_NEEDED          NO: the Case totals are sums over existing rows; each row can be reconciled on the money it holds
```

## Design (no new table, no V64)

```text
CaseRenditionLedger (new)     per Case and currency: delivered = delivered advances, justified = APROBADO Case expenses (0 before a
                              delivery), movements = sums of the rows, balance, derived status (SIN_INICIAR / ABIERTO / CONCILIADO /
                              CERRADO), version token (sum of row versions + delivered count), commands admitted now
CaseRenditionService          registerReturn / registerReimbursement / reconcile on the Case (expectedRenditionVersion); every refusal
                              before any write; first command opens missing rows (OpenSettlementUseCase); return stored on the rows
                              holding most money (split when needed), reimbursement on the largest tranche's row, one balance event per
                              stored part; Conciliar only when the Case balances, sets each open row's justified total to the money it
                              holds; requireOutsideCase guards the per-advance settlement API
ApprovedExpenseTotalQueryPort zero for a Case advance: an approval resets a Case row, which reopens a reconciled Case
ExpenseCaseService            Detail.renditions and financialSummary from the ledger; close order: expenses, documents, drafts (Owner
                              copy), observed advances, unbalanced Case, not reconciled; closes every open row and every advance
Reports                       justified = APROBADO per Case with delivered money; directions per Case before adding up
FIFO compatibility code       NONE remains (CaseJustifiedTotalAllocation deleted); legacy CERRADO rows keep frozen totals
```

## Changes

```text
gm-expenses main    AdvanceSettlement (heldAmount, carryCaseReturn, carryCaseReimbursement); CaseRenditionLedger (new);
                    CaseRenditionService (rewritten); ExpenseCaseService; JdbcApprovedExpenseTotalQueryPort; JdbcExpenseReportPort;
                    Javadoc of ApprovedExpenseTotalQueryPort, SettlementJustifiedTotals, ExpenseCaseFinancialSummary;
                    CaseJustifiedTotalAllocation deleted (untracked earlier WIP)
gm-expenses tests   CaseRenditionServiceTest (new, §17 1-12 incl. §13/§14); AdvanceSettlementTest +4; SettlementJustifiedTotalRefreshTest;
                    InMemoryApprovedExpenseTotals; JdbcExpenseReportPortFundingTest; CaseJustifiedTotalAllocationTest and
                    CaseRenditionViewTest deleted (untracked earlier WIP)
Host main           ExpenseCaseConfig; ExpenseCaseController (POST /{case}/rendition/returns|reimbursements|reconcile, JSON renditions[],
                    per-advance rendition endpoints and renditionSummary removed); ExpensesResponseFormatting.caseRendition;
                    ExpenseAdvanceController (renditionManagedByCase, no rendition); AdvanceSettlementController (Case advances refused)
Host tests          ExpenseCaseHttpApiTest (Case-level scenarios incl. §13, §14, legacy refusal, tenant isolation); ExpenseCasePermissionTest;
                    GmExpensesHttpApiTest
Studio              expenseService (Case endpoints); renditionRules; caseClosureRules (expenses -> drafts -> rendition, draftsMessage);
                    ExpenseCaseDetailPage (one Resumen financiero per currency with Case actions); ExpenseCases.css; caseRules
                    (option B zeros, Uso 0%); AdvanceDetailPage(+css) (Rendición: Se gestiona desde el expediente)
Studio contracts    AdvanceRenditionFlow (§18 A-D, I; B/C source checks); ExpenseCaseCard (G option B, H 110%); ExpenseCases;
                    ExpenseOperationIdBoundary; ExpensesUixCompliance
Fixtures            UIX harness simulates the Case-level rendition (c9 option B); card fixture adds the option B and 110% cards
Fabric              domain baseline (§3, §5 Case-level rendition, vocabulary, progress bar); Reglas.md +1 superseding entry;
                    CURRENT_STEP.md via Set-GypportCurrentStep.ps1; STEP prompt stored verbatim
```

## Verification

```text
gm-expenses module (install)          748/748, jar 1C6FEF03720249E9FBA6D4B8F7D89FA46E4F7671D81FE9750E7B10B57330AB8D (s11-module-install.log)
Host expenses real-DB runner          99/99, flywayMax 63, delete guards 17, canonical categories 8, container and evidence disposed
                                      (s11-host-realdb-result.json); raw log withheld (it prints generated security passwords)
Host permission unit test             6/6 (s11-host-permission-unit.log)
Host jar                              ECD17C12F8AF6EEC4B442B79D0391E01B3E9B237D9C596D09971834EFF43D234; nested gm-expenses = installed jar
Migration bytes                       64/64 SQL entries byte-identical to the REHEARSAL_03 jar CC028B886C4D (V62 D805797CC90A4489...,
                                      V63 6DB2EACC9842D948...)
Studio full contracts                 628/628 (53 files) (s11-studio-contracts.log)
ESLint (changed shell files)          0 problems
UIX harness (5188)                    Owner's two-advance record: reimburse 20 -> Conciliar -> Cerrar expediente closes both advances;
                                      c9 option B zeros and draft blocker copy; a1 reads Rendición: Se gestiona desde el expediente;
                                      console errors = the harness's known /auth/me 401s only
Card fixture (5189)                   option B card (USD 0.00 ..., Uso 0%, empty non-inactive capsule), Uso 110% (fill 100%);
                                      375px: document width 375, no card overflow
Local runtime redeploy                backend PID 47916, jar ecd17c12f8af, isolated copy 127.0.0.1:3310 at V63 (no migration)
Live runtime smoke                    16/16 (s11-runtime-smoke-results.txt): §13 end to end, §10 close order, §8 per-advance API refused,
                                      §7 advance JSON, §11 draft copy, §14 additional advance, §15 +30/-20 per Case, §17.12 isolation
Stored rows of the §13 Case           4 rows CERRADO, justified 35000, returned 2300, 0 unbalanced rows, 1 balance event
Access log                            0 5xx; 19 /rendition/ requests
Legacy impact (read only)             s11-legacy-impact-results.txt: 0 approved expenses leave their Case; 0 closed Cases change
```

## Findings and open points

```text
FACT                       Shared DEV holds 1 open Case rendition row with a per-advance justified total (legacy); it is a
                           technical carrier now and is reset by an approval or overwritten by Conciliar. Not repaired.
FACT                       Legacy CERRADO rows with open advances keep blocking the close with the regularization message.
OWNER_DECISION_REQUIRED    Reports keep "No aplica" for a Case without a delivered advance, while the card and the Case
                           detail read zeros (option B). Presentation only; no code path depends on it.
INFERENCE                  A Case row reconciled before STEP 11 (per-advance FIFO totals) and already CONCILIADO closes as it is
                           when its Case balances; its frozen row totals are non-authoritative.
PRE_EXISTING_DEBT          ERROR_DISPATCH_404_MASKED_AS_401 (deferred); UIX harness /auth/me 401 noise.
NEW_REGRESSION             none found
REHEARSAL_03               business smoke invalidated by this STEP; migration evidence reusable (bytes identical);
                           GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 required after Owner acceptance.
```

## Continuity packet

```text
STEP=GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11
PHASE=CASE_LEVEL_RENDITION_CANONICALIZATION
STATUS=READY_FOR_OWNER_CASE_LEVEL_RENDITION_REVIEW
REPOSITORY_HEADS=Gystigo d9f3dde; Modules/gm-expenses ab74610; Fabric 70fd250
WORKING_TREE_STATE=uncommitted; FILES_STAGED=0
UNRELATED_WIP=earlier gm-expenses release-readiness STEPs (uncommitted, preserved)
LAST_VERIFIED_RESULT=module 748/748, Host real-DB 99/99, Studio 628/628, runtime smoke 16/16
OWNER_DECISIONS_APPLIED=option B zero usage; Case-level rendition; FIFO not canonical; Case commands; draft copy
OPEN_CONFLICTS=none
NEXT_EXACT_ACTION=STOP for Owner review; after acceptance GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 on a disposable Shared DEV copy
COMMIT_STATUS=NONE
PUSH_STATUS=NONE
SHARED_DEV_STATUS=V43, untouched
```

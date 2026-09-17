# GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 — evidence

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12.md
DATE=2026-09-17; run 2026-09-17T08:30Z-09:30Z
STATUS=READY_FOR_OWNER_FINAL_RUNTIME_REHEARSAL_REVIEW
ACCEPTED_BEFORE_THIS_STEP=GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11
COMMIT_STATUS=NONE (FILES_STAGED=0)
PUSH_STATUS=NONE
SHARED_DEV_STATUS=V43, not modified (SELECT, metadata queries and one mysqldump --single-transaction only)
REPOSITORY_HEADS=Gystigo d9f3dde; Modules/gm-expenses ab74610; Fabric 70fd250 (uncommitted work on top)
```

## 1. Owner decision applied: report zero state

Reports use the numeric zero vocabulary of the Case card and detail. Without a delivered advance the funding fields
read USD 0.00, never "No aplica" or "—", and Usado keeps the real expense amount. Presentation only.

```text
Studio        reportRules.summarizePeriodFunding / relatedFundingLine: numbers only; ExpenseReportsPage renders formatMoney
Contract      ExpenseReportHome: REPORT_NO_DELIVERED_ADVANCE_NUMERIC_ZEROS, empty period zeros, related Cases line
UIX harness   scenario "Sin anticipo entregado" (backend-shaped zero payload)
Fabric        domain baseline §5 zero-state rule and vocabulary; Reglas.md +1 superseding entry (prefix cmp OK)
Studio tests  628/628 contracts (53 files); ESLint clean
```

## 2. Source (Shared DEV, read only)

```text
SERVER            mysql 8.4.10, default flags (log_bin_trust_function_creators=0), utf8mb4_0900_ai_ci
DEV BACKEND USER  root (the official DEV backend migrates as root) -> the rehearsal mirrors root and default flags
FLYWAY            max=43 history_rows=27 failed=0
TABLES / ROWS     102 / 3,192 (f12-dev-counts.txt)
TRIGGERS          29, definer root@% (f12-dev-triggers.txt, SHA-256 of each statement)
ROUTINES          0
VS REHEARSAL_03   per-table counts identical 102/102; gm-expenses content CRC identical 19/19 -> no relevant change
```

## 3. Fresh disposable copy

```text
CONTAINER         gypport-rehearsal-final12-b61a7e05 (mysql:8.4.10, label gypport.rehearsal), 127.0.0.1:3314, db gypport_rehearsal_final12
COPY              mysqldump --single-transaction --routines --triggers --events --hex-blob --no-tablespaces --set-gtid-purged=OFF,
                  piped straight into the copy as its root (no dump file on disk), 8 s, no errors
EQUALITY          flyway, per-table counts, trigger definitions, routines, column definitions, gm-expenses CRC: all identical
SHARED DEV AFTER  re-fingerprinted: counts and CRC unchanged, Flyway 43
```

## 4. Build of the current working tree

```text
gm-expenses       748/748 tests; jar 1C6FEF03720249E9FBA6D4B8F7D89FA46E4F7671D81FE9750E7B10B57330AB8D (content unchanged since STEP 11,
                  built 2026-09-17T03:55:20Z; ~/.m2 = target)
Host jar          F4A5509405EAC47F38017C75C38FC0D1D2735CC3E2DC9B07E0BE0795177C2996 (built 2026-09-17T08:35:45Z);
                  532/532 entries content-identical to the accepted STEP 11 jar ECD17C12 (zip timestamps only)
Nested module     BOOT-INF/lib/gm-expenses-0.1.0-SNAPSHOT.jar = module jar
Migrations        highest V63, none beyond; 64 SQL entries byte-identical to the REHEARSAL_03 jar CC028B88
Packaged proof    CaseRenditionService and CaseRenditionLedger present; CaseJustifiedTotalAllocation 0; FIFO references 0;
                  OneActiveAdvancePerCaseCurrency 0 and no "anticipo activo" copy; endpoints /{reference}/rendition/returns,
                  /reimbursements, /reconcile and /close present, per-advance rendition path absent; per-advance settlement API
                  guarded (requireOutsideCase); renditionManagedByCase; V62 AdvanceDeliveryPlan + plan-is-fixed copy; V63
                  SettlementBalance + chk_settlement_reconciled_equation; draft, unbalanced and not-reconciled close copy
                  (f12-jar-proof.txt)
```

## 5. Migration V43 -> V63

```text
BACKEND           127.0.0.1:18084, SPRING_* stripped, root of the copy, Flyway enabled
FLYWAY            43 -> 63, 20 migrations in 7.7 s, 0 failed; history 47 rows; nothing beyond V63
WARNINGS          guarded DROP PROCEDURE IF EXISTS notes and one integer display width deprecation note only
TABLES / ROWS     102 -> 107 (none missing; added: user_tenant_memberships 11, user_tenant_membership_events 11,
                  tax_subjects 0, mdm_identity_intakes 0, mdm_identity_intake_identifiers 0); 3,192 -> 3,234
                  only flyway_schema_history changed among existing tables; 0 business tables lost rows
GM-EXPENSES       19/19 tables content-identical to Shared DEV over shared columns (no silent rewrite)
TRIGGERS          29 unchanged + 3 new membership guards; 0 routines left
INVARIANTS        17 delete guards, 8 canonical categories
V61               origin columns 2, old columns 0, origin FKs 3, old FKs 0, identity pair check 1, retired key 0,
                  11 accounts, 0 without membership
V62               planned columns 2, planned checks 3, 0 existing rows with a plan
V63               return/reimbursement exclusivity 0, reconciled equation 1, shortfall-only 1, 10 settlement checks,
                  0 reconciled rows violating the equation
LEGACY LINKS      0 ambiguous
```

## 6. Final runtime smoke (33/33, f12-runtime-smoke-results.txt)

```text
§9  Construcción       30000 + 2000 + 300 + 5000 in USD, all allowed and delivered; delivered 37300, justified 35000,
                       return 2300, Conciliar, Cerrar expediente: Case and 4 advances CERRADO
§10 additional advance 30000 / 29500 -> +2000 delivered -> 32000; justified 29500; 2500 to return; older view 409; 0 rows created
§11 V63                real return 20, later approval 20 accepted, Case-level reimbursement 20, Conciliar, close; returned 20 +
                       reimbursed 20 persisted
§12 drafts             two drafts beside a delivered advance; plural copy; cancel -> singular copy; delivery beside the
                       others; blocker gone (next: saldo pendiente); balanced, reconciled, closed
§13 expenses           REGISTRADO -> PENDIENTE_REVISION -> APROBADO; OBSERVADO -> correction -> PENDIENTE_REVISION -> APROBADO
                       (SUBMITTED, OBSERVED, CORRECTION_SUBMITTED, ACCEPTED); RECHAZADO terminal (accept 400, correction 400);
                       justified 115 (APROBADO only), Usado 135
§14 blockers           A REGISTRADO, B PENDIENTE_REVISION, C OBSERVADO, D BORRADOR, E balance != 0, F not reconciled; then close OK
§15 presentation data  closed 679 / 200 / 200 / 499 / 20 / 0 (Uso 29%); open overuse 1000 / 1100 (Uso 110%, 100 to reimburse)
§16 zero advance       own tenant: Usado 260, every funding amount 0, no rendition; period summary and related Cases numeric
§17 reports            period summary = per-Case sums (delivered 71729, used 66420, justified 66405, returned 2954,
                       reimbursed 40, pendingReturn 2530, pendingReimbursement 120, never netted); categories, query with
                       related Cases (2530/120), vehicle totals, resources: 200
§18 advance detail     history kept, renditionManagedByCase=true, no justified/returned/reimbursed/pending fields
§19 isolation          tenant B: 404 on case, advance, expense, return, reimbursement, reconcile, close, add advance, add
                       expense, cancel, submit; empty lists and reports
§21 legacy API         2 deliberate probes refused with "La rendición de este anticipo se gestiona desde su expediente."
```

Stored rows after the smoke (f12-rows-check-results.txt): Construcción 4 rows CERRADO, justified 35000, returned 2300, 0 unbalanced
rows, 1 balance event; Tramo adicional 0 rows; 0 reconciled rows violating V63; Flyway 63, 0 failed.

Access log (f12-access-log-summary.txt): 279 requests, 0 5xx; 200 x199, 201 x53, 400 x14 (expected refusals), 404 x11
(isolation), 409 x1 (stale view), 401 x1 (readiness probe /auth/me); 21 Case rendition calls; 2 legacy settlement calls =
the 2 deliberate probes.

## 7. Studio against the rehearsal data

```text
OLD SETTLEMENT CALLS  Studio src: 0 references to /api/settlements or advance settlement; writes only to
                      /api/expense-cases/{id}/rendition/returns|reimbursements|reconcile (ExpenseCaseDetailPage);
                      UIX harness network: 0 settlement requests
CARDS (real payload)  the production card rendering the rehearsal list (f12-card-payload.json):
                      Viaje Loja (ensayo final) 679 / 200 / 200 / Conciliado 100% / 499 / 20 / Pendiente de conciliar 0.00 / Uso 29%;
                      Sobreuso Uso 110% (fill 100%); Construcción Conciliado 100%, Uso 94%;
                      Sin anticipo entregado USD 0.00 x5 + Usado 260.00, Uso 0% on an empty visible track
REPORTS (real payload) zero tenant period summary (f12-zero-tenant-period-summary.json): Dinero entregado USD 0.00, Dinero usado
                      USD 260.00, Justificado / Devuelto / Reembolsado / Pendiente de conciliar USD 0.00; related Cases line
                      numeric; no "No aplica", no "—"
RESPONSIVE            cards desktop / 375 / 320: no overflow, Uso visible; Case detail with two advances and the closure blocker
                      375 / 320: no overflow inside Expenses, blocker readable; reports 320: content fits
CONSOLE               only localhost:8080/auth/me failures from the fixture header (the known 401 normally; connection refused
                      while the Owner runtime was down); no application errors
```

## 8. Legacy Shared DEV data (read only, not repaired; f12-dev-legacy.txt)

```text
INCONSISTENT          1 OBSERVADO expense without an OBSERVED event (tenant 1, no Case, 5E63494A...)
INCONSISTENT          3 CERRADO settlements whose advances are EN_RENDICION (tenant 1, Case 0BA391C4...): that Case cannot close
                      until regularized ("requiere regularización antes de cerrar el expediente")
OPEN WORK             16 BORRADOR advances: tenant 1 3 standalone (2026-08-31) + 10 in Case 2075C587 (2026-09-15/16);
                      tenant 4 1 (2026-08-31); tenant 70 2 (2026-09-03)
LEGACY SHAPES         3 advances outside any Case (the 3 tenant-1 drafts); 0 legacy-link-only advances; 4 expenses without a
                      Case (tenant 1 APROBADO 1 + OBSERVADO 1; tenant 4 REGISTRADO 2)
VALID                 4 Cases with more than one advance in USD (tenant 1 x3, tenant 70 x1): not a defect
TECHNICAL CARRIER     1 open rendition row with a per-advance justified total (tenant 33, CON_DIFERENCIA): not business truth
CASE-LEVEL IMPACT     0 approved expenses outside their Case; 0 closed Cases whose justified total changes
TENANTS               1 REAL_DEV_DATA; 4 and 387 TEST_DATA; 33 and 70 UNKNOWN (not classified, not cleaned)
```

## 9. Environment

```text
CLEANUP               rehearsal backend stopped; container and its volume removed; ports 18084 and 3314 free; backend workdir
                      (logs with the generated security password) deleted; no dump file was written
OWNER RUNTIME         found the 8080 backend stopped (its log ends 2026-09-17T04:10:12Z without a shutdown: the previous
                      session ended); restarted detached (WMI) with the same accepted jar ecd17c12f8af, PID 10352, schema
                      V63 up to date; 3310 MySQL, Mailpit and the Owner's Vite untouched
NOT PROMOTED          raw backend logs, raw access log, any dump, passwords, cookies, tokens
```

## Findings

```text
FACT                     The rehearsal mirrors the real migration conditions: current Shared DEV bytes, root, default flags.
PRE_EXISTING_DEBT        Studio shell topbar reaches 336px at a 320px viewport in the full app harness (layout files unchanged
                         since 59bd77f); Expenses content fits. ERROR_DISPATCH_404_MASKED_AS_401 (deferred).
OWNER_DECISION_REQUIRED  Regularization of the 2 inconsistent legacy shapes above (separate Owner STEP); tenants 33 and 70.
NEW_REGRESSION           none found
READY_FOR_CONTROLLED_COMMIT_GATE=YES
READY_FOR_SHARED_DEV_MIGRATION_AFTER_COMMIT=YES (fresh backup, backend built from the accepted commit, migrate as root with
                         default flags as rehearsed, per handoffs/SHARED_DEV_MIGRATION_V43_V63_PLAN_2026-09-16.md)
```

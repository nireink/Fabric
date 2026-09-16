# GM_EXPENSES_VEHICLE_HTTP_CONTRACT_RECONCILIATION_18

TRACK=GYPPORT-MVP-GENERAL-01
MODE=TARGETED_CONTRACT_REPAIR
STATUS=COMPLETED
RECOMMENDED_GM_EXPENSES_BASELINE_STATUS=READY_TO_FREEZE
EVIDENCE_STATE=IMPLEMENTED_AND_TESTED; independent audit not asserted

## Authority and starting state

The attached STEP 18 Owner decision accepts STEP 17 isolation and authorizes bounded
reconciliation with Case-driven vehicle semantics. It explicitly forbids direct Expense
vehicle overrides and tenant/organization-wide fallback. The existing production contract
already implements that decision; this change repairs tests only.

Gystigo branch: `feature/gm-fleets-minimum-vehicle-master-01`.
Starting HEAD: `40c49f631c1d27be198ce0c4eb1892fa3eaa1909` (STEP 17 isolation).
Modules/gm-expenses: `master`, `049c74adda2b774841ddb931176be8e7785f847f`, clean.
Authoritative checkouts are under `D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT`.
Unrelated pre-existing Studio/design-system changes and seven untracked files are protected.
No independent STEP 18 audit is asserted by this implementation report.

## Seven original failures: classification before edits

Every original failure is STALE_TEST_FIXTURE. No production or isolation bug was confirmed.

| Failure | Original test | Root cause |
|---|---|---|
| 01 | canonicalPersonsAreCreatedOnceReusedAndDeliveryActorsAreSeparated | Sent fleetVehicleReference despite an already associated Case vehicle. |
| 02 | multipleVehiclesExplicitChoiceAndRemovalPreserveHistoricalSnapshot | Tried to choose a vehicle per Expense with two active Case resources; current contract requires unambiguous Case context. |
| 03 | vehicleCaseFoodWithoutVehicleFuelSnapshotAndIdempotency | Expected 400 for an Expense without an override, although caseBody explicitly included resources(vehicle). The actual 201 was correct Case derivation. |
| 04 | vehicleCategoriesRequireFleetSelectionAndPreserveSnapshot: COMBUSTIBLE | Stale direct override after associating the Case vehicle. |
| 05 | Same parameterized test: PEAJE | Same stale override. |
| 06 | Same parameterized test: PARQUEADERO | Same stale override. |
| 07 | Same parameterized test: MANTENIMIENTO | Same stale override. |

The STEP 18 prompt's tentative description of failure 03 as a Case without a vehicle is
not borne out by disk evidence: the original test created it with a VEHICLE resource.
No global unique-vehicle fallback was removed because none exists on this command path.

## Production trace (read-only)

- Host `ExpenseCaseController.addExpense` accepts only operationId, categoryScope,
  categoryCode, amount, currency, expenseDate and description. AddExpenseCommand has no
  vehicle override. Unknown fields receive the existing human-safe validation response.
- Module `ExpenseCaseService.addExpense` reads the category's requiresVehicle policy.
  For vehicle categories it filters this Case's resources by active and VEHICLE, requiring
  exactly one. Missing or ambiguous resources produce the existing message:
  "Este gasto necesita un vehículo. Asocia primero un vehículo al expediente."
- `JdbcExpenseCaseRepository.resources` constrains by tenant, organization scope and Case
  UUID. It does not search other Cases or choose a global available vehicle.
- `RegisterExpenseUseCase` receives the derived reference and calls ExpenseVehicleResolver
  only when that explicit reference is present. It captures plate/description in the
  expense snapshot and persists a new vehicle reference through existing composition.
- Host `FleetExpenseVehicleResolver` finds the exact derived Fleet identifier in the
  authorized tenant. It does not choose the first/only Fleet vehicle. It captures a new
  immutable reference. `FleetVehicleLabel.brandAndModel` formats the existing KIA/RIO
  fixture as KIA RIO; old later assertions expecting only KIA were also stale.
- gm-expenses POM has no gm-fleets dependency. No production source, port, FK, schema,
  migration, catalog rule, Fleet selector or snapshot implementation changed.

## Test reconciliation

Only ExpenseCaseHttpApiTest.java and ExpenseFleetHttpApiTest.java are edited.

Normal expense builders no longer accept a vehicle argument or emit fleetVehicleReference.
The field remains only in deliberate rejection requests, including an override matching
the associated vehicle. Valid fixtures associate vehicles via canonical Case resources.

The multi-resource scenario still rejects ambiguity and duplicate association. It now
resolves ambiguity by deactivating the first resource at the Case, captures the second,
creates another Case using the first vehicle, verifies each Expense's own plate, then
removes the remaining resource and proves both safe rejection and preserved historical
snapshot. A vehicle active in another Case does not supply missing context.

The four vehicle-required parameter cases explicitly prove that one available tenant
vehicle with no Case association is rejected with the exact human-safe message and no
Expense row. After association, the same category succeeds without an override; retry
idempotency and immutable snapshots remain covered. Existing cross-tenant resource
rejection scenarios are preserved.

COMISIONES is added to the existing non-vehicle parameterized scenario alongside
ALIMENTACION/HOSPEDAJE/OTRO. Existing GmExpensesHttpApiTest coverage creates a custom
non-vehicle TENANT category and registers it in a Case without vehicle resources, so no
duplicate custom-category test is introduced. The expected full suite count is 74 (one
additional parameter case); none of the original test scenarios is disabled.

## Validation

All requested implementation completion gates passed. The STEP 17 isolation files are
unchanged, as are production source, migrations and the gm-expenses module checkout.

| Fresh suite | Tests | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
| gm-expenses unit suite | 677 | 0 | 0 | 0 |
| Gystigo unflagged suite | 356 | 0 | 0 | 119 |
| Isolated full run 1 | 74 | 0 | 0 | 0 |
| Isolated full run 2 | 74 | 0 | 0 | 0 |
| Guard suite, executed in each full run | 15 | 0 | 0 | 0 |

Each full run consists of Case HTTP 11, Fleet HTTP 9, guard 15, Host integration 11 and
Expenses HTTP 28. All seven original failures are resolved. Unflagged executes 237 tests
successfully and skips 119 opt-in tests. Fresh supporting module builds also pass:
gm-entities 139, gm-organizations 56, gm-fleets 42, gm-workforce 20. Studio tests/build are
NOT_REQUIRED because no Studio source changed in STEP 18.

The unchanged canonical PowerShell runner was invoked with -InstallModules for run 1,
without it for run 2, and with -Mode Unflagged for the last run. JAVA_HOME used Java
25.0.4 and -MavenCommand selected the installed Maven 3.9.16 launcher. No tests were
skipped through Maven flags and no guard was bypassed.

| Mode | Run UUID | Port | Fresh tables | Flyway max | Delete triggers | Global categories | Evidence files | Container/evidence disposed |
|---|---|---:|---:|---:|---:|---:|---:|---|
| RealDb | 31ce2165-93b3-4319-975c-a77bc5ad7bcc | 52840 | 0 | 35 | 17 | 8 | 3 | True/True |
| RealDb | 546d9f0a-9028-439b-b7d0-49890df1f892 | 51541 | 0 | 35 | 17 | 8 | 3 | True/True |
| Unflagged | 28bc9c57-57f6-40d0-96b6-dc3c11cde138 | 56460 | 0 | 35 | 17 | 8 | 0 | True/True |

All databases were core_business_expenses_test on 127.0.0.1, in distinct disposable
instances. Evidence roots were `<temp>/gypport/gm-expenses-realdb/<run-uuid>` and were
removed. Final Docker inspection found no remaining expenses test-run container.

| Fixture table | Run 1 | Run 2 |
|---|---:|---:|
| tenants | 39 | 39 |
| user_accounts | 39 | 39 |
| expense_case | 24 | 24 |
| expense | 40 | 40 |
| expense_advance | 4 | 4 |
| advance_settlement | 2 | 2 |
| expense_document | 4 | 4 |
| expense_category | 26 | 26 |
| responsible_reference | 28 | 28 |
| vehicle_reference | 9 | 9 |
| expense_command_receipt | 178 | 178 |
| expense_allocation | 2 | 2 |
| expense_case_resource | 5 | 5 |
| expense_review_event | 9 | 9 |
| expense_revision_event | 1 | 1 |
| expense_document_review_event | 0 | 0 |
| expense_advance_participant_event | 6 | 6 |
| settlement_balance_event | 1 | 1 |

Counts are equivalent, with each run starting from zero tables. Case/Fleet transactional
fixtures roll back within their suites; other fixtures remain until external disposal.

### Protected DEV verification

Read-only snapshots before and after all tests contain identical rows across all 91
tables, and identical columns/FKs/triggers metadata. Flyway history is unchanged.
SHA-256 of both complete snapshots:

`b9888f573f2ec2ebff157b25c6a392428c08b818b91d245db95f1a62d1dbe9d5`

| Shared DEV table | Before | After |
|---|---:|---:|
| advance_settlement | 6 | 6 |
| expense | 44 | 44 |
| expense_adjustment | 0 | 0 |
| expense_advance | 16 | 16 |
| expense_advance_assignment_event | 0 | 0 |
| expense_advance_participant_event | 10 | 10 |
| expense_allocation | 0 | 0 |
| expense_case | 15 | 15 |
| expense_case_resource | 10 | 10 |
| expense_category | 13 | 13 |
| expense_command_receipt | 227 | 227 |
| expense_document | 11 | 11 |
| expense_document_review_event | 0 | 0 |
| expense_review_event | 40 | 40 |
| expense_revision_event | 13 | 13 |
| responsible_reference | 13 | 13 |
| settlement_adjustment_event | 0 | 0 |
| settlement_balance_event | 0 | 0 |
| vehicle_reference | 21 | 21 |

CORE_BUSINESS_DEV_MUTATIONS=0. The four preserved ambiguous E2E expenses remain unchanged.
Manual evidence has the same 58 relative paths and SHA-256 file hashes before/after.
No shared database/evidence cleanup was performed.

Sanitized evidence is retained in this report. Raw local run reports remain in
`platform_os/server/target/expenses-realdb-results/<run-uuid>/`; logs and read-only snapshot
comparison results are in `%TEMP%/gypport-step18/`. Raw reports, session details and DEV
row snapshots are not copied into repository documentation or staged.


## Git scope

No staging or commit is performed in STEP 18: its implementation authorization does not
explicitly authorize those separate Git operations (AGENTS.md section 11 and canonical
execution order section 2). STEP 17's existing local commit remains on the Fleet feature
branch; this repair remains in the working tree on that same branch. No history rewrite,
push, deployment or VPS operation.


## Final scope and next action

FILES_CHANGED=ExpenseCaseHttpApiTest.java; ExpenseFleetHttpApiTest.java; this handoff.
LOCAL_COMMITS=NONE_FOR_STEP_18.
STEP_17_LOCAL_COMMIT=40c49f631c1d27be198ce0c4eb1892fa3eaa1909.
PREEXISTING_WIP_PRESERVED=YES; the ten protected file hashes still match the STEP 17 baseline.
MIGRATIONS=NONE. PUSH=NO. VPS=NO.

NEXT_EXACT_ACTION=FREEZE_GM_EXPENSES_MVP_AND_RESUME_GM_FLEETS.
This is a recommendation based on the requested fresh checks, not an executed freeze,
independent audit, commit or branch integration. Owner branch integration remains separate.

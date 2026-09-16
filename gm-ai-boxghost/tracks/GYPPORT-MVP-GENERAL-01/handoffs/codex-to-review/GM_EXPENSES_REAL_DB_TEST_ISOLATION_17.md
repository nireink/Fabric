# GM_EXPENSES_REAL_DB_TEST_ISOLATION_17

TRACK=GYPPORT-MVP-GENERAL-01
MODE=CONTROLLED_TEST_INFRASTRUCTURE_IMPLEMENTATION
STATUS=BLOCKED
RECOMMENDED_GM_EXPENSES_BASELINE_STATUS=NOT_READY

Isolation infrastructure is implemented and its safety/lifecycle checks passed. Full
acceptance is blocked by seven existing Cases/Fleet assertions that disagree with the
current HTTP contract. Both full isolated runs reproduce these failures. No assertion,
production behavior or migration was changed to hide them. Do not freeze the baseline.

## Verified repository baseline

- Gystigo: `feature/gm-fleets-minimum-vehicle-master-01`, initial HEAD
  `6252359c01f6d9125549b2bd2ca9b35599401798`.
- Modules/gm-expenses: `master`, HEAD `049c74adda2b774841ddb931176be8e7785f847f`, clean and unchanged.
- Authoritative parent: `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT`.
  The initially configured Documents/ChatGPT/gm-expenses checkout is not the source checkout.
- Pre-existing Gystigo WIP: Button.tsx, AuthPage.css, ShortRegisterPage.jsx;
  five STUDIO handoff documents and HeaderBrandingFixture.jsx/header-branding.html.
  All excluded from this change and from its exact-path local commit.
- Flyway maximum verified on disk and DEV: V35. Existing migrations remain unchanged.
- Runtime: Java 25.0.4, Maven 3.9.16, MySQL image 8.4.10, Docker CLI.

## Previous architecture and selected mechanism

`GmExpensesHostIntegrationTest` and `GmExpensesHttpApiTest` inherited the Host datasource
configuration targeting localhost:3308/core_business_dev. Their previous BeforeEach
checks explicitly approved that shared database, after Spring/Flyway startup. The Host
suite selected the first tenant and used actor 1; the HTTP suite registered accounts,
tenants and related fixtures. Neither suite used whole-test transactional rollback.
Partial AfterEach deactivation/deletion could not remove the append-only history and
could itself fail on dependent records. Evidence used the Host default
`platform_os/server/data/expense-documents`. Canonical Flyway ran in the shared Host
configuration; the existing development Docker service was persistent.

Cases/Fleet HTTP suites already used `@Transactional`, the fleets real-DB flag, and the
fixed endpoint localhost:3310/core_business_fleets_test. Other module tests also showed
dedicated Docker/MySQL acceptance databases (including workforce port 3312). An isolated
Docker/MySQL pattern existed, but no reusable disposable lifecycle runner was found.

EXISTING_ISOLATED_PATTERN_FOUND=YES
SELECTED_TEST_ISOLATION_STRATEGY=DOCKER_CLI_DISPOSABLE_MYSQL_PER_RUN

Reuse the established Docker/MySQL tooling, without Testcontainers, new dependencies,
Compose changes or production wiring. A single script creates a unique container, fresh
anonymous volume, test-schema-only user, dynamic loopback port and UUID evidence root;
runs canonical Flyway and all four expenses real-DB suites; captures counts; and disposes
the owned instance/volume/evidence in finally. This is suitable for a future Docker-enabled
CI worker with the required sibling module checkouts; no CI deployment was added.

## Implementation

- `ExpensesTestDatabaseGuard`: exact test-name/local-port/URL option allowlist, both
  explicit opt-in flags, UUID evidence-root validation, JDBC metadata/catalog and actual
  SELECT DATABASE() validation. Shared DEV and port 3308 fail closed.
- `ExpensesRealDbIsolation`: test initializer before Spring refresh/Flyway; explicitly
  owned guarded DataSource, every borrowed connection checked, separate Flyway datasource
  settings rejected, evidence redirects rejected, canonical migrations and logging email.
- `ExpensesTestDatabaseGuardTest`: 15 tests including positive/negative names, missing
  configuration, unsafe options/paths and rejection before fixture mutation.
- Host integration: register a fresh account/tenant through existing onboarding per test;
  use the returned actor in commands and allocation fixtures; remove first-tenant lookup.
- HTTP integration: retain self-owned accounts/organizations/vehicles and remove partial
  SQL teardown. Disposal handles the whole database with real triggers still active.
- Case/Fleet HTTP: shared initializer and expenses opt-in flag; existing tests, payloads,
  assertions and transactional rollback unchanged.
- `run-expenses-real-db-tests.ps1`: one canonical lifecycle command, optional module
  install/test step, Unflagged mode, fresh Surefire reports, ownership/path cleanup guards.
- `docs/testing/GM_EXPENSES_REAL_DB_TESTS.md`: reproducible command, prerequisites, flags,
  failure message, disposal and result locations.

Production source, production HTTP contract, module dependencies and V1..V35 migrations
are unchanged. No Flyway repair, shared SQL mutation, trigger disablement, push or VPS work.

## Fresh execution results

| Suite | Tests | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
| gm-expenses module | 677 | 0 | 0 | 0 |
| Gystigo unflagged | 356 | 0 | 0 | 119 |
| Each isolated full run (includes guard) | 73 | 7 | 0 | 0 |
| Guard in each full run | 15 | 0 | 0 | 0 |
| GmExpensesHostIntegrationTest | 11 | 0 | 0 | 0 |
| GmExpensesHttpApiTest | 28 | 0 | 0 | 0 |
| ExpenseCaseHttpApiTest | 11 | 3 | 0 | 0 |
| ExpenseFleetHttpApiTest | 8 | 4 | 0 | 0 |

The 58 real-DB tests yield 51 passed and seven failed; the additional 15 guard tests pass.
Unflagged means 237 executed successfully and 119 opt-in tests skipped. Studio tests/build
are NOT_REQUIRED because this change touches no Studio source. Fresh supporting module
builds also passed: gm-entities 139, gm-organizations 56, gm-fleets 42, gm-workforce 20.

Append-only physical-delete checks, document/evidence replacement, tenant and organization
isolation, and report coverage in the two GmExpenses suites pass. This does not imply that
the failed Case/Fleet scenarios completed their later assertions. Overall real-DB
acceptance and the no-regression completion gate remain unfulfilled.

| Mode | Run UUID | Port | Fresh tables | Flyway max | Delete triggers | Global categories | Evidence files | Container/evidence disposed |
|---|---|---:|---:|---:|---:|---:|---:|---|
| RealDb | c039899c-2401-471b-a6fc-8734ea8deed1 | 53302 | 0 | 35 | 17 | 8 | 3 | True/True |
| RealDb | acf253d0-581c-4835-9d51-bd4aff8e0664 | 60726 | 0 | 35 | 17 | 8 | 3 | True/True |
| Unflagged | 6dba87ec-99f2-4152-bbce-0c062458dada | 63300 | 0 | 35 | 17 | 8 | 0 | True/True |

All connections used 127.0.0.1/core_business_expenses_test. Evidence roots were
`<temp>/gypport/gm-expenses-realdb/<run-uuid>` and were removed. Final Docker inspection
found no container with the expenses test-run label. DEV services remained running.

### Fixture count equivalence

| Table | Run 1 | Run 2 |
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

Both runs started with zero tables. Counts are identical, so prior fixtures did not
accumulate. The runner disposed resources even when Maven returned failure.

## Negative acceptance and protected DEV

Two actual contexts were intentionally configured for
`jdbc:mysql://127.0.0.1:3308/core_business_dev` with dummy credentials and both explicit
flags. The Host and HTTP selectors failed during initialization, before connection,
fixture setup or evidence creation, with the required message:

> gm-expenses real-DB tests require an isolated test database. Refusing to run against core_business_dev.

Negative-test mutations: zero. Before/after full snapshots matched across 91 tables plus
column/FK/trigger metadata. Final snapshots after both full runs and the unflagged suite
also match exactly, including flyway_schema_history. Snapshot SHA-256 before and after:

`b9888f573f2ec2ebff157b25c6a392428c08b818b91d245db95f1a62d1dbe9d5`

| Protected shared table | Before | After |
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

The four ambiguous E2E Food/Settlement Flow expenses are preserved with all other rows.
Manual evidence: 58 files before, 58 after, identical relative paths and SHA-256 hashes.
There were no cleanup operations against shared DEV in STEP 17. Final source search found
zero mutating expenses test configuration references approving core_business_dev/3308;
remaining literals are guard denylist/negative assertions or explanatory documentation.

## Blocking assertions (same in both runs)

All paths below are relative to `platform_os/server/src/test/java/com/gypport/server/module/expenses/`.

| Test | Failure location | Expected / actual |
|---|---|---|
| canonicalPersonsAreCreatedOnceReusedAndDeliveryActorsAreSeparated | ExpenseCaseHttpApiTest.java:184 | 201 / 400 |
| multipleVehiclesExplicitChoiceAndRemovalPreserveHistoricalSnapshot | ExpenseCaseHttpApiTest.java:91 | 201 / 400 |
| vehicleCaseFoodWithoutVehicleFuelSnapshotAndIdempotency | ExpenseCaseHttpApiTest.java:68 | 400 / 201 |
| vehicleCategoriesRequireFleetSelectionAndPreserveSnapshot, COMBUSTIBLE | ExpenseFleetHttpApiTest.java:57 | 201 / 400 |
| Same parameterized method, PEAJE | ExpenseFleetHttpApiTest.java:57 | 201 / 400 |
| Same parameterized method, PARQUEADERO | ExpenseFleetHttpApiTest.java:57 | 201 / 400 |
| Same parameterized method, MANTENIMIENTO | ExpenseFleetHttpApiTest.java:57 | 201 / 400 |

The six rejected creation requests send `fleetVehicleReference`; current production
`ExpenseCaseController.java:101` does not permit that field and responds
"El formulario contiene campos no admitidos." The opposite-status failure expects an
explicit vehicle requirement where the current implementation resolves the sole case
vehicle and creates the expense. These assertions/payloads already exist at the starting
HEAD; only their isolation annotations/import/flag changed in this STEP. We did not run
the old configuration against shared DEV to reproduce them there.

Resolving the contract/test discrepancy requires a separate bounded decision about the
accepted Cases/Fleet contract. Changing production behavior or silently weakening
assertions is outside this isolation STEP. STATUS must remain BLOCKED until both complete
real-DB runs pass after that reconciliation. FREEZE_GM_EXPENSES_MVP_AND_RESUME_GM_FLEETS is
the requested downstream action, currently blocked; it was not executed.

## Evidence and local publication scope

Sanitized aggregate evidence is recorded above. Local raw reports are under
`platform_os/server/target/expenses-realdb-results/<run-uuid>/`; execution logs and
read-only comparison artifacts are in `%TEMP%/gypport-step17/`. They are not staged because
raw HTTP/Surefire reports can include test session details. The full DEV snapshot remains
local and is not copied into repository documents.

One controlled local commit contains only the seven Java test files, lifecycle script,
developer guide and this handoff (10 paths). The commit is identified in the final task
response; this document belongs to that same commit. No module commit or push.

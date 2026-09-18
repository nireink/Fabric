# GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24 — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24
MODE=PREDEPLOYMENT_PROOF -> BACKUP -> V64 MIGRATION -> BUILD_FROM_COMMITTED_BYTES -> DEPLOY -> PROVENANCE -> SMOKE
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24.md
STATUS=DEPLOYED_READY_FOR_OWNER_SMOKE
SOURCE_EDITED=NO   NEW_COMMITS=0   PUSH_PERFORMED=NO   OWNER_CASE_MODIFIED=NO
```

## 1. Source baseline (§1) — matched exactly

```text
Modules/gm-expenses  master                                       874a3e5071e46b179444730089d34afa5fe0e742
Gystigo              feature/gm-fleets-minimum-vehicle-master-01   0293ff45e94b2ebbec67e792fea28e7b80bc8901
Fabric               main                                          018ea843b6bbb86f4e47c3ad43edb42ac7f7ffe5
```

The other module heads are the ones the STEP 18 image was built from and are unchanged: gm-entities e6d3cbc,
gm-organizations 62f3de4, gm-fleets 756cccc, gm-human-resources 08f10c7, gm-security d3fa0b4,
gm-fuel-stations 8ee330d.

## 2. Pre-deployment Shared DEV state (§4)

```text
DATABASE=core_business_dev   FLYWAY=63 (last row: 63 gm expenses unified settlement reconciliation, success, 16:24:52)
FAILED_MIGRATIONS=0
expense_case=30  expense=82  expense_advance=54  advance_settlement=28  settlement_balance_event=14
expense_review_event=131
OWNER_CASE 437a92bf: 2 RETURN_REGISTERED events totalling USD 300.00
```

## 3. Backup and its validation (§5)

```text
BACKUP_PATH=C:\Users\elbur\AppData\Local\Temp\gypport\shared-dev-backups\core_business_dev-pre-v64-20260917T200210.sql
BACKUP_SIZE=1011872
BACKUP_SHA256=0f5fbd0ee6c2e7815d57a95c4a1947e7d06ce0bce41977a13aeb95bdab2505b1
RESTORE_VALIDATION=PASS   (restored into a disposable MySQL 8.4.10 container: 107 tables, 30 Cases, Flyway 63)
```

On that restored copy the committed V64 byte was then applied as a pre-flight: 30 of 30 Cases numbered, 0 null,
0 duplicates, Owner Case -> 202609170001 / 2026-09-17 / sequence 1, and the six financial tables byte-identical
(CHECKSUM TABLE) before and after. The disposable container was removed.

## 4. V64 provenance (§6)

```text
V64_FROM=git show 0293ff45...:database/modules/gm-expenses/migration/V64__gm_expenses_case_business_number.sql
V64_COMMITTED_SHA256=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21  bytes=7568
V64_BYTES_UNCHANGED_SINCE_REHEARSAL=YES (same hash as the STEP 22 rehearsal and the STEP 23 staged blob)
V64_PACKAGED_IN_ARTIFACT_SHA256=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21
```

## 5. Build from committed bytes (§11, §12)

Every repository was exported at its committed HEAD into a clean tree (the unrelated Gystigo WIP never entered it),
each module was built from that export, and the Host was packaged from it with the exported Maven wrapper, offline.

```text
HOST_ARTIFACT_SHA256=eee602458e586b8a63a4b653b7a85d062fee718e68c298f979d3ffee1612de35  bytes=31343455
NESTED_MODULE_JARS_EQUAL_EXPORT_BUILDS=7 of 7
PACKAGED_MIGRATIONS=65  MISSING=0  DIFFERENT=0  HIGHEST=V64
CLASSES_PRESENT=CaseNumber, BusinessDatePort, JdbcCaseNumberSequenceRepository
CONTROLLER_EMITS=caseNumber, caseSequence, businessDate, movements, movement-reversals
IMAGE_TAG=gystigo-backend:4.1.0-java25-gm-expenses-v64-0293ff4
IMAGE_ID=sha256:7d1018c48e74e9b251782e251df75de6d0a0d65592dfe949857c0530443e368e
LABELS gypport.step=GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24,
       gypport.source.gystigo=0293ff45..., gypport.source.gm-expenses=874a3e50...,
       gypport.artifact.sha256=eee60245...
```

The deployment Dockerfile is the committed runtime stage verbatim; its single changed line replaces the build-stage
COPY with a COPY of that artifact.

## 6. The migration (§7, §8, §9, §10)

Applied through the accepted path: the Host application's own Flyway, from this image, with the official DEV service
configuration, in a one-off container with no published port. No manual SQL ran against Shared DEV.

```text
OFFICIAL_BACKEND_STOPPED_FIRST=YES   OTHER_DB_SESSIONS=0   PRE_FLYWAY=63/47 rows/0 failed
Migrating schema core_business_dev to version "64 - gm expenses case business number"
Successfully applied 1 migration, now at version v64   execution 680 ms
POST_FLYWAY=64  history_rows=48  failed=0  v64_success=1  beyond_64=0
```

Data result:

```text
EXPENSE_CASE_COUNT=30   CASES_WITH_BUSINESS_DATE=30   CASES_WITH_CASE_SEQUENCE=30   CASES_WITH_CASE_NUMBER=30
NULL_CASE_NUMBERS=0     DUPLICATE_TENANT_CASE_NUMBERS=0   NUMBER_MATCHES_PARTS=30 of 30   COUNTER_ROWS=13
OWNER_CASE=Compra Filtro | businessDate=2026-09-17 | caseSequence=1 | caseNumber=202609170001
SINGLE_SEQUENCE_SOURCE=case_sequence  (the number is a generated column over the same value; no second counter exists)
```

Financial integrity:

```text
FINANCIAL_CHECKSUMS_IDENTICAL=YES  (expense, expense_advance, advance_settlement, settlement_balance_event,
                                    expense_review_event, expense_command_receipt - identical before and after)
ROW_COUNTS_UNCHANGED=YES (82 expenses, 54 advances, 28 settlements, 14 balance events, 131 review events)
OWNER_CASE_RETURN_EVENTS_PRESERVED=YES  (2 events, USD 300.00, 0 reversals)
```

## 7. Runtime after deployment (§13, §14)

```text
FRONTEND=http://localhost:5173, Vite on the current Gystigo Studio working tree (caseTitle + "ID:" in the served bytes),
         API base http://localhost:8080
BACKEND=gypport-backend-dev, image gystigo-backend:4.1.0-java25-gm-expenses-v64-0293ff4, healthy, 127.0.0.1:8080
        /app/app.jar sha256 = eee602458e586b8a63a4b653b7a85d062fee718e68c298f979d3ffee1612de35 (the built artifact)
BACKEND_RUNTIME_SOURCE=0293ff45e94b2ebbec67e792fea28e7b80bc8901
GM_EXPENSES_RUNTIME_SOURCE=874a3e5071e46b179444730089d34afa5fe0e742
DATABASE=core_business_dev, Flyway validated 65 migrations, current version 64, no migration necessary
```

## 8. Smoke on the deployed runtime (§15, §20)

22 checks, 0 failures, 0 HTTP 5xx, with synthetic `@example.test` accounts in their own tenants. The Owner's account,
Case and data were never touched (the smoke's probe of the Owner Case correctly answered 404).

```text
AUTHENTICATION, CASE_CREATED, CASE_DETAIL, CASE_LIST, FINANCIAL_SUMMARY_PRESENT, ADVANCES_PRESENT
DETAIL_HAS_BUSINESS_DATE / CASE_SEQUENCE / CASE_NUMBER = YES      LIST_HAS_ the same three = YES
NUMBER_IS_DATE_PLUS_SEQUENCE: 202609170001 = 20260917 + 0001      FIRST_CASE_OF_ITS_TENANT_DAY: sequence 1
BUSINESS_DATE_IS_TODAY: 2026-09-17 while created_at is 2026-09-18T01:15Z UTC - the configured business zone at work
SEQUENCE_ADVANCES: the second Case of the day took sequence 2
TENANT_COUNTS_ITS_OWN_DAY: another tenant's first Case is also sequence 1
TENANT_ISOLATION: cross-tenant read 404      UUID_ROUTES_PRESERVED: GET by number 400
```

## 9. Reversal readiness, proved on the deployed runtime (§18)

In a synthetic tenant (never the Owner's Case): an advance of USD 200 was delivered, a Return of USD 100 registered
and then reversed through the product.

```text
RETURN_REQUIRES_REASON=YES      400 "Indica el motivo del movimiento."
REVERSAL_REQUIRES_REASON=YES    400 "Indica el motivo del reverso."
REVERSAL_ACCEPTED=YES           200 MOVEMENT_REVERSED, and the rendition's returned total went 100.00 -> 0.00
APPEND_ONLY=YES                 database: RETURN_REGISTERED (reverses NULL) kept, plus RETURN_REVERSED with
                                reverses_balance_event_id set, both with the authenticated actor and their reason
ORIGINAL_IMMUTABLE=YES          the movement is shown as reversed (reversed=true, reversedAt, canReverse=false)
OWNER_REVERSALS_EXECUTED=NO
```

Observation, not a defect of this deployment: the movement's `performedByName` came back empty for the synthetic
account, whose identity is still PENDING; the actor id is recorded in the event either way.

## 10. The Owner's Case before the reversal (§17)

Read-only from the migrated database, this is what the Case now holds, and therefore what the card will show:

```text
DELIVERED_ADVANCES=320.00 (200 EN_RENDICION + 100 EN_RENDICION + 20 ENTREGADO)
EXPENSES=APROBADO 4 for 400.00, RECHAZADO 1 for 200.00 (which weighs nothing)
SETTLEMENTS returned=300.00 reimbursed=0.00 adjustments=0.00
=> Total anticipos 320.00 | Total gastos 400.00 | Total a conciliar 80.00 Por reembolsar
   Devuelto 300.00 | Reembolsado 0.00 | Pendiente 380.00 Por reembolsar | Usado 400.00
   ID Gasto 202609170001, Fecha 2026-09-17, EXP. 01
```

Devuelto 300.00 and Pendiente 380.00 are expected until the Owner reverses the two historical Return events.

# GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27 — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27
MODE=PREDEPLOYMENT_PROOF -> BACKUP -> V65_MIGRATION -> BUILD_FROM_COMMITTED_HEADS -> DEPLOY -> PROVENANCE -> SMOKE
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27.md
STATUS=DEPLOYED_READY_FOR_OWNER_FINAL_SMOKE
SOURCE_EDITED=NO   NEW_SOURCE_COMMITS=0   PUSH_PERFORMED=NO   OWNER_CASE_MODIFIED=NO   OWNER_REVERSALS_EXECUTED=NO
```

## 1. Source and evidence (§2, §4, §7, §8)

```text
gm-expenses master 39a2adf4dfff0196208a1f80719be1c12c047ac2   Gystigo feature/gm-fleets-minimum-vehicle-master-01
5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc   Fabric main 1f5bed831c54d01efe74444f02ee2b2d947df549
worktrees: gm-expenses clean; Gystigo and Fabric hold only their 5 and 10 unrelated WIP paths
COMMITTED_BYTES_MATCH_ACCEPTED_EVIDENCE=YES (proved at the STEP 26 gate; no accepted path has changed since)
V64_COMMITTED_SHA256=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21   V64_UNCHANGED=YES
V65_COMMITTED_SHA256=8ed3c20b1b45af4f832623992882612f4fe78d8327b31d8cb3a90a245e1962b4   V65_COMMITTED_BYTE_VERIFIED=YES
```

## 2. Before any change (§5)

```text
official backend gystigo-backend:4.1.0-java25-gm-expenses-v64-0293ff4   Shared DEV Flyway 64, 0 failed
expense_sequence column absent   expense_case=35 in 11 tenants
Owner Case 437a92bf: RETURN_REGISTERED 200 and RETURN_REGISTERED 100, no reversal
financial CHECKSUM TABLE and an MD5 over every Case's business date, daily sequence, business number and created_at
recorded before the migration
```

## 3. Backup (§6)

```text
BACKUP_PATH=C:\Users\elbur\AppData\Local\Temp\gypport\shared-dev-backups\core_business_dev-pre-v65-20260917T222529.sql
BACKUP_SIZE=1068711
BACKUP_SHA256=ffd4abb7674f5a4f268bad0198016cdfc62bd7ea7151326d84c7796e3263482e
RESTORE_VALIDATION=PASS (disposable MySQL 8.4.10: 108 tables, 35 Cases, Flyway 64)
PRE-FLIGHT on that restored copy with the committed V65 byte: 35 of 35 numbered, 0 null, 0 duplicates,
0 order mismatches, Owner Case exp 8 / ID 202609170001, financial checksums equal to the live ones
```

## 4. Build from committed bytes (§14, §15)

```text
EXPORTS=each repository archived at its committed HEAD; the other six modules at the heads the STEP 24 image used
GM_EXPENSES_BUILD=PASS  jar sha256 54f50a3e185c54615c5d4421723908dba6605d2e45a1ad66e0ec6aa453c3ad2c (from 39a2adf)
HOST_ARTIFACT_SHA256=8c438d5da7de3f84329810ed1d9481f597fbc178229f859305381915f207baf8  bytes=31349087
NESTED_MODULE_JARS_EQUAL_EXPORT_BUILDS=7 of 7   PACKAGED_MIGRATIONS=66, MISSING=0, DIFFERENT=0, HIGHEST=V65
V64_PACKAGED=95dc6f57...   V65_PACKAGED=8ed3c20b...   ExpenseSequence and JdbcExpenseSequenceRepository present
CONTROLLER_EMITS=expenseSequence, caseNumber, caseSequence, businessDate, movements, movement-reversals
IMAGE_TAG=gystigo-backend:4.1.0-java25-gm-expenses-v65-5eed5d6
IMAGE_ID=sha256:f44f598a5a786ab4f91a0d1b42fcfb1ee803a819f680c51cd11513a702d6533e
LABELS gypport.step=GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27, gypport.source.gystigo=5eed5d6...,
       gypport.source.gm-expenses=39a2adf..., gypport.artifact.sha256=8c438d5d...
```

## 5. Migration (§9, §10, §11, §12, §13)

Applied by the Host application's own Flyway from this image, with the official DEV service configuration, in a
one-off container with no published port; the official backend was stopped first and no other session was connected.

```text
Migrating schema core_business_dev to version "65 - gm expenses case permanent sequence"
Successfully applied 1 migration, now at v65 (1176 ms)   FLYWAY=65, history rows 49, FAILED=0   SHARED_DEV_VERSION=V65
TOTAL_EXPENSE_CASES=35  CASES_WITH_EXPENSE_SEQUENCE=35  NULL_EXPENSE_SEQUENCE=0  DUPLICATE_TENANT_EXPENSE_SEQUENCE=0
ORDER_MISMATCHES=0 against tenant, created_at, expense_case_id   TENANTS=11  COUNTER_ROWS=11  COUNTER_GAPS=0
FINANCIAL_CHECKSUMS_IDENTICAL=YES   BUSINESS_NUMBERS_AND_CREATED_AT_UNCHANGED=YES
FINANCIAL_HISTORY_CHANGED_BY_V65=NO   OWNER_CASE_RETURN_HISTORY_PRESERVED=YES (200 and 100, no reversal)
```

The real numbers of the Owner's tenant, read from the migrated database - creation order, never the business date:

```text
EXP 01 Viaje los encuentros   202608310001     EXP 06 PRUEBA20260909    202609100001
EXP 02 Viaje A Loja           202608310002     EXP 07 Viaje Loja        202609130001
EXP 03 Viaje Zamora           202609010001     EXP 08 Compra Filtro     202609170001  (uuid 437a92bf-..., case_sequence 1)
EXP 04 SUSCRIPCION IA         202609020001     EXP 09 VIAJE QUITO       202609170002  (uuid a41aa6c9-..., case_sequence 2)
EXP 05 Compra Camaras         202609030001
```

EXP and the ID are independent in the real data: Compra Filtro is EXP 08 and the first Case of its day, VIAJE QUITO
EXP 09 and the second.

## 6. Runtime (§16, §17)

```text
FRONTEND=http://localhost:5173 - Vite on the Gystigo Studio working tree, whose expenses files are the committed
         5eed5d6 bytes (served modules: caseTitle(item) and caseTitle(detail) over expenseSequenceOf, "ID: " + caseNumber)
BACKEND=gypport-backend-dev, image gystigo-backend:4.1.0-java25-gm-expenses-v65-5eed5d6, healthy, 127.0.0.1:8080;
        /app/app.jar sha256 = 8c438d5d... (the built artifact)
DATABASE=core_business_dev: Flyway validated 66 migrations, current version 65, no migration necessary
```

## 7. Smoke and reversal readiness (§18, §23, §24)

Synthetic `@example.test` accounts, each in its own tenant; the Owner's account and data were never touched.

```text
SMOKE 27 checks, 0 failures, 0 HTTP 5xx: authentication, list and detail with expenseSequence, caseSequence,
      caseNumber and businessDate; the first Case of a new tenant is EXP 1, the second EXP 2; another tenant counts from
      1 on both counters; cross-tenant read 404; GET by number 400 (the UUID route); financial summary present
REVERSAL 12 checks, 0 failures: a Return needs a motive, a reverso needs a reason, the reverso nets the return to 0,
      the original stays and is marked reversed (canReverse=false), a second reverso of the same movement is refused
      ("Este movimiento ya fue reversado."); in the database the original RETURN_REGISTERED is kept and a
      RETURN_REVERSED pointing at it is appended with the authenticated actor
```

How the Owner's two stored returns will present: events 29 (USD 200, settlement 61) and 30 (USD 100, settlement 62)
share the same instant, actor and reason, so the product shows them as ONE movement "Devolución USD 300.00". Its single
reverso appends two RETURN_REVERSED events, 200 and 100. Both rows are CONCILIADO: the reverso is allowed (only CERRADO
refuses), it reopens them to EN_CONCILIACION / PENDING in the same update, and the reconciled-equation CHECK applies
only to RECONCILED rows - so the database accepts the result. After it: Devuelto 0.00, Pendiente 80.00 Por reembolsar.

## 8. The Owner's Case before the reverso (§22)

Read-only from the migrated database: delivered 320.00 (200 + 100 + 20), approved 400.00, one rejected 200.00, returned
300.00, reimbursed 0.00. The card and detail therefore read Total anticipos 320.00 | Total gastos 400.00 | Total a
conciliar 80.00 Por reembolsar | Devuelto 300.00 | Reembolsado 0.00 | Pendiente 380.00 Por reembolsar | Usado 400.00 |
Uso 125%, with EXP. 08: Compra Filtro, Fecha 2026-09-17, ID: 202609170001.

## 9. What was not done

```text
REAL_UI_WITH_OWNER_SESSION=NOT PERFORMED - the Owner's cards need the Owner's own login, which Claude does not use; the
        served code, the deployed API fields and the migrated values above fix what those cards render
OWNER_REVERSALS_EXECUTED=NO   PUSH_PERFORMED=NO   NEW_SOURCE_COMMITS=0
FABRIC_EVIDENCE_OF_THIS_STEP=written, uncommitted (this folder, the stored prompt, CURRENT_STEP) - awaiting authorization
```

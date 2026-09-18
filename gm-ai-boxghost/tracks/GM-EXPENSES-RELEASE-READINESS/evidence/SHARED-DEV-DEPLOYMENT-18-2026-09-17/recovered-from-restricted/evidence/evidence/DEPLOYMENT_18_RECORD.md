# GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 — deployment record (2026-09-17, non-secret)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18
MODE=CONTROLLED_SHARED_DEV_MIGRATION_AND_DEPLOYMENT
STATUS=READY_FOR_OWNER_REAL_LOGIN_SMOKE
SOURCE gm-expenses=545eae0fb287f8e04f7f1b4ac73780304ec53f22 Gystigo=bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f Fabric baseline commit=bbdd66a0c5a1c9cbb21293beb74c3e5e61cc5de0
VERIFIED_BASELINE=GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
OTHER MODULE SOURCES (clean HEADs) gm-entities=e6d3cbcc5e004e8fbd11c78dc1817b5a00e6bffb gm-organizations=62f3de4cf6e30b874c2342b1cb864f704293504c gm-fleets=756cccc5fcfcdf5b745a612afbb1071495441036 gm-human-resources=08f10c72c23eeaace12f00cc317c6a4a672b9405 gm-security=d3fa0b470cb117fb5c1620b6860ecc34ad73a50d gm-fuel-stations=8ee330d78149b8f8d0b1886b0d34ac82efc9361b
```

## Precheck (16:14Z–16:24Z)
- Process, User and Machine scopes: no SPRING_DATASOURCE_* / SPRING_FLYWAY_*; no value references Shared DEV.
- Host TCP: no process connected to 3308; the local runtime backend (PID 23072) held 10 connections to 3310 only.
- Shared DEV sessions: only event_scheduler; innodb_trx 0; events 0; binlog.000040:158 unchanged; trx_rw_commits 0 since server start.
  Innodb_rows_inserted rose 0→4 while trx_rw_commits stayed 0 and Created_tmp_disk_tables rose 0→2: intrinsic temporary tables of the
  audit's own read-only diagnostic queries, not writes. UNKNOWN_SHARED_DEV_WRITERS=NONE.
- Official DEV backend gypport-backend-dev exited (image gystigo-backend:4.1.0-java25, sha256:45953ec7…); non-secret config saved.

## Build from committed bytes (16:15Z–16:18Z)
- `git archive` exports of the 8 commits: every file byte-identical to its blob except .cmd/.ps1 files converted by .gitattributes eol;
  0 missing, 0 extra. Gystigo WIP absent (README.md and AuthPage.css / ShortRegisterPage.jsx at committed versions, both untracked fixtures absent).
- Isolated offline Maven repository (third-party artifacts only, no com/gypport), `-o`.
- Modules: 6 x `clean install -DskipTests`; gm-expenses `clean install` with tests: 748/748, BUILD SUCCESS.
- Host: `-pl server -am -DskipTests clean package` (the committed Dockerfile's build stage).
- GM_EXPENSES_JAR_SHA256=0c39764d5cbee6188cd30e3d360a6ac2e1611f25c11637b8256a3acd0b1aa35e
- GYSTIGO_ARTIFACT_SHA256=da5fa8c361953f739058c6098656bdec266a4f320c7efa487b4ab95d2e3a9d8d (31,318,800 bytes)
- Artifact proof: 7 nested module jars = isolated builds; 64 packaged migrations = baseline MIGRATION_SHA256 (V62 d805797c…, V63 6db2eacc…);
  highest V63, no V64, no duplicates; Host classes 188 = sources of bcb9591; gm-expenses classes 217 = sources of 545eae0 (removed classes absent);
  every class/resource byte-identical to the accepted tested jars (gm-expenses 250/250 vs 1C6FEF03; Host 224/224 vs F4A55094; all 7 nested
  modules identical; 56/56 third-party libraries identical).

## Image (16:20Z)
- Deployment Dockerfile: the committed runtime stage verbatim; only `COPY --from=build …` replaced by `COPY` of the proven artifact.
- IMAGE_TAG=gystigo-backend:4.1.0-java25-gm-expenses-mvp-bcb9591
- IMAGE_ID=sha256:9e3ff62f02d670bd003408a5d3631f4e17daa0cf0dbb00b887c0266e99048f81 (local store digest gystigo-backend@sha256:9e3ff62f…; not pushed to a registry)
- /app/app.jar SHA-256 = artifact; user app:app; /app/data/expense-documents app:app; JRE 25.0.3; labels carry every source commit.
- Built with --pull=false --network none from the local eclipse-temurin:25-jre-noble (sha256:2f1da100…).

## Backup (16:21Z)
- BACKUP_FILE=GYPPORT-Storage/Restricted/Gystigo/shared-dev-deployment-18-2026-09-17/core_business_dev_V43_20260917T162128Z.sql
- BACKUP_SHA256=eb5f88d8d37a1fdb28f079ade99582e20f319635081c0af3dc8cb36840d13c56 (838,347 bytes; created 2026-09-17T16:21:29Z)
- SOURCE_DB=gypport-mysql-dev 127.0.0.1:3308 core_business_dev; SOURCE_FLYWAY=V43 (27 rows, 0 failed)
- mysqldump --single-transaction --routines --triggers --events --hex-blob --no-tablespaces --set-gtid-purged=OFF, exit 0, empty stderr;
  header and completion trailer present; 102 CREATE TABLE; 29 triggers; Flyway history included.
- BACKUP_VERIFIED=YES: restored as root into a disposable mysql:8.4.10 (127.0.0.1:52237) in 7 s with no output; fingerprint identical to live
  Shared DEV on 10/10 facets (flyway, flyway history, counts, triggers, routines, columns, constraints, gm-expenses CRC, legacy rows, audit);
  container removed.

## Pre-migration fingerprint
- Identical to FINAL_12 on flyway, triggers, routines, columns, per-table counts, gm-expenses CRC and legacy rows: SCHEMA_DRIFT=NONE,
  DATA_CHANGE=NONE, UNKNOWN_DRIFT=NONE.

## Migration (16:24:38Z–16:24:58Z)
- Final gate: binlog.000040:158, rw_commits 0, no other session, Flyway 43/27/0, old backend exited.
- One-off container from the new image with the official compose service configuration (root via .env, network gystigo-dev_default,
  no published port): Flyway validated 64, current 43, applied V44..V63: "Successfully applied 20 migrations … now at version v63
  (execution time 00:08.428s)"; warnings only the guarded DROP PROCEDURE IF EXISTS notes and one integer display width note.
- START_VERSION=V43 END_VERSION=V63 MIGRATIONS_APPLIED=20 FAILED_MIGRATIONS=0 installed_by=root; container stopped and removed.

## Post-migration integrity (identical to the FINAL_12 rehearsal)
- Tables 102→107, rows 3,192→3,234; only flyway_schema_history changed among existing tables (27→47); added: mdm_identity_intake_identifiers(0),
  mdm_identity_intakes(0), tax_subjects(0), user_tenant_membership_events(11), user_tenant_memberships(11); no table lost rows.
- 19/19 gm-expenses tables content-identical over the pre-migration columns (expense_advance gained planned_delivery_method_code,
  planned_rendition_days).
- Triggers 29→32 (3 membership guards), none changed or removed; routines 0; 17 delete guards; 8 canonical categories.
- V61 origin columns 2 / old 0 / origin FKs 3 / identity pair check / 11 accounts, 0 without membership; V62 planned columns 2, checks 3,
  0 rows with a plan; V63 reconciled equation + shortfall-only checks, 10 settlement checks, 0 reconciled rows violating; 0 ambiguous legacy links.
- Legacy rows unchanged; audit_logs 0.

## Official DEV backend (16:26:20Z)
- Local runtime backend (PID 23072, 127.0.0.1:8080 → 3310) stopped to free 8080; its MySQL 3310 kept running.
- `docker compose -f Gystigo/docker/compose.yaml -f <deploy override: image tag> up --detach --no-deps --no-build --pull never backend`
  (compose.yaml equals bcb9591): container gypport-backend-dev recreated as c46c761c…, image sha256:9e3ff62f…, restart unless-stopped,
  127.0.0.1:8080, gystigo-dev_default 172.18.0.4, healthy after ~11 s.
- Flyway validated 64, schema 63 up to date, no migration; Started ServerApplication in 5.3 s; 0 ERROR lines.
- Connections: Shared DEV 10 sessions from 172.18.0.4 (root, core_business_dev); 3310 has no application session.

## Automated deployment smoke (16:28:55Z–16:29:05Z)
- 37/37 PASS, 0 server 5xx: the 33 accepted FINAL_12 checks (same results, e.g. period summary delivered 71729 / used 66420 / pendingReturn 2530 /
  pendingReimbursement 120) plus anonymous /auth/me 401 + tenant context, REGISTRADO edit, review-history event types, list/read APIs.
- Tenant isolation: tenant B 404 on 11 operations, empty lists and reports.
- Synthetic records (identifiable S18): accounts 592/593/594 deploy-smoke-s18{a,z,b}-…@example.test in new tenants 593/594/595; 24 tables grew,
  none shrank, schema unchanged. Pre-existing rows of all 19 gm-expenses tables unchanged (CRC excluding the smoke tenants = pre-migration).
- Backend log: 0 ERROR; 2 WARN (the startup default-user notice; the smoke's deliberate refused correction of a RECHAZADO expense).

## Legacy data (unchanged, not cleaned)
- OBSERVADO expense 5E63494AA2564C1E847CD54A6ED67A51 (tenant 1): OBSERVADO v2, 0 review events.
- 3 CERRADO settlements on EN_RENDICION advances (tenant 1, Case 0BA391C4…): unchanged.
- Draft and standalone records of pre-existing tenants: unchanged.

## Rollback inputs (not executed)
- V43 backup: path and SHA-256 above, verified restorable.
- Previous image: gystigo-backend:4.1.0-java25 sha256:45953ec7bb8b7a40927d269031113d967e751ff535ecdb42dc2aaeea202de421 (kept);
  previous container non-secret config saved (deploy/old-backend-container-nonsecret.json).
- New image: gystigo-backend:4.1.0-java25-gm-expenses-mvp-bcb9591 sha256:9e3ff62f02d670bd003408a5d3631f4e17daa0cf0dbb00b887c0266e99048f81.
- Rollback would be: stop gypport-backend-dev; restore the V43 backup into core_business_dev as root; recreate the backend from the committed
  compose.yaml (previous tag). Never a hand-written reverse migration. A restore also removes the S18 smoke records.

## Not done in this STEP
- No source, Fabric or documentation change; nothing staged or committed; no push; no V64; no legacy cleanup.

# GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30 — record (2026-09-18)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30
MODE=READ_ONLY_INVENTORY -> HASH_VERIFY -> SECURE_ARCHIVE_COPY -> RESTORE_VALIDATION -> OWNER_SAFE_TEMP_CLEANUP -> EVIDENCE
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30.md
STATUS=ARCHIVED_AND_VERIFIED
SOURCE_CODE_CHANGED=NO   SHARED_DEV_MODIFIED=NO   RUNTIME_CHANGED=NO   SQL_CONTENT_IN_FABRIC=NO
```

Raw evidence in this folder, metadata only: `inventory.tsv`, `archive-results.tsv`, `restore-validation.txt`,
`cleanup-results.txt`. No dump and no row of any dump is in Fabric.

## 1. Inventory and recorded evidence (§1, §2)

`%LOCALAPPDATA%\Temp\gypport\shared-dev-backups` held 11 files; no other dump exists anywhere under
`%LOCALAPPDATA%\Temp\gypport`.

```text
KIND                   FILE                                            BYTES     SHA-256           MODIFIED
DATABASE_DUMP          core_business_dev-pre-v64-20260917T200210.sql   1011872   0f5fbd0ee6c2e781  2026-09-17T20:02:11
DATABASE_DUMP          core_business_dev-pre-v65-20260917T222529.sql   1068711   ffd4abb7674f5a4f  2026-09-17T22:25:32
COMPANION_METADATA     pre-migration-checksums.txt                         285   7c201655f253658c  2026-09-17T20:01:35
COMPANION_METADATA     post-migration-checksums.txt                        285   7c201655f253658c  2026-09-17T20:08:54
COMPANION_METADATA     preflight-20260917T200210.txt                      1110   93d2cc57a17f1684  2026-09-17T20:02:36
COMPANION_METADATA     pre-v65-checksums.txt                               283   9889f175c5d0ddc9  2026-09-17T22:27:35
COMPANION_METADATA     post-v65-checksums.txt                              283   9889f175c5d0ddc9  2026-09-17T22:31:28
COMPANION_METADATA     pre-v65-business-numbers.md5                         33   9d65384338e1a123  2026-09-17T22:27:37
COMPANION_METADATA     preflight-20260917T222529.txt                      1138   3291dc54119e749b  2026-09-17T22:27:15
MIGRATION_SOURCE_COPY  V64-from-commit-0293ff4.sql                        7568   95dc6f57abf5609c  2026-09-17T20:02:12
MIGRATION_SOURCE_COPY  V65-from-commit-5eed5d6.sql                        5614   8ed3c20b1b45af4f  2026-09-17T22:25:35
```

```text
PRE_V64  size 1011872 and SHA-256 0f5fbd0ee6c2e7815d57a95c4a1947e7d06ce0bce41977a13aeb95bdab2505b1
         = STEP 24 evidence (SHARED-DEV-V64-DEPLOYMENT-24-2026-09-17/backup-and-preflight.txt)
PRE_V65  size 1068711 and SHA-256 ffd4abb7674f5a4f268bad0198016cdfc62bd7ea7151326d84c7796e3263482e
         = STEP 27 evidence (V65-SHARED-DEV-DEPLOYMENT-27-2026-09-17/backup-and-preflight.txt)
KNOWN_BACKUPS_MATCH_RECORDED_HASHES=YES
MIGRATION_SOURCE_COPIES=byte-identical to the committed migrations (V64 at Gystigo 0293ff4, V65 at Gystigo 5eed5d6)
```

The pre and post checksum pairs are equal to each other, which is what STEPs 24 and 27 reported: the migrations left
the six financial tables unchanged.

## 2. Restricted destination (§3, §4)

GYPPORT_STORAGE was resolved through `GYPPORT_LOCATIONS.properties`. `Restricted/` already follows one convention -
`Restricted/Gystigo/<runtime-or-deployment>-<date>/`, with evidence under `evidence/` (`runtime-local-alignment-2026-09-16/`,
`shared-dev-deployment-18-2026-09-17/`) - so no new hierarchy was invented:

```text
GYPPORT_STORAGE/Restricted/Gystigo/shared-dev-deployment-24-2026-09-17/   the pre-V64 dump, companions in evidence/db/
GYPPORT_STORAGE/Restricted/Gystigo/shared-dev-deployment-27-2026-09-17/   the pre-V65 dump, companions in evidence/db/
GYPPORT_STORAGE/Restricted/Gystigo/ARCHIVE_MANIFEST_SHARED_DEV_BACKUPS_STEP30.md
```

The architecture's Restricted rules held: only path, size, hash, timestamps and classification were read or recorded;
no dump content entered the agent's output or Fabric.

## 3. Copy first, then validation (§5)

```text
ARCHIVED_COUNT=9 (2 dumps, 7 companions)   COPY_HASH_MISMATCHES=0   SIZES_EQUAL=9/9   MODIFICATION_TIMES_PRESERVED=9/9
```

The companions are archived with their dumps because they are each backup's own record: the checksum files and the
business-number fingerprint appeared nowhere in Fabric (0 of their lines in the committed deployment evidence), and the
pre-flight outputs, already in Fabric line for line, complete the set. Full table: `archive-results.tsv`.

## 4. Restore validation from the restricted copies (§6)

Each restricted copy - never the Temp source - was streamed into a fresh `mysql:8.4.10` container with no network, a
random root password that was never printed and a scratch schema; only metadata was read; the container was removed.
Expectations are the deployment evidence's own restore results.

```text
PRE_V64  SQL_DUMP_READABLE=YES RESTORE_EXIT=0   tables 107 (expected 107)   expense_case 30 (expected 30)
         Flyway 63 (expected 63), 0 failed   financial CHECKSUM TABLE 6/6 equal to the pre-migration record   PASS
PRE_V65  SQL_DUMP_READABLE=YES RESTORE_EXIT=0   tables 108 (expected 108)   expense_case 35 (expected 35)
         Flyway 64 (expected 64), 0 failed   financial CHECKSUM TABLE 6/6 equal to the pre-migration record   PASS
RESTRICTED_COPY_RESTORE_VALIDATION=PASS   DISPOSABLE_CONTAINERS_LEFT=0
SHARED_DEV_MYSQL_CONTAINER=same start time before and after the validation; never addressed
```

The checksum comparison goes beyond the deployments' own restore checks: each restored copy reproduces, table for
table, the financial checksums taken from the live database just before its migration.

## 5. Temp cleanup (§8, §9)

```text
GATE: source hash verified, restricted copy present, destination hash equal, restore validation PASS, manifest written
TEMP_BACKUPS_SAFE_TO_REMOVE=YES
TEMP_REMOVED_COUNT=2 - the two dumps, each re-hashed on both sides against its recorded SHA-256 immediately before removal
POST: both restricted copies present with the recorded SHA-256; both Temp dumps absent; TEMP_DUMPS_REMAINING=0
TEMP_RETAINED=9 non-dump files - the 7 companions (archived copies in Restricted) and the 2 migration-source copies
       (identical to Git); the prompt limits removal to backup files, so they and the directory stay
CLEANUP_DEFERRED=NO
```

## 6. Frozen MVP and Shared DEV (§12)

```text
GM_EXPENSES master 39a2adf4dfff0196208a1f80719be1c12c047ac2 = origin, clean
GYSTIGO master 5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc = origin (5 unrelated WIP paths, unchanged)
SHARED_DEV Flyway 65, 0 failed, 49 versioned rows; the Owner Case unchanged since STEP 28 (reversals 35/36, returned 0)
DEV_CONTAINERS gypport-mysql-dev and gypport-backend-dev were started again at 2026-09-18T10:43:07Z, before this
               STEP (restart count 0); the backend still runs gystigo-backend:4.1.0-java25-gm-expenses-v65-5eed5d6, healthy
```

## 7. For the Owner

```text
STEP_18_RESTRICTED_FOLDER=shared-dev-deployment-18-2026-09-17/ already holds the STEP 18 dump and an evidence/ tree
      (build logs, database audits) - input for GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31, whose non-sensitive parts
      would belong in BoxGhost
TEMP_LEFTOVERS=9 non-sensitive files remain in %LOCALAPPDATA%\Temp\gypport\shared-dev-backups; removing them is a
      one-line decision whenever wanted
PRE_PRODUCTION_SECURITY_DEBT=SPRING_GENERATED_PASSWORD_STARTUP_LOG (unchanged)
```

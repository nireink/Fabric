#!/usr/bin/env bash
# GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - fresh Shared DEV V43 backup (read-only mysqldump, root inside the container).
# The dump goes to GYPPORT-Storage/Restricted (never Git, never Fabric). Nothing secret is printed; the dump content is never shown.
set -uo pipefail
S18="C:/Users/elbur/AppData/Local/Temp/claude/D--NZXTG7-GYPPORT-GYPPORT-ERP/6bd391c2-9dd7-4c98-8f41-546e5a9baea1/scratchpad/s18"
DIR="D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT-Storage/Restricted/Gystigo/shared-dev-deployment-18-2026-09-17"
mkdir -p "$DIR"
ro() { { printf 'SET SESSION TRANSACTION READ ONLY;\nSTART TRANSACTION READ ONLY;\n'; cat; printf '\nROLLBACK;\n'; } | docker exec -i gypport-mysql-dev sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql -uroot --batch --skip-column-names "$MYSQL_DATABASE"' 2>&1 | tr -d '\r' | { grep -v "Using a password" || true; }; }

echo "== writer state before backup"
echo "SHOW BINARY LOG STATUS; SELECT CONCAT('rows_ins_upd_del=', SUM(VARIABLE_VALUE)) FROM performance_schema.global_status WHERE VARIABLE_NAME IN ('Innodb_rows_inserted','Innodb_rows_updated','Innodb_rows_deleted'); SELECT CONCAT('sessions=', COUNT(*)) FROM information_schema.PROCESSLIST WHERE USER NOT IN ('event_scheduler') AND ID <> CONNECTION_ID(); SELECT CONCAT('flyway_max=', MAX(CAST(version AS UNSIGNED)), ' rows=', COUNT(*), ' failed=', SUM(success=0)) FROM flyway_schema_history WHERE version IS NOT NULL;" | ro

TS="$(date -u +%Y%m%dT%H%M%SZ)"
FILE="$DIR/core_business_dev_V43_${TS}.sql"
echo "BACKUP_STARTED_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
docker exec gypport-mysql-dev sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysqldump -uroot --single-transaction --routines --triggers --events --hex-blob --no-tablespaces --set-gtid-purged=OFF --default-character-set=utf8mb4 "$MYSQL_DATABASE"' > "$FILE" 2> "$S18/precheck/mysqldump.stderr.txt"
DUMP_EXIT=$?
echo "BACKUP_FINISHED_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ) MYSQLDUMP_EXIT=$DUMP_EXIT STDERR_LINES=$(grep -c . "$S18/precheck/mysqldump.stderr.txt")"
grep -v -i "password" "$S18/precheck/mysqldump.stderr.txt" | head -5
echo "BACKUP_FILE=$FILE"
echo "BACKUP_BYTES=$(stat -c %s "$FILE")"
echo "BACKUP_SHA256=$(sha256sum "$FILE" | cut -c1-64)"
echo "BACKUP_CREATED_AT=$(date -u -r "$FILE" +%Y-%m-%dT%H:%M:%SZ)"
echo "HEADER_IS_MYSQLDUMP=$(head -c 200 "$FILE" | grep -c 'MySQL dump')"
echo "TRAILER_DUMP_COMPLETED=$(tail -c 200 "$FILE" | grep -c 'Dump completed on')"
echo "CREATE_TABLE_STATEMENTS=$(grep -c '^CREATE TABLE ' "$FILE")"
echo "TRIGGER_DEFINITIONS=$(grep -c 'TRIGGER `' "$FILE")"
echo "FLYWAY_HISTORY_INSERTS=$(grep -c '^INSERT INTO `flyway_schema_history`' "$FILE")"
echo "SOURCE_DB=gypport-mysql-dev 127.0.0.1:3308 core_business_dev"
echo "$FILE" > "$S18/precheck/backup-file.txt"

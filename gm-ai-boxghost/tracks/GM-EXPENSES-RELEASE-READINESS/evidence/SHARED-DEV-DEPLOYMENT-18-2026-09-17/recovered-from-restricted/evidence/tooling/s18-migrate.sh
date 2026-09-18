#!/usr/bin/env bash
# GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - apply V43 -> V63 to Shared DEV through the accepted path: the Host application's own
# Flyway, from the verified deployment image, with the official DEV service configuration (compose service `backend`, root via
# the gitignored .env, network gystigo-dev_default) in a one-off container with no published port. No manual SQL.
set -uo pipefail
export MSYS_NO_PATHCONV=1
S18="C:/Users/elbur/AppData/Local/Temp/claude/D--NZXTG7-GYPPORT-GYPPORT-ERP/6bd391c2-9dd7-4c98-8f41-546e5a9baea1/scratchpad/s18"
G="D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo"
ro() { { printf 'SET SESSION TRANSACTION READ ONLY;\nSTART TRANSACTION READ ONLY;\n'; cat; printf '\nROLLBACK;\n'; } | docker exec -i gypport-mysql-dev sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql -uroot --batch --skip-column-names "$MYSQL_DATABASE"' 2>&1 | tr -d '\r' | { grep -v "Using a password" || true; }; }

echo "== final writer check"
CHECK="$(echo "SELECT CONCAT('binlog=', FILE, ':', POSITION) FROM performance_schema.log_status CROSS JOIN JSON_TABLE(JSON_EXTRACT(LOCAL, '\$.binary_log_position'), '\$' COLUMNS (POSITION BIGINT PATH '\$')) jt CROSS JOIN JSON_TABLE(JSON_EXTRACT(LOCAL, '\$.binary_log_file'), '\$' COLUMNS (FILE VARCHAR(64) PATH '\$')) jf; SELECT CONCAT('rw_commits=', COUNT) FROM information_schema.INNODB_METRICS WHERE NAME = 'trx_rw_commits'; SELECT CONCAT('other_sessions=', COUNT(*)) FROM information_schema.PROCESSLIST WHERE USER <> 'event_scheduler' AND ID <> CONNECTION_ID(); SELECT CONCAT('flyway=', MAX(CAST(version AS UNSIGNED)), '/', COUNT(*), '/', SUM(success=0)) FROM flyway_schema_history WHERE version IS NOT NULL;" | ro)"
echo "$CHECK"
echo "$CHECK" | grep -q '^binlog=binlog.000040:158$' || { echo "STOP: binlog position moved"; exit 2; }
echo "$CHECK" | grep -q '^rw_commits=0$' || { echo "STOP: a read-write transaction committed"; exit 2; }
echo "$CHECK" | grep -q '^other_sessions=0$' || { echo "STOP: another session is connected"; exit 2; }
echo "$CHECK" | grep -q '^flyway=43/27/0$' || { echo "STOP: unexpected Flyway state"; exit 2; }
docker inspect gypport-backend-dev --format '{{.State.Status}}' | grep -q '^exited$' || { echo "STOP: the old DEV backend is not stopped"; exit 2; }

echo "MIGRATION_CONTAINER_START_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
docker compose -f "$G/docker/compose.yaml" -f "$S18/deploy/compose.deploy18.yaml" run --detach --no-deps --name gypport-dev-migration-18 backend > "$S18/deploy/migration-run.out.txt" 2>&1
echo "COMPOSE_RUN_EXIT=$? $(tr -d '\r' < "$S18/deploy/migration-run.out.txt" | tail -1)"
ID="$(docker ps -a --filter name=^gypport-dev-migration-18$ --format '{{.ID}}' | head -1)"
[ -n "$ID" ] || { echo "STOP: migration container not created"; exit 3; }
echo "MIGRATION_CONTAINER_ID=$ID IMAGE=$(docker inspect "$ID" --format '{{.Config.Image}} {{.Image}}') PUBLISHED_PORTS=$(docker inspect "$ID" --format '{{json .HostConfig.PortBindings}}')"
RESULT=TIMEOUT
for i in $(seq 1 150); do
  LOG="$(docker logs "$ID" 2>&1)"
  if echo "$LOG" | grep -q "Started ServerApplication"; then RESULT=STARTED; break; fi
  if echo "$LOG" | grep -q -E "APPLICATION FAILED TO START|FlywayException|Migration .* failed|Validate failed"; then RESULT=FAILED; break; fi
  if [ "$(docker inspect "$ID" --format '{{.State.Status}}')" = "exited" ]; then RESULT=EXITED; break; fi
  sleep 2
done
echo "MIGRATION_RESULT=$RESULT AFTER_POLLS=$i AT_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
docker logs "$ID" 2>&1 | tr -d '\r' | grep -v -i "generated security password" > "$S18/deploy/migration-container.log"
grep -E "Flyway|DbValidate|DbMigrate|Migrating schema|Successfully applied|Current version|up to date|Started ServerApplication|ERROR|WARN .*o.f.c" "$S18/deploy/migration-container.log" | cut -c1-220 | head -60
docker stop --time 30 "$ID" > /dev/null && echo "MIGRATION_CONTAINER_STOPPED=YES"
docker container rm --volumes "$ID" > /dev/null && echo "MIGRATION_CONTAINER_REMOVED=YES"
echo "== Flyway after"
echo "SELECT CONCAT('flyway_max=', MAX(CAST(version AS UNSIGNED)), ' history_rows=', COUNT(*), ' failed=', SUM(success = 0), ' applied_44_63=', SUM(CAST(version AS UNSIGNED) BETWEEN 44 AND 63 AND success = 1), ' beyond_63=', SUM(CAST(version AS UNSIGNED) > 63), ' first_new=', MIN(CASE WHEN CAST(version AS UNSIGNED) > 43 THEN installed_on END), ' last_new=', MAX(CASE WHEN CAST(version AS UNSIGNED) > 43 THEN installed_on END), ' total_exec_ms=', SUM(CASE WHEN CAST(version AS UNSIGNED) > 43 THEN execution_time END), ' installed_by=', GROUP_CONCAT(DISTINCT CASE WHEN CAST(version AS UNSIGNED) > 43 THEN installed_by END)) FROM flyway_schema_history WHERE version IS NOT NULL;" | ro

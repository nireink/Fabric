#!/usr/bin/env bash
# GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 - read-only fingerprint of one MySQL database.
# Usage: f12-snapshot.sh <target> <outprefix>
#   target = dev  -> Shared DEV 127.0.0.1:3308 (gypport-mysql-dev, core_business_dev), every statement READ ONLY
#   target = copy -> the disposable rehearsal container named in f12-container-name.txt
set -euo pipefail
S="C:/Users/elbur/AppData/Local/Temp/claude/D--NZXTG7-GYPPORT-GYPPORT-ERP/6bd391c2-9dd7-4c98-8f41-546e5a9baea1/scratchpad"
target="$1"; out="$2"

run_sql() {
  if [ "$target" = "dev" ]; then
    { printf 'SET SESSION TRANSACTION READ ONLY;\nSTART TRANSACTION READ ONLY;\n'; cat; printf '\nROLLBACK;\n'; } |
      MYSQL_PWD="$SPRING_DATASOURCE_PASSWORD" docker exec -i -e MYSQL_PWD gypport-mysql-dev \
        mysql -u"$SPRING_DATASOURCE_USERNAME" --batch --skip-column-names core_business_dev 2>&1 | { grep -v "Using a password" || true; }
  else
    name="$(tr -d '\r\n' < "$S/f12-container-name.txt")"
    case "$name" in gypport-rehearsal-final12-*) ;; *) echo "NOT_THE_REHEARSAL_CONTAINER" >&2; exit 1;; esac
    { printf 'SET SESSION TRANSACTION READ ONLY;\nSTART TRANSACTION READ ONLY;\n'; cat; printf '\nROLLBACK;\n'; } |
      docker exec -i "$name" sh -c 'MYSQL_PWD=$MYSQL_ROOT_PASSWORD exec mysql -uroot --batch --skip-column-names gypport_rehearsal_final12' 2>&1 | { grep -v "Using a password" || true; }
  fi
}

echo "SELECT CONCAT('flyway_max=', MAX(CAST(version AS UNSIGNED)), ' history_rows=', COUNT(*), ' failed=', SUM(success = 0)) FROM flyway_schema_history WHERE version IS NOT NULL;" | run_sql > "$out-flyway.txt"

tables="$(echo "SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE() AND table_type = 'BASE TABLE' ORDER BY table_name;" | run_sql)"
query=""
for t in $tables; do
  [ -n "$query" ] && query="$query UNION ALL "
  query="${query}SELECT '$t', COUNT(*) FROM \`$t\`"
done
echo "SELECT * FROM ($query) x ORDER BY 1;" | run_sql | tr -d '\r' | LC_ALL=C sort > "$out-counts.txt"

echo "SELECT TRIGGER_NAME, EVENT_OBJECT_TABLE, ACTION_TIMING, EVENT_MANIPULATION, DEFINER, SHA2(ACTION_STATEMENT, 256) FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = DATABASE() ORDER BY TRIGGER_NAME;" | run_sql > "$out-triggers.txt"
echo "SELECT ROUTINE_TYPE, ROUTINE_NAME, SHA2(ROUTINE_DEFINITION, 256) FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = DATABASE() ORDER BY ROUTINE_TYPE, ROUTINE_NAME;" | run_sql > "$out-routines.txt"
echo "SELECT table_name, SHA2(GROUP_CONCAT(CONCAT_WS(':', column_name, column_type, is_nullable, IFNULL(column_default, '~'), extra) ORDER BY ordinal_position SEPARATOR '|'), 256) FROM information_schema.columns WHERE table_schema = DATABASE() GROUP BY table_name ORDER BY table_name;" | run_sql > "$out-columns.txt"

: > "$out-expenses-crc.txt"
for t in responsible_reference vehicle_reference expense_category expense_advance expense advance_settlement \
         expense_advance_assignment_event expense_review_event expense_revision_event settlement_adjustment_event \
         settlement_balance_event expense_adjustment expense_document expense_command_receipt expense_allocation \
         expense_document_review_event expense_advance_participant_event expense_case expense_case_resource; do
  cols="$(echo "SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = '$t' ORDER BY ordinal_position;" | run_sql)"
  expr=""
  for c in $cols; do [ -n "$expr" ] && expr="$expr, "; expr="${expr}\`$c\`"; done
  line="$(echo "SELECT CONCAT(COUNT(*), ':', COALESCE(SUM(CRC32(CONCAT_WS('|', $expr))), 0)) FROM \`$t\`;" | run_sql)"
  printf '%s\t%s\n' "$t" "$line" >> "$out-expenses-crc.txt"
done
echo "SNAPSHOT_DONE target=$target tables=$(wc -l < "$out-counts.txt")"

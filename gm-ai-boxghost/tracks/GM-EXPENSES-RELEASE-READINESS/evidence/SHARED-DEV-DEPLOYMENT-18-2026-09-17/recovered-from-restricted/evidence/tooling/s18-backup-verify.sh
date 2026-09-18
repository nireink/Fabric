#!/usr/bin/env bash
# GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - prove the fresh backup restores: disposable mysql:8.4.10 (random 127.0.0.1 port, never
# 3308/3310), restore as its root with default flags (the 29 triggers are defined by root@%), fingerprint, compare, remove.
set -uo pipefail
export MSYS_NO_PATHCONV=1
S18="C:/Users/elbur/AppData/Local/Temp/claude/D--NZXTG7-GYPPORT-GYPPORT-ERP/6bd391c2-9dd7-4c98-8f41-546e5a9baea1/scratchpad/s18"
FILE="$(cat "$S18/precheck/backup-file.txt")"
RUN="$(python -c 'import uuid; print(uuid.uuid4().hex[:8])')"
NAME="gypport-backup-verify-18-$RUN"
PW="$(python -c 'import secrets; print(secrets.token_hex(24))')"
docker run --detach --name "$NAME" --label "gypport.deploy18=backup-verify-$RUN" --env "MYSQL_ROOT_PASSWORD=$PW" \
  --env MYSQL_DATABASE=core_business_dev_restore --publish 127.0.0.1::3306 mysql:8.4.10 > "$S18/precheck/verify-container-id.txt"
unset PW
ID="$(cut -c1-12 "$S18/precheck/verify-container-id.txt")"
BINDING="$(docker port "$ID" 3306/tcp | head -1)"
echo "VERIFY_CONTAINER=$NAME ID=$ID BINDING=$BINDING"
case "$BINDING" in *:3308|*:3310) echo "REFUSED: forbidden port"; docker container rm --force --volumes "$ID" >/dev/null; exit 1;; esac
for i in $(seq 1 120); do
  if docker logs "$ID" 2>&1 | grep -q "ready for connections.*port: 3306 "; then break; fi
  sleep 2
done
echo "READY_AFTER_POLLS=$i"
START=$(date +%s)
docker exec -i "$ID" sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql -uroot "$MYSQL_DATABASE"' < "$FILE" > "$S18/precheck/restore.out.txt" 2>&1
echo "RESTORE_EXIT=$? SECONDS=$(( $(date +%s) - START )) RESTORE_OUTPUT_LINES=$(grep -v 'Using a password' "$S18/precheck/restore.out.txt" | grep -c .)"
PYTHONIOENCODING=utf-8 python "$S18/s18_db.py" fingerprint "$ID" restore
PYTHONIOENCODING=utf-8 python "$S18/s18_db.py" compare pre restore
docker container rm --force --volumes "$ID" > /dev/null && echo "VERIFY_CONTAINER_REMOVED=YES"
docker ps -a --filter "label=gypport.deploy18=backup-verify-$RUN" --format '{{.Names}}' | grep -c . | sed 's/^/LEFTOVER_CONTAINERS=/'

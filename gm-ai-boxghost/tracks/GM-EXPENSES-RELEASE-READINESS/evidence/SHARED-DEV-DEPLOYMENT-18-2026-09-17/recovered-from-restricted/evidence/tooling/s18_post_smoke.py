"""GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - read-only post-smoke proof on Shared DEV.
- the smoke footprint: synthetic S18 accounts, their tenants and the rows created in them;
- every pre-existing gm-expenses row is unchanged: CRC over the pre-migration columns restricted to non-smoke tenants equals the
  pre-migration CRC (all pre-migration rows belonged to pre-existing tenants);
- the legacy inconsistencies are unchanged."""
import io, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s18_db import ro, read, DB, EXPENSES_TABLES

C = "gypport-mysql-dev"
out = []
accounts = ro(C, "SELECT CONCAT(u.user_account_id, '|', u.username, '|', m.tenant_id) FROM user_accounts u JOIN user_tenant_memberships m ON m.user_account_id = u.user_account_id WHERE u.username LIKE 'deploy-smoke-s18%@example.test' ORDER BY u.user_account_id;")
smoke_tenants = sorted({int(line.split("|")[2]) for line in accounts})
out.append("SMOKE_ACCOUNTS=%d SMOKE_TENANTS=%s" % (len(accounts), smoke_tenants))
for line in accounts:
    account_id, username, tenant = line.split("|")
    out.append("  SMOKE_ACCOUNT id=%s username=%s tenant=%s" % (account_id, username, tenant))
if not smoke_tenants:
    raise SystemExit("no smoke tenants found")
tenant_list = ",".join(str(t) for t in smoke_tenants)
out += ["  " + l for l in ro(C, "SELECT CONCAT('SMOKE_TENANT id=', tenant_id, ' created_at=', created_at) FROM tenants WHERE tenant_id IN (%s) ORDER BY tenant_id;" % tenant_list)]
pre_existing_max_tenant = ro(C, "SELECT MAX(tenant_id) FROM tenants WHERE tenant_id NOT IN (%s);" % tenant_list)[0]
out.append("PRE_EXISTING_TENANTS=%s MAX_PRE_EXISTING_TENANT_ID=%s" % (ro(C, "SELECT COUNT(*) FROM tenants WHERE tenant_id NOT IN (%s);" % tenant_list)[0], pre_existing_max_tenant))

pre_columns = json.load(io.open(os.path.join(DB, "pre-expenses-columns.json"), encoding="utf-8"))
pre_crc = dict(l.split("\t") for l in read(os.path.join(DB, "pre-expenses-crc.txt")))
unchanged, smoke_rows = 0, {}
for table in EXPENSES_TABLES:
    cols = pre_columns[table]
    expr = ", ".join("`%s`" % c for c in cols)
    has_tenant = "tenant_id" in cols
    where = "WHERE tenant_id IS NULL OR tenant_id NOT IN (%s)" % tenant_list if has_tenant else ""
    now = ro(C, "SELECT CONCAT(COUNT(*), ':', COALESCE(SUM(CRC32(CONCAT_WS('|', %s))), 0)) FROM `%s` %s;" % (expr, table, where))[0]
    created = ro(C, "SELECT COUNT(*) FROM `%s` WHERE tenant_id IN (%s);" % (table, tenant_list))[0] if has_tenant else "n/a"
    smoke_rows[table] = created
    same = now == pre_crc[table]
    unchanged += 1 if same else 0
    out.append("%-36s pre_existing_rows:crc now=%s pre_migration=%s unchanged=%s smoke_rows=%s tenant_scoped=%s" % (table, now, pre_crc[table], same, created, has_tenant))
out.append("PRE_EXISTING_GM_EXPENSES_TABLES_UNCHANGED=%d/%d" % (unchanged, len(EXPENSES_TABLES)))

legacy_sql = io.open(r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-EXPENSES-RELEASE-READINESS\evidence\RUNTIME-REHEARSAL-FINAL-12-2026-09-17\f12-legacy.sql", encoding="utf-8-sig").read()
now_legacy = ro(C, legacy_sql)
pre_legacy = read(os.path.join(DB, "pre-legacy.txt"))


def section(lines, title):
    capture, rows = False, []
    for line in lines:
        if line.startswith("## "):
            capture = line.startswith(title)
            continue
        if capture:
            rows.append(line)
    return rows


for title in ("## INCONSISTENT: OBSERVADO expense without an OBSERVED review event",
              "## INCONSISTENT: CERRADO settlement whose advance is not RENDIDO/CERRADO"):
    a, b = section(pre_legacy, title), section(now_legacy, title)
    out.append("%s rows_pre=%d rows_now=%d identical=%s" % (title.replace("## ", ""), len(a), len(b), a == b))
    out += ["  " + r for r in b]
known = ro(C, "SELECT CONCAT('known_row_5E63494A=', lifecycle_status, ' v', version, ' review_events=', (SELECT COUNT(*) FROM expense_review_event r WHERE r.expense_id = e.expense_id)) FROM expense e WHERE HEX(expense_uuid) = '5E63494AA2564C1E847CD54A6ED67A51';")
out += known
drafts_pre, drafts_now = section(pre_legacy, "## OPEN WORK"), section(now_legacy, "## OPEN WORK")
out.append("OPEN_WORK_DRAFTS_OF_PRE_EXISTING_TENANTS_UNCHANGED=%s" % ([r for r in drafts_now if int(r.split("\t")[0]) not in smoke_tenants] == drafts_pre))
out += ro(C, "SELECT CONCAT('flyway=', MAX(CAST(version AS UNSIGNED)), '/', COUNT(*), '/', SUM(success=0)) FROM flyway_schema_history WHERE version IS NOT NULL;")
out += ro(C, "SELECT CONCAT('audit_logs=', (SELECT COUNT(*) FROM audit_logs), ' audit_action_types=', (SELECT COUNT(*) FROM audit_action_types));")
text = "\n".join(out)
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence", "post-smoke.txt"), "w", encoding="utf-8", newline="\n").write(text + "\n")
print(text)

"""GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - read-only database fingerprints and post-migration integrity checks.

usage:
  s18_db.py fingerprint <container> <prefix>        every statement inside SET SESSION TRANSACTION READ ONLY + START TRANSACTION READ ONLY
  s18_db.py compare-final12 <prefix>                classify the live fingerprint against FINAL_12 (EXPECTED_DATA_CHANGE / SCHEMA_DRIFT / UNKNOWN_DRIFT)
  s18_db.py compare <prefixA> <prefixB>             byte comparison of two fingerprints (backup restore vs live)
  s18_db.py post-migration <container> <pre-prefix> <post-prefix>

Credentials never leave the container: MYSQL_PWD is set inside it from its own environment (root, as the DEV backend)."""
import io, json, os, subprocess, sys

S18 = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(S18, "db")
F12 = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-EXPENSES-RELEASE-READINESS\evidence\RUNTIME-REHEARSAL-FINAL-12-2026-09-17"
EXPENSES_TABLES = ["responsible_reference", "vehicle_reference", "expense_category", "expense_advance", "expense", "advance_settlement",
                   "expense_advance_assignment_event", "expense_review_event", "expense_revision_event", "settlement_adjustment_event",
                   "settlement_balance_event", "expense_adjustment", "expense_document", "expense_command_receipt", "expense_allocation",
                   "expense_document_review_event", "expense_advance_participant_event", "expense_case", "expense_case_resource"]
LOGIN = 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" exec mysql -uroot --batch --skip-column-names "$MYSQL_DATABASE"'


def ro(container, sql):
    script = "SET SESSION TRANSACTION READ ONLY;\nSTART TRANSACTION READ ONLY;\n" + sql + "\nROLLBACK;\n"
    proc = subprocess.run(["docker", "exec", "-i", container, "sh", "-c", LOGIN], input=script.encode("utf-8"), capture_output=True)
    err = proc.stderr.decode("utf-8", "replace").replace("\r", "")
    err = "\n".join(l for l in err.splitlines() if "Using a password" not in l)
    if proc.returncode != 0 or err.strip():
        raise SystemExit("READ_ONLY_QUERY_FAILED on %s: %s" % (container, err.strip()[:300]))
    return [l for l in proc.stdout.decode("utf-8").replace("\r", "").split("\n") if l != ""]


def write(prefix, name, lines):
    with io.open(os.path.join(DB, "%s-%s.txt" % (prefix, name)), "w", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(line + "\n" for line in lines))


def read(path):
    return [l for l in io.open(path, encoding="utf-8-sig").read().replace("\r", "").split("\n") if l != ""]


def fingerprint(container, prefix):
    os.makedirs(DB, exist_ok=True)
    write(prefix, "identity", ro(container, "SELECT CONCAT('database=', DATABASE(), ' version=', VERSION(), ' utc=', UTC_TIMESTAMP(3));"))
    write(prefix, "flyway", ro(container, "SELECT CONCAT('flyway_max=', MAX(CAST(version AS UNSIGNED)), ' history_rows=', COUNT(*), ' failed=', SUM(success = 0)) FROM flyway_schema_history WHERE version IS NOT NULL;"))
    write(prefix, "flyway-history", ro(container, "SELECT IFNULL(version, '-'), type, checksum, success, script FROM flyway_schema_history ORDER BY installed_rank;"))
    tables = ro(container, "SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE() AND table_type = 'BASE TABLE' ORDER BY table_name;")
    counts = ro(container, "SELECT * FROM (" + " UNION ALL ".join("SELECT '%s', COUNT(*) FROM `%s`" % (t, t) for t in tables) + ") x ORDER BY 1;")
    write(prefix, "counts", sorted(counts))
    write(prefix, "triggers", ro(container, "SELECT TRIGGER_NAME, EVENT_OBJECT_TABLE, ACTION_TIMING, EVENT_MANIPULATION, DEFINER, SHA2(ACTION_STATEMENT, 256) FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = DATABASE() ORDER BY TRIGGER_NAME;"))
    write(prefix, "routines", ro(container, "SELECT ROUTINE_TYPE, ROUTINE_NAME, SHA2(ROUTINE_DEFINITION, 256) FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = DATABASE() ORDER BY ROUTINE_TYPE, ROUTINE_NAME;"))
    write(prefix, "columns", ro(container, "SELECT table_name, SHA2(GROUP_CONCAT(CONCAT_WS(':', column_name, column_type, is_nullable, IFNULL(column_default, '~'), extra) ORDER BY ordinal_position SEPARATOR '|'), 256) FROM information_schema.columns WHERE table_schema = DATABASE() GROUP BY table_name ORDER BY table_name;"))
    write(prefix, "constraints", ro(container, "SELECT table_name, constraint_type, constraint_name FROM information_schema.table_constraints WHERE table_schema = DATABASE() ORDER BY table_name, constraint_type, constraint_name;"))
    columns, crc = {}, []
    for table in EXPENSES_TABLES:
        cols = ro(container, "SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = '%s' ORDER BY ordinal_position;" % table)
        columns[table] = cols
        expr = ", ".join("`%s`" % c for c in cols)
        crc.append("%s\t%s" % (table, ro(container, "SELECT CONCAT(COUNT(*), ':', COALESCE(SUM(CRC32(CONCAT_WS('|', %s))), 0)) FROM `%s`;" % (expr, table))[0]))
    write(prefix, "expenses-crc", crc)
    with io.open(os.path.join(DB, prefix + "-expenses-columns.json"), "w", encoding="utf-8") as handle:
        json.dump(columns, handle, indent=1)
    write(prefix, "legacy", ro(container, io.open(os.path.join(F12, "f12-legacy.sql"), encoding="utf-8-sig").read()))
    write(prefix, "audit", ro(container, "SELECT CONCAT('audit_logs=', (SELECT COUNT(*) FROM audit_logs), ' audit_action_types=', (SELECT COUNT(*) FROM audit_action_types), ' events=', (SELECT COUNT(*) FROM information_schema.EVENTS WHERE EVENT_SCHEMA = DATABASE()));"))
    print("FINGERPRINT %s container=%s tables=%d triggers=%d flyway=%s" % (prefix, container, len(tables), len(read(os.path.join(DB, prefix + "-triggers.txt"))), read(os.path.join(DB, prefix + "-flyway.txt"))[0]))


LEGACY_HEADERS = {"section", "flyway_max\thistory_rows\tfailed", "expense\ttenant_id\texpense_case_id\tcreated_at",
                  "settlement\tadvance\tadvance_status\ttenant_id\texpense_case\tcase_status", "tenant_id\tin_case\tdrafts\toldest\tnewest",
                  "tenant_id\tlifecycle_status\tadvances", "legacy_linked_advances", "tenant_id\tlifecycle_status\tlinked_to_advance\texpenses",
                  "tenant_id\texpense_case\tcase_status\tadvance_currency\tadvances\tstatuses",
                  "lifecycle_status\treconciliation_result\tsettlements\twith_justified_total\twith_return\twith_reimbursement\twith_adjustment",
                  "tenant_id\tlifecycle_status\trows_with_justified_total", "advance_linked_expenses_outside_their_advance_case",
                  "closed_cases_with_changed_justified", "tenant_id\texpense_case\tcurrency\tdelivered\tjustified\treturned\treimbursed\trows_opened\trows_closed",
                  "open_cases\tclosed_cases\tadvances\texpenses\tsettlements"}


def compare_final12(prefix):
    verdict = []
    for name, kind in (("flyway", "SCHEMA"), ("triggers", "SCHEMA"), ("routines", "SCHEMA"), ("columns", "SCHEMA"), ("counts", "DATA"), ("expenses-crc", "DATA"), ("legacy", "DATA")):
        live = read(os.path.join(DB, "%s-%s.txt" % (prefix, name)))
        ref = read(os.path.join(F12, "f12-dev-%s.txt" % name))
        if name == "legacy":
            ref = [l for l in ref if l not in LEGACY_HEADERS]
        same = live == ref
        diff = [l for l in live if l not in ref][:6] + ["-" + l for l in ref if l not in live][:6]
        verdict.append((name, kind, same))
        print("VS_FINAL12 %-13s %s%s" % (name, "IDENTICAL" if same else "DIFFERENT", "" if same else " sample=%s" % diff))
    schema_drift = [n for n, k, s in verdict if k == "SCHEMA" and not s]
    data_change = [n for n, k, s in verdict if k == "DATA" and not s]
    print("SCHEMA_DRIFT=%s DATA_CHANGE=%s CLASSIFICATION=%s" % (schema_drift or "NONE", data_change or "NONE",
          "SCHEMA_DRIFT" if schema_drift else ("EXPECTED_DATA_CHANGE_REVIEW_REQUIRED" if data_change else "NO_DRIFT")))


def compare(a, b):
    diffs = 0
    for name in ("flyway", "flyway-history", "counts", "triggers", "routines", "columns", "constraints", "expenses-crc", "legacy", "audit"):
        la, lb = read(os.path.join(DB, "%s-%s.txt" % (a, name))), read(os.path.join(DB, "%s-%s.txt" % (b, name)))
        same = la == lb
        diffs += 0 if same else 1
        print("COMPARE %s vs %s %-15s %s" % (a, b, name, "IDENTICAL" if same else "DIFFERENT %s" % ([l for l in la if l not in lb][:3] + ["-" + l for l in lb if l not in la][:3])))
    print("COMPARE_DIFFERENCES=%d" % diffs)


def post_migration(container, pre, post):
    out = []
    out += ro(container, "SELECT CONCAT('max=', MAX(CAST(version AS UNSIGNED)), ' rows=', COUNT(*), ' failed=', SUM(success = 0), ' applied_44_63=', SUM(CAST(version AS UNSIGNED) BETWEEN 44 AND 63 AND success = 1), ' beyond_63=', SUM(CAST(version AS UNSIGNED) > 63)) FROM flyway_schema_history WHERE version IS NOT NULL;")
    before = dict(l.split("\t") for l in read(os.path.join(DB, pre + "-counts.txt")))
    after = dict(l.split("\t") for l in read(os.path.join(DB, post + "-counts.txt")))
    missing = sorted(t for t in before if t not in after)
    changed = sorted("%s %s->%s" % (t, before[t], after[t]) for t in before if t in after and before[t] != after[t])
    added = sorted("%s(%s)" % (t, after[t]) for t in after if t not in before)
    lost = [c for c in changed if int(c.split(" ")[1].split("->")[1]) < int(c.split(" ")[1].split("->")[0])]
    out.append("tables_before=%d tables_after=%d rows_before=%d rows_after=%d" % (len(before), len(after), sum(map(int, before.values())), sum(map(int, after.values()))))
    out.append("tables_missing_after=[%s]" % ", ".join(missing))
    out.append("tables_with_changed_counts=[%s]" % "; ".join(changed))
    out.append("tables_added_by_migrations=[%s]" % ", ".join(added))
    out.append("tables_with_fewer_rows=[%s]" % "; ".join(lost))
    pre_columns = json.load(io.open(os.path.join(DB, pre + "-expenses-columns.json"), encoding="utf-8"))
    pre_crc = dict(l.split("\t") for l in read(os.path.join(DB, pre + "-expenses-crc.txt")))
    mismatches = 0
    for table in EXPENSES_TABLES:
        now_cols = ro(container, "SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = '%s' ORDER BY ordinal_position;" % table)
        shared = [c for c in pre_columns[table] if c in now_cols]
        added_cols = [c for c in now_cols if c not in pre_columns[table]]
        removed_cols = [c for c in pre_columns[table] if c not in now_cols]
        expr = ", ".join("`%s`" % c for c in shared)
        now = ro(container, "SELECT CONCAT(COUNT(*), ':', COALESCE(SUM(CRC32(CONCAT_WS('|', %s))), 0)) FROM `%s`;" % (expr, table))[0]
        same = (now == pre_crc[table]) and not removed_cols
        mismatches += 0 if same else 1
        out.append("%-36s rows:crc before=%s after=%s same=%s shared_columns=%d columns_added=%s columns_removed=%s" % (
            table, pre_crc[table], now, same, len(shared), ",".join(added_cols) or "-", ",".join(removed_cols) or "-"))
    out.append("EXPENSES_CONTENT_MISMATCHES=%d" % mismatches)
    tb, ta = read(os.path.join(DB, pre + "-triggers.txt")), read(os.path.join(DB, post + "-triggers.txt"))
    out.append("triggers_before=%d triggers_after=%d changed_or_removed=[%s] new_or_changed=[%s]" % (
        len(tb), len(ta), ", ".join(l.split("\t")[0] for l in tb if l not in ta), ", ".join(l.split("\t")[0] for l in ta if l not in tb)))
    out += ro(container, "SELECT CONCAT('routines_left_by_migrations=', COUNT(*)) FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = DATABASE();")
    guards = ["trg_responsible_reference_no_delete:responsible_reference", "trg_vehicle_reference_no_delete:vehicle_reference",
              "trg_expense_category_no_delete:expense_category", "trg_expense_advance_no_delete:expense_advance", "trg_expense_no_delete:expense",
              "trg_advance_settlement_no_delete:advance_settlement", "trg_assign_event_no_delete:expense_advance_assignment_event",
              "trg_review_event_no_delete:expense_review_event", "trg_revision_event_no_delete:expense_revision_event",
              "trg_set_adj_event_no_delete:settlement_adjustment_event", "trg_exp_adjustment_no_delete:expense_adjustment",
              "trg_exp_document_no_delete:expense_document", "trg_set_balance_event_no_delete:settlement_balance_event",
              "trg_command_receipt_no_delete:expense_command_receipt", "trg_expense_allocation_no_delete:expense_allocation",
              "trg_exp_doc_review_event_no_delete:expense_document_review_event", "trg_advance_participant_event_no_delete:expense_advance_participant_event"]
    pairs = ",".join("('%s','%s')" % tuple(g.split(":")) for g in guards)
    out += ro(container, "SELECT CONCAT('expenses_delete_guards=', COUNT(*)) FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = DATABASE() AND ACTION_TIMING = 'BEFORE' AND EVENT_MANIPULATION = 'DELETE' AND (TRIGGER_NAME, EVENT_OBJECT_TABLE) IN (%s);" % pairs)
    out += ro(container, "SELECT CONCAT('canonical_categories=', COUNT(*)) FROM expense_category WHERE tenant_id IS NULL AND active = 1 AND category_code IN ('ALIMENTACION','COMBUSTIBLE','PEAJE','PARQUEADERO','MANTENIMIENTO','HOSPEDAJE','COMISIONES','OTRO');")
    out += ro(container, """SELECT CONCAT('V61 origin_columns=', (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND column_name IN ('origin_tenant_id','origin_party_id')),
  ' old_columns=', (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND column_name IN ('tenant_id','party_id')),
  ' origin_fks=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND constraint_type = 'FOREIGN KEY' AND constraint_name IN ('fk_user_accounts_origin_tenant','fk_user_accounts_origin_party','fk_user_accounts_origin_tenant_party')),
  ' old_fks=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND constraint_name IN ('fk_user_tenant','fk_user_party','fk_user_accounts_tenant_party')),
  ' identity_pair_check=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND constraint_name = 'ck_user_account_identity_pair'),
  ' retired_unique_key=', (SELECT COUNT(*) FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'user_accounts' AND index_name = 'uk_user_accounts_tenant_user'),
  ' accounts=', (SELECT COUNT(*) FROM user_accounts),
  ' accounts_without_membership=', (SELECT COUNT(*) FROM user_accounts u WHERE NOT EXISTS (SELECT 1 FROM user_tenant_memberships m WHERE m.user_account_id = u.user_account_id)));""")
    out += ro(container, """SELECT CONCAT('V62 planned_columns=', (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'expense_advance' AND column_name IN ('planned_delivery_method_code','planned_rendition_days')),
  ' planned_checks=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'expense_advance' AND constraint_name LIKE 'chk_advance_planned%'),
  ' existing_rows_with_plan=', (SELECT COUNT(*) FROM expense_advance WHERE planned_delivery_method_code IS NOT NULL OR planned_rendition_days IS NOT NULL));""")
    out += ro(container, """SELECT CONCAT('V63 return_reimburse_check=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'advance_settlement' AND constraint_name = 'chk_settlement_return_reimburse'),
  ' reconciled_equation_check=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'advance_settlement' AND constraint_name = 'chk_settlement_reconciled_equation'),
  ' adjustment_shortfall_check=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'advance_settlement' AND constraint_name = 'chk_settlement_adjustment_shortfall_only'),
  ' settlement_checks=', (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = 'advance_settlement' AND constraint_type = 'CHECK'),
  ' unified_clause=', (SELECT check_clause LIKE '%advance_amount_snapshot% + %reimbursement_amount%' FROM information_schema.check_constraints WHERE constraint_schema = DATABASE() AND constraint_name = 'chk_settlement_reconciled_equation'),
  ' reconciled_rows_violating=', (SELECT COUNT(*) FROM advance_settlement WHERE reconciliation_result = 'RECONCILED' AND advance_amount_snapshot + reimbursement_amount <> justified_expense_total + returned_amount + authorized_adjustment_total));""")
    out += ro(container, "SELECT CONCAT('ambiguous_legacy_links=', COUNT(*)) FROM expense_case c JOIN expense_advance a ON a.advance_id = c.advance_id AND a.tenant_id = c.tenant_id WHERE a.expense_case_id IS NOT NULL AND a.expense_case_id <> c.expense_case_id;")
    lb, la = read(os.path.join(DB, pre + "-legacy.txt")), read(os.path.join(DB, post + "-legacy.txt"))
    flyway_lines = {"## flyway"}
    lb_data = [l for l in lb if not l.startswith(("43\t", "63\t"))]
    la_data = [l for l in la if not l.startswith(("43\t", "63\t"))]
    out.append("LEGACY_ROWS_UNCHANGED_EXCEPT_FLYWAY_LINE=%s" % (lb_data == la_data))
    for line in la_data:
        if line not in lb_data:
            out.append("  LEGACY_NEW_LINE %s" % line)
    for line in lb_data:
        if line not in la_data:
            out.append("  LEGACY_GONE_LINE %s" % line)
    with io.open(os.path.join(DB, "post-migration-results.txt"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(l + "\n" for l in out))
    print("\n".join(out))


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "fingerprint":
        fingerprint(sys.argv[2], sys.argv[3])
    elif command == "compare-final12":
        compare_final12(sys.argv[2])
    elif command == "compare":
        compare(sys.argv[2], sys.argv[3])
    elif command == "post-migration":
        post_migration(sys.argv[2], sys.argv[3], sys.argv[4])

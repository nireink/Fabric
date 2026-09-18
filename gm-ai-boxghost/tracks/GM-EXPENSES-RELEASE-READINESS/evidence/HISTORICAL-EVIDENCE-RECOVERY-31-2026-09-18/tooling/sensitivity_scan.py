"""STEP 31 §5 (read-only): sensitivity scan of every non-dump file in the restricted STEP 18 folder. Only COUNTS per
pattern category are printed - never a matched value or a line. Writes sensitivity-scan.tsv next to this script."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FABRIC = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric"
props = open(os.path.join(FABRIC, r"Knowledge\00-GYPPORT-UNIVERSE\GYPPORT_LOCATIONS.properties"), encoding="utf-8").read()
STORAGE = next(l.split("=", 1)[1].strip() for l in props.splitlines() if l.startswith("GYPPORT_STORAGE_ROOT="))
R18 = os.path.join(STORAGE, "Restricted", "Gystigo", "shared-dev-deployment-18-2026-09-17")
PATTERNS = {
    "generated_password_line": re.compile(r"Using generated security password"),
    "password_value": re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token)\b[\"']?\s*[:=]\s*[\"']?(?!\$|<|\*|\{|\s|[\"'],|redacted|REDACTED)[^\s\"',}]{6,}"),
    "credential_env": re.compile(r"(?i)(MYSQL_ROOT_PASSWORD|SPRING_DATASOURCE_PASSWORD|MYSQL_PASSWORD)\s*=\s*[^\s\"'$]{3,}"),
    "password_hash": re.compile(r"\$2[aby]\$\d{2}\$[./A-Za-z0-9]{20,}|\$argon2"),
    "jwt": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    "cookie_value": re.compile(r"(?i)\b(SESSION|JSESSIONID|XSRF-TOKEN)=[A-Za-z0-9%_-]{8,}"),
    "url_credentials": re.compile(r"[a-z][a-z0-9+.-]*://[^/\s:@'\"]+:[^/\s@'\"]{3,}@"),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36}"),
}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
OWNER_DATA = re.compile(r"Compra Filtro|VIAJE QUITO|Viaje Loja|Viaje Zamora|SUSCRIPCION IA|Compra Camaras|PRUEBA20260909|Viaje los encuentros|Viaje A Loja")

rows = []
for d, _, files in os.walk(R18):
    for f in sorted(files):
        p = os.path.join(d, f)
        rel = os.path.relpath(p, R18).replace(os.sep, "/")
        if rel.endswith(".sql") and "/" not in rel:
            continue  # the dump itself: never scanned into output, never promoted
        text = open(p, "rb").read().decode("utf-8", "replace")
        counts = {k: len(rx.findall(text)) for k, rx in PATTERNS.items()}
        emails = EMAIL.findall(text)
        counts["email_example_test"] = sum(1 for e in emails if e.lower().endswith("@example.test"))
        counts["email_other"] = sum(1 for e in emails if not e.lower().endswith("@example.test"))
        counts["owner_business_data"] = len(OWNER_DATA.findall(text))
        rows.append((rel, os.path.getsize(p), counts))
keys = list(PATTERNS) + ["email_example_test", "email_other", "owner_business_data"]
with open(os.path.join(HERE, "sensitivity-scan.tsv"), "w", newline="\n", encoding="utf-8") as out:
    out.write("relative_path\tbytes\t" + "\t".join(keys) + "\n")
    for rel, size, c in rows:
        out.write("%s\t%d\t%s\n" % (rel, size, "\t".join(str(c[k]) for k in keys)))
flagged = 0
for rel, size, c in rows:
    hits = {k: v for k, v in c.items() if v and k != "email_example_test"}
    if hits:
        flagged += 1
        print("%-52s %6d %s" % (rel, size, " ".join("%s=%d" % kv for kv in hits.items())))
print("SCANNED=%d FLAGGED=%d CLEAN=%d" % (len(rows), flagged, len(rows) - flagged))
print("FILES_WITH_EXAMPLE_TEST_EMAILS_ONLY=%d" % sum(1 for _, _, c in rows if c["email_example_test"] and not c["email_other"]))

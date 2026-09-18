"""GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - derive the deployment smoke from the accepted FINAL_12 smoke (f12-runtime-smoke.ps1):
same assertions, pointed at the official DEV backend (127.0.0.1:8080) and DEV Mailpit (8025), with clearly identifiable S18
synthetic records, a 5xx counter and the extra STEP 18 checks. Output is a UTF-8 BOM script for Windows PowerShell 5.1."""
import io, os

S18 = os.path.dirname(os.path.abspath(__file__))
SRC = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-EXPENSES-RELEASE-READINESS\evidence\RUNTIME-REHEARSAL-FINAL-12-2026-09-17\f12-runtime-smoke.ps1"
text = io.open(SRC, encoding="utf-8-sig").read().replace("\r\n", "\n")
smoke_dir = os.path.join(S18, "smoke")
os.makedirs(smoke_dir, exist_ok=True)


def sub(old, new, count=1):
    global text
    found = text.count(old)
    if found != count:
        raise SystemExit("expected %d occurrence(s) of %r, found %d" % (count, old, found))
    text = text.replace(old, new)


sub("# GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 - final runtime smoke against the rehearsal backend only\n"
    "# (127.0.0.1:18084 -> disposable Shared DEV copy 127.0.0.1:3314 migrated to V63; Mailpit 127.0.0.1:8026).\n"
    "# Synthetic @example.test accounts, each in its own tenant. Never 8080/3310 (Owner runtime) and never 3308 (Shared DEV).\n",
    "# GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 - deployment smoke against the official DEV backend (127.0.0.1:8080 -> Shared DEV V63;\n"
    "# DEV Mailpit 127.0.0.1:8025). Derived from the accepted FINAL_12 smoke: same assertions plus the STEP 18 checks.\n"
    "# Synthetic @example.test accounts, each in its own tenant, and records named S18 so they stay identifiable. No legacy data is touched.\n")
sub("$api = 'http://127.0.0.1:18084'; $mailpit = 'http://127.0.0.1:8026'", "$api = 'http://127.0.0.1:8080'; $mailpit = 'http://127.0.0.1:8025'")
sub("$scratch = 'C:\\Users\\elbur\\AppData\\Local\\Temp\\claude\\D--NZXTG7-GYPPORT-GYPPORT-ERP\\6bd391c2-9dd7-4c98-8f41-546e5a9baea1\\scratchpad'",
    "$scratch = '%s'" % smoke_dir)
sub("$ids = [ordered]@{}", "$ids = [ordered]@{}\n$server5xx = 0; $server5xxCalls = New-Object System.Collections.Generic.List[string]")
sub("    $response = $s.Client.SendAsync($request).GetAwaiter().GetResult()\n",
    "    $response = $s.Client.SendAsync($request).GetAwaiter().GetResult()\n"
    "    if ([int]$response.StatusCode -ge 500) { $script:server5xx++; $script:server5xxCalls.Add(\"$method $path $([int]$response.StatusCode)\") }\n")
sub("\"runtime-smoke-f12$tag-", "\"deploy-smoke-s18$tag-")
sub("'Rs-Smoke-'", "'Ds-Smoke-'")
sub("firstSurname = \"SmokeF12$tag\"", "firstSurname = \"SmokeS18$tag\"")
sub("displayName = \"F12 Responsable $tag\"", "displayName = \"S18 Responsable $tag\"")
sub("primaryEmail = \"f12-$tag-", "primaryEmail = \"s18-$tag-")
sub("    $s.LoginStatus = $login.Status\n", "    $s.LoginStatus = $login.Status\n    $s.Email = $email\n")
sub("activityDescription = \"F12 tramo $amount\"", "activityDescription = \"S18 tramo $amount\"")
sub("reason = 'F12 smoke'", "reason = 'S18 deployment smoke'")
text = text.replace("New-Case $a '", "New-Case $a 'S18 ").replace("New-Case $z '", "New-Case $z 'S18 ")
text = text.replace("Join-Path $scratch 'f12-", "Join-Path $scratch 's18-")
sub("$results.Add(\"F12_RUNTIME_CHECKS=$($results.Count) FAILURES=$failures\")",
    "$results.Add(\"S18_SERVER_5XX=$server5xx [$($server5xxCalls -join '; ')]\")\n"
    "$results.Add(\"S18_DEPLOY_CHECKS=$($results.Count - 1) FAILURES=$failures\")")

# STEP 18 additions
sub("Check 'synthetic session, tenant A' ($a.LoginStatus -eq 200 -and [bool]$a.Xsrf -and [bool]$a.Responsible) \"login=$($a.LoginStatus)\"\n",
    "Check 'synthetic session, tenant A' ($a.LoginStatus -eq 200 -and [bool]$a.Xsrf -and [bool]$a.Responsible) \"login=$($a.LoginStatus)\"\n"
    "$anonymous = New-Session; $anonymousMe = Send $anonymous 'GET' '/auth/me' $null; $meA = Send $a 'GET' '/auth/me' $null\n"
    "Check 'S18 authentication path reachable (anonymous /auth/me 401) and tenant context for the session' ($anonymousMe.Status -eq 401 -and $meA.Status -eq 200 -and ($meA.Text -match '\"tenant')) \"anonymous=$($anonymousMe.Status) me=$($meA.Status)\"\n"
    "$ids['account:a'] = $a.Email; $ids['me:a'] = $meA.Text\n")
sub("# ---- §16 zero-advance Case in its own tenant: numbers only, in the Case and in the reports\n",
    "# ---- S18 edit a REGISTRADO expense before review (own Case, after the report sums)\n"
    "$cEdit = New-Case $a 'S18 Edición de gasto registrado'\n"
    "$eEdit = Registered $a $cEdit '40'\n"
    "$edit = Send $a 'POST' \"/api/expenses/$eEdit/edit\" @{ operationId = (Op); expectedVersion = (Expense $a $eEdit).version; categoryScope = 'GLOBAL'; categoryCode = 'ALIMENTACION'; amount = '45'; currency = 'USD'; expenseDate = $today; description = 'S18 editado' }\n"
    "$afterEdit = Expense $a $eEdit\n"
    "Check 'S18 a REGISTRADO expense is edited before review' ($edit.Status -eq 200 -and $afterEdit.status -eq 'REGISTRADO' -and [decimal]$afterEdit.amount.amount -eq 45) \"edit=$($edit.Status) status=$($afterEdit.status) amount=$($afterEdit.amount.amount)\"\n"
    "$historyTypes = @(@($e2Detail.reviewHistory) | ForEach-Object eventType)\n"
    "Check 'S18 review-history API: the corrected expense carries SUBMITTED, OBSERVED, CORRECTION_SUBMITTED and ACCEPTED' ((@('SUBMITTED','OBSERVED','CORRECTION_SUBMITTED','ACCEPTED') | Where-Object { $historyTypes -notcontains $_ }).Count -eq 0 -and $historyTypes.Count -eq 4) \"history=$($historyTypes -join ',')\"\n"
    "$listCasesA = Send $a 'GET' '/api/expense-cases?page=0&pageSize=50' $null; $listAdvancesA = Send $a 'GET' '/api/expense-advances' $null; $listExpensesA = Send $a 'GET' '/api/expenses' $null\n"
    "Check 'S18 Expenses list and read APIs answer for the tenant' ($listCasesA.Status -eq 200 -and @($listCasesA.Json.items).Count -ge 10 -and $listAdvancesA.Status -eq 200 -and @($listAdvancesA.Json.items).Count -ge 1 -and $listExpensesA.Status -eq 200 -and @($listExpensesA.Json.items).Count -ge 1) \"cases=$($listCasesA.Status)/$(@($listCasesA.Json.items).Count) advances=$($listAdvancesA.Status)/$(@($listAdvancesA.Json.items).Count) expenses=$($listExpensesA.Status)/$(@($listExpensesA.Json.items).Count)\"\n\n"
    "# ---- §16 zero-advance Case in its own tenant: numbers only, in the Case and in the reports\n")
sub("$z = Login 'z'\n", "$z = Login 'z'\n$ids['account:z'] = $z.Email\n")
sub("$b = Login 'b'\n", "$b = Login 'b'\n$ids['account:b'] = $b.Email\n")
for forbidden in ("18084", "8026", "3314", "3310", "3308"):
    if forbidden in text:
        raise SystemExit("forbidden target %s left in the smoke script" % forbidden)
out = os.path.join(S18, "s18-deploy-smoke.ps1")
with open(out, "wb") as handle:
    handle.write(b"\xef\xbb\xbf" + text.replace("\n", "\r\n").encode("utf-8"))
print("SMOKE_SCRIPT=%s lines=%d checks=%d" % (out, text.count("\n"), text.count("\nCheck '")))

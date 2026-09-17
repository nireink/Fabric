# GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11 - live smoke against the local runtime only
# (127.0.0.1:8080 -> isolated copy 127.0.0.1:3310 at V63; Mailpit 8026). Synthetic @example.test accounts, each in its own tenant.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Net.Http
$api = 'http://127.0.0.1:8080'; $mailpit = 'http://127.0.0.1:8026'
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\4bbfc1ff-e737-4ade-bbb8-169c21a07560\scratchpad'
$results = New-Object System.Collections.Generic.List[string]; $failures = 0
$managedByCase = 'La rendición de este anticipo se gestiona desde su expediente.'
function New-Session {
    $handler = New-Object System.Net.Http.HttpClientHandler; $handler.UseCookies = $false
    $client = New-Object System.Net.Http.HttpClient($handler); $client.Timeout = [TimeSpan]::FromSeconds(60)
    return @{ Client = $client; Cookies = @{}; Xsrf = $null }
}
function Send($s, [string]$method, [string]$path, $body) {
    $request = New-Object System.Net.Http.HttpRequestMessage((New-Object System.Net.Http.HttpMethod($method)), ($api + $path))
    if ($s.Cookies.Count -gt 0) { $request.Headers.Add('Cookie', (($s.Cookies.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join '; ')) }
    if ($s.Xsrf -and $method -ne 'GET') { $request.Headers.Add('X-XSRF-TOKEN', $s.Xsrf) }
    if ($null -ne $body) {
        $json = if ($body -is [string]) { $body } else { $body | ConvertTo-Json -Depth 10 -Compress }
        $request.Content = New-Object System.Net.Http.StringContent($json, [System.Text.Encoding]::UTF8, 'application/json')
    }
    $response = $s.Client.SendAsync($request).GetAwaiter().GetResult()
    $text = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    $values = $null
    if ($response.Headers.TryGetValues('Set-Cookie', [ref]$values)) {
        foreach ($cookie in $values) { $pair = ($cookie -split ';')[0]; $name, $value = $pair -split '=', 2
            if ([string]::IsNullOrEmpty($value)) { $s.Cookies.Remove($name) } else { $s.Cookies[$name] = $value }
            if ($name -eq 'XSRF-TOKEN') { $s.Xsrf = [Uri]::UnescapeDataString($value) } }
    }
    $parsed = $null; if ($text -and $text.TrimStart().StartsWith('{')) { try { $parsed = $text | ConvertFrom-Json } catch { } }
    return [pscustomobject]@{ Status = [int]$response.StatusCode; Text = $text; Json = $parsed }
}
function Check([string]$label, [bool]$ok, [string]$detail) { if (-not $ok) { $script:failures++ }; $results.Add(("{0,-4} {1} :: {2}" -f $(if ($ok) { 'PASS' } else { 'FAIL' }), $label, $detail)) }
function Op { [guid]::NewGuid().ToString() }
function Login([string]$tag) {
    $s = New-Session
    $email = "runtime-smoke-s11$tag-$([guid]::NewGuid().ToString('N').Substring(0,8))@example.test"; $password = 'Rs-Smoke-' + [guid]::NewGuid().ToString('N')
    $null = Send $s 'POST' '/auth/register' @{ firstName = 'Runtime'; firstSurname = "SmokeS11$tag"; email = $email; password = $password }
    $code = $null
    for ($i = 0; $i -lt 40 -and -not $code; $i++) { Start-Sleep -Milliseconds 500
        $list = (Invoke-WebRequest -UseBasicParsing -Uri "$mailpit/api/v1/messages?limit=50").Content | ConvertFrom-Json
        $message = $list.messages | Where-Object { $_.To | Where-Object { $_.Address -eq $email } } | Select-Object -First 1
        if ($message) { $detail = (Invoke-WebRequest -UseBasicParsing -Uri "$mailpit/api/v1/message/$($message.ID)").Content | ConvertFrom-Json; if ($detail.Text -match 'es:\s*(\S+)') { $code = $Matches[1] } } }
    $null = Send $s 'POST' '/auth/email-verification/verify' @{ identifier = $email; code = $code }
    $login = Send $s 'POST' '/auth/login' @{ identifier = $email; password = $password }
    $null = Send $s 'GET' '/api/expense-persons' $null
    $s.LoginStatus = $login.Status
    return $s
}
function New-Case($s, [string]$name) {
    $responsible = (Send $s 'POST' '/api/expense-persons' @{ operationId = (Op); displayName = 'S11 Responsable'; primaryEmail = "s11-$([guid]::NewGuid().ToString('N').Substring(0,8))@example.test" }).Json.reference
    return (Send $s 'POST' '/api/expense-cases' ('{"operationId":"' + (Op) + '","name":"' + $name + '","responsibleId":"' + $responsible + '","advanceId":null,"resources":[]}')).Json.caseId
}
function Add-Advance($s, [string]$caseId, [string]$amount) {
    return Send $s 'POST' "/api/expense-cases/$caseId/advances" @{ operationId = (Op); activityType = 'VIAJE'; activityDescription = "S11 tramo $amount"; amount = $amount; currency = 'USD'; deliveryMethodCode = 'EFECTIVO'; renditionDays = 7 }
}
function Deliver($s, [string]$advanceId) { return Send $s 'POST' "/api/expense-advances/$advanceId/deliver" @{ operationId = (Op); expectedVersion = 0 } }
function Approved($s, [string]$caseId, [string]$amount) {
    $expenseId = (Send $s 'POST' "/api/expense-cases/$caseId/expenses" @{ operationId = (Op); categoryScope = 'GLOBAL'; categoryCode = 'ALIMENTACION'; amount = $amount; currency = 'USD'; expenseDate = '2026-09-16'; description = "S11 gasto $amount" }).Json.expenseId
    $version = (Send $s 'GET' "/api/expenses/$expenseId" $null).Json.version
    $submit = Send $s 'POST' "/api/expenses/$expenseId/submit" @{ operationId = (Op); expectedVersion = $version }
    $version = (Send $s 'GET' "/api/expenses/$expenseId" $null).Json.version
    $accept = Send $s 'POST' "/api/expenses/$expenseId/accept" @{ operationId = (Op); expectedVersion = $version }
    return "$($submit.Status)/$($accept.Status)"
}
function Detail($s, [string]$caseId) { return (Send $s 'GET' "/api/expense-cases/$caseId" $null).Json }
function Rendition($s, [string]$caseId) { return @((Detail $s $caseId).renditions)[0] }
function Close($s, [string]$caseId) { return Send $s 'POST' "/api/expense-cases/$caseId/close" @{ operationId = (Op); expectedVersion = (Detail $s $caseId).version } }
function Movement($s, [string]$caseId, [string]$kind, [string]$amount, $version) {
    if ($null -eq $version) { $version = (Rendition $s $caseId).version }
    return Send $s 'POST' "/api/expense-cases/$caseId/rendition/$kind" @{ operationId = (Op); expectedRenditionVersion = $version; amount = $amount; currency = 'USD'; reason = 'S11 smoke' }
}
function Reconcile($s, [string]$caseId) { return Send $s 'POST' "/api/expense-cases/$caseId/rendition/reconcile" @{ operationId = (Op); currency = 'USD'; expectedRenditionVersion = (Rendition $s $caseId).version } }

$a = Login 'a'
Check 'synthetic session A' ($a.LoginStatus -eq 200 -and [bool]$a.Xsrf) "login=$($a.LoginStatus)"

# §13: four funding tranches, one approved total, one return, Conciliar, Cerrar expediente.
$c13 = New-Case $a 'S11 smoke - cuatro tramos'
$tranches = @('30000', '2000', '300', '5000') | ForEach-Object { (Add-Advance $a $c13 $_).Json.advanceId }
$delivered = @($tranches | ForEach-Object { (Deliver $a $_).Status })
$approvals = @((Approved $a $c13 '20000'), (Approved $a $c13 '15000'))
$raw = (Send $a 'GET' "/api/expense-cases/$c13" $null).Text
$r = Rendition $a $c13
Check '§13 tranches delivered and expenses approved on the Case' (($delivered -join ',') -eq '200,200,200,200' -and ($approvals -join ',') -eq '200/200,200/200') "deliver=$($delivered -join ',') approvals=$($approvals -join ',')"
Check '§13 one Case rendition: delivered 37300, justified 35000, 2300 to return, Conciliar not yet offered' ([decimal]$r.delivered.amount -eq 37300 -and [decimal]$r.justified.amount -eq 35000 -and [decimal]$r.pendingReturn.amount -eq 2300 -and -not $r.canReconcile -and $r.canRegisterReturn) "status=$($r.status) delivered=$($r.delivered.amount) justified=$($r.justified.amount) pendingReturn=$($r.pendingReturn.amount) canReconcile=$($r.canReconcile)"
Check '§18 C no advance carries a rendition, a settlement or a Resumen per advance' (-not ($raw -match '"rendition"|settlementId|settlementVersion|renditionSummary')) 'case detail JSON scanned'
$close = Close $a $c13
Check '§10 an unbalanced Case does not close' ($close.Status -eq 400 -and $close.Json.message -eq 'La rendición del expediente tiene saldo pendiente; registra la devolución o el reembolso y vuelve a conciliar.') "close=$($close.Status) message=$($close.Json.message)"
$ret = Movement $a $c13 'returns' '2300' $null
$r = Rendition $a $c13
Check '§13 the return of 2300 balances the Case and offers Conciliar' ($ret.Status -eq 200 -and [decimal]$r.returned.amount -eq 2300 -and [decimal]$r.pendingReturn.amount -eq 0 -and [decimal]$r.pendingReimbursement.amount -eq 0 -and $r.canReconcile) "return=$($ret.Status) status=$($r.status) canReconcile=$($r.canReconcile)"
$close = Close $a $c13
Check '§10 a balanced Case still needs Conciliar before closing' ($close.Status -eq 400 -and $close.Json.message -eq 'Concilia la rendición del expediente antes de cerrarlo.') "close=$($close.Status) message=$($close.Json.message)"
$legacy = Send $a 'GET' "/api/expense-advances/$($tranches[0])/settlement" $null
$legacyOpen = Send $a 'POST' "/api/expense-advances/$($tranches[1])/settlement" @{ operationId = (Op); expectedAdvanceVersion = 2 }
Check '§8 the per-advance settlement API refuses a Case advance, reads included' ($legacy.Status -eq 400 -and $legacy.Json.message -eq $managedByCase -and $legacyOpen.Status -eq 400 -and $legacyOpen.Json.message -eq $managedByCase) "get=$($legacy.Status) open=$($legacyOpen.Status)"
$rec = Reconcile $a $c13
$r = Rendition $a $c13
Check '§13 Conciliar reconciles the Case' ($rec.Status -eq 200 -and $r.status -eq 'CONCILIADO' -and -not $r.canReconcile) "reconcile=$($rec.Status) status=$($r.status)"
$close = Close $a $c13
$final = Detail $a $c13
$advanceStatuses = (@($final.advances) | ForEach-Object status) -join ','
Check '§11/§13 Cerrar expediente closes the Case and every funding advance' ($close.Status -eq 200 -and $final.status -eq 'CERRADO' -and $advanceStatuses -eq 'CERRADO,CERRADO,CERRADO,CERRADO' -and @($final.renditions)[0].status -eq 'CERRADO') "close=$($close.Status) case=$($final.status) advances=$advanceStatuses rendition=$(@($final.renditions)[0].status)"
$advance = Send $a 'GET' "/api/expense-advances/$($tranches[0])" $null
Check '§7 the Advance page says its rendition is managed by the Case, with no rendition of its own' ($advance.Status -eq 200 -and $advance.Json.renditionManagedByCase -eq $true -and -not ($advance.Text -match '"rendition"')) "advance=$($advance.Status) managedByCase=$($advance.Json.renditionManagedByCase)"

# §14: an additional advance after expenses only adds to what the Case received; §11: the draft blocker copy.
$c14 = New-Case $a 'S11 smoke - tramo adicional'
$firstTranche = (Add-Advance $a $c14 '30000').Json.advanceId
$null = Deliver $a $firstTranche
$approval = Approved $a $c14 '29500'
$before = Rendition $a $c14
$extra = (Add-Advance $a $c14 '2000').Json.advanceId
$draftView = Rendition $a $c14
$close = Close $a $c14
Check '§11 a draft blocks the close with its count and amount' ($close.Status -eq 400 -and $close.Json.message -eq 'Hay 1 anticipo en borrador por USD 2000.00. Confirma su entrega o cancélalo antes de cerrar el expediente.') "close=$($close.Status) message=$($close.Json.message)"
$null = Deliver $a $extra
$after = Rendition $a $c14
$stale = Movement $a $c14 'returns' '10' $before.version
Check '§14 delivered 30000 -> 32000, justified 29500, 500 -> 2500 to return; nothing reassigned, older views stale' ($approval -eq '200/200' -and [decimal]$before.delivered.amount -eq 30000 -and [decimal]$before.pendingReturn.amount -eq 500 -and [decimal]$draftView.delivered.amount -eq 30000 -and [decimal]$after.delivered.amount -eq 32000 -and [decimal]$after.justified.amount -eq 29500 -and [decimal]$after.pendingReturn.amount -eq 2500 -and $stale.Status -eq 409) "before=$($before.delivered.amount)/$($before.pendingReturn.amount) draft=$($draftView.delivered.amount) after=$($after.delivered.amount)/$($after.justified.amount)/$($after.pendingReturn.amount) stale=$($stale.Status)"

# §15: per-Case directions stay separate in the reports (+30 and -20, never a net 10).
$cA = New-Case $a 'S11 smoke - por justificar'
$null = Deliver $a (Add-Advance $a $cA '100').Json.advanceId
$null = Approved $a $cA '70'
$cB = New-Case $a 'S11 smoke - por reembolsar'
$null = Deliver $a (Add-Advance $a $cB '100').Json.advanceId
$null = Approved $a $cB '80'
$giveBack = Movement $a $cB 'returns' '20' $null
$null = Approved $a $cB '20'
$rA = Rendition $a $cA; $rB = Rendition $a $cB
$today = [DateTime]::UtcNow.Date
$period = Send $a 'GET' ("/api/expense-reports/period-summary?from=" + $today.AddDays(-1).ToString('yyyy-MM-dd') + "&to=" + $today.AddDays(1).ToString('yyyy-MM-dd')) $null
$usd = @($period.Json.currencies) | Where-Object { $_.currency -eq 'USD' }
Check '§15 Case A is +30 and Case B is -20 on their own renditions' ([decimal]$rA.pendingReturn.amount -eq 30 -and $giveBack.Status -eq 200 -and [decimal]$rB.pendingReimbursement.amount -eq 20 -and [decimal]$rB.pendingReturn.amount -eq 0) "A=$($rA.pendingReturn.amount) B=$($rB.pendingReimbursement.amount)"
Check '§15 the report adds per-Case directions apart: 2500 + 30 to return and 20 to reimburse' ($period.Status -eq 200 -and [decimal]$usd.pendingReturn -eq 2530 -and [decimal]$usd.pendingReimbursement -eq 20 -and [decimal]$usd.delivered -eq 69500 -and [decimal]$usd.justified -eq 64670) "report=$($period.Status) delivered=$($usd.delivered) justified=$($usd.justified) pendingReturn=$($usd.pendingReturn) pendingReimbursement=$($usd.pendingReimbursement)"

# §17.12: another tenant neither reads nor moves the Case rendition.
$b = Login 'b'
$foreignRead = Send $b 'GET' "/api/expense-cases/$cA" $null
$foreignReturn = Send $b 'POST' "/api/expense-cases/$cA/rendition/returns" @{ operationId = (Op); expectedRenditionVersion = $rA.version; amount = '10'; currency = 'USD' }
$foreignReconcile = Send $b 'POST' "/api/expense-cases/$cA/rendition/reconcile" @{ operationId = (Op); currency = 'USD'; expectedRenditionVersion = $rA.version }
$rAafter = Rendition $a $cA
Check '§17.12 tenant isolation of the Case rendition' ($b.LoginStatus -eq 200 -and $foreignRead.Status -eq 404 -and $foreignReturn.Status -eq 404 -and $foreignReconcile.Status -eq 404 -and $rAafter.version -eq $rA.version) "read=$($foreignRead.Status) return=$($foreignReturn.Status) reconcile=$($foreignReconcile.Status) version=$($rAafter.version)"

$results.Add("CASES=$c13,$c14,$cA,$cB")
$results.Add("S11_RUNTIME_CHECKS=$($results.Count - 1) FAILURES=$failures")
$results | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $scratch 's11-runtime-smoke-results.txt')
$results

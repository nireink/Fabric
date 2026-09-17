# GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12 - final runtime smoke against the rehearsal backend only
# (127.0.0.1:18084 -> disposable Shared DEV copy 127.0.0.1:3314 migrated to V63; Mailpit 127.0.0.1:8026).
# Synthetic @example.test accounts, each in its own tenant. Never 8080/3310 (Owner runtime) and never 3308 (Shared DEV).
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Net.Http
$api = 'http://127.0.0.1:18084'; $mailpit = 'http://127.0.0.1:8026'
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\6bd391c2-9dd7-4c98-8f41-546e5a9baea1\scratchpad'
$results = New-Object System.Collections.Generic.List[string]; $failures = 0
$ids = [ordered]@{}
$managedByCase = 'La rendición de este anticipo se gestiona desde su expediente.'
$unbalancedCopy = 'La rendición del expediente tiene saldo pendiente; registra la devolución o el reembolso y vuelve a conciliar.'
$notReconciledCopy = 'Concilia la rendición del expediente antes de cerrarlo.'
$today = (Get-Date).ToString('yyyy-MM-dd')
$from = [DateTime]::UtcNow.Date.AddDays(-1).ToString('yyyy-MM-dd'); $to = [DateTime]::UtcNow.Date.AddDays(1).ToString('yyyy-MM-dd')

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
    $parsed = $null; if ($text -and ($text.TrimStart().StartsWith('{') -or $text.TrimStart().StartsWith('['))) { try { $parsed = $text | ConvertFrom-Json } catch { } }
    return [pscustomobject]@{ Status = [int]$response.StatusCode; Text = $text; Json = $parsed }
}
function Check([string]$label, [bool]$ok, [string]$detail) { if (-not $ok) { $script:failures++ }; $results.Add(("{0,-4} {1} :: {2}" -f $(if ($ok) { 'PASS' } else { 'FAIL' }), $label, $detail)) }
function Op { [guid]::NewGuid().ToString() }
function Amount($money) { if ($null -eq $money) { return [decimal]::MinValue }; return [decimal]$money.amount }
function Login([string]$tag) {
    $s = New-Session
    $email = "runtime-smoke-f12$tag-$([guid]::NewGuid().ToString('N').Substring(0,8))@example.test"; $password = 'Rs-Smoke-' + [guid]::NewGuid().ToString('N')
    $null = Send $s 'POST' '/auth/register' @{ firstName = 'Runtime'; firstSurname = "SmokeF12$tag"; email = $email; password = $password }
    $code = $null
    for ($i = 0; $i -lt 40 -and -not $code; $i++) { Start-Sleep -Milliseconds 500
        $list = (Invoke-WebRequest -UseBasicParsing -Uri "$mailpit/api/v1/messages?limit=50").Content | ConvertFrom-Json
        $message = $list.messages | Where-Object { $_.To | Where-Object { $_.Address -eq $email } } | Select-Object -First 1
        if ($message) { $detail = (Invoke-WebRequest -UseBasicParsing -Uri "$mailpit/api/v1/message/$($message.ID)").Content | ConvertFrom-Json; if ($detail.Text -match 'es:\s*(\S+)') { $code = $Matches[1] } } }
    $null = Send $s 'POST' '/auth/email-verification/verify' @{ identifier = $email; code = $code }
    $login = Send $s 'POST' '/auth/login' @{ identifier = $email; password = $password }
    $null = Send $s 'GET' '/api/expense-persons' $null
    $s.LoginStatus = $login.Status
    $s.Responsible = (Send $s 'POST' '/api/expense-persons' @{ operationId = (Op); displayName = "F12 Responsable $tag"; primaryEmail = "f12-$tag-$([guid]::NewGuid().ToString('N').Substring(0,8))@example.test" }).Json.reference
    return $s
}
function New-Case($s, [string]$name) {
    $response = Send $s 'POST' '/api/expense-cases' ('{"operationId":"' + (Op) + '","name":"' + $name + '","responsibleId":"' + $s.Responsible + '","advanceId":null,"resources":[]}')
    $script:ids["case:$name"] = $response.Json.caseId
    return $response.Json.caseId
}
function Add-Advance($s, [string]$caseId, [string]$amount) {
    return Send $s 'POST' "/api/expense-cases/$caseId/advances" @{ operationId = (Op); activityType = 'VIAJE'; activityDescription = "F12 tramo $amount"; amount = $amount; currency = 'USD'; deliveryMethodCode = 'EFECTIVO'; renditionDays = 7 }
}
function Deliver($s, [string]$advanceId) { return Send $s 'POST' "/api/expense-advances/$advanceId/deliver" @{ operationId = (Op); expectedVersion = 0 } }
function Delivered-Advance($s, [string]$caseId, [string]$amount) { $id = (Add-Advance $s $caseId $amount).Json.advanceId; $null = Deliver $s $id; return $id }
function Expense($s, [string]$expenseId) { return (Send $s 'GET' "/api/expenses/$expenseId" $null).Json }
function Registered($s, [string]$caseId, [string]$amount) {
    return (Send $s 'POST' "/api/expense-cases/$caseId/expenses" @{ operationId = (Op); categoryScope = 'GLOBAL'; categoryCode = 'ALIMENTACION'; amount = $amount; currency = 'USD'; expenseDate = $today; description = "F12 gasto $amount" }).Json.expenseId
}
function Submit($s, [string]$id) { return Send $s 'POST' "/api/expenses/$id/submit" @{ operationId = (Op); expectedVersion = (Expense $s $id).version } }
function Accept($s, [string]$id) { return Send $s 'POST' "/api/expenses/$id/accept" @{ operationId = (Op); expectedVersion = (Expense $s $id).version } }
function Approved($s, [string]$caseId, [string]$amount) { $id = Registered $s $caseId $amount; $null = Submit $s $id; $null = Accept $s $id; return $id }
function Detail($s, [string]$caseId) { return (Send $s 'GET' "/api/expense-cases/$caseId" $null) }
function Rendition($s, [string]$caseId) { return @((Detail $s $caseId).Json.renditions)[0] }
function Close($s, [string]$caseId) { return Send $s 'POST' "/api/expense-cases/$caseId/close" @{ operationId = (Op); expectedVersion = (Detail $s $caseId).Json.version } }
function Movement($s, [string]$caseId, [string]$kind, [string]$amount) {
    return Send $s 'POST' "/api/expense-cases/$caseId/rendition/$kind" @{ operationId = (Op); expectedRenditionVersion = (Rendition $s $caseId).version; amount = $amount; currency = 'USD'; reason = 'F12 smoke' }
}
function Reconcile($s, [string]$caseId) { return Send $s 'POST' "/api/expense-cases/$caseId/rendition/reconcile" @{ operationId = (Op); currency = 'USD'; expectedRenditionVersion = (Rendition $s $caseId).version } }
function Shape([string]$text) { return -not ($text -match '"rendition"|settlementId|settlementVersion|renditionSummary|expectedSettlementVersion') }

$a = Login 'a'
Check 'synthetic session, tenant A' ($a.LoginStatus -eq 200 -and [bool]$a.Xsrf -and [bool]$a.Responsible) "login=$($a.LoginStatus)"

# ---- §9 Construcción: four same-currency funding tranches, one approved total, one return, Conciliar, Cerrar expediente
$c9 = New-Case $a 'Construcción'
$created9 = @('30000', '2000', '300', '5000') | ForEach-Object { Add-Advance $a $c9 $_ }
$tranches9 = @($created9 | ForEach-Object { $_.Json.advanceId })
$delivered9 = @($tranches9 | ForEach-Object { (Deliver $a $_).Status })
Check '§9 four USD advances allowed in one Case and delivered' ((@($created9 | ForEach-Object Status) -join ',') -eq '201,201,201,201' -and ($delivered9 -join ',') -eq '200,200,200,200' -and -not ((@($created9 | ForEach-Object Text) -join ' ') -match 'anticipo activo')) "create=$((@($created9 | ForEach-Object Status)) -join ',') deliver=$($delivered9 -join ',')"
$null = Approved $a $c9 '20000'; $null = Approved $a $c9 '15000'
$d9 = Detail $a $c9; $r9 = @($d9.Json.renditions)[0]
Check '§9 Case totals: delivered 37300, justified 35000, 2300 to return, Conciliar not offered yet' ([decimal]$r9.delivered.amount -eq 37300 -and [decimal]$r9.justified.amount -eq 35000 -and [decimal]$r9.pendingReturn.amount -eq 2300 -and -not $r9.canReconcile -and @($d9.Json.renditions).Count -eq 1 -and (Shape $d9.Text)) "delivered=$($r9.delivered.amount) justified=$($r9.justified.amount) pendingReturn=$($r9.pendingReturn.amount) renditions=$(@($d9.Json.renditions).Count)"
$ret9 = Movement $a $c9 'returns' '2300'; $r9 = Rendition $a $c9
Check '§9 the Case-level return balances the Case and offers Conciliar' ($ret9.Status -eq 200 -and [decimal]$r9.pendingReturn.amount -eq 0 -and [decimal]$r9.pendingReimbursement.amount -eq 0 -and $r9.canReconcile) "return=$($ret9.Status) status=$($r9.status) canReconcile=$($r9.canReconcile)"
$rec9 = Reconcile $a $c9; $close9 = Close $a $c9; $final9 = (Detail $a $c9).Json
Check '§9 Conciliar and Cerrar expediente close the Case and every funding advance' ($rec9.Status -eq 200 -and $close9.Status -eq 200 -and $final9.status -eq 'CERRADO' -and ((@($final9.advances) | ForEach-Object status) -join ',') -eq 'CERRADO,CERRADO,CERRADO,CERRADO' -and @($final9.renditions)[0].status -eq 'CERRADO') "reconcile=$($rec9.Status) close=$($close9.Status) advances=$((@($final9.advances) | ForEach-Object status) -join ',')"
$ids['advance:Construcción:30000'] = $tranches9[0]

# ---- §10 an additional advance after approvals only adds funding
$c10 = New-Case $a 'Tramo adicional'
$null = Delivered-Advance $a $c10 '30000'
$null = Approved $a $c10 '29500'
$before10 = Rendition $a $c10
$extra10 = (Add-Advance $a $c10 '2000').Json.advanceId
$draft10 = Rendition $a $c10
$deliver10 = Deliver $a $extra10
$after10 = Rendition $a $c10
$stale10 = Send $a 'POST' "/api/expense-cases/$c10/rendition/returns" @{ operationId = (Op); expectedRenditionVersion = $before10.version; amount = '10'; currency = 'USD' }
Check '§10 delivered 30000 -> 32000, justified stays 29500, 500 -> 2500 to return, older views stale' ([decimal]$before10.delivered.amount -eq 30000 -and [decimal]$before10.pendingReturn.amount -eq 500 -and [decimal]$draft10.delivered.amount -eq 30000 -and $deliver10.Status -eq 200 -and [decimal]$after10.delivered.amount -eq 32000 -and [decimal]$after10.justified.amount -eq 29500 -and [decimal]$after10.pendingReturn.amount -eq 2500 -and $stale10.Status -eq 409) "before=$($before10.delivered.amount)/$($before10.pendingReturn.amount) after=$($after10.delivered.amount)/$($after10.justified.amount)/$($after10.pendingReturn.amount) stale=$($stale10.Status)"

# ---- §11 return, later approval, reimbursement (V63 at Case level)
$c11 = New-Case $a 'Devolución y reembolso'
$null = Delivered-Advance $a $c11 '150'; $null = Delivered-Advance $a $c11 '50'
$null = Approved $a $c11 '180'
$ret11 = Movement $a $c11 'returns' '20'; $rec11a = Reconcile $a $c11
$late11 = Registered $a $c11 '20'; $null = Submit $a $late11; $acceptLate11 = Accept $a $late11
$owed11 = Rendition $a $c11
$refusedReturn11 = Movement $a $c11 'returns' '20'
$reimburse11 = Movement $a $c11 'reimbursements' '20'
$rec11b = Reconcile $a $c11; $close11 = Close $a $c11; $final11 = @((Detail $a $c11).Json.renditions)[0]
Check '§11 a later approval is allowed after a real return and opens a Case-level reimbursement' ($ret11.Status -eq 200 -and $rec11a.Status -eq 200 -and $acceptLate11.Status -eq 200 -and $owed11.status -eq 'ABIERTO' -and [decimal]$owed11.pendingReimbursement.amount -eq 20 -and $owed11.canRegisterReimbursement -and $refusedReturn11.Status -eq 400) "accept=$($acceptLate11.Status) status=$($owed11.status) owed=$($owed11.pendingReimbursement.amount) refusedReturn=$($refusedReturn11.Status)"
Check '§11 the reimbursement balances the Case, Conciliar and close succeed, both movements persist' ($reimburse11.Status -eq 200 -and $rec11b.Status -eq 200 -and $close11.Status -eq 200 -and $final11.status -eq 'CERRADO' -and [decimal]$final11.returned.amount -eq 20 -and [decimal]$final11.reimbursed.amount -eq 20 -and [decimal]$final11.justified.amount -eq 200) "reimburse=$($reimburse11.Status) reconcile=$($rec11b.Status) close=$($close11.Status) returned=$($final11.returned.amount) reimbursed=$($final11.reimbursed.amount)"

# ---- §12 drafts: several allowed, delivery beside other advances, closure copy plural then singular, blocker disappears
$c12 = New-Case $a 'Borradores'
$null = Delivered-Advance $a $c12 '100'
$null = Approved $a $c12 '100'
$null = Reconcile $a $c12
$draftA = Add-Advance $a $c12 '50'; $draftB = Add-Advance $a $c12 '25'
$plural = Close $a $c12
$cancelB = Send $a 'POST' "/api/expense-advances/$($draftB.Json.advanceId)/cancel" @{ operationId = (Op); expectedVersion = 0 }
$singular = Close $a $c12
$deliverA = Deliver $a $draftA.Json.advanceId
$afterDrafts = Close $a $c12
Check '§12 several drafts are allowed beside a delivered advance' ($draftA.Status -eq 201 -and $draftB.Status -eq 201) "draftA=$($draftA.Status) draftB=$($draftB.Status)"
Check '§12 closure refused with the plural copy' ($plural.Status -eq 400 -and $plural.Json.message -eq 'Hay 2 anticipos en borrador por un total de USD 75.00. Confirma su entrega o cancélalos antes de cerrar el expediente.') "close=$($plural.Status) message=$($plural.Json.message)"
Check '§12 after cancelling one draft, the singular copy' ($cancelB.Status -eq 200 -and $singular.Status -eq 400 -and $singular.Json.message -eq 'Hay 1 anticipo en borrador por USD 50.00. Confirma su entrega o cancélalo antes de cerrar el expediente.') "cancel=$($cancelB.Status) close=$($singular.Status) message=$($singular.Json.message)"
Check '§12 delivering the last draft beside the others removes the draft blocker' ($deliverA.Status -eq 200 -and $afterDrafts.Status -eq 400 -and $afterDrafts.Json.message -eq $unbalancedCopy) "deliver=$($deliverA.Status) next_blocker=$($afterDrafts.Json.message)"
$null = Movement $a $c12 'returns' '50'; $null = Reconcile $a $c12; $close12 = Close $a $c12
Check '§12 once balanced and reconciled the Case closes' ($close12.Status -eq 200 -and (Detail $a $c12).Json.status -eq 'CERRADO') "close=$($close12.Status)"

# ---- §13 / §14 expense workflows and every closure blocker, on one Case
$c13 = New-Case $a 'Flujo de gastos y bloqueos'
$null = Delivered-Advance $a $c13 '200'
$e1 = Registered $a $c13 '80'; $e1Registered = (Expense $a $e1).status
$blockA = Close $a $c13
$null = Submit $a $e1; $e1Pending = (Expense $a $e1).status
$blockB = Close $a $c13
$acceptE1 = Accept $a $e1; $e1Final = (Expense $a $e1).status
$e2 = Registered $a $c13 '30'; $null = Submit $a $e2
$observe = Send $a 'POST' "/api/expenses/$e2/observe" @{ operationId = (Op); expectedVersion = (Expense $a $e2).version; reasonCode = 'FALTA_COMPROBANTE'; detail = 'Adjunta la factura' }
$e2Observed = (Expense $a $e2).status
$blockC = Close $a $c13
$correct = Send $a 'POST' "/api/expenses/$e2/correct-observed" @{ operationId = (Op); expectedVersion = (Expense $a $e2).version; categoryScope = 'GLOBAL'; categoryCode = 'ALIMENTACION'; amount = '35'; currency = 'USD'; expenseDate = $today; description = 'F12 corregido'; reason = 'Factura adjunta' }
$e2Corrected = (Expense $a $e2).status
$acceptE2 = Accept $a $e2; $e2Detail = Expense $a $e2
$e3 = Registered $a $c13 '50'; $null = Submit $a $e3
$reject = Send $a 'POST' "/api/expenses/$e3/reject" @{ operationId = (Op); expectedVersion = (Expense $a $e3).version; reasonCode = 'GASTO_DUPLICADO'; detail = 'Mismo comprobante' }
$acceptRejected = Accept $a $e3
$correctRejected = Send $a 'POST' "/api/expenses/$e3/correct-observed" @{ operationId = (Op); expectedVersion = (Expense $a $e3).version; categoryScope = 'GLOBAL'; categoryCode = 'ALIMENTACION'; amount = '50'; currency = 'USD'; expenseDate = $today; description = 'F12 rechazado'; reason = 'Intento' }
$e3Detail = Expense $a $e3
$e4 = Registered $a $c13 '20'; $null = Submit $a $e4
$mid13 = (Detail $a $c13).Json; $mid13Summary = @($mid13.financialSummary)[0]; $mid13Rendition = @($mid13.renditions)[0]
Check '§13 REGISTRADO -> PENDIENTE_REVISION -> APROBADO' ($e1Registered -eq 'REGISTRADO' -and $e1Pending -eq 'PENDIENTE_REVISION' -and $acceptE1.Status -eq 200 -and $e1Final -eq 'APROBADO') "$e1Registered -> $e1Pending -> $e1Final"
Check '§13 OBSERVADO -> correction -> PENDIENTE_REVISION -> APROBADO with its review history' ($observe.Status -eq 200 -and $e2Observed -eq 'OBSERVADO' -and $correct.Status -eq 200 -and $e2Corrected -eq 'PENDIENTE_REVISION' -and $acceptE2.Status -eq 200 -and $e2Detail.status -eq 'APROBADO' -and [decimal]$e2Detail.amount.amount -eq 35 -and @($e2Detail.reviewHistory).Count -eq 4) "observed=$e2Observed corrected=$e2Corrected final=$($e2Detail.status) amount=$($e2Detail.amount.amount) history=$((@($e2Detail.reviewHistory) | ForEach-Object eventType) -join ',')"
Check '§13 RECHAZADO is terminal: approval and correction refused' ($reject.Status -eq 200 -and $e3Detail.status -eq 'RECHAZADO' -and $acceptRejected.Status -ge 400 -and $acceptRejected.Status -lt 500 -and $correctRejected.Status -ge 400 -and $correctRejected.Status -lt 500) "reject=$($reject.Status) accept=$($acceptRejected.Status) correct=$($correctRejected.Status) status=$($e3Detail.status)"
Check '§13 justified counts APROBADO only; Usado excludes the rejected expense' ([decimal]$mid13Rendition.justified.amount -eq 115 -and [decimal]$mid13Summary.spent.amount -eq 135 -and [decimal]$mid13Summary.justified.amount -eq 115) "justified=$($mid13Rendition.justified.amount) used=$($mid13Summary.spent.amount)"
$null = Accept $a $e4
$draft13 = Add-Advance $a $c13 '40'
$blockD = Close $a $c13
$null = Send $a 'POST' "/api/expense-advances/$($draft13.Json.advanceId)/cancel" @{ operationId = (Op); expectedVersion = 0 }
$blockE = Close $a $c13
$pending13 = Rendition $a $c13
$null = Movement $a $c13 'returns' ([string]$pending13.pendingReturn.amount)
$blockF = Close $a $c13
$rec13 = Reconcile $a $c13; $close13 = Close $a $c13
Check '§14 A REGISTRADO blocks the close' ($blockA.Status -eq 400 -and $blockA.Json.message -eq 'El expediente tiene gastos registrados sin enviar a revisión.') "message=$($blockA.Json.message)"
Check '§14 B PENDIENTE_REVISION blocks the close' ($blockB.Status -eq 400 -and $blockB.Json.message -eq 'El expediente tiene gastos pendientes de aprobación.') "message=$($blockB.Json.message)"
Check '§14 C OBSERVADO blocks the close' ($blockC.Status -eq 400 -and $blockC.Json.message -eq 'El expediente tiene gastos observados pendientes de corrección.') "message=$($blockC.Json.message)"
Check '§14 D BORRADOR blocks the close' ($blockD.Status -eq 400 -and $blockD.Json.message -eq 'Hay 1 anticipo en borrador por USD 40.00. Confirma su entrega o cancélalo antes de cerrar el expediente.') "message=$($blockD.Json.message)"
Check '§14 E a balance other than 0 blocks the close' ($blockE.Status -eq 400 -and $blockE.Json.message -eq $unbalancedCopy -and [decimal]$pending13.pendingReturn.amount -eq 65) "pendingReturn=$($pending13.pendingReturn.amount) message=$($blockE.Json.message)"
Check '§14 F a balanced but unreconciled Case does not close' ($blockF.Status -eq 400 -and $blockF.Json.message -eq $notReconciledCopy) "message=$($blockF.Json.message)"
Check '§14 with every blocker resolved Conciliar and the close succeed' ($rec13.Status -eq 200 -and $close13.Status -eq 200 -and (Detail $a $c13).Json.status -eq 'CERRADO') "reconcile=$($rec13.Status) close=$($close13.Status)"

# ---- §15 presentation data: closed 679/200/200/499/20 and open overuse 1000/1100
$c15 = New-Case $a 'Viaje Loja (ensayo final)'
$null = Delivered-Advance $a $c15 '479'; $null = Delivered-Advance $a $c15 '200'
$null = Approved $a $c15 '180'
$null = Movement $a $c15 'returns' '499'; $null = Reconcile $a $c15
$null = Approved $a $c15 '20'
$null = Movement $a $c15 'reimbursements' '20'; $null = Reconcile $a $c15
$close15 = Close $a $c15
$c15b = New-Case $a 'Sobreuso'
$null = Delivered-Advance $a $c15b '1000'
$null = Approved $a $c15b '1100'
$list = (Send $a 'GET' '/api/expense-cases?page=0&pageSize=50' $null).Json.items
$card15 = @(($list | Where-Object { $_.caseId -eq $c15 }).financialSummary)[0]
$card15b = @(($list | Where-Object { $_.caseId -eq $c15b }).financialSummary)[0]
$usage15 = [math]::Round([decimal]$card15.spent.amount / [decimal]$card15.delivered.amount * 100)
$usage15b = [math]::Round([decimal]$card15b.spent.amount / [decimal]$card15b.delivered.amount * 100)
Check '§15 closed Case card data: 679 delivered, 200 used and justified, 499 returned, 20 reimbursed, nothing pending (Conciliado 100%, Uso 29%)' ($close15.Status -eq 200 -and [decimal]$card15.delivered.amount -eq 679 -and [decimal]$card15.spent.amount -eq 200 -and [decimal]$card15.justified.amount -eq 200 -and [decimal]$card15.returned.amount -eq 499 -and [decimal]$card15.reimbursed.amount -eq 20 -and [decimal]$card15.pendingReturn.amount -eq 0 -and [decimal]$card15.pendingReimbursement.amount -eq 0 -and $usage15 -eq 29) "close=$($close15.Status) usage=$usage15%"
Check '§15 open overuse card data: Uso 110% with 100 to reimburse' ([decimal]$card15b.delivered.amount -eq 1000 -and [decimal]$card15b.spent.amount -eq 1100 -and $usage15b -eq 110 -and [decimal]$card15b.pendingReimbursement.amount -eq 100) "usage=$usage15b% pendingReimbursement=$($card15b.pendingReimbursement.amount)"
$list | ConvertTo-Json -Depth 12 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $scratch 'f12-tenant-a-case-list.json')

# ---- §17 per-Case directions, then reports (+30 and -20 never net)
$cPlus = New-Case $a 'Por justificar'
$null = Delivered-Advance $a $cPlus '100'; $null = Approved $a $cPlus '70'; $null = Registered $a $cPlus '15'
$cMinus = New-Case $a 'Por reembolsar'
$null = Delivered-Advance $a $cMinus '100'; $null = Approved $a $cMinus '80'
$null = Movement $a $cMinus 'returns' '20'; $null = Approved $a $cMinus '20'
$renditionsA = @($list | ForEach-Object caseId) + @($cPlus, $cMinus) | Sort-Object -Unique | ForEach-Object { Rendition $a $_ } | Where-Object { $_ }
$sum = { param($field) ($renditionsA | ForEach-Object { [decimal]$_.$field.amount } | Measure-Object -Sum).Sum }
$period = Send $a 'GET' "/api/expense-reports/period-summary?from=$from&to=$to" $null
$usd = @($period.Json.currencies) | Where-Object { $_.currency -eq 'USD' }
$usedA = (@((Send $a 'GET' '/api/expense-cases?page=0&pageSize=50' $null).Json.items) | ForEach-Object { @($_.financialSummary) } | ForEach-Object { [decimal]$_.spent.amount } | Measure-Object -Sum).Sum
Check '§17 period summary equals the per-Case totals and never nets directions' ($period.Status -eq 200 -and [decimal]$usd.delivered -eq (& $sum 'delivered') -and [decimal]$usd.justified -eq (& $sum 'justified') -and [decimal]$usd.returned -eq (& $sum 'returned') -and [decimal]$usd.reimbursed -eq (& $sum 'reimbursed') -and [decimal]$usd.pendingReturn -eq (& $sum 'pendingReturn') -and [decimal]$usd.pendingReimbursement -eq (& $sum 'pendingReimbursement') -and [decimal]$usd.used -eq $usedA -and [decimal]$usd.pendingReturn -eq 2530 -and [decimal]$usd.pendingReimbursement -eq 120) "delivered=$($usd.delivered) used=$($usd.used) justified=$($usd.justified) returned=$($usd.returned) reimbursed=$($usd.reimbursed) pendingReturn=$($usd.pendingReturn) pendingReimbursement=$($usd.pendingReimbursement)"
$categories = Send $a 'GET' "/api/expense-reports?from=$from&to=$to" $null
$query = Send $a 'GET' "/api/expense-reports/detail?criterion=CATEGORY&target=ALIMENTACION&categoryScope=GLOBAL&from=$from&to=$to" $null
$vehicleTotals = Send $a 'GET' "/api/expense-reports/vehicle-totals?from=$from&to=$to" $null
$resources = Send $a 'GET' '/api/expense-reports/resources' $null
$related = @($query.Json.relatedCaseFunding) | Where-Object { $_.currency -eq 'USD' }
Check '§17 categories, query with related Cases, vehicles and resources answer' ($categories.Status -eq 200 -and $query.Status -eq 200 -and @($query.Json.lines).Count -ge 1 -and [decimal]$related.pendingReturn -eq 2530 -and [decimal]$related.pendingReimbursement -eq 120 -and $vehicleTotals.Status -eq 200 -and $resources.Status -eq 200) "categories=$($categories.Status) query=$($query.Status) lines=$(@($query.Json.lines).Count) related=$($related.pendingReturn)/$($related.pendingReimbursement) vehicles=$($vehicleTotals.Status) resources=$($resources.Status)"

# ---- §16 zero-advance Case in its own tenant: numbers only, in the Case and in the reports
$z = Login 'z'
$cZero = New-Case $z 'Sin anticipo entregado'
$zeroDraft = Add-Advance $z $cZero '50'
$null = Approved $z $cZero '260'
$zDetail = Detail $z $cZero; $zSummary = @($zDetail.Json.financialSummary)[0]
Check '§16 Case detail without a delivered advance: Usado 260 and every funding amount 0, no rendition yet' ($zeroDraft.Status -eq 201 -and -not $zSummary.hasDeliveredAdvance -and [decimal]$zSummary.delivered.amount -eq 0 -and [decimal]$zSummary.spent.amount -eq 260 -and [decimal]$zSummary.justified.amount -eq 0 -and [decimal]$zSummary.returned.amount -eq 0 -and [decimal]$zSummary.reimbursed.amount -eq 0 -and [decimal]$zSummary.pendingReturn.amount -eq 0 -and [decimal]$zSummary.pendingReimbursement.amount -eq 0 -and @($zDetail.Json.renditions).Count -eq 0) "used=$($zSummary.spent.amount) delivered=$($zSummary.delivered.amount) renditions=$(@($zDetail.Json.renditions).Count)"
$zPeriod = Send $z 'GET' "/api/expense-reports/period-summary?from=$from&to=$to" $null
$zUsd = @($zPeriod.Json.currencies) | Where-Object { $_.currency -eq 'USD' }
$zQuery = Send $z 'GET' "/api/expense-reports/detail?criterion=CATEGORY&target=ALIMENTACION&categoryScope=GLOBAL&from=$from&to=$to" $null
$zRelated = @($zQuery.Json.relatedCaseFunding) | Where-Object { $_.currency -eq 'USD' }
Check '§16 report values without a delivered advance are numbers: delivered 0, used 260, the rest 0' ($zPeriod.Status -eq 200 -and [decimal]$zUsd.delivered -eq 0 -and [decimal]$zUsd.used -eq 260 -and [decimal]$zUsd.justified -eq 0 -and [decimal]$zUsd.returned -eq 0 -and [decimal]$zUsd.reimbursed -eq 0 -and [decimal]$zUsd.pendingReturn -eq 0 -and [decimal]$zUsd.pendingReimbursement -eq 0 -and [decimal]$zRelated.used -eq 260 -and [decimal]$zRelated.delivered -eq 0 -and -not ($zPeriod.Text -match 'No aplica') -and -not ($zQuery.Text -match 'No aplica')) "period=$($zPeriod.Text)"
$zPeriod.Text | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $scratch 'f12-zero-tenant-period-summary.json')
$zRelated | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $scratch 'f12-zero-tenant-related-funding.json')
$zDetail.Text | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $scratch 'f12-zero-tenant-case-detail.json')

# ---- §18 Advance detail: history only, the rendition managed by the Case
$advance18 = Send $a 'GET' "/api/expense-advances/$($tranches9[0])" $null
Check '§18 advance detail keeps its history and names no rendition of its own' ($advance18.Status -eq 200 -and $advance18.Json.renditionManagedByCase -eq $true -and $advance18.Json.status -eq 'CERRADO' -and [bool]$advance18.Json.delivery.deliveredAt -and (Shape $advance18.Text) -and -not ($advance18.Text -match '"justified"|"returned"|"reimbursed"|"pendingReturn"')) "status=$($advance18.Json.status) managedByCase=$($advance18.Json.renditionManagedByCase)"

# ---- §21 the per-advance settlement API refuses a Case advance (deliberate probes, counted apart in the access log)
$legacyGet = Send $a 'GET' "/api/expense-advances/$($tranches9[1])/settlement" $null
$legacyOpen = Send $a 'POST' "/api/expense-advances/$extra10/settlement" @{ operationId = (Op); expectedAdvanceVersion = 2 }
Check '§21 per-advance settlement API refused for Case advances (2 deliberate probes)' ($legacyGet.Status -eq 400 -and $legacyGet.Json.message -eq $managedByCase -and $legacyOpen.Status -eq 400 -and $legacyOpen.Json.message -eq $managedByCase) "get=$($legacyGet.Status) open=$($legacyOpen.Status)"

# ---- §19 tenant isolation
$b = Login 'b'
$e1b = Send $b 'GET' "/api/expenses/$e1" $null
$bResponses = [ordered]@{
    'case' = Send $b 'GET' "/api/expense-cases/$c10" $null
    'advance' = Send $b 'GET' "/api/expense-advances/$extra10" $null
    'expense' = $e1b
    'return' = Send $b 'POST' "/api/expense-cases/$c10/rendition/returns" @{ operationId = (Op); expectedRenditionVersion = $after10.version; amount = '1'; currency = 'USD' }
    'reimbursement' = Send $b 'POST' "/api/expense-cases/$cMinus/rendition/reimbursements" @{ operationId = (Op); expectedRenditionVersion = (Rendition $a $cMinus).version; amount = '1'; currency = 'USD' }
    'reconcile' = Send $b 'POST' "/api/expense-cases/$c10/rendition/reconcile" @{ operationId = (Op); currency = 'USD'; expectedRenditionVersion = $after10.version }
    'close' = Send $b 'POST' "/api/expense-cases/$c10/close" @{ operationId = (Op); expectedVersion = 0 }
    'addAdvance' = Send $b 'POST' "/api/expense-cases/$c10/advances" @{ operationId = (Op); activityType = 'VIAJE'; activityDescription = 'intruso'; amount = '1'; currency = 'USD'; deliveryMethodCode = 'EFECTIVO'; renditionDays = 7 }
    'addExpense' = Send $b 'POST' "/api/expense-cases/$c10/expenses" @{ operationId = (Op); categoryScope = 'GLOBAL'; categoryCode = 'ALIMENTACION'; amount = '1'; currency = 'USD'; expenseDate = $today }
    'cancel' = Send $b 'POST' "/api/expense-advances/$($draftA.Json.advanceId)/cancel" @{ operationId = (Op); expectedVersion = 1 }
    'submit' = Send $b 'POST' "/api/expenses/$e4/submit" @{ operationId = (Op); expectedVersion = 3 }
}
$statuses = ($bResponses.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value.Status)" }) -join ' '
$bCases = @((Send $b 'GET' '/api/expense-cases' $null).Json.items)
$bAdvances = @((Send $b 'GET' '/api/expense-advances' $null).Json.items)
$bExpenses = @((Send $b 'GET' '/api/expenses' $null).Json.items)
$bPeriod = @((Send $b 'GET' "/api/expense-reports/period-summary?from=$from&to=$to" $null).Json.currencies)
$bQuery = @((Send $b 'GET' "/api/expense-reports/detail?criterion=CATEGORY&target=ALIMENTACION&categoryScope=GLOBAL&from=$from&to=$to" $null).Json.lines)
$allNotFound = @($bResponses.Values | Where-Object { $_.Status -ne 404 }).Count -eq 0
$after10Check = Rendition $a $c10
Check '§19 tenant B reads and mutates nothing of tenant A (404 on every record, empty lists and reports)' ($b.LoginStatus -eq 200 -and $allNotFound -and $bCases.Count -eq 0 -and $bAdvances.Count -eq 0 -and $bExpenses.Count -eq 0 -and @($bPeriod | Where-Object { [decimal]$_.delivered -gt 0 -or [decimal]$_.used -gt 0 }).Count -eq 0 -and $bQuery.Count -eq 0 -and $after10Check.version -eq $after10.version) "$statuses lists=$($bCases.Count)/$($bAdvances.Count)/$($bExpenses.Count) reports=$($bPeriod.Count)/$($bQuery.Count)"

$ids['case:Construcción'] = $c9; $ids['case:Tramo adicional'] = $c10
$ids | ConvertTo-Json | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $scratch 'f12-smoke-ids.json')
$results.Add("F12_RUNTIME_CHECKS=$($results.Count) FAILURES=$failures")
$results | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $scratch 'f12-runtime-smoke-results.txt')
$results

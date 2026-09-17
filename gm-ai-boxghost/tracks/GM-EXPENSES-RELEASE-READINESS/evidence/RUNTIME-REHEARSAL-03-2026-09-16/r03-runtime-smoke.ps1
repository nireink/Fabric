# GM_EXPENSES_RUNTIME_REHEARSAL_03 - real workflow smoke against the rehearsal backend only
# (127.0.0.1:18082 -> disposable Shared DEV copy 127.0.0.1:3312 at V63; Mailpit 8026). Synthetic accounts in their own tenants.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Net.Http
$api = 'http://127.0.0.1:18082'; $mailpit = 'http://127.0.0.1:8026'
$results = New-Object System.Collections.Generic.List[string]; $failures = 0
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
function Amount($money) { return [decimal]$money.amount }
function Login([string]$tag) {
    $s = New-Session
    $email = "rehearsal03-$tag-$([guid]::NewGuid().ToString('N').Substring(0,8))@example.test"; $password = 'Rh-Smoke-' + [guid]::NewGuid().ToString('N')
    $null = Send $s 'POST' '/auth/register' @{ firstName = 'Rehearsal'; firstSurname = "Smoke$tag"; email = $email; password = $password }
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
$today = (Get-Date).ToString('yyyy-MM-dd')
$from = (Get-Date).ToUniversalTime().AddDays(-1).ToString('yyyy-MM-dd'); $to = (Get-Date).ToUniversalTime().AddDays(1).ToString('yyyy-MM-dd')

$a = Login 'a'
Check 'synthetic session (tenant A)' ($a.LoginStatus -eq 200 -and [bool]$a.Xsrf) "login=$($a.LoginStatus)"
$responsible = (Send $a 'POST' '/api/expense-persons' @{ operationId = (Op); displayName = 'R03 Responsable'; primaryEmail = "r03-$([guid]::NewGuid().ToString('N').Substring(0,8))@example.test" }).Json.reference
function New-Case($s, [string]$name) { return (Send $s 'POST' '/api/expense-cases' ('{"operationId":"' + (Op) + '","name":"' + $name + '","responsibleId":"' + $responsible + '","advanceId":null,"resources":[]}')) }
function Get-Case($s, [string]$caseId) { return (Send $s 'GET' "/api/expense-cases/$caseId" $null).Json }
function Version($s, [string]$expenseId) { return (Send $s 'GET' "/api/expenses/$expenseId" $null).Json.version }
function Registered($s, [string]$caseId, [string]$amount) {
    return (Send $s 'POST' "/api/expense-cases/$caseId/expenses" @{ operationId = (Op); categoryScope = 'GLOBAL'; categoryCode = 'ALIMENTACION'; amount = $amount; currency = 'USD'; expenseDate = $today; description = 'R03 smoke' }).Json.expenseId
}
function Submit($s, [string]$id) { return Send $s 'POST' "/api/expenses/$id/submit" @{ operationId = (Op); expectedVersion = (Version $s $id) } }
function Accept($s, [string]$id) { return Send $s 'POST' "/api/expenses/$id/accept" @{ operationId = (Op); expectedVersion = (Version $s $id) } }
function Approved($s, [string]$caseId, [string]$amount) { $id = Registered $s $caseId $amount; $null = Submit $s $id; $null = Accept $s $id; return $id }
function Rendition($s, [string]$caseId) { return (Get-Case $s $caseId).advances[0].rendition }
function Movement($s, [string]$caseId, [string]$advanceId, [string]$kind, [string]$amount) {
    $version = (Rendition $s $caseId).settlementVersion
    $body = @{ operationId = (Op); amount = $amount; currency = 'USD'; reason = 'R03 smoke' }
    if ($null -ne $version) { $body.expectedSettlementVersion = $version }
    return Send $s 'POST' "/api/expense-cases/$caseId/advances/$advanceId/rendition/$kind" $body
}
function Reconcile($s, [string]$caseId, [string]$advanceId) {
    $version = (Rendition $s $caseId).settlementVersion
    $body = @{ operationId = (Op) }; if ($null -ne $version) { $body.expectedSettlementVersion = $version }
    return Send $s 'POST' "/api/expense-cases/$caseId/advances/$advanceId/rendition/reconcile" $body
}

# 1. ExpenseCase -> Advance window 1 -> window 2 -> BORRADOR summary
$created = New-Case $a 'R03 smoke - viaje con rendición'
$r1 = $created.Json.caseId
$openCases = (Send $a 'GET' '/api/expense-cases' $null).Json.items
Check 'ExpenseCase created and offered to Nuevo anticipo window 1 (open Cases)' ($created.Status -eq 201 -and ($openCases | Where-Object { $_.caseId -eq $r1 -and $_.status -eq 'ABIERTO' })) "status=$($created.Status) open=$(@($openCases).Count)"
$adv = Send $a 'POST' "/api/expense-cases/$r1/advances" @{ operationId = (Op); activityType = 'VIAJE'; activityDescription = 'R03 viaje'; amount = '150'; currency = 'USD'; deliveryMethodCode = 'EFECTIVO'; renditionDays = 7 }
$a1 = $adv.Json.advanceId
$draft = (Send $a 'GET' "/api/expense-advances/$a1" $null).Json
Check 'window 2 registers the draft with its plan; BORRADOR summary reads names' ($adv.Status -eq 201 -and $draft.status -eq 'BORRADOR' -and $draft.plannedDelivery.deliveryMethodCode -eq 'EFECTIVO' -and $draft.caseName -and ($draft.registeredByName -isnot [int] -and $draft.registeredByName -isnot [long])) "status=$($adv.Status) advance=$($draft.status) registeredBy=$($draft.registeredByName)"
$second = Send $a 'POST' "/api/expense-cases/$r1/advances" @{ operationId = (Op); activityType = 'VIAJE'; activityDescription = 'R03 segundo'; amount = '20'; currency = 'USD'; deliveryMethodCode = 'EFECTIVO'; renditionDays = 7 }
Check 'one financially active advance per Case and currency (S06 copy)' ($second.Status -eq 400 -and $second.Json.message -eq 'Este expediente ya tiene un anticipo activo en USD. Resuelve el anticipo actual antes de registrar otro.') "status=$($second.Status) message=$($second.Json.message)"

# 2. B: Confirmar entrega never takes deliveredByPersonReference; the actor is the session account
$legacyBody = Send $a 'POST' "/api/expense-advances/$a1/deliver" @{ operationId = (Op); expectedVersion = 0; deliveredByPersonReference = $responsible }
$deliver = Send $a 'POST' "/api/expense-advances/$a1/deliver" @{ operationId = (Op); expectedVersion = 0 }
$delivered = (Send $a 'GET' "/api/expense-advances/$a1" $null).Json
Check 'B Confirmar entrega refuses deliveredByPersonReference and delivers without it' ($legacyBody.Status -eq 400 -and $deliver.Status -eq 200 -and $delivered.status -eq 'ENTREGADO' -and $delivered.delivery.deliveredAt) "legacyBody=$($legacyBody.Status) deliver=$($deliver.Status) status=$($delivered.status) confirmedBy=$($delivered.deliveryConfirmedByName)"

# 3. A and C: BORRADOR -> CANCELADO through the real /cancel route
$r2 = (New-Case $a 'R03 smoke - anticipo cancelado').Json.caseId
$a2 = (Send $a 'POST' "/api/expense-cases/$r2/advances" @{ operationId = (Op); activityType = 'COMPRA'; activityDescription = 'R03 cancelado'; amount = '40'; currency = 'USD'; deliveryMethodCode = 'TRANSFERENCIA'; renditionDays = 5 }).Json.advanceId
$cancel = Send $a 'POST' "/api/expense-advances/$a2/cancel" @{ operationId = (Op); expectedVersion = 0 }
$cancelled = (Send $a 'GET' "/api/expense-advances/$a2" $null).Json
Check 'A BORRADOR -> CANCELADO' ($cancel.Status -eq 200 -and $cancelled.status -eq 'CANCELADO') "cancel=$($cancel.Status) status=$($cancelled.status)"
$cancelDelivered = Send $a 'POST' "/api/expense-advances/$a1/cancel" @{ operationId = (Op); expectedVersion = 1 }
$unmapped = Send $a 'POST' "/api/expense-advances/$a1/not-a-route" @{ operationId = (Op) }
Check 'C /cancel is a mapped route (business 400 on a delivered advance; an unmapped route answers 401)' ($cancelDelivered.Status -eq 400 -and $unmapped.Status -eq 401) "cancelDelivered=$($cancelDelivered.Status) message=$($cancelDelivered.Json.message) unmapped=$($unmapped.Status)"

# 4. Expense registration -> review (observe/correct, approve, reject) -> justified total
$e1 = Registered $a $r1 '80'; $null = Submit $a $e1; $acceptE1 = Accept $a $e1
$e2 = Registered $a $r1 '30'; $null = Submit $a $e2
$observe = Send $a 'POST' "/api/expenses/$e2/observe" @{ operationId = (Op); expectedVersion = (Version $a $e2); reasonCode = 'FALTA_COMPROBANTE'; detail = 'Adjunta la factura' }
$correct = Send $a 'POST' "/api/expenses/$e2/correct-observed" @{ operationId = (Op); expectedVersion = (Version $a $e2); categoryScope = 'GLOBAL'; categoryCode = 'ALIMENTACION'; amount = '35'; currency = 'USD'; expenseDate = $today; description = 'R03 corregido'; reason = 'Factura adjunta' }
$acceptE2 = Accept $a $e2
$e3 = Registered $a $r1 '50'; $null = Submit $a $e3
$reject = Send $a 'POST' "/api/expenses/$e3/reject" @{ operationId = (Op); expectedVersion = (Version $a $e3); reasonCode = 'GASTO_DUPLICADO'; detail = 'Mismo comprobante' }
$e2Detail = (Send $a 'GET' "/api/expenses/$e2" $null).Json; $e3Detail = (Send $a 'GET' "/api/expenses/$e3" $null).Json
Check 'review: APROBADO, OBSERVADO -> corrected -> APROBADO, RECHAZADO with history' ($acceptE1.Status -eq 200 -and $observe.Status -eq 200 -and $correct.Status -eq 200 -and $acceptE2.Status -eq 200 -and $reject.Status -eq 200 -and $e2Detail.status -eq 'APROBADO' -and @($e2Detail.reviewHistory).Count -eq 4 -and $e3Detail.status -eq 'RECHAZADO' -and @($e3Detail.reviewHistory).Count -eq 2) "e2=$($e2Detail.status)/$(@($e2Detail.reviewHistory).Count) e3=$($e3Detail.status)/$(@($e3Detail.reviewHistory).Count) events=$((@($e2Detail.reviewHistory) | ForEach-Object eventType) -join ',')"
$r = Rendition $a $r1
Check 'justified total = approved expenses only (80 + 35)' ((Amount $r.justified) -eq 115 -and (Amount $r.pendingReturn) -eq 35) "justified=$($r.justified.amount) pendingReturn=$($r.pendingReturn.amount)"

# 5. return -> reconcile -> close ExpenseCase
$return = Movement $a $r1 $a1 'returns' '35'; $rec = Reconcile $a $r1 $a1
$close = Send $a 'POST' "/api/expense-cases/$r1/close" @{ operationId = (Op); expectedVersion = (Get-Case $a $r1).version }
$closedCase = Get-Case $a $r1
Check 'return -> Conciliar -> Cerrar expediente closes the rendition and the advance' ($return.Status -eq 200 -and $rec.Status -eq 200 -and $close.Status -eq 200 -and $closedCase.status -eq 'CERRADO' -and $closedCase.advances[0].status -eq 'CERRADO' -and $closedCase.advances[0].rendition.status -eq 'CERRADO') "return=$($return.Status) reconcile=$($rec.Status) close=$($close.Status) case=$($closedCase.status)"

# 6. V63 on the migrated lineage: real return, later approval, reimbursement, close
$r3 = (New-Case $a 'R03 smoke - devolución y reembolso').Json.caseId
$a3 = (Send $a 'POST' "/api/expense-cases/$r3/advances" @{ operationId = (Op); activityType = 'VIAJE'; activityDescription = 'R03 V63'; amount = '200'; currency = 'USD'; deliveryMethodCode = 'EFECTIVO'; renditionDays = 7 }).Json.advanceId
$null = Send $a 'POST' "/api/expense-advances/$a3/deliver" @{ operationId = (Op); expectedVersion = 0 }
$null = Approved $a $r3 '180'; $null = Movement $a $r3 $a3 'returns' '20'; $null = Reconcile $a $r3 $a3
$null = Approved $a $r3 '20'
$owed = Rendition $a $r3
$reimburse = Movement $a $r3 $a3 'reimbursements' '20'; $rec3 = Reconcile $a $r3 $a3
$close3 = Send $a 'POST' "/api/expense-cases/$r3/close" @{ operationId = (Op); expectedVersion = (Get-Case $a $r3).version }
$final3 = (Get-Case $a $r3).advances[0].rendition
Check 'V63: return 20 + later approval -> Por reembolsar 20 -> reimbursement -> reconciled and closed' ((Amount $owed.pendingReimbursement) -eq 20 -and [bool]$owed.canRegisterReimbursement -and $reimburse.Status -eq 200 -and $rec3.Status -eq 200 -and $close3.Status -eq 200 -and $final3.status -eq 'CERRADO' -and (Amount $final3.returned) -eq 20 -and (Amount $final3.reimbursed) -eq 20) "owed=$($owed.pendingReimbursement.amount) reimburse=$($reimburse.Status) close=$($close3.Status) final=$($final3.status)"

# 7. Reports
$period = Send $a 'GET' "/api/expense-reports/period-summary?from=$from&to=$to" $null
$usd = $period.Json.currencies | Where-Object { $_.currency -eq 'USD' }
$totals = Send $a 'GET' "/api/expense-reports?from=$from&to=$to" $null
$query = Send $a 'GET' "/api/expense-reports/detail?criterion=CATEGORY&from=$from&to=$to" $null
$vehicles = Send $a 'GET' "/api/expense-reports/vehicle-totals?from=$from&to=$to" $null
$categories = Send $a 'GET' '/api/expense-reports/categories' $null
Check 'reports: period summary on justified amounts (per-Case directions), totals, query, vehicles, categories' ($period.Status -eq 200 -and [decimal]$usd.delivered -eq 350 -and [decimal]$usd.used -eq 315 -and [decimal]$usd.justified -eq 315 -and [decimal]$usd.returned -eq 55 -and [decimal]$usd.reimbursed -eq 20 -and [decimal]$usd.pendingReturn -eq 0 -and [decimal]$usd.pendingReimbursement -eq 0 -and $totals.Status -eq 200 -and $query.Status -eq 200 -and @($query.Json.lines).Count -ge 1 -and $vehicles.Status -eq 200 -and $categories.Status -eq 200) "period=$($period.Status) delivered=$($usd.delivered) used=$($usd.used) justified=$($usd.justified) returned=$($usd.returned) reimbursed=$($usd.reimbursed) query_lines=$(@($query.Json.lines).Count)"

# 8. E: no raw actor ids in what Studio reads (names only)
function Find-ActorIds($node, [string]$path) {
    $found = @()
    if ($null -eq $node) { return $found }
    if ($node -is [System.Management.Automation.PSCustomObject]) {
        foreach ($property in $node.PSObject.Properties) {
            $childPath = "$path.$($property.Name)"
            if ($property.Name -match '(?i)(By|actor|userAccount)(Id)?$' -and ($property.Value -is [int] -or $property.Value -is [long] -or $property.Value -is [decimal] -or ("$($property.Value)" -match '^\d+$'))) { $found += "$childPath=$($property.Value)" }
            $found += Find-ActorIds $property.Value $childPath
        }
    } elseif ($node -is [System.Array]) { $index = 0; foreach ($item in $node) { $found += Find-ActorIds $item "$path[$index]"; $index++ } }
    return $found
}
$actorIds = @()
$actorIds += Find-ActorIds (Get-Case $a $r1) 'case'
$actorIds += Find-ActorIds (Send $a 'GET' "/api/expense-advances/$a1" $null).Json 'advance'
$actorIds += Find-ActorIds $e2Detail 'expense'
$studioShowsClosedBy = [bool](Select-String -Path 'D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo\platform_os\studio\channel\browser\shell\src\application\expenses\cases\*.jsx' -Pattern 'closedBy' -Quiet)
Check 'E no raw actor ids rendered (API numeric actor fields found are listed; Studio renders none)' (-not $studioShowsClosedBy -and @($actorIds | Where-Object { $_ -notmatch '\.closedBy=' }).Count -eq 0) "numeric_actor_fields=[$($actorIds -join ', ')] studio_renders_closedBy=$studioShowsClosedBy"

# 9. F: tenant isolation
$b = Login 'b'
$bCase = Send $b 'GET' "/api/expense-cases/$r1" $null
$bAdvance = Send $b 'GET' "/api/expense-advances/$a1" $null
$bExpense = Send $b 'GET' "/api/expenses/$e1" $null
$bMovement = Send $b 'POST' "/api/expense-cases/$r3/advances/$a3/rendition/returns" @{ operationId = (Op); amount = '1'; currency = 'USD' }
$bList = (Send $b 'GET' '/api/expense-cases' $null).Json.items
$bPeriod = (Send $b 'GET' "/api/expense-reports/period-summary?from=$from&to=$to" $null).Json.currencies
$bQuery = (Send $b 'GET' "/api/expense-reports/detail?criterion=CATEGORY&from=$from&to=$to" $null).Json.lines
Check 'F tenant B never reaches tenant A (case, advance, expense, rendition, list, reports)' ($b.LoginStatus -eq 200 -and $bCase.Status -eq 404 -and $bAdvance.Status -eq 404 -and $bExpense.Status -eq 404 -and $bMovement.Status -eq 404 -and @($bList).Count -eq 0 -and @($bPeriod | Where-Object { [decimal]$_.delivered -gt 0 -or [decimal]$_.used -gt 0 }).Count -eq 0 -and @($bQuery).Count -eq 0) "case=$($bCase.Status) advance=$($bAdvance.Status) expense=$($bExpense.Status) movement=$($bMovement.Status) list=$(@($bList).Count) period=$(@($bPeriod).Count) query=$(@($bQuery).Count)"

$results | ForEach-Object { $_ }
"R1=$r1 R2=$r2 R3=$r3"
"R03_RUNTIME_CHECKS=$($results.Count) FAILURES=$failures"

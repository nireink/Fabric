# GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10 - live smoke against the local runtime only
# (127.0.0.1:8080 -> isolated copy 127.0.0.1:3310 at V63; Mailpit 8026). One synthetic @example.test account in its own tenant.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Net.Http
$api = 'http://127.0.0.1:8080'; $mailpit = 'http://127.0.0.1:8026'
$scratch = 'C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\4bbfc1ff-e737-4ade-bbb8-169c21a07560\scratchpad'
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
function Login {
    $s = New-Session
    $email = "runtime-smoke-s10-$([guid]::NewGuid().ToString('N').Substring(0,8))@example.test"; $password = 'Rs-Smoke-' + [guid]::NewGuid().ToString('N')
    $null = Send $s 'POST' '/auth/register' @{ firstName = 'Runtime'; firstSurname = 'SmokeS10'; email = $email; password = $password }
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

$s = Login
Check 'synthetic session' ($s.LoginStatus -eq 200 -and [bool]$s.Xsrf) "login=$($s.LoginStatus)"
$responsible = (Send $s 'POST' '/api/expense-persons' @{ operationId = (Op); displayName = 'S10 Responsable'; primaryEmail = "s10-$([guid]::NewGuid().ToString('N').Substring(0,8))@example.test" }).Json.reference
$case = Send $s 'POST' '/api/expense-cases' ('{"operationId":"' + (Op) + '","name":"S10 smoke - varios anticipos","responsibleId":"' + $responsible + '","advanceId":null,"resources":[]}')
$caseId = $case.Json.caseId
function Add-Advance([string]$amount, [string]$currency) {
    return Send $s 'POST' "/api/expense-cases/$caseId/advances" @{ operationId = (Op); activityType = 'VIAJE'; activityDescription = "S10 tramo $amount"; amount = $amount; currency = $currency; deliveryMethodCode = 'EFECTIVO'; renditionDays = 7 }
}
function Deliver([string]$advanceId) { return Send $s 'POST' "/api/expense-advances/$advanceId/deliver" @{ operationId = (Op); expectedVersion = 0 } }

# D. several advances in one Case and currency, plus another currency
$created = @('30000', '2000', '300', '5000') | ForEach-Object { Add-Advance $_ 'USD' }
$euros = Add-Advance '70' 'EUR'
$bodies = (@($created) + @($euros) | ForEach-Object Text) -join ' '
Check 'D four USD advances and one EUR advance registered in the same open Case' ($case.Status -eq 201 -and @($created | Where-Object { $_.Status -eq 201 }).Count -eq 4 -and $euros.Status -eq 201) "case=$($case.Status) usd=$((@($created) | ForEach-Object Status) -join ',') eur=$($euros.Status)"
Check 'E no one-active-advance refusal anywhere' (-not ($bodies -match 'anticipo activo|Resuelve (el|ese) anticipo')) 'registration responses carry no refusal text'
$ids = @($created | ForEach-Object { $_.Json.advanceId })

# D. drafts are delivered beside drafts and delivered advances
$second = Deliver $ids[1]; $first = Deliver $ids[0]
Check 'D a draft is delivered beside drafts, and another beside a delivered advance' ($second.Status -eq 200 -and $first.Status -eq 200 -and -not (($second.Text + $first.Text) -match 'anticipo activo')) "second=$($second.Status) first=$($first.Status)"

# F. the drafts left still block closing the Case
$detail = (Send $s 'GET' "/api/expense-cases/$caseId" $null).Json
$close = Send $s 'POST' "/api/expense-cases/$caseId/close" @{ operationId = (Op); expectedVersion = $detail.version }
Check 'F drafts block Cerrar expediente' ($close.Status -eq 400 -and $close.Json.message -eq 'El expediente tiene anticipos en borrador; confirma su entrega o cancélalos.') "close=$($close.Status) message=$($close.Json.message)"

$cancel = Send $s 'POST' "/api/expense-advances/$($ids[2])/cancel" @{ operationId = (Op); expectedVersion = 0 }
$fourth = Deliver $ids[3]
$final = (Send $s 'GET' "/api/expense-cases/$caseId" $null).Json
$statuses = (@($final.advances) | ForEach-Object { "$($_.amount.currency):$([decimal]$_.amount.amount):$($_.status)" }) -join ','
$list = (Send $s 'GET' '/api/expense-cases' $null).Json.items | Where-Object { $_.caseId -eq $caseId }
$usd = @($list.financialSummary) | Where-Object { $_.delivered.currency -eq 'USD' }
Check 'the Case holds all its tranches; its card reads 37000 delivered and nothing used yet' ($cancel.Status -eq 200 -and $fourth.Status -eq 200 -and @($final.advances).Count -eq 5 -and [decimal]$usd.delivered.amount -eq 37000 -and [decimal]$usd.spent.amount -eq 0 -and [bool]$usd.hasDeliveredAdvance -and $final.status -eq 'ABIERTO') "advances=$statuses delivered=$($usd.delivered.amount) spent=$($usd.spent.amount) case=$($final.status)"

$results.Add("CASE=$caseId")
$results.Add("S10_RUNTIME_CHECKS=$($results.Count - 1) FAILURES=$failures")
$results | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $scratch 's10-runtime-smoke-results.txt')
$results

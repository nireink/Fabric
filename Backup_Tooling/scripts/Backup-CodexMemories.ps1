[CmdletBinding()]
param(
    [string]$CodexHome = (Join-Path $env:USERPROFILE ".codex")
)

$ErrorActionPreference = "Stop"

$fabricRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$source = Join-Path $CodexHome "memories"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$destination = Join-Path $fabricRoot "Private_State\codex-memory-backup\$timestamp"

if (-not (Test-Path -LiteralPath $source -PathType Container)) {
    throw "No se encontró la carpeta de memorias de Codex: $source"
}

New-Item -ItemType Directory -Path $destination -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force

$copiedRoot = Join-Path $destination "memories"
$manifestPath = Join-Path $destination "SHA256SUMS.csv"

Get-ChildItem -LiteralPath $copiedRoot -File -Recurse |
    Sort-Object FullName |
    ForEach-Object {
        $hash = Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256
        [PSCustomObject]@{
            RelativePath = $_.FullName.Substring($copiedRoot.Length).TrimStart("\")
            SHA256 = $hash.Hash
            Length = $_.Length
        }
    } |
    Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding UTF8

Write-Host "Respaldo selectivo completado: $destination"
Write-Host "No se copiaron auth.json, sesiones ni configuración global."


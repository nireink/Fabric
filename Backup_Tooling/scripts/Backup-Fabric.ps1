[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$DestinationRoot
)

$ErrorActionPreference = "Stop"

$fabricRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupRoot = Join-Path $DestinationRoot "Fabric-$timestamp"

if (-not (Test-Path -LiteralPath $DestinationRoot -PathType Container)) {
    New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null
}

New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
Copy-Item -LiteralPath $fabricRoot -Destination $backupRoot -Recurse -Force

$copiedFabric = Join-Path $backupRoot "Fabric"
$manifestPath = Join-Path $backupRoot "FABRIC_SHA256SUMS.csv"

Get-ChildItem -LiteralPath $copiedFabric -File -Recurse |
    Sort-Object FullName |
    ForEach-Object {
        $hash = Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256
        [PSCustomObject]@{
            RelativePath = $_.FullName.Substring($copiedFabric.Length).TrimStart("\")
            SHA256 = $hash.Hash
            Length = $_.Length
        }
    } |
    Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding UTF8

Write-Host "Copia fechada completada: $backupRoot"
Write-Host "La operación no elimina respaldos anteriores."


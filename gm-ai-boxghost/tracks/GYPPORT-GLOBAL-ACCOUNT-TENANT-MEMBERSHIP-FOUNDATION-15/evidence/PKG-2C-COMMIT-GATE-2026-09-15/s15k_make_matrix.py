"""Derive s15k_matrix.ps1 from s15j_matrix.ps1: the same 39 PKG-2C entries, plus a quick drift check after every entry
(git status + size + last-write time of every uncommitted file in every GYPPORT repository). The first change stops the
matrix as EXTERNAL_DRIFT_DETECTED_AFTER=<entry>; no reconciliation is attempted."""
import re

SCRATCH = r"C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP\8142c294-1815-45b4-90ee-94d1198faa7d\scratchpad"
SOURCE = SCRATCH + r"\s15j_matrix.ps1"
TARGET = SCRATCH + r"\s15k_matrix.ps1"

QUICK_STATE = r"""# Quick drift detector: any change of any uncommitted file (status, size or last-write time) in any GYPPORT repository.
$workspace = Split-Path -Parent $gystigo
$quickRepos = @($gystigo, (Join-Path $workspace 'Fabric')) + @(Get-ChildItem -Directory -LiteralPath (Join-Path $workspace 'Modules') |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName '.git') } | ForEach-Object { $_.FullName })
function Get-QuickState {
    $text = New-Object System.Text.StringBuilder
    foreach ($repo in $quickRepos) {
        foreach ($line in @(& git -C $repo status --porcelain -uall 2>$null | Where-Object { $_ })) {
            [void]$text.Append($repo).Append('|').Append($line)
            $full = Join-Path $repo ($line.Substring(3).Trim('"'))
            if (Test-Path -LiteralPath $full -PathType Leaf) {
                $item = Get-Item -LiteralPath $full
                [void]$text.Append('|').Append($item.Length).Append('|').Append($item.LastWriteTimeUtc.Ticks)
            }
            [void]$text.AppendLine()
        }
    }
    $sha = [System.Security.Cryptography.SHA256]::Create()
    return [BitConverter]::ToString($sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($text.ToString()))).Replace('-', '')
}
$initialState = Get-QuickState
Add-Content -LiteralPath $summary -Value ('QUICK_STATE_START=' + $initialState)
"""

DRIFT_CHECK = """    if ((Get-QuickState) -ne $initialState) {
        Add-Content -LiteralPath $summary -Value ('EXTERNAL_DRIFT_DETECTED_AFTER=' + $run.Name)
        break
    }
"""

with open(SOURCE, encoding="utf-8-sig") as handle:
    text = handle.read()

text = text.replace("'s15j_'", "'s15k_'")
header = "# STEP 15 PKG-2C full disposable runtime matrix:"
assert text.count(header) == 1, "header anchor"
text = text.replace(header, "# STEP 15 PKG-2C FINAL coherent matrix (Owner OPTION_A resume, 2026-09-15): the entries of s15j_matrix.ps1, run\n"
                    "# from entry 1 to entry 39, with a quick drift check after every entry (first change = stop).\n"
                    "# Origin, s15j_matrix.ps1 --" + header[1:], 1)
entries_anchor = "Add-Content -LiteralPath $summary -Value ('MATRIX_ENTRIES=' + $runs.Count)"
assert text.count(entries_anchor) == 1, "entries anchor"
text = text.replace(entries_anchor, QUICK_STATE + entries_anchor, 1)
result_anchor = "    Add-Result $run.Name $LASTEXITCODE $log\n"
assert text.count(result_anchor) == 1, "result anchor"
text = text.replace(result_anchor, result_anchor + DRIFT_CHECK, 1)

with open(TARGET, "w", encoding="utf-8", newline="\r\n") as handle:
    handle.write(text)
print("WROTE", TARGET, "entries:", len(re.findall(r"@\{ Name = '", text)),
      "drift_check:", text.count("EXTERNAL_DRIFT_DETECTED_AFTER"), "prefix_s15k:", text.count("'s15k_'"))

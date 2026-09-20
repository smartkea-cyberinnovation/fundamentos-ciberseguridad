#requires -Version 5.1
<# Ejemplo nativo sobre datos sinteticos. No cambia politicas de ejecucion. #>
[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Workspace)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
try {
    $root = Get-Item -LiteralPath $Workspace -Force
    if (-not $root.PSIsContainer -or ($root.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Directorio no admitido' }
    $marker = Get-Item -LiteralPath (Join-Path $root.FullName '.oslab') -Force
    $data = Get-Item -LiteralPath (Join-Path $root.FullName 'datos') -Force
    if ($marker.PSIsContainer -or $marker.Length -gt 128 -or ($marker.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Marcador no admitido' }
    if (-not $data.PSIsContainer -or ($data.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'datos no admitido' }
    if ((Get-Content -LiteralPath $marker.FullName -Raw).Trim() -ne 'OSLAB-SYNTHETIC-1') { throw 'Workspace incorrecto' }
    $files = @(Get-ChildItem -LiteralPath $data.FullName -Force)
    [long]$bytes = 0
    foreach ($file in $files) {
        if ($file.PSIsContainer -or ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Entrada no regular' }
        $bytes += $file.Length
    }
    [pscustomobject]@{count=$files.Count; total_bytes=$bytes} | ConvertTo-Json -Compress
    exit 0
} catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 2
}

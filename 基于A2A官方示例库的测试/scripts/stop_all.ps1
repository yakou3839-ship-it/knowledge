$ErrorActionPreference = 'Continue'

$root = Split-Path -Parent $PSScriptRoot
$logDir = Join-Path $root 'logs'

foreach ($service in @('weather', 'ticket', 'host')) {
    $pidFile = Join-Path $logDir "$service.pid"
    if (-not (Test-Path $pidFile)) {
        continue
    }
    $processId = (Get-Content $pidFile | Select-Object -First 1).Trim()
    if ($processId) {
        Write-Host "Stopping $service (PID $processId)..."
        taskkill /PID $processId /T /F 2>$null | Out-Null
    }
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
}

Write-Host 'Done. Check http://localhost:10001, :10002 and :8083 if they are still responding.'

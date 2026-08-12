$ErrorActionPreference = 'Continue'

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

$root = Split-Path -Parent $PSScriptRoot
$envExample = Join-Path $root '.env.example'
$envFile = Join-Path $root '.env'

Write-Host '==> Checking JDK 17+'
if (Test-Command 'java') {
    java -version 2>&1 | ForEach-Object { Write-Host $_ }
} elseif (Test-Command 'winget') {
    Write-Host 'JDK not found. Trying to install Temurin 17 via winget...'
    winget install --id EclipseAdoptium.Temurin.17.JDK --accept-source-agreements --accept-package-agreements
} elseif (Test-Command 'choco') {
    Write-Host 'JDK not found. Trying to install Temurin 17 via choco...'
    choco install temurin17 -y
} else {
    Write-Host 'JDK not found and neither winget nor choco is available.'
    Write-Host 'Please install JDK 17+ manually, then set JAVA_HOME in the root .env file.'
}

Write-Host '==> Maven'
Write-Host 'The weather_agent folder includes mvnw.cmd (Maven wrapper); no system Maven install is required.'

# Refresh PATH so newly installed tools are usable in this session.
$machinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($machinePath) { $env:Path = "$machinePath;$env:Path" }
if ($userPath) { $env:Path = "$userPath;$env:Path" }

Write-Host '==> Creating .env from template if missing'
if (-not (Test-Path $envFile)) {
    Copy-Item -LiteralPath $envExample -Destination $envFile
    Write-Host "Created $envFile - edit it and fill in your API keys."
} else {
    Write-Host "$envFile already exists."
}

Write-Host '==> Installing Python dependencies'
if (-not (Test-Command 'uv')) {
    Write-Host 'uv was not found. Install it from https://docs.astral.sh/uv/ first.'
    exit 1
}
uv --directory (Join-Path $root 'host') sync
uv --directory (Join-Path $root 'ticket_agent') sync
uv --directory (Join-Path $root 'weather_agent\mcp') sync

Write-Host ''
Write-Host 'Setup finished. Next steps:'
Write-Host '1. Edit the root .env file and set DEEPSEEK_API_KEY.'
Write-Host '2. If java is not on PATH or JAVA_HOME is not set, add JAVA_HOME to .env.'
Write-Host '3. If the 12306 MCP needs a login cookie, set TICKET_MCP_ENV_JSON.'
Write-Host "4. Run: powershell -ExecutionPolicy Bypass -File '$root\scripts\start_all.ps1'"
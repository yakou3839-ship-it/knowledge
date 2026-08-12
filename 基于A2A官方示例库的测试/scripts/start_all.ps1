$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root '.env'
if (-not (Test-Path $envFile)) {
    throw "Missing $envFile. Copy .env.example to .env and set DEEPSEEK_API_KEY first."
}

# Load the root .env into the current process so child servers inherit it.
Get-Content $envFile | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
    $kv = $_ -split '=', 2
    $name = $kv[0].Trim()
    $value = $kv[1].Trim().Trim('"')
    [Environment]::SetEnvironmentVariable($name, $value, 'Process')
}

if (-not $env:DEEPSEEK_API_KEY) {
    throw 'DEEPSEEK_API_KEY is missing from the root .env file.'
}

# Locate JDK 17+. Prefer JAVA_HOME from .env/system, otherwise derive it from java on PATH.
$javaHome = $env:JAVA_HOME
if ($javaHome) {
    $javaHome = $javaHome.TrimEnd('\')
    if (-not (Test-Path (Join-Path $javaHome 'bin\java.exe'))) {
        throw "JAVA_HOME is set to '$javaHome' but bin\java.exe was not found. Fix JAVA_HOME in the root .env file."
    }
} elseif (Get-Command java -ErrorAction SilentlyContinue) {
    $javaExe = (Get-Command java).Source
    $javaHome = Split-Path -Parent (Split-Path -Parent $javaExe)
} else {
    throw 'JDK 17+ was not found. Run scripts\setup.ps1, or set JAVA_HOME in the root .env file.'
}

$env:JAVA_HOME = $javaHome
$env:Path = "$env:JAVA_HOME\bin;$env:Path"

# Project-local Maven cache, ignored by git. Keeps a fresh clone self-contained.
$mavenRepo = Join-Path $root '.m2'
New-Item -ItemType Directory -Force -Path $mavenRepo | Out-Null

$logDir = Join-Path $root 'logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

Write-Host '==> Starting Weather Agent (Java, port 10001)'
$weatherOut = Join-Path $logDir 'weather.out.log'
$weatherErr = Join-Path $logDir 'weather.err.log'
$weather = Start-Process -FilePath (Join-Path $root 'weather_agent\mvnw.cmd') `
    -ArgumentList @("-Dmaven.repo.local=$mavenRepo", 'quarkus:dev') `
    -WorkingDirectory (Join-Path $root 'weather_agent') `
    -WindowStyle Hidden `
    -RedirectStandardOutput $weatherOut `
    -RedirectStandardError $weatherErr `
    -PassThru
$weather.Id | Set-Content (Join-Path $logDir 'weather.pid')

Write-Host '==> Starting Ticket Agent (Python, port 10002)'
$ticketOut = Join-Path $logDir 'ticket.out.log'
$ticketErr = Join-Path $logDir 'ticket.err.log'
$ticket = Start-Process -FilePath 'uv' `
    -ArgumentList @('run', '.') `
    -WorkingDirectory (Join-Path $root 'ticket_agent') `
    -WindowStyle Hidden `
    -RedirectStandardOutput $ticketOut `
    -RedirectStandardError $ticketErr `
    -PassThru
$ticket.Id | Set-Content (Join-Path $logDir 'ticket.pid')

Write-Host '==> Starting Host Agent (Python ADK, port 8083)'
$hostOut = Join-Path $logDir 'host.out.log'
$hostErr = Join-Path $logDir 'host.err.log'
$hostProc = Start-Process -FilePath 'uv' `
    -ArgumentList @('run', '.') `
    -WorkingDirectory (Join-Path $root 'host') `
    -WindowStyle Hidden `
    -RedirectStandardOutput $hostOut `
    -RedirectStandardError $hostErr `
    -PassThru
$hostProc.Id | Set-Content (Join-Path $logDir 'host.pid')

Write-Host ''
Write-Host 'All servers started:'
Write-Host '  Weather Agent: http://localhost:10001'
Write-Host '  Ticket Agent:  http://localhost:10002'
Write-Host '  Host UI:       http://localhost:8083'
Write-Host "Logs are under $logDir"
Write-Host "Stop everything with: powershell -ExecutionPolicy Bypass -File '$root\scripts\stop_all.ps1'"
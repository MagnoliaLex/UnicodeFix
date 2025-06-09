# PowerShell script to launch UnicodeFix Web Interface
# This provides a modern web UI for cleaning Unicode text

param(
    [switch]$NoBrowser = $false,
    [int]$Port = 8000
)

Write-Host "🚀 UnicodeFix Web Interface" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan
Write-Host ""

# Get script location and change to project root
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptRoot

# Check for virtual environment
$VenvPath = Join-Path $ScriptRoot "venv"
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"

if (!(Test-Path $ActivateScript)) {
    Write-Error "Virtual environment not found."
    Write-Host "Please run setup.ps1 first to set up the environment." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🔧 Activating virtual environment..." -ForegroundColor Green
try {
    & $ActivateScript
} catch {
    Write-Error "Failed to activate virtual environment: $($_.Exception.Message)"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check and install web dependencies
Write-Host "📦 Checking web dependencies..." -ForegroundColor Green
try {
    python -c "import fastapi, uvicorn" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing web dependencies..." -ForegroundColor Yellow
        pip install fastapi uvicorn python-multipart
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install dependencies"
        }
    }
} catch {
    Write-Error "Failed to install or check dependencies: $($_.Exception.Message)"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🌐 Starting UnicodeFix Web Interface..." -ForegroundColor Green
Write-Host "📱 Access URL: http://localhost:$Port" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:$Port/docs" -ForegroundColor Cyan

if (!$NoBrowser) {
    Write-Host "🔗 Opening browser automatically..." -ForegroundColor Green
}

Write-Host ""
Write-Host "⏹️  Press Ctrl+C to stop the server when you're done." -ForegroundColor Yellow
Write-Host "-" * 40 -ForegroundColor Gray
Write-Host ""

try {
    # Start the web application
    if ($NoBrowser) {
        $env:UNICODEFIX_NO_BROWSER = "1"
    }
    
    python run_web.py
    
} catch {
    Write-Error "Error running web application: $($_.Exception.Message)"
} finally {
    Write-Host ""
    Write-Host "👋 UnicodeFix Web Interface stopped." -ForegroundColor Green
    Write-Host "Thank you for using UnicodeFix!" -ForegroundColor Cyan
}

if (!$NoBrowser) {
    Read-Host "`nPress Enter to close this window"
} 
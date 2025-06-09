# PowerShell setup script for UnicodeFix on Windows
# This script creates a virtual environment, installs dependencies, and sets up the environment

param(
    [switch]$Force = $false
)

Write-Host "UnicodeFix Windows Setup" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

# Get the project root directory
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.8+ and try again."
    exit 1
}

# Create virtual environment
$venvPath = Join-Path $ProjectRoot "venv"
if (Test-Path $venvPath) {
    if ($Force) {
        Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item $venvPath -Recurse -Force
    } else {
        Write-Host "Virtual environment already exists. Use -Force to recreate it." -ForegroundColor Yellow
        Write-Host "Activating existing environment..." -ForegroundColor Green
    }
}

if (!(Test-Path $venvPath) -or $Force) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment"
        exit 1
    }
}

# Activate virtual environment
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $activateScript
} else {
    Write-Error "Failed to find virtual environment activation script"
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies"
    exit 1
}

# Create batch file for easy execution
$batchContent = @"
@echo off
REM UnicodeFix Windows launcher
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"
call venv\Scripts\activate.bat
python bin\cleanup-text.py %*
"@

$batchFile = Join-Path $ProjectRoot "unicodefix.bat"
$batchContent | Out-File -FilePath $batchFile -Encoding ASCII
Write-Host "Created launcher: unicodefix.bat" -ForegroundColor Green

# Create PowerShell function for easier usage
$psProfile = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path $psProfile -Parent
if (!(Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$functionDef = @"

# UnicodeFix function - added by UnicodeFix setup
function Invoke-UnicodeFix {
    param([string[]]`$Files)
    `$scriptPath = "$ProjectRoot"
    Push-Location `$scriptPath
    try {
        & .\venv\Scripts\activate.ps1
        if (`$Files) {
            python bin\cleanup-text.py `$Files
        } else {
            python bin\cleanup-text.py
        }
    } finally {
        Pop-Location
    }
}
Set-Alias unicodefix Invoke-UnicodeFix
Set-Alias cleanup-text Invoke-UnicodeFix
"@

# Check if function already exists in profile
$profileExists = Test-Path $psProfile
$needsUpdate = $true

if ($profileExists) {
    $profileContent = Get-Content $psProfile -Raw
    if ($profileContent -match "UnicodeFix function") {
        $needsUpdate = $false
        Write-Host "PowerShell profile already configured" -ForegroundColor Yellow
    }
}

if ($needsUpdate) {
    $functionDef | Add-Content $psProfile
    Write-Host "Added UnicodeFix function to PowerShell profile: $psProfile" -ForegroundColor Green
    Write-Host "You can now use 'unicodefix' or 'cleanup-text' commands after restarting PowerShell" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Usage options:" -ForegroundColor Cyan
Write-Host "  1. Direct batch file: .\unicodefix.bat [files...]" -ForegroundColor White
Write-Host "  2. After restarting PowerShell: unicodefix [files...]" -ForegroundColor White
Write-Host "  3. Manual activation: .\venv\Scripts\activate.ps1 && python bin\cleanup-text.py [files...]" -ForegroundColor White
Write-Host ""
Write-Host "For pipe usage: type file.txt | .\unicodefix.bat" -ForegroundColor White
Write-Host "Or: Get-Content file.txt | unicodefix" -ForegroundColor White 
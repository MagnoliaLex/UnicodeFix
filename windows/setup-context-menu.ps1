# PowerShell script to set up Windows Explorer context menu for UnicodeFix
# Run this script as Administrator

param(
    [switch]$Remove = $false
)

# Get the project root directory
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Security: Validate and sanitize the project root path
if ($ProjectRoot -match '\.\.' -or $ProjectRoot -match '[&|;<>`]') {
    Write-Error "Invalid or potentially unsafe path detected: $ProjectRoot"
    Write-Error "Please ensure the script is running from a safe location."
    exit 1
}

# Ensure path doesn't contain injection characters
$ProjectRoot = $ProjectRoot -replace '[&|;<>`]', ''
$UnicodeFix = Join-Path $ProjectRoot "unicodefix.bat"

if (!(Test-Path $UnicodeFix)) {
    Write-Error "unicodefix.bat not found. Please run setup.ps1 first."
    exit 1
}

Write-Host "UnicodeFix Context Menu Setup" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

if ($Remove) {
    Write-Host "Removing context menu entries..." -ForegroundColor Yellow
    
    # Remove registry entries
    try {
        Remove-Item "HKCR:\*\shell\UnicodeFix" -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item "HKCR:\Directory\Background\shell\UnicodeFix" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Context menu entries removed successfully." -ForegroundColor Green
    } catch {
        Write-Error "Failed to remove context menu entries: $($_.Exception.Message)"
    }
    return
}

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (!$isAdmin) {
    Write-Warning "This script needs to be run as Administrator to modify the registry."
    Write-Host "Please right-click on PowerShell and 'Run as Administrator', then run this script again."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Installing context menu entries..." -ForegroundColor Green

try {
    # Create registry entries for single file selection
    New-Item -Path "HKCR:\*\shell\UnicodeFix" -Force | Out-Null
    Set-ItemProperty -Path "HKCR:\*\shell\UnicodeFix" -Name "(Default)" -Value "Clean Unicode"
    Set-ItemProperty -Path "HKCR:\*\shell\UnicodeFix" -Name "Icon" -Value "C:\Windows\System32\shell32.dll,134"
    
    New-Item -Path "HKCR:\*\shell\UnicodeFix\command" -Force | Out-Null
    $singleFileCommand = "cmd /c `"cd /d `"$ProjectRoot`" && `"$UnicodeFix`" `"%1`" && pause`""
    Set-ItemProperty -Path "HKCR:\*\shell\UnicodeFix\command" -Name "(Default)" -Value $singleFileCommand
    
    # Create registry entries for directory background (right-click in empty space)
    New-Item -Path "HKCR:\Directory\Background\shell\UnicodeFix" -Force | Out-Null
    Set-ItemProperty -Path "HKCR:\Directory\Background\shell\UnicodeFix" -Name "(Default)" -Value "Clean Unicode Files Here"
    Set-ItemProperty -Path "HKCR:\Directory\Background\shell\UnicodeFix" -Name "Icon" -Value "C:\Windows\System32\shell32.dll,134"
    
    New-Item -Path "HKCR:\Directory\Background\shell\UnicodeFix\command" -Force | Out-Null
    $directoryCommand = "powershell -WindowStyle Normal -Command `"cd '%V'; Get-ChildItem -File | ForEach-Object { & '$UnicodeFix' `$_.FullName }; Read-Host 'Press Enter to close'`""
    Set-ItemProperty -Path "HKCR:\Directory\Background\shell\UnicodeFix\command" -Name "(Default)" -Value $directoryCommand
    
    Write-Host "Context menu entries installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now:" -ForegroundColor Cyan
    Write-Host "  1. Right-click any file and select 'Clean Unicode'" -ForegroundColor White
    Write-Host "  2. Right-click in empty space in a folder and select 'Clean Unicode Files Here'" -ForegroundColor White
    Write-Host ""
    Write-Host "To remove these entries later, run: .\setup-context-menu.ps1 -Remove" -ForegroundColor Yellow
    
} catch {
    Write-Error "Failed to create context menu entries: $($_.Exception.Message)"
    Write-Host "Make sure you're running this script as Administrator."
}

Read-Host "Press Enter to exit" 
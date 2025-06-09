@echo off
REM Windows batch wrapper for cleanup-text.py
REM This ensures the virtual environment is activated and the script runs properly

setlocal

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
REM Go up one level to the project root
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Change to project root directory
cd /d "%PROJECT_ROOT%"

REM Activate the virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Error: Virtual environment not found. Please run setup.ps1 first.
    pause
    exit /b 1
)

REM Run the Python script with all passed arguments
python bin\cleanup-text.py %*

REM Deactivate virtual environment
if defined VIRTUAL_ENV (
    deactivate
) 
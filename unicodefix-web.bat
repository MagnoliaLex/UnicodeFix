@echo off
REM UnicodeFix Web Interface Launcher for Windows
REM This launches the modern web interface in your browser

setlocal

echo.
echo ==========================================
echo  UnicodeFix Web Interface Launcher
echo ==========================================
echo.

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found.
    echo Please run setup.ps1 first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Checking dependencies...
python -c "import fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo Installing web dependencies...
    pip install fastapi uvicorn python-multipart
)

echo.
echo Starting UnicodeFix Web Interface...
echo Your browser will open automatically.
echo.
echo Press Ctrl+C to stop the server when you're done.
echo.

REM Start the web application
python run_web.py

echo.
echo Web interface stopped.
pause 
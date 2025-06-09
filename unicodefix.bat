@echo off
REM UnicodeFix Windows launcher
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"
call venv\Scripts\activate.bat
python bin\cleanup-text.py %*

@echo off
set "JARVIS_PYTHON=%LocalAppData%\Programs\Python\Python312\python.exe"

if not exist "%JARVIS_PYTHON%" (
    echo Python 3.12 was not found. Install it, then try again.
    pause
    exit /b 1
)

cd /d "%~dp0"
"%JARVIS_PYTHON%" run.py

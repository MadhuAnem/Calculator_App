@echo off
REM ============================================
REM  AllCalc Launcher - 206 Calculators in One
REM ============================================
cd /d "%~dp0"

REM Try the full Python 3.12 install first
set "PY=C:\Users\Guest1\AppData\Local\Programs\Python\Python312\python.exe"
if exist "%PY%" (
    "%PY%" app.py
    goto :eof
)

REM Fall back to any python on PATH
python app.py 2>nul
if errorlevel 1 (
    echo.
    echo Python was not found. Install Python 3.12+ from python.org
    pause
)


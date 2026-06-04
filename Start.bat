@echo off
title FileBox
chcp 65001 >nul 2>&1
cls

echo.
echo   ███████╗██╗██╗     ███████╗██████╗  ██████╗ ██╗  ██╗
echo   ██╔════╝██║██║     ██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝
echo   █████╗  ██║██║     █████╗  ██████╔╝██║   ██║ ╚███╔╝
echo   ██╔══╝  ██║██║     ██╔══╝  ██╔══██╗██║   ██║ ██╔██╗
echo   ██║     ██║███████╗███████╗██████╔╝╚██████╔╝██╔╝ ██╗
echo   ╚═╝     ╚═╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
echo.

:: ── Check Python ──────────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python not found.
    echo   Please install Python 3.8+ from https://python.org
    echo   Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo   [OK] Python %PYVER% found

:: ── Create virtual environment ────────────────────────────────────────────────
if not exist "venv\" (
    echo   [..] Creating virtual environment...
    python -m venv .venv
    echo   [OK] Virtual environment created
)

:: ── Activate and install ──────────────────────────────────────────────────────
call .venv\Scripts\activate.bat

echo   [..] Installing dependencies...
pip install -r requirements.txt -q --disable-pip-version-check
echo   [OK] Dependencies ready

:: ── Launch ────────────────────────────────────────────────────────────────────
echo.
echo   +---------------------------------------+
echo   ^|  FileBox is running!                 ^|
echo   ^|  Local:  http://localhost:8000       ^|
echo   ^|  Press Ctrl+C to stop                ^|
echo   +---------------------------------------+
echo.

:: Open browser after short delay
ping -n 2 127.0.0.1 >nul
start http://localhost:8000

python Server.py

pause

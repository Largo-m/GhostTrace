@echo off
setlocal enabledelayedexpansion
title GhostTrace v2.0

cd /d "%~dp0"

echo.
echo ==========================================
echo          GHOSTTRACE v2.0
echo    Stealth Proxy Chain Analyzer
echo ==========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found
    pause
    exit /b 1
)
echo [+] Python found

if not exist "venv\" (
    echo [*] Creating venv...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo [+] Venv ready

if not exist "venv\.deps_installed" (
    echo [*] Installing packages...
    pip install --upgrade pip --quiet 2>nul
    pip install requests[socks] PySocks stem pyyaml colorama aiohttp fake-useragent rich loguru pytest pytest-asyncio scapy fastapi uvicorn websockets asyncio-throttle --quiet 2>nul
    type nul > venv\.deps_installed
    echo [+] Done
) else (
    echo [+] Packages already installed
)

if not exist "output\logs\" mkdir output\logs
if not exist "output\captures\" mkdir output\captures
if not exist "output\sessions\" mkdir output\sessions

if not exist "config\settings.yaml" (
    if exist "config\settings.yaml.example" (
        copy config\settings.yaml.example config\settings.yaml >nul
    )
)

:: ============================================
:: Find Tor Browser
:: ============================================
set "TOR_EXE="

if exist "%~dp0tor\firefox.exe" set "TOR_EXE=%~dp0tor\firefox.exe"
if not defined TOR_EXE if exist "%~dp0firefox.exe" set "TOR_EXE=%~dp0firefox.exe"

set "TOR_CONNECTED=0"

if defined TOR_EXE (
    echo [+] Tor Browser found

    tasklist /FI "IMAGENAME eq firefox.exe" 2>nul | find /I "firefox.exe" >nul
    if !errorlevel! neq 0 (
        echo [*] Opening Tor Browser...
        start "" "!TOR_EXE!" >nul 2>&1
    )

    echo [*] Waiting for Tor network...
    echo.

    for /L %%i in (1,1,24) do (
        timeout /t 5 /nobreak >nul
        set /a elapsed=%%i*5

        python -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('127.0.0.1',9050)); s.close(); print('OK')" 2>nul | findstr "OK" >nul
        if !errorlevel! equ 0 (
            set "TOR_CONNECTED=1"
            echo [+] Tor connected after !elapsed! seconds
            goto menu
        )
        <nul set /p "=."
    )

    echo.
    echo [!] Tor did not connect within 2 minutes
    echo [!] You can continue but Demo/Scan need Tor
    echo.
) else (
    echo [!] Tor Browser not found
)

:menu
echo.
echo ==========================================
echo          GHOSTTRACE v2.0
echo    Stealth Proxy Chain Analyzer
echo ==========================================
echo.
if "!TOR_CONNECTED!"=="1" (
    echo [Tor: CONNECTED]
) else if defined TOR_EXE (
    echo [Tor: CONNECTING... wait or skip]
) else (
    echo [Tor: NOT FOUND]
)
echo.
echo 1) Demo - Show real IP vs Ghost IP
echo 2) Scrape fresh proxies from internet
echo 3) Stealth scan a target
echo 4) Run stealth loop
echo 5) Web Dashboard
echo 6) Run tests
echo 0) Exit
echo.
set /p "choice=Choice [0-6]: "

if "%choice%"=="1" (
    python ghost.py --demo
    pause
    goto menu
)
if "%choice%"=="2" (
    python ghost.py --scrape
    pause
    goto menu
)
if "%choice%"=="3" (
    set /p "target=Target IP: "
    python ghost.py --scan !target!
    pause
    goto menu
)
if "%choice%"=="4" (
    set /p "dur=Duration in seconds: "
    if "!dur!"=="" set dur=60
    python ghost.py --duration !dur!
    pause
    goto menu
)
if "%choice%"=="5" (
    start http://127.0.0.1:5000
    python ghost.py --web
    pause
    goto menu
)
if "%choice%"=="6" (
    python -m pytest tests/ -v --tb=short
    pause
    goto menu
)
if "%choice%"=="0" exit /b 0

echo Invalid choice
pause
goto menu
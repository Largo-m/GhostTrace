#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd "$(dirname "$0")"

clear
echo ""
echo -e "${GREEN}=========================================="
echo -e "         GHOSTTRACE v2.0"
echo -e "   Stealth Proxy Chain Analyzer"
echo -e "==========================================${NC}"
echo ""

if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo -e "${RED}Python not found${NC}"
    exit 1
fi
echo -e "${GREEN}[+] Python found${NC}"

if [ ! -d "venv" ]; then
    echo -e "${CYAN}[*] Creating venv...${NC}"
    $PYTHON -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}[+] Venv ready${NC}"

if [ ! -f "venv/.deps_installed" ]; then
    echo -e "${CYAN}[*] Installing packages...${NC}"
    pip install --upgrade pip --quiet 2>/dev/null
    pip install requests[socks] PySocks stem pyyaml colorama aiohttp fake-useragent rich loguru pytest pytest-asyncio scapy fastapi uvicorn websockets asyncio-throttle --quiet 2>/dev/null
    touch venv/.deps_installed
    echo -e "${GREEN}[+] Done${NC}"
else
    echo -e "${GREEN}[+] Packages already installed${NC}"
fi

mkdir -p output/logs output/captures output/sessions

if [ ! -f "config/settings.yaml" ] && [ -f "config/settings.yaml.example" ]; then
    cp config/settings.yaml.example config/settings.yaml
fi

TOR_EXE=""
TOR_CONNECTED=0

if [ -f "tor/firefox.exe" ]; then
    TOR_EXE="tor/firefox.exe"
elif [ -f "firefox.exe" ]; then
    TOR_EXE="firefox.exe"
fi

if [ -n "$TOR_EXE" ]; then
    echo -e "${GREEN}[+] Tor Browser found${NC}"
    
    if ! pgrep -f firefox.exe >/dev/null 2>&1; then
        echo -e "${CYAN}[*] Opening Tor Browser...${NC}"
        start "" "$TOR_EXE" 2>/dev/null
    fi
    
    echo -e "${CYAN}[*] Waiting for Tor network...${NC}"
    echo ""
    
    for i in $(seq 1 24); do
        sleep 5
        elapsed=$((i * 5))
        
        python3 -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('127.0.0.1',9050)); s.close()" 2>/dev/null
        if [ $? -eq 0 ]; then
            TOR_CONNECTED=1
            echo -e "${GREEN}[+] Tor connected after ${elapsed} seconds${NC}"
            break
        fi
        echo -n "."
    done
    echo ""
    
    if [ $TOR_CONNECTED -eq 0 ]; then
        echo -e "${YELLOW}[!] Tor did not connect within 2 minutes${NC}"
        echo -e "${YELLOW}[!] You can continue but Demo/Scan need Tor${NC}"
    fi
else
    echo -e "${YELLOW}[!] Tor Browser not found${NC}"
fi

while true; do
    echo ""
    echo -e "${GREEN}=========================================="
    echo -e "         GHOSTTRACE v2.0"
    echo -e "   Stealth Proxy Chain Analyzer"
    echo -e "==========================================${NC}"
    echo ""
    
    if [ $TOR_CONNECTED -eq 1 ]; then
        echo -e "[Tor: ${GREEN}CONNECTED${NC}]"
    elif [ -n "$TOR_EXE" ]; then
        echo -e "[Tor: ${YELLOW}CONNECTING...${NC}]"
    else
        echo -e "[Tor: ${RED}NOT FOUND${NC}]"
    fi
    
    echo ""
    echo "1) Demo - Show real IP vs Ghost IP"
    echo "2) Scrape fresh proxies"
    echo "3) Stealth scan a target"
    echo "4) Run stealth loop"
    echo "5) Launch Web Dashboard"
    echo "6) Run tests"
    echo "0) Exit"
    echo ""
    read -p "Choice [0-6]: " choice
    
    case $choice in
        1) $PYTHON ghost.py --demo ;;
        2) $PYTHON ghost.py --scrape ;;
        3) read -p "Target IP: " target; $PYTHON ghost.py --scan "$target" ;;
        4) read -p "Duration (seconds): " dur; $PYTHON ghost.py --duration "${dur:-60}" ;;
        5) echo "Starting Web Dashboard on http://127.0.0.1:5000"; $PYTHON ghost.py --web ;;
        6) $PYTHON -m pytest tests/ -v --tb=short 2>/dev/null ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo -e "${RED}Invalid choice${NC}" ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done
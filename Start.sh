#!/bin/bash
# ─────────────────────────────────────────
#  FileBox – Start Script (Linux / macOS)
# ─────────────────────────────────────────

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}  ███████╗██╗██╗     ███████╗██████╗  ██████╗ ██╗  ██╗${NC}"
echo -e "${CYAN}  ██╔════╝██║██║     ██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝${NC}"
echo -e "${CYAN}  █████╗  ██║██║     █████╗  ██████╔╝██║   ██║ ╚███╔╝ ${NC}"
echo -e "${CYAN}  ██╔══╝  ██║██║     ██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ ${NC}"
echo -e "${CYAN}  ██║     ██║███████╗███████╗██████╔╝╚██████╔╝██╔╝ ██╗${NC}"
echo -e "${CYAN}  ╚═╝     ╚═╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝${NC}"
echo ""

# ── Check Python ──────────────────────────────────────────────────────────────
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}  ✗ Python 3 not found.${NC}"
    echo    "    Please install Python 3.8+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}  ✓ Python ${PYTHON_VERSION} found${NC}"

# ── Create virtual environment ────────────────────────────────────────────────
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}  → Creating virtual environment...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}  ✓ Virtual environment created${NC}"
fi

# ── Activate virtual environment ──────────────────────────────────────────────
source .venv/bin/activate

# ── Install dependencies ──────────────────────────────────────────────────────
echo -e "${YELLOW}  → Installing dependencies...${NC}"
pip install -r requirements.txt -q --disable-pip-version-check
echo -e "${GREEN}  ✓ Dependencies ready${NC}"

# ── Launch ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}  ┌─────────────────────────────────────┐${NC}"
echo -e "${CYAN}  │  FileBox is running!                │${NC}"
echo -e "${CYAN}  │  Local:  http://localhost:8000      │${NC}"
echo -e "${CYAN}  │  Press Ctrl+C to stop               │${NC}"
echo -e "${CYAN}  └─────────────────────────────────────┘${NC}"
echo ""

# Open browser (best effort)
sleep 1
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000 &> /dev/null &
elif command -v open &> /dev/null; then
    open http://localhost:8000 &> /dev/null &
fi

python3 Server.py

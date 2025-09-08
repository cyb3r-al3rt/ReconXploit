#!/bin/bash
# ReconXploit v4.0 ULTIMATE - Global Launcher

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to find ReconXploit installation
find_reconxploit() {
    local search_dirs=(
        "$HOME/ReconXploit-v4.0-ULTIMATE"
        "$HOME/ReconXploit"
        "/opt/reconxploit"
        "/usr/local/share/reconxploit"
        "$(dirname "$(readlink -f "$0")")"
    )

    for dir in "${search_dirs[@]}"; do
        if [[ -d "$dir" && -f "$dir/core/reconxploit.py" ]]; then
            echo "$dir"
            return 0
        fi
    done

    return 1
}

# Find ReconXploit installation
RECONXPLOIT_DIR=$(find_reconxploit)

if [[ -z "$RECONXPLOIT_DIR" ]]; then
    echo -e "${RED}[ERROR]${NC} ReconXploit installation not found!"
    echo -e "${YELLOW}[SEARCHED]${NC} The following directories were checked:"
    echo "  • $HOME/ReconXploit-v4.0-ULTIMATE"
    echo "  • $HOME/ReconXploit"
    echo "  • /opt/reconxploit"
    echo "  • /usr/local/share/reconxploit"
    echo ""
    echo -e "${CYAN}[SOLUTION]${NC} Extract ReconXploit to one of the above locations or run from the installation directory"
    exit 1
fi

echo -e "${BLUE}[GLOBAL LAUNCHER]${NC} Found ReconXploit at: $RECONXPLOIT_DIR"

# Change to ReconXploit directory and execute
cd "$RECONXPLOIT_DIR"
exec ./reconxploit "$@"

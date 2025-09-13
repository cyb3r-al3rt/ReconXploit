#!/usr/bin/env bash

INSTALL_DIR="/opt/reconxploit"
BIN_DIR="/usr/local/bin"
BINARY_NAME="reconxploit"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

log_message() {
    local level=$1
    local message=$2
    local color=""
    case $level in
        "INFO") color=$BLUE ;;
        "SUCCESS") color=$GREEN ;;
        "WARNING") color=$YELLOW ;;
        "ERROR") color=$RED ;;
    esac
    echo -e "${color}[${level}]${NC} ${message}"
}

print_banner() {
    echo -e "${CYAN}"
    echo "================================================================================"
    echo "||                 RECONXPLOIT FRAMEWORK - GLOBAL INSTALLER                  ||"
    echo "||               Creates global 'reconxploit' command                        ||"
    echo "================================================================================"
    echo -e "${NC}"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_message "ERROR" "This script must be run as root (use sudo)"
        exit 1
    fi
}

create_global_binary() {
    log_message "INFO" "Creating global binary installation..."

    if [[ ! -f "reconxploit.py" ]]; then
        log_message "ERROR" "reconxploit.py not found in current directory"
        exit 1
    fi

    mkdir -p "$INSTALL_DIR"
    log_message "INFO" "Installing framework to $INSTALL_DIR"
    cp -r * "$INSTALL_DIR/" 2>/dev/null || true
    chmod +x "$INSTALL_DIR/reconxploit.py"

    log_message "INFO" "Creating global binary: $BIN_DIR/$BINARY_NAME"

cat > "$BIN_DIR/$BINARY_NAME" << 'EOFBIN'
#!/bin/bash
RECONXPLOIT_HOME="/opt/reconxploit"
if [[ ! -f "$RECONXPLOIT_HOME/reconxploit.py" ]]; then
    echo -e "\033[0;31m[ERROR]\033[0m ReconXploit Framework not found"
    exit 1
fi
export RECONXPLOIT_HOME="$RECONXPLOIT_HOME"
export PYTHONPATH="$RECONXPLOIT_HOME:$PYTHONPATH"
cd "$RECONXPLOIT_HOME"
python3 "$RECONXPLOIT_HOME/reconxploit.py" "$@"
EOFBIN

    chmod +x "$BIN_DIR/$BINARY_NAME"
    mkdir -p "$INSTALL_DIR"/{results,logs,wordlists,plugins,custom_plugins,config}
    chmod -R 755 "$INSTALL_DIR"

    create_uninstaller
    log_message "SUCCESS" "Global binary created successfully!"
}

create_uninstaller() {
cat > "$BIN_DIR/reconxploit-uninstall" << 'EOFUNINST'
#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}[ERROR]${NC} This script must be run as root (use sudo)"
    exit 1
fi

echo -e "${YELLOW}ReconXploit Framework Uninstaller${NC}"
read -p "Remove ReconXploit completely? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}[INFO]${NC} Removing ReconXploit Framework..."
    if [[ -d "/opt/reconxploit" ]]; then
        rm -rf "/opt/reconxploit"
        echo -e "${GREEN}[SUCCESS]${NC} Removed: /opt/reconxploit"
    fi
    if [[ -f "/usr/local/bin/reconxploit" ]]; then
        rm -f "/usr/local/bin/reconxploit"
        echo -e "${GREEN}[SUCCESS]${NC} Removed: /usr/local/bin/reconxploit"
    fi
    if [[ -f "/usr/local/bin/reconxploit-uninstall" ]]; then
        rm -f "/usr/local/bin/reconxploit-uninstall"
        echo -e "${GREEN}[SUCCESS]${NC} Removed uninstaller"
    fi
    echo
    echo -e "${GREEN}ReconXploit Framework completely removed!${NC}"
else
    echo -e "${YELLOW}[CANCELLED]${NC} Uninstallation cancelled"
fi
EOFUNINST

    chmod +x "$BIN_DIR/reconxploit-uninstall"
}

show_completion() {
    echo -e "${GREEN}"
    echo "================================================================================"
    echo "||                     GLOBAL INSTALLATION COMPLETED!                        ||"
    echo "||                   ReconXploit is now globally available                   ||"
    echo "================================================================================"
    echo -e "${NC}"

    echo -e "${WHITE}RECONXPLOIT FRAMEWORK - NOW GLOBAL!${NC}"
    echo
    echo -e "${CYAN}USAGE (from anywhere):${NC}"
    echo -e "${WHITE}  reconxploit --framework-info${NC}"
    echo -e "${WHITE}  reconxploit -t example.com${NC}"
    echo -e "${WHITE}  reconxploit -t example.com --comprehensive${NC}"
    echo
    echo -e "${GREEN}LOCATIONS:${NC}"
    echo "  Framework: /opt/reconxploit/"
    echo "  Command: /usr/local/bin/reconxploit"
    echo "  Uninstaller: /usr/local/bin/reconxploit-uninstall"
    echo
    echo -e "${GREEN}Test: reconxploit --framework-info${NC}"
}

main() {
    print_banner
    check_root

    if [[ ! -f "reconxploit.py" ]]; then
        log_message "ERROR" "reconxploit.py not found in current directory"
        exit 1
    fi

    echo -e "${WHITE}Install ReconXploit as global binary?${NC}"
    read -p "Continue? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_global_binary
        show_completion
    else
        log_message "INFO" "Installation cancelled"
    fi
}

main "$@"

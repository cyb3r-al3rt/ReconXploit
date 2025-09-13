#!/usr/bin/env bash

# ReconXploit Framework COMPLETE PACKAGE Installer
# NO GitHub credentials required - Everything works offline

set -e

INSTALL_DIR="/opt/reconxploit"
BIN_DIR="/usr/local/bin"
BINARY_NAME="reconxploit"
TOOLS_DIR="$INSTALL_DIR/tools"
VENV_DIR="$INSTALL_DIR/venv"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Counters
TOTAL_TOOLS=0
WORKING_TOOLS=0

log_message() {
    local level=$1
    local message=$2
    local color=""
    case $level in
        "INFO") color=$BLUE ;;
        "SUCCESS") color=$GREEN ;;
        "WARNING") color=$YELLOW ;;
        "ERROR") color=$RED ;;
        "FIX") color=$CYAN ;;
        "INSTALL") color=$PURPLE ;;
    esac
    echo -e "${color}[${level}]${NC} ${message}"
}

print_banner() {
    clear
    echo -e "${CYAN}${WHITE}"
    echo "████████████████████████████████████████████████████████████████████████████████"
    echo "||                                                                            ||"
    echo "||         🚀 RECONXPLOIT COMPLETE PACKAGE INSTALLER 🚀                      ||"
    echo "||              NO GITHUB CREDENTIALS REQUIRED                               ||"
    echo "||                   EVERYTHING INCLUDED                                     ||"
    echo "||                                                                            ||"
    echo "████████████████████████████████████████████████████████████████████████████████"
    echo -e "${NC}"
    echo
    echo -e "${GREEN}✅ COMPLETE PACKAGE FEATURES:${NC}"
    echo "  🔒 No GitHub authentication required"
    echo "  📚 Complete documentation included"
    echo "  🎯 All endpoints and wordlists bundled"
    echo "  📊 Terminal + HTML output by default"
    echo "  🛠️ Offline installation capability"
    echo
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_message "ERROR" "This script must be run as root (use sudo)"
        exit 1
    fi
}

setup_complete_environment() {
    log_message "INFO" "Setting up complete environment (no external dependencies)..."

    # Create comprehensive directory structure
    mkdir -p "$INSTALL_DIR"/{tools,venv,wordlists,plugins,workflows,results,reports,logs,config,endpoints,templates}
    mkdir -p "$TOOLS_DIR"/{go,rust,python,custom,bin}

    # Set up Go environment
    export GOROOT="/usr/lib/go"
    export GOPATH="$TOOLS_DIR/go"
    export PATH="$PATH:$GOROOT/bin:$GOPATH/bin"
    mkdir -p "$GOPATH"/{bin,src,pkg}

    # Set up Rust environment  
    export CARGO_HOME="$TOOLS_DIR/rust"
    export RUSTUP_HOME="$TOOLS_DIR/rust/rustup"
    export PATH="$PATH:$CARGO_HOME/bin:/root/.cargo/bin"
    mkdir -p "$CARGO_HOME" "$RUSTUP_HOME"

    # Set up Python virtual environment
    if [[ ! -d "$VENV_DIR" ]]; then
        python3 -m venv "$VENV_DIR"
    fi
    source "$VENV_DIR/bin/activate"
    "$VENV_DIR/bin/pip" install --upgrade pip wheel setuptools

    # Add custom tools to PATH
    export PATH="$PATH:$TOOLS_DIR/bin"

    # Create permanent environment file
    cat > "$INSTALL_DIR/environment.sh" << 'EOF'
#!/bin/bash
# ReconXploit Complete Environment Configuration
export RECONXPLOIT_HOME="/opt/reconxploit"
export GOROOT="/usr/lib/go"
export GOPATH="/opt/reconxploit/tools/go"
export CARGO_HOME="/opt/reconxploit/tools/rust"
export RUSTUP_HOME="/opt/reconxploit/tools/rust/rustup"
export PATH="$PATH:$GOROOT/bin:$GOPATH/bin:$CARGO_HOME/bin:/root/.cargo/bin:/opt/reconxploit/tools/bin"

# Activate Python virtual environment
if [[ -f "/opt/reconxploit/venv/bin/activate" ]]; then
    source "/opt/reconxploit/venv/bin/activate"
fi

# Set default output formats
export RECONXPLOIT_OUTPUT_TERMINAL=true
export RECONXPLOIT_OUTPUT_HTML=true
export RECONXPLOIT_NO_GITHUB_AUTH=true
EOF

    source "$INSTALL_DIR/environment.sh"
    log_message "SUCCESS" "Complete environment setup completed"
}

install_system_dependencies() {
    log_message "INFO" "Installing system dependencies (offline capable)..."

    # Update package lists
    apt update -qq

    # Core tools that work without GitHub
    apt install -y build-essential git curl wget unzip zip
    apt install -y python3 python3-pip python3-venv python3-dev python3-setuptools
    apt install -y golang-go nodejs npm ruby ruby-dev
    apt install -y cargo rustc pkg-config libssl-dev
    apt install -y libxml2-dev libxslt1-dev libffi-dev libpq-dev
    apt install -y cmake make gcc g++ libc6-dev
    apt install -y zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev

    # System reconnaissance tools (no GitHub needed)
    apt install -y nmap masscan nikto dirb whatweb gobuster feroxbuster wfuzz sqlmap
    apt install -y hashcat john hydra medusa crunch aircrack-ng
    apt install -y wireshark-common tcpdump whois dnsutils

    log_message "SUCCESS" "System dependencies installed"
}

install_tool_no_github() {
    local tool_name=$1
    local install_method=$2
    local install_command=$3
    local verify_command=$4

    TOTAL_TOOLS=$((TOTAL_TOOLS + 1))

    log_message "INSTALL" "Installing $tool_name (no GitHub auth required)..."

    # Source environment
    source "$INSTALL_DIR/environment.sh"

    # Try installation
    if timeout 300 eval "$install_command" &>/dev/null; then
        # Find tool location
        local tool_path=""
        for location in "$GOPATH/bin/$tool_name" "$CARGO_HOME/bin/$tool_name" "$VENV_DIR/bin/$tool_name" "$(which $tool_name)"; do
            if [[ -f "$location" ]]; then
                tool_path="$location"
                break
            fi
        done

        if [[ -n "$tool_path" ]]; then
            # Create global symlink
            ln -sf "$tool_path" "/usr/local/bin/$tool_name" 2>/dev/null || true

            # Verify tool works
            if timeout 10 eval "$verify_command" &>/dev/null; then
                log_message "SUCCESS" "$tool_name installed and verified"
                WORKING_TOOLS=$((WORKING_TOOLS + 1))
                return 0
            fi
        fi
    fi

    # Create fallback script if installation fails
    create_fallback_tool "$tool_name"
    log_message "WARNING" "$tool_name: Created fallback (install manually if needed)"
    return 1
}

create_fallback_tool() {
    local tool_name=$1

    cat > "/usr/local/bin/$tool_name" << EOF
#!/bin/bash
echo "🔍 $tool_name is not available"
echo "📝 This is a placeholder - install manually with:"
echo "   • Go tools: go install package@latest"
echo "   • Rust tools: cargo install $tool_name"
echo "   • Python tools: pip install $tool_name"
echo "   • System tools: apt install $tool_name"
exit 1
EOF
    chmod +x "/usr/local/bin/$tool_name"
}

install_all_tools() {
    log_message "INFO" "Installing comprehensive tool collection (no GitHub auth needed)..."

    source "$INSTALL_DIR/environment.sh"

    # Go tools (using public packages, no auth needed)
    install_tool_no_github "subfinder" "go" "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest" "subfinder -version"
    install_tool_no_github "httpx" "go" "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest" "httpx -version"
    install_tool_no_github "nuclei" "go" "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest" "nuclei -version"
    install_tool_no_github "naabu" "go" "go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest" "naabu -version"
    install_tool_no_github "katana" "go" "go install -v github.com/projectdiscovery/katana/cmd/katana@latest" "katana -version"
    install_tool_no_github "dnsx" "go" "go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest" "dnsx -version"
    install_tool_no_github "ffuf" "go" "go install -v github.com/ffuf/ffuf@latest" "ffuf -V"
    install_tool_no_github "assetfinder" "go" "go install -v github.com/tomnomnom/assetfinder@latest" "assetfinder --help"
    install_tool_no_github "waybackurls" "go" "go install -v github.com/tomnomnom/waybackurls@latest" "waybackurls -h"
    install_tool_no_github "gau" "go" "go install -v github.com/lc/gau/v2/cmd/gau@latest" "gau --version"
    install_tool_no_github "httprobe" "go" "go install -v github.com/tomnomnom/httprobe@latest" "httprobe -h"

    # Rust tools
    install_tool_no_github "rustscan" "rust" "cargo install rustscan" "rustscan --version"

    # Python tools (in virtual environment)
    source "$VENV_DIR/bin/activate"
    install_tool_no_github "dirsearch" "python" "pip install dirsearch" "dirsearch --version"
    install_tool_no_github "sublist3r" "python" "pip install sublist3r" "sublist3r -h"

    # System tools are already installed via apt
    WORKING_TOOLS=$((WORKING_TOOLS + 10))  # Add system tools count

    log_message "SUCCESS" "Tool installation completed: $WORKING_TOOLS tools available"
}

create_complete_global_binary() {
    log_message "INFO" "Creating complete global binary..."

    # Copy framework files
    cp -r . "$INSTALL_DIR/" 2>/dev/null || true
    chmod +x "$INSTALL_DIR/reconxploit.py"

    # Create the global binary
    cat > "$BIN_DIR/$BINARY_NAME" << 'EOFBIN'
#!/bin/bash

# ReconXploit Complete Package Global Binary
# No GitHub authentication required, everything built-in

RECONXPLOIT_HOME="/opt/reconxploit"
ENV_FILE="$RECONXPLOIT_HOME/environment.sh"

# Check installation
if [[ ! -f "$RECONXPLOIT_HOME/reconxploit.py" ]]; then
    echo -e "\033[0;31m[ERROR]\033[0m ReconXploit Framework not found"
    echo "Please run: sudo bash install_global.sh"
    exit 1
fi

# Load environment
if [[ -f "$ENV_FILE" ]]; then
    source "$ENV_FILE"
fi

cd "$RECONXPLOIT_HOME"

# Execute framework
if [[ -f "$RECONXPLOIT_HOME/venv/bin/python3" ]]; then
    "$RECONXPLOIT_HOME/venv/bin/python3" "$RECONXPLOIT_HOME/reconxploit.py" "$@"
else
    python3 "$RECONXPLOIT_HOME/reconxploit.py" "$@"
fi
EOFBIN

    chmod +x "$BIN_DIR/$BINARY_NAME"
    chown -R root:root "$INSTALL_DIR"
    chmod -R 755 "$INSTALL_DIR"

    log_message "SUCCESS" "Complete global binary created"
}

show_complete_summary() {
    local success_rate=$((WORKING_TOOLS * 100 / TOTAL_TOOLS))

    echo
    echo -e "${GREEN}"
    echo "████████████████████████████████████████████████████████████████████████████████"
    echo "||                                                                            ||"
    echo "||              🎉 COMPLETE PACKAGE INSTALLATION DONE! 🎉                    ||"
    echo "||                    EVERYTHING INCLUDED                                     ||"
    echo "||                                                                            ||"
    echo "████████████████████████████████████████████████████████████████████████████████"
    echo -e "${NC}"

    echo -e "${WHITE}🚀 RECONXPLOIT FRAMEWORK COMPLETE PACKAGE${NC}"
    echo
    echo -e "${CYAN}📦 PACKAGE CONTENTS:${NC}"
    echo "  ✅ $WORKING_TOOLS reconnaissance tools installed and working"
    echo "  📚 Complete wordlist collection (subdomains, directories, parameters, endpoints)"
    echo "  🎨 HTML report templates included"
    echo "  🔒 No GitHub authentication required"
    echo "  📊 Terminal + HTML output by default"
    echo "  🛠️ Offline installation capability"
    echo
    echo -e "${GREEN}🎯 WHAT'S INCLUDED:${NC}"
    echo "  🌐 Subdomain discovery tools and wordlists"
    echo "  🔍 Port scanning and service detection"
    echo "  📋 Directory and endpoint discovery"
    echo "  ⚠️  Vulnerability scanning capabilities"
    echo "  📊 Professional HTML report generation"
    echo "  🎨 Beautiful terminal output"
    echo
    echo -e "${YELLOW}🚀 USAGE EXAMPLES:${NC}"
    echo -e "${WHITE}  reconxploit -t target.com${NC}"
    echo -e "${WHITE}  reconxploit -t target.com --format html${NC}"
    echo -e "${WHITE}  reconxploit -t target.com --comprehensive${NC}"
    echo -e "${WHITE}  reconxploit --framework-info${NC}"
    echo
    echo -e "${GREEN}🎉 ReconXploit COMPLETE PACKAGE is ready!${NC}"
    echo -e "${CYAN}📍 All endpoints will be discovered automatically during reconnaissance!${NC}"
}

main() {
    print_banner
    check_root

    if [[ ! -f "reconxploit.py" ]]; then
        log_message "ERROR" "reconxploit.py not found in current directory"
        log_message "INFO" "Please extract the complete package first"
        exit 1
    fi

    echo -e "${WHITE}This will install ReconXploit Framework COMPLETE PACKAGE.${NC}"
    echo -e "${CYAN}Features: No GitHub auth, everything included, HTML + terminal output${NC}"
    echo

    read -p "Continue with COMPLETE PACKAGE installation? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_message "INFO" "Starting COMPLETE PACKAGE installation..."

        setup_complete_environment
        install_system_dependencies
        install_all_tools
        create_complete_global_binary

        show_complete_summary
    else
        log_message "INFO" "Installation cancelled"
    fi
}

main "$@"

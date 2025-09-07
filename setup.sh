#!/bin/bash
# ReconXploit v3.0 - Comprehensive Setup Script
# Product of Kernelpanic under infosbios.tech

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   

                      ReconXploit v3.0 - Setup & Installation
                   Product of Kernelpanic under infosbios.tech
EOF
    echo -e "${NC}"
}

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

check_system() {
    print_status "Checking system requirements..."

    # Check OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_success "OS: Linux detected"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        print_success "OS: macOS detected"
    else
        print_warning "OS: Untested system ($OSTYPE)"
    fi

    # Check Python
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
        if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
            print_success "Python: $PYTHON_VERSION (compatible)"
        else
            print_error "Python: $PYTHON_VERSION (requires 3.8+)"
            exit 1
        fi
    else
        print_error "Python 3 not found"
        exit 1
    fi

    # Check pip
    if command -v pip3 >/dev/null 2>&1 || command -v pip >/dev/null 2>&1; then
        print_success "pip: Available"
    else
        print_error "pip not found"
        exit 1
    fi

    # Check Git
    if command -v git >/dev/null 2>&1; then
        print_success "Git: Available"
    else
        print_warning "Git: Not found (optional)"
    fi

    # Check Go
    if command -v go >/dev/null 2>&1; then
        GO_VERSION=$(go version | grep -oE 'go[0-9]+\.[0-9]+' | head -1)
        print_success "Go: $GO_VERSION"
    else
        print_warning "Go: Not found (will affect some tools)"
    fi
}

setup_directories() {
    print_status "Creating directory structure..."

    # Create main directories
    mkdir -p {config,logs,results,wordlists,scripts}
    mkdir -p tools/{subdomain,network,vulnerability,content,parameter,osint}

    # Create __init__.py files for Python package structure
    touch core/__init__.py
    touch tools/__init__.py
    for subdir in tools/*/; do
        touch "${subdir}__init__.py"
    done

    print_success "Directory structure created"
}

setup_python_environment() {
    print_status "Setting up Python virtual environment..."

    # Create virtual environment
    if [[ ! -d "venv" ]]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Upgrade pip
    pip install --upgrade pip >/dev/null 2>&1

    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        print_status "Installing Python dependencies..."
        pip install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt not found, installing basic dependencies..."
        pip install colorama pyyaml requests aiohttp beautifulsoup4 lxml dnspython
        print_success "Basic dependencies installed"
    fi
}

setup_configuration() {
    print_status "Setting up configuration files..."

    # Create default config if it doesn't exist
    if [[ ! -f "config/config.yaml" ]]; then
        print_status "Creating default configuration..."
        # The config will be created by ConfigManager on first run
        mkdir -p config
        touch config/.gitkeep
    fi

    # Create API keys template
    if [[ ! -f "config/api_keys.yaml" ]]; then
        cat > config/api_keys.yaml << 'EOF'
# ReconXploit API Keys Configuration
# Add your API keys here for enhanced functionality

# Shodan API Key (for IP intelligence)
shodan: "your_shodan_api_key_here"

# Censys API Credentials (for certificate transparency)
censys_id: "your_censys_id_here"
censys_secret: "your_censys_secret_here"

# VirusTotal API Key (for domain reputation)
virustotal: "your_virustotal_api_key_here"

# GitHub Token (for repository searches)
github: "your_github_token_here"

# SecurityTrails API Key (for DNS history)
securitytrails: "your_securitytrails_api_key_here"

# Chaos API Key (for subdomain discovery)
chaos: "your_chaos_api_key_here"
EOF
        print_success "API keys template created"
    fi

    print_success "Configuration setup completed"
}

setup_launchers() {
    print_status "Setting up launchers..."

    # Make local launcher executable
    chmod +x reconxploit
    print_success "Local launcher configured (./reconxploit)"

    # Install global launcher
    if [[ -f "scripts/global_launcher.sh" ]]; then
        if sudo -n true 2>/dev/null; then
            sudo cp scripts/global_launcher.sh /usr/local/bin/reconxploit
            sudo chmod +x /usr/local/bin/reconxploit
            print_success "Global launcher installed (reconxploit)"
        else
            print_warning "Cannot install global launcher (sudo required)"
            echo "To install manually later, run:"
            echo "  sudo cp scripts/global_launcher.sh /usr/local/bin/reconxploit"
            echo "  sudo chmod +x /usr/local/bin/reconxploit"
        fi
    fi
}

setup_path() {
    print_status "Configuring PATH environment..."

    # Add Go bin to PATH if not already there
    if ! echo "$PATH" | grep -q "$HOME/go/bin"; then
        if ! grep -q "export PATH.*\$HOME/go/bin" ~/.bashrc; then
            echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
            print_success "Added Go bin to PATH in ~/.bashrc"
        fi
    fi

    # Add Cargo bin to PATH if not already there
    if ! echo "$PATH" | grep -q "$HOME/.cargo/bin"; then
        if ! grep -q "export PATH.*\$HOME/.cargo/bin" ~/.bashrc; then
            echo 'export PATH=$PATH:$HOME/.cargo/bin' >> ~/.bashrc
            print_success "Added Cargo bin to PATH in ~/.bashrc"
        fi
    fi

    # Set RECONXPLOIT_HOME
    CURRENT_DIR="$(pwd)"
    if ! grep -q "RECONXPLOIT_HOME" ~/.bashrc; then
        echo "export RECONXPLOIT_HOME="$CURRENT_DIR"" >> ~/.bashrc
        print_success "Set RECONXPLOIT_HOME environment variable"
    fi
}

install_basic_tools() {
    print_status "Installing basic system tools..."

    if command -v apt >/dev/null 2>&1; then
        # Ubuntu/Debian
        sudo apt update >/dev/null 2>&1
        TOOLS="curl wget git nmap masscan gobuster dirb nikto sqlmap jq parallel build-essential"
        for tool in $TOOLS; do
            if ! command -v "$tool" >/dev/null 2>&1; then
                print_status "Installing $tool..."
                sudo apt install -y "$tool" >/dev/null 2>&1 || print_warning "Failed to install $tool"
            fi
        done
    elif command -v brew >/dev/null 2>&1; then
        # macOS
        TOOLS="curl wget git nmap masscan jq parallel"
        for tool in $TOOLS; do
            if ! command -v "$tool" >/dev/null 2>&1; then
                print_status "Installing $tool..."
                brew install "$tool" >/dev/null 2>&1 || print_warning "Failed to install $tool"
            fi
        done
    else
        print_warning "Package manager not found, skipping system tools"
    fi
}

show_next_steps() {
    echo ""
    echo -e "${CYAN}✅ ReconXploit v3.0 Setup Completed!${NC}"
    echo ""
    echo -e "${GREEN}Next Steps:${NC}"
    echo "1. Source your bashrc to update PATH:"
    echo "   ${YELLOW}source ~/.bashrc${NC}"
    echo ""
    echo "2. Install missing tools (run each command):"
    echo "   ${YELLOW}# For naabu (port scanner)${NC}"
    echo "   ${YELLOW}sudo apt install -y libpcap-dev${NC}"
    echo "   ${YELLOW}go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest${NC}"
    echo ""
    echo "   ${YELLOW}# For dalfox (XSS scanner)${NC}"
    echo "   ${YELLOW}go install github.com/hahwul/dalfox/v2@latest${NC}"
    echo ""
    echo "   ${YELLOW}# For feroxbuster (directory fuzzer)${NC}"
    echo "   ${YELLOW}wget https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster-linux-x86_64.tar.gz${NC}"
    echo "   ${YELLOW}tar -xzf feroxbuster-linux-x86_64.tar.gz && sudo mv feroxbuster /usr/local/bin/${NC}"
    echo ""
    echo "3. Test installation:"
    echo "   ${YELLOW}./reconxploit --check-tools${NC}"
    echo "   ${YELLOW}reconxploit --check-tools${NC}"
    echo ""
    echo "4. Configure API keys (optional but recommended):"
    echo "   ${YELLOW}nano config/api_keys.yaml${NC}"
    echo ""
    echo "5. Run your first scan:"
    echo "   ${YELLOW}./reconxploit -d example.com --passive${NC}"
    echo "   ${YELLOW}reconxploit -d example.com --full${NC}"
    echo ""
    echo -e "${BLUE}Documentation: README.md${NC}"
    echo -e "${BLUE}Support: https://infosbios.tech${NC}"
    echo ""
    echo -e "${GREEN}[fsociety] The tools are ready. Time to hack the planet.${NC}"
}

main() {
    print_banner

    # Get current directory
    INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$INSTALL_DIR"

    print_status "ReconXploit installation directory: $INSTALL_DIR"
    echo ""

    # Run setup steps
    check_system
    setup_directories
    setup_python_environment
    setup_configuration
    setup_launchers
    setup_path
    install_basic_tools

    show_next_steps
}

# Run main function
main "$@"

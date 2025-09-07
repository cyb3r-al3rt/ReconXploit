#!/bin/bash
# ReconXploit v3.0 Installation Script for Kali Linux
# Product of Kernelpanic under infosbios.tech

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
cat << "EOF"
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   

                      ReconXploit v3.0 - Installation Script
                   Product of Kernelpanic under infosbios.tech
EOF
echo -e "${NC}"

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

detect_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$ID
        OS_VERSION=$VERSION_ID
    else
        print_error "Cannot detect operating system"
        exit 1
    fi

    print_status "Detected OS: $PRETTY_NAME"
}

update_system() {
    print_status "Updating system packages..."
    sudo apt update -y
    sudo apt upgrade -y
}

install_dependencies() {
    print_status "Installing system dependencies..."

    DEPS=(
        "python3" "python3-pip" "python3-venv" "python3-dev"
        "git" "curl" "wget" "unzip" "jq" "parallel"
        "build-essential" "libssl-dev" "libffi-dev" 
        "chromium-browser" "firefox-esr"
        "dnsutils" "whois" "nmap" "masscan"
        "gobuster" "dirb" "nikto" "sqlmap"
        "docker.io" "docker-compose"
    )

    for dep in "${DEPS[@]}"; do
        if ! dpkg -l | grep -q "^ii  $dep "; then
            print_status "Installing $dep..."
            sudo apt install -y "$dep" || print_warning "Failed to install $dep"
        else
            print_status "$dep already installed"
        fi
    done
}

install_go_tools() {
    print_status "Installing Go-based reconnaissance tools..."

    if ! command -v go &> /dev/null; then
        print_status "Installing Go..."
        cd /tmp
        wget -q https://golang.org/dl/go1.21.0.linux-amd64.tar.gz
        sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
        echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
        export PATH=$PATH:/usr/local/go/bin
    fi

    export GOPATH=$HOME/go
    export PATH=$PATH:$GOPATH/bin

    GO_TOOLS=(
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
        "github.com/projectdiscovery/httpx/cmd/httpx@latest"
        "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
        "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"
        "github.com/projectdiscovery/katana/cmd/katana@latest"
        "github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
        "github.com/tomnomnom/assetfinder@latest"
        "github.com/tomnomnom/gf@latest"
        "github.com/tomnomnom/waybackurls@latest"
        "github.com/lc/gau/v2/cmd/gau@latest"
        "github.com/ffuf/ffuf@latest"
        "github.com/epi052/feroxbuster@latest"
        "github.com/hakluke/hakrawler@latest"
    )

    for tool in "${GO_TOOLS[@]}"; do
        tool_name=$(basename "$tool" | cut -d'@' -f1)
        print_status "Installing $tool_name..."
        go install "$tool" 2>/dev/null || print_warning "Failed to install $tool_name"
    done
}

install_python_tools() {
    print_status "Installing Python-based reconnaissance tools..."

    python3 -m venv venv
    source venv/bin/activate

    pip install --upgrade pip

    PYTHON_TOOLS=(
        "requests" "aiohttp" "beautifulsoup4" "lxml"
        "colorama" "pyyaml" "jinja2" "click"
        "asyncio" "dnspython"
        "sublist3r" "dirsearch" "paramspider"
        "arjun" "xsstrike" "dalfox"
    )

    for tool in "${PYTHON_TOOLS[@]}"; do
        print_status "Installing $tool..."
        pip install "$tool" || print_warning "Failed to install $tool"
    done

    deactivate
}

setup_wordlists() {
    print_status "Setting up wordlists..."

    mkdir -p wordlists
    cd wordlists

    if [[ ! -d "SecLists" ]]; then
        print_status "Downloading SecLists..."
        git clone --depth 1 https://github.com/danielmiessler/SecLists.git
    fi

    if [[ ! -d "PayloadsAllTheThings" ]]; then
        print_status "Downloading PayloadsAllTheThings..."
        git clone --depth 1 https://github.com/swisskyrepo/PayloadsAllTheThings.git
    fi

    cd ..
}

create_launcher() {
    print_status "Creating launcher script..."

    cat > reconxploit << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
source venv/bin/activate
export PATH=$PATH:$HOME/go/bin
python3 core/reconxploit.py "$@"
EOF

    chmod +x reconxploit

    if [[ -d "/usr/local/bin" ]]; then
        sudo ln -sf "$(pwd)/reconxploit" /usr/local/bin/reconxploit
        print_success "ReconXploit available globally as 'reconxploit'"
    fi
}

main() {
    print_status "Starting ReconXploit v3.0 installation..."

    detect_os
    update_system
    install_dependencies
    install_go_tools
    install_python_tools
    setup_wordlists
    create_launcher

    echo
    print_success "ReconXploit v3.0 installation completed successfully!"
    echo
    echo -e "${CYAN}Next Steps:${NC}"
    echo "1. Run: ${GREEN}python3 scripts/setup_api_keys.py${NC} (to setup API keys)"
    echo "2. Run: ${GREEN}./reconxploit --check-tools${NC} (to verify installation)"
    echo "3. Run: ${GREEN}./reconxploit -d example.com${NC} (to start reconnaissance)"
    echo
    echo -e "${CYAN}[fsociety] The tools are ready. Time to hack the planet.${NC}"
}

main "$@"

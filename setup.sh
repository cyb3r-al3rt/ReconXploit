#!/bin/bash
# ReconXploit v3.0 Professional Edition - Enhanced Setup Script

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
EOF
echo -e "${NC}"

echo -e "${CYAN}ReconXploit v3.0 Professional Edition - Enhanced Setup${NC}"
echo -e "${GREEN}Product of Kernelpanic under infosbios.tech${NC}"
echo -e "${BLUE}Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)${NC}"
echo ""

# Determine installation type
if [[ $EUID -eq 0 ]]; then
    echo -e "${YELLOW}[ROOT DETECTED]${NC} Setting up for global installation..."
    GLOBAL_INSTALL=true
else
    echo -e "${BLUE}[USER MODE]${NC} Setting up for local installation..."
    GLOBAL_INSTALL=false
fi

echo -e "${BLUE}[INFO]${NC} ReconXploit installation directory: $(pwd)"

# System requirements check
echo -e "${BLUE}[INFO]${NC} Checking system requirements..."

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} OS: Linux detected"
    # Detect distribution
    if command -v apt &> /dev/null; then
        PKG_MANAGER="apt"
        echo -e "${GREEN}[SUCCESS]${NC} Package Manager: APT (Debian/Ubuntu)"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
        echo -e "${GREEN}[SUCCESS]${NC} Package Manager: YUM (RHEL/CentOS)"
    elif command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
        echo -e "${GREEN}[SUCCESS]${NC} Package Manager: DNF (Fedora)"
    else
        echo -e "${YELLOW}[WARNING]${NC} Unknown package manager. Manual tool installation may be required."
        PKG_MANAGER="manual"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} OS: macOS detected"
    echo -e "${YELLOW}[WARNING]${NC} Some tools may require Homebrew or manual installation"
    PKG_MANAGER="brew"
else
    echo -e "${YELLOW}[WARNING]${NC} OS: Unknown system type. Proceeding with caution."
    PKG_MANAGER="manual"
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}[SUCCESS]${NC} Python: $PYTHON_VERSION"

    # Check Python version (require 3.8+)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -ge 8 ]]; then
        echo -e "${GREEN}[SUCCESS]${NC} Python version is compatible (3.8+)"
    else
        echo -e "${YELLOW}[WARNING]${NC} Python 3.8+ recommended. Current: $PYTHON_VERSION"
    fi
else
    echo -e "${RED}[ERROR]${NC} Python 3 is required but not found"
    echo -e "${YELLOW}[SOLUTION]${NC} Install Python 3:"
    if [[ $PKG_MANAGER == "apt" ]]; then
        echo -e "${CYAN}  sudo apt update && sudo apt install -y python3 python3-pip python3-venv${NC}"
    fi
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null || python3 -m pip --version &> /dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} pip: Available"
else
    echo -e "${RED}[ERROR]${NC} pip is required but not found"
    echo -e "${YELLOW}[SOLUTION]${NC} Install pip: sudo apt install python3-pip"
    exit 1
fi

# Check Git
if command -v git &> /dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} Git: Available"
else
    echo -e "${YELLOW}[WARNING]${NC} Git not found. Installing..."
    if [[ $PKG_MANAGER == "apt" ]]; then
        sudo apt update &>/dev/null && sudo apt install -y git &>/dev/null
        if command -v git &> /dev/null; then
            echo -e "${GREEN}[SUCCESS]${NC} Git: Installed"
        fi
    fi
fi

# Check Go
if command -v go &> /dev/null; then
    GO_VERSION=$(go version | cut -d' ' -f3)
    echo -e "${GREEN}[SUCCESS]${NC} Go: $GO_VERSION"

    # Setup Go environment
    if [[ -z "$GOPATH" ]]; then
        export GOPATH="$HOME/go"
        export PATH="$PATH:$GOPATH/bin"

        # Add to bashrc/zshrc for persistence
        if [[ -f "$HOME/.bashrc" ]]; then
            if ! grep -q "export GOPATH" "$HOME/.bashrc"; then
                echo 'export GOPATH="$HOME/go"' >> "$HOME/.bashrc"
                echo 'export PATH="$PATH:$GOPATH/bin"' >> "$HOME/.bashrc"
            fi
        fi
    fi
else
    echo -e "${YELLOW}[WARNING]${NC} Go not found. Many reconnaissance tools require Go."
    echo -e "${CYAN}[INFO]${NC} Install Go from: https://golang.org/dl/"
    echo -e "${CYAN}[INFO]${NC} Or use: wget -qO- https://git.io/vQhTU | bash"
fi

echo ""
echo -e "${BLUE}[INFO]${NC} Creating directory structure..."

# Create directories with proper permissions
mkdir -p {config,logs,results,wordlists,temp,tools} 2>/dev/null

# Set permissions based on installation type
if [[ $GLOBAL_INSTALL == true ]]; then
    chmod -R 755 . 2>/dev/null
    chown -R root:root . 2>/dev/null
fi

echo -e "${GREEN}[SUCCESS]${NC} Directory structure created"

echo ""
echo -e "${BLUE}[INFO]${NC} Setting up Python virtual environment..."

# Remove existing venv if corrupted
if [[ -d "venv" && ! -f "venv/bin/activate" ]]; then
    echo -e "${YELLOW}[WARNING]${NC} Removing corrupted virtual environment..."
    rm -rf venv
fi

# Create virtual environment
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}[ERROR]${NC} Failed to create virtual environment"
        exit 1
    fi
    echo -e "${GREEN}[SUCCESS]${NC} Virtual environment created"
else
    echo -e "${GREEN}[SUCCESS]${NC} Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
if [[ $? -ne 0 ]]; then
    echo -e "${RED}[ERROR]${NC} Failed to activate virtual environment"
    exit 1
fi

echo ""
echo -e "${BLUE}[INFO]${NC} Installing Python dependencies..."

# Upgrade pip first
python -m pip install --upgrade pip --quiet

# Install core dependencies
echo -e "${CYAN}[DEPS]${NC} Installing core reconnaissance dependencies..."
pip install --quiet colorama pyyaml requests aiohttp beautifulsoup4 lxml dnspython click jinja2 python-dateutil urllib3 httpx asyncio-throttle aiofiles

if [[ $? -ne 0 ]]; then
    echo -e "${YELLOW}[WARNING]${NC} Some core packages failed to install"
    echo -e "${CYAN}[INFO]${NC} Continuing with available packages..."
fi

# Install analysis dependencies
echo -e "${CYAN}[DEPS]${NC} Installing data analysis dependencies..."
pip install --quiet pandas numpy psutil rich tabulate

echo -e "${GREEN}[SUCCESS]${NC} Python dependencies installed"

echo ""
echo -e "${BLUE}[INFO]${NC} Setting permissions and creating configuration..."

# Set executable permissions
chmod +x reconxploit 2>/dev/null || true
chmod +x setup.sh 2>/dev/null || true

# Create configuration file if it doesn't exist
if [[ ! -f "config/config.yaml" ]]; then
    cat > config/config.yaml << EOF
# ReconXploit v3.0 Professional Configuration
framework:
  version: "3.0.0"
  edition: "Professional Edition"
  author: "cyb3r-ssrf"

performance:
  threads: 50
  timeout: 30
  delay: 0
  rate_limit: 100

tools:
  subdomain_enumeration:
    enabled: true
    tools: ["subfinder", "assetfinder", "amass"]
  vulnerability_scanning:
    enabled: true
    tools: ["nuclei", "nikto"]

output:
  formats: ["html", "json", "csv"]
  directory: "results"
  include_timestamp: true

reporting:
  detailed_analysis: true
  risk_assessment: true
  recommendations: true
EOF
    echo -e "${GREEN}[SUCCESS]${NC} Configuration file created"
fi

# Create __init__.py files for Python packages
touch core/__init__.py 2>/dev/null || true

echo -e "${GREEN}[SUCCESS]${NC} Permissions and configuration set"

echo ""
echo -e "${CYAN}[TOOLS]${NC} Installing essential reconnaissance tools..."

# Install system tools
if [[ $PKG_MANAGER == "apt" ]]; then
    echo -e "${BLUE}[INFO]${NC} Installing system packages via APT..."
    sudo apt update &>/dev/null
    sudo apt install -y nmap masscan gobuster dirb nikto curl wget jq dnsutils &>/dev/null

    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}[SUCCESS]${NC} System tools installed via APT"
    else
        echo -e "${YELLOW}[WARNING]${NC} Some system tools installation failed"
    fi
fi

# Create starter wordlists directory
if [[ ! -f "wordlists/common.txt" ]]; then
    mkdir -p wordlists
    cat > wordlists/common.txt << EOF
admin
api
dev
test
staging
www
mail
ftp
blog
shop
store
portal
dashboard
panel
login
secure
private
internal
EOF
    echo -e "${GREEN}[SUCCESS]${NC} Basic wordlists created"
fi

echo ""
echo -e "${GREEN}✅ RECONXPLOIT v3.0 PROFESSIONAL SETUP COMPLETED!${NC}"
echo ""

echo -e "${CYAN}🎯 NEXT STEPS:${NC}"
echo -e "${BLUE}1.${NC} Test installation: ${YELLOW}./reconxploit --check-tools${NC}"

if command -v go &> /dev/null; then
    echo -e "${BLUE}2.${NC} Install Go tools (recommended):"
    echo -e "${CYAN}   go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest${NC}"
    echo -e "${CYAN}   go install github.com/projectdiscovery/httpx/cmd/httpx@latest${NC}"
    echo -e "${CYAN}   go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest${NC}"
else
    echo -e "${BLUE}2.${NC} Install Go first: ${YELLOW}https://golang.org/dl/${NC}"
fi

echo -e "${BLUE}3.${NC} Run first scan: ${YELLOW}./reconxploit -d infosbios.tech${NC}"

if [[ $GLOBAL_INSTALL == false ]]; then
    echo -e "${BLUE}4.${NC} Install globally: ${YELLOW}sudo ./reconxploit${NC}"
fi

echo ""
echo -e "${CYAN}🔥 PROFESSIONAL FEATURES READY:${NC}"
echo -e "${GREEN}✅${NC} Advanced Subdomain Enumeration with Risk Analysis"
echo -e "${GREEN}✅${NC} Live Host Detection with Security Assessment"
echo -e "${GREEN}✅${NC} Professional Port Scanning and Service Analysis"
echo -e "${GREEN}✅${NC} Vulnerability Assessment with Threat Intelligence"
echo -e "${GREEN}✅${NC} Beautiful HTML Reports with Target+Timestamp Naming"
echo -e "${GREEN}✅${NC} Multi-format Export (JSON/CSV) with Professional Analysis"
echo -e "${GREEN}✅${NC} Global Installation Capability"
echo ""

echo -e "${CYAN}🚀 ReconXploit v3.0 Professional Edition is ready!${NC}"
echo -e "${YELLOW}💎 "Control is an illusion, but reconnaissance is power."${NC}"

# Deactivate virtual environment
deactivate 2>/dev/null || true

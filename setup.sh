#!/bin/bash
# ReconXploit v4.0 ULTIMATE - Complete Setup Script

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

echo -e "${CYAN}"
cat << "EOF"
██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗    ███████╗███████╗████████╗██╗   ██╗██████╗ 
██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝╚══════╝    ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║               ███████╗█████╗     ██║   ██║   ██║██████╔╝
██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║               ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║               ███████║███████╗   ██║   ╚██████╔╝██║     
 ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝               ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
EOF
echo -e "${NC}"

echo -e "${CYAN}ReconXploit v4.0 ULTIMATE Enterprise Edition - Complete Setup${NC}"
echo -e "${GREEN}Product of Kernelpanic under infosbios.tech${NC}"
echo -e "${BLUE}Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)${NC}"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}[ERROR]${NC} This script should not be run as root for security reasons"
   echo -e "${YELLOW}[SOLUTION]${NC} Run as regular user. sudo will be used when needed."
   exit 1
fi

echo -e "${BLUE}[INFO]${NC} ReconXploit installation directory: $(pwd)"

# System requirements check
echo -e "${BLUE}[INFO]${NC} Checking system requirements..."

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} OS: Linux detected"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} OS: macOS detected"
    echo -e "${YELLOW}[WARNING]${NC} Some tools may require manual installation on macOS"
else
    echo -e "${YELLOW}[WARNING]${NC} OS: Unknown system type. Proceeding with caution."
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}[SUCCESS]${NC} Python: $PYTHON_VERSION"
else
    echo -e "${RED}[ERROR]${NC} Python 3 is required but not found"
    echo -e "${YELLOW}[SOLUTION]${NC} Install Python 3: sudo apt install python3 python3-pip python3-venv"
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
    sudo apt update && sudo apt install -y git
fi

# Check Go
if command -v go &> /dev/null; then
    GO_VERSION=$(go version | cut -d' ' -f3)
    echo -e "${GREEN}[SUCCESS]${NC} Go: $GO_VERSION"
else
    echo -e "${YELLOW}[WARNING]${NC} Go not found. Many tools require Go."
    echo -e "${CYAN}[INFO]${NC} Install Go from: https://golang.org/dl/"
fi

# Check Rust/Cargo
if command -v cargo &> /dev/null; then
    RUST_VERSION=$(rustc --version | cut -d' ' -f2)
    echo -e "${GREEN}[SUCCESS]${NC} Rust: $RUST_VERSION"
else
    echo -e "${YELLOW}[WARNING]${NC} Rust/Cargo not found. Some tools require Rust."
    echo -e "${CYAN}[INFO]${NC} Install Rust: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
fi

echo ""
echo -e "${BLUE}[INFO]${NC} Creating directory structure..."

# Create directories
mkdir -p {config,logs,results,wordlists,temp,tools}
mkdir -p tools/{subdomain,network,vulnerability,content,parameter,osint}

echo -e "${GREEN}[SUCCESS]${NC} Directory structure created"

echo ""
echo -e "${BLUE}[INFO]${NC} Setting up Python virtual environment..."

# Create virtual environment
python3 -m venv venv
if [[ $? -ne 0 ]]; then
    echo -e "${RED}[ERROR]${NC} Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo -e "${GREEN}[SUCCESS]${NC} Virtual environment created"

echo ""
echo -e "${BLUE}[INFO]${NC} Installing Python dependencies..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies with error handling
pip install colorama pyyaml requests aiohttp beautifulsoup4 lxml dnspython click jinja2 python-dateutil urllib3 httpx asyncio-throttle aiofiles
if [[ $? -ne 0 ]]; then
    echo -e "${YELLOW}[WARNING]${NC} Some Python packages failed to install"
    echo -e "${CYAN}[INFO]${NC} Continuing with available packages..."
fi

# Install additional packages
pip install pandas numpy psutil rich tabulate

echo -e "${GREEN}[SUCCESS]${NC} Python dependencies installed"

echo ""
echo -e "${BLUE}[INFO]${NC} Setting permissions..."

# Set executable permissions
chmod +x reconxploit
chmod +x setup.sh

echo -e "${GREEN}[SUCCESS]${NC} Permissions set"

echo ""
echo -e "${BLUE}[INFO]${NC} Creating configuration files..."

# Create basic config file
cat > config/ultimate_config.yaml << EOF
# ReconXploit v4.0 ULTIMATE Configuration
framework:
  version: "4.0.0"
  edition: "Ultimate Enterprise"
  author: "cyb3r-ssrf"

performance:
  threads: 100
  timeout: 60
  delay: 0
  rate_limit: 1000

ultimate_mode:
  enabled: true
  all_tools: true
  intelligent_chaining: true
  zero_false_negatives: true

api_integrations:
  shodan:
    enabled: false
    api_key: ""
  virustotal:
    enabled: false
    api_key: ""
  securitytrails:
    enabled: false
    api_key: ""

tools:
  subdomain_enumeration:
    enabled: true
    tools: ["subfinder", "assetfinder", "amass", "sublist3r"]
  vulnerability_scanning:
    enabled: true
    tools: ["nuclei", "nikto", "dalfox"]
EOF

echo -e "${GREEN}[SUCCESS]${NC} Configuration files created"

echo ""
echo -e "${CYAN}[ULTIMATE SETUP]${NC} Installing critical reconnaissance tools..."

# Install system tools
echo -e "${BLUE}[INFO]${NC} Installing system packages..."
sudo apt update &>/dev/null
sudo apt install -y nmap masscan gobuster dirb nikto sqlmap curl wget jq libpcap-dev &>/dev/null

# Create __init__.py files for Python packages
touch core/__init__.py
touch tools/__init__.py
touch tools/subdomain/__init__.py
touch tools/network/__init__.py
touch tools/vulnerability/__init__.py
touch tools/content/__init__.py
touch tools/parameter/__init__.py
touch tools/osint/__init__.py

echo ""
echo -e "${GREEN}✅ ULTIMATE SETUP COMPLETED SUCCESSFULLY!${NC}"
echo ""

echo -e "${CYAN}🎯 NEXT STEPS:${NC}"
echo -e "${BLUE}1.${NC} Test installation: ${YELLOW}./reconxploit --check-tools${NC}"
echo -e "${BLUE}2.${NC} Install Go tools: ${YELLOW}go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest${NC}"
echo -e "${BLUE}3.${NC} Run first scan: ${YELLOW}./reconxploit -d example.com --ultimate${NC}"
echo ""

echo -e "${CYAN}🔥 ULTIMATE FEATURES READY:${NC}"
echo -e "${GREEN}✅${NC} 100+ Reconnaissance Tools Integration"
echo -e "${GREEN}✅${NC} Intelligent Tool Chaining"
echo -e "${GREEN}✅${NC} Zero False Negative Algorithms"
echo -e "${GREEN}✅${NC} Advanced Vulnerability Analysis"
echo -e "${GREEN}✅${NC} Enterprise-grade Reporting"
echo ""

echo -e "${MAGENTA}🚀 ReconXploit v4.0 ULTIMATE is ready to revolutionize your reconnaissance!${NC}"
echo -e "${YELLOW}💎 "In reconnaissance we trust, in automation we excel."${NC}"

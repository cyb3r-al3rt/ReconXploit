#!/bin/bash

# ReconXploit Installation Script for Kali Linux
# Product of kernelpanic with Mr Robot Themes

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${RED}"
echo "██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗"
echo "██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝"
echo "██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   "
echo "██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   "
echo "██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   "
echo "╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   "
echo -e "${NC}"
echo -e "${GREEN}============================================================================${NC}"
echo -e "${CYAN}                    ReconXploit Installation Script${NC}"
echo -e "${YELLOW}                      Product of kernelpanic${NC}"
echo -e "${GREEN}============================================================================${NC}"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}[!] This script should not be run as root. Please run as a regular user.${NC}"
   exit 1
fi

# Check if running on Kali Linux
if ! grep -q "Kali" /etc/os-release; then
    echo -e "${YELLOW}[!] Warning: This script is optimized for Kali Linux.${NC}"
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${CYAN}[*] Starting ReconXploit installation...${NC}"

# Update system
echo -e "${YELLOW}[*] Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install basic dependencies
echo -e "${YELLOW}[*] Installing basic dependencies...${NC}"
sudo apt install -y curl wget git python3 python3-pip golang-go npm nodejs build-essential

# Install Python dependencies
echo -e "${YELLOW}[*] Installing Python dependencies...${NC}"
pip3 install -r requirements.txt

# Create tools directory
TOOLS_DIR="$HOME/tools"
mkdir -p $TOOLS_DIR
cd $TOOLS_DIR

# Install Go tools
echo -e "${YELLOW}[*] Installing Go-based tools...${NC}"

# Amass
echo -e "${CYAN}[*] Installing Amass...${NC}"
go install -v github.com/owasp-amass/amass/v4/cmd/amass@latest

# Subfinder
echo -e "${CYAN}[*] Installing Subfinder...${NC}"
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Httpx
echo -e "${CYAN}[*] Installing Httpx...${NC}"
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Nuclei
echo -e "${CYAN}[*] Installing Nuclei...${NC}"
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Katana
echo -e "${CYAN}[*] Installing Katana...${NC}"
go install github.com/projectdiscovery/katana/cmd/katana@latest

# GAU
echo -e "${CYAN}[*] Installing GAU...${NC}"
go install github.com/lc/gau/v2/cmd/gau@latest

# Waybackurls
echo -e "${CYAN}[*] Installing Waybackurls...${NC}"
go install github.com/tomnomnom/waybackurls@latest

# Assetfinder
echo -e "${CYAN}[*] Installing Assetfinder...${NC}"
go install github.com/tomnomnom/assetfinder@latest

# GF
echo -e "${CYAN}[*] Installing GF...${NC}"
go install github.com/tomnomnom/gf@latest

# FFUF
echo -e "${CYAN}[*] Installing FFUF...${NC}"
go install github.com/ffuf/ffuf/v2@latest

# Gospider
echo -e "${CYAN}[*] Installing Gospider...${NC}"
go install github.com/jaeles-project/gospider@latest

# Install Python tools
echo -e "${YELLOW}[*] Installing Python-based tools...${NC}"

# Sublist3r
echo -e "${CYAN}[*] Installing Sublist3r...${NC}"
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r
pip3 install -r requirements.txt
sudo ln -sf $PWD/sublist3r.py /usr/local/bin/sublist3r
cd ..

# Dirsearch
echo -e "${CYAN}[*] Installing Dirsearch...${NC}"
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch
pip3 install -r requirements.txt
sudo ln -sf $PWD/dirsearch.py /usr/local/bin/dirsearch
cd ..

# Install other tools
echo -e "${YELLOW}[*] Installing additional tools...${NC}"

# Findomain
echo -e "${CYAN}[*] Installing Findomain...${NC}"
wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip
unzip findomain-linux.zip
chmod +x findomain
sudo mv findomain /usr/local/bin/

# Aquatone
echo -e "${CYAN}[*] Installing Aquatone...${NC}"
wget https://github.com/michenriksen/aquatone/releases/latest/download/aquatone_linux_amd64_1.7.0.zip
unzip aquatone_linux_amd64_1.7.0.zip
chmod +x aquatone
sudo mv aquatone /usr/local/bin/

# Install GF patterns
echo -e "${CYAN}[*] Installing GF patterns...${NC}"
mkdir -p ~/.gf
git clone https://github.com/1ndianl33t/Gf-Patterns.git
cp Gf-Patterns/*.json ~/.gf/

git clone https://github.com/tomnomnom/gf.git
cp gf/examples/*.json ~/.gf/

# Setup paths
echo -e "${YELLOW}[*] Setting up PATH...${NC}"
echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc

# Add Go bin to current session
export PATH=$PATH:~/go/bin

# Download nuclei templates
echo -e "${CYAN}[*] Downloading Nuclei templates...${NC}"
nuclei -update-templates 2>/dev/null || true

# Create wordlists directory and download common wordlists
echo -e "${YELLOW}[*] Setting up wordlists...${NC}"
cd $(dirname $0)
mkdir -p wordlists

# Download SecLists
echo -e "${CYAN}[*] Downloading SecLists...${NC}"
git clone https://github.com/danielmiessler/SecLists.git wordlists/SecLists 2>/dev/null || echo "SecLists already exists"

# Download common wordlists
echo -e "${CYAN}[*] Downloading additional wordlists...${NC}"
wget -O wordlists/common.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt 2>/dev/null || true
wget -O wordlists/subdomains-top1million-5000.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt 2>/dev/null || true

# Make reconxploit executable
chmod +x reconxploit.py

# Create symbolic link
sudo ln -sf $PWD/reconxploit.py /usr/local/bin/reconxploit

echo -e "${GREEN}============================================================================${NC}"
echo -e "${GREEN}[✓] ReconXploit installation completed successfully!${NC}"
echo -e "${GREEN}============================================================================${NC}"
echo ""
echo -e "${CYAN}Usage Examples:${NC}"
echo -e "${YELLOW}  reconxploit -d example.com${NC}"
echo -e "${YELLOW}  reconxploit -d example.com --quick${NC}"
echo -e "${YELLOW}  reconxploit --check-tools${NC}"
echo ""
echo -e "${CYAN}Configuration:${NC}"
echo -e "${YELLOW}  - Please restart your terminal or run: source ~/.bashrc${NC}"
echo -e "${YELLOW}  - Configure API keys for better results:${NC}"
echo -e "${YELLOW}    • Subfinder: ~/.config/subfinder/provider-config.yaml${NC}"
echo -e "${YELLOW}    • Amass: ~/.config/amass/config.ini${NC}"
echo ""
echo -e "${RED}[Mr. Robot]: \"Control is an illusion.\"${NC}"
echo -e "${GREEN}============================================================================${NC}"
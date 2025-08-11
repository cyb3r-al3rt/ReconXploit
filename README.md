# ReconXploit - Advanced Reconnaissance Automation Tool

```
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
```

**Product of kernelpanic** | **Mr. Robot Themed** | **"Control is an illusion."**

## 🎯 Overview

ReconXploit is a comprehensive reconnaissance automation tool designed for bug hunters, penetration testers, and security researchers. Featuring a Mr. Robot theme with dynamic banners and quotes, this tool integrates multiple reconnaissance techniques and tools into a single, powerful platform.

## ✨ Features

### 🔍 Subdomain Enumeration
- **Amass** - OWASP's leading subdomain discovery tool
- **Subfinder** - Fast passive subdomain discovery
- **Sublist3r** - Python-based subdomain enumerator
- **Assetfinder** - Find domains and subdomains
- **Findomain** - Fast subdomain enumerator
- **Certificate Transparency** - crt.sh integration
- **DNS Bruteforcing** - Wordlist-based discovery

### 🌐 URL Discovery
- **Waybackurls** - Historical URL discovery via Wayback Machine
- **GAU (GetAllUrls)** - Fetch known URLs from various sources
- **Katana** - Next-generation crawling and spidering
- **Gospider** - Fast web spider written in Go
- **Common Path Discovery** - Check for common endpoints

### 🔗 Endpoint Discovery
- **JavaScript Analysis** - Extract endpoints from JS files
- **API Endpoint Detection** - Identify REST/GraphQL APIs
- **GF Pattern Matching** - Use regex patterns for endpoint discovery
- **Parameter Discovery** - Find hidden parameters

### ☁️ Cloud Service Enumeration
- **AWS S3 Buckets** - Discover and test S3 bucket permissions
- **Azure Blob Storage** - Find Azure storage accounts
- **Google Cloud Storage** - Enumerate GCP buckets
- **CDN Detection** - Identify CloudFront, Cloudflare, Fastly
- **Cloud Misconfigurations** - Detect common cloud security issues

### 🎨 Mr. Robot Theme
- **Dynamic Banners** - Rotating ASCII art banners
- **Random Quotes** - Authentic Mr. Robot quotes
- **Color-coded Output** - Beautiful terminal interface
- **Hacker Aesthetic** - Immersive experience

## 📋 Requirements

- **Operating System**: Kali Linux (Optimized) / Ubuntu / Debian
- **Python**: 3.8+
- **Go**: 1.19+ (for Go-based tools)
- **Git**: For cloning repositories
- **Curl/Wget**: For downloading tools

## 🚀 Installation

### Quick Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/kernelpanic/reconxploit.git
cd reconxploit

# Make installation script executable
chmod +x install.sh

# Run the installation script
./install.sh
```

### Manual Installation

#### 1. Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install basic dependencies
sudo apt install -y curl wget git python3 python3-pip golang-go npm nodejs build-essential
```

#### 2. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

#### 3. Install Go Tools

```bash
# Amass
go install -v github.com/owasp-amass/amass/v4/cmd/amass@latest

# Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Httpx
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Katana
go install github.com/projectdiscovery/katana/cmd/katana@latest

# GAU
go install github.com/lc/gau/v2/cmd/gau@latest

# Waybackurls
go install github.com/tomnomnom/waybackurls@latest

# Assetfinder
go install github.com/tomnomnom/assetfinder@latest

# GF
go install github.com/tomnomnom/gf@latest

# FFUF
go install github.com/ffuf/ffuf/v2@latest

# Gospider
go install github.com/jaeles-project/gospider@latest
```

## 📖 Usage

### Basic Usage

```bash
# Basic reconnaissance
reconxploit -d example.com

# Quick scan (subdomains only)
reconxploit -d example.com --quick

# Custom output directory
reconxploit -d example.com -o /custom/output

# Check tool availability
reconxploit --check-tools
```

### Command Line Options

```
  -d, --domain          Target domain for reconnaissance
  -o, --output          Custom output directory (default: results)
  --quick               Quick scan (subdomains only)
  --check-tools         Check tool availability and exit
  -v, --verbose         Verbose output
  -h, --help            Show help message
```

## 📁 Directory Structure

```
reconxploit/
├── reconxploit.py          # Main tool
├── install.sh              # Installation script
├── requirements.txt        # Python dependencies
├── setup.py               # Setup configuration
├── src/                   # Source modules
│   ├── __init__.py
│   ├── subdomain_enum.py  # Subdomain enumeration
│   └── url_discovery.py   # URL discovery
├── utils/                 # Utility modules
│   ├── __init__.py
│   └── cloud_enum.py      # Cloud enumeration
├── wordlists/             # Wordlists directory
└── results/               # Output directory
```

## 🔧 Configuration

### API Keys Setup

For better results, configure API keys for various services:

#### Subfinder
```bash
mkdir -p ~/.config/subfinder
cat > ~/.config/subfinder/provider-config.yaml << 'EOF'
binaryedge:
  - "YOUR_BINARYEDGE_API_KEY"
censys:
  - "YOUR_CENSYS_API_ID:YOUR_CENSYS_SECRET"
chaos:
  - "YOUR_CHAOS_API_KEY"
shodan:
  - "YOUR_SHODAN_API_KEY"
virustotal:
  - "YOUR_VIRUSTOTAL_API_KEY"
EOF
```

## 📊 Output Format

ReconXploit generates comprehensive reports in multiple formats:

### Directory Structure
```
results/example.com_20240115_143022/
├── subdomains/
│   ├── all_subdomains.txt
│   └── alive_subdomains.txt
├── urls/
│   └── all_urls.txt
├── endpoints/
├── javascript/
├── api/
├── cloud/
└── reports/
    ├── final_report.json
    └── summary.txt
```

## 🛡️ Security Features

- **Rate Limiting** - Respects target server resources
- **Timeout Management** - Prevents hanging requests
- **Error Handling** - Graceful failure handling

## 🔍 Example Workflow

```bash
# Step 1: Check tools
reconxploit --check-tools

# Step 2: Quick reconnaissance
reconxploit -d example.com --quick

# Step 3: Full reconnaissance
reconxploit -d example.com

# Step 4: Review results
cd results/example.com_*
cat reports/summary.txt
```

## 🐛 Troubleshooting

### Common Issues

1. **Tools not found**
   ```bash
   # Ensure PATH is set correctly
   source ~/.bashrc
   which amass subfinder httpx
   ```

2. **Permission errors**
   ```bash
   # Fix permissions
   chmod +x reconxploit.py
   ```

3. **Python module errors**
   ```bash
   # Reinstall dependencies
   pip3 install -r requirements.txt --upgrade
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY**

ReconXploit is designed for:
- Bug bounty programs
- Authorized penetration testing
- Security research with proper authorization

**DO NOT USE FOR:**
- Unauthorized testing
- Malicious activities
- Illegal reconnaissance

Users are responsible for ensuring they have proper authorization before using this tool.

## 🙏 Acknowledgments

- **OWASP Amass** - Amazing subdomain discovery
- **ProjectDiscovery** - Excellent security tools
- **Tom Hudson (tomnomnom)** - Inspiring Go tools
- **SecLists** - Comprehensive wordlists
- **Mr. Robot** - Inspiration and quotes

---

*"The only way to patch a vulnerability is by exposing it first." - Mr. Robot*

# ReconXploit v3.0 Professional Edition

## 🎯 The Professional Reconnaissance Framework

ReconXploit v3.0 Professional Edition is the ultimate reconnaissance automation framework designed for professional penetration testers, bug hunters, and security researchers. Built with Python and integrated with the best reconnaissance tools available.

### 🚀 Key Features

- **🌐 Advanced Subdomain Enumeration** - Multi-source discovery with risk analysis
- **✅ Live Host Detection** - HTTP/HTTPS service identification with security assessment  
- **🔌 Professional Port Scanning** - Comprehensive network service discovery and analysis
- **⚠️ Vulnerability Assessment** - Automated security vulnerability detection with threat intelligence
- **📊 Beautiful HTML Reports** - Professional reports with target+timestamp naming
- **📈 Multi-format Export** - JSON, CSV, and HTML output with advanced analytics
- **🧠 Intelligent Workflow** - Smart execution order for maximum efficiency
- **🌍 Global Installation** - Install once, use anywhere in your system

## 🔧 Installation & Setup

### Prerequisites
- **Operating System**: Linux (Ubuntu/Debian/Kali recommended), macOS
- **Python**: 3.8+ required  
- **Memory**: 2GB+ RAM recommended
- **Storage**: 5GB+ disk space
- **Network**: Internet connection for tool installation

### Quick Installation

```bash
# 1. Extract the package
unzip ReconXploit-v3.0-FINAL-*.zip
cd ReconXploit-v3.0-FINAL

# 2. Run automated setup
chmod +x setup.sh
./setup.sh

# 3. Install globally (optional but recommended)
sudo ./reconxploit

# 4. Test installation
reconxploit --check-tools
```

### Manual Go Tools Installation (Recommended)

```bash
# Install essential Go-based reconnaissance tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/ffuf/ffuf@latest

# Add Go bin to PATH
export PATH=$PATH:$HOME/go/bin
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
```

## 🎯 Usage Examples

### Basic Reconnaissance
```bash
# Standard reconnaissance scan
reconxploit -d example.com

# Multiple domains from file
reconxploit -l domains.txt

# Single IP target
reconxploit --ip 192.168.1.1

# URL target analysis
reconxploit --url https://example.com
```

### Advanced Professional Options
```bash
# Full comprehensive scan (all modules)
reconxploit -d example.com --full

# High-performance scanning
reconxploit -d example.com --threads 100 --timeout 60

# Stealth reconnaissance
reconxploit -d example.com --stealth --delay 2

# Professional vulnerability assessment
reconxploit -d example.com --vulnerability --full
```

### Specialized Workflow Control
```bash
# Only subdomain enumeration
reconxploit -d example.com --only-subdomains

# Skip port scanning
reconxploit -d example.com --skip-port-scan

# Passive reconnaissance only (OSINT)
reconxploit -d example.com --passive

# Focus on specific workflows
reconxploit -d example.com --vulnerability
```

### Output and Reporting Options
```bash
# JSON output with detailed analysis
reconxploit -d example.com --output json

# CSV export for data analysis
reconxploit -d example.com --output csv

# Custom output directory
reconxploit -d example.com --output-dir /tmp/recon_results

# Custom report naming
reconxploit -d example.com --report-name "client_assessment"
```

## 🛠️ Integrated Professional Tools

### Subdomain Enumeration (Unique Functionality)
- **subfinder** - Multi-source passive subdomain discovery with API integrations
- **assetfinder** - Certificate transparency log enumeration  
- **amass** - Advanced DNS enumeration with relationship mapping

### HTTP Service Detection (Unique Functionality)  
- **httpx** - HTTP response analysis with technology detection
- **httprobe** - Simple HTTP/HTTPS service discovery

### Port & Network Scanning (Unique Functionality)
- **nmap** - Comprehensive service detection and OS fingerprinting
- **naabu** - SYN/CONNECT/UDP port scanning with IP verification
- **masscan** - Extremely fast TCP port scanning

### Content & Directory Discovery (Unique Functionality)
- **gobuster** - Multi-mode brute forcing (dir, dns, vhost, s3)
- **dirb** - Recursive directory scanning with mutation testing
- **ffuf** - Parameter fuzzing with advanced filtering

### Vulnerability Assessment (Unique Functionality)
- **nuclei** - Template-based vulnerability detection with community templates
- **nikto** - Comprehensive web vulnerability scanning with plugin system

### System & Utility Tools (Unique Functionality)
- **curl** - HTTP client with extensive protocol support
- **wget** - Recursive web downloading and mirroring
- **jq** - Advanced JSON filtering and transformation

## 📊 Professional Reporting Features

ReconXploit generates beautiful, professional HTML reports with:

### Report Content
- **Executive Summary** - High-level findings overview with risk assessment
- **Security Score** - Comprehensive security assessment (0-100)
- **Threat Analysis** - Professional threat intelligence and risk vectors
- **Detailed Findings** - Complete vulnerability details with remediation guidance  
- **Visual Analytics** - Charts and graphs for easy analysis and presentation
- **Target+Timestamp Naming** - Automatic naming: `target_YYYYMMDD_HHMMSS_report.html`

### Export Formats
- **HTML** - Beautiful interactive reports with professional styling
- **JSON** - Machine-readable data for integration and analysis
- **CSV** - Structured data for spreadsheet analysis and reporting
- **TXT** - Quick summary files for rapid review

## ⚙️ Professional Configuration

Edit `config/config.yaml` for advanced customization:

```yaml
# ReconXploit v3.0 Professional Configuration
framework:
  version: "3.0.0"
  edition: "Professional Edition"

performance:
  threads: 50              # Concurrent threads
  timeout: 30              # Operation timeout (seconds)
  delay: 0                 # Request delay (seconds)  
  rate_limit: 100          # Requests per minute
  max_subdomains: 1000     # Maximum subdomains to process
  max_urls: 500            # Maximum URLs to analyze

tools:
  subdomain_enumeration:
    enabled: true
    tools: ["subfinder", "assetfinder", "amass"]
    priority: ["subfinder", "assetfinder"]

  vulnerability_scanning:
    enabled: true
    tools: ["nuclei", "nikto"]
    priority: ["nuclei"]

output:
  formats: ["html", "json", "csv"]
  directory: "results"
  include_timestamp: true
  generate_summary: true

security:
  safe_mode: true
  respect_robots_txt: true
  max_recursion_depth: 3

reporting:
  include_charts: true
  detailed_analysis: true
  risk_assessment: true
  recommendations: true
```

## 🔍 System Management Commands

```bash
# Check tool installation status
reconxploit --check-tools

# Install missing reconnaissance tools
reconxploit --install-tools  

# Update all installed tools
reconxploit --update-tools

# List all supported tools with unique features
reconxploit --list-tools

# System health check
reconxploit --check-tools --verbose
```

## 🎯 Complete Command Line Reference

### Target Specification
- `-d, --domain` - Target domain for reconnaissance
- `-l, --list` - File containing list of domains  
- `--ip` - Single IP address target
- `--url` - Single URL target
- `--cidr` - CIDR range for network scanning

### Professional Scan Modes
- `--passive` - Passive reconnaissance only (OSINT)
- `--active` - Active reconnaissance (default)
- `--full` - Full comprehensive scan (all modules)
- `--quick` - Quick essential scan (core modules)
- `--stealth` - Stealth reconnaissance (low profile)

### Workflow Control
- `--skip-subdomain` - Skip subdomain enumeration
- `--skip-port-scan` - Skip port scanning  
- `--skip-vulnerability` - Skip vulnerability scanning
- `--only-subdomains` - Only subdomain enumeration
- `--only-ports` - Only port scanning
- `--vulnerability` - Focus on vulnerability assessment

### Output & Reporting  
- `--output` - Format: html, json, csv (default: html)
- `--output-dir` - Custom output directory (default: results)
- `--report-name` - Custom report name prefix

### Performance Tuning
- `--threads` - Number of concurrent threads (default: 50)
- `--timeout` - Operation timeout in seconds (default: 30)
- `--delay` - Request delay in seconds (default: 0)
- `--rate-limit` - Requests per minute limit (default: 100)

### Configuration & Debug
- `--config` - Custom configuration file path
- `--debug` - Enable debug mode with verbose output
- `--verbose, -v` - Increase output verbosity
- `--silent` - Silent mode (errors only)
- `--dry-run` - Test run without actual scanning

## 🚨 Troubleshooting Guide

### Common Installation Issues

**Virtual environment not found:**
```bash
# Re-run setup
chmod +x setup.sh && ./setup.sh
```

**Tools not found:**
```bash  
# Check tool availability
reconxploit --check-tools

# Install missing system tools
sudo apt update && sudo apt install nmap gobuster nikto

# Install Go tools manually
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

**Permission errors:**
```bash
# Fix permissions
chmod +x reconxploit setup.sh
sudo chown -R $USER:$USER .
```

**Global installation issues:**
```bash
# Install globally with proper permissions
sudo ./reconxploit
```

**HTML reports not visible:**
```bash
# Check output directory permissions
ls -la results/
chmod 755 results/
```

### Performance Optimization

**For large targets:**
```bash
# Increase threads and timeout
reconxploit -d example.com --threads 100 --timeout 60
```

**For network-constrained environments:**
```bash  
# Reduce rate and add delay
reconxploit -d example.com --rate-limit 50 --delay 1 --threads 20
```

**For stealth operations:**
```bash
# Low-profile reconnaissance  
reconxploit -d example.com --stealth --passive --delay 3
```

## 🎓 Professional Use Cases & Examples

### Bug Hunting Workflow
```bash
# 1. Initial reconnaissance
reconxploit -d target.com --passive --only-subdomains

# 2. Comprehensive analysis
reconxploit -d target.com --full --threads 75

# 3. Vulnerability focus  
reconxploit -d target.com --vulnerability --output json
```

### Enterprise Security Assessment  
```bash
# Multiple targets with comprehensive analysis
reconxploit -l enterprise_domains.txt --full --output-dir enterprise_report --threads 100
```

### Red Team Operations
```bash
# Stealth reconnaissance for red team exercises
reconxploit -d target.com --stealth --passive --delay 2 --silent
```

### Continuous Security Monitoring
```bash
# Automated daily scans with timestamped reports
reconxploit -d company.com --quick --output json --output-dir daily_scans
```

## 📈 Performance & Scalability

### Recommended System Specifications

**Basic Usage:**
- CPU: 2+ cores
- RAM: 4GB+  
- Network: Standard broadband

**Professional Usage:**
- CPU: 4+ cores  
- RAM: 8GB+
- Network: High-speed broadband
- SSD storage recommended

**Enterprise Usage:**
- CPU: 8+ cores
- RAM: 16GB+
- Network: Dedicated/enterprise connection
- NVMe SSD storage

### Performance Tips

1. **Optimize thread count** - Start with 50, adjust based on system capability
2. **Use appropriate scan modes** - `--quick` for fast results, `--full` for comprehensive analysis
3. **Leverage rate limiting** - Use `--rate-limit` to respect target resources
4. **Enable stealth mode** - Use `--stealth` for low-profile operations
5. **Utilize specific workflows** - Use `--only-subdomains` or `--vulnerability` for targeted scans

## 🔒 Ethical Usage & Legal Compliance

### ⚠️ IMPORTANT DISCLAIMER

**ONLY use ReconXploit on systems you own or have explicit written permission to test.**

### Ethical Guidelines

- ✅ Always obtain proper authorization before testing
- ✅ Respect rate limits and target resources  
- ✅ Follow responsible disclosure practices
- ✅ Comply with local laws and regulations
- ✅ Document and report findings responsibly
- ❌ Never use for malicious purposes
- ❌ Never scan without permission
- ❌ Never overwhelm target systems

### Legal Compliance

- **Penetration Testing**: Only on authorized systems
- **Bug Bounty Programs**: Follow program rules and scope
- **Educational Use**: For learning and training purposes
- **Research**: Academic and security research with proper authorization

## 🏢 Professional Support & Services

### Product Information
- **Version**: 3.0.0 Professional Edition
- **Author**: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)
- **Organization**: Kernelpanic
- **Website**: infosbios.tech
- **License**: Educational and Professional Use

### Support Channels
- **Documentation**: Comprehensive user manual included
- **Issues**: GitHub repository for bug reports and feature requests
- **Community**: Professional security community discussions
- **Training**: Professional reconnaissance training available

## 🤝 Contributing & Development

### Contributing Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Test thoroughly with multiple targets
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)  
6. Open a Pull Request

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/your-repo/reconxploit.git
cd reconxploit
python -m venv dev_env
source dev_env/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

## 📞 Contact & Support

- **Professional Services**: Available through infosbios.tech
- **Training**: Professional reconnaissance training programs
- **Custom Development**: Enterprise customization available
- **Security Consulting**: Professional security assessment services

---

## 🎯 Final Note

**ReconXploit v3.0 Professional Edition** represents the pinnacle of automated reconnaissance frameworks. Designed by security professionals for security professionals, it combines the power of multiple reconnaissance tools with intelligent automation and beautiful reporting.

### Professional Motto
**💎 "Control is an illusion, but reconnaissance is power."**

*Discover the hidden. Uncover the truth. Master the art of professional reconnaissance.*

**ReconXploit v3.0 Professional Edition - The Security Professional's Choice for Comprehensive Reconnaissance**

---

*Copyright © 2024 Kernelpanic under infosbios.tech. All rights reserved.*
*Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)*
*Educational and Professional Use License*

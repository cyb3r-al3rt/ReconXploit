# ReconXploit v3.0 - Advanced Reconnaissance Framework

<div align="center">

```
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
```

**Advanced Reconnaissance Automation Framework**

*"Control is an illusion, but reconnaissance is power."*

**Product of Kernelpanic under [infosbios.tech](https://infosbios.tech)**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Version](https://img.shields.io/badge/version-3.0.0-red.svg)](https://github.com/your-repo/ReconXploit)

</div>

## 🎯 Overview

ReconXploit v3.0 is a comprehensive reconnaissance automation framework designed for security professionals, penetration testers, and bug hunters. Built with a Mr. Robot theme and powered by 100+ integrated tools, it provides end-to-end reconnaissance capabilities from subdomain discovery to vulnerability identification.

### ✨ Key Features

- **🚀 Intelligent Workflow Engine**: Automated multi-stage reconnaissance
- **🔧 100+ Integrated Tools**: Seamless integration with popular security tools
- **📊 Advanced Reporting**: Beautiful HTML dashboards with dark theme
- **⚡ High Performance**: Concurrent processing with configurable threading
- **🎭 Mr. Robot Theme**: FSociety-inspired interface and quotes
- **🌐 Global Access**: Both local (`./reconxploit`) and global (`reconxploit`) commands
- **🔒 Security-First**: Built-in rate limiting and safety mechanisms
- **📋 Multiple Formats**: HTML, JSON, CSV, PDF report generation

## 🛠️ Installation

### Quick Installation

```bash
# Download and extract ReconXploit
unzip ReconXploit-v3.0-COMPLETE-FIXED-*.zip
cd ReconXploit-v3.0

# Run automated setup
chmod +x setup.sh
./setup.sh

# Install missing tools
sudo apt install -y libpcap-dev
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install github.com/hahwul/dalfox/v2@latest
wget https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster-linux-x86_64.tar.gz
tar -xzf feroxbuster-linux-x86_64.tar.gz && sudo mv feroxbuster /usr/local/bin/
```

### Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

1. **System Requirements**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git curl wget nmap

   # Install Go (for Go-based tools)
   wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
   sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
   echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Python Environment**
   ```bash
   cd ReconXploit-v3.0
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Tool Installation**
   ```bash
   # Go tools
   go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
   go install github.com/projectdiscovery/httpx/cmd/httpx@latest
   go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

   # System tools
   sudo apt install nmap masscan gobuster dirb nikto sqlmap
   ```

</details>

## 🚀 Quick Start

### Basic Usage

```bash
# Check tool installation
./reconxploit --check-tools

# Basic reconnaissance
./reconxploit -d example.com

# Passive reconnaissance (no active scanning)
./reconxploit -d example.com --passive

# Full comprehensive scan
./reconxploit -d example.com --full

# Multiple domains
./reconxploit -l domains.txt --threads 100
```

### Advanced Usage

```bash
# Custom output format
./reconxploit -d example.com --output json

# Skip specific stages
./reconxploit -d example.com --skip-port-scan --skip-vulnerability

# Custom configuration
./reconxploit -d example.com --config custom-config.yaml

# Debug mode
./reconxploit -d example.com --debug --verbose
```

## 📊 Reconnaissance Stages

ReconXploit follows an intelligent multi-stage workflow:

1. **🌐 Subdomain Enumeration**
   - Passive DNS discovery
   - Certificate transparency logs
   - Search engine reconnaissance
   - Brute force discovery

2. **✅ Live Host Detection**
   - HTTP/HTTPS probing
   - Response code analysis
   - Technology detection
   - SSL certificate analysis

3. **🔌 Port Scanning**
   - TCP port discovery
   - Service fingerprinting
   - Banner grabbing
   - Custom port ranges

4. **🔍 Content Discovery**
   - Directory enumeration
   - File discovery
   - API endpoint detection
   - Hidden resource identification

5. **🔑 Parameter Discovery**
   - URL parameter mining
   - Form analysis
   - API parameter discovery
   - Reflection testing

6. **⚠️ Vulnerability Scanning**
   - Template-based scanning
   - CVE identification
   - Security misconfiguration detection
   - Custom vulnerability checks

## 🛡️ Integrated Tools

### Go-based Tools
- **subfinder** - Subdomain discovery
- **httpx** - HTTP probing and analysis
- **nuclei** - Vulnerability scanner with templates
- **naabu** - Fast port scanner
- **katana** - Web crawling framework
- **dalfox** - XSS parameter analysis

### System Tools
- **nmap** - Network discovery and security auditing
- **masscan** - Internet-scale port scanner
- **gobuster** - Directory/file/DNS brute-forcer
- **nikto** - Web server scanner

### Python Tools
- **sublist3r** - Subdomain enumeration
- **dirsearch** - Web path discovery
- **arjun** - HTTP parameter discovery

### Rust Tools
- **feroxbuster** - Fast directory/file brute forcer

## 📋 Configuration

### Main Configuration (`config/config.yaml`)

```yaml
performance:
  threads: 50
  timeout: 30
  rate_limit: 100

tools:
  subdomain_enumeration:
    enabled: true
    tools: ["subfinder", "assetfinder"]
    timeout: 300

  vulnerability_scanning:
    enabled: true
    tools: ["nuclei"]
    severity: ["critical", "high", "medium"]
```

### API Keys (`config/api_keys.yaml`)

```yaml
# Optional but recommended for enhanced functionality
shodan: "your_shodan_api_key"
censys_id: "your_censys_id"
virustotal: "your_virustotal_key"
github: "your_github_token"
```

## 📊 Report Formats

### HTML Dashboard (Default)
- Beautiful dark-themed interface
- Interactive charts and metrics
- Vulnerability severity breakdown
- Risk assessment scoring

### JSON Export
- Machine-readable format
- Complete raw data
- API integration friendly

### CSV Summary
- Spreadsheet compatible
- Metrics overview
- Quick analysis

## 🔧 Tool Management

```bash
# Check all tool availability
reconxploit --check-tools

# Install missing tools automatically
reconxploit --install-tools

# Update existing tools
reconxploit --update-tools

# Setup API keys interactively
reconxploit --setup-keys
```

## 🎯 Use Cases

### Bug Bounty Hunting
```bash
# Comprehensive reconnaissance for bug bounty
reconxploit -d target.com --full --output html
reconxploit -l scope.txt --passive --threads 100
```

### Penetration Testing
```bash
# Active reconnaissance with all tools
reconxploit -d client.com --full --debug
```

### Security Assessment
```bash
# Focus on vulnerabilities
reconxploit -d company.com --skip-content --use-nuclei
```

### Red Team Operations
```bash
# Stealthy passive reconnaissance
reconxploit -d target.org --passive --delay 2 --silent
```

## 📈 Performance Optimization

### High-Performance Scanning
```bash
# Maximum performance configuration
reconxploit -d target.com --threads 200 --timeout 15
```

### Resource-Constrained Environment
```bash
# Low resource usage
reconxploit -d target.com --threads 10 --timeout 60 --quick
```

## 🔐 Security Considerations

- **Rate Limiting**: Built-in rate limiting to avoid overwhelming targets
- **Stealth Mode**: Configurable delays and user agents
- **Proxy Support**: HTTP/HTTPS/SOCKS proxy integration
- **SSL Verification**: Configurable SSL certificate verification

## 🛠️ Development

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Custom Tool Integration
```python
# Add custom tool to workflow
class CustomTool:
    async def execute(self, target, config):
        # Implementation here
        return results
```

## 🆘 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'core'`
```bash
# Fix: Ensure __init__.py files exist and PYTHONPATH is set
touch core/__init__.py tools/__init__.py
export PYTHONPATH="$(pwd):$PYTHONPATH"
```

**Issue**: `command not found: reconxploit`
```bash
# Fix: Install global launcher
sudo cp scripts/global_launcher.sh /usr/local/bin/reconxploit
sudo chmod +x /usr/local/bin/reconxploit
```

**Issue**: Tools not found
```bash
# Fix: Check and install missing tools
./reconxploit --check-tools
# Follow installation suggestions
```

### Debug Mode
```bash
# Run with full debugging
./reconxploit -d target.com --debug --verbose
```

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Tool Integration](docs/TOOLS.md)
- [API Reference](docs/API.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Author**: Muhammad Ismaeel Shareef S S (cyb3r-ssrf)
- **Organization**: Kernelpanic
- **Website**: [infosbios.tech](https://infosbios.tech)

Special thanks to the creators of all integrated tools and the security community.

## ⚠️ Disclaimer

ReconXploit is designed for authorized security testing only. Users are responsible for complying with applicable laws and regulations. The authors are not responsible for any misuse or damage caused by this tool.

## 🌟 Support

- 📧 Email: support@infosbios.tech
- 🌐 Website: [infosbios.tech](https://infosbios.tech)
- 📱 GitHub Issues: [Report Bug](https://github.com/your-repo/ReconXploit/issues)

---

<div align="center">

**"Control is an illusion, but reconnaissance is power."**

*ReconXploit v3.0 - The Future of Automated Reconnaissance*

</div>

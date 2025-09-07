# ReconXploit v3.0

<div align="center">

```
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ──╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
```

**Advanced Reconnaissance Automation Framework**  
*Product of Kernelpanic under infosbios.tech*

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/cyb3r-al3rt/ReconXploit)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux-red.svg)](https://www.kali.org/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](docker/)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://python.org/)

*"Control is an illusion, but reconnaissance is power."*

</div>

## 🎯 Overview

ReconXploit v3.0 is the most advanced reconnaissance automation framework ever built, integrating **100+ cutting-edge security tools** with intelligent workflow management and AI-powered result correlation. Inspired by the Mr. Robot series, it revolutionizes how security professionals conduct reconnaissance with adaptive tool chaining, real-time data processing, and professional-grade reporting.

### 🚀 Key Features

- **🔥 100+ Tool Integration**: Seamlessly integrates the most powerful reconnaissance tools
- **🧠 Intelligent Workflow Engine**: Adaptive decision trees and parallel processing
- **🎭 Mr. Robot Themed Interface**: Dynamic banners and quotes from the series
- **⚡ Parallel Processing**: Multi-threaded execution with intelligent resource management
- **📊 Advanced Reporting**: HTML dashboards, PDF reports, JSON/CSV exports
- **🐳 Docker Support**: Containerized deployment for consistency and portability
- **🔐 API Integration**: Shodan, Censys, SecurityTrails, VirusTotal, and more
- **📱 Real-time Monitoring**: Live progress tracking and webhook notifications
- **🎨 Professional Reports**: Client-ready documents with custom branding

## 🛠️ Integrated Tools

### Subdomain Discovery (20+ tools)
- **Passive**: Amass, Subfinder, Assetfinder, Sublist3r, Findomain, Chaos, DNScan, Crobat
- **Active**: DNSx, MassDNS, Shuffledns, AltDNS, DNSGen, Gotator

### Web Discovery & Crawling (18+ tools)  
- **Crawlers**: Katana, Hakrawler, Gospider, GAU, Waybackurls, Galer
- **Content Discovery**: Gobuster, FFuf, Dirsearch, Feroxbuster, Dirb, Wfuzz

### Vulnerability Scanning (25+ tools)
- **Comprehensive**: Nuclei (5000+ templates), Jaeles, Nikto, Wapiti, Skipfish
- **Specialized**: SQLmap, XSStrike, Dalfox, Subjack, Takeover, Cloud_enum

### Network Analysis (15+ tools)
- **Port Scanning**: Nmap, Masscan, Naabu, Rustscan, Zmap
- **Service Detection**: Httpx, Httprobe, Banner grabbing, Technology detection

### Intelligence Gathering (12+ tools)
- **OSINT**: Shodan, Censys, SecurityTrails, TheHarvester, Maltego, Recon-ng
- **Social Media**: Sherlock, WhatsMyName, Social-analyzer

### Parameter & API Discovery (10+ tools)
- **Parameter Discovery**: ParamSpider, Arjun, X8, GF patterns, Unfurl
- **API Testing**: KiteRunner, OpenAPI Scanner, API-Guesser

## 📦 Installation

### Prerequisites
- **Operating System**: Kali Linux (recommended), Ubuntu 20.04+, Debian 11+
- **Python**: 3.8 or higher
- **Go**: 1.19 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 10GB free space

### Quick Installation (Kali Linux)

```bash
# Clone the repository
git clone https://github.com/cyb3r-al3rt/ReconXploit.git
cd ReconXploit

# Run the automated installer
chmod +x scripts/install.sh
./scripts/install.sh

# Setup API keys (optional but recommended)
python3 scripts/setup_api_keys.py

# Verify installation
./reconxploit --check-tools
```

### Docker Installation

```bash
# Using Docker Compose (recommended)
docker-compose up -d reconxploit

# Or build and run manually
docker build -t cyb3r-al3rt/reconxploit:3.0.0 .
docker run -v $(pwd)/results:/opt/reconxploit/results cyb3r-al3rt/reconxploit:3.0.0 -d example.com
```

## 🚀 Quick Start

### Basic Usage

```bash
# Basic reconnaissance
./reconxploit -d example.com

# Full comprehensive scan
./reconxploit -d example.com --full

# Passive reconnaissance only
./reconxploit -d example.com --passive

# Custom output format
./reconxploit -d example.com --output json

# Multiple domains from file
./reconxploit -l domains.txt

# Custom threads and timeout
./reconxploit -d example.com --threads 100 --timeout 60
```

### Advanced Usage

```bash
# Skip specific stages
./reconxploit -d example.com --skip-port-scan --skip-vulnerability

# Custom configuration
./reconxploit -d example.com --config custom_config.yaml

# Generate only PDF reports
./reconxploit -d example.com --output pdf

# Debug mode with verbose output
./reconxploit -d example.com --debug --verbose
```

## ⚙️ Configuration

### API Keys Setup

ReconXploit supports integration with multiple external services:

```yaml
# config/api_keys.yaml
shodan:
  api_key: "YOUR_SHODAN_API_KEY"

censys:
  api_id: "YOUR_CENSYS_API_ID"
  api_secret: "YOUR_CENSYS_API_SECRET"

securitytrails:
  api_key: "YOUR_SECURITYTRAILS_API_KEY"

virustotal:
  api_key: "YOUR_VIRUSTOTAL_API_KEY"

github:
  token: "YOUR_GITHUB_TOKEN"
```

Run the interactive setup:
```bash
python3 scripts/setup_api_keys.py
```

## 📊 Output Formats

### JSON Output
```json
{
  "target": "example.com",
  "scan_time": 1245.67,
  "subdomains": ["sub1.example.com", "sub2.example.com"],
  "live_hosts": ["https://example.com", "https://sub1.example.com"],
  "vulnerabilities": [
    {
      "severity": "high",
      "title": "SQL Injection",
      "url": "https://example.com/login",
      "tool": "nuclei"
    }
  ]
}
```

### HTML Dashboard
Interactive dashboard with:
- Executive summary with risk metrics
- Interactive charts and timelines
- Detailed findings with evidence
- Tool execution logs
- Exportable results

### PDF Reports
Professional client-ready reports with:
- Executive summary
- Technical findings
- Risk assessment matrix
- Remediation recommendations
- Custom branding

## 🔧 Workflow Stages

ReconXploit follows an intelligent 12-stage workflow:

1. **🚀 Initialization** - Environment setup and target validation
2. **🌐 Subdomain Enumeration** - Multi-tool subdomain discovery
3. **💻 Live Host Detection** - HTTP probing and service detection
4. **🔍 Technology Detection** - Stack fingerprinting and version detection
5. **🚪 Port Scanning** - Network service enumeration
6. **🕷️ Web Crawling** - Site mapping and URL discovery
7. **📡 URL Discovery** - Historical and archived URL collection
8. **📂 Content Discovery** - Directory and file enumeration
9. **🔍 Parameter Discovery** - GET/POST parameter identification
10. **🛡️ Vulnerability Scanning** - Comprehensive security testing
11. **🕵️ OSINT Gathering** - Open source intelligence collection
12. **📋 Report Generation** - Multi-format report creation

## 🐳 Docker Deployment

### Single Container
```bash
docker run -d \
  --name reconxploit \
  -v $(pwd)/results:/opt/reconxploit/results \
  -v $(pwd)/config:/opt/reconxploit/config \
  kernelpanic/reconxploit:3.0.0 \
  -d example.com --full
```

### Docker Compose
```yaml
version: '3.8'
services:
  reconxploit:
    image: kernelpanic/reconxploit:3.0.0
    volumes:
      - ./results:/opt/reconxploit/results
      - ./config:/opt/reconxploit/config
    environment:
      - RECONXPLOIT_HOME=/opt/reconxploit
    command: ["-d", "example.com"]
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Tools Integrated
Thanks to the amazing authors of all integrated tools:
- ProjectDiscovery team (Subfinder, Httpx, Nuclei, Katana, Naabu, DNSx)
- Tom Hudson (Assetfinder, GF, Waybackurls)
- OWASP team (Amass)
- And many more open source contributors

### Inspiration
- **Mr. Robot Series** - For the incredible cybersecurity narrative and aesthetic
- **fsociety** - For inspiring the hacker mindset
- **Security Community** - For continuous innovation in reconnaissance

## 📞 Contact

- **Email**: cyb3r-ssrf@proton.me
- **LinkedIn**: https://www.linkedin.com/in/cyb3r-ssrf
- **Website**: https://infosbios.tech

---

<div align="center">

**ReconXploit v3.0** - *Where reconnaissance meets artificial intelligence*

*Product of Kernelpanic under infosbios.tech*

*"In reconnaissance we trust, in automation we excel."*

**⭐ Star this repository if ReconXploit helped you find vulnerabilities! ⭐**

</div>

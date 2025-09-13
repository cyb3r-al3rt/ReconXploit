# ReconXploit Framework

Complete Reconnaissance Framework with 150+ Integrated Tools

## Quick Start

```bash
# Extract and install
unzip ReconXploit-Framework-*.zip
cd ReconXploit-Framework/

# Install globally  
sudo bash install_global.sh

# Use from anywhere
reconxploit -t example.com --comprehensive
```

## Features

### 150+ Professional Tools
- Subdomain Enumeration (15 tools)
- Port Scanning (12 tools) 
- Web Discovery (20 tools)
- Directory Bruteforce (15 tools)
- Vulnerability Scanning (25 tools)
- OSINT Gathering (30 tools)
- Cloud Security (15 tools)
- Network Analysis (7 tools)
- Mobile Testing (6 tools)
- Wireless Testing (5 tools)
- Crypto Tools (5 tools)

### Advanced Capabilities
- Multi-phase reconnaissance workflow
- Parallel execution optimization
- Professional output formats
- Enterprise-ready architecture

## Usage

```bash
# Framework info
reconxploit --framework-info

# List all tools
reconxploit --list-tools

# Basic scan
reconxploit -t example.com

# Advanced scan
reconxploit -t example.com --advanced

# Full scan (all tools)
reconxploit -t example.com --comprehensive

# Multiple targets
reconxploit --target-list targets.txt --comprehensive

# Save results
reconxploit -t example.com -o results.json --format json
```

## Global Access

After installation:
- Works from any directory
- No more `python3 reconxploit.py`
- Just `reconxploit` command
- Self-contained deployment

## Management

```bash
# Update
sudo bash install_global.sh

# Uninstall
sudo reconxploit-uninstall
```

## Author

**Author:** cyb3r-ssrf (Muhammad Ismaeel Shareef S S)  
**Organization:** Kernelpanic under infosbios.tech  
**Version:** 1.0  
**License:** MIT

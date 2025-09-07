# ReconXploit v3.0 - Advanced Reconnaissance Framework

## 🎯 Overview

ReconXploit v3.0 is a comprehensive reconnaissance automation framework designed for security professionals, penetration testers, and bug hunters.

## 🚀 Quick Start

```bash
# Extract and setup
cd ReconXploit-v3.0
chmod +x setup.sh
./setup.sh

# Test installation
./reconxploit --check-tools

# Run reconnaissance
./reconxploit -d example.com
./reconxploit -d example.com --passive
./reconxploit -d example.com --full
```

## 📊 Features

- ✅ Subdomain Enumeration
- ✅ Live Host Detection  
- ✅ Port Scanning
- ✅ Vulnerability Scanning
- ✅ Beautiful HTML Reports
- ✅ JSON/CSV Export
- ✅ Mr. Robot Theme

## 🛠️ Tool Integration

- **subfinder** - Subdomain discovery
- **httpx** - HTTP probing
- **nmap** - Port scanning
- **nuclei** - Vulnerability scanning
- **feroxbuster** - Directory bruteforcing

## 📋 Usage

```bash
# Basic commands
./reconxploit --help
./reconxploit --check-tools
./reconxploit -d target.com
./reconxploit -d target.com --passive
./reconxploit -d target.com --output json

# Advanced usage
./reconxploit -d target.com --threads 100 --timeout 60
./reconxploit -d target.com --skip-port-scan
./reconxploit -d target.com --debug --verbose
```

## 🎯 Product Information

- **Version**: 3.0.0
- **Author**: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)
- **Organization**: Kernelpanic
- **Website**: infosbios.tech

*"Control is an illusion, but reconnaissance is power."*

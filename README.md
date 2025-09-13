# ReconXploit Framework v1.0

**🎯 Advanced Reconnaissance Framework with 150+ Integrated Professional Tools**

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/cyb3r-al3rt/ReconXploit)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://linux.org)
[![Tools](https://img.shields.io/badge/tools-150+-red.svg)](https://github.com/cyb3r-al3rt/ReconXploit)

---

## 🚀 **Quick Start**

```bash
# One-command installation
git clone https://github.com/cyb3r-al3rt/ReconXploit.git
cd ReconXploit
sudo bash install_global.sh

# Use from anywhere
reconxploit --framework-info
reconxploit -t example.com --comprehensive
```

---

## 🎯 **Overview**

ReconXploit Framework is the most comprehensive reconnaissance framework designed for:
- 🔴 **Penetration Testers** - Complete attack surface mapping
- 🏆 **Bug Bounty Hunters** - Automated vulnerability discovery  
- 🛡️ **Security Professionals** - Infrastructure assessment
- 🎓 **CTF Players** - Rapid reconnaissance deployment
- 🔵 **Blue Teams** - Attack surface monitoring

**🎪 What makes ReconXploit revolutionary:**
- **150+ Professional Tools** integrated into one framework
- **Global Binary Access** - works from any directory
- **Intelligent Orchestration** - multi-phase workflow
- **Built-in Plugin System** - extensible architecture
- **Enterprise Ready** - production-grade deployment

---

## ✨ **Key Features**

### 🛠️ **150+ Professional Tools by Category**

| **Category** | **Count** | **Key Tools** |
|--------------|-----------|---------------|
| **Subdomain Enumeration** | 15 | subfinder, amass, assetfinder, findomain |
| **Port Scanning** | 12 | nmap, masscan, naabu, rustscan |
| **Web Discovery** | 20 | httpx, katana, waybackurls, gau |
| **Directory Bruteforce** | 15 | ffuf, gobuster, feroxbuster, dirb |
| **Vulnerability Scanning** | 25 | nuclei, nikto, sqlmap, xssstrike |
| **OSINT Gathering** | 30 | theHarvester, shodan, sherlock |
| **Cloud Security** | 15 | cloudenum, S3Scanner, prowler |
| **Network Analysis** | 7 | wireshark, tcpdump, netstat |
| **Mobile Security** | 6 | mobsf, drozer, apktool |
| **Wireless Security** | 5 | aircrack-ng, kismet, wifite |
| **Cryptography** | 5 | hashcat, john, hydra |

### 🔌 **12+ Built-in Plugins**
1. **Subdomain Monitor** - Track subdomain changes over time
2. **Vulnerability Reporter** - Generate professional reports  
3. **Screenshot Automator** - Automated visual reconnaissance
4. **Port Analyzer** - Compare scan results across time
5. **Notification Sender** - Slack/Discord/Email integration
6. **Wordlist Generator** - Custom target-specific wordlists
7. **CIDR Expander** - Network range expansion
8. **DNS Resolver** - Mass domain resolution
9. **HTTP Prober** - Live service detection
10. **Certificate Analyzer** - SSL certificate intelligence
11. **GitHub Dorker** - Source code reconnaissance  
12. **Cloud Bucket Finder** - Misconfigured storage detection

### 📚 **25+ Comprehensive Wordlists**
- **Directory/File Discovery**: common.txt, directory-list-2.3-*.txt, raft-large-*.txt
- **Subdomain Enumeration**: subdomains-top1million-*.txt, fierce-hostlist.txt
- **Parameter Discovery**: burp-parameter-names.txt, common-parameters.txt
- **Password Testing**: darkweb2017-*.txt, common-passwords.txt
- **Fuzzing Payloads**: XSS, SQLi, Command Injection, LFI
- **API Discovery**: api-endpoints.txt, swagger.txt
- **Custom Collections**: Target-specific generated wordlists

---

## 🚀 **Installation**

### **Recommended Installation (Complete Setup)**
```bash
# Clone repository
git clone https://github.com/cyb3r-al3rt/ReconXploit.git
cd ReconXploit

# Complete installation with all tools
sudo bash install_global.sh

# Verify installation
reconxploit --framework-info
```

### **Alternative Installation (Bundle)**
```bash
# Extract downloaded bundle
unzip ReconXploit-Framework-Final-*.zip
cd ReconXploit-Framework/

# Install with all dependencies
sudo bash install_global.sh
```

### **Manual Setup**
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run setup script  
python3 setup.py

# Install tools manually
reconxploit --install-tools
```

---

## 💻 **Usage Examples**

### **🔍 Basic Reconnaissance**
```bash
# Quick reconnaissance
reconxploit -t example.com

# Basic scan with output
reconxploit -t example.com -o results.json

# Multiple targets
echo -e "example.com\ntest.com" > targets.txt
reconxploit --target-list targets.txt
```

### **🎯 Advanced Reconnaissance**
```bash
# Advanced multi-phase scan
reconxploit -t example.com --advanced

# Comprehensive scan (all 150+ tools)
reconxploit -t example.com --comprehensive

# Custom output format
reconxploit -t example.com --advanced --format text -o report.txt
```

### **⚙️ Framework Management**
```bash
# Show framework information
reconxploit --framework-info

# List all tools by category
reconxploit --list-tools

# Show available plugins
reconxploit --list-plugins

# Update framework and tools
reconxploit --update

# Install missing tools
reconxploit --install-tools

# Download wordlist collection
reconxploit --download-wordlists
```

### **🔧 Advanced Options**
```bash
# Verbose debugging
reconxploit -t example.com --comprehensive -v 3

# Quiet mode (minimal output)
reconxploit -t example.com --advanced --quiet

# Custom verbosity levels
reconxploit -t example.com -v 2  # Detailed output
reconxploit -t example.com -v 0  # Errors only
```

---

## 🎪 **Use Cases & Applications**

### **🔴 Bug Bounty Hunting**
```bash
# Complete attack surface mapping
reconxploit -t bugcrowd-target.com --comprehensive -o bounty-results.json

# Focus on web vulnerabilities
reconxploit -t hackerone-target.com --advanced --format text
```

**Benefits:**
- ✅ **Complete Coverage**: 150+ tools ensure no attack vector is missed
- ✅ **Automated Discovery**: From subdomains to vulnerabilities automatically
- ✅ **Professional Reports**: JSON/Text output for easy analysis
- ✅ **Time Efficiency**: Parallel execution saves hours of manual work

### **🏆 CTF Competitions**
```bash
# Rapid reconnaissance deployment
reconxploit -t ctf-target.local --advanced

# Quick enumeration for time-sensitive challenges  
reconxploit -t 10.0.0.1 --basic -v 3
```

**Advantages:**
- ⚡ **Speed**: One-command reconnaissance
- 🎯 **Comprehensive**: All necessary tools included
- 🔧 **Flexible**: Basic to comprehensive scan options
- 📊 **Clear Output**: Easy to parse results

### **🔵 Red Team Operations**
```bash
# Enterprise infrastructure mapping
reconxploit -t enterprise-target.com --comprehensive --quiet

# Stealth reconnaissance with custom timing
reconxploit --target-list enterprise-ranges.txt --advanced
```

**Features:**
- 🕵️ **OSINT Collection**: 30+ tools for intelligence gathering
- 🗺️ **Infrastructure Mapping**: Complete network and service discovery  
- 🔒 **Stealth Options**: Advanced evasion techniques
- 📈 **Scalability**: Handle large enterprise networks

### **🛡️ Blue Team Defense**
```bash
# External attack surface assessment
reconxploit -t company.com --comprehensive -o external-assessment.json

# Continuous monitoring setup
reconxploit -t company.com --advanced --format text > daily-scan.txt
```

**Applications:**
- 🔍 **Attack Surface Discovery**: Understand your external exposure
- 📋 **Compliance Auditing**: Generate reports for security assessments  
- 📊 **Vulnerability Management**: Proactive security gap identification
- 🔄 **Continuous Monitoring**: Track infrastructure changes

---

## 🌐 **Global Binary Access**

After installation, ReconXploit becomes a true system command:

```bash
# Works from ANY directory
cd /tmp && reconxploit -t example.com
cd /home/user && reconxploit --framework-info  
cd /var/log && reconxploit -t target.com --comprehensive

# No more "python3 reconxploit.py"
# Just "reconxploit" like nmap, curl, or any system tool
```

**🎯 Benefits:**
- ✅ **Convenience**: Access from anywhere on the system
- ✅ **Professional**: Behaves like native system tools
- ✅ **Efficiency**: No directory navigation required
- ✅ **Integration**: Easy to use in scripts and automation

---

## 📊 **Output & Reporting**

### **JSON Output (Default)**
```json
{
  "target": "example.com",
  "scan_type": "comprehensive", 
  "framework_version": "1.0",
  "findings": {
    "subdomains": {
      "count": 45,
      "subdomains": ["api.example.com", "dev.example.com", ...]
    },
    "ports": {
      "count": 12,
      "ports": [80, 443, 8080, ...]
    },
    "vulnerabilities": {
      "count": 3,
      "vulnerabilities": [...]
    }
  },
  "statistics": {
    "tools_executed": 89,
    "findings_discovered": 156,
    "plugins_executed": 8
  },
  "duration_seconds": 1847.3
}
```

### **Text Output**
```
ReconXploit Framework v1.0 - Reconnaissance Report
==================================================
Target: example.com
Scan Type: comprehensive
Duration: 30m 47s
Status: completed

SUBDOMAINS (45):
  - api.example.com
  - dev.example.com
  - staging.example.com
  [...]

PORTS (12):
  - 80/tcp (http)
  - 443/tcp (https)  
  - 8080/tcp (http-alt)
  [...]

VULNERABILITIES (3):
  - [HIGH] SQL Injection in /login.php
  - [MEDIUM] XSS in search parameter
  - [LOW] Information disclosure
```

---

## 🔧 **Advanced Configuration**

### **Environment Variables**
```bash
# Custom directories
export RECONXPLOIT_OUTPUT="/custom/results"
export RECONXPLOIT_WORDLISTS="/custom/wordlists"  
export RECONXPLOIT_PLUGINS="/custom/plugins"

# Performance tuning
export RECONXPLOIT_MAX_CONCURRENT=20
export RECONXPLOIT_TIMEOUT=600
```

### **Configuration File**
```yaml
# ~/.reconxploit/config.yml
framework:
  version: "1.0"
  default_scan_type: "advanced"

performance:
  max_concurrent_tools: 15
  timeout_seconds: 300

output:
  default_format: "json"
  save_results: true
  timestamp_files: true

plugins:
  auto_execute: true
  notification_webhook: "https://hooks.slack.com/..."
```

### **Custom Target Lists**
```bash
# Create comprehensive target list
cat > targets.txt << EOF
# Web applications
example.com
test.com
staging.example.com

# Network ranges  
192.168.1.0/24
10.0.0.0/16

# Specific IPs
203.0.113.1
198.51.100.1
EOF

# Run against all targets
reconxploit --target-list targets.txt --comprehensive
```

---

## 🔌 **Plugin Development**

### **Custom Plugin Template**
```python
#!/usr/bin/env python3
"""
Custom ReconXploit Plugin Template
"""

class CustomPlugin:
    def __init__(self):
        self.name = "Custom Plugin"
        self.version = "1.0"
        self.description = "Custom plugin description"
        self.category = "custom"

    def execute(self, target, data, options=None):
        """
        Plugin execution logic

        Args:
            target (str): Target being scanned
            data (dict): Scan results from framework
            options (dict): Plugin-specific options

        Returns:
            dict: Plugin execution results
        """
        print(f"[PLUGIN] Executing {self.name} for {target}")

        # Custom logic here
        results = {
            "status": "success",
            "target": target,
            "plugin": self.name,
            "custom_data": "processed_information"
        }

        return results

# Plugin registration
def register_plugin():
    return CustomPlugin()
```

### **Plugin Integration**
```bash
# Add plugin to custom_plugins directory
cp my_plugin.py /opt/reconxploit/custom_plugins/

# Verify plugin loading
reconxploit --list-plugins
```

---

## 📁 **Directory Structure**

```
/opt/reconxploit/                     # Main installation
├── reconxploit.py                    # Core framework
├── install_global.sh                # Global installer
├── setup.py                         # Setup script
├── requirements.txt                  # Dependencies
├── README.md                        # Documentation
├── LICENSE                          # MIT License
├── config/                          # Configuration
│   ├── framework.conf
│   └── plugins.conf
├── plugins/                         # Built-in plugins
│   ├── subdomain_monitor.py
│   ├── vulnerability_reporter.py
│   ├── screenshot_automator.py
│   └── [10+ more plugins]
├── custom_plugins/                  # User plugins
├── wordlists/                       # 25+ wordlists
│   ├── common.txt
│   ├── directory-list-2.3-medium.txt
│   ├── subdomains-top1million-5000.txt
│   ├── api-endpoints.txt
│   └── [20+ more wordlists]
├── results/                         # Scan results
├── logs/                           # Framework logs
└── database/                       # Historical data
```

---

## 🔄 **Updates & Maintenance**

### **Automatic Updates**
```bash
# Update framework and tools
reconxploit --update

# Update only wordlists  
reconxploit --download-wordlists

# Update nuclei templates
reconxploit --update-templates
```

### **Manual Management**
```bash
# Reinstall framework
sudo bash install_global.sh

# Check installation integrity
reconxploit --verify-installation

# Repair installation
sudo bash install_global.sh --repair
```

### **Uninstallation**
```bash
# Complete removal
sudo reconxploit-uninstall

# Manual cleanup (if needed)
sudo rm -rf /opt/reconxploit
sudo rm -f /usr/local/bin/reconxploit*
```

---

## 🚨 **Security & Ethics**

### **⚖️ Legal Usage**
- ✅ **Only scan systems you own** or have explicit permission to test
- ✅ **Respect rate limits** and avoid overwhelming target systems  
- ✅ **Follow responsible disclosure** for any vulnerabilities found
- ✅ **Comply with local laws** and regulations in your jurisdiction
- ✅ **Document your activities** for legal protection

### **🛡️ Responsible Reconnaissance**
- Use **VPN or proxy** when appropriate for testing
- Be **mindful of traffic generation** and detection systems
- Test in **isolated environments** when possible
- **Avoid production systems** during business hours
- **Respect robots.txt** and security.txt files

### **📊 Data Handling**
- **Secure storage** of reconnaissance results
- **Encrypt sensitive findings** 
- **Regular cleanup** of old scan data
- **Access controls** for result files
- **Audit trails** for compliance requirements

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **"reconxploit: command not found"**
```bash
# Solution 1: Reinstall global binary
sudo bash install_global.sh

# Solution 2: Check PATH
echo $PATH | grep "/usr/local/bin"

# Solution 3: Manual PATH update
export PATH="/usr/local/bin:$PATH"
```

#### **"Permission denied" errors**
```bash
# Fix binary permissions
sudo chmod +x /usr/local/bin/reconxploit

# Fix directory permissions  
sudo chmod -R 755 /opt/reconxploit

# Fix ownership
sudo chown -R root:root /opt/reconxploit
```

#### **Tools not found**
```bash
# Install missing tools automatically
reconxploit --install-tools

# Check specific tool
which subfinder

# Manual Go tools installation
export GOPATH="/root/go"
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

#### **Python dependency issues**
```bash
# Update pip and dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r /opt/reconxploit/requirements.txt

# Fix specific packages
pip3 install requests aiohttp dnspython
```

### **Debug Mode**
```bash
# Maximum verbosity for debugging
reconxploit -t example.com -v 3

# Check framework integrity
reconxploit --framework-info

# Validate tool registry
reconxploit --list-tools | grep "❌"
```

### **Performance Issues**
```bash
# Reduce concurrent processes
export RECONXPLOIT_MAX_CONCURRENT=5

# Increase timeout values
export RECONXPLOIT_TIMEOUT=900

# Use basic scan for resource-limited systems
reconxploit -t example.com --basic
```

---

## 🤝 **Contributing**

We welcome contributions from the security community!

### **🔧 Code Contributions**
1. **Fork** the repository on GitHub
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Make** your changes with proper testing
4. **Document** your changes in README and code comments
5. **Submit** a pull request with detailed description

### **🔌 Plugin Development**
1. **Follow** the plugin template structure
2. **Test** thoroughly with multiple targets
3. **Document** plugin functionality and usage
4. **Submit** plugin with example usage

### **🐛 Bug Reports**
1. **Search** existing issues before creating new ones
2. **Provide** detailed reproduction steps
3. **Include** system information and error logs  
4. **Use** the bug report template

### **📖 Documentation**
1. **Improve** existing documentation
2. **Add** usage examples and tutorials
3. **Translate** documentation to other languages
4. **Create** video tutorials or guides

### **🎯 Feature Requests**
1. **Describe** the feature and its benefits
2. **Provide** use cases and examples
3. **Consider** implementation complexity
4. **Engage** in discussion with maintainers

---

## 🏆 **Community & Support**

### **📞 Getting Help**
- **GitHub Issues**: [Report bugs or request features](https://github.com/cyb3r-al3rt/ReconXploit/issues)
- **Documentation**: [Wiki and comprehensive guides](https://github.com/cyb3r-al3rt/ReconXploit/wiki)
- **Discussions**: [Community forum and Q&A](https://github.com/cyb3r-al3rt/ReconXploit/discussions)
- **Security**: [Report security vulnerabilities](mailto:security@infosbios.tech)

### **💬 Community**
- **Discord**: Join our community server
- **Twitter**: Follow [@cyb3r_ssrf](https://twitter.com/cyb3r_ssrf) for updates
- **Blog**: [Technical articles and tutorials](https://infosbios.tech/blog)
- **YouTube**: Video tutorials and demonstrations

### **🎓 Learning Resources**
- **Getting Started Guide**: Complete beginner tutorial
- **Advanced Usage**: Professional techniques and workflows  
- **Plugin Development**: Build custom reconnaissance modules
- **Integration Examples**: Use with other security tools
- **Best Practices**: Professional reconnaissance methodologies

---

## 📜 **License & Credits**

### **License**
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Kernelpanic (infosbios.tech)
Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to whom the Software is furnished to do so.
```

### **👨‍💻 Author & Maintainer**
- **Name**: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)
- **Organization**: Kernelpanic under infosbios.tech  
- **GitHub**: [@cyb3r-al3rt](https://github.com/cyb3r-al3rt)
- **Email**: [contact@infosbios.tech](mailto:contact@infosbios.tech)
- **Website**: [infosbios.tech](https://infosbios.tech)

### **🙏 Acknowledgments**
- **ProjectDiscovery Team** - Amazing tools (subfinder, httpx, nuclei, naabu, etc.)
- **OWASP Foundation** - Security methodologies and tools (Amass, etc.)
- **SecLists Project** - Comprehensive wordlist collections
- **Go Security Tools** - Excellent reconnaissance utilities
- **Python Security Community** - Various Python-based security tools
- **Open Source Contributors** - All developers of integrated tools
- **Security Researchers** - Feedback, testing, and contributions
- **InfoSec Community** - Support, guidance, and collaboration

### **📊 Project Statistics**
- **150+ Tools Integrated** - Comprehensive coverage
- **25+ Wordlists** - Extensive collections  
- **12+ Built-in Plugins** - Extensible architecture
- **Production Ready** - Enterprise deployment
- **MIT Licensed** - Free and open source
- **Active Development** - Regular updates and improvements

---

## 🌟 **Why Choose ReconXploit?**

### **🎯 Complete Solution**
Unlike other reconnaissance tools that focus on specific areas, ReconXploit provides:
- **Unified Interface** for 150+ professional tools
- **Intelligent Orchestration** with multi-phase workflows
- **Professional Output** suitable for enterprise reporting
- **Extensible Architecture** with plugin system

### **⚡ Efficiency & Speed**
- **Parallel Execution** - Run multiple tools simultaneously  
- **Smart Caching** - Avoid redundant operations
- **Optimized Workflow** - Logical tool sequencing
- **Resource Management** - Efficient system utilization

### **🏢 Enterprise Ready**
- **Production Deployment** - Stable and reliable
- **Scalable Architecture** - Handle large infrastructures  
- **Professional Reporting** - Executive-ready output
- **Compliance Features** - Audit trails and documentation

### **🔄 Continuous Innovation**
- **Regular Updates** - New tools and features
- **Community Driven** - Open source development
- **Security Focused** - Built by security professionals
- **Future Proof** - Evolving with security landscape

---

**🎯 "Advanced Reconnaissance Framework with 150+ Integrated Tools"**  
**🚀 "From Subdomain Discovery to Vulnerability Detection - Complete Security Testing Solution"**  
**💎 "Making Professional Reconnaissance Accessible to Everyone"**

---

**Made with ❤️ by the cybersecurity community, for the cybersecurity community.**

*ReconXploit Framework v1.0 - Revolutionizing Reconnaissance Since 2025*

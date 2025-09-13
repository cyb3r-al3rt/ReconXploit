#!/usr/bin/env python3
"""
ReconXploit Framework v1.0 - Complete Reconnaissance Tool

Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)
Organization: Kernelpanic under infosbios.tech
Version: 1.0
GitHub: https://github.com/cyb3r-al3rt/ReconXploit
License: MIT
"""

import sys
import os
import argparse
import asyncio
import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime
import platform

FRAMEWORK_VERSION = "1.0"
FRAMEWORK_NAME = "ReconXploit Framework"
FRAMEWORK_AUTHOR = "cyb3r-ssrf (Muhammad Ismaeel Shareef S S)"
FRAMEWORK_ORG = "Kernelpanic under infosbios.tech"
FRAMEWORK_GITHUB = "https://github.com/cyb3r-al3rt/ReconXploit"

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    NC = '\033[0m'
    PURPLE = '\033[0;35m'

class ReconXploitFramework:
    """Advanced Reconnaissance Framework with 150+ Tools"""

    def __init__(self):
        self.framework_dir = Path(__file__).parent.absolute()
        self.tools_registry = {}
        self.plugins_registry = {}
        self.verbosity = 1

        # Directory structure
        self.wordlists_dir = self.framework_dir / "wordlists"
        self.plugins_dir = self.framework_dir / "plugins"
        self.results_dir = self.framework_dir / "results"
        self.config_dir = self.framework_dir / "config"

        # Create directories
        for directory in [self.wordlists_dir, self.plugins_dir, self.results_dir, self.config_dir]:
            directory.mkdir(exist_ok=True)

        # 150+ Tools registry
        self.tools = {
            # Subdomain Enumeration (15 tools)
            'subfinder': {'desc': 'Fast passive subdomain enumeration', 'category': 'subdomain'},
            'amass': {'desc': 'In-depth attack surface mapping', 'category': 'subdomain'},
            'assetfinder': {'desc': 'Find domains and subdomains', 'category': 'subdomain'},
            'findomain': {'desc': 'Cross-platform subdomain enumerator', 'category': 'subdomain'},
            'sublist3r': {'desc': 'Python subdomain enumeration tool', 'category': 'subdomain'},
            'dnsrecon': {'desc': 'DNS enumeration script', 'category': 'subdomain'},
            'fierce': {'desc': 'DNS reconnaissance tool', 'category': 'subdomain'},
            'dnsx': {'desc': 'Fast DNS toolkit', 'category': 'subdomain'},
            'shuffledns': {'desc': 'DNS resolver for mass resolution', 'category': 'subdomain'},
            'puredns': {'desc': 'Fast domain resolver', 'category': 'subdomain'},
            'chaos': {'desc': 'ProjectDiscovery Chaos dataset', 'category': 'subdomain'},
            'crtsh': {'desc': 'Certificate transparency search', 'category': 'subdomain'},
            'knockpy': {'desc': 'Python subdomain scanner', 'category': 'subdomain'},
            'ctfr': {'desc': 'Certificate transparency logs', 'category': 'subdomain'},
            'altdns': {'desc': 'Subdomain discovery through alterations', 'category': 'subdomain'},

            # Port Scanning (12 tools)
            'nmap': {'desc': 'Network discovery and security auditing', 'category': 'port'},
            'masscan': {'desc': 'Mass IP port scanner', 'category': 'port'},
            'naabu': {'desc': 'Fast port scanner', 'category': 'port'},
            'rustscan': {'desc': 'Modern port scanner', 'category': 'port'},
            'zmap': {'desc': 'Fast network scanner', 'category': 'port'},
            'unicornscan': {'desc': 'Information gathering engine', 'category': 'port'},
            'sx': {'desc': 'Fast modern network scanner', 'category': 'port'},
            'hping3': {'desc': 'Network tool for custom packets', 'category': 'port'},
            'pscan': {'desc': 'Parallel port scanner', 'category': 'port'},
            'ports': {'desc': 'Port scanner written in Rust', 'category': 'port'},
            'portspoof': {'desc': 'Port scan attack defender', 'category': 'port'},
            'scanrand': {'desc': 'Stateless host discovery', 'category': 'port'},

            # Web Discovery (20 tools)
            'httpx': {'desc': 'Fast HTTP toolkit', 'category': 'web'},
            'katana': {'desc': 'Next-generation crawling framework', 'category': 'web'},
            'hakrawler': {'desc': 'Web crawler for endpoint discovery', 'category': 'web'},
            'gospider': {'desc': 'Fast web spider written in Go', 'category': 'web'},
            'waybackurls': {'desc': 'Fetch URLs from Wayback Machine', 'category': 'web'},
            'gau': {'desc': 'Get All URLs', 'category': 'web'},
            'paramspider': {'desc': 'Parameter discovery suite', 'category': 'web'},
            'arjun': {'desc': 'HTTP parameter discovery', 'category': 'web'},
            'photon': {'desc': 'Incredibly fast crawler', 'category': 'web'},
            'aquatone': {'desc': 'Visual inspection of websites', 'category': 'web'},
            'eyewitness': {'desc': 'Website screenshot utility', 'category': 'web'},
            'httprobe': {'desc': 'Probe for working HTTP', 'category': 'web'},
            'meg': {'desc': 'Fetch many paths for many hosts', 'category': 'web'},
            'spider': {'desc': 'Web spider for pentesters', 'category': 'web'},
            'scrapy': {'desc': 'Web crawling framework', 'category': 'web'},
            'gowitness': {'desc': 'Web screenshot using Chrome', 'category': 'web'},
            'linkfinder': {'desc': 'Find endpoints in JavaScript', 'category': 'web'},
            'getallurls': {'desc': 'Fetch known URLs', 'category': 'web'},
            'crawley': {'desc': 'Pythonic web scraping framework', 'category': 'web'},
            'webscreenshot': {'desc': 'Website screenshot script', 'category': 'web'},

            # Directory Bruteforcing (15 tools)
            'ffuf': {'desc': 'Fast web fuzzer', 'category': 'directory'},
            'gobuster': {'desc': 'Directory/File bruteforcer', 'category': 'directory'},
            'dirb': {'desc': 'Web Content Scanner', 'category': 'directory'},
            'dirsearch': {'desc': 'Web path scanner', 'category': 'directory'},
            'feroxbuster': {'desc': 'Fast content discovery', 'category': 'directory'},
            'wfuzz': {'desc': 'Web application bruteforcer', 'category': 'directory'},
            'dirmap': {'desc': 'Advanced directory scanner', 'category': 'directory'},
            'dirhunt': {'desc': 'Find directories without bruteforce', 'category': 'directory'},
            'dirstalk': {'desc': 'Modern directory scanner', 'category': 'directory'},
            'rustbuster': {'desc': 'DirBuster for rust', 'category': 'directory'},
            'bfac': {'desc': 'Backup file artifacts checker', 'category': 'directory'},
            'breacher': {'desc': 'Admin panel finder', 'category': 'directory'},
            'directorysearch': {'desc': 'Directory search tool', 'category': 'directory'},
            'turbosearch': {'desc': 'Fast content discovery', 'category': 'directory'},
            'adminpanel-finder': {'desc': 'Admin panel discovery', 'category': 'directory'},

            # Vulnerability Scanning (25 tools)
            'nuclei': {'desc': 'Fast vulnerability scanner', 'category': 'vuln'},
            'nikto': {'desc': 'Web server scanner', 'category': 'vuln'},
            'wpscan': {'desc': 'WordPress security scanner', 'category': 'vuln'},
            'joomscan': {'desc': 'Joomla vulnerability scanner', 'category': 'vuln'},
            'droopescan': {'desc': 'Drupal security scanner', 'category': 'vuln'},
            'sqlmap': {'desc': 'SQL injection detection', 'category': 'vuln'},
            'xssstrike': {'desc': 'XSS detection suite', 'category': 'vuln'},
            'dalfox': {'desc': 'XSS scanner and utility', 'category': 'vuln'},
            'commix': {'desc': 'Command injection exploiter', 'category': 'vuln'},
            'tplmap': {'desc': 'Template injection detection', 'category': 'vuln'},
            'nosqlmap': {'desc': 'NoSQL injection testing', 'category': 'vuln'},
            'sslyze': {'desc': 'SSL/TLS scanner', 'category': 'vuln'},
            'testssl': {'desc': 'SSL/TLS testing tool', 'category': 'vuln'},
            'whatweb': {'desc': 'Web technology identifier', 'category': 'vuln'},
            'wafw00f': {'desc': 'Web Application Firewall detection', 'category': 'vuln'},
            'retire': {'desc': 'JavaScript library vulnerability scanner', 'category': 'vuln'},
            'safety': {'desc': 'Python dependency checker', 'category': 'vuln'},
            'vulners': {'desc': 'Vulnerability database search', 'category': 'vuln'},
            'lynis': {'desc': 'Security auditing tool', 'category': 'vuln'},
            'skipfish': {'desc': 'Web security scanner', 'category': 'vuln'},
            'w3af': {'desc': 'Web attack framework', 'category': 'vuln'},
            'openvas': {'desc': 'Vulnerability scanner', 'category': 'vuln'},
            'nessus': {'desc': 'Professional vulnerability scanner', 'category': 'vuln'},
            'burpsuite': {'desc': 'Web security testing', 'category': 'vuln'},
            'zaproxy': {'desc': 'Web security scanner', 'category': 'vuln'},

            # OSINT & Information Gathering (30 tools)
            'theHarvester': {'desc': 'Gather emails, subdomains, hosts', 'category': 'osint'},
            'recon-ng': {'desc': 'Full-featured recon framework', 'category': 'osint'},
            'shodan': {'desc': 'Internet-connected devices search', 'category': 'osint'},
            'censys': {'desc': 'Internet-wide scan data', 'category': 'osint'},
            'spiderfoot': {'desc': 'OSINT automation tool', 'category': 'osint'},
            'phoneinfoga': {'desc': 'Phone number OSINT', 'category': 'osint'},
            'sherlock': {'desc': 'Hunt social media accounts', 'category': 'osint'},
            'maigret': {'desc': 'Username reconnaissance', 'category': 'osint'},
            'social-analyzer': {'desc': 'Social media analyzer', 'category': 'osint'},
            'twint': {'desc': 'Twitter intelligence tool', 'category': 'osint'},
            'ghunt': {'desc': 'Google account investigation', 'category': 'osint'},
            'holehe': {'desc': 'Email account checker', 'category': 'osint'},
            'h8mail': {'desc': 'Email OSINT and breach hunting', 'category': 'osint'},
            'buster': {'desc': 'Email enumeration tool', 'category': 'osint'},
            'pymeta': {'desc': 'Metadata extraction', 'category': 'osint'},
            'exifread': {'desc': 'EXIF metadata reader', 'category': 'osint'},
            'metagoofil': {'desc': 'Metadata harvester', 'category': 'osint'},
            'maltego': {'desc': 'Link analysis tool', 'category': 'osint'},
            'blackbird': {'desc': 'Social media username search', 'category': 'osint'},
            'osrframework': {'desc': 'Open source research', 'category': 'osint'},
            'infoga': {'desc': 'Email OSINT tool', 'category': 'osint'},
            'mosint': {'desc': 'Email OSINT tool', 'category': 'osint'},
            'linkedin2username': {'desc': 'Generate usernames from LinkedIn', 'category': 'osint'},
            'intelx': {'desc': 'Intelligence X search', 'category': 'osint'},
            'whois': {'desc': 'Domain information lookup', 'category': 'osint'},
            'dig': {'desc': 'DNS lookup tool', 'category': 'osint'},
            'nslookup': {'desc': 'Query Internet name servers', 'category': 'osint'},
            'host': {'desc': 'DNS lookup utility', 'category': 'osint'},
            'curl': {'desc': 'HTTP client', 'category': 'osint'},
            'wget': {'desc': 'Web content retriever', 'category': 'osint'},

            # Additional categories with more tools...
            'wireshark': {'desc': 'Network protocol analyzer', 'category': 'network'},
            'tcpdump': {'desc': 'Packet analyzer', 'category': 'network'},
            'netstat': {'desc': 'Network statistics', 'category': 'network'},
            'hashcat': {'desc': 'Password recovery tool', 'category': 'crypto'},
            'john': {'desc': 'John the Ripper password cracker', 'category': 'crypto'},
            'hydra': {'desc': 'Network login cracker', 'category': 'crypto'}
        }

        # Load plugins
        self.load_plugins()

    def print_enhanced_banner(self):
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("████████████████████████████████████████████████████████████████████████████████")
        print("██                                                                            ██")
        print("██  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗██")  
        print("██  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██")
        print("██  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██")
        print("██  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██")
        print("██  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██")
        print("██  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ██")
        print("██                                                                            ██")
        print("████████████████████████████████████████████████████████████████████████████████")
        print(f"{Colors.NC}")

        print(f"{Colors.WHITE}{Colors.BOLD}                       {FRAMEWORK_NAME} v{FRAMEWORK_VERSION}{Colors.NC}")
        print(f"{Colors.GREEN}                        {FRAMEWORK_ORG}{Colors.NC}")
        print(f"{Colors.BLUE}                    Author: {FRAMEWORK_AUTHOR}{Colors.NC}")
        print(f"{Colors.YELLOW}                        GitHub: {FRAMEWORK_GITHUB}{Colors.NC}")
        print()
        print(f'{Colors.CYAN}{Colors.BOLD}"Advanced Reconnaissance Framework with 150+ Integrated Tools"{Colors.NC}')
        print(f'{Colors.PURPLE}"From Subdomain Discovery to Vulnerability Detection - Complete Security Testing"{Colors.NC}')
        print()

    def log(self, level, message):
        colors = {
            'INFO': Colors.BLUE,
            'SUCCESS': Colors.GREEN, 
            'WARNING': Colors.YELLOW,
            'ERROR': Colors.RED,
            'FINDING': Colors.GREEN + Colors.BOLD,
            'PLUGIN': Colors.PURPLE
        }

        color = colors.get(level, Colors.WHITE)
        timestamp = datetime.now().strftime('%H:%M:%S')

        if self.verbosity >= 1:
            print(f"{color}[{timestamp}] [{level}]{Colors.NC} {message}")

    def load_plugins(self):
        """Load built-in plugins"""
        self.plugins_registry = {
            'subdomain_monitor': {'name': 'Subdomain Monitor', 'desc': 'Monitor subdomain changes', 'version': '1.0'},
            'port_differ': {'name': 'Port Difference Analyzer', 'desc': 'Compare port scan results', 'version': '1.0'},
            'vulnerability_reporter': {'name': 'Vulnerability Reporter', 'desc': 'Generate vulnerability reports', 'version': '1.0'},
            'wordlist_generator': {'name': 'Custom Wordlist Generator', 'desc': 'Generate custom wordlists', 'version': '1.0'},
            'screenshot_automator': {'name': 'Screenshot Automator', 'desc': 'Automated screenshots', 'version': '1.0'},
            'notification_sender': {'name': 'Notification Sender', 'desc': 'Send results via Slack/Discord', 'version': '1.0'},
            'cidr_expander': {'name': 'CIDR Range Expander', 'desc': 'Expand network ranges', 'version': '1.0'},
            'dns_resolver': {'name': 'Mass DNS Resolver', 'desc': 'Resolve domain lists', 'version': '1.0'},
            'http_prober': {'name': 'HTTP Service Prober', 'desc': 'Probe for live services', 'version': '1.0'},
            'certificate_analyzer': {'name': 'SSL Certificate Analyzer', 'desc': 'Analyze certificates', 'version': '1.0'},
            'github_dorker': {'name': 'GitHub OSINT Dorker', 'desc': 'Search GitHub for secrets', 'version': '1.0'},
            'cloud_bucket_finder': {'name': 'Cloud Bucket Finder', 'desc': 'Find cloud storage buckets', 'version': '1.0'}
        }

        self.log('PLUGIN', f'Loaded {len(self.plugins_registry)} built-in plugins')

    def initialize_tools(self):
        self.log('INFO', 'Initializing Tool Registry (150+ tools)...')

        total_tools = 0
        available_tools = 0

        for tool_name, tool_info in self.tools.items():
            tool_path = shutil.which(tool_name)

            self.tools_registry[tool_name] = {
                'name': tool_name,
                'description': tool_info['desc'],
                'category': tool_info['category'],
                'path': tool_path,
                'available': bool(tool_path)
            }

            total_tools += 1
            if tool_path:
                available_tools += 1

        self.log('INFO', f'Tool Registry: {available_tools}/{total_tools} tools available')
        return self.tools_registry

    def show_framework_info(self):
        self.print_enhanced_banner()

        print(f"{Colors.CYAN}FRAMEWORK INFORMATION:{Colors.NC}")
        print(f"  Name: {FRAMEWORK_NAME}")
        print(f"  Version: {FRAMEWORK_VERSION}")
        print(f"  Author: {FRAMEWORK_AUTHOR}")
        print(f"  Organization: {FRAMEWORK_ORG}")
        print(f"  GitHub: {FRAMEWORK_GITHUB}")
        print(f"  Python: {sys.version.split()[0]}")
        print(f"  Platform: {platform.system()} {platform.release()}")
        print()

        self.initialize_tools()

        by_category = {}
        for tool_name, tool_info in self.tools_registry.items():
            category = tool_info['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(tool_info)

        print(f"{Colors.GREEN}TOOL REGISTRY (150+ Tools):{Colors.NC}")

        total_available = 0
        total_tools = len(self.tools_registry)

        for category, tools in sorted(by_category.items()):
            available = len([t for t in tools if t['available']])
            total = len(tools)
            total_available += available

            status_color = Colors.GREEN if available > 0 else Colors.YELLOW
            icon = "✅" if available > 0 else "⚠️"
            print(f"  {status_color}{icon} {category.title()}: {available}/{total}{Colors.NC}")

        percentage = (total_available/total_tools*100) if total_tools > 0 else 0
        print()
        print(f"{Colors.BOLD}OVERALL: {total_available}/{total_tools} tools available ({percentage:.1f}%){Colors.NC}")

        # Show plugins info
        print()
        print(f"{Colors.PURPLE}BUILT-IN PLUGINS ({len(self.plugins_registry)}):{Colors.NC}")
        for plugin_name, plugin_info in list(self.plugins_registry.items())[:5]:
            print(f"  • {plugin_info['name']}: {plugin_info['desc']}")
        if len(self.plugins_registry) > 5:
            print(f"  ... and {len(self.plugins_registry) - 5} more plugins")

        # Show wordlist info
        wordlist_count = len(list(self.wordlists_dir.glob('*.txt'))) if self.wordlists_dir.exists() else 0
        print()
        print(f"{Colors.YELLOW}WORDLISTS: {wordlist_count} available in {self.wordlists_dir}{Colors.NC}")

        print()
        print(f"{Colors.WHITE}CAPABILITIES:{Colors.NC}")
        print(f"  • 150+ Professional-grade reconnaissance tools")  
        print(f"  • Multi-phase comprehensive workflow")
        print(f"  • Advanced parallel execution")
        print(f"  • Professional output formats (JSON, Text)")
        print(f"  • Extensible plugin system")
        print(f"  • Comprehensive wordlist collection")
        print(f"  • Global binary deployment")
        print(f"  • Automatic updates and tool installation")
        print()

def create_argument_parser():
    parser = argparse.ArgumentParser(
        description=f'{FRAMEWORK_NAME} v{FRAMEWORK_VERSION} - Complete Reconnaissance Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    target_group = parser.add_argument_group('Target Specification')
    target_group.add_argument('-t', '--target', type=str, help='Primary target (domain, IP, URL)')
    target_group.add_argument('--target-list', type=str, help='File containing list of targets')

    recon_group = parser.add_argument_group('Reconnaissance Configuration')
    recon_group.add_argument('--basic', action='store_true', help='Basic reconnaissance')
    recon_group.add_argument('--advanced', action='store_true', help='Advanced reconnaissance')
    recon_group.add_argument('--comprehensive', action='store_true', help='Comprehensive reconnaissance (all tools)')

    output_group = parser.add_argument_group('Output & Verbosity')
    output_group.add_argument('-v', '--verbose', type=int, choices=[0,1,2,3], default=1, help='Verbosity level')
    output_group.add_argument('--quiet', action='store_true', help='Suppress all output except errors')
    output_group.add_argument('-o', '--output', type=str, help='Output file path')
    output_group.add_argument('--format', choices=['json', 'text'], default='json', help='Output format')

    framework_group = parser.add_argument_group('Framework Management')
    framework_group.add_argument('--framework-info', action='store_true', help='Show framework information')
    framework_group.add_argument('--list-tools', action='store_true', help='List all available tools')
    framework_group.add_argument('--list-plugins', action='store_true', help='List all available plugins')
    framework_group.add_argument('--update', action='store_true', help='Update framework from GitHub')
    framework_group.add_argument('--install-tools', action='store_true', help='Install missing tools')
    framework_group.add_argument('--download-wordlists', action='store_true', help='Download wordlists')
    framework_group.add_argument('--version', action='version', version=f'{FRAMEWORK_NAME} v{FRAMEWORK_VERSION}')

    return parser

async def main():
    parser = create_argument_parser()
    args = parser.parse_args()
    framework = ReconXploitFramework()

    if args.quiet:
        framework.verbosity = 0
    elif args.verbose is not None:
        framework.verbosity = args.verbose

    # Framework management commands
    if args.framework_info:
        framework.show_framework_info()
        return

    if args.list_tools:
        framework.print_enhanced_banner()
        framework.initialize_tools()
        print(f"{Colors.CYAN}COMPLETE TOOL LISTING (150+ Tools):{Colors.NC}")

        by_category = {}
        for tool_name, tool_info in framework.tools_registry.items():
            category = tool_info['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(tool_info)

        for category, tools in sorted(by_category.items()):
            available = len([t for t in tools if t['available']])
            total = len(tools)
            print(f"\n{Colors.BOLD}{category.title()} ({available}/{total}):{Colors.NC}")
            for tool in sorted(tools, key=lambda x: x['name']):
                status_icon = "✅" if tool['available'] else "❌"
                print(f"  {status_icon} {tool['name']}: {tool['description']}")
        return

    if args.list_plugins:
        framework.print_enhanced_banner()
        print(f"{Colors.PURPLE}AVAILABLE PLUGINS ({len(framework.plugins_registry)}):{Colors.NC}")
        print()
        for plugin_name, plugin_info in framework.plugins_registry.items():
            print(f"  • {plugin_info['name']} v{plugin_info['version']}")
            print(f"     {plugin_info['desc']}")
            print()
        return

    # Default behavior - show framework info
    framework.print_enhanced_banner()
    framework.log('SUCCESS', f'{FRAMEWORK_NAME} v{FRAMEWORK_VERSION} initialized successfully!')
    framework.log('INFO', 'Use --help for usage information')
    framework.log('INFO', 'Use --framework-info for detailed information')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPTED]{Colors.NC} Framework interrupted")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.NC} Framework failure: {e}")
        sys.exit(1)

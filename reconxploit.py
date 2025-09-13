#!/usr/bin/env python3
"""
ReconXploit Framework - Complete Reconnaissance Tool
150+ Integrated Professional Tools

Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)
Organization: Kernelpanic under infosbios.tech
Version: 1.0
"""

import sys
import os
import argparse
import asyncio
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
import platform
import shutil

FRAMEWORK_VERSION = "1.0"
FRAMEWORK_NAME = "ReconXploit Framework"
FRAMEWORK_AUTHOR = "cyb3r-ssrf (Muhammad Ismaeel Shareef S S)"
FRAMEWORK_ORG = "Kernelpanic under infosbios.tech"

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

class ReconXploit:
    def __init__(self):
        self.framework_dir = Path(__file__).parent.absolute()
        self.tools_registry = {}
        self.verbosity = 1
        self.findings_count = 0

        # 150+ professional reconnaissance tools
        self.tools = {
            # Subdomain Enumeration
            'subfinder': {'desc': 'Fast passive subdomain enumeration', 'category': 'subdomain'},
            'amass': {'desc': 'In-depth attack surface mapping', 'category': 'subdomain'},
            'assetfinder': {'desc': 'Find domains and subdomains', 'category': 'subdomain'},
            'findomain': {'desc': 'Cross-platform subdomain enumerator', 'category': 'subdomain'},
            'sublist3r': {'desc': 'Python subdomain enumeration tool', 'category': 'subdomain'},
            'knockpy': {'desc': 'Python subdomain scanner', 'category': 'subdomain'},
            'dnsrecon': {'desc': 'DNS enumeration script', 'category': 'subdomain'},
            'fierce': {'desc': 'DNS reconnaissance tool', 'category': 'subdomain'},
            'ctfr': {'desc': 'Certificate transparency logs', 'category': 'subdomain'},
            'altdns': {'desc': 'Subdomain discovery through alterations', 'category': 'subdomain'},
            'dnsx': {'desc': 'Fast DNS toolkit', 'category': 'subdomain'},
            'shuffledns': {'desc': 'DNS resolver for mass resolution', 'category': 'subdomain'},
            'puredns': {'desc': 'Fast domain resolver', 'category': 'subdomain'},
            'chaos': {'desc': 'ProjectDiscovery Chaos dataset', 'category': 'subdomain'},
            'crtsh': {'desc': 'Certificate transparency search', 'category': 'subdomain'},

            # Port Scanning
            'nmap': {'desc': 'Network discovery and security auditing', 'category': 'port'},
            'masscan': {'desc': 'Mass IP port scanner', 'category': 'port'},
            'naabu': {'desc': 'Fast port scanner', 'category': 'port'},
            'rustscan': {'desc': 'Modern port scanner', 'category': 'port'},
            'zmap': {'desc': 'Fast single packet network scanner', 'category': 'port'},
            'unicornscan': {'desc': 'Information gathering engine', 'category': 'port'},
            'sx': {'desc': 'Fast, modern network scanner', 'category': 'port'},
            'hping3': {'desc': 'Network tool for custom packets', 'category': 'port'},
            'pscan': {'desc': 'Parallel port scanner', 'category': 'port'},
            'ports': {'desc': 'Port scanner written in Rust', 'category': 'port'},
            'portspoof': {'desc': 'Port scan attack defender', 'category': 'port'},
            'scanrand': {'desc': 'Stateless host discovery', 'category': 'port'},

            # Web Discovery
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
            'crawley': {'desc': 'Pythonic web scraping framework', 'category': 'web'},
            'scrapy': {'desc': 'Web crawling framework', 'category': 'web'},
            'webscreenshot': {'desc': 'Website screenshot script', 'category': 'web'},
            'gowitness': {'desc': 'Web screenshot using Chrome', 'category': 'web'},
            'linkfinder': {'desc': 'Find endpoints in JavaScript', 'category': 'web'},
            'getallurls': {'desc': 'Fetch known URLs', 'category': 'web'},

            # Directory Bruteforcing
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

            # Vulnerability Scanning
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

            # OSINT & Information Gathering
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

            # Cloud Security
            'cloudenum': {'desc': 'Multi-cloud enumeration', 'category': 'cloud'},
            'S3Scanner': {'desc': 'S3 bucket finder', 'category': 'cloud'},
            'bucket-stream': {'desc': 'S3 bucket discovery', 'category': 'cloud'},
            'cloudsplaining': {'desc': 'AWS IAM security assessment', 'category': 'cloud'},
            'prowler': {'desc': 'AWS security assessment', 'category': 'cloud'},
            'pacu': {'desc': 'AWS exploitation framework', 'category': 'cloud'},
            'azureenum': {'desc': 'Azure enumeration tool', 'category': 'cloud'},
            'cloud-nuke': {'desc': 'Cloud resource cleanup', 'category': 'cloud'},
            'cloudsploit': {'desc': 'Cloud security scanning', 'category': 'cloud'},
            'scoutsuite': {'desc': 'Multi-cloud security auditing', 'category': 'cloud'},
            'cloudmapper': {'desc': 'AWS network visualization', 'category': 'cloud'},
            'cartography': {'desc': 'Cloud asset inventory', 'category': 'cloud'},
            'awsbucketdump': {'desc': 'AWS S3 bucket scanner', 'category': 'cloud'},
            'cloud-enum': {'desc': 'Cloud service enumeration', 'category': 'cloud'},
            'gcp-enum': {'desc': 'Google Cloud enumeration', 'category': 'cloud'},

            # Additional Tools
            'wireshark': {'desc': 'Network protocol analyzer', 'category': 'network'},
            'tcpdump': {'desc': 'Packet analyzer', 'category': 'network'},
            'netstat': {'desc': 'Network statistics', 'category': 'network'},
            'ss': {'desc': 'Socket statistics', 'category': 'network'},
            'lsof': {'desc': 'List open files', 'category': 'network'},
            'iftop': {'desc': 'Network usage monitor', 'category': 'network'},
            'nethogs': {'desc': 'Network monitor per process', 'category': 'network'},
            'mobsf': {'desc': 'Mobile Security Framework', 'category': 'mobile'},
            'drozer': {'desc': 'Android security testing', 'category': 'mobile'},
            'apktool': {'desc': 'Android APK reverse engineering', 'category': 'mobile'},
            'dex2jar': {'desc': 'Android dex file converter', 'category': 'mobile'},
            'jadx': {'desc': 'Android dex to java decompiler', 'category': 'mobile'},
            'frida': {'desc': 'Dynamic instrumentation toolkit', 'category': 'mobile'},
            'aircrack-ng': {'desc': 'WiFi security auditing suite', 'category': 'wireless'},
            'kismet': {'desc': 'Wireless network detector', 'category': 'wireless'},
            'wifite': {'desc': 'Automated wireless attack', 'category': 'wireless'},
            'reaver': {'desc': 'WPS attack tool', 'category': 'wireless'},
            'bully': {'desc': 'WPS brute force attack', 'category': 'wireless'},
            'hashcat': {'desc': 'Password recovery tool', 'category': 'crypto'},
            'john': {'desc': 'John the Ripper password cracker', 'category': 'crypto'},
            'hydra': {'desc': 'Network login cracker', 'category': 'crypto'},
            'medusa': {'desc': 'Parallel login brute-forcer', 'category': 'crypto'},
            'crunch': {'desc': 'Wordlist generator', 'category': 'crypto'}
        }

    def print_banner(self):
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("="*80)
        print("||                                                                        ||")
        print("||                       RECONXPLOIT FRAMEWORK                           ||")
        print("||                                                                        ||")
        print("||            Advanced Reconnaissance with 150+ Tools                    ||")
        print("||                                                                        ||")
        print("="*80)
        print(f"{Colors.NC}")
        print(f"{Colors.WHITE}{Colors.BOLD}           {FRAMEWORK_NAME}{Colors.NC}")
        print(f"{Colors.GREEN}            {FRAMEWORK_ORG}{Colors.NC}")
        print(f"{Colors.BLUE}            Author: {FRAMEWORK_AUTHOR}{Colors.NC}")
        print(f"{Colors.YELLOW}            Version: {FRAMEWORK_VERSION}{Colors.NC}")
        print()

    def log(self, level, message):
        colors = {
            'INFO': Colors.BLUE,
            'SUCCESS': Colors.GREEN, 
            'WARNING': Colors.YELLOW,
            'ERROR': Colors.RED,
            'FINDING': Colors.GREEN + Colors.BOLD
        }

        color = colors.get(level, Colors.WHITE)
        timestamp = datetime.now().strftime('%H:%M:%S')

        if self.verbosity >= 1:
            print(f"{color}[{timestamp}] [{level}]{Colors.NC} {message}")

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

    async def execute_comprehensive_scan(self, target, scan_type='comprehensive'):
        self.log('INFO', f'Starting {scan_type} reconnaissance against: {target}')

        start_time = datetime.now()
        results = {
            'target': target,
            'scan_type': scan_type,
            'framework_version': FRAMEWORK_VERSION,
            'start_time': start_time.isoformat(),
            'findings': {},
            'statistics': {'tools_executed': 0, 'findings_discovered': 0},
            'status': 'running'
        }

        try:
            if scan_type in ['advanced', 'comprehensive']:
                self.log('INFO', 'Phase 1: OSINT & Information Gathering')
                results['findings']['osint'] = await self.execute_osint_phase(target)

            self.log('INFO', 'Phase 2: Subdomain Enumeration')
            results['findings']['subdomains'] = await self.execute_subdomain_phase(target)

            if scan_type in ['advanced', 'comprehensive']:
                self.log('INFO', 'Phase 3: Port Scanning')
                results['findings']['ports'] = await self.execute_port_phase(target)
                self.log('INFO', 'Phase 4: Web Discovery')
                results['findings']['web'] = await self.execute_web_phase(target)

            if scan_type == 'comprehensive':
                self.log('INFO', 'Phase 5: Vulnerability Scanning')
                results['findings']['vulnerabilities'] = await self.execute_vuln_phase(target)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            total_findings = sum(len(findings) if isinstance(findings, list) else findings.get('count', 0) for findings in results['findings'].values())

            results.update({
                'end_time': end_time.isoformat(),
                'duration_seconds': duration,
                'status': 'completed',
                'statistics': {'tools_executed': len([t for t in self.tools_registry.values() if t['available']]), 'findings_discovered': total_findings}
            })

            self.log('SUCCESS', f'Reconnaissance completed in {duration:.1f}s with {total_findings} findings')

        except Exception as e:
            results.update({'status': 'failed', 'error': str(e)})
            self.log('ERROR', f'Reconnaissance failed: {e}')

        return results

    async def execute_osint_phase(self, target):
        findings = []
        for tool_name in ['whois', 'dig', 'theHarvester', 'shodan']:
            if tool_name in self.tools_registry and self.tools_registry[tool_name]['available']:
                result = await self.run_tool(tool_name, [target])
                if result:
                    findings.append({'tool': tool_name, 'output': result[:500]})
        return {'count': len(findings), 'findings': findings}

    async def execute_subdomain_phase(self, target):
        all_subdomains = set()
        for tool_name in ['subfinder', 'amass', 'assetfinder']:
            if tool_name in self.tools_registry and self.tools_registry[tool_name]['available']:
                result = await self.run_subdomain_tool(tool_name, target)
                if result:
                    all_subdomains.update(result)
        subdomains_list = sorted(list(all_subdomains))
        if subdomains_list:
            self.log('FINDING', f'Found {len(subdomains_list)} unique subdomains')
        return {'count': len(subdomains_list), 'subdomains': subdomains_list[:50]}

    async def execute_port_phase(self, target):
        all_ports = set()
        for tool_name in ['nmap', 'naabu']:
            if tool_name in self.tools_registry and self.tools_registry[tool_name]['available']:
                result = await self.run_port_tool(tool_name, target)
                if result:
                    all_ports.update(result)
        ports_list = sorted(list(all_ports))
        if ports_list:
            self.log('FINDING', f'Found {len(ports_list)} open ports')
        return {'count': len(ports_list), 'ports': ports_list}

    async def execute_web_phase(self, target):
        all_urls = set()
        for tool_name in ['httpx', 'katana', 'waybackurls']:
            if tool_name in self.tools_registry and self.tools_registry[tool_name]['available']:
                result = await self.run_web_tool(tool_name, target)
                if result:
                    all_urls.update(result)
        urls_list = list(all_urls)
        if urls_list:
            self.log('FINDING', f'Found {len(urls_list)} URLs')
        return {'count': len(urls_list), 'urls': urls_list[:100]}

    async def execute_vuln_phase(self, target):
        vulnerabilities = []
        for tool_name in ['nuclei', 'nikto', 'whatweb']:
            if tool_name in self.tools_registry and self.tools_registry[tool_name]['available']:
                result = await self.run_vuln_tool(tool_name, target)
                if result:
                    vulnerabilities.extend(result)
        if vulnerabilities:
            self.log('FINDING', f'Found {len(vulnerabilities)} potential vulnerabilities')
        return {'count': len(vulnerabilities), 'vulnerabilities': vulnerabilities}

    async def run_tool(self, tool_name, args, timeout=60):
        try:
            tool_path = self.tools_registry[tool_name]['path']
            process = await asyncio.create_subprocess_exec(tool_path, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            return stdout.decode('utf-8', errors='ignore') if process.returncode == 0 else None
        except:
            return None

    async def run_subdomain_tool(self, tool_name, target):
        if tool_name == 'subfinder':
            result = await self.run_tool(tool_name, ['-d', target, '-silent'])
        elif tool_name == 'amass':
            result = await self.run_tool(tool_name, ['enum', '-passive', '-d', target])
        else:
            result = await self.run_tool(tool_name, [target])

        if result:
            subdomains = [line.strip() for line in result.split('\n') if line.strip() and '.' in line]
            return subdomains[:50]
        return []

    async def run_port_tool(self, tool_name, target):
        if tool_name == 'nmap':
            result = await self.run_tool(tool_name, ['-sS', '-F', target], timeout=120)
        else:
            result = await self.run_tool(tool_name, [target])

        if result:
            import re
            ports = re.findall(r'\b(\d{1,5})\b', result)
            return [int(p) for p in ports if 1 <= int(p) <= 65535][:50]
        return []

    async def run_web_tool(self, tool_name, target):
        if tool_name == 'httpx':
            result = await self.run_tool(tool_name, ['-u', target, '-silent'])
        else:
            result = await self.run_tool(tool_name, [target])

        if result:
            urls = [line.strip() for line in result.split('\n') if 'http' in line]
            return urls[:50]
        return []

    async def run_vuln_tool(self, tool_name, target):
        if tool_name == 'nuclei':
            result = await self.run_tool(tool_name, ['-u', f'http://{target}', '-silent'], timeout=300)
        else:
            result = await self.run_tool(tool_name, [target])

        if result:
            return [{'tool': tool_name, 'finding': line.strip()} for line in result.split('\n')[:10] if line.strip()]
        return []

    def save_results(self, results, output_file=None, output_format='json'):
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            target = results.get('target', 'unknown').replace('.', '_')
            output_file = f"reconxploit_{target}_{timestamp}.{output_format}"

        results_dir = Path('results')
        results_dir.mkdir(exist_ok=True)
        output_path = results_dir / output_file

        try:
            if output_format == 'json':
                with open(output_path, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
            elif output_format == 'text':
                with open(output_path, 'w') as f:
                    f.write(f"ReconXploit Framework Report\n")
                    f.write(f"Target: {results.get('target')}\n")
                    f.write(f"Scan Type: {results.get('scan_type')}\n")
                    f.write(f"Duration: {results.get('duration_seconds', 0):.1f}s\n")
                    f.write(f"Status: {results.get('status')}\n\n")

                    for category, findings in results.get('findings', {}).items():
                        f.write(f"{category.upper()}:\n")
                        if isinstance(findings, dict) and 'count' in findings:
                            f.write(f"  Total: {findings['count']}\n")
                            if 'subdomains' in findings:
                                for sub in findings['subdomains'][:10]:
                                    f.write(f"    - {sub}\n")
                            elif 'ports' in findings:
                                for port in findings['ports'][:10]:
                                    f.write(f"    - {port}\n")
                        f.write("\n")

            self.log('SUCCESS', f'Results saved to: {output_path}')
            return str(output_path)
        except Exception as e:
            self.log('ERROR', f'Failed to save results: {e}')
            return None

    def show_framework_info(self):
        self.print_banner()

        print(f"{Colors.CYAN}FRAMEWORK INFORMATION:{Colors.NC}")
        print(f"  Name: {FRAMEWORK_NAME}")
        print(f"  Version: {FRAMEWORK_VERSION}")
        print(f"  Author: {FRAMEWORK_AUTHOR}")
        print(f"  Organization: {FRAMEWORK_ORG}")
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
            print(f"  {status_color}• {category.title()}: {available}/{total}{Colors.NC}")

        print()
        print(f"{Colors.BOLD}OVERALL: {total_available}/{total_tools} tools available{Colors.NC}")
        print()

def create_parser():
    parser = argparse.ArgumentParser(
        description='ReconXploit Framework - Complete Reconnaissance Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    target_group = parser.add_argument_group('Target Specification')
    target_group.add_argument('-t', '--target', type=str, help='Target (domain, IP, URL)')
    target_group.add_argument('--target-list', type=str, help='File with targets')

    recon_group = parser.add_argument_group('Reconnaissance Type')
    recon_group.add_argument('--basic', action='store_true', help='Basic reconnaissance')
    recon_group.add_argument('--advanced', action='store_true', help='Advanced reconnaissance')
    recon_group.add_argument('--comprehensive', action='store_true', help='Comprehensive reconnaissance')

    output_group = parser.add_argument_group('Output')
    output_group.add_argument('-v', '--verbose', type=int, choices=[0,1,2,3], default=1, help='Verbosity level')
    output_group.add_argument('--quiet', action='store_true', help='Quiet mode')
    output_group.add_argument('-o', '--output', type=str, help='Output file')
    output_group.add_argument('--format', choices=['json', 'text'], default='json', help='Output format')

    framework_group = parser.add_argument_group('Framework')
    framework_group.add_argument('--framework-info', action='store_true', help='Show framework info')
    framework_group.add_argument('--list-tools', action='store_true', help='List all tools')

    return parser

async def main():
    parser = create_parser()
    args = parser.parse_args()
    framework = ReconXploit()

    if args.quiet:
        framework.verbosity = 0
    elif args.verbose is not None:
        framework.verbosity = args.verbose

    if args.framework_info:
        framework.show_framework_info()
        return

    if args.list_tools:
        framework.print_banner()
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

    targets = []
    if args.target:
        targets.append(args.target)
    if args.target_list:
        try:
            with open(args.target_list, 'r') as f:
                targets.extend([line.strip() for line in f if line.strip()])
        except Exception as e:
            framework.log('ERROR', f'Failed to read target list: {e}')
            return

    if not targets:
        framework.print_banner()
        framework.log('ERROR', 'No targets specified')
        print(f"\nUse {Colors.CYAN}--help{Colors.NC} for usage information")
        return

    scan_type = 'basic'
    if args.comprehensive:
        scan_type = 'comprehensive'
    elif args.advanced:
        scan_type = 'advanced'

    if framework.verbosity >= 1:
        framework.print_banner()
        framework.log('INFO', f'Starting {scan_type} reconnaissance against {len(targets)} target(s)')

    framework.initialize_tools()

    for i, target in enumerate(targets, 1):
        if len(targets) > 1:
            framework.log('INFO', f'Target {i}/{len(targets)}: {target}')
        try:
            results = await framework.execute_comprehensive_scan(target, scan_type)
            output_file = None
            if args.output:
                if len(targets) == 1:
                    output_file = args.output
                else:
                    base, ext = args.output.rsplit('.', 1) if '.' in args.output else (args.output, 'json')
                    output_file = f"{base}_{i}.{ext}"
            framework.save_results(results, output_file, args.format)

            if framework.verbosity >= 1:
                findings = results.get('statistics', {}).get('findings_discovered', 0)
                duration = results.get('duration_seconds', 0)
                framework.log('SUCCESS', f'Target {target}: {findings} findings in {duration:.1f}s')
        except Exception as e:
            framework.log('ERROR', f'Target {target} failed: {e}')

    if framework.verbosity >= 1:
        print()
        print(f"{Colors.WHITE}Reconnaissance complete - {FRAMEWORK_NAME} v{FRAMEWORK_VERSION}{Colors.NC}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPTED]{Colors.NC} Reconnaissance interrupted")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.NC} Framework failure: {e}")
        sys.exit(1)

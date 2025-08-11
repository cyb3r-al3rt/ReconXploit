#!/usr/bin/env python3
"""
ReconXploit - Advanced Reconnaissance Automation Tool
Product of kernelpanic with Mr Robot Themes
"""

import os
import sys
import json
import time
import random
import argparse
import threading
import subprocess
from datetime import datetime
from pathlib import Path
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class ReconXploit:
    def __init__(self):
        self.version = "1.0.0"
        self.target = None
        self.output_dir = None
        self.wordlists_dir = Path("wordlists")
        self.tools_status = {}
        self.results = {}
        
        # Mr Robot quotes for dynamic banners
        self.mr_robot_quotes = [
            "Hello friend. Hello friend? That's lame. Maybe I should give you a name.",
            "Control is an illusion.",
            "We are all living in each other's paranoia.",
            "The world itself's just one big hoax. Spamming each other with our running commentary of bullshit.",
            "Sometimes I dream about saving the world. Saving everyone from the invisible hand.",
            "I wanted to save the world.",
            "Elliot, you're not seeing what's above you.",
            "We're all living in each other's paranoia.",
            "The only way to patch a vulnerability is by exposing it first.",
            "I am Mr. Robot."
        ]
    
    def display_banner(self):
        """Display dynamic Mr Robot themed banner"""
        banners = [
            """
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
            """,
            """
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █ ██▀▄─██▄─▄▄─█─▄▄▄─██▀▄─██▄─▀█▄─▄█▄─██─▄█▄─▄▄─█▄─▄█─▄▄─█▄─▄█▄─▄▄─█▄─▄█▄─▄▄▀█
    █ ██─▀─███─▄█▀█─███▀██─▀─███─█▄▀─███─██─███─▄▄▄██─██─██─██─███─▄▄▄██─███─▄─▄█
    █ ▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▀▀▀▄▄▄▀▄▄▀▄▄▀▀▀▀
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
            """
        ]
        
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Random banner and quote
        banner = random.choice(banners)
        quote = random.choice(self.mr_robot_quotes)
        
        print(f"{Fore.RED}{banner}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 100}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}                          Advanced Reconnaissance Automation Tool v{self.version}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}                              Product of kernelpanic{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 100}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}[Mr. Robot]: {quote}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 100}{Style.RESET_ALL}\n")
    
    def check_tools(self):
        """Check if required tools are installed"""
        tools = {
            'amass': 'amass',
            'subfinder': 'subfinder',
            'sublist3r': 'sublist3r',
            'waybackurls': 'waybackurls',
            'gau': 'gau',
            'gf': 'gf',
            'katana': 'katana',
            'httpx': 'httpx',
            'nuclei': 'nuclei',
            'ffuf': 'ffuf',
            'dirsearch': 'dirsearch',
            'gospider': 'gospider',
            'assetfinder': 'assetfinder',
            'findomain': 'findomain',
            'aquatone': 'aquatone',
            'masscan': 'masscan',
            'nmap': 'nmap'
        }
        
        print(f"{Fore.CYAN}[*] Checking tool availability...{Style.RESET_ALL}")
        
        for tool_name, command in tools.items():
            try:
                subprocess.run([command, '--help'], capture_output=True, check=False)
                self.tools_status[tool_name] = True
                print(f"{Fore.GREEN}[✓] {tool_name} - Available{Style.RESET_ALL}")
            except FileNotFoundError:
                self.tools_status[tool_name] = False
                print(f"{Fore.RED}[✗] {tool_name} - Not found{Style.RESET_ALL}")
        
        print()
    
    def setup_output_directory(self):
        """Create output directory structure"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(f"results/{self.target}_{timestamp}")
        
        directories = [
            "subdomains",
            "urls",
            "endpoints",
            "screenshots",
            "vulnerabilities",
            "ports",
            "javascript",
            "api",
            "cloud",
            "reports"
        ]
        
        for directory in directories:
            (self.output_dir / directory).mkdir(parents=True, exist_ok=True)
        
        print(f"{Fore.CYAN}[*] Output directory created: {self.output_dir}{Style.RESET_ALL}")
    
    def run_subdomain_enumeration(self):
        """Run comprehensive subdomain enumeration"""
        print(f"\n{Fore.YELLOW}[*] Starting Subdomain Enumeration...{Style.RESET_ALL}")
        
        subdomain_file = self.output_dir / "subdomains" / "all_subdomains.txt"
        temp_files = []
        
        # Amass
        if self.tools_status.get('amass'):
            print(f"{Fore.CYAN}[*] Running Amass...{Style.RESET_ALL}")
            amass_file = self.output_dir / "subdomains" / "amass.txt"
            temp_files.append(amass_file)
            subprocess.run([
                'amass', 'enum', '-d', self.target, '-o', str(amass_file)
            ], capture_output=True)
        
        # Subfinder
        if self.tools_status.get('subfinder'):
            print(f"{Fore.CYAN}[*] Running Subfinder...{Style.RESET_ALL}")
            subfinder_file = self.output_dir / "subdomains" / "subfinder.txt"
            temp_files.append(subfinder_file)
            subprocess.run([
                'subfinder', '-d', self.target, '-o', str(subfinder_file)
            ], capture_output=True)
        
        # Sublist3r
        if self.tools_status.get('sublist3r'):
            print(f"{Fore.CYAN}[*] Running Sublist3r...{Style.RESET_ALL}")
            sublist3r_file = self.output_dir / "subdomains" / "sublist3r.txt"
            temp_files.append(sublist3r_file)
            subprocess.run([
                'sublist3r', '-d', self.target, '-o', str(sublist3r_file)
            ], capture_output=True)
        
        # Assetfinder
        if self.tools_status.get('assetfinder'):
            print(f"{Fore.CYAN}[*] Running Assetfinder...{Style.RESET_ALL}")
            assetfinder_file = self.output_dir / "subdomains" / "assetfinder.txt"
            temp_files.append(assetfinder_file)
            with open(assetfinder_file, 'w') as f:
                subprocess.run(['assetfinder', self.target], stdout=f, capture_output=False)
        
        # Findomain
        if self.tools_status.get('findomain'):
            print(f"{Fore.CYAN}[*] Running Findomain...{Style.RESET_ALL}")
            findomain_file = self.output_dir / "subdomains" / "findomain.txt"
            temp_files.append(findomain_file)
            subprocess.run([
                'findomain', '-t', self.target, '-o'
            ], cwd=str(self.output_dir / "subdomains"), capture_output=True)
        
        # Combine and deduplicate subdomains
        all_subdomains = set()
        for temp_file in temp_files:
            if temp_file.exists():
                with open(temp_file, 'r') as f:
                    for line in f:
                        subdomain = line.strip()
                        if subdomain and subdomain != self.target:
                            all_subdomains.add(subdomain)
        
        # Write combined results
        with open(subdomain_file, 'w') as f:
            for subdomain in sorted(all_subdomains):
                f.write(f"{subdomain}\n")
        
        self.results['subdomains'] = len(all_subdomains)
        print(f"{Fore.GREEN}[✓] Found {len(all_subdomains)} unique subdomains{Style.RESET_ALL}")
        
        return subdomain_file
    
    def run_url_discovery(self, subdomains_file):
        """Discover URLs using multiple tools"""
        print(f"\n{Fore.YELLOW}[*] Starting URL Discovery...{Style.RESET_ALL}")
        
        urls_file = self.output_dir / "urls" / "all_urls.txt"
        all_urls = set()
        
        # Read subdomains
        with open(subdomains_file, 'r') as f:
            subdomains = [line.strip() for line in f if line.strip()]
        
        # Waybackurls
        if self.tools_status.get('waybackurls'):
            print(f"{Fore.CYAN}[*] Running Waybackurls...{Style.RESET_ALL}")
            for subdomain in subdomains[:10]:  # Limit to first 10 for speed
                try:
                    result = subprocess.run(
                        ['waybackurls', subdomain],
                        capture_output=True, text=True, timeout=60
                    )
                    for url in result.stdout.split('\n'):
                        if url.strip():
                            all_urls.add(url.strip())
                except subprocess.TimeoutExpired:
                    continue
        
        # GAU (GetAllUrls)
        if self.tools_status.get('gau'):
            print(f"{Fore.CYAN}[*] Running GAU...{Style.RESET_ALL}")
            for subdomain in subdomains[:10]:
                try:
                    result = subprocess.run(
                        ['gau', subdomain],
                        capture_output=True, text=True, timeout=60
                    )
                    for url in result.stdout.split('\n'):
                        if url.strip():
                            all_urls.add(url.strip())
                except subprocess.TimeoutExpired:
                    continue
        
        # Katana
        if self.tools_status.get('katana'):
            print(f"{Fore.CYAN}[*] Running Katana...{Style.RESET_ALL}")
            katana_file = self.output_dir / "urls" / "katana.txt"
            subprocess.run([
                'katana', '-u', str(subdomains_file), '-o', str(katana_file)
            ], capture_output=True)
            
            if katana_file.exists():
                with open(katana_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            all_urls.add(line.strip())
        
        # Write all URLs
        with open(urls_file, 'w') as f:
            for url in sorted(all_urls):
                f.write(f"{url}\n")
        
        self.results['urls'] = len(all_urls)
        print(f"{Fore.GREEN}[✓] Found {len(all_urls)} URLs{Style.RESET_ALL}")
        
        return urls_file
    
    def run_endpoint_discovery(self, urls_file):
        """Discover API and JS endpoints"""
        print(f"\n{Fore.YELLOW}[*] Starting Endpoint Discovery...{Style.RESET_ALL}")
        
        # GF patterns for endpoint discovery
        if self.tools_status.get('gf'):
            patterns = ['api', 'json', 'js', 'redirect', 'sql', 'ssrf', 'xss']
            
            for pattern in patterns:
                print(f"{Fore.CYAN}[*] Running GF pattern: {pattern}...{Style.RESET_ALL}")
                output_file = self.output_dir / "endpoints" / f"{pattern}_endpoints.txt"
                
                with open(urls_file, 'r') as f:
                    subprocess.run(
                        ['gf', pattern],
                        stdin=f, stdout=open(output_file, 'w'),
                        capture_output=False
                    )
        
        # JavaScript file analysis
        js_urls_file = self.output_dir / "javascript" / "js_files.txt"
        api_endpoints_file = self.output_dir / "api" / "api_endpoints.txt"
        
        js_urls = []
        api_endpoints = []
        
        with open(urls_file, 'r') as f:
            for url in f:
                url = url.strip()
                if url.endswith('.js'):
                    js_urls.append(url)
                elif '/api/' in url or url.endswith('/api'):
                    api_endpoints.append(url)
        
        # Write JS files
        with open(js_urls_file, 'w') as f:
            for js_url in js_urls:
                f.write(f"{js_url}\n")
        
        # Write API endpoints
        with open(api_endpoints_file, 'w') as f:
            for api_url in api_endpoints:
                f.write(f"{api_url}\n")
        
        self.results['js_files'] = len(js_urls)
        self.results['api_endpoints'] = len(api_endpoints)
        
        print(f"{Fore.GREEN}[✓] Found {len(js_urls)} JavaScript files{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(api_endpoints)} API endpoints{Style.RESET_ALL}")
    
    def run_cloud_discovery(self, subdomains_file):
        """Discover cloud services and storage"""
        print(f"\n{Fore.YELLOW}[*] Starting Cloud Service Discovery...{Style.RESET_ALL}")
        
        cloud_patterns = [
            's3.amazonaws.com',
            'amazonaws.com',
            'blob.core.windows.net',
            'storage.googleapis.com',
            'firebaseio.com',
            'cloudfront.net',
            'azurewebsites.net',
            'herokuapp.com'
        ]
        
        cloud_services = []
        
        with open(subdomains_file, 'r') as f:
            subdomains = [line.strip() for line in f]
        
        for subdomain in subdomains:
            for pattern in cloud_patterns:
                if pattern in subdomain:
                    cloud_services.append(subdomain)
        
        cloud_file = self.output_dir / "cloud" / "cloud_services.txt"
        with open(cloud_file, 'w') as f:
            for service in cloud_services:
                f.write(f"{service}\n")
        
        self.results['cloud_services'] = len(cloud_services)
        print(f"{Fore.GREEN}[✓] Found {len(cloud_services)} cloud services{Style.RESET_ALL}")
    
    def run_alive_check(self, subdomains_file):
        """Check which subdomains are alive"""
        print(f"\n{Fore.YELLOW}[*] Checking alive subdomains...{Style.RESET_ALL}")
        
        if self.tools_status.get('httpx'):
            alive_file = self.output_dir / "subdomains" / "alive_subdomains.txt"
            subprocess.run([
                'httpx', '-l', str(subdomains_file), '-o', str(alive_file),
                '-silent', '-status-code', '-title'
            ], capture_output=True)
            
            if alive_file.exists():
                with open(alive_file, 'r') as f:
                    alive_count = len(f.readlines())
                self.results['alive_subdomains'] = alive_count
                print(f"{Fore.GREEN}[✓] Found {alive_count} alive subdomains{Style.RESET_ALL}")
    
    def generate_report(self):
        """Generate final report"""
        print(f"\n{Fore.YELLOW}[*] Generating final report...{Style.RESET_ALL}")
        
        report_file = self.output_dir / "reports" / "final_report.json"
        report_data = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'results': self.results,
            'output_directory': str(self.output_dir)
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Text report
        text_report = self.output_dir / "reports" / "summary.txt"
        with open(text_report, 'w') as f:
            f.write(f"ReconXploit Reconnaissance Report\n")
            f.write(f"{'=' * 40}\n\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Results Summary:\n")
            f.write(f"{'─' * 20}\n")
            
            for key, value in self.results.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        print(f"{Fore.GREEN}[✓] Report generated: {report_file}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Summary saved: {text_report}{Style.RESET_ALL}")
    
    def run_reconnaissance(self, target, quick=False):
        """Main reconnaissance workflow"""
        self.target = target
        self.setup_output_directory()
        
        start_time = time.time()
        
        try:
            # Check tools
            self.check_tools()
            
            # Run subdomain enumeration
            subdomains_file = self.run_subdomain_enumeration()
            
            if not quick:
                # Run URL discovery
                urls_file = self.run_url_discovery(subdomains_file)
                
                # Run endpoint discovery
                self.run_endpoint_discovery(urls_file)
                
                # Run cloud discovery
                self.run_cloud_discovery(subdomains_file)
            
            # Check alive subdomains
            self.run_alive_check(subdomains_file)
            
            # Generate report
            self.generate_report()
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Reconnaissance completed in {duration:.2f} seconds{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Results saved to: {self.output_dir}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] Reconnaissance interrupted by user{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error during reconnaissance: {str(e)}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="ReconXploit - Advanced Reconnaissance Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 reconxploit.py -d example.com
  python3 reconxploit.py -d example.com --quick
  python3 reconxploit.py -d example.com -o /custom/output
  python3 reconxploit.py --check-tools
        """
    )
    
    parser.add_argument('-d', '--domain', 
                       help='Target domain for reconnaissance',
                       required=False)
    
    parser.add_argument('-o', '--output',
                       help='Custom output directory',
                       default='results')
    
    parser.add_argument('--quick',
                       action='store_true',
                       help='Quick scan (subdomains only)')
    
    parser.add_argument('--check-tools',
                       action='store_true',
                       help='Check tool availability and exit')
    
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Create ReconXploit instance
    reconxploit = ReconXploit()
    
    # Display banner
    reconxploit.display_banner()
    
    # Check tools only
    if args.check_tools:
        reconxploit.check_tools()
        return
    
    # Validate domain
    if not args.domain:
        print(f"{Fore.RED}[!] Please specify a target domain with -d/--domain{Style.RESET_ALL}")
        parser.print_help()
        return
    
    # Run reconnaissance
    reconxploit.run_reconnaissance(args.domain, args.quick)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Program interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
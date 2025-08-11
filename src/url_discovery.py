#!/usr/bin/env python3
"""
URL Discovery Module for ReconXploit
Comprehensive URL and endpoint discovery
"""

import os
import re
import subprocess
import threading
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

class URLDiscovery:
    def __init__(self, target, subdomains_file, output_dir):
        self.target = target
        self.subdomains_file = Path(subdomains_file)
        self.output_dir = Path(output_dir)
        self.urls = set()
        self.js_files = set()
        self.api_endpoints = set()
        self.subdomains = []
        
        # Load subdomains
        if self.subdomains_file.exists():
            with open(self.subdomains_file, 'r') as f:
                self.subdomains = [line.strip() for line in f if line.strip()]
    
    def run_waybackurls(self):
        """Use waybackurls to discover historical URLs"""
        print(f"{Fore.CYAN}[*] Running waybackurls...{Style.RESET_ALL}")
        
        wayback_file = self.output_dir / "wayback_urls.txt"
        all_urls = set()
        
        for subdomain in self.subdomains[:20]:  # Limit for performance
            try:
                result = subprocess.run([
                    'waybackurls', subdomain
                ], capture_output=True, text=True, timeout=60)
                
                for url in result.stdout.split('\n'):
                    url = url.strip()
                    if url and self.is_valid_url(url):
                        all_urls.add(url)
                        self.categorize_url(url)
                        
            except subprocess.TimeoutExpired:
                print(f"{Fore.YELLOW}[!] Waybackurls timeout for {subdomain}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Waybackurls error for {subdomain}: {str(e)}{Style.RESET_ALL}")
        
        # Save wayback URLs
        with open(wayback_file, 'w') as f:
            for url in sorted(all_urls):
                f.write(f"{url}\n")
        
        self.urls.update(all_urls)
    
    def run_gau(self):
        """Use GAU (GetAllUrls) to discover URLs"""
        print(f"{Fore.CYAN}[*] Running GAU...{Style.RESET_ALL}")
        
        gau_file = self.output_dir / "gau_urls.txt"
        all_urls = set()
        
        for subdomain in self.subdomains[:20]:  # Limit for performance
            try:
                result = subprocess.run([
                    'gau', subdomain
                ], capture_output=True, text=True, timeout=60)
                
                for url in result.stdout.split('\n'):
                    url = url.strip()
                    if url and self.is_valid_url(url):
                        all_urls.add(url)
                        self.categorize_url(url)
                        
            except subprocess.TimeoutExpired:
                print(f"{Fore.YELLOW}[!] GAU timeout for {subdomain}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] GAU error for {subdomain}: {str(e)}{Style.RESET_ALL}")
        
        # Save GAU URLs
        with open(gau_file, 'w') as f:
            for url in sorted(all_urls):
                f.write(f"{url}\n")
        
        self.urls.update(all_urls)
    
    def run_katana(self):
        """Use Katana for crawling and URL discovery"""
        print(f"{Fore.CYAN}[*] Running Katana crawler...{Style.RESET_ALL}")
        
        katana_file = self.output_dir / "katana_urls.txt"
        
        # Create temporary subdomain file for katana
        temp_subs_file = self.output_dir / "temp_subdomains.txt"
        with open(temp_subs_file, 'w') as f:
            for subdomain in self.subdomains[:10]:  # Limit for performance
                f.write(f"https://{subdomain}\n")
                f.write(f"http://{subdomain}\n")
        
        try:
            subprocess.run([
                'katana', '-list', str(temp_subs_file),
                '-d', '3', '-ps', '-pss', 'waybackarchive,commoncrawl,alienvault',
                '-o', str(katana_file)
            ], capture_output=True, timeout=300)
            
            if katana_file.exists():
                with open(katana_file, 'r') as f:
                    for line in f:
                        url = line.strip()
                        if url and self.is_valid_url(url):
                            self.urls.add(url)
                            self.categorize_url(url)
            
            # Clean up temp file
            temp_subs_file.unlink()
            
        except subprocess.TimeoutExpired:
            print(f"{Fore.YELLOW}[!] Katana timeout{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Katana error: {str(e)}{Style.RESET_ALL}")
    
    def run_gospider(self):
        """Use gospider for web crawling"""
        print(f"{Fore.CYAN}[*] Running gospider...{Style.RESET_ALL}")
        
        gospider_dir = self.output_dir / "gospider"
        gospider_dir.mkdir(exist_ok=True)
        
        for subdomain in self.subdomains[:5]:  # Limit for performance
            try:
                subprocess.run([
                    'gospider', '-s', f"https://{subdomain}",
                    '-d', '2', '-c', '10', '-t', '20',
                    '--sitemap', '--robots',
                    '-o', str(gospider_dir)
                ], capture_output=True, timeout=120)
                
            except subprocess.TimeoutExpired:
                print(f"{Fore.YELLOW}[!] Gospider timeout for {subdomain}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Gospider error for {subdomain}: {str(e)}{Style.RESET_ALL}")
        
        # Parse gospider results
        for result_file in gospider_dir.glob("*.txt"):
            with open(result_file, 'r') as f:
                for line in f:
                    if line.startswith('[url]'):
                        url = line.replace('[url] - ', '').strip()
                        if self.is_valid_url(url):
                            self.urls.add(url)
                            self.categorize_url(url)
    
    def discover_common_paths(self):
        """Discover common paths on alive subdomains"""
        print(f"{Fore.CYAN}[*] Discovering common paths...{Style.RESET_ALL}")
        
        common_paths = [
            '/robots.txt', '/sitemap.xml', '/.well-known/security.txt',
            '/api', '/api/v1', '/api/v2', '/admin', '/login',
            '/swagger', '/swagger.json', '/swagger-ui', '/docs',
            '/graphql', '/debug', '/.env', '/config.json',
            '/backup', '/test', '/dev', '/staging'
        ]
        
        alive_subdomains = []
        
        # Get alive subdomains
        alive_file = self.output_dir.parent / "subdomains" / "alive_subdomains.txt"
        if alive_file.exists():
            with open(alive_file, 'r') as f:
                alive_subdomains = [line.strip() for line in f if line.strip()]
        
        def check_path(base_url, path):
            try:
                url = urljoin(base_url, path)
                response = requests.head(url, timeout=10, allow_redirects=True)
                if response.status_code in [200, 301, 302, 403]:
                    return url
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for base_url in alive_subdomains[:10]:  # Limit for performance
                for path in common_paths:
                    futures.append(executor.submit(check_path, base_url, path))
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.urls.add(result)
                    self.categorize_url(result)
    
    def extract_js_endpoints(self):
        """Extract endpoints from JavaScript files"""
        print(f"{Fore.CYAN}[*] Extracting endpoints from JavaScript files...{Style.RESET_ALL}")
        
        endpoint_patterns = [
            r'["\']([a-zA-Z0-9_\-/\.]*?/api/[a-zA-Z0-9_\-/\.]*?)["\']',
            r'["\']([a-zA-Z0-9_\-/\.]*?\.json)["\']',
            r'["\']([a-zA-Z0-9_\-/\.]*?\.xml)["\']',
            r'["\']([a-zA-Z0-9_\-/\.]*?/v[0-9]+/[a-zA-Z0-9_\-/\.]*?)["\']',
            r'["\']([a-zA-Z0-9_\-/\.]*?/admin[a-zA-Z0-9_\-/\.]*?)["\']',
            r'["\']([a-zA-Z0-9_\-/\.]*?/graphql[a-zA-Z0-9_\-/\.]*?)["\']'
        ]
        
        def analyze_js_file(js_url):
            try:
                response = requests.get(js_url, timeout=15)
                if response.status_code == 200:
                    content = response.text
                    
                    for pattern in endpoint_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            if match.startswith('/'):
                                # Construct full URL
                                parsed_js_url = urlparse(js_url)
                                full_url = f"{parsed_js_url.scheme}://{parsed_js_url.netloc}{match}"
                                self.api_endpoints.add(full_url)
            except:
                pass
        
        # Analyze JavaScript files in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(analyze_js_file, js_url) for js_url in list(self.js_files)[:50]]
            
            for future in as_completed(futures):
                future.result()
    
    def categorize_url(self, url):
        """Categorize URL into different types"""
        url_lower = url.lower()
        
        # JavaScript files
        if url_lower.endswith('.js') or '/js/' in url_lower:
            self.js_files.add(url)
        
        # API endpoints
        if any(pattern in url_lower for pattern in ['/api/', '/graphql', '.json', '/v1/', '/v2/', '/v3/']):
            self.api_endpoints.add(url)
    
    def is_valid_url(self, url):
        """Check if URL is valid and relevant"""
        if not url or len(url) > 2000:
            return False
        
        # Filter out common unwanted extensions
        unwanted_extensions = ['.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', 
                             '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.mp3', '.pdf']
        
        for ext in unwanted_extensions:
            if url.lower().endswith(ext):
                return False
        
        # Must be related to target domain
        return self.target in url
    
    def save_results(self):
        """Save URL discovery results"""
        # Save all URLs
        all_urls_file = self.output_dir / "all_urls.txt"
        with open(all_urls_file, 'w') as f:
            for url in sorted(self.urls):
                f.write(f"{url}\n")
        
        # Save JavaScript files
        js_files_file = self.output_dir / "js_files.txt"
        with open(js_files_file, 'w') as f:
            for js_url in sorted(self.js_files):
                f.write(f"{js_url}\n")
        
        # Save API endpoints
        api_endpoints_file = self.output_dir / "api_endpoints.txt"
        with open(api_endpoints_file, 'w') as f:
            for api_url in sorted(self.api_endpoints):
                f.write(f"{api_url}\n")
        
        print(f"{Fore.GREEN}[✓] Found {len(self.urls)} total URLs{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(self.js_files)} JavaScript files{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(self.api_endpoints)} API endpoints{Style.RESET_ALL}")
        
        return len(self.urls), len(self.js_files), len(self.api_endpoints)
    
    def run_all(self):
        """Run all URL discovery techniques"""
        print(f"{Fore.YELLOW}[*] Starting comprehensive URL discovery...{Style.RESET_ALL}")
        
        # Create threads for parallel execution
        threads = []
        
        methods = [
            self.run_waybackurls,
            self.run_gau,
            self.run_katana,
            self.run_gospider
        ]
        
        for method in methods:
            thread = threading.Thread(target=method)
            threads.append(thread)
            thread.start()
        
        # Wait for all methods to complete
        for thread in threads:
            thread.join()
        
        # Sequential operations
        self.discover_common_paths()
        self.extract_js_endpoints()
        
        # Save results
        return self.save_results()
#!/usr/bin/env python3
"""
Subdomain Enumeration Module for ReconXploit
Advanced subdomain discovery with multiple techniques
"""

import os
import subprocess
import threading
import dns.resolver
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

class SubdomainEnumerator:
    def __init__(self, target, output_dir):
        self.target = target
        self.output_dir = Path(output_dir)
        self.subdomains = set()
        self.alive_subdomains = set()
        
    def run_amass(self):
        """Run Amass subdomain enumeration"""
        print(f"{Fore.CYAN}[*] Running Amass for {self.target}...{Style.RESET_ALL}")
        
        amass_file = self.output_dir / "amass_subdomains.txt"
        try:
            subprocess.run([
                'amass', 'enum', '-d', self.target, 
                '-brute', '-min-for-recursive', '2',
                '-o', str(amass_file)
            ], capture_output=True, timeout=300)
            
            if amass_file.exists():
                with open(amass_file, 'r') as f:
                    for line in f:
                        subdomain = line.strip()
                        if subdomain:
                            self.subdomains.add(subdomain)
        except subprocess.TimeoutExpired:
            print(f"{Fore.YELLOW}[!] Amass timeout for {self.target}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Amass error: {str(e)}{Style.RESET_ALL}")
    
    def run_subfinder(self):
        """Run Subfinder subdomain enumeration"""
        print(f"{Fore.CYAN}[*] Running Subfinder for {self.target}...{Style.RESET_ALL}")
        
        subfinder_file = self.output_dir / "subfinder_subdomains.txt"
        try:
            subprocess.run([
                'subfinder', '-d', self.target, '-all',
                '-o', str(subfinder_file)
            ], capture_output=True, timeout=180)
            
            if subfinder_file.exists():
                with open(subfinder_file, 'r') as f:
                    for line in f:
                        subdomain = line.strip()
                        if subdomain:
                            self.subdomains.add(subdomain)
        except subprocess.TimeoutExpired:
            print(f"{Fore.YELLOW}[!] Subfinder timeout for {self.target}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Subfinder error: {str(e)}{Style.RESET_ALL}")
    
    def run_assetfinder(self):
        """Run Assetfinder subdomain enumeration"""
        print(f"{Fore.CYAN}[*] Running Assetfinder for {self.target}...{Style.RESET_ALL}")
        
        try:
            result = subprocess.run([
                'assetfinder', '--subs-only', self.target
            ], capture_output=True, text=True, timeout=120)
            
            for line in result.stdout.split('\n'):
                subdomain = line.strip()
                if subdomain:
                    self.subdomains.add(subdomain)
        except subprocess.TimeoutExpired:
            print(f"{Fore.YELLOW}[!] Assetfinder timeout for {self.target}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Assetfinder error: {str(e)}{Style.RESET_ALL}")
    
    def run_findomain(self):
        """Run Findomain subdomain enumeration"""
        print(f"{Fore.CYAN}[*] Running Findomain for {self.target}...{Style.RESET_ALL}")
        
        try:
            result = subprocess.run([
                'findomain', '-t', self.target, '-q'
            ], capture_output=True, text=True, timeout=120)
            
            for line in result.stdout.split('\n'):
                subdomain = line.strip()
                if subdomain:
                    self.subdomains.add(subdomain)
        except subprocess.TimeoutExpired:
            print(f"{Fore.YELLOW}[!] Findomain timeout for {self.target}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Findomain error: {str(e)}{Style.RESET_ALL}")
    
    def certificate_transparency_search(self):
        """Search certificate transparency logs"""
        print(f"{Fore.CYAN}[*] Searching Certificate Transparency logs...{Style.RESET_ALL}")
        
        try:
            # crt.sh search
            url = f"https://crt.sh/?q=%.{self.target}&output=json"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                for cert in data:
                    name_value = cert.get('name_value', '')
                    for domain in name_value.split('\n'):
                        domain = domain.strip()
                        if domain and self.target in domain:
                            self.subdomains.add(domain)
        except Exception as e:
            print(f"{Fore.RED}[!] Certificate Transparency search error: {str(e)}{Style.RESET_ALL}")
    
    def bruteforce_subdomains(self, wordlist_path=None):
        """Bruteforce subdomains using wordlist"""
        if not wordlist_path:
            wordlist_path = Path("wordlists/subdomains-top1million-5000.txt")
        
        if not wordlist_path.exists():
            print(f"{Fore.YELLOW}[!] Wordlist not found: {wordlist_path}{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}[*] Bruteforcing subdomains with wordlist...{Style.RESET_ALL}")
        
        with open(wordlist_path, 'r') as f:
            subdomains = [f"{line.strip()}.{self.target}" for line in f if line.strip()]
        
        def check_subdomain(subdomain):
            try:
                dns.resolver.resolve(subdomain, 'A')
                return subdomain
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(check_subdomain, sub) for sub in subdomains[:1000]]
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.subdomains.add(result)
    
    def check_subdomain_alive(self, subdomain):
        """Check if subdomain is alive"""
        try:
            # Try HTTP first
            response = requests.head(f"http://{subdomain}", timeout=5, allow_redirects=True)
            if response.status_code < 400:
                self.alive_subdomains.add(f"http://{subdomain}")
                return True
        except:
            pass
        
        try:
            # Try HTTPS
            response = requests.head(f"https://{subdomain}", timeout=5, allow_redirects=True)
            if response.status_code < 400:
                self.alive_subdomains.add(f"https://{subdomain}")
                return True
        except:
            pass
        
        return False
    
    def check_alive_subdomains(self):
        """Check which subdomains are alive"""
        print(f"{Fore.CYAN}[*] Checking alive subdomains...{Style.RESET_ALL}")
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.check_subdomain_alive, sub) for sub in self.subdomains]
            
            for future in as_completed(futures):
                future.result()  # Wait for completion
    
    def save_results(self):
        """Save enumeration results"""
        # Save all subdomains
        all_subdomains_file = self.output_dir / "all_subdomains.txt"
        with open(all_subdomains_file, 'w') as f:
            for subdomain in sorted(self.subdomains):
                f.write(f"{subdomain}\n")
        
        # Save alive subdomains
        alive_subdomains_file = self.output_dir / "alive_subdomains.txt"
        with open(alive_subdomains_file, 'w') as f:
            for subdomain in sorted(self.alive_subdomains):
                f.write(f"{subdomain}\n")
        
        print(f"{Fore.GREEN}[✓] Found {len(self.subdomains)} total subdomains{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(self.alive_subdomains)} alive subdomains{Style.RESET_ALL}")
        
        return len(self.subdomains), len(self.alive_subdomains)
    
    def run_all(self):
        """Run all subdomain enumeration techniques"""
        print(f"{Fore.YELLOW}[*] Starting comprehensive subdomain enumeration for {self.target}...{Style.RESET_ALL}")
        
        # Create threads for parallel execution
        threads = []
        
        # Passive enumeration
        for method in [self.run_amass, self.run_subfinder, self.run_assetfinder, 
                      self.run_findomain, self.certificate_transparency_search]:
            thread = threading.Thread(target=method)
            threads.append(thread)
            thread.start()
        
        # Wait for all passive enumeration to complete
        for thread in threads:
            thread.join()
        
        # Active enumeration
        self.bruteforce_subdomains()
        
        # Check alive subdomains
        self.check_alive_subdomains()
        
        # Save results
        return self.save_results()
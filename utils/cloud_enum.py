#!/usr/bin/env python3
"""
Cloud Services Enumeration Utility for ReconXploit
Discover cloud storage, CDN, and other cloud services
"""

import re
import requests
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

class CloudEnumerator:
    def __init__(self, target, subdomains_file, output_dir):
        self.target = target
        self.subdomains_file = Path(subdomains_file)
        self.output_dir = Path(output_dir)
        self.cloud_services = set()
        self.s3_buckets = set()
        self.azure_blobs = set()
        self.gcp_buckets = set()
        self.cdn_services = set()
        
        # Load subdomains
        self.subdomains = []
        if self.subdomains_file.exists():
            with open(self.subdomains_file, 'r') as f:
                self.subdomains = [line.strip() for line in f if line.strip()]
    
    def identify_cloud_services(self):
        """Identify cloud services from subdomains"""
        print(f"{Fore.CYAN}[*] Identifying cloud services...{Style.RESET_ALL}")
        
        cloud_patterns = {
            'aws_s3': [
                r'.*\.s3\.amazonaws\.com',
                r'.*\.s3\..*\.amazonaws\.com',
                r'.*\.s3-.*\.amazonaws\.com'
            ],
            'aws_cloudfront': [
                r'.*\.cloudfront\.net'
            ],
            'aws_elb': [
                r'.*\.elb\.amazonaws\.com',
                r'.*\.elb\..*\.amazonaws\.com'
            ],
            'azure_blob': [
                r'.*\.blob\.core\.windows\.net'
            ],
            'azure_cdn': [
                r'.*\.azureedge\.net'
            ],
            'gcp_storage': [
                r'.*\.storage\.googleapis\.com'
            ],
            'gcp_appengine': [
                r'.*\.appspot\.com'
            ],
            'cloudflare': [
                r'.*\.cloudflaressl\.com'
            ],
            'fastly': [
                r'.*\.fastly\.com'
            ],
            'github_pages': [
                r'.*\.github\.io'
            ],
            'heroku': [
                r'.*\.herokuapp\.com'
            ],
            'firebase': [
                r'.*\.firebaseio\.com',
                r'.*\.firebaseapp\.com'
            ]
        }
        
        for subdomain in self.subdomains:
            for service_type, patterns in cloud_patterns.items():
                for pattern in patterns:
                    if re.match(pattern, subdomain):
                        service_info = {
                            'subdomain': subdomain,
                            'service_type': service_type,
                            'pattern': pattern
                        }
                        self.cloud_services.add(f"{service_type}: {subdomain}")
                        
                        # Categorize specific services
                        if 's3' in service_type:
                            self.s3_buckets.add(subdomain)
                        elif 'azure' in service_type:
                            self.azure_blobs.add(subdomain)
                        elif 'gcp' in service_type:
                            self.gcp_buckets.add(subdomain)
                        elif any(cdn in service_type for cdn in ['cloudfront', 'cdn', 'fastly', 'cloudflare']):
                            self.cdn_services.add(subdomain)
    
    def enumerate_s3_buckets(self):
        """Enumerate AWS S3 buckets"""
        print(f"{Fore.CYAN}[*] Enumerating S3 buckets...{Style.RESET_ALL}")
        
        # Generate potential bucket names
        bucket_names = set()
        
        # Based on target domain
        domain_parts = self.target.split('.')
        base_name = domain_parts[0] if domain_parts else self.target
        
        common_prefixes = ['', 'www-', 'dev-', 'test-', 'prod-', 'staging-', 'backup-']
        common_suffixes = ['', '-backup', '-dev', '-test', '-prod', '-staging', '-assets', '-static']
        
        for prefix in common_prefixes:
            for suffix in common_suffixes:
                bucket_names.add(f"{prefix}{base_name}{suffix}")
                bucket_names.add(f"{prefix}{self.target.replace('.', '-')}{suffix}")
        
        # Check bucket accessibility
        def check_s3_bucket(bucket_name):
            try:
                # Check if bucket exists and is accessible
                url = f"https://{bucket_name}.s3.amazonaws.com"
                response = requests.head(url, timeout=10)
                
                if response.status_code == 200:
                    return f"Public: {bucket_name}"
                elif response.status_code == 403:
                    return f"Private: {bucket_name}"
                elif response.status_code == 404:
                    return None
                else:
                    return f"Unknown: {bucket_name} (Status: {response.status_code})"
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_s3_bucket, bucket) for bucket in bucket_names]
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.s3_buckets.add(result)
    
    def enumerate_azure_blobs(self):
        """Enumerate Azure Blob storage"""
        print(f"{Fore.CYAN}[*] Enumerating Azure Blob storage...{Style.RESET_ALL}")
        
        # Generate potential storage account names
        storage_names = set()
        
        domain_parts = self.target.split('.')
        base_name = domain_parts[0] if domain_parts else self.target
        
        common_prefixes = ['', 'dev', 'test', 'prod', 'staging']
        common_suffixes = ['', 'storage', 'data', 'backup', 'assets']
        
        for prefix in common_prefixes:
            for suffix in common_suffixes:
                if prefix and suffix:
                    storage_names.add(f"{prefix}{base_name}{suffix}")
                elif prefix:
                    storage_names.add(f"{prefix}{base_name}")
                elif suffix:
                    storage_names.add(f"{base_name}{suffix}")
                else:
                    storage_names.add(base_name)
        
        def check_azure_storage(storage_name):
            try:
                url = f"https://{storage_name}.blob.core.windows.net"
                response = requests.head(url, timeout=10)
                
                if response.status_code in [200, 400]:  # 400 might indicate existing but restricted
                    return f"Azure: {storage_name}"
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_azure_storage, storage) for storage in storage_names]
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.azure_blobs.add(result)
    
    def enumerate_gcp_buckets(self):
        """Enumerate Google Cloud Platform buckets"""
        print(f"{Fore.CYAN}[*] Enumerating GCP buckets...{Style.RESET_ALL}")
        
        # Generate potential bucket names
        bucket_names = set()
        
        domain_parts = self.target.split('.')
        base_name = domain_parts[0] if domain_parts else self.target
        
        common_variations = [
            base_name,
            self.target.replace('.', '-'),
            f"{base_name}-backup",
            f"{base_name}-assets",
            f"{base_name}-static",
            f"www-{base_name}",
            f"{base_name}-prod",
            f"{base_name}-dev"
        ]
        
        bucket_names.update(common_variations)
        
        def check_gcp_bucket(bucket_name):
            try:
                url = f"https://storage.googleapis.com/{bucket_name}"
                response = requests.head(url, timeout=10)
                
                if response.status_code in [200, 403]:
                    return f"GCP: {bucket_name}"
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_gcp_bucket, bucket) for bucket in bucket_names]
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.gcp_buckets.add(result)
    
    def check_cdn_misconfigurations(self):
        """Check for CDN misconfigurations"""
        print(f"{Fore.CYAN}[*] Checking CDN misconfigurations...{Style.RESET_ALL}")
        
        for cdn_service in self.cdn_services:
            try:
                # Check for common CDN vulnerabilities
                response = requests.get(f"https://{cdn_service}", timeout=10, allow_redirects=False)
                
                # Check for cache poisoning indicators
                cache_headers = ['X-Cache', 'CF-Cache-Status', 'X-Served-By']
                for header in cache_headers:
                    if header in response.headers:
                        print(f"{Fore.YELLOW}[!] CDN Cache header found on {cdn_service}: {header}{Style.RESET_ALL}")
                
            except:
                continue
    
    def save_results(self):
        """Save cloud enumeration results"""
        # Save all cloud services
        cloud_services_file = self.output_dir / "cloud_services.txt"
        with open(cloud_services_file, 'w') as f:
            for service in sorted(self.cloud_services):
                f.write(f"{service}\n")
        
        # Save S3 buckets
        s3_buckets_file = self.output_dir / "s3_buckets.txt"
        with open(s3_buckets_file, 'w') as f:
            for bucket in sorted(self.s3_buckets):
                f.write(f"{bucket}\n")
        
        # Save Azure blobs
        azure_blobs_file = self.output_dir / "azure_blobs.txt"
        with open(azure_blobs_file, 'w') as f:
            for blob in sorted(self.azure_blobs):
                f.write(f"{blob}\n")
        
        # Save GCP buckets
        gcp_buckets_file = self.output_dir / "gcp_buckets.txt"
        with open(gcp_buckets_file, 'w') as f:
            for bucket in sorted(self.gcp_buckets):
                f.write(f"{bucket}\n")
        
        # Save CDN services
        cdn_services_file = self.output_dir / "cdn_services.txt"
        with open(cdn_services_file, 'w') as f:
            for cdn in sorted(self.cdn_services):
                f.write(f"{cdn}\n")
        
        print(f"{Fore.GREEN}[✓] Found {len(self.cloud_services)} cloud services{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(self.s3_buckets)} S3 buckets{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(self.azure_blobs)} Azure blobs{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(self.gcp_buckets)} GCP buckets{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(self.cdn_services)} CDN services{Style.RESET_ALL}")
        
        return {
            'cloud_services': len(self.cloud_services),
            's3_buckets': len(self.s3_buckets),
            'azure_blobs': len(self.azure_blobs),
            'gcp_buckets': len(self.gcp_buckets),
            'cdn_services': len(self.cdn_services)
        }
    
    def run_all(self):
        """Run all cloud enumeration techniques"""
        print(f"{Fore.YELLOW}[*] Starting comprehensive cloud service enumeration...{Style.RESET_ALL}")
        
        # Identify cloud services from subdomains
        self.identify_cloud_services()
        
        # Create threads for parallel enumeration
        threads = []
        
        methods = [
            self.enumerate_s3_buckets,
            self.enumerate_azure_blobs,
            self.enumerate_gcp_buckets,
            self.check_cdn_misconfigurations
        ]
        
        for method in methods:
            thread = threading.Thread(target=method)
            threads.append(thread)
            thread.start()
        
        # Wait for all methods to complete
        for thread in threads:
            thread.join()
        
        # Save results
        return self.save_results()
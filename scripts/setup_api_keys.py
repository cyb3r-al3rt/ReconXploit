#!/usr/bin/env python3
"""
ReconXploit v3.0 - Interactive API Key Setup
Product of Kernelpanic under infosbios.tech
"""

import os
import sys
import yaml
import getpass
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

class APIKeySetup:
    def __init__(self):
        self.config_dir = Path("config")
        self.api_keys_file = self.config_dir / "api_keys.yaml"

        self.services = {
            "shodan": {
                "name": "Shodan",
                "description": "Internet-connected device search engine",
                "url": "https://account.shodan.io/",
                "fields": ["api_key"]
            },
            "censys": {
                "name": "Censys",
                "description": "Internet scanning and threat intelligence",
                "url": "https://censys.io/account/api",
                "fields": ["api_id", "api_secret"]
            },
            "securitytrails": {
                "name": "SecurityTrails",
                "description": "DNS and domain intelligence",
                "url": "https://securitytrails.com/corp/api",
                "fields": ["api_key"]
            },
            "virustotal": {
                "name": "VirusTotal",
                "description": "File and URL analysis service",
                "url": "https://www.virustotal.com/gui/my-apikey",
                "fields": ["api_key"]
            },
            "github": {
                "name": "GitHub",
                "description": "Code repository and developer platform",
                "url": "https://github.com/settings/tokens",
                "fields": ["token"]
            }
        }

    def show_banner(self):
        print(Fore.CYAN + Style.BRIGHT + """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                 ReconXploit v3.0 - API Setup                 ║
    ║              Product of Kernelpanic under infosbios.tech     ║
    ╚═══════════════════════════════════════════════════════════════╝
        """)

    def setup_service(self, service_key, service_config):
        print(f"\n{Fore.BLUE}{'='*60}{Fore.RESET}")
        print(f"{Fore.CYAN}Setting up: {service_config['name']}{Fore.RESET}")
        print(f"{Fore.WHITE}Description: {service_config['description']}{Fore.RESET}")
        print(f"{Fore.YELLOW}API URL: {service_config['url']}{Fore.RESET}")
        print(f"{'='*60}")

        while True:
            choice = input(f"\nConfigure {service_config['name']}? (y/n/skip): ").lower().strip()
            if choice in ['y', 'yes']:
                break
            elif choice in ['n', 'no', 'skip']:
                return {}

        service_data = {}
        for field in service_config['fields']:
            while True:
                if 'secret' in field.lower() or 'token' in field.lower() or 'key' in field.lower():
                    value = getpass.getpass(f"Enter {field}: ")
                else:
                    value = input(f"Enter {field}: ").strip()

                if value:
                    service_data[field] = value
                    break
                else:
                    print(f"{Fore.RED}This field is required. Please enter a value.{Fore.RESET}")

        return service_data

    def save_config(self, config):
        try:
            self.config_dir.mkdir(exist_ok=True)

            with open(self.api_keys_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)

            print(f"{Fore.GREEN}[INFO]{Fore.RESET} Configuration saved to: {self.api_keys_file}")

            os.chmod(self.api_keys_file, 0o600)
            print(f"{Fore.GREEN}[INFO]{Fore.RESET} File permissions set to 600 (owner read/write only)")

        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Fore.RESET} Failed to save configuration: {e}")

    def run_setup(self):
        self.show_banner()

        print(f"{Fore.WHITE}This script will help you configure API keys for ReconXploit.{Fore.RESET}")
        print(f"{Fore.WHITE}API keys enable additional features and data sources.{Fore.RESET}")
        print(f"{Fore.YELLOW}All API keys are optional but recommended for best results.{Fore.RESET}")

        input(f"\n{Fore.GREEN}Press Enter to continue...{Fore.RESET}")

        new_config = {}

        for service_key, service_config in self.services.items():
            service_data = self.setup_service(service_key, service_config)
            if service_data:
                new_config[service_key] = service_data

        if new_config:
            self.save_config(new_config)
            print(f"\n{Fore.GREEN}✓ API key setup completed successfully!{Fore.RESET}")
            print(f"{Fore.CYAN}[fsociety] The keys to the kingdom are now yours.{Fore.RESET}")
        else:
            print(f"\n{Fore.YELLOW}No API keys were configured.{Fore.RESET}")

if __name__ == "__main__":
    try:
        setup = APIKeySetup()
        setup.run_setup()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Setup interrupted by user{Fore.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Setup failed: {e}{Fore.RESET}")
        sys.exit(1)

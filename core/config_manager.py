#!/usr/bin/env python3
"""
ReconXploit v3.0 - Professional Configuration Manager
Product of Kernelpanic under infosbios.tech
"""

import yaml
from pathlib import Path
from typing import Dict, Any
import os

class ConfigManager:
    """Professional configuration management system"""

    def __init__(self):
        pass

    async def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load professional configuration from file"""

        config_file = Path(config_path)

        # Professional default configuration
        default_config = {
            "framework": {
                "version": "3.0.0",
                "edition": "Professional Edition",
                "author": "cyb3r-ssrf",
                "organization": "Kernelpanic",
                "website": "infosbios.tech"
            },
            "performance": {
                "threads": 50,
                "timeout": 30,
                "delay": 0,
                "rate_limit": 100,
                "max_subdomains": 1000,
                "max_urls": 500
            },
            "tools": {
                "subdomain_enumeration": {
                    "enabled": True,
                    "tools": ["subfinder", "assetfinder", "amass"],
                    "priority": ["subfinder", "assetfinder"]
                },
                "http_probing": {
                    "enabled": True,
                    "tools": ["httpx", "httprobe"],
                    "priority": ["httpx"]
                },
                "port_scanning": {
                    "enabled": True,
                    "tools": ["naabu", "nmap"],
                    "priority": ["naabu"]
                },
                "vulnerability_scanning": {
                    "enabled": True,
                    "tools": ["nuclei", "nikto"],
                    "priority": ["nuclei"]
                }
            },
            "output": {
                "formats": ["html", "json", "csv"],
                "directory": "results",
                "include_timestamp": True,
                "generate_summary": True
            },
            "security": {
                "safe_mode": True,
                "respect_robots_txt": True,
                "max_recursion_depth": 3,
                "blacklisted_extensions": [".exe", ".zip", ".rar"]
            },
            "reporting": {
                "include_charts": True,
                "detailed_analysis": True,
                "risk_assessment": True,
                "recommendations": True
            }
        }

        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = yaml.safe_load(f)

                if user_config:
                    # Merge with default config
                    merged_config = self._merge_configs(default_config, user_config)
                    print(f"\033[0;36m[CONFIG]\033[0m Loaded user configuration from {config_file}")
                    return merged_config
                else:
                    print(f"\033[0;33m[CONFIG]\033[0m Empty config file, using defaults")

            except yaml.YAMLError as e:
                print(f"\033[0;33m[WARNING]\033[0m Invalid YAML in config: {e}")
                print("\033[0;36m[INFO]\033[0m Using default configuration")
            except Exception as e:
                print(f"\033[0;33m[WARNING]\033[0m Failed to load config: {e}")
                print("\033[0;36m[INFO]\033[0m Using default configuration")
        else:
            print(f"\033[0;36m[CONFIG]\033[0m Using default professional configuration")

        return default_config

    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user configuration with default"""

        merged = default.copy()

        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value

        return merged

    def create_default_config(self, config_path: str):
        """Create default configuration file"""

        config_dir = Path(config_path).parent
        config_dir.mkdir(parents=True, exist_ok=True)

        default_yaml = """# ReconXploit v3.0 Professional Configuration
# Product of Kernelpanic under infosbios.tech

framework:
  version: "3.0.0"
  edition: "Professional Edition"
  author: "cyb3r-ssrf"

performance:
  threads: 50              # Number of concurrent threads
  timeout: 30              # Timeout per operation (seconds)  
  delay: 0                 # Delay between requests (seconds)
  rate_limit: 100          # Requests per minute limit
  max_subdomains: 1000     # Maximum subdomains to process
  max_urls: 500            # Maximum URLs to analyze

tools:
  subdomain_enumeration:
    enabled: true
    tools: ["subfinder", "assetfinder", "amass"]
    priority: ["subfinder", "assetfinder"]

  http_probing:
    enabled: true
    tools: ["httpx", "httprobe"] 
    priority: ["httpx"]

  port_scanning:
    enabled: true
    tools: ["naabu", "nmap"]
    priority: ["naabu"]

  vulnerability_scanning:
    enabled: true
    tools: ["nuclei", "nikto"]
    priority: ["nuclei"]

output:
  formats: ["html", "json", "csv"]
  directory: "results"
  include_timestamp: true
  generate_summary: true

security:
  safe_mode: true
  respect_robots_txt: true
  max_recursion_depth: 3
  blacklisted_extensions: [".exe", ".zip", ".rar"]

reporting:
  include_charts: true
  detailed_analysis: true
  risk_assessment: true
  recommendations: true
"""

        try:
            with open(config_path, 'w') as f:
                f.write(default_yaml)
            print(f"\033[0;32m[CONFIG]\033[0m Created default configuration at {config_path}")
        except Exception as e:
            print(f"\033[0;31m[ERROR]\033[0m Failed to create config file: {e}")

#!/usr/bin/env python3
"""
ReconXploit v3.0 - Configuration Manager
Product of Kernelpanic under infosbios.tech
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """Comprehensive configuration management system"""

    def __init__(self):
        self.default_config = self._get_default_config()
        self.api_keys_file = "config/api_keys.yaml"
        self.user_config_file = "config/user_config.yaml"

    def load_config(self, config_path: str = "config/config.yaml") -> Dict[str, Any]:
        """Load configuration with fallbacks and validation"""
        config_file = Path(config_path)

        # Start with default configuration
        config = self.default_config.copy()

        # Load main config file
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f) or {}
                config = self._deep_merge(config, file_config)
            except Exception as e:
                print(f"\033[0;33m[WARNING]\033[0m Failed to load config {config_path}: {e}")

        # Load API keys
        api_keys = self._load_api_keys()
        if api_keys:
            config['api_keys'] = api_keys

        # Load user-specific overrides
        user_config = self._load_user_config()
        if user_config:
            config = self._deep_merge(config, user_config)

        return self._validate_config(config)

    def save_config(self, config: Dict[str, Any], config_path: str = "config/config.yaml") -> bool:
        """Save configuration to file"""
        try:
            config_file = Path(config_path)
            config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False, indent=2)

            return True
        except Exception as e:
            print(f"\033[0;31m[ERROR]\033[0m Failed to save config: {e}")
            return False

    def _load_api_keys(self) -> Optional[Dict[str, str]]:
        """Load API keys from secure file"""
        api_keys_path = Path(self.api_keys_file)
        if not api_keys_path.exists():
            return None

        try:
            with open(api_keys_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"\033[0;33m[WARNING]\033[0m Failed to load API keys: {e}")
            return None

    def _load_user_config(self) -> Optional[Dict[str, Any]]:
        """Load user-specific configuration overrides"""
        user_config_path = Path(self.user_config_file)
        if not user_config_path.exists():
            return None

        try:
            with open(user_config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"\033[0;33m[WARNING]\033[0m Failed to load user config: {e}")
            return None

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries"""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration values"""
        # Ensure required sections exist
        required_sections = ['framework', 'tools', 'output', 'performance']
        for section in required_sections:
            if section not in config:
                config[section] = {}

        # Validate performance settings
        perf = config['performance']
        perf['threads'] = max(1, min(perf.get('threads', 50), 200))
        perf['timeout'] = max(5, min(perf.get('timeout', 30), 300))

        # Validate tool settings
        for category in config['tools']:
            tool_config = config['tools'][category]
            if 'enabled' not in tool_config:
                tool_config['enabled'] = True
            if 'timeout' not in tool_config:
                tool_config['timeout'] = config['performance']['timeout']

        return config

    def _get_default_config(self) -> Dict[str, Any]:
        """Return comprehensive default configuration"""
        return {
            'framework': {
                'version': '3.0.0',
                'name': 'ReconXploit',
                'author': 'cyb3r-ssrf',
                'organization': 'Kernelpanic',
                'website': 'infosbios.tech'
            },
            'performance': {
                'threads': 50,
                'timeout': 30,
                'delay': 0,
                'max_retries': 3,
                'rate_limit': 100
            },
            'output': {
                'format': 'html',
                'directory': 'results',
                'save_raw': True,
                'generate_summary': True,
                'include_screenshots': False,
                'timestamp_format': '%Y%m%d_%H%M%S'
            },
            'tools': {
                'subdomain_enumeration': {
                    'enabled': True,
                    'tools': ['subfinder', 'assetfinder'],
                    'timeout': 300,
                    'max_results': 10000,
                    'use_passive_sources': True,
                    'use_certificate_transparency': True
                },
                'live_host_detection': {
                    'enabled': True,
                    'tools': ['httpx'],
                    'timeout': 30,
                    'threads': 100,
                    'follow_redirects': True,
                    'verify_ssl': False,
                    'check_response_codes': [200, 301, 302, 403, 404]
                },
                'port_scanning': {
                    'enabled': True,
                    'tools': ['naabu', 'nmap'],
                    'timeout': 600,
                    'top_ports': 1000,
                    'scan_type': 'syn',
                    'exclude_ports': [],
                    'rate_limit': 1000
                },
                'content_discovery': {
                    'enabled': True,
                    'tools': ['feroxbuster', 'gobuster'],
                    'timeout': 900,
                    'wordlists': ['common.txt', 'directories.txt'],
                    'extensions': ['php', 'html', 'js', 'css', 'txt'],
                    'recursion_depth': 3,
                    'follow_redirects': True
                },
                'parameter_discovery': {
                    'enabled': True,
                    'tools': ['arjun', 'paramspider'],
                    'timeout': 300,
                    'methods': ['GET', 'POST'],
                    'wordlists': ['parameters.txt'],
                    'check_reflection': True
                },
                'vulnerability_scanning': {
                    'enabled': True,
                    'tools': ['nuclei'],
                    'timeout': 1800,
                    'templates': 'all',
                    'severity': ['critical', 'high', 'medium'],
                    'exclude_tags': ['dos'],
                    'update_templates': True
                }
            },
            'api_keys': {
                'shodan': '',
                'censys_id': '',
                'censys_secret': '',
                'virustotal': '',
                'github': '',
                'securitytrails': '',
                'chaos': ''
            },
            'wordlists': {
                'subdomain': [
                    'wordlists/subdomains/subdomains-top1million-5000.txt',
                    'wordlists/subdomains/fierce-hostlist.txt'
                ],
                'directory': [
                    'wordlists/directories/common.txt',
                    'wordlists/directories/big.txt'
                ],
                'parameters': [
                    'wordlists/parameters/common-parameters.txt'
                ]
            },
            'user_agent': 'ReconXploit/3.0 (+https://infosbios.tech)',
            'proxy': {
                'enabled': False,
                'http': '',
                'https': '',
                'socks': ''
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/reconxploit.log',
                'max_size': '100MB',
                'backup_count': 5,
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'notifications': {
                'enabled': False,
                'webhook_url': '',
                'slack_token': '',
                'discord_webhook': '',
                'email': {
                    'smtp_server': '',
                    'port': 587,
                    'username': '',
                    'password': '',
                    'from_addr': '',
                    'to_addr': ''
                }
            }
        }

    def get_tool_config(self, tool_category: str, tool_name: str = None) -> Dict[str, Any]:
        """Get configuration for specific tool category or tool"""
        config = self.load_config()

        if tool_category not in config['tools']:
            return {}

        tool_config = config['tools'][tool_category].copy()

        # Merge with global performance settings
        if 'timeout' not in tool_config:
            tool_config['timeout'] = config['performance']['timeout']
        if 'threads' not in tool_config:
            tool_config['threads'] = config['performance']['threads']

        return tool_config

    def is_tool_enabled(self, tool_category: str) -> bool:
        """Check if a tool category is enabled"""
        config = self.load_config()
        return config.get('tools', {}).get(tool_category, {}).get('enabled', True)

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service"""
        config = self.load_config()
        return config.get('api_keys', {}).get(service)

    def create_default_files(self) -> None:
        """Create default configuration files"""
        # Create directories
        for directory in ['config', 'logs', 'results', 'wordlists']:
            Path(directory).mkdir(exist_ok=True)

        # Create main config file
        config_file = Path('config/config.yaml')
        if not config_file.exists():
            self.save_config(self.default_config, str(config_file))

        # Create API keys template
        api_keys_file = Path(self.api_keys_file)
        if not api_keys_file.exists():
            api_keys_template = {
                '# API Keys Configuration': None,
                '# Add your API keys here for enhanced functionality': None,
                'shodan': 'your_shodan_api_key_here',
                'censys_id': 'your_censys_id_here',
                'censys_secret': 'your_censys_secret_here',
                'virustotal': 'your_virustotal_api_key_here',
                'github': 'your_github_token_here',
                'securitytrails': 'your_securitytrails_api_key_here',
                'chaos': 'your_chaos_api_key_here'
            }

            try:
                with open(api_keys_file, 'w') as f:
                    yaml.dump(api_keys_template, f, default_flow_style=False)
            except Exception as e:
                print(f"\033[0;33m[WARNING]\033[0m Failed to create API keys template: {e}")

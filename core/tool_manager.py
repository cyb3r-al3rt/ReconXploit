#!/usr/bin/env python3
"""
ReconXploit v3.0 - Comprehensive Tool Manager
Product of Kernelpanic under infosbios.tech
"""

import shutil
import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ToolManager:
    """Comprehensive tool management and verification system"""

    def __init__(self):
        self.go_bin_path = Path.home() / "go" / "bin"
        self.cargo_bin_path = Path.home() / ".cargo" / "bin"
        self.local_bin_path = Path("/usr/local/bin")

        # Tool categories and installation methods
        self.tool_definitions = {
            "go_tools": {
                "subfinder": {
                    "repo": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
                    "description": "Fast subdomain discovery tool",
                    "required": True
                },
                "httpx": {
                    "repo": "github.com/projectdiscovery/httpx/cmd/httpx@latest", 
                    "description": "Fast HTTP probing tool",
                    "required": True
                },
                "nuclei": {
                    "repo": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
                    "description": "Vulnerability scanner with templates",
                    "required": True
                },
                "naabu": {
                    "repo": "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
                    "description": "Fast port scanner",
                    "required": False,
                    "dependencies": ["libpcap-dev"],
                    "post_install": "sudo setcap cap_net_raw,cap_net_admin+eip $(which naabu)"
                },
                "katana": {
                    "repo": "github.com/projectdiscovery/katana/cmd/katana@latest",
                    "description": "Web crawling framework",
                    "required": False
                },
                "dnsx": {
                    "repo": "github.com/projectdiscovery/dnsx/cmd/dnsx@latest",
                    "description": "Fast DNS toolkit",
                    "required": False
                },
                "assetfinder": {
                    "repo": "github.com/tomnomnom/assetfinder@latest",
                    "description": "Find domains and subdomains",
                    "required": False
                },
                "gf": {
                    "repo": "github.com/tomnomnom/gf@latest",
                    "description": "Grep-friendly pattern matcher",
                    "required": False
                },
                "waybackurls": {
                    "repo": "github.com/tomnomnom/waybackurls@latest",
                    "description": "Fetch URLs from Wayback Machine",
                    "required": False
                },
                "gau": {
                    "repo": "github.com/lc/gau/v2/cmd/gau@latest", 
                    "description": "Get All URLs",
                    "required": False
                },
                "ffuf": {
                    "repo": "github.com/ffuf/ffuf@latest",
                    "description": "Fast web fuzzer",
                    "required": False
                },
                "hakrawler": {
                    "repo": "github.com/hakluke/hakrawler@latest",
                    "description": "Web crawler for pentesters",
                    "required": False
                },
                "dalfox": {
                    "repo": "github.com/hahwul/dalfox/v2@latest",
                    "description": "XSS parameter analysis tool", 
                    "required": False
                },
                "anew": {
                    "repo": "github.com/tomnomnom/anew@latest",
                    "description": "Add new lines to files",
                    "required": False
                },
                "shuffledns": {
                    "repo": "github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest",
                    "description": "DNS brute-force tool",
                    "required": False
                }
            },
            "rust_tools": {
                "feroxbuster": {
                    "cargo_name": "feroxbuster",
                    "description": "Fast directory/file brute forcer",
                    "required": False,
                    "binary_url": "https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster-linux-x86_64.tar.gz"
                }
            },
            "system_tools": {
                "nmap": {
                    "package": "nmap",
                    "description": "Network discovery and security scanner",
                    "required": True
                },
                "masscan": {
                    "package": "masscan", 
                    "description": "Fast TCP port scanner",
                    "required": False
                },
                "gobuster": {
                    "package": "gobuster",
                    "description": "Directory/file brute forcer",
                    "required": False
                },
                "dirb": {
                    "package": "dirb",
                    "description": "Web content scanner",
                    "required": False
                },
                "nikto": {
                    "package": "nikto",
                    "description": "Web server scanner",
                    "required": False
                },
                "sqlmap": {
                    "package": "sqlmap",
                    "description": "SQL injection testing tool",
                    "required": False
                },
                "curl": {
                    "package": "curl",
                    "description": "Command line HTTP client",
                    "required": True
                },
                "wget": {
                    "package": "wget",
                    "description": "Command line downloader",
                    "required": True
                },
                "git": {
                    "package": "git",
                    "description": "Version control system",
                    "required": True
                },
                "python3": {
                    "package": "python3",
                    "description": "Python interpreter",
                    "required": True
                },
                "jq": {
                    "package": "jq",
                    "description": "JSON processor",
                    "required": False
                }
            },
            "python_tools": {
                "sublist3r": {
                    "package": "sublist3r",
                    "description": "Subdomain enumeration tool",
                    "required": False
                },
                "dirsearch": {
                    "package": "dirsearch",
                    "description": "Web path discovery tool", 
                    "required": False
                },
                "arjun": {
                    "package": "arjun",
                    "description": "HTTP parameter discovery",
                    "required": False
                },
                "paramspider": {
                    "package": "paramspider", 
                    "description": "Parameter mining tool",
                    "required": False,
                    "install_method": "git+https://github.com/devanshbatham/ParamSpider.git"
                },
                "xsstrike": {
                    "package": "xsstrike",
                    "description": "XSS detection suite",
                    "required": False
                }
            }
        }

    def check_tool_availability(self, tool_name: str) -> bool:
        """Check if a tool is available in any standard location"""
        # Check system PATH first
        if shutil.which(tool_name):
            return True

        # Check Go bin directory
        go_tool_path = self.go_bin_path / tool_name
        if go_tool_path.exists() and go_tool_path.is_file():
            return True

        # Check Cargo bin directory  
        cargo_tool_path = self.cargo_bin_path / tool_name
        if cargo_tool_path.exists() and cargo_tool_path.is_file():
            return True

        # Check local bin
        local_tool_path = self.local_bin_path / tool_name
        if local_tool_path.exists() and local_tool_path.is_file():
            return True

        return False

    def get_tool_version(self, tool_name: str) -> str:
        """Get version information for a tool"""
        if not self.check_tool_availability(tool_name):
            return "not found"

        try:
            # Try different version command variations
            version_commands = [
                [tool_name, "-version"],
                [tool_name, "--version"], 
                [tool_name, "-V"],
                [tool_name, "version"],
                [tool_name, "-h"],
                [tool_name, "--help"]
            ]

            for cmd in version_commands:
                try:
                    result = subprocess.run(
                        cmd, 
                        capture_output=True, 
                        text=True, 
                        timeout=5,
                        env=dict(os.environ, PATH=f"{os.environ['PATH']}:{self.go_bin_path}:{self.cargo_bin_path}")
                    )

                    output = result.stdout + result.stderr
                    if output and any(word in output.lower() for word in ['version', 'v.', 'v2', 'v3']):
                        # Extract version info (first line, first 50 chars)
                        version_line = output.strip().split('\n')[0][:50]
                        return version_line
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    continue

            return "installed"

        except Exception:
            return "unknown"

    def check_python_package(self, package_name: str) -> bool:
        """Check if Python package is installed"""
        try:
            # Try importing the package
            subprocess.run([
                sys.executable, "-c", f"import {package_name.replace('-', '_')}"
            ], check=True, capture_output=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            try:
                # Try with pip show
                result = subprocess.run([
                    sys.executable, "-m", "pip", "show", package_name
                ], capture_output=True, timeout=5)
                return result.returncode == 0
            except:
                return False

    def check_all_tools(self) -> Dict[str, Dict[str, bool]]:
        """Check availability of all reconnaissance tools"""
        status = {}

        # Check Go tools
        go_tools = {}
        for tool_name in self.tool_definitions["go_tools"]:
            go_tools[tool_name] = self.check_tool_availability(tool_name)
        status["go_tools"] = go_tools

        # Check Rust tools
        rust_tools = {}
        for tool_name in self.tool_definitions["rust_tools"]:
            rust_tools[tool_name] = self.check_tool_availability(tool_name)
        status["rust_tools"] = rust_tools

        # Check system tools
        system_tools = {}
        for tool_name in self.tool_definitions["system_tools"]:
            system_tools[tool_name] = self.check_tool_availability(tool_name)
        status["system_tools"] = system_tools

        # Check Python tools
        python_tools = {}
        for tool_name in self.tool_definitions["python_tools"]:
            python_tools[tool_name] = self.check_python_package(tool_name)
        status["python_tools"] = python_tools

        return status

    def get_missing_tools(self) -> Dict[str, List[str]]:
        """Get list of missing tools by category"""
        status = self.check_all_tools()
        missing = {}

        for category, tools in status.items():
            missing_in_category = []
            for tool_name, available in tools.items():
                if not available:
                    missing_in_category.append(tool_name)
            if missing_in_category:
                missing[category] = missing_in_category

        return missing

    def get_required_tools_status(self) -> Tuple[List[str], List[str]]:
        """Get status of required tools (available, missing)"""
        available_required = []
        missing_required = []

        for category, tools in self.tool_definitions.items():
            for tool_name, tool_info in tools.items():
                if tool_info.get("required", False):
                    if self.check_tool_availability(tool_name) or (category == "python_tools" and self.check_python_package(tool_name)):
                        available_required.append(tool_name)
                    else:
                        missing_required.append(tool_name)

        return available_required, missing_required

    def get_installation_commands(self, tool_name: str) -> Optional[List[str]]:
        """Get installation commands for a specific tool"""
        for category, tools in self.tool_definitions.items():
            if tool_name in tools:
                tool_info = tools[tool_name]
                commands = []

                if category == "go_tools":
                    if "dependencies" in tool_info:
                        commands.append(f"sudo apt install -y {' '.join(tool_info['dependencies'])}")
                    commands.append(f"go install {tool_info['repo']}")
                    if "post_install" in tool_info:
                        commands.append(tool_info["post_install"])

                elif category == "rust_tools":
                    if "cargo_name" in tool_info:
                        commands.append(f"cargo install {tool_info['cargo_name']}")
                    elif "binary_url" in tool_info:
                        commands.extend([
                            f"wget {tool_info['binary_url']}",
                            f"tar -xzf {tool_name}-*.tar.gz",
                            f"sudo mv {tool_name} /usr/local/bin/",
                            f"rm {tool_name}-*.tar.gz"
                        ])

                elif category == "system_tools":
                    if "package" in tool_info:
                        commands.append(f"sudo apt install -y {tool_info['package']}")

                elif category == "python_tools":
                    if "install_method" in tool_info:
                        commands.append(f"pip install {tool_info['install_method']}")
                    else:
                        commands.append(f"pip install {tool_info['package']}")

                return commands

        return None

    def generate_installation_script(self) -> str:
        """Generate complete installation script for missing tools"""
        missing = self.get_missing_tools()
        script_lines = [
            "#!/bin/bash",
            "# ReconXploit - Automated Tool Installation Script",
            "# Product of Kernelpanic under infosbios.tech",
            "",
            "set -e",
            "echo 'Installing missing ReconXploit tools...'",
            ""
        ]

        for category, tools in missing.items():
            if not tools:
                continue

            script_lines.extend([
                f"# {category.replace('_', ' ').title()}",
                f"echo 'Installing {category.replace('_', ' ')}...'"
            ])

            for tool in tools:
                commands = self.get_installation_commands(tool)
                if commands:
                    script_lines.extend([f"echo 'Installing {tool}...'"] + commands + [""])

        script_lines.extend([
            "echo 'Installation completed!'",
            "echo 'Run: reconxploit --check-tools to verify'"
        ])

        return "\n".join(script_lines)

    def check_dependencies(self) -> Dict[str, bool]:
        """Check system dependencies"""
        dependencies = {
            "go": shutil.which("go") is not None,
            "python3": shutil.which("python3") is not None,
            "pip": shutil.which("pip3") is not None or shutil.which("pip") is not None,
            "git": shutil.which("git") is not None,
            "curl": shutil.which("curl") is not None,
            "wget": shutil.which("wget") is not None
        }

        # Check Go version if available
        if dependencies["go"]:
            try:
                result = subprocess.run(["go", "version"], capture_output=True, text=True, timeout=5)
                go_version = result.stdout.strip()
                # Check if Go version is recent enough (1.19+)
                if "go1.1" in go_version and any(v in go_version for v in ["go1.19", "go1.20", "go1.21", "go1.22"]):
                    dependencies["go_version"] = True
                else:
                    dependencies["go_version"] = False
            except:
                dependencies["go_version"] = False

        return dependencies

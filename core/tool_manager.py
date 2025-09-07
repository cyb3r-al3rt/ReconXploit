#!/usr/bin/env python3
"""
ReconXploit v3.0 - Tool Manager
Product of Kernelpanic under infosbios.tech
"""

import shutil
import subprocess
import sys
from pathlib import Path

class ToolManager:
    """Comprehensive tool management and verification"""

    def __init__(self):
        self.go_bin_path = Path.home() / "go" / "bin"
        self.cargo_bin_path = Path.home() / ".cargo" / "bin"

    def check_tool_availability(self, tool_name: str) -> bool:
        """Check if tool is available in system"""
        # Check system PATH
        if shutil.which(tool_name):
            return True

        # Check Go bin directory
        go_tool = self.go_bin_path / tool_name
        if go_tool.exists() and go_tool.is_file():
            return True

        # Check Cargo bin directory
        cargo_tool = self.cargo_bin_path / tool_name
        if cargo_tool.exists() and cargo_tool.is_file():
            return True

        return False

    def get_tool_version(self, tool_name: str) -> str:
        """Get tool version information"""
        if not self.check_tool_availability(tool_name):
            return "not found"

        try:
            # Try common version commands
            for cmd in ["-version", "--version", "-V", "version"]:
                try:
                    result = subprocess.run(
                        [tool_name, cmd], 
                        capture_output=True, 
                        text=True, 
                        timeout=3
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        version_line = result.stdout.strip().split('\n')[0]
                        return version_line[:60] if len(version_line) > 60 else version_line
                except:
                    continue
            return "installed"
        except:
            return "unknown"

    def check_python_package(self, package_name: str) -> bool:
        """Check if Python package is available"""
        try:
            subprocess.run([
                sys.executable, "-c", f"import {package_name.replace('-', '_')}"
            ], check=True, capture_output=True, timeout=3)
            return True
        except:
            return False

    def check_all_tools(self) -> dict:
        """Check availability of all reconnaissance tools"""
        tools = {
            "go_tools": {
                "subfinder": self.check_tool_availability("subfinder"),
                "httpx": self.check_tool_availability("httpx"),
                "nuclei": self.check_tool_availability("nuclei"),
                "naabu": self.check_tool_availability("naabu"),
                "katana": self.check_tool_availability("katana"),
                "dnsx": self.check_tool_availability("dnsx"),
                "assetfinder": self.check_tool_availability("assetfinder"),
                "waybackurls": self.check_tool_availability("waybackurls"),
                "gau": self.check_tool_availability("gau"),
                "ffuf": self.check_tool_availability("ffuf"),
                "dalfox": self.check_tool_availability("dalfox"),
                "anew": self.check_tool_availability("anew"),
                "shuffledns": self.check_tool_availability("shuffledns")
            },
            "rust_tools": {
                "feroxbuster": self.check_tool_availability("feroxbuster")
            },
            "system_tools": {
                "nmap": self.check_tool_availability("nmap"),
                "masscan": self.check_tool_availability("masscan"), 
                "gobuster": self.check_tool_availability("gobuster"),
                "dirb": self.check_tool_availability("dirb"),
                "nikto": self.check_tool_availability("nikto"),
                "sqlmap": self.check_tool_availability("sqlmap"),
                "curl": self.check_tool_availability("curl"),
                "wget": self.check_tool_availability("wget"),
                "git": self.check_tool_availability("git"),
                "python3": self.check_tool_availability("python3"),
                "jq": self.check_tool_availability("jq")
            },
            "python_tools": {
                "sublist3r": self.check_python_package("sublist3r"),
                "dirsearch": self.check_python_package("dirsearch"),
                "arjun": self.check_python_package("arjun")
            }
        }

        return tools

    def get_installation_suggestion(self, tool_name: str, category: str) -> str:
        """Get installation suggestion for a tool"""
        suggestions = {
            "go_tools": {
                "subfinder": "go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
                "httpx": "go install github.com/projectdiscovery/httpx/cmd/httpx@latest",
                "nuclei": "go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
                "naabu": "go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
                "dalfox": "go install github.com/hahwul/dalfox/v2@latest"
            },
            "system_tools": {
                "nmap": "sudo apt install nmap",
                "gobuster": "sudo apt install gobuster",
                "curl": "sudo apt install curl"
            },
            "rust_tools": {
                "feroxbuster": "cargo install feroxbuster"
            }
        }

        return suggestions.get(category, {}).get(tool_name, f"Install {tool_name} manually")

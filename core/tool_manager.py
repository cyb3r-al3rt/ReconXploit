#!/usr/bin/env python3
"""
ReconXploit v3.0 - Tool Manager
Product of Kernelpanic under infosbios.tech
"""

import shutil
import subprocess
from pathlib import Path

class ToolManager:
    def __init__(self):
        self.go_bin_path = Path.home() / "go" / "bin"

    def check_tool_availability(self, tool_name):
        """Check if a tool is available in PATH"""
        # Check system PATH first
        if shutil.which(tool_name):
            return True

        # Check Go bin directory
        go_tool_path = self.go_bin_path / tool_name
        if go_tool_path.exists() and go_tool_path.is_file():
            return True

        return False

    def get_tool_version(self, tool_name):
        """Get version of a tool"""
        try:
            # Try different version commands
            for cmd in ["-version", "--version", "-V", "version"]:
                try:
                    result = subprocess.run([tool_name, cmd], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0 and result.stdout.strip():
                        return result.stdout.strip().split("\n")[0][:50]
                except:
                    continue
            return "installed"
        except:
            return "unknown"

    def check_all_tools(self):
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
                "gf": self.check_tool_availability("gf"),
                "waybackurls": self.check_tool_availability("waybackurls"),
                "gau": self.check_tool_availability("gau"),
                "ffuf": self.check_tool_availability("ffuf"),
                "hakrawler": self.check_tool_availability("hakrawler"),
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
                "python3": self.check_tool_availability("python3")
            },
            "python_tools": {
                "sublist3r": self.check_python_package("sublist3r"),
                "dirsearch": self.check_python_package("dirsearch"),
                "arjun": self.check_python_package("arjun"),
                "paramspider": self.check_python_package("paramspider"),
                "xsstrike": self.check_python_package("xsstrike")
            }
        }

        return tools

    def check_python_package(self, package_name):
        """Check if Python package is installed"""
        try:
            subprocess.run([
                "python3", "-c", f"import {package_name}"
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except Exception:
            return False

    def install_missing_tools(self):
        """Install missing tools (basic implementation)"""
        print("Tool installation feature coming soon...")
        print("For now, please install missing tools manually.")

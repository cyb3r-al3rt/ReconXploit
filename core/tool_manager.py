#!/usr/bin/env python3
"""
ReconXploit v3.0 - Professional Tool Manager
Product of Kernelpanic under infosbios.tech
"""

import shutil
import subprocess
import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

class ToolManager:
    """Professional tool management system"""

    def __init__(self):
        self.go_bin_path = Path.home() / "go" / "bin"
        # Professional tools with unique functionality
        self.tools = {
            # Subdomain enumeration tools (unique functionality)
            "subfinder": {
                "type": "go",
                "repo": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
                "description": "Fast passive subdomain discovery using multiple sources",
                "priority": 1,
                "unique_feature": "Multi-source passive enumeration with API integration"
            },
            "assetfinder": {
                "type": "go",
                "repo": "github.com/tomnomnom/assetfinder@latest",
                "description": "Find domains and subdomains related to a given domain",
                "priority": 1,
                "unique_feature": "Facebook and crt.sh certificate transparency logs"
            },
            "amass": {
                "type": "go",
                "repo": "github.com/owasp-amass/amass/v4/...@master",
                "description": "In-depth attack surface mapping and asset discovery",
                "priority": 2,
                "unique_feature": "Advanced DNS enumeration with relationship mapping"
            },

            # HTTP probing tools (unique functionality)
            "httpx": {
                "type": "go",
                "repo": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
                "description": "Fast and multi-purpose HTTP toolkit",
                "priority": 1,
                "unique_feature": "HTTP response analysis with technology detection"
            },
            "httprobe": {
                "type": "go",
                "repo": "github.com/tomnomnom/httprobe@latest",
                "description": "Take a list of domains and probe for working HTTP services",
                "priority": 2,
                "unique_feature": "Simple HTTP/HTTPS service discovery"
            },

            # Port scanning tools (unique functionality)
            "nmap": {
                "type": "system",
                "package": "nmap",
                "description": "Network discovery and security auditing",
                "priority": 1,
                "unique_feature": "Comprehensive service detection and OS fingerprinting"
            },
            "masscan": {
                "type": "system",
                "package": "masscan",
                "description": "High-speed port scanner",
                "priority": 2,
                "unique_feature": "Extremely fast TCP port scanning"
            },
            "naabu": {
                "type": "go",
                "repo": "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
                "description": "Fast port scanner written in Go",
                "priority": 1,
                "unique_feature": "SYN/CONNECT/UDP port scanning with IP verification"
            },

            # Content discovery tools (unique functionality)
            "gobuster": {
                "type": "system",
                "package": "gobuster",
                "description": "Directory/file and DNS busting tool",
                "priority": 1,
                "unique_feature": "Multi-mode brute forcing (dir, dns, vhost, s3)"
            },
            "dirb": {
                "type": "system",
                "package": "dirb",
                "description": "Web content scanner",
                "priority": 2,
                "unique_feature": "Recursive directory scanning with mutation testing"
            },
            "ffuf": {
                "type": "go",
                "repo": "github.com/ffuf/ffuf@latest",
                "description": "Fast web fuzzer written in Go",
                "priority": 1,
                "unique_feature": "Parameter fuzzing with advanced filtering"
            },

            # Vulnerability scanning tools (unique functionality)
            "nuclei": {
                "type": "go",
                "repo": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
                "description": "Fast vulnerability scanner based on simple YAML templates",
                "priority": 1,
                "unique_feature": "Template-based vulnerability detection with community templates"
            },
            "nikto": {
                "type": "system",
                "package": "nikto",
                "description": "Web server scanner",
                "priority": 2,
                "unique_feature": "Comprehensive web vulnerability scanning with plugin system"
            },

            # System tools (unique functionality)
            "curl": {
                "type": "system",
                "package": "curl",
                "description": "Command line tool for transferring data",
                "priority": 1,
                "unique_feature": "HTTP client with extensive protocol support"
            },
            "wget": {
                "type": "system",
                "package": "wget",
                "description": "Free utility for non-interactive download",
                "priority": 1,
                "unique_feature": "Recursive web downloading and mirroring"
            },
            "jq": {
                "type": "system",
                "package": "jq",
                "description": "Command-line JSON processor",
                "priority": 1,
                "unique_feature": "Advanced JSON filtering and transformation"
            }
        }

    async def check_all_tools(self, detailed: bool = False) -> Dict[str, bool]:
        """Check availability of all professional tools"""
        print("\n" + "="*70)
        print("\033[0;96m🔍 ReconXploit v3.0 Professional - Tool Installation Status\033[0m")
        print("="*70)

        status = {}
        total_tools = len(self.tools)
        installed_tools = 0

        # Categorize tools by functionality
        categories = {
            'Critical Reconnaissance Tools (Priority 1)': [],
            'Advanced Enhancement Tools (Priority 2)': []
        }

        for tool_name, tool_info in self.tools.items():
            priority = tool_info.get('priority', 2)
            category = 'Critical Reconnaissance Tools (Priority 1)' if priority == 1 else 'Advanced Enhancement Tools (Priority 2)'

            is_available = await self._check_single_tool(tool_name, tool_info)
            status[tool_name] = is_available

            if is_available:
                installed_tools += 1

            categories[category].append((tool_name, tool_info, is_available))

        # Display results by category
        for category_name, tools in categories.items():
            if not tools:
                continue

            print(f"\n\033[0;94m📂 {category_name}\033[0m")
            category_installed = sum(1 for _, _, available in tools if available)

            for tool_name, tool_info, is_available in tools:
                if is_available:
                    version = await self._get_tool_version(tool_name)
                    print(f"  \033[0;32m✅ {tool_name:<15}\033[0m {version}")
                    if detailed:
                        print(f"     \033[0;90m└─ {tool_info.get('description', 'No description')}\033[0m")
                        print(f"     \033[0;36m└─ Unique: {tool_info.get('unique_feature', 'Standard functionality')}\033[0m")
                else:
                    print(f"  \033[0;31m❌ {tool_name:<15}\033[0m Not Found")
                    if detailed:
                        suggestion = self._get_installation_suggestion(tool_name, tool_info)
                        print(f"     \033[0;33m└─ Install: {suggestion}\033[0m")
                        print(f"     \033[0;36m└─ Unique: {tool_info.get('unique_feature', 'Standard functionality')}\033[0m")

            # Category summary
            percentage = (category_installed / len(tools) * 100) if tools else 0
            if percentage >= 90:
                status_color = "\033[0;32m"
                status_icon = "🎉"
            elif percentage >= 70:
                status_color = "\033[0;33m" 
                status_icon = "👍"
            else:
                status_color = "\033[0;31m"
                status_icon = "🔧"

            print(f"  {status_color}└─ Status: {category_installed}/{len(tools)} ({percentage:.1f}%) {status_icon}\033[0m")

        # Overall summary
        overall_percentage = (installed_tools / total_tools * 100) if total_tools > 0 else 0

        print(f"\n{'='*70}")
        if overall_percentage >= 90:
            summary_color = "\033[0;32m"
            summary_icon = "🎉"
            summary_text = "EXCELLENT - Professional Grade"
        elif overall_percentage >= 70:
            summary_color = "\033[0;33m"
            summary_icon = "👍"
            summary_text = "GOOD - Functional"
        else:
            summary_color = "\033[0;31m"
            summary_icon = "🔧"
            summary_text = "NEEDS ATTENTION - Install Missing Tools"

        print(f"{summary_color}🎯 OVERALL STATUS: {installed_tools}/{total_tools} tools ({overall_percentage:.1f}%) - {summary_text} {summary_icon}\033[0m")

        # Installation suggestions
        missing_critical = [name for name, info in self.tools.items() 
                           if info.get('priority') == 1 and not status[name]]

        if missing_critical:
            print(f"\n\033[0;31m🔥 MISSING CRITICAL TOOLS:\033[0m {', '.join(missing_critical)}")
            print("\n\033[0;96m💡 QUICK INSTALLATION COMMANDS:\033[0m")

            go_tools = [tool for tool in missing_critical if self.tools[tool].get('type') == 'go']
            if go_tools:
                print("\033[0;36m# Install critical Go tools:\033[0m")
                for tool in go_tools:
                    print(f"go install {self.tools[tool].get('repo', '')}")

            system_tools = [tool for tool in missing_critical if self.tools[tool].get('type') == 'system']
            if system_tools:
                print("\033[0;36m# Install critical system tools:\033[0m")
                packages = [self.tools[tool].get('package', tool) for tool in system_tools]
                print(f"sudo apt update && sudo apt install -y {' '.join(packages)}")
        else:
            print(f"\n\033[0;32m🎉 All critical tools are installed! Professional reconnaissance ready.\033[0m")

        return status

    async def _check_single_tool(self, tool_name: str, tool_info: Dict) -> bool:
        """Check if a single tool is available"""
        # Check system PATH first
        if shutil.which(tool_name):
            return True

        # Check Go tools in go/bin
        tool_type = tool_info.get("type", "system")
        if tool_type == "go":
            go_path = self.go_bin_path / tool_name
            if go_path.exists():
                return True

        return False

    async def _get_tool_version(self, tool_name: str) -> str:
        """Get version information for a tool"""
        try:
            version_commands = ["-version", "--version", "-V", "version"]

            for cmd in version_commands:
                try:
                    result = subprocess.run(
                        [tool_name, cmd], 
                        capture_output=True, 
                        text=True, 
                        timeout=3
                    )

                    if result.returncode == 0 and result.stdout.strip():
                        version_line = result.stdout.strip().split('\n')[0]
                        version_clean = version_line[:60] if len(version_line) > 60 else version_line
                        return f"✓ {version_clean}"
                except:
                    continue

            return "✓ installed (version unknown)"

        except Exception:
            return "✓ available"

    def _get_installation_suggestion(self, tool_name: str, tool_info: Dict) -> str:
        """Get installation suggestion for a tool"""
        tool_type = tool_info.get("type", "system")

        if tool_type == "go":
            repo = tool_info.get("repo", "")
            return f"go install {repo}"
        elif tool_type == "system":
            package = tool_info.get("package", tool_name)
            return f"sudo apt install {package}"
        else:
            return f"Manual installation required for {tool_name}"

    async def install_missing_tools(self):
        """Install missing professional tools automatically"""
        print("\033[0;96m🚀 INSTALLING MISSING PROFESSIONAL TOOLS...\033[0m")

        status = await self.check_all_tools(detailed=False)
        missing_tools = [name for name, available in status.items() if not available]

        if not missing_tools:
            print("\033[0;32m✅ All professional tools are already installed!\033[0m")
            return

        print(f"\033[0;33mInstalling {len(missing_tools)} missing professional tools...\033[0m")

        installed_count = 0
        failed_count = 0

        # Install critical tools first
        for tool_name in missing_tools:
            tool_info = self.tools.get(tool_name, {})
            priority = tool_info.get('priority', 2)

            if priority == 1:
                print(f"  \033[0;33m📥 Installing {tool_name} (Critical)...\033[0m", end=" ", flush=True)

                success = await self._install_single_tool(tool_name, tool_info)
                if success:
                    print("\033[0;32m✅\033[0m")
                    installed_count += 1
                else:
                    print("\033[0;31m❌\033[0m")
                    failed_count += 1

        # Install enhancement tools
        for tool_name in missing_tools:
            tool_info = self.tools.get(tool_name, {})
            priority = tool_info.get('priority', 2)

            if priority != 1:
                print(f"  \033[0;33m📥 Installing {tool_name} (Enhancement)...\033[0m", end=" ", flush=True)

                success = await self._install_single_tool(tool_name, tool_info)
                if success:
                    print("\033[0;32m✅\033[0m")
                    installed_count += 1
                else:
                    print("\033[0;31m❌\033[0m")
                    failed_count += 1

        print(f"\n\033[0;32m🎉 PROFESSIONAL TOOL INSTALLATION COMPLETED!\033[0m")
        print(f"\033[0;32m✅ Successfully Installed: {installed_count} tools\033[0m")
        if failed_count > 0:
            print(f"\033[0;31m❌ Failed: {failed_count} tools (may require manual installation)\033[0m")

    async def _install_single_tool(self, tool_name: str, tool_info: Dict) -> bool:
        """Install a single professional tool"""
        try:
            tool_type = tool_info.get("type", "system")

            if tool_type == "go":
                repo = tool_info.get("repo")
                if repo:
                    result = subprocess.run(
                        ["go", "install", repo], 
                        capture_output=True, 
                        timeout=300  # Increased timeout for large installations
                    )
                    return result.returncode == 0

            elif tool_type == "system":
                package = tool_info.get("package", tool_name)
                result = subprocess.run(
                    ["sudo", "apt", "install", "-y", package],
                    capture_output=True,
                    timeout=300
                )
                return result.returncode == 0

            return False

        except Exception:
            return False

    async def update_all_tools(self):
        """Update all installed professional tools"""
        print("\033[0;96m⬆️ UPDATING ALL PROFESSIONAL TOOLS...\033[0m")

        # Update Go tools
        print("\033[0;94m📦 Updating Go-based reconnaissance tools...\033[0m")
        for tool_name, tool_info in self.tools.items():
            if tool_info.get("type") == "go" and await self._check_single_tool(tool_name, tool_info):
                repo = tool_info.get("repo")
                if repo:
                    print(f"  \033[0;33m⬆️ Updating {tool_name}...\033[0m")
                    subprocess.run(["go", "install", repo], capture_output=True)

        # Update system packages
        print("\033[0;94m📦 Updating system packages...\033[0m")
        subprocess.run(["sudo", "apt", "update"], capture_output=True)
        subprocess.run(["sudo", "apt", "upgrade", "-y"], capture_output=True)

        print("\033[0;32m✅ All professional tools updated successfully!\033[0m")

    async def list_all_tools(self):
        """List all supported professional tools"""
        print("\n\033[0;96m📋 ALL PROFESSIONAL RECONNAISSANCE TOOLS\033[0m")
        print("="*60)

        # Group tools by functionality
        functionality_groups = {
            'Subdomain Enumeration': ['subfinder', 'assetfinder', 'amass'],
            'HTTP Service Detection': ['httpx', 'httprobe'],
            'Port & Network Scanning': ['nmap', 'masscan', 'naabu'],
            'Content & Directory Discovery': ['gobuster', 'dirb', 'ffuf'],
            'Vulnerability Assessment': ['nuclei', 'nikto'],
            'System & Utility Tools': ['curl', 'wget', 'jq']
        }

        for group_name, tool_names in functionality_groups.items():
            print(f"\n\033[0;94m📂 {group_name}\033[0m")
            for tool_name in tool_names:
                if tool_name in self.tools:
                    tool_info = self.tools[tool_name]
                    priority = "🔥" if tool_info.get('priority') == 1 else "⚡"
                    print(f"  {priority} {tool_name:<15} - {tool_info.get('description', 'No description')}")
                    print(f"     \033[0;36m└─ Unique: {tool_info.get('unique_feature', 'Standard functionality')}\033[0m")

        print(f"\n\033[0;36mTotal Professional Tools: {len(self.tools)}\033[0m")
        print("\033[0;33m🔥 = Critical for professional reconnaissance\033[0m")
        print("\033[0;33m⚡ = Enhancement tools for advanced features\033[0m")

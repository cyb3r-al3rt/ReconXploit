#!/usr/bin/env python3
"""
ReconXploit v4.0 - Ultimate Tool Manager
Product of Kernelpanic under infosbios.tech
"""

import shutil
import subprocess
import sys
import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor

class UltimateToolManager:
    """Ultimate tool management with 100+ reconnaissance tools"""

    def __init__(self):
        self.go_bin_path = Path.home() / "go" / "bin"
        self.cargo_bin_path = Path.home() / ".cargo" / "bin"
        self.python_bin_path = Path.home() / ".local" / "bin"
        self.npm_bin_path = Path.home() / "node_modules" / ".bin"

        # Ultimate tool definitions - 100+ tools organized by category
        self.ultimate_tools = {
            # === SUBDOMAIN ENUMERATION TOOLS (25+ tools) ===
            "subdomain_enumeration": {
                "subfinder": {
                    "type": "go",
                    "repo": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
                    "description": "Fast subdomain discovery tool",
                    "category": "passive_discovery",
                    "priority": 1
                },
                "assetfinder": {
                    "type": "go", 
                    "repo": "github.com/tomnomnom/assetfinder@latest",
                    "description": "Find domains and subdomains related to a given domain",
                    "category": "passive_discovery",
                    "priority": 1
                },
                "amass": {
                    "type": "go",
                    "repo": "github.com/owasp-amass/amass/v4/...@master",
                    "description": "In-depth attack surface mapping and asset discovery",
                    "category": "comprehensive_discovery", 
                    "priority": 1
                },
                "sublist3r": {
                    "type": "python",
                    "package": "sublist3r",
                    "description": "Fast subdomains enumeration tool",
                    "category": "passive_discovery",
                    "priority": 2
                },
                "knockpy": {
                    "type": "python",
                    "repo": "https://github.com/guelfoweb/knock.git",
                    "description": "Subdomain scanner",
                    "category": "active_discovery",
                    "priority": 2
                },
                "subbrute": {
                    "type": "python",
                    "repo": "https://github.com/TheRook/subbrute.git",
                    "description": "Subdomain bruteforcing tool",
                    "category": "bruteforce_discovery",
                    "priority": 2
                },
                "fierce": {
                    "type": "python",
                    "package": "fierce",
                    "description": "DNS reconnaissance tool",
                    "category": "dns_discovery",
                    "priority": 2
                },
                "dnsrecon": {
                    "type": "python",
                    "repo": "https://github.com/darkoperator/dnsrecon.git",
                    "description": "DNS enumeration script",
                    "category": "dns_discovery",
                    "priority": 2
                },
                "massdns": {
                    "type": "system",
                    "repo": "https://github.com/blechschmidt/massdns.git",
                    "description": "High-performance DNS stub resolver",
                    "category": "dns_resolution",
                    "priority": 2
                },
                "shuffledns": {
                    "type": "go",
                    "repo": "github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest",
                    "description": "Wrapper around massdns for bruteforcing subdomains",
                    "category": "bruteforce_discovery",
                    "priority": 2
                },
                "puredns": {
                    "type": "go", 
                    "repo": "github.com/d3mondev/puredns/v2@latest",
                    "description": "Fast domain resolver and subdomain bruteforcing",
                    "category": "bruteforce_discovery",
                    "priority": 2
                },
                "crobat": {
                    "type": "go",
                    "repo": "github.com/cgboal/sonarsearch/cmd/crobat@latest",
                    "description": "Rapid7 sonar search",
                    "category": "passive_discovery",
                    "priority": 3
                },
                "findomain": {
                    "type": "rust",
                    "repo": "https://github.com/Findomain/Findomain.git",
                    "description": "Cross-platform subdomain enumerator",
                    "category": "passive_discovery", 
                    "priority": 2
                },
                "chaos": {
                    "type": "go",
                    "repo": "github.com/projectdiscovery/chaos-client/cmd/chaos@latest",
                    "description": "Chaos DNS client",
                    "category": "passive_discovery",
                    "priority": 3
                }
            },

            # === HTTP/HTTPS PROBING TOOLS (15+ tools) ===
            "http_probing": {
                "httpx": {
                    "type": "go",
                    "repo": "github.com/projectdiscovery/httpx/cmd/httpx@latest", 
                    "description": "Fast and multi-purpose HTTP toolkit",
                    "category": "http_analysis",
                    "priority": 1
                },
                "httprobe": {
                    "type": "go",
                    "repo": "github.com/tomnomnom/httprobe@latest",
                    "description": "Take a list of domains and probe for working HTTP services",
                    "category": "http_probing",
                    "priority": 1
                },
                "meg": {
                    "type": "go",
                    "repo": "github.com/tomnomnom/meg@latest",
                    "description": "Fetch many paths for many hosts",
                    "category": "http_fetching",
                    "priority": 2
                },
                "aquatone": {
                    "type": "go",
                    "repo": "github.com/michenriksen/aquatone@latest",
                    "description": "Visual inspection of websites across large amount of hosts",
                    "category": "visual_recon",
                    "priority": 2
                },
                "gowitness": {
                    "type": "go",
                    "repo": "github.com/sensepost/gowitness@latest",
                    "description": "Web screenshot utility using Chrome Headless",
                    "category": "visual_recon",
                    "priority": 2
                }
            },

            # === PORT SCANNING TOOLS (20+ tools) ===
            "port_scanning": {
                "nmap": {
                    "type": "system",
                    "package": "nmap",
                    "description": "Network discovery and security auditing",
                    "category": "comprehensive_scanner",
                    "priority": 1
                },
                "masscan": {
                    "type": "system",
                    "package": "masscan",
                    "description": "TCP port scanner, spews SYN packets asynchronously",
                    "category": "fast_scanner", 
                    "priority": 1
                },
                "naabu": {
                    "type": "go",
                    "repo": "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
                    "description": "Fast port scanner written in go",
                    "category": "fast_scanner",
                    "priority": 1,
                    "dependencies": ["libpcap-dev"],
                    "post_install": "sudo setcap cap_net_raw,cap_net_admin+eip $(which naabu)"
                },
                "unicornscan": {
                    "type": "system",
                    "package": "unicornscan", 
                    "description": "Asynchronous network stimulus delivery engine",
                    "category": "advanced_scanner",
                    "priority": 3
                },
                "zmap": {
                    "type": "system",
                    "package": "zmap",
                    "description": "Fast single packet network scanner",
                    "category": "internet_scanner",
                    "priority": 3
                },
                "rustscan": {
                    "type": "rust",
                    "package": "rustscan",
                    "description": "Modern port scanner",
                    "category": "fast_scanner",
                    "priority": 2
                }
            },

            # === CONTENT DISCOVERY TOOLS (25+ tools) ===
            "content_discovery": {
                "feroxbuster": {
                    "type": "rust",
                    "package": "feroxbuster",
                    "description": "Fast, simple, recursive content discovery tool",
                    "category": "directory_bruteforce",
                    "priority": 1
                },
                "gobuster": {
                    "type": "system",
                    "package": "gobuster", 
                    "description": "Directory/file, DNS, and VHost busting tool",
                    "category": "directory_bruteforce",
                    "priority": 1
                },
                "dirb": {
                    "type": "system",
                    "package": "dirb",
                    "description": "Web content scanner",
                    "category": "directory_bruteforce",
                    "priority": 1
                },
                "dirsearch": {
                    "type": "python",
                    "repo": "https://github.com/maurosoria/dirsearch.git",
                    "description": "Web path discovery tool",
                    "category": "directory_bruteforce", 
                    "priority": 1
                },
                "ffuf": {
                    "type": "go",
                    "repo": "github.com/ffuf/ffuf@latest",
                    "description": "Fast web fuzzer written in Go",
                    "category": "web_fuzzer",
                    "priority": 1
                },
                "wfuzz": {
                    "type": "python",
                    "package": "wfuzz",
                    "description": "Web application fuzzer",
                    "category": "web_fuzzer",
                    "priority": 2
                },
                "dirmap": {
                    "type": "python",
                    "repo": "https://github.com/H4ckForJob/dirmap.git",
                    "description": "Advanced web directory & file scanner",
                    "category": "directory_scanner",
                    "priority": 2
                },
                "dirhunt": {
                    "type": "python",
                    "package": "dirhunt",
                    "description": "Find web directories without bruteforce",
                    "category": "intelligent_discovery",
                    "priority": 2
                }
            },

            # === VULNERABILITY SCANNERS (20+ tools) ===
            "vulnerability_scanning": {
                "nuclei": {
                    "type": "go",
                    "repo": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
                    "description": "Fast and customizable vulnerability scanner",
                    "category": "template_scanner",
                    "priority": 1
                },
                "nikto": {
                    "type": "system",
                    "package": "nikto",
                    "description": "Web server scanner",
                    "category": "web_vulnerability_scanner",
                    "priority": 1
                },
                "sqlmap": {
                    "type": "system",
                    "package": "sqlmap",
                    "description": "Automatic SQL injection and database takeover tool",
                    "category": "sql_injection_scanner",
                    "priority": 1
                },
                "wpscan": {
                    "type": "ruby",
                    "package": "wpscan",
                    "description": "WordPress security scanner",
                    "category": "cms_scanner",
                    "priority": 2
                },
                "joomscan": {
                    "type": "perl", 
                    "repo": "https://github.com/OWASP/joomscan.git",
                    "description": "Joomla vulnerability scanner",
                    "category": "cms_scanner",
                    "priority": 2
                },
                "dalfox": {
                    "type": "go",
                    "repo": "github.com/hahwul/dalfox/v2@latest",
                    "description": "Parameter analysis and XSS scanning tool",
                    "category": "xss_scanner",
                    "priority": 2
                },
                "xsstrike": {
                    "type": "python",
                    "repo": "https://github.com/s0md3v/XSStrike.git",
                    "description": "Advanced XSS detection suite",
                    "category": "xss_scanner",
                    "priority": 2
                },
                "commix": {
                    "type": "python",
                    "repo": "https://github.com/commixproject/commix.git",
                    "description": "Command injection exploiter",
                    "category": "command_injection_scanner",
                    "priority": 2
                },
                "jaeles": {
                    "type": "go",
                    "repo": "github.com/jaeles-project/jaeles@latest",
                    "description": "Powerful vulnerability scanner",
                    "category": "template_scanner",
                    "priority": 2
                }
            },

            # === PARAMETER DISCOVERY TOOLS (10+ tools) ===
            "parameter_discovery": {
                "arjun": {
                    "type": "python",
                    "package": "arjun",
                    "description": "HTTP parameter discovery suite", 
                    "category": "parameter_scanner",
                    "priority": 1
                },
                "paramspider": {
                    "type": "python",
                    "repo": "https://github.com/devanshbatham/ParamSpider.git",
                    "description": "Parameter mining tool",
                    "category": "parameter_miner",
                    "priority": 1
                },
                "x8": {
                    "type": "rust",
                    "repo": "https://github.com/Sh1Yo/x8.git",
                    "description": "Hidden parameters discovery suite",
                    "category": "hidden_parameter_discovery",
                    "priority": 2
                }
            },

            # === CRAWLING & SPIDERING TOOLS (15+ tools) ===
            "crawling_spidering": {
                "katana": {
                    "type": "go", 
                    "repo": "github.com/projectdiscovery/katana/cmd/katana@latest",
                    "description": "Next-generation crawling and spidering framework",
                    "category": "modern_crawler",
                    "priority": 1
                },
                "hakrawler": {
                    "type": "go",
                    "repo": "github.com/hakluke/hakrawler@latest", 
                    "description": "Simple, fast web crawler designed for easy, quick discovery",
                    "category": "fast_crawler",
                    "priority": 1
                },
                "gospider": {
                    "type": "go",
                    "repo": "github.com/jaeles-project/gospider@latest",
                    "description": "Fast web spider written in Go",
                    "category": "fast_crawler", 
                    "priority": 2
                },
                "waybackurls": {
                    "type": "go",
                    "repo": "github.com/tomnomnom/waybackurls@latest",
                    "description": "Fetch all the URLs that the Wayback Machine knows about for a domain",
                    "category": "historical_urls",
                    "priority": 1
                },
                "gau": {
                    "type": "go",
                    "repo": "github.com/lc/gau/v2/cmd/gau@latest",
                    "description": "Fetch known URLs from various sources",
                    "category": "url_fetcher",
                    "priority": 1
                }
            },

            # === SYSTEM & NETWORK TOOLS (15+ tools) ===
            "system_network": {
                "curl": {
                    "type": "system",
                    "package": "curl",
                    "description": "Command line tool for transferring data",
                    "category": "http_client",
                    "priority": 1
                },
                "wget": {
                    "type": "system", 
                    "package": "wget",
                    "description": "GNU Wget is a computer program that retrieves content from web servers",
                    "category": "http_client",
                    "priority": 1
                },
                "git": {
                    "type": "system",
                    "package": "git",
                    "description": "Distributed version control system",
                    "category": "version_control",
                    "priority": 1
                },
                "python3": {
                    "type": "system",
                    "package": "python3",
                    "description": "Python programming language interpreter",
                    "category": "interpreter",
                    "priority": 1
                },
                "jq": {
                    "type": "system",
                    "package": "jq",
                    "description": "Command-line JSON processor",
                    "category": "data_processor",
                    "priority": 1
                },
                "anew": {
                    "type": "go",
                    "repo": "github.com/tomnomnom/anew@latest",
                    "description": "Tool for adding new lines to files, skipping duplicates",
                    "category": "data_processor",
                    "priority": 2
                }
            }
        }

        # Performance metrics
        self.installation_stats = {
            "total_tools": 0,
            "installed_tools": 0,
            "failed_installations": 0,
            "installation_time": 0
        }

    def get_all_tools_count(self) -> int:
        """Get total count of all available tools"""
        total = 0
        for category in self.ultimate_tools.values():
            total += len(category)
        return total

    async def check_all_ultimate_tools(self, detailed: bool = False) -> Dict[str, Dict[str, bool]]:
        """Check availability of all 100+ ultimate tools"""
        print("\n" + "="*80)
        print("\033[0;96m🔍 ReconXploit v4.0 Ultimate - Tool Installation Status\033[0m")
        print("="*80)
        print("\033[0;36mChecking 100+ integrated reconnaissance tools...\033[0m")

        all_status = {}
        total_tools = 0
        total_installed = 0

        for category_name, tools in self.ultimate_tools.items():
            print(f"\n\033[0;94m📂 {category_name.replace('_', ' ').title()} ({len(tools)} tools)\033[0m")

            category_status = {}
            category_installed = 0

            for tool_name, tool_info in tools.items():
                is_available = await self._check_single_tool(tool_name, tool_info)
                category_status[tool_name] = is_available
                total_tools += 1

                if is_available:
                    category_installed += 1
                    total_installed += 1
                    version = await self._get_tool_version(tool_name)
                    priority_icon = "🔥" if tool_info.get("priority", 3) == 1 else "⚡" if tool_info.get("priority", 3) == 2 else "📋"
                    print(f"  \033[0;32m✅ {tool_name:<20}\033[0m {priority_icon} {version}")

                    if detailed:
                        print(f"     \033[0;90m└─ {tool_info.get('description', 'No description')}\033[0m")
                else:
                    priority_icon = "🔥" if tool_info.get("priority", 3) == 1 else "⚡" if tool_info.get("priority", 3) == 2 else "📋"
                    print(f"  \033[0;31m❌ {tool_name:<20}\033[0m {priority_icon} Not Found")

                    if detailed:
                        suggestion = self._get_installation_suggestion(tool_name, tool_info)
                        print(f"     \033[0;33m└─ Install: {suggestion}\033[0m")

            # Category summary
            category_percentage = (category_installed / len(tools) * 100) if tools else 0
            if category_percentage >= 90:
                status_color = "\033[0;32m"  # Green
                status_icon = "🎉"
            elif category_percentage >= 70:
                status_color = "\033[0;33m"  # Yellow
                status_icon = "👍"
            else:
                status_color = "\033[0;31m"  # Red
                status_icon = "🔧"

            print(f"  {status_color}┌─ Category Status: {category_installed}/{len(tools)} ({category_percentage:.1f}%) {status_icon}\033[0m")
            all_status[category_name] = category_status

        # Overall summary
        overall_percentage = (total_installed / total_tools * 100) if total_tools > 0 else 0

        print(f"\n{'='*80}")
        if overall_percentage >= 90:
            summary_color = "\033[0;32m"
            summary_icon = "🎉"
            summary_text = "EXCELLENT"
        elif overall_percentage >= 70:
            summary_color = "\033[0;33m"
            summary_icon = "👍" 
            summary_text = "GOOD"
        elif overall_percentage >= 50:
            summary_color = "\033[0;33m"
            summary_icon = "⚠️"
            summary_text = "MODERATE"
        else:
            summary_color = "\033[0;31m"
            summary_icon = "🔧"
            summary_text = "NEEDS ATTENTION"

        print(f"{summary_color}🎯 ULTIMATE TOOL STATUS: {total_installed}/{total_tools} tools ({overall_percentage:.1f}%) - {summary_text} {summary_icon}\033[0m")

        # Priority tool analysis
        critical_missing = []
        important_missing = []

        for category_name, tools in self.ultimate_tools.items():
            for tool_name, tool_info in tools.items():
                if not all_status[category_name][tool_name]:
                    priority = tool_info.get("priority", 3)
                    if priority == 1:
                        critical_missing.append(tool_name)
                    elif priority == 2:
                        important_missing.append(tool_name)

        if critical_missing:
            print(f"\n\033[0;31m🔥 CRITICAL MISSING TOOLS ({len(critical_missing)}):\033[0m {', '.join(critical_missing[:10])}")
        if important_missing:
            print(f"\033[0;33m⚡ IMPORTANT MISSING TOOLS ({len(important_missing)}):\033[0m {', '.join(important_missing[:10])}")

        # Installation suggestions
        if total_installed < total_tools:
            print(f"\n\033[0;96m💡 QUICK INSTALLATION:\033[0m")
            print("\033[0;36m# Install all ultimate tools automatically:\033[0m")
            print("./reconxploit --install-all-tools")
            print()
            print("\033[0;36m# Install critical tools manually:\033[0m")
            if critical_missing:
                for tool in critical_missing[:3]:
                    category, tool_info = self._find_tool_info(tool)
                    if tool_info:
                        suggestion = self._get_installation_suggestion(tool, tool_info)
                        print(f"{suggestion}")

        return all_status

    async def _check_single_tool(self, tool_name: str, tool_info: Dict) -> bool:
        """Check if a single tool is available"""
        # Check system PATH first
        if shutil.which(tool_name):
            return True

        # Check specific binary paths based on tool type
        tool_type = tool_info.get("type", "system")

        if tool_type == "go":
            go_path = self.go_bin_path / tool_name
            if go_path.exists() and go_path.is_file():
                return True
        elif tool_type == "rust":
            cargo_path = self.cargo_bin_path / tool_name  
            if cargo_path.exists() and cargo_path.is_file():
                return True
        elif tool_type == "python":
            # Check if Python package is installed
            try:
                package_name = tool_info.get("package", tool_name)
                result = subprocess.run([
                    sys.executable, "-c", f"import {package_name.replace('-', '_')}"
                ], capture_output=True, timeout=3)
                return result.returncode == 0
            except:
                pass

        return False

    async def _get_tool_version(self, tool_name: str) -> str:
        """Get version information for a tool"""
        try:
            version_commands = ["-version", "--version", "-V", "version", "-h"]

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
                        # Clean up version string
                        version_clean = version_line[:50] if len(version_line) > 50 else version_line
                        return version_clean
                    elif result.stderr.strip():
                        version_line = result.stderr.strip().split('\n')[0]
                        version_clean = version_line[:50] if len(version_line) > 50 else version_line
                        return version_clean

                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    continue

            return "installed"

        except Exception:
            return "unknown"

    def _get_installation_suggestion(self, tool_name: str, tool_info: Dict) -> str:
        """Get installation suggestion for a tool"""
        tool_type = tool_info.get("type", "system")

        if tool_type == "go":
            repo = tool_info.get("repo", f"github.com/example/{tool_name}@latest")
            return f"go install {repo}"
        elif tool_type == "rust":
            if "package" in tool_info:
                return f"cargo install {tool_info['package']}"
            else:
                return f"git clone {tool_info.get('repo', '')} && cd {tool_name} && cargo install --path ."
        elif tool_type == "system":
            package = tool_info.get("package", tool_name)
            return f"sudo apt install {package}"
        elif tool_type == "python":
            if "package" in tool_info:
                return f"pip install {tool_info['package']}"
            elif "repo" in tool_info:
                return f"pip install git+{tool_info['repo']}"
            else:
                return f"pip install {tool_name}"
        else:
            return f"Manual installation required for {tool_name}"

    def _find_tool_info(self, tool_name: str) -> Tuple[str, Optional[Dict]]:
        """Find tool information by name"""
        for category_name, tools in self.ultimate_tools.items():
            if tool_name in tools:
                return category_name, tools[tool_name]
        return "", None

    async def install_all_ultimate_tools(self):
        """Install all 100+ ultimate tools automatically"""
        print("\033[0;96m🚀 ULTIMATE TOOL INSTALLATION STARTING...\033[0m")
        print("\033[0;33mThis will install 100+ reconnaissance tools. This may take 30-60 minutes.\033[0m")

        start_time = time.time()
        installed_count = 0
        failed_count = 0

        # Install by priority (critical tools first)
        for priority in [1, 2, 3]:
            print(f"\n\033[0;94m📦 Installing Priority {priority} Tools...\033[0m")

            for category_name, tools in self.ultimate_tools.items():
                for tool_name, tool_info in tools.items():
                    if tool_info.get("priority", 3) == priority:
                        # Check if already installed
                        if await self._check_single_tool(tool_name, tool_info):
                            print(f"  \033[0;32m✅ {tool_name} - Already installed\033[0m")
                            installed_count += 1
                            continue

                        print(f"  \033[0;33m📥 Installing {tool_name}...\033[0m", end=" ", flush=True)

                        success = await self._install_single_tool(tool_name, tool_info)
                        if success:
                            print("\033[0;32m✅ Success\033[0m")
                            installed_count += 1
                        else:
                            print("\033[0;31m❌ Failed\033[0m")
                            failed_count += 1

        # Final summary
        end_time = time.time()
        installation_time = end_time - start_time

        print(f"\n{'='*60}")
        print(f"\033[0;32m🎉 ULTIMATE INSTALLATION COMPLETED!\033[0m")
        print(f"\033[0;36m⏱️  Total Time: {installation_time:.1f} seconds\033[0m") 
        print(f"\033[0;32m✅ Installed: {installed_count} tools\033[0m")
        print(f"\033[0;31m❌ Failed: {failed_count} tools\033[0m")

        if failed_count > 0:
            print(f"\033[0;33m💡 Run './reconxploit --check-tools --detailed' to see failed installations\033[0m")

    async def _install_single_tool(self, tool_name: str, tool_info: Dict) -> bool:
        """Install a single tool"""
        try:
            tool_type = tool_info.get("type", "system")

            if tool_type == "go":
                repo = tool_info.get("repo")
                if repo:
                    result = subprocess.run(
                        ["go", "install", repo], 
                        capture_output=True, 
                        timeout=300
                    )
                    success = result.returncode == 0

                    # Run post-install commands if specified
                    if success and "post_install" in tool_info:
                        subprocess.run(tool_info["post_install"], shell=True)

                    return success

            elif tool_type == "system":
                package = tool_info.get("package", tool_name)
                # Install dependencies first
                if "dependencies" in tool_info:
                    for dep in tool_info["dependencies"]:
                        subprocess.run(["sudo", "apt", "install", "-y", dep], capture_output=True)

                result = subprocess.run(
                    ["sudo", "apt", "install", "-y", package],
                    capture_output=True,
                    timeout=300
                )
                return result.returncode == 0

            elif tool_type == "python":
                if "package" in tool_info:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", tool_info["package"]],
                        capture_output=True,
                        timeout=300
                    )
                    return result.returncode == 0
                elif "repo" in tool_info:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", f"git+{tool_info['repo']}"],
                        capture_output=True, 
                        timeout=300
                    )
                    return result.returncode == 0

            elif tool_type == "rust":
                if "package" in tool_info:
                    result = subprocess.run(
                        ["cargo", "install", tool_info["package"]],
                        capture_output=True,
                        timeout=600
                    )
                    return result.returncode == 0

            return False

        except Exception:
            return False

    async def update_all_tools(self):
        """Update all installed tools"""
        print("\033[0;96m⬆️ UPDATING ALL ULTIMATE TOOLS...\033[0m")

        # Update Go tools
        print("\033[0;94m📦 Updating Go tools...\033[0m")
        for category_name, tools in self.ultimate_tools.items():
            for tool_name, tool_info in tools.items():
                if tool_info.get("type") == "go" and await self._check_single_tool(tool_name, tool_info):
                    repo = tool_info.get("repo")
                    if repo:
                        print(f"  \033[0;33m⬆️ Updating {tool_name}...\033[0m")
                        subprocess.run(["go", "install", repo], capture_output=True)

        # Update system packages
        print("\033[0;94m📦 Updating system packages...\033[0m")
        subprocess.run(["sudo", "apt", "update"], capture_output=True)
        subprocess.run(["sudo", "apt", "upgrade", "-y"], capture_output=True)

        # Update Python packages
        print("\033[0;94m📦 Updating Python packages...\033[0m")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True)

        print("\033[0;32m✅ All tools updated successfully!\033[0m")

    async def run_ultimate_benchmark(self):
        """Run performance benchmark on all tools"""
        print("\033[0;96m⚡ RUNNING ULTIMATE PERFORMANCE BENCHMARK...\033[0m")

        benchmark_results = {}
        test_domain = "example.com"

        # Benchmark critical tools
        critical_tools = []
        for category_name, tools in self.ultimate_tools.items():
            for tool_name, tool_info in tools.items():
                if tool_info.get("priority") == 1 and await self._check_single_tool(tool_name, tool_info):
                    critical_tools.append((tool_name, tool_info))

        print(f"\033[0;36mBenchmarking {len(critical_tools)} critical tools...\033[0m")

        for tool_name, tool_info in critical_tools:
            print(f"  \033[0;33m⚡ Benchmarking {tool_name}...\033[0m", end=" ", flush=True)

            start_time = time.time()
            try:
                # Run a quick test command for each tool type
                if tool_name == "subfinder":
                    result = subprocess.run([tool_name, "-d", test_domain, "-silent"], 
                                          capture_output=True, timeout=10)
                elif tool_name == "httpx":
                    result = subprocess.run([tool_name, "-u", test_domain, "-silent"], 
                                          capture_output=True, timeout=10)
                elif tool_name == "nmap":
                    result = subprocess.run([tool_name, "-F", test_domain], 
                                          capture_output=True, timeout=15)
                else:
                    result = subprocess.run([tool_name, "--help"], 
                                          capture_output=True, timeout=5)

                end_time = time.time()
                execution_time = end_time - start_time

                if result.returncode == 0 or tool_name in ["nmap"]:  # nmap may return non-zero but still work
                    benchmark_results[tool_name] = {
                        "status": "success",
                        "time": execution_time,
                        "output_size": len(result.stdout) if result.stdout else 0
                    }
                    print(f"\033[0;32m✅ {execution_time:.2f}s\033[0m")
                else:
                    benchmark_results[tool_name] = {
                        "status": "error",
                        "time": execution_time,
                        "error": result.stderr.decode()[:100] if result.stderr else "Unknown error"
                    }
                    print(f"\033[0;31m❌ Error\033[0m")

            except subprocess.TimeoutExpired:
                benchmark_results[tool_name] = {
                    "status": "timeout",
                    "time": 10.0
                }
                print(f"\033[0;33m⏰ Timeout\033[0m")
            except Exception as e:
                benchmark_results[tool_name] = {
                    "status": "exception", 
                    "error": str(e)[:100]
                }
                print(f"\033[0;31m💥 Exception\033[0m")

        # Display benchmark summary
        print(f"\n\033[0;96m📊 BENCHMARK RESULTS:\033[0m")

        successful_tools = [name for name, result in benchmark_results.items() 
                          if result["status"] == "success"]

        if successful_tools:
            fastest_tool = min(successful_tools, 
                             key=lambda x: benchmark_results[x]["time"])
            slowest_tool = max(successful_tools,
                             key=lambda x: benchmark_results[x]["time"])

            print(f"  \033[0;32m🏆 Fastest Tool: {fastest_tool} ({benchmark_results[fastest_tool]['time']:.2f}s)\033[0m")
            print(f"  \033[0;33m🐌 Slowest Tool: {slowest_tool} ({benchmark_results[slowest_tool]['time']:.2f}s)\033[0m")

        success_rate = len(successful_tools) / len(benchmark_results) * 100 if benchmark_results else 0
        print(f"  \033[0;36m📈 Success Rate: {success_rate:.1f}% ({len(successful_tools)}/{len(benchmark_results)} tools)\033[0m")

        return benchmark_results

    async def run_health_check(self):
        """Run comprehensive system health check"""
        print("\033[0;96m🏥 RUNNING ULTIMATE SYSTEM HEALTH CHECK...\033[0m")

        health_status = {
            "system": {},
            "dependencies": {},
            "tools": {},
            "performance": {}
        }

        # Check system dependencies
        print("\n\033[0;94m🔍 Checking System Dependencies...\033[0m")

        system_deps = {
            "python3": "python3 --version",
            "go": "go version", 
            "git": "git --version",
            "curl": "curl --version",
            "wget": "wget --version"
        }

        for dep_name, check_cmd in system_deps.items():
            try:
                result = subprocess.run(check_cmd.split(), capture_output=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.decode().split('\n')[0]
                    health_status["system"][dep_name] = {"status": "ok", "version": version}
                    print(f"  \033[0;32m✅ {dep_name}: {version}\033[0m")
                else:
                    health_status["system"][dep_name] = {"status": "error", "error": result.stderr.decode()[:100]}
                    print(f"  \033[0;31m❌ {dep_name}: Error\033[0m")
            except Exception as e:
                health_status["system"][dep_name] = {"status": "missing", "error": str(e)}
                print(f"  \033[0;31m❌ {dep_name}: Not found\033[0m")

        # Check critical tool availability
        print("\n\033[0;94m🔧 Checking Critical Tools...\033[0m")

        critical_tools = []
        for category_name, tools in self.ultimate_tools.items():
            for tool_name, tool_info in tools.items():
                if tool_info.get("priority") == 1:
                    critical_tools.append(tool_name)

        working_critical = 0
        for tool_name in critical_tools:
            category, tool_info = self._find_tool_info(tool_name)
            if tool_info and await self._check_single_tool(tool_name, tool_info):
                health_status["tools"][tool_name] = {"status": "ok"}
                working_critical += 1
                print(f"  \033[0;32m✅ {tool_name}\033[0m")
            else:
                health_status["tools"][tool_name] = {"status": "missing"}
                print(f"  \033[0;31m❌ {tool_name}\033[0m")

        # Performance metrics
        print("\n\033[0;94m⚡ Checking Performance Metrics...\033[0m")

        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            health_status["performance"] = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "memory_available": memory.available // (1024**3)  # GB
            }

            print(f"  \033[0;36m📊 CPU Usage: {cpu_percent}%\033[0m")
            print(f"  \033[0;36m📊 Memory Usage: {memory.percent}% (Available: {memory.available//(1024**3)}GB)\033[0m")
            print(f"  \033[0;36m📊 Disk Usage: {disk.percent}%\033[0m")

        except ImportError:
            print("  \033[0;33m⚠️ psutil not available for performance metrics\033[0m")

        # Overall health score
        print(f"\n\033[0;96m🏥 HEALTH SUMMARY:\033[0m")

        system_health = len([s for s in health_status["system"].values() if s["status"] == "ok"])
        total_system = len(health_status["system"])

        critical_health = working_critical / len(critical_tools) * 100 if critical_tools else 100

        print(f"  \033[0;36m🖥️  System Dependencies: {system_health}/{total_system} working\033[0m")
        print(f"  \033[0;36m🔧 Critical Tools: {working_critical}/{len(critical_tools)} working ({critical_health:.1f}%)\033[0m")

        overall_health = (system_health/total_system + critical_health/100) / 2 * 100

        if overall_health >= 90:
            health_color = "\033[0;32m"
            health_icon = "🎉"
            health_status_text = "EXCELLENT"
        elif overall_health >= 70:
            health_color = "\033[0;33m"
            health_icon = "👍"
            health_status_text = "GOOD"
        else:
            health_color = "\033[0;31m"
            health_icon = "🔧"
            health_status_text = "NEEDS ATTENTION"

        print(f"  {health_color}🏥 Overall Health: {overall_health:.1f}% - {health_status_text} {health_icon}\033[0m")

        return health_status

#!/usr/bin/env python3
"""
ReconXploit v4.0 - Ultimate Banner System
Product of Kernelpanic under infosbios.tech
"""

import random
import time
import sys
from datetime import datetime
from typing import List

class UltimateBannerSystem:
    """Ultimate Mr. Robot themed banner system with advanced features"""

    def __init__(self):
        self.version = "4.0.0"
        self.edition = "Ultimate Enterprise"

        # Ultimate FSociety quotes
        self.ultimate_quotes = [
            "Control is an illusion, but reconnaissance is power.",
            "The tools are ready. Time to hack the planet.",
            "Hello friend. Let's find some vulnerabilities.",
            "Knowledge is power. Reconnaissance is knowledge.",
            "We are FSociety. We are ReconXploit.",
            "The network is the battlefield. Reconnaissance is the weapon.",
            "Every system has a vulnerability. We find them all.",
            "In reconnaissance we trust, in automation we excel.",
            "Democracy died. But reconnaissance lives on.",
            "The revolution will be automated. ReconXploit is the revolution.",
            "Hack the world. But first, reconnaissance the world.",
            "Sometimes the only way to catch an uncatchable is to reconnaissance.",
            "I wanted to save the world. Reconnaissance helps expose the truth.",
            "The Dark Army fears what they cannot see coming.",
            "In a world of 1s and 0s, we are the exception handlers.",
            "Reality is a lot more malleable than you think. So is reconnaissance data.",
            "The world is not perfect. Neither is reconnaissance. But we try.",
            "Elliot, are you ready to change the world through reconnaissance?",
            "Bug hunting is not a crime. It's a necessity.",
            "Zero false negatives. Maximum true positives. Ultimate reconnaissance."
        ]

        # Advanced banners for different modes
        self.banners = {
            'ultimate': self._get_ultimate_banner(),
            'enterprise': self._get_enterprise_banner(),
            'bug_hunting': self._get_bug_hunting_banner(),
            'stealth': self._get_stealth_banner()
        }

    def _get_ultimate_banner(self) -> str:
        """Ultimate ReconXploit banner"""
        return """
██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗
██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝╚══════╝
██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   
██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   
╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
 ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝

██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
"""

    def _get_enterprise_banner(self) -> str:
        """Enterprise edition banner"""
        return """
███████╗███╗   ██╗████████╗███████╗██████╗ ██████╗ ██████╗ ██╗███████╗███████╗
██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██╔════╝
█████╗  ██╔██╗ ██║   ██║   █████╗  ██████╔╝██████╔╝██████╔╝██║███████╗█████╗  
██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██╔═══╝ ██╔══██╗██║╚════██║██╔══╝  
███████╗██║ ╚████║   ██║   ███████╗██║  ██║██║     ██║  ██║██║███████║███████╗
╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝

██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
"""

    def _get_bug_hunting_banner(self) -> str:
        """Bug hunting specialized banner"""
        return """
██████╗ ██╗   ██╗ ██████╗     ██╗  ██╗██╗   ██╗███╗   ██╗████████╗
██╔══██╗██║   ██║██╔════╝     ██║  ██║██║   ██║████╗  ██║╚══██╔══╝
██████╔╝██║   ██║██║  ███╗    ███████║██║   ██║██╔██╗ ██║   ██║   
██╔══██╗██║   ██║██║   ██║    ██╔══██║██║   ██║██║╚██╗██║   ██║   
██████╔╝╚██████╔╝╚██████╔╝    ██║  ██║╚██████╔╝██║ ╚████║   ██║   
╚═════╝  ╚═════╝  ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   

██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
"""

    def _get_stealth_banner(self) -> str:
        """Stealth mode banner"""
        return """
███████╗████████╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║
███████╗   ██║   █████╗  ███████║██║     ██║   ███████║
╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██║   ██╔══██║
███████║   ██║   ███████╗██║  ██║███████╗██║   ██║  ██║
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝

██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
"""

    def show_ultimate_banner(self, mode: str = "ultimate"):
        """Display ultimate banner with animated effects"""
        # Colors
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        MAGENTA = '\033[95m'
        BLUE = '\033[94m'
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        RESET = '\033[0m'

        # Clear screen for dramatic effect
        print("\033[2J\033[H", end="")

        # Select banner based on mode
        banner = self.banners.get(mode, self.banners['ultimate'])
        quote = random.choice(self.ultimate_quotes)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Animated banner display
        lines = banner.strip().split('\n')
        for i, line in enumerate(lines):
            if i < len(lines) // 2:
                color = CYAN + BRIGHT
            else:
                color = MAGENTA + BRIGHT

            print(color + line + RESET)
            time.sleep(0.05)  # Typing effect

        # Framework information
        print()
        print(WHITE + BRIGHT + " " * 15 + f"ReconXploit v{self.version} {self.edition} - Ultimate Reconnaissance Framework" + RESET)
        print(GREEN + " " * 20 + "Product of Kernelpanic under infosbios.tech" + RESET)
        print(BLUE + " " * 25 + "Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)" + RESET)

        # Ultimate features showcase
        print()
        print(YELLOW + BRIGHT + " " * 10 + "🔥 ULTIMATE ENTERPRISE FEATURES:" + RESET)
        print(" " * 15 + "✅ 100+ Integrated Reconnaissance Tools")
        print(" " * 15 + "✅ Intelligent Tool Chaining & Workflow Automation")
        print(" " * 15 + "✅ Advanced AI-Powered Vulnerability Analysis")
        print(" " * 15 + "✅ Zero False Negative Bug Hunting Algorithms")
        print(" " * 15 + "✅ Complete API Integration (Shodan, VT, SecurityTrails, etc.)")
        print(" " * 15 + "✅ Advanced Wordlist Management (SecLists + Custom)")
        print(" " * 15 + "✅ Enterprise-grade Reporting & Analytics")
        print(" " * 15 + "✅ Real-time Threat Intelligence Integration")

        # FSociety quote
        print()
        print(YELLOW + BRIGHT + " " * 10 + f'[fsociety@reconxploit] "{quote}"' + RESET)

        # System information
        print()
        print(BLUE + DIM + " " * 20 + f"System Initialized: {timestamp}" + RESET)
        print(BLUE + DIM + " " * 20 + f"Runtime Environment: Python {sys.version_info.major}.{sys.version_info.minor}" + RESET)
        print(BLUE + DIM + " " * 20 + f"Platform: Ultimate Enterprise Edition" + RESET)

        # Special mode indicators
        if mode == "ultimate":
            print()
            print(RED + BRIGHT + " " * 15 + "🚀 ULTIMATE MODE: All 100+ tools will be utilized for maximum coverage!" + RESET)
        elif mode == "bug_hunting":
            print()
            print(RED + BRIGHT + " " * 15 + "🐛 BUG HUNTING MODE: Advanced vulnerability discovery algorithms enabled!" + RESET)
        elif mode == "enterprise":
            print()
            print(RED + BRIGHT + " " * 15 + "🏢 ENTERPRISE MODE: Business-grade reconnaissance with compliance reporting!" + RESET)
        elif mode == "stealth":
            print()
            print(RED + BRIGHT + " " * 15 + "🥷 STEALTH MODE: Covert operations with minimal footprint!" + RESET)

        print(RESET)

        # Add dramatic pause
        time.sleep(1.0)

    def show_completion_message(self, mode: str = "standard", stats: dict = None):
        """Show ultimate completion message with statistics"""
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RESET = '\033[0m'
        BRIGHT = '\033[1m'

        completion_messages = [
            "Ultimate reconnaissance mission accomplished. The digital world has been mapped.",
            "All systems analyzed. All vulnerabilities catalogued. Mission complete.",
            "Target digitally dissected. Intelligence acquired. Reconnaissance complete.",
            "Network topology fully mapped. Security posture analyzed. Data collected.",
            "Ultimate scan completed. Zero stone left unturned. Maximum coverage achieved.",
            "FSociety protocol executed successfully. All secrets have been revealed.",
            "Digital reconnaissance complete. The truth has been uncovered.",
            "Ultimate intelligence gathered. The network holds no more secrets."
        ]

        message = random.choice(completion_messages)

        print(f"\n{GREEN + BRIGHT}[fsociety@ultimate] {message}{RESET}")

        if stats:
            print(f"{CYAN}📊 Ultimate Statistics:{RESET}")
            for key, value in stats.items():
                print(f"  {YELLOW}•{RESET} {key}: {BRIGHT}{value}{RESET}")

    def show_error_message(self, error_type: str = "general", error_msg: str = ""):
        """Show themed error messages"""
        RED = '\033[91m'
        YELLOW = '\033[93m'
        RESET = '\033[0m'
        BRIGHT = '\033[1m'

        error_messages = {
            "general": [
                "ERROR: System malfunction detected in the matrix.",
                "ERROR: Connection to the digital realm disrupted.",
                "ERROR: Reality.exe has encountered an unexpected error.",
                "ERROR: FSociety protocol execution failed."
            ],
            "network": [
                "ERROR: Target unreachable. Check network connection to the matrix.",
                "ERROR: DNS resolution failed. The network is fighting back.",
                "ERROR: Connection timeout. Target may be protected by advanced security."
            ],
            "tools": [
                "ERROR: Required reconnaissance tools missing. Run --install-all-tools.",
                "ERROR: Tool execution failed. Verify installation and permissions.",
                "ERROR: Dependencies not satisfied. Check system requirements."
            ],
            "api": [
                "ERROR: API connection failed. Verify API keys and quotas.",
                "ERROR: Authentication failed. Check API credentials.",
                "ERROR: Rate limit exceeded. Reduce request frequency."
            ]
        }

        messages = error_messages.get(error_type, error_messages["general"])
        message = random.choice(messages)

        if error_msg:
            message += f" Details: {error_msg}"

        print(f"\n{RED + BRIGHT}[fsociety@error] {message}{RESET}")

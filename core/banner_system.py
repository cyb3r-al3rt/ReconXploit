#!/usr/bin/env python3
"""
ReconXploit v3.0 - Mr. Robot Themed Banner System
Product of Kernelpanic under infosbios.tech
"""

import random
import time
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback ANSI colors if colorama not available
    class Fore:
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[0m'

    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        RESET_ALL = '\033[0m'

class BannerSystem:
    """Mr. Robot themed banner system with dynamic ASCII art"""

    def __init__(self):
        self.version = "3.0.0"
        self.author = "cyb3r-ssrf"
        self.organization = "Kernelpanic"
        self.website = "infosbios.tech"

        self.banners = [
            self._get_main_banner(),
            self._get_compact_banner(),
            self._get_matrix_banner()
        ]

        self.quotes = [
            "Control is an illusion, but reconnaissance is power.",
            "The tools are ready. Time to hack the planet.",
            "In reconnaissance we trust, in automation we excel.", 
            "Hello friend. Let's find some vulnerabilities.",
            "Knowledge is power. Reconnaissance is knowledge.",
            "We are FSociety. We are ReconXploit.",
            "The network is the battlefield. Reconnaissance is the weapon.",
            "Sometimes the only way to catch an uncatchable is to reconnaissance.",
            "I wanted to save the world. Reconnaissance helps expose the truth.",
            "The revolution will be automated. ReconXploit is the revolution.",
            "Hack the world. But first, reconnaissance the world.",
            "Every system has a vulnerability. We find them all.",
            "Democracy died. But reconnaissance lives on.",
            "The Dark Army fears what they cannot see coming.",
            "In a world of 1s and 0s, we are the exception handlers."
        ]

    def _get_main_banner(self):
        """Main ReconXploit banner"""
        return """
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
"""

    def _get_compact_banner(self):
        """Compact banner for smaller terminals"""
        return """
    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝

                  ██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
                  ╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
                   ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
                   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
                  ██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
                  ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
"""

    def _get_matrix_banner(self):
        """Matrix-style banner"""
        return """
    ╔══════════════════════════════════════════════════════════════════╗
    ║  ██▀▀▀▀▀ ██▀▀▀▀▀ ██▀▀▀▀▀ ██▀▀▀▀▀ ██▀▀▀██ ██▀▀▀██ ██▀▀▀██         ║
    ║  ██▄▄▄▄▄ ██▄▄▄▄▄ ██      ██▄▄▄▄▄ ██   ██ ██   ██ ██▄▄▄▄▄         ║
    ║  ██▀▀▀██ ██▀▀▀▀▀ ██      ██▀▀▀██ ██   ██ ██   ██ ██▀▀▀██         ║
    ║  ██   ██ ██▄▄▄▄▄ ██▄▄▄▄▄ ██▄▄▄██ ██▄▄▄██ ██   ██ ██   ██         ║
    ║                                                                  ║
    ║           ██▀▀▀██ ██▀▀▀██ ██      ██▄▄▄▄▄ ██▄▄▄██ ████████       ║
    ║           ╚██▄▄██ ██▄▄▄██ ██      ██▄▄▄▄▄ ██▄▄▄██ ╚══██▀▀        ║
    ║            ╚███▀  ██▀▀▀██ ██      ██▀▀▀██ ██▀▀▀██    ██          ║
    ║           ██▄▄██▄ ██   ██ ██▄▄▄▄▄ ██▄▄▄██ ██   ██    ██          ║
    ╚══════════════════════════════════════════════════════════════════╝
"""

    def show_banner(self):
        """Display random banner with quote and system info"""
        # Select random banner and quote
        banner = random.choice(self.banners)
        quote = random.choice(self.quotes)

        # Current time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print banner with colors
        print(Fore.CYAN + Style.BRIGHT + banner)
        print(Fore.WHITE + Style.BRIGHT + " " * 20 + f"ReconXploit v{self.version} - Advanced Reconnaissance Framework")
        print(Fore.GREEN + " " * 25 + f"Product of {self.organization} under {self.website}")
        print()
        print(Fore.YELLOW + Style.BRIGHT + " " * 15 + f'[fsociety] "{quote}"')
        print()
        print(Fore.BLUE + Style.DIM + " " * 30 + f"Initialized: {timestamp}")
        print(Fore.BLUE + Style.DIM + " " * 28 + f"Author: {self.author} | Runtime: Python")
        print(Style.RESET_ALL)

        # Add a small delay for dramatic effect
        time.sleep(0.5)

    def show_minimal_banner(self):
        """Show minimal banner for quiet mode"""
        print(f"{Fore.CYAN}ReconXploit v{self.version}{Style.RESET_ALL} - {random.choice(self.quotes)}")

    def show_completion_message(self):
        """Show completion message with fsociety style"""
        completion_messages = [
            "Mission accomplished. The network has been mapped.",
            "Reconnaissance complete. Knowledge is power.",
            "Target analyzed. Vulnerabilities catalogued.",  
            "Network topology exposed. Information gathered.",
            "Digital footprint analyzed. Intelligence acquired.",
            "Perimeter breached. Intelligence collected.",
            "System reconnaissance complete. Data acquired.",
            "Network analysis finished. Prepare for infiltration."
        ]

        message = random.choice(completion_messages)
        print(f"\n{Fore.GREEN + Style.BRIGHT}[fsociety] {message}{Style.RESET_ALL}")

    def show_error_message(self, error_type="general"):
        """Show themed error message"""
        error_messages = {
            "general": [
                "ERROR: System malfunction detected.",
                "ERROR: Connection to matrix lost.",
                "ERROR: Reality.exe has stopped working.",
                "ERROR: Hack the planet protocol failed."
            ],
            "network": [
                "ERROR: Target unreachable. Check network connection.",
                "ERROR: DNS resolution failed. Try different resolver.",
                "ERROR: Connection timeout. Increase timeout value."
            ],
            "tools": [
                "ERROR: Required tools missing. Run --check-tools.",
                "ERROR: Tool execution failed. Check installation.",
                "ERROR: Dependencies not satisfied. See documentation."
            ]
        }

        messages = error_messages.get(error_type, error_messages["general"])
        message = random.choice(messages)
        print(f"\n{Fore.RED + Style.BRIGHT}[fsociety] {message}{Style.RESET_ALL}")

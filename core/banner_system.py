#!/usr/bin/env python3
"""
ReconXploit v3.0 - Mr. Robot Themed Banner System
Product of Kernelpanic under infosbios.tech
"""

import random
from colorama import init, Fore, Style
init(autoreset=True)

class BannerSystem:
    def __init__(self):
        self.banners = [
            """
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
            """,
            """
        ████████████████████████████████████████████████████████████
        ██                                                        ██
        ██  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗          ██
        ██  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║          ██
        ██  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║          ██
        ██  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║          ██
        ██  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║          ██
        ██  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝          ██
        ██                                                        ██
        ████████████████████████████████████████████████████████████
            """
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
        ]

    def show_banner(self):
        """Display random banner with quote"""
        banner = random.choice(self.banners)
        quote = random.choice(self.quotes)

        print(Fore.CYAN + Style.BRIGHT + banner)
        print(Fore.WHITE + Style.BRIGHT + "                      ReconXploit v3.0 - Advanced Reconnaissance Framework")
        print(Fore.GREEN + "                   Product of Kernelpanic under infosbios.tech")
        print(Fore.YELLOW + f"                   \"[fsociety] {quote}\"")
        print(Style.RESET_ALL)

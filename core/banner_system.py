#!/usr/bin/env python3
"""
ReconXploit v3.0 - Banner System
Product of Kernelpanic under infosbios.tech
"""

import random
import time
from datetime import datetime

class BannerSystem:
    """Mr. Robot themed banner system"""

    def __init__(self):
        self.version = "3.0.0"
        self.quotes = [
            "Control is an illusion, but reconnaissance is power.",
            "The tools are ready. Time to hack the planet.",
            "Hello friend. Let's find some vulnerabilities.",
            "Knowledge is power. Reconnaissance is knowledge.", 
            "We are FSociety. We are ReconXploit.",
            "The network is the battlefield. Reconnaissance is the weapon.",
            "Every system has a vulnerability. We find them all.",
            "In reconnaissance we trust, in automation we excel."
        ]

    def show_banner(self):
        """Display Mr. Robot themed banner"""
        banner = """
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
"""

        quote = random.choice(self.quotes)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Colors using ANSI escape codes
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        BRIGHT = '\033[1m'
        RESET = '\033[0m'

        print(CYAN + BRIGHT + banner + RESET)
        print(WHITE + BRIGHT + f"                    ReconXploit v{self.version} - Advanced Reconnaissance Framework" + RESET)
        print(GREEN + "                      Product of Kernelpanic under infosbios.tech" + RESET)
        print()
        print(YELLOW + BRIGHT + f'                        [fsociety] "{quote}"' + RESET)
        print()
        print(BLUE + f"                           Initialized: {timestamp}" + RESET)
        print()

        # Small delay for dramatic effect
        time.sleep(0.3)

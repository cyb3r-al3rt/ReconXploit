#!/usr/bin/env python3
"""
ReconXploit v3.0 - Banner System
Product of Kernelpanic under infosbios.tech
"""

import random
import time
import sys
from datetime import datetime

class BannerSystem:
    """Professional banner system"""

    def __init__(self):
        self.version = "3.0.0"
        self.edition = "Professional Edition"

        # Professional quotes
        self.quotes = [
            "Control is an illusion, but reconnaissance is power.",
            "The network is the battlefield. Intelligence is the weapon.",
            "Every system has vulnerabilities. We find them all.",
            "In reconnaissance we trust, in automation we excel.",
            "Knowledge is power. Reconnaissance is knowledge.",
            "Bug hunting is not a crime. It is a necessity.",
            "Security through obscurity is not security at all.",
            "The best hackers are those who think like defenders.",
            "Reconnaissance is the art of seeing the invisible.",
            "In the digital realm, information is the ultimate currency."
        ]

    def show_banner(self):
        """Display ReconXploit banner"""
        # Colors
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        BRIGHT = '\033[1m'
        RESET = '\033[0m'

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

        print(CYAN + BRIGHT + banner + RESET)
        print(WHITE + BRIGHT + "           ReconXploit v" + self.version + " " + self.edition + " - Professional Reconnaissance Framework" + RESET)
        print(GREEN + "                     Product of Kernelpanic under infosbios.tech" + RESET)
        print(BLUE + "                       Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)" + RESET)
        print()
        print(YELLOW + BRIGHT + "           🔥 PROFESSIONAL FEATURES:" + RESET)
        print("                     ✅ Advanced Subdomain Enumeration")
        print("                     ✅ Live Host Detection & Analysis")  
        print("                     ✅ Comprehensive Port Scanning")
        print("                     ✅ Vulnerability Assessment")
        print("                     ✅ Professional HTML Reports")
        print("                     ✅ Multi-format Export (JSON/CSV)")
        print()
        print(YELLOW + BRIGHT + f'           [fsociety@reconxploit] "{quote}"' + RESET)
        print()
        print(BLUE + "                     System Initialized: " + timestamp + RESET)
        print(BLUE + f"                     Runtime: Python {sys.version_info.major}.{sys.version_info.minor}" + RESET)
        print(RESET)

        # Add pause for effect
        time.sleep(1.0)

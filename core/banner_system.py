#!/usr/bin/env python3
"""
ReconXploit v3.0 - Mr. Robot Banner System
Product of Kernelpanic under infosbios.tech
"""

import random
import time
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class BannerSystem:
    """Mr. Robot themed banner and quote system"""

    def __init__(self):
        self.version = "3.0.0"
        self.banners = self._load_banners()
        self.quotes = self._load_quotes()

    def _load_banners(self):
        """Load ASCII art banners"""
        banners = []

        # Main ReconXploit banner
        banner1 = """
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
        """

        banners.append(banner1)
        return banners

    def _load_quotes(self):
        """Load Mr. Robot quotes"""
        quotes = [
            "Hello friend. Hello friend? That's lame.",
            "Control is an illusion.",
            "We are all living in each other's paranoia.",
            "The world itself's just one big hoax.",
            "Sometimes I dream about saving the world.",
            "The only way to patch a vulnerability is by exposing it first.",
            "We are everywhere. We are legion.",
            "Power belongs to the people that take it.",
            "I am Mr. Robot.",
            "Are you a one or a zero? That's the question you have to ask yourself.",
            "Every hack starts with reconnaissance.",
            "In the digital age, privacy is the new freedom.",
            "Sometimes the most important recon happens in the shadows.",
            "Every vulnerability is a story waiting to be told.",
            "The best hackers are the ones you never hear about.",
            "Information is power, but information warfare is art.",
            "In reconnaissance, patience is your greatest weapon.",
            "The network is the battlefield.",
            "Every subdomain is a potential door.",
            "Automation is just organized laziness, and that's beautiful.",
            "In cybersecurity, paranoia is professionalism.",
            "The quieter you become, the more you can hear."
        ]
        return quotes

    def get_random_banner(self):
        """Get a random banner"""
        return random.choice(self.banners)

    def get_random_quote(self):
        """Get a random Mr. Robot quote"""
        return random.choice(self.quotes)

    def show_banner(self):
        """Display animated banner with quote"""
        print(Fore.CYAN + Style.BRIGHT + self.get_random_banner())

        # Product branding
        print(Fore.GREEN + Style.BRIGHT + "               Advanced Reconnaissance Automation Framework v" + self.version)
        print(Fore.YELLOW + "                    Product of Kernelpanic under infosbios.tech")
        print(Fore.RED + Style.BRIGHT + "                        Developed by cyb3r-ssrf")

        # Random quote
        quote = self.get_random_quote()
        print()
        print(Fore.MAGENTA + f"[fsociety] {quote}")
        print()

        # Status indicators
        self._show_status()

    def _show_status(self):
        """Show system status"""
        print(Fore.WHITE + "━" * 80)
        print(Fore.CYAN + "[STATUS] Initializing ReconXploit framework...")

        # Simulate loading
        statuses = [
            "Loading tool integrations...",
            "Checking wordlists...", 
            "Verifying API keys...",
            "Initializing workflow engine...",
            "Framework ready!"
        ]

        for status in statuses:
            print(Fore.GREEN + f"[INFO] {status}")
            time.sleep(0.3)

        print(Fore.WHITE + "━" * 80)
        print()

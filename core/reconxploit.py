#!/usr/bin/env python3
"""
ReconXploit v3.0 - Advanced Reconnaissance Automation Framework
Product of Kernelpanic under infosbios.tech
Author: Muhammad Ismaeel Shareef S S (cyb3r-ssrf)

A comprehensive reconnaissance framework integrating 100+ security tools
with intelligent workflow management and Mr. Robot themed interface.
"""

import os
import sys
import argparse
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Import core modules
from core.banner_system import BannerSystem
from core.workflow_engine import WorkflowEngine
from core.config_manager import ConfigManager
from core.tool_manager import ToolManager
from core.result_processor import ResultProcessor
from core.report_generator import ReportGenerator

class ReconXploit:
    """Main ReconXploit framework class"""

    def __init__(self):
        self.version = "3.0.0"
        self.banner_system = BannerSystem()
        self.config_manager = ConfigManager()
        self.tool_manager = ToolManager()
        self.workflow_engine = WorkflowEngine()
        self.result_processor = ResultProcessor()
        self.report_generator = ReportGenerator()

        # Setup logging
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/reconxploit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def display_banner(self):
        """Display Mr. Robot themed banner"""
        self.banner_system.show_banner()

    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="ReconXploit v3.0 - Advanced Reconnaissance Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  reconxploit -d example.com                    # Basic reconnaissance
  reconxploit -d example.com --full            # Full comprehensive scan
  reconxploit -d example.com --passive         # Passive reconnaissance only
  reconxploit -d example.com --output json     # JSON output format
  reconxploit --wordlist-sync                  # Sync wordlists
  reconxploit --setup-keys                     # Setup API keys
            """
        )

        # Target specification
        parser.add_argument('-d', '--domain', type=str, help='Target domain for reconnaissance')
        parser.add_argument('-l', '--list', type=str, help='File containing list of domains')
        parser.add_argument('--scope', type=str, help='Scope file for bug bounty programs')

        # Scan types
        parser.add_argument('--passive', action='store_true', help='Passive reconnaissance only')
        parser.add_argument('--active', action='store_true', help='Active reconnaissance (default)')
        parser.add_argument('--full', action='store_true', help='Full comprehensive scan')
        parser.add_argument('--quick', action='store_true', help='Quick scan mode')

        # Output options
        parser.add_argument('--output', choices=['json', 'csv', 'html', 'pdf', 'xml'], 
                           default='html', help='Output format')
        parser.add_argument('--output-dir', type=str, default='results', 
                           help='Output directory')

        # Configuration
        parser.add_argument('--config', type=str, default='config/config.yaml',
                           help='Configuration file path')
        parser.add_argument('--threads', type=int, default=50, 
                           help='Number of threads for parallel processing')
        parser.add_argument('--timeout', type=int, default=30,
                           help='Timeout for individual tools')

        # Workflow control
        parser.add_argument('--skip-subdomain', action='store_true', 
                           help='Skip subdomain enumeration')
        parser.add_argument('--skip-port-scan', action='store_true',
                           help='Skip port scanning')
        parser.add_argument('--skip-vulnerability', action='store_true',
                           help='Skip vulnerability scanning')

        # Utilities
        parser.add_argument('--wordlist-sync', action='store_true',
                           help='Sync wordlists from external sources')
        parser.add_argument('--setup-keys', action='store_true',
                           help='Setup API keys interactively')
        parser.add_argument('--check-tools', action='store_true',
                           help='Check tool installation status')
        parser.add_argument('--update-tools', action='store_true',
                           help='Update installed tools')

        # Debugging
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        parser.add_argument('--verbose', '-v', action='store_true', 
                           help='Verbose output')

        return parser.parse_args()

    async def run_reconnaissance(self, args):
        """Main reconnaissance workflow"""
        try:
            self.logger.info(f"Starting reconnaissance for: {args.domain}")

            # Load configuration
            config = self.config_manager.load_config(args.config)

            # Initialize workflow
            workflow = self.workflow_engine.create_workflow(args, config)

            # Execute workflow
            results = await self.workflow_engine.execute(workflow)

            # Process results
            processed_results = self.result_processor.process(results)

            # Generate reports
            await self.report_generator.generate(processed_results, args)

            self.logger.info("Reconnaissance completed successfully")
            return processed_results

        except Exception as e:
            self.logger.error(f"Reconnaissance failed: {str(e)}")
            if args.debug:
                raise
            return None

    async def setup_api_keys(self):
        """Interactive API key setup"""
        from scripts.setup_api_keys import setup_keys_interactive
        await setup_keys_interactive()

    async def sync_wordlists(self):
        """Sync wordlists from external sources"""
        self.logger.info("Starting wordlist synchronization...")
        # Implementation for wordlist sync
        pass

    async def check_tools(self):
        """Check tool installation status"""
        self.logger.info("Checking tool installation status...")
        status = self.tool_manager.check_all_tools()

        for category, tools in status.items():
            print(f"\n[{category.upper()}]")
            for tool, installed in tools.items():
                status_icon = "✓" if installed else "✗"
                print(f"  {status_icon} {tool}")

    async def main(self):
        """Main entry point"""
        args = self.parse_arguments()

        # Always display banner first
        self.display_banner()

        # Handle utility commands
        if args.setup_keys:
            await self.setup_api_keys()
            return

        if args.wordlist_sync:
            await self.sync_wordlists()
            return

        if args.check_tools:
            await self.check_tools()
            return

        # Validate target
        if not args.domain and not args.list:
            print("\n[ERROR] Please specify a target domain (-d) or domain list (-l)")
            return

        # Run reconnaissance
        results = await self.run_reconnaissance(args)

        if results:
            print(f"\n[SUCCESS] Reconnaissance completed. Results saved to: {args.output_dir}")
        else:
            print("\n[ERROR] Reconnaissance failed. Check logs for details.")

if __name__ == "__main__":
    try:
        reconxploit = ReconXploit()
        asyncio.run(reconxploit.main())
    except KeyboardInterrupt:
        print("\n[INFO] Reconnaissance interrupted by user")
    except Exception as e:
        print(f"\n[FATAL] {str(e)}")
        sys.exit(1)

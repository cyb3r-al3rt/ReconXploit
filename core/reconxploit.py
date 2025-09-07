#!/usr/bin/env python3
"""
ReconXploit v3.0 - Advanced Reconnaissance Framework
Product of Kernelpanic under infosbios.tech
Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)
"""

import os
import sys
import argparse
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Fix imports - Add current directory to Python path
current_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(current_dir))

# Import core modules with error handling
try:
    from core.banner_system import BannerSystem
    from core.tool_manager import ToolManager
    from core.workflow_engine import WorkflowEngine
    from core.result_processor import ResultProcessor  
    from core.report_generator import ReportGenerator
    from core.config_manager import ConfigManager
except ImportError as e:
    print(f"\033[0;31m[CRITICAL ERROR]\033[0m Missing core module: {e}")
    print("\033[0;33m[FIX]\033[0m Ensure all files are present in core/ directory")
    sys.exit(1)

class ReconXploit:
    """Main ReconXploit application class"""

    def __init__(self):
        self.version = "3.0.0"
        self.banner_system = BannerSystem()
        self.tool_manager = ToolManager()
        self.workflow_engine = WorkflowEngine()
        self.result_processor = ResultProcessor()
        self.report_generator = ReportGenerator()
        self.config_manager = ConfigManager()

    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="ReconXploit v3.0 - Advanced Reconnaissance Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  ./reconxploit -d example.com                 # Basic reconnaissance
  ./reconxploit -d example.com --passive      # Passive reconnaissance  
  ./reconxploit -d example.com --full         # Full comprehensive scan
  ./reconxploit --check-tools                 # Check tool status

Product of Kernelpanic under infosbios.tech
"Control is an illusion, but reconnaissance is power."
            """
        )

        # Target specification
        parser.add_argument('-d', '--domain', type=str, help='Target domain for reconnaissance')
        parser.add_argument('-l', '--list', type=str, help='File containing list of domains')

        # Scan types
        parser.add_argument('--passive', action='store_true', help='Passive reconnaissance only')
        parser.add_argument('--active', action='store_true', help='Active reconnaissance (default)')
        parser.add_argument('--full', action='store_true', help='Full comprehensive scan')
        parser.add_argument('--quick', action='store_true', help='Quick scan mode')

        # Output options
        parser.add_argument('--output', choices=['json', 'csv', 'html'], default='html', 
                           help='Output format (default: html)')
        parser.add_argument('--output-dir', type=str, default='results', 
                           help='Output directory (default: results)')

        # Performance
        parser.add_argument('--threads', type=int, default=50, 
                           help='Number of threads (default: 50)')
        parser.add_argument('--timeout', type=int, default=30,
                           help='Timeout in seconds (default: 30)')

        # Workflow control
        parser.add_argument('--skip-subdomain', action='store_true', help='Skip subdomain enumeration')
        parser.add_argument('--skip-port-scan', action='store_true', help='Skip port scanning')
        parser.add_argument('--skip-vulnerability', action='store_true', help='Skip vulnerability scanning')

        # Utilities
        parser.add_argument('--check-tools', action='store_true', help='Check tool installation status')
        parser.add_argument('--update-tools', action='store_true', help='Update installed tools')

        # Debug
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
        parser.add_argument('--silent', action='store_true', help='Silent mode')

        return parser.parse_args()

    async def run_reconnaissance(self, args):
        """Main reconnaissance workflow"""
        try:
            print(f"\033[0;36m[RECON]\033[0m Starting reconnaissance for: {args.domain}")

            # Load configuration
            config = self.config_manager.load_config()

            # Create workflow
            workflow = self.workflow_engine.create_workflow(args, config)

            # Execute reconnaissance
            results = await self.workflow_engine.execute(workflow)

            # Process results
            processed_results = self.result_processor.process(results)

            # Generate reports
            await self.report_generator.generate(processed_results, args)

            print(f"\033[0;32m[SUCCESS]\033[0m Reconnaissance completed successfully")
            return processed_results

        except Exception as e:
            print(f"\033[0;31m[ERROR]\033[0m Reconnaissance failed: {str(e)}")
            if args.debug:
                import traceback
                traceback.print_exc()
            return None

    async def check_tools(self):
        """Check tool installation status"""
        print("\n" + "="*60)
        print("\033[0;36m🔍 ReconXploit v3.0 - Tool Installation Status\033[0m")
        print("="*60)

        status = self.tool_manager.check_all_tools()

        total_available = 0
        total_tools = 0

        for category, tools in status.items():
            available = sum(tools.values())
            total = len(tools)
            percentage = (available/total*100) if total > 0 else 0

            # Category header
            category_name = category.replace('_', ' ').title()
            if percentage >= 80:
                color = "\033[0;32m"  # Green
                icon = "✅"
            elif percentage >= 50:
                color = "\033[0;33m"  # Yellow
                icon = "⚠️"
            else:
                color = "\033[0;31m"  # Red
                icon = "❌"

            print(f"\n{color}[{icon} {category_name}] {available}/{total} ({percentage:.0f}%)\033[0m")

            # Individual tools
            for tool, installed in sorted(tools.items()):
                if installed:
                    version = self.tool_manager.get_tool_version(tool)
                    print(f"  \033[0;32m✅\033[0m {tool:<20} - {version}")
                    total_available += 1
                else:
                    print(f"  \033[0;31m❌\033[0m {tool:<20} - Not Found")
                total_tools += 1

        # Overall summary
        overall_percentage = (total_available/total_tools*100) if total_tools > 0 else 0
        print(f"\n{'='*60}")

        if overall_percentage >= 90:
            summary_color = "\033[0;32m"
            summary_icon = "🎉"
            summary_text = "Excellent"
        elif overall_percentage >= 70:
            summary_color = "\033[0;33m"
            summary_icon = "👍"
            summary_text = "Good"
        else:
            summary_color = "\033[0;31m"
            summary_icon = "🔧"
            summary_text = "Needs Work"

        print(f"{summary_color}{summary_icon} Overall Status: {total_available}/{total_tools} tools ({overall_percentage:.1f}%) - {summary_text}\033[0m")

        if total_available < total_tools:
            print(f"\n\033[0;36m💡 Installation Help:\033[0m")
            print("Go tools: go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")
            print("System tools: sudo apt install nmap gobuster curl")
            print("Rust tools: cargo install feroxbuster")

    async def main(self):
        """Main entry point"""
        try:
            args = self.parse_arguments()

            # Display banner (unless silent)
            if not args.silent:
                self.banner_system.show_banner()

            # Handle utility commands
            if args.check_tools:
                await self.check_tools()
                return 0

            # Validate input
            if not args.domain and not args.list:
                print("\n\033[0;31m❌ [ERROR]\033[0m Please specify a target domain (-d) or domain list (-l)")
                print("\n\033[0;36mExamples:\033[0m")
                print("  ./reconxploit -d example.com")
                print("  ./reconxploit -d example.com --passive")
                print("  ./reconxploit --check-tools")
                print("  ./reconxploit --help")
                return 1

            # Run reconnaissance
            if not args.silent:
                print(f"\n\033[0;36m🚀 Starting ReconXploit v{self.version}\033[0m")

            results = await self.run_reconnaissance(args)

            if results:
                if not args.silent:
                    summary = results.get('summary', {})
                    print(f"\n\033[0;32m✅ [SUCCESS]\033[0m Reconnaissance completed!")
                    print(f"\033[0;36m📁 Results:\033[0m {args.output_dir}")
                    print(f"\033[0;36m📊 Found:\033[0m {summary.get('subdomains_found', 0)} subdomains, {summary.get('live_hosts_found', 0)} live hosts")
                return 0
            else:
                print("\n\033[0;31m❌ [ERROR]\033[0m Reconnaissance failed")
                return 1

        except KeyboardInterrupt:
            print("\n\n\033[0;33m⚡ [INTERRUPTED]\033[0m Reconnaissance interrupted by user")
            return 130
        except Exception as e:
            print(f"\n\033[0;31m💥 [FATAL ERROR]\033[0m {str(e)}")
            if hasattr(args, 'debug') and args.debug:
                import traceback
                traceback.print_exc()
            return 1

if __name__ == "__main__":
    reconxploit = ReconXploit()
    exit_code = asyncio.run(reconxploit.main())
    sys.exit(exit_code)

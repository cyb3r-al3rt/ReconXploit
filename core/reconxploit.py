#!/usr/bin/env python3
"""
ReconXploit v3.0 - Advanced Reconnaissance Automation Framework
Product of Kernelpanic under infosbios.tech
Author: Muhammad Ismaeel Shareef S S (cyb3r-ssrf)
"""

import os
import sys
import argparse
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Fix Python path and imports
current_dir = Path(__file__).parent.parent.resolve()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(current_dir) + ':' + os.environ.get('PYTHONPATH', '')

# Import with error handling
try:
    from core.banner_system import BannerSystem
    from core.workflow_engine import WorkflowEngine
    from core.tool_manager import ToolManager
    from core.result_processor import ResultProcessor
    from core.report_generator import ReportGenerator
    from core.config_manager import ConfigManager
except ImportError as e:
    print(f"\033[0;31m[ERROR]\033[0m Failed to import ReconXploit modules: {e}")
    print(f"\033[0;33m[INFO]\033[0m Current directory: {current_dir}")
    print(f"\033[0;33m[INFO]\033[0m Python path: {sys.path}")
    print(f"\033[0;33m[FIX]\033[0m Please run from ReconXploit directory or check installation")
    sys.exit(1)

class ReconXploit:
    """Main ReconXploit framework class"""

    def __init__(self):
        self.version = "3.0.0"
        self.banner_system = BannerSystem()
        self.tool_manager = ToolManager()
        self.workflow_engine = WorkflowEngine()
        self.result_processor = ResultProcessor()
        self.report_generator = ReportGenerator()
        self.config_manager = ConfigManager()

        # Setup logging
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = current_dir / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"reconxploit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
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
  reconxploit --check-tools                    # Check tool installation
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
        parser.add_argument('--output', choices=['json', 'csv', 'html', 'pdf', 'xml'], 
                           default='html', help='Output format')
        parser.add_argument('--output-dir', type=str, default='results', 
                           help='Output directory')

        # Configuration
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

            # Create workflow configuration
            config = {}
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
        try:
            api_setup_path = current_dir / "scripts/setup_api_keys.py"
            if api_setup_path.exists():
                os.system(f"python3 {api_setup_path}")
            else:
                print("\033[0;33m[WARNING]\033[0m API setup script not found.")
        except Exception as e:
            print(f"\033[0;31m[ERROR]\033[0m Error setting up API keys: {e}")

    async def check_tools(self):
        """Check tool installation status"""
        self.logger.info("Checking tool installation status...")
        status = self.tool_manager.check_all_tools()

        print("\n" + "="*60)
        print("\033[0;36mReconXploit v3.0 - Tool Installation Status\033[0m")
        print("="*60)

        total_available = 0
        total_tools = 0

        for category, tools in status.items():
            print(f"\n\033[1;34m[{category.upper().replace('_', ' ')}]\033[0m")
            for tool, installed in tools.items():
                status_icon = "\033[0;32m✅\033[0m" if installed else "\033[0;31m❌\033[0m"
                status_text = "\033[0;32mAvailable\033[0m" if installed else "\033[0;31mMissing\033[0m"
                print(f"  {status_icon} {tool:<20} - {status_text}")
                total_tools += 1
                if installed:
                    total_available += 1

        # Summary
        success_rate = (total_available / total_tools * 100) if total_tools > 0 else 0
        print(f"\n{'='*60}")
        print(f"\033[1;36mSummary: {total_available}/{total_tools} tools available ({success_rate:.1f}%)\033[0m")

        if total_available < total_tools:
            print("\n\033[0;33m🔧 To install missing tools:\033[0m")
            print("   sudo apt install -y libpcap-dev")
            print("   go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest")
            print("   go install github.com/hahwul/dalfox/v2@latest")
            print("   wget https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster-linux-x86_64.tar.gz")
            print("   tar -xzf feroxbuster-linux-x86_64.tar.gz && sudo mv feroxbuster /usr/local/bin/")

    async def main(self):
        """Main entry point"""
        args = self.parse_arguments()

        # Always display banner first
        self.display_banner()

        # Handle utility commands
        if args.setup_keys:
            await self.setup_api_keys()
            return

        if args.check_tools:
            await self.check_tools()
            return

        # Validate target
        if not args.domain and not args.list:
            print("\n\033[0;31m❌ [ERROR]\033[0m Please specify a target domain (-d) or domain list (-l)")
            print("\nExamples:")
            print("  reconxploit -d example.com")
            print("  reconxploit -l domains.txt") 
            print("  reconxploit --help")
            return

        # Run reconnaissance
        results = await self.run_reconnaissance(args)

        if results:
            print(f"\n\033[0;32m✅ [SUCCESS]\033[0m Reconnaissance completed. Results saved to: {args.output_dir}")
        else:
            print("\n\033[0;31m❌ [ERROR]\033[0m Reconnaissance failed. Check logs for details.")

if __name__ == "__main__":
    try:
        reconxploit = ReconXploit()
        asyncio.run(reconxploit.main())
    except KeyboardInterrupt:
        print("\n\n\033[0;33m⚡ [INFO]\033[0m Reconnaissance interrupted by user")
    except Exception as e:
        print(f"\n\033[0;31m💥 [FATAL]\033[0m {str(e)}")
        sys.exit(1)

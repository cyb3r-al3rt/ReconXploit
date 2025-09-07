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

# Fix Python path and imports - CRITICAL FIX
current_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(current_dir))

# Set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(current_dir) + ':' + os.environ.get('PYTHONPATH', '')

# Import with comprehensive error handling
try:
    from core.banner_system import BannerSystem
    from core.workflow_engine import WorkflowEngine
    from core.tool_manager import ToolManager
    from core.result_processor import ResultProcessor
    from core.report_generator import ReportGenerator
    from core.config_manager import ConfigManager
except ImportError as e:
    print(f"\033[0;31m[CRITICAL ERROR]\033[0m Failed to import ReconXploit modules: {e}")
    print(f"\033[0;33m[PATH INFO]\033[0m Current directory: {current_dir}")
    print(f"\033[0;33m[PATH INFO]\033[0m Python path: {':'.join(sys.path)}")
    print(f"\033[0;32m[FIX]\033[0m Ensure you're running from ReconXploit directory")
    print(f"\033[0;32m[FIX]\033[0m All __init__.py files should be present in core/ and tools/")
    sys.exit(1)

class ReconXploit:
    """Main ReconXploit framework class - Complete Implementation"""

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
        """Setup comprehensive logging"""
        log_dir = current_dir / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"reconxploit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
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
        """Parse command line arguments with full options"""
        parser = argparse.ArgumentParser(
            description="ReconXploit v3.0 - Advanced Reconnaissance Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  reconxploit -d example.com                    # Basic reconnaissance
  reconxploit -d example.com --full            # Full comprehensive scan
  reconxploit -d example.com --passive         # Passive reconnaissance only
  reconxploit -l domains.txt --threads 100     # Multiple domains with custom threads
  reconxploit --check-tools                    # Check tool installation status
  reconxploit --setup-keys                     # Setup API keys interactively

Workflow Control:
  reconxploit -d example.com --skip-port-scan  # Skip port scanning
  reconxploit -d example.com --skip-vulnerability # Skip vulnerability scanning

Output Formats:
  reconxploit -d example.com --output json     # JSON output
  reconxploit -d example.com --output html     # HTML dashboard (default)
  reconxploit -d example.com --output csv      # CSV format

Product of Kernelpanic under infosbios.tech
"Control is an illusion, but reconnaissance is power."
            """
        )

        # Target specification
        parser.add_argument('-d', '--domain', type=str, 
                           help='Target domain for reconnaissance')
        parser.add_argument('-l', '--list', type=str, 
                           help='File containing list of domains')
        parser.add_argument('--scope', type=str, 
                           help='Scope file for bug bounty programs')

        # Scan types
        parser.add_argument('--passive', action='store_true', 
                           help='Passive reconnaissance only (no active scanning)')
        parser.add_argument('--active', action='store_true', 
                           help='Active reconnaissance (default)')
        parser.add_argument('--full', action='store_true', 
                           help='Full comprehensive scan (all tools)')
        parser.add_argument('--quick', action='store_true', 
                           help='Quick scan mode (essential tools only)')

        # Output options
        parser.add_argument('--output', choices=['json', 'csv', 'html', 'pdf', 'xml'], 
                           default='html', help='Output format (default: html)')
        parser.add_argument('--output-dir', type=str, default='results', 
                           help='Output directory (default: results)')

        # Performance configuration
        parser.add_argument('--threads', type=int, default=50, 
                           help='Number of threads for parallel processing (default: 50)')
        parser.add_argument('--timeout', type=int, default=30,
                           help='Timeout for individual tools in seconds (default: 30)')
        parser.add_argument('--delay', type=float, default=0,
                           help='Delay between requests in seconds (default: 0)')

        # Tool configuration
        parser.add_argument('--config', type=str, default='config/config.yaml',
                           help='Configuration file path')
        parser.add_argument('--wordlist', type=str,
                           help='Custom wordlist for content discovery')
        parser.add_argument('--resolvers', type=str,
                           help='Custom DNS resolvers file')

        # Workflow control
        parser.add_argument('--skip-subdomain', action='store_true', 
                           help='Skip subdomain enumeration')
        parser.add_argument('--skip-port-scan', action='store_true',
                           help='Skip port scanning')
        parser.add_argument('--skip-vulnerability', action='store_true',
                           help='Skip vulnerability scanning')
        parser.add_argument('--skip-content', action='store_true',
                           help='Skip content discovery')
        parser.add_argument('--skip-parameter', action='store_true',
                           help='Skip parameter discovery')

        # Tool selection
        parser.add_argument('--use-nuclei', action='store_true',
                           help='Force use Nuclei for vulnerability scanning')
        parser.add_argument('--use-naabu', action='store_true',
                           help='Force use Naabu for port scanning')
        parser.add_argument('--use-feroxbuster', action='store_true',
                           help='Force use Feroxbuster for directory fuzzing')

        # Utilities
        parser.add_argument('--setup-keys', action='store_true',
                           help='Setup API keys interactively')
        parser.add_argument('--check-tools', action='store_true',
                           help='Check tool installation status')
        parser.add_argument('--update-tools', action='store_true',
                           help='Update installed tools')
        parser.add_argument('--install-tools', action='store_true',
                           help='Install missing tools automatically')

        # Advanced options
        parser.add_argument('--proxy', type=str,
                           help='HTTP proxy (e.g., http://127.0.0.1:8080)')
        parser.add_argument('--user-agent', type=str,
                           help='Custom User-Agent string')
        parser.add_argument('--headers', type=str,
                           help='Custom headers file')

        # Debugging and verbosity
        parser.add_argument('--debug', action='store_true', 
                           help='Enable debug mode')
        parser.add_argument('--verbose', '-v', action='store_true', 
                           help='Verbose output')
        parser.add_argument('--silent', action='store_true',
                           help='Silent mode (minimal output)')

        return parser.parse_args()

    async def run_reconnaissance(self, args):
        """Main reconnaissance workflow execution"""
        try:
            self.logger.info(f"Starting reconnaissance for: {args.domain}")

            # Load configuration
            config = self.config_manager.load_config(args.config)

            # Create and execute workflow
            workflow = self.workflow_engine.create_workflow(args, config)
            results = await self.workflow_engine.execute(workflow)

            # Process and correlate results
            processed_results = self.result_processor.process(results)

            # Generate comprehensive reports
            await self.report_generator.generate(processed_results, args)

            self.logger.info("Reconnaissance completed successfully")
            return processed_results

        except Exception as e:
            self.logger.error(f"Reconnaissance failed: {str(e)}")
            if args.debug:
                import traceback
                traceback.print_exc()
            return None

    async def setup_api_keys(self):
        """Interactive API key setup"""
        try:
            api_setup_path = current_dir / "scripts" / "setup_api_keys.py"
            if api_setup_path.exists():
                import subprocess
                subprocess.run([sys.executable, str(api_setup_path)], check=True)
            else:
                print("\033[0;33m[WARNING]\033[0m API setup script not found.")
                print("\033[0;36m[INFO]\033[0m You can manually configure API keys in config/api_keys.yaml")
        except Exception as e:
            print(f"\033[0;31m[ERROR]\033[0m Error setting up API keys: {e}")

    async def check_tools(self):
        """Comprehensive tool installation status check"""
        self.logger.info("Checking tool installation status...")
        status = self.tool_manager.check_all_tools()

        print("\n" + "="*70)
        print("\033[0;36m🔍 ReconXploit v3.0 - Tool Installation Status\033[0m")
        print("="*70)

        total_available = 0
        total_tools = 0
        category_stats = {}

        for category, tools in status.items():
            available = sum(tools.values())
            total = len(tools)
            category_stats[category] = {'available': available, 'total': total}

            # Display category header
            category_name = category.replace('_', ' ').title()
            percentage = (available/total*100) if total > 0 else 0

            if percentage >= 80:
                status_color = "\033[0;32m"  # Green
                status_icon = "✅"
            elif percentage >= 50:
                status_color = "\033[0;33m"  # Yellow  
                status_icon = "⚠️"
            else:
                status_color = "\033[0;31m"  # Red
                status_icon = "❌"

            print(f"\n{status_color}[{status_icon} {category_name}] {available}/{total} ({percentage:.0f}%)\033[0m")

            # Display individual tools
            for tool, installed in sorted(tools.items()):
                if installed:
                    version = self.tool_manager.get_tool_version(tool)
                    print(f"  \033[0;32m✅\033[0m {tool:<20} - \033[0;32m{version}\033[0m")
                    total_available += 1
                else:
                    print(f"  \033[0;31m❌\033[0m {tool:<20} - \033[0;31mNot Found\033[0m")
                total_tools += 1

        # Overall summary
        overall_percentage = (total_available/total_tools*100) if total_tools > 0 else 0
        print(f"\n{'='*70}")

        if overall_percentage >= 90:
            summary_color = "\033[0;32m"  # Green
            summary_icon = "🎉"
            summary_text = "Excellent"
        elif overall_percentage >= 70:
            summary_color = "\033[0;33m"  # Yellow
            summary_icon = "👍"
            summary_text = "Good"
        else:
            summary_color = "\033[0;31m"  # Red
            summary_icon = "🔧"
            summary_text = "Needs Work"

        print(f"{summary_color}{summary_icon} Overall Status: {total_available}/{total_tools} tools ({overall_percentage:.1f}%) - {summary_text}\033[0m")

        # Installation recommendations
        if total_available < total_tools:
            print(f"\n\033[0;36m🔧 Missing Tool Installation Guide:\033[0m")

            missing_go_tools = []
            missing_system_tools = []
            missing_rust_tools = []

            for category, tools in status.items():
                for tool, installed in tools.items():
                    if not installed:
                        if category == 'go_tools':
                            missing_go_tools.append(tool)
                        elif category == 'system_tools':
                            missing_system_tools.append(tool)
                        elif category == 'rust_tools':
                            missing_rust_tools.append(tool)

            if missing_system_tools:
                print(f"\n\033[0;33m📦 System packages:\033[0m")
                print(f"   sudo apt install -y {' '.join(missing_system_tools)}")

            if missing_go_tools:
                print(f"\n\033[0;33m🔧 Go tools:\033[0m")
                go_installs = {
                    'naabu': 'github.com/projectdiscovery/naabu/v2/cmd/naabu@latest',
                    'dalfox': 'github.com/hahwul/dalfox/v2@latest',
                    'subfinder': 'github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
                    'httpx': 'github.com/projectdiscovery/httpx/cmd/httpx@latest',
                    'nuclei': 'github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest'
                }

                for tool in missing_go_tools:
                    if tool in go_installs:
                        print(f"   go install {go_installs[tool]}")

                if 'naabu' in missing_go_tools:
                    print(f"   \033[0;36m# For naabu, also run:\033[0m")
                    print(f"   sudo apt install -y libpcap-dev")
                    print(f"   sudo setcap cap_net_raw,cap_net_admin+eip $(which naabu)")

            if missing_rust_tools:
                print(f"\n\033[0;33m🦀 Rust tools:\033[0m")
                print(f"   # Install Rust first: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
                for tool in missing_rust_tools:
                    if tool == 'feroxbuster':
                        print(f"   cargo install feroxbuster")
                        print(f"   # OR download binary:")
                        print(f"   wget https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster-linux-x86_64.tar.gz")
                        print(f"   tar -xzf feroxbuster-linux-x86_64.tar.gz && sudo mv feroxbuster /usr/local/bin/")

        print(f"\n\033[0;36m💡 Tip:\033[0m Run 'reconxploit --install-tools' to automatically install missing tools")
        print(f"\033[0;36m📚 Documentation:\033[0m See README.md for detailed installation guide")

    async def install_missing_tools(self):
        """Automatically install missing tools"""
        print("\033[0;36m🔧 Auto-installing missing tools...\033[0m")
        print("This feature will be implemented in a future version.")
        print("For now, please use the installation commands shown by --check-tools")

    async def main(self):
        """Main entry point with comprehensive error handling"""
        try:
            args = self.parse_arguments()

            # Set logging level based on verbosity
            if args.silent:
                logging.getLogger().setLevel(logging.ERROR)
            elif args.verbose:
                logging.getLogger().setLevel(logging.DEBUG)
            elif args.debug:
                logging.getLogger().setLevel(logging.DEBUG)

            # Always display banner first (unless silent mode)
            if not args.silent:
                self.display_banner()

            # Handle utility commands
            if args.setup_keys:
                await self.setup_api_keys()
                return

            if args.check_tools:
                await self.check_tools()
                return

            if args.install_tools:
                await self.install_missing_tools()
                return

            # Validate target input
            if not args.domain and not args.list:
                print("\n\033[0;31m❌ [ERROR]\033[0m Please specify a target domain (-d) or domain list (-l)")
                print("\n\033[0;36mExamples:\033[0m")
                print("  reconxploit -d example.com                 # Single domain")
                print("  reconxploit -l domains.txt                # Multiple domains")  
                print("  reconxploit -d example.com --passive      # Passive scan")
                print("  reconxploit -d example.com --full         # Full scan")
                print("  reconxploit --check-tools                 # Check tools")
                print("\n\033[0;36mHelp:\033[0m")
                print("  reconxploit --help                        # Show all options")
                return

            # Validate input files exist
            if args.list and not Path(args.list).exists():
                print(f"\033[0;31m❌ [ERROR]\033[0m Domain list file not found: {args.list}")
                return

            if args.scope and not Path(args.scope).exists():
                print(f"\033[0;31m❌ [ERROR]\033[0m Scope file not found: {args.scope}")
                return

            # Run reconnaissance workflow
            if not args.silent:
                print(f"\n\033[0;36m🚀 Starting ReconXploit v{self.version}\033[0m")

            results = await self.run_reconnaissance(args)

            if results:
                if not args.silent:
                    print(f"\n\033[0;32m✅ [SUCCESS]\033[0m Reconnaissance completed successfully!")
                    print(f"\033[0;36m📁 Results saved to:\033[0m {args.output_dir}")
                    print(f"\033[0;36m📊 Summary:\033[0m {results.get('summary', {})}")
            else:
                print("\n\033[0;31m❌ [ERROR]\033[0m Reconnaissance failed. Check logs for details.")
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

        return 0

if __name__ == "__main__":
    reconxploit = ReconXploit()
    exit_code = asyncio.run(reconxploit.main())
    sys.exit(exit_code)

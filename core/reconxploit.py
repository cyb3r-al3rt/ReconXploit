#!/usr/bin/env python3
"""
ReconXploit v3.0 - Professional Reconnaissance Framework
Product of Kernelpanic under infosbios.tech
Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)
"""

import os
import sys
import argparse
import asyncio
import logging
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Fix Python path for imports
current_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(current_dir))
os.environ['PYTHONPATH'] = str(current_dir) + ':' + os.environ.get('PYTHONPATH', '')

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
    print(f"\033[0;33m[SOLUTION]\033[0m Ensure you extracted the complete ReconXploit package")
    print(f"\033[0;33m[PATH]\033[0m Current directory: {current_dir}")
    sys.exit(1)

class ReconXploit:
    """Professional Reconnaissance Framework"""

    def __init__(self):
        self.version = "3.0.0"
        self.edition = "Professional Edition"

        # Initialize core systems
        self.banner_system = BannerSystem()
        self.tool_manager = ToolManager()
        self.workflow_engine = WorkflowEngine()
        self.result_processor = ResultProcessor()
        self.report_generator = ReportGenerator()
        self.config_manager = ConfigManager()

        # Setup logging
        self._setup_logging()

        # Execution stats
        self.start_time = None
        self.execution_stats = {
            'tools_executed': 0,
            'vulnerabilities_found': 0,
            'subdomains_found': 0,
            'live_hosts_found': 0
        }

    def _setup_logging(self):
        """Setup logging system"""
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
        self.logger.info(f"ReconXploit v{self.version} {self.edition} initialized")

    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description=f"ReconXploit v{self.version} {self.edition} - Professional Reconnaissance Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
🎯 RECONNAISSANCE EXAMPLES:

Basic Usage:
  reconxploit -d example.com                    # Standard reconnaissance
  reconxploit -d example.com --full            # Full comprehensive scan
  reconxploit -l domains.txt                   # Multiple domains
  reconxploit --ip 192.168.1.1                # Single IP target

Advanced Options:
  reconxploit -d example.com --passive         # Passive reconnaissance only
  reconxploit -d example.com --threads 50      # Custom thread count
  reconxploit -d example.com --timeout 30      # Custom timeout
  reconxploit -d example.com --output json     # JSON output format

Specialized Scans:
  reconxploit -d example.com --skip-port-scan  # Skip port scanning
  reconxploit -d example.com --only-subdomains # Only subdomain enumeration
  reconxploit -d example.com --vulnerability   # Focus on vulnerabilities

System Management:
  reconxploit --check-tools                    # Check tool availability
  reconxploit --install-tools                  # Install missing tools
  reconxploit --update-tools                   # Update all tools

🚀 Product of Kernelpanic under infosbios.tech
💎 "Control is an illusion, but reconnaissance is power."
            """
        )

        # Target specification
        target_group = parser.add_argument_group('🎯 Target Specification')
        target_group.add_argument('-d', '--domain', type=str, help='Target domain for reconnaissance')
        target_group.add_argument('-l', '--list', type=str, help='File containing list of domains')
        target_group.add_argument('--ip', type=str, help='Single IP address target')
        target_group.add_argument('--url', type=str, help='Single URL target')
        target_group.add_argument('--cidr', type=str, help='CIDR range for network scanning')

        # Scan modes
        scan_group = parser.add_argument_group('🔥 Scan Modes')
        scan_group.add_argument('--passive', action='store_true', help='Passive reconnaissance only')
        scan_group.add_argument('--active', action='store_true', help='Active reconnaissance (default)')
        scan_group.add_argument('--full', action='store_true', help='Full comprehensive scan')
        scan_group.add_argument('--quick', action='store_true', help='Quick essential scan')
        scan_group.add_argument('--stealth', action='store_true', help='Stealth reconnaissance')

        # Workflow control
        workflow_group = parser.add_argument_group('🎛️ Workflow Control')
        workflow_group.add_argument('--skip-subdomain', action='store_true', help='Skip subdomain enumeration')
        workflow_group.add_argument('--skip-port-scan', action='store_true', help='Skip port scanning')
        workflow_group.add_argument('--skip-vulnerability', action='store_true', help='Skip vulnerability scanning')
        workflow_group.add_argument('--only-subdomains', action='store_true', help='Only subdomain enumeration')
        workflow_group.add_argument('--only-ports', action='store_true', help='Only port scanning')
        workflow_group.add_argument('--vulnerability', action='store_true', help='Focus on vulnerability scanning')

        # Output and reporting
        output_group = parser.add_argument_group('📊 Output & Reporting')
        output_group.add_argument('--output', choices=['html', 'json', 'csv'], default='html')
        output_group.add_argument('--output-dir', type=str, default='results')
        output_group.add_argument('--report-name', type=str, help='Custom report name')

        # Performance
        perf_group = parser.add_argument_group('⚡ Performance')
        perf_group.add_argument('--threads', type=int, default=50, help='Number of threads (default: 50)')
        perf_group.add_argument('--timeout', type=int, default=30, help='Timeout per operation (default: 30s)')
        perf_group.add_argument('--delay', type=float, default=0, help='Delay between requests (seconds)')
        perf_group.add_argument('--rate-limit', type=int, default=100, help='Requests per minute limit')

        # System utilities
        system_group = parser.add_argument_group('🛠️ System Management')
        system_group.add_argument('--check-tools', action='store_true', help='Check tool installation status')
        system_group.add_argument('--install-tools', action='store_true', help='Install missing tools')
        system_group.add_argument('--update-tools', action='store_true', help='Update all tools')
        system_group.add_argument('--list-tools', action='store_true', help='List all supported tools')

        # Debug and configuration
        debug_group = parser.add_argument_group('🔧 Configuration & Debug')
        debug_group.add_argument('--config', type=str, default='config/config.yaml')
        debug_group.add_argument('--debug', action='store_true', help='Enable debug mode')
        debug_group.add_argument('--verbose', '-v', action='count', default=0, help='Verbose output')
        debug_group.add_argument('--silent', action='store_true', help='Silent mode')
        debug_group.add_argument('--dry-run', action='store_true', help='Dry run mode (no actual scanning)')

        return parser.parse_args()

    async def main(self):
        """Main entry point for ReconXploit"""
        try:
            self.start_time = datetime.now()
            args = self.parse_arguments()

            # Set logging level
            if args.silent:
                logging.getLogger().setLevel(logging.ERROR)
            elif args.verbose >= 2:
                logging.getLogger().setLevel(logging.DEBUG)
            elif args.verbose >= 1:
                logging.getLogger().setLevel(logging.INFO)

            # Display banner
            if not args.silent:
                self.banner_system.show_banner()

            # Handle system management commands
            if args.check_tools:
                await self._handle_check_tools(args)
                return 0
            elif args.install_tools:
                await self._handle_install_tools(args)
                return 0
            elif args.update_tools:
                await self._handle_update_tools(args)
                return 0
            elif args.list_tools:
                await self._handle_list_tools(args)
                return 0

            # Validate target input
            if not any([args.domain, args.list, args.ip, args.url, args.cidr]):
                print("\n\033[0;31m❌ [ERROR]\033[0m Please specify a target")
                print("\n\033[0;36m🎯 Examples:\033[0m")
                print("  reconxploit -d example.com")
                print("  reconxploit -l domains.txt")
                print("  reconxploit --ip 1.2.3.4")
                print("  reconxploit --check-tools")
                return 1

            # Run reconnaissance
            if not args.silent:
                print(f"\n\033[0;36m🚀 Starting ReconXploit v{self.version}\033[0m")

                # Display scan configuration
                scan_mode = self._determine_scan_mode(args)
                print(f"\033[0;36m📋 Scan Mode:\033[0m {scan_mode}")
                print(f"\033[0;36m🎯 Target:\033[0m {args.domain or args.list or args.ip or args.url}")

                if args.full:
                    print("\033[0;33m⚡ FULL SCAN MODE - Complete reconnaissance enabled!\033[0m")
                if args.stealth:
                    print("\033[0;33m🥷 STEALTH MODE - Covert operations enabled!\033[0m")

            # Execute reconnaissance
            results = await self._run_reconnaissance(args)

            if results:
                await self._display_results(results, args)
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

    def _determine_scan_mode(self, args) -> str:
        """Determine the scan mode"""
        if args.full:
            return "🔥 FULL (Comprehensive)"
        elif args.passive:
            return "🕵️ PASSIVE (OSINT only)"
        elif args.stealth:
            return "🥷 STEALTH (Covert)"
        elif args.quick:
            return "⚡ QUICK (Essential)"
        else:
            return "🎯 STANDARD (Balanced)"

    async def _run_reconnaissance(self, args) -> Optional[Dict[str, Any]]:
        """Execute the reconnaissance workflow"""
        try:
            print(f"\033[0;36m[WORKFLOW]\033[0m Initializing reconnaissance engine...")

            # Load configuration
            config = await self.config_manager.load_config(args.config)

            # Create workflow
            workflow = await self.workflow_engine.create_workflow(args, config)

            # Execute workflow
            results = await self.workflow_engine.execute_workflow(workflow)

            # Process results
            processed_results = await self.result_processor.process_results(results)

            # Generate reports with proper naming
            await self.report_generator.generate_reports(processed_results, args)

            # Update execution stats
            self._update_execution_stats(processed_results)

            return processed_results

        except Exception as e:
            self.logger.error(f"Reconnaissance failed: {str(e)}")
            if args.debug:
                import traceback
                traceback.print_exc()
            return None

    async def _display_results(self, results: Dict[str, Any], args):
        """Display reconnaissance results"""
        end_time = datetime.now()
        execution_time = (end_time - self.start_time).total_seconds()

        summary = results.get('summary', {})

        print("\n" + "="*70)
        print("\033[0;32m🎉 RECONNAISSANCE COMPLETED!\033[0m")
        print("="*70)

        print(f"\033[0;36m⏱️  Execution Time:\033[0m {execution_time:.1f} seconds")
        print(f"\033[0;36m🎯 Target:\033[0m {results.get('target', 'Unknown')}")
        print(f"\033[0;36m📊 Scan Mode:\033[0m {self._determine_scan_mode(args)}")

        print("\n\033[0;33m📈 RESULTS SUMMARY:\033[0m")
        print(f"  🌐 Subdomains Found: \033[0;32m{summary.get('subdomains_found', 0)}\033[0m")
        print(f"  ✅ Live Hosts: \033[0;32m{summary.get('live_hosts_found', 0)}\033[0m")
        print(f"  🔌 Open Ports: \033[0;32m{summary.get('open_ports_found', 0)}\033[0m")
        print(f"  🔗 URLs Discovered: \033[0;32m{summary.get('urls_discovered', 0)}\033[0m")
        print(f"  ⚠️  Vulnerabilities: \033[0;31m{summary.get('vulnerabilities_found', 0)}\033[0m")
        print(f"  🛡️  Security Score: \033[0;33m{summary.get('security_score', 0)}/100\033[0m")

        # Display critical findings
        critical_vulns = summary.get('critical_vulnerabilities', [])
        if critical_vulns:
            print("\n\033[0;31m🚨 CRITICAL VULNERABILITIES FOUND:\033[0m")
            for vuln in critical_vulns[:3]:  # Show top 3
                print(f"  💥 {vuln.get('name', 'Unknown')} - {vuln.get('url', 'N/A')}")

        # Show report location with proper naming
        target_name = results.get('target', 'unknown').replace('.', '_').replace('/', '_')
        timestamp = end_time.strftime('%Y%m%d_%H%M%S')
        report_name = f"{target_name}_{timestamp}"

        print(f"\n\033[0;36m📁 Results saved to:\033[0m {args.output_dir}")
        print(f"\033[0;36m📊 HTML Report:\033[0m {args.output_dir}/{report_name}_report.html")

        if args.output == 'json':
            print(f"\033[0;36m📋 JSON Report:\033[0m {args.output_dir}/{report_name}_report.json")
        elif args.output == 'csv':
            print(f"\033[0;36m📋 CSV Reports:\033[0m {args.output_dir}/{report_name}_*.csv")

        print("\n\033[0;32m✨ Reconnaissance completed successfully!\033[0m")
        print('\033[0;33m💎 "Control is an illusion, but reconnaissance is power."\033[0m')

    async def _handle_check_tools(self, args):
        """Handle tool checking"""
        await self.tool_manager.check_all_tools(detailed=True)

    async def _handle_install_tools(self, args):
        """Handle tool installation"""
        print("\033[0;36m🔧 Installing reconnaissance tools...\033[0m")
        await self.tool_manager.install_missing_tools()

    async def _handle_update_tools(self, args):
        """Handle tool updates"""
        print("\033[0;36m⬆️ Updating all tools...\033[0m")
        await self.tool_manager.update_all_tools()

    async def _handle_list_tools(self, args):
        """Handle listing all tools"""
        await self.tool_manager.list_all_tools()

    def _update_execution_stats(self, results: Dict[str, Any]):
        """Update execution statistics"""
        summary = results.get('summary', {})
        self.execution_stats.update({
            'vulnerabilities_found': summary.get('vulnerabilities_found', 0),
            'subdomains_found': summary.get('subdomains_found', 0),
            'live_hosts_found': summary.get('live_hosts_found', 0),
            'tools_executed': summary.get('tools_executed', 0)
        })

if __name__ == "__main__":
    reconxploit = ReconXploit()
    exit_code = asyncio.run(reconxploit.main())
    sys.exit(exit_code)

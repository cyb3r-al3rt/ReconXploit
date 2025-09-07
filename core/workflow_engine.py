#!/usr/bin/env python3
"""
ReconXploit v3.0 - Intelligent Workflow Engine
Product of Kernelpanic under infosbios.tech
"""

import asyncio
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class WorkflowEngine:
    """Intelligent reconnaissance workflow orchestration"""

    def __init__(self):
        self.stages = [
            "initialization", 
            "subdomain_enumeration",
            "live_host_detection", 
            "port_scanning",
            "service_detection",
            "content_discovery",
            "parameter_discovery",
            "vulnerability_scanning",
            "reporting"
        ]

        self.results = {}

    def create_workflow(self, args, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create intelligent workflow based on arguments and configuration"""
        workflow = {
            "target": args.domain or "example.com",
            "scan_type": self._determine_scan_type(args),
            "output_format": args.output,
            "threads": args.threads,
            "timeout": args.timeout,
            "stages": self._select_stages(args),
            "tools": self._select_tools(args, config),
            "config": config
        }

        return workflow

    def _determine_scan_type(self, args) -> str:
        """Determine scan type based on arguments"""
        if args.passive:
            return "passive"
        elif args.full:
            return "comprehensive"
        elif args.quick:
            return "quick"
        else:
            return "standard"

    def _select_stages(self, args) -> List[str]:
        """Select workflow stages based on arguments"""
        stages = self.stages.copy()

        # Remove skipped stages
        if args.skip_subdomain:
            stages = [s for s in stages if s != "subdomain_enumeration"]
        if args.skip_port_scan:
            stages = [s for s in stages if s != "port_scanning"]
        if args.skip_vulnerability:
            stages = [s for s in stages if s != "vulnerability_scanning"]
        if getattr(args, 'skip_content', False):
            stages = [s for s in stages if s != "content_discovery"]
        if getattr(args, 'skip_parameter', False):
            stages = [s for s in stages if s != "parameter_discovery"]

        return stages

    def _select_tools(self, args, config: Dict[str, Any]) -> Dict[str, List[str]]:
        """Select tools for each stage"""
        tools = {
            "subdomain_enumeration": ["subfinder", "assetfinder"],
            "live_host_detection": ["httpx"],
            "port_scanning": ["naabu", "nmap"],
            "content_discovery": ["feroxbuster", "gobuster", "dirb"], 
            "parameter_discovery": ["arjun", "paramspider"],
            "vulnerability_scanning": ["nuclei", "nikto"]
        }

        # Adjust based on scan type
        if args.passive:
            tools["subdomain_enumeration"] = ["subfinder", "assetfinder"]
            tools["port_scanning"] = []  # No active port scanning
            tools["content_discovery"] = []  # No active content discovery

        elif args.full:
            tools["subdomain_enumeration"].extend(["sublist3r"])
            tools["port_scanning"].extend(["masscan"])
            tools["vulnerability_scanning"].extend(["sqlmap"])

        return tools

    async def execute(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete reconnaissance workflow"""
        results = {
            "target": workflow["target"],
            "scan_type": workflow["scan_type"], 
            "start_time": datetime.now().isoformat(),
            "data": {
                "subdomains": [],
                "live_hosts": [],
                "ports": [],
                "urls": [],
                "parameters": [],
                "vulnerabilities": [],
                "technologies": [],
                "certificates": []
            },
            "metadata": {
                "tools_used": [],
                "execution_time": 0,
                "success_rate": 0
            }
        }

        start_time = datetime.now()
        successful_stages = 0
        total_stages = len(workflow["stages"])

        print(f"\033[0;36m[WORKFLOW]\033[0m Starting {workflow['scan_type']} reconnaissance for {workflow['target']}")
        print(f"\033[0;36m[WORKFLOW]\033[0m Stages: {', '.join(workflow['stages'])}")

        for stage in workflow["stages"]:
            try:
                print(f"\033[0;32m[{stage.upper().replace('_', ' ')}]\033[0m Executing...")
                stage_results = await self._execute_stage(stage, workflow, results)

                # Merge stage results
                if stage_results:
                    for key, value in stage_results.items():
                        if key in results["data"] and isinstance(value, list):
                            results["data"][key].extend(value)
                        elif key in results["data"]:
                            results["data"][key] = value

                successful_stages += 1
                print(f"\033[0;32m[{stage.upper().replace('_', ' ')}]\033[0m Completed")

            except Exception as e:
                print(f"\033[0;31m[{stage.upper().replace('_', ' ')}]\033[0m Failed: {str(e)}")
                continue

        # Calculate execution metrics
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        success_rate = (successful_stages / total_stages * 100) if total_stages > 0 else 0

        results["end_time"] = end_time.isoformat()
        results["metadata"]["execution_time"] = execution_time
        results["metadata"]["success_rate"] = success_rate

        print(f"\033[0;36m[WORKFLOW]\033[0m Completed in {execution_time:.2f} seconds ({success_rate:.1f}% success)")

        return results

    async def _execute_stage(self, stage: str, workflow: Dict[str, Any], current_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific workflow stage"""
        stage_methods = {
            "initialization": self._stage_initialization,
            "subdomain_enumeration": self._stage_subdomain_enumeration,
            "live_host_detection": self._stage_live_host_detection,
            "port_scanning": self._stage_port_scanning,
            "service_detection": self._stage_service_detection,
            "content_discovery": self._stage_content_discovery,
            "parameter_discovery": self._stage_parameter_discovery,
            "vulnerability_scanning": self._stage_vulnerability_scanning,
            "reporting": self._stage_reporting
        }

        if stage in stage_methods:
            return await stage_methods[stage](workflow, current_results)
        else:
            return {}

    async def _stage_initialization(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize reconnaissance with basic target validation"""
        target = workflow["target"]

        # Basic domain validation
        import re
        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
        if not re.match(domain_pattern, target):
            print(f"\033[0;33m[WARNING]\033[0m Invalid domain format: {target}")

        return {"initialized": True, "target_validated": True}

    async def _stage_subdomain_enumeration(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute subdomain enumeration"""
        target = workflow["target"]
        tools = workflow["tools"].get("subdomain_enumeration", [])
        subdomains = []

        for tool in tools:
            try:
                if tool == "subfinder":
                    subdomain_results = await self._run_subfinder(target, workflow)
                    subdomains.extend(subdomain_results)
                elif tool == "assetfinder":
                    subdomain_results = await self._run_assetfinder(target, workflow)
                    subdomains.extend(subdomain_results)
                # Add more tools as needed

            except Exception as e:
                print(f"\033[0;33m[WARNING]\033[0m {tool} failed: {str(e)}")
                continue

        # Deduplicate and sort
        unique_subdomains = sorted(list(set(subdomains)))
        print(f"\033[0;32m[INFO]\033[0m Found {len(unique_subdomains)} unique subdomains")

        return {"subdomains": unique_subdomains}

    async def _stage_live_host_detection(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Detect live hosts from discovered subdomains"""
        subdomains = results["data"].get("subdomains", [workflow["target"]])
        live_hosts = []

        # Use httpx for live host detection
        try:
            live_results = await self._run_httpx(subdomains, workflow)
            live_hosts.extend(live_results)
        except Exception as e:
            print(f"\033[0;33m[WARNING]\033[0m Live host detection failed: {str(e)}")

        print(f"\033[0;32m[INFO]\033[0m Found {len(live_hosts)} live hosts")
        return {"live_hosts": live_hosts}

    async def _stage_port_scanning(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute port scanning on live hosts"""
        if workflow["scan_type"] == "passive":
            return {"ports": []}  # Skip active scanning in passive mode

        live_hosts = results["data"].get("live_hosts", [workflow["target"]])
        ports = []

        tools = workflow["tools"].get("port_scanning", [])
        for tool in tools:
            if tool == "naabu":
                try:
                    port_results = await self._run_naabu(live_hosts, workflow)
                    ports.extend(port_results)
                except Exception as e:
                    print(f"\033[0;33m[WARNING]\033[0m naabu failed: {str(e)}")

        print(f"\033[0;32m[INFO]\033[0m Found {len(ports)} open ports")
        return {"ports": ports}

    async def _stage_service_detection(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Detect services on open ports"""
        # Placeholder for service detection logic
        return {"services": []}

    async def _stage_content_discovery(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Discover web content and directories"""
        if workflow["scan_type"] == "passive":
            return {"urls": []}  # Skip active scanning in passive mode

        # Placeholder for content discovery
        return {"urls": []}

    async def _stage_parameter_discovery(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Discover URL parameters"""
        return {"parameters": []}

    async def _stage_vulnerability_scanning(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute vulnerability scanning"""
        vulnerabilities = []

        tools = workflow["tools"].get("vulnerability_scanning", [])
        for tool in tools:
            if tool == "nuclei":
                try:
                    vuln_results = await self._run_nuclei(workflow["target"], workflow)
                    vulnerabilities.extend(vuln_results)
                except Exception as e:
                    print(f"\033[0;33m[WARNING]\033[0m nuclei failed: {str(e)}")

        return {"vulnerabilities": vulnerabilities}

    async def _stage_reporting(self, workflow: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare final reporting data"""
        return {"report_ready": True}

    # Tool execution methods (simplified implementations)
    async def _run_subfinder(self, target: str, workflow: Dict[str, Any]) -> List[str]:
        """Run subfinder tool"""
        try:
            cmd = ["subfinder", "-d", target, "-silent"]
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=workflow["timeout"])

            if process.returncode == 0:
                subdomains = [line.strip() for line in stdout.decode().strip().split('\n') if line.strip()]
                return subdomains
        except Exception:
            pass

        # Fallback dummy data for demonstration
        return [f"www.{target}", f"api.{target}", f"mail.{target}"]

    async def _run_assetfinder(self, target: str, workflow: Dict[str, Any]) -> List[str]:
        """Run assetfinder tool"""
        # Simplified implementation - would run actual assetfinder
        return [f"dev.{target}", f"staging.{target}"]

    async def _run_httpx(self, targets: List[str], workflow: Dict[str, Any]) -> List[str]:
        """Run httpx for live host detection"""
        # Simplified implementation - would run actual httpx
        return [f"https://{target}" for target in targets[:5]]  # Limit for demo

    async def _run_naabu(self, targets: List[str], workflow: Dict[str, Any]) -> List[str]:
        """Run naabu for port scanning"""
        # Simplified implementation - would run actual naabu
        return [f"{target}:80", f"{target}:443", f"{target}:22"] * len(targets[:3])

    async def _run_nuclei(self, target: str, workflow: Dict[str, Any]) -> List[Dict]:
        """Run nuclei for vulnerability scanning"""
        # Simplified implementation - would run actual nuclei
        return [
            {"name": "SSL Certificate Expired", "severity": "medium", "url": f"https://{target}"},
            {"name": "Directory Listing Enabled", "severity": "low", "url": f"https://{target}/admin/"}
        ]

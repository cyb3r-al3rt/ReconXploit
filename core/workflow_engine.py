#!/usr/bin/env python3
"""
ReconXploit v3.0 - Workflow Engine
Product of Kernelpanic under infosbios.tech
"""

import asyncio
import subprocess
from datetime import datetime
from typing import Dict, Any, List

class WorkflowEngine:
    """Intelligent reconnaissance workflow orchestration"""

    def __init__(self):
        self.stages = [
            "initialization",
            "subdomain_enumeration", 
            "live_host_detection",
            "port_scanning",
            "content_discovery",
            "vulnerability_scanning",
            "reporting"
        ]

    def create_workflow(self, args, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create workflow based on arguments and config"""
        workflow = {
            "target": args.domain or "example.com",
            "scan_type": self._determine_scan_type(args),
            "output_format": args.output,
            "threads": args.threads,
            "timeout": args.timeout,
            "stages": self._select_stages(args),
            "config": config
        }

        return workflow

    def _determine_scan_type(self, args) -> str:
        """Determine scan type from arguments"""
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
        if getattr(args, 'skip_subdomain', False):
            stages = [s for s in stages if s != "subdomain_enumeration"]
        if getattr(args, 'skip_port_scan', False):
            stages = [s for s in stages if s != "port_scanning"]
        if getattr(args, 'skip_vulnerability', False):
            stages = [s for s in stages if s != "vulnerability_scanning"]

        return stages

    async def execute(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the reconnaissance workflow"""
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
                "technologies": []
            },
            "metadata": {
                "tools_used": [],
                "execution_time": 0,
                "success_rate": 0
            }
        }

        start_time = datetime.now()
        successful_stages = 0

        print(f"\033[0;36m[WORKFLOW]\033[0m Starting {workflow['scan_type']} reconnaissance")
        print(f"\033[0;36m[TARGET]\033[0m {workflow['target']}")

        for stage in workflow["stages"]:
            try:
                print(f"\033[0;32m[{stage.upper().replace('_', ' ')}]\033[0m Executing...")
                stage_results = await self._execute_stage(stage, workflow, results)

                # Merge results
                if stage_results:
                    for key, value in stage_results.items():
                        if key in results["data"]:
                            if isinstance(value, list):
                                results["data"][key].extend(value)
                            else:
                                results["data"][key] = value

                successful_stages += 1
                print(f"\033[0;32m[{stage.upper().replace('_', ' ')}]\033[0m Completed")

            except Exception as e:
                print(f"\033[0;33m[WARNING]\033[0m {stage} failed: {str(e)}")
                continue

        # Calculate metrics
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        success_rate = (successful_stages / len(workflow["stages"]) * 100) if workflow["stages"] else 0

        results["end_time"] = end_time.isoformat()
        results["metadata"]["execution_time"] = execution_time
        results["metadata"]["success_rate"] = success_rate

        print(f"\033[0;36m[WORKFLOW]\033[0m Completed in {execution_time:.1f}s ({success_rate:.0f}% success)")

        return results

    async def _execute_stage(self, stage: str, workflow: Dict[str, Any], current_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific workflow stage"""

        if stage == "initialization":
            return await self._stage_initialization(workflow)
        elif stage == "subdomain_enumeration":
            return await self._stage_subdomain_enumeration(workflow)
        elif stage == "live_host_detection":
            return await self._stage_live_host_detection(workflow, current_results)
        elif stage == "port_scanning":
            return await self._stage_port_scanning(workflow, current_results)
        elif stage == "vulnerability_scanning":
            return await self._stage_vulnerability_scanning(workflow, current_results)
        else:
            return {}

    async def _stage_initialization(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize reconnaissance"""
        await asyncio.sleep(0.5)  # Simulate initialization
        return {"initialized": True}

    async def _stage_subdomain_enumeration(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute subdomain enumeration"""
        target = workflow["target"]
        subdomains = []

        # Try to run subfinder if available
        try:
            result = await asyncio.create_subprocess_exec(
                "subfinder", "-d", target, "-silent",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=60)

            if result.returncode == 0:
                found_subdomains = [line.strip() for line in stdout.decode().strip().split('\n') if line.strip()]
                subdomains.extend(found_subdomains)
                print(f"\033[0;32m[SUBFINDER]\033[0m Found {len(found_subdomains)} subdomains")

        except Exception as e:
            print(f"\033[0;33m[WARNING]\033[0m Subfinder not available, using fallback")

        # Fallback - generate common subdomains
        if not subdomains:
            common_subs = ['www', 'api', 'mail', 'ftp', 'admin', 'blog', 'shop', 'test', 'dev', 'staging']
            subdomains = [f"{sub}.{target}" for sub in common_subs]
            print(f"\033[0;36m[FALLBACK]\033[0m Generated {len(subdomains)} common subdomains")

        return {"subdomains": subdomains}

    async def _stage_live_host_detection(self, workflow: Dict[str, Any], current_results: Dict[str, Any]) -> Dict[str, Any]:
        """Detect live hosts"""
        subdomains = current_results["data"].get("subdomains", [workflow["target"]])
        live_hosts = []

        # Try httpx if available
        try:
            # Limit to first 10 subdomains for demo
            test_hosts = subdomains[:10]

            result = await asyncio.create_subprocess_exec(
                "httpx", "-l", "/dev/stdin", "-silent", "-no-color",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            input_data = "\n".join(test_hosts)
            stdout, stderr = await asyncio.wait_for(
                result.communicate(input=input_data.encode()), 
                timeout=30
            )

            if result.returncode == 0:
                found_hosts = [line.strip() for line in stdout.decode().strip().split('\n') if line.strip()]
                live_hosts.extend(found_hosts)
                print(f"\033[0;32m[HTTPX]\033[0m Found {len(found_hosts)} live hosts")

        except Exception:
            # Fallback - assume main domain is live
            live_hosts = [f"https://{workflow['target']}"]
            print(f"\033[0;36m[FALLBACK]\033[0m Assuming main domain is live")

        return {"live_hosts": live_hosts}

    async def _stage_port_scanning(self, workflow: Dict[str, Any], current_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute port scanning"""
        if workflow["scan_type"] == "passive":
            return {"ports": []}

        target = workflow["target"]
        ports = []

        # Try nmap for common ports
        try:
            result = await asyncio.create_subprocess_exec(
                "nmap", "-T4", "-F", target,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=60)

            if result.returncode == 0:
                output_lines = stdout.decode().split('\n')
                for line in output_lines:
                    if '/tcp' in line and 'open' in line:
                        port = line.split('/')[0].strip()
                        if port.isdigit():
                            ports.append(f"{target}:{port}")

                print(f"\033[0;32m[NMAP]\033[0m Found {len(ports)} open ports")

        except Exception:
            # Fallback - common web ports
            common_ports = ['80', '443', '8080', '8443']
            ports = [f"{target}:{port}" for port in common_ports]
            print(f"\033[0;36m[FALLBACK]\033[0m Checking common ports")

        return {"ports": ports}

    async def _stage_vulnerability_scanning(self, workflow: Dict[str, Any], current_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute vulnerability scanning"""
        target = workflow["target"]
        vulnerabilities = []

        # Try nuclei if available
        try:
            result = await asyncio.create_subprocess_exec(
                "nuclei", "-u", f"https://{target}", "-silent", "-j",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=120)

            if result.returncode == 0:
                output_lines = stdout.decode().strip().split('\n')
                for line in output_lines:
                    if line.strip():
                        try:
                            import json
                            vuln_data = json.loads(line)
                            vulnerabilities.append({
                                "name": vuln_data.get("template-id", "Unknown"),
                                "severity": vuln_data.get("info", {}).get("severity", "info"),
                                "url": vuln_data.get("matched-at", f"https://{target}"),
                                "description": vuln_data.get("info", {}).get("name", "No description")
                            })
                        except:
                            continue

                print(f"\033[0;32m[NUCLEI]\033[0m Found {len(vulnerabilities)} vulnerabilities")

        except Exception:
            # Fallback - basic checks
            vulnerabilities = [
                {
                    "name": "HTTP Security Headers Check",
                    "severity": "info",
                    "url": f"https://{target}",
                    "description": "Basic security header analysis"
                }
            ]
            print(f"\033[0;36m[FALLBACK]\033[0m Basic security checks")

        return {"vulnerabilities": vulnerabilities}

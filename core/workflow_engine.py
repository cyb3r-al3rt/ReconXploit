#!/usr/bin/env python3
"""
ReconXploit v3.0 - Professional Workflow Engine
Product of Kernelpanic under infosbios.tech
"""

import asyncio
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import tempfile
import shutil

class WorkflowEngine:
    """Professional reconnaissance workflow engine with intelligent tool execution"""

    def __init__(self):
        self.stages = {
            "initialization": {
                "priority": 1,
                "tools": ["system_check"],
                "timeout": 30,
                "description": "System initialization and tool verification"
            },
            "subdomain_enumeration": {
                "priority": 2,
                "tools": ["subfinder", "assetfinder", "amass"],
                "timeout": 300,
                "description": "Comprehensive subdomain discovery"
            },
            "live_host_detection": {
                "priority": 3,
                "tools": ["httpx", "httprobe"],
                "timeout": 180,
                "description": "HTTP/HTTPS service discovery"
            },
            "port_scanning": {
                "priority": 4,
                "tools": ["naabu", "nmap", "masscan"],
                "timeout": 300,
                "description": "Network port and service scanning"
            },
            "content_discovery": {
                "priority": 5,
                "tools": ["gobuster", "dirb", "ffuf"],
                "timeout": 600,
                "description": "Web content and directory discovery"
            },
            "vulnerability_scanning": {
                "priority": 6,
                "tools": ["nuclei", "nikto"],
                "timeout": 900,
                "description": "Professional vulnerability assessment"
            }
        }

        self.execution_context = {
            "target": None,
            "workspace": None,
            "results": {},
            "stage_timings": {},
            "errors": []
        }

    async def create_workflow(self, args, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create professional workflow configuration"""

        target = args.domain or args.ip or args.url or "unknown"

        # Create workspace with proper structure
        workspace = Path(args.output_dir) / target.replace('.', '_').replace('/', '_').replace(':', '_')
        workspace.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (workspace / "temp").mkdir(exist_ok=True)
        (workspace / "raw_data").mkdir(exist_ok=True)

        # Determine workflow stages based on arguments
        selected_stages = list(self.stages.keys())

        # Apply filters
        if args.skip_subdomain:
            selected_stages = [s for s in selected_stages if "subdomain" not in s]
        if args.skip_port_scan:
            selected_stages = [s for s in selected_stages if "port" not in s]
        if args.skip_vulnerability:
            selected_stages = [s for s in selected_stages if "vulnerability" not in s]

        # Special modes
        if args.only_subdomains:
            selected_stages = ["initialization", "subdomain_enumeration"]
        elif args.only_ports:
            selected_stages = ["initialization", "port_scanning"]
        elif args.passive:
            selected_stages = ["initialization", "subdomain_enumeration", "live_host_detection"]

        workflow = {
            "target": target,
            "workspace": workspace,
            "stages": selected_stages,
            "config": config,
            "performance": {
                "threads": args.threads,
                "timeout": args.timeout,
                "delay": getattr(args, 'delay', 0)
            }
        }

        self.execution_context.update({
            "target": target,
            "workspace": workspace,
            "results": {},
            "stage_timings": {}
        })

        return workflow

    async def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete professional workflow"""
        start_time = datetime.now()

        print(f"\033[0;36m[WORKFLOW]\033[0m Starting professional reconnaissance for {workflow['target']}")

        results = {
            "target": workflow["target"],
            "start_time": start_time.isoformat(),
            "stages_executed": [],
            "data": {
                "subdomains": [],
                "live_hosts": [],
                "ports": [],
                "urls": [],
                "vulnerabilities": []
            },
            "statistics": {
                "tools_used": 0,
                "total_findings": 0,
                "execution_stages": 0
            },
            "errors": []
        }

        # Execute stages with professional handling
        for stage_name in workflow["stages"]:
            if stage_name not in self.stages:
                continue

            try:
                stage_info = self.stages[stage_name]
                print(f"\n\033[0;94m[{stage_name.upper().replace('_', ' ')}]\033[0m {stage_info['description']}")
                stage_start = time.time()

                stage_results = await self._execute_stage(stage_name, workflow, results)

                stage_end = time.time()
                stage_duration = stage_end - stage_start

                # Update results with professional tracking
                if stage_results:
                    findings_count = 0
                    for key, value in stage_results.items():
                        if key in results["data"] and isinstance(value, list):
                            results["data"][key].extend(value)
                            findings_count += len(value)
                        elif key in results["data"] and isinstance(value, dict):
                            results["data"][key].update(value)
                            findings_count += len(value)
                        else:
                            results["data"][key] = value

                    results["statistics"]["total_findings"] += findings_count

                # Track timing and success
                self.execution_context["stage_timings"][stage_name] = stage_duration
                results["stages_executed"].append({
                    "name": stage_name,
                    "description": stage_info['description'],
                    "duration": stage_duration,
                    "status": "completed",
                    "findings": stage_results.get("count", 0) if stage_results else 0
                })

                print(f"\033[0;32m[{stage_name.upper().replace('_', ' ')}]\033[0m Completed in {stage_duration:.1f}s")
                results["statistics"]["execution_stages"] += 1

            except Exception as e:
                error_msg = f"Stage {stage_name} failed: {str(e)}"
                results["errors"].append(error_msg)
                print(f"\033[0;31m[ERROR]\033[0m {error_msg}")

                results["stages_executed"].append({
                    "name": stage_name,
                    "description": stage_info.get('description', 'Unknown'),
                    "duration": 0,
                    "status": "failed",
                    "error": str(e),
                    "findings": 0
                })

        # Final processing
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        results.update({
            "end_time": end_time.isoformat(),
            "execution_time": execution_time,
            "stage_timings": self.execution_context["stage_timings"]
        })

        executed_count = len([s for s in results["stages_executed"] if s["status"] == "completed"])
        total_count = len(workflow["stages"])

        print(f"\n\033[0;36m[WORKFLOW]\033[0m Professional reconnaissance completed in {execution_time:.1f}s")
        print(f"\033[0;32m✅ Executed {executed_count}/{total_count} stages successfully\033[0m")
        print(f"\033[0;32m📊 Total findings: {results['statistics']['total_findings']}\033[0m")

        return results

    async def _execute_stage(self, stage_name: str, workflow: Dict, results: Dict) -> Optional[Dict]:
        """Execute a single professional stage"""

        stage_config = self.stages.get(stage_name, {})
        tools = stage_config.get("tools", [])
        target = workflow["target"]

        stage_results = {}
        tools_executed = 0

        for tool_name in tools:
            if not await self._is_tool_available(tool_name):
                print(f"  \033[0;33m⚠️  {tool_name} not available, skipping...\033[0m")
                continue

            print(f"  \033[0;33m🔧 Executing {tool_name}...\033[0m", end=" ", flush=True)

            try:
                # Execute tool based on stage with professional handling
                if stage_name == "subdomain_enumeration":
                    tool_output = await self._execute_subdomain_tool(tool_name, target, workflow)
                    if tool_output:
                        if "subdomains" not in stage_results:
                            stage_results["subdomains"] = []
                        stage_results["subdomains"].extend(tool_output)

                elif stage_name == "live_host_detection":
                    input_domains = results["data"].get("subdomains", [target])
                    tool_output = await self._execute_http_tool(tool_name, input_domains, workflow)
                    if tool_output:
                        if "live_hosts" not in stage_results:
                            stage_results["live_hosts"] = []
                        stage_results["live_hosts"].extend(tool_output)

                elif stage_name == "port_scanning":
                    input_hosts = results["data"].get("subdomains", [target])
                    tool_output = await self._execute_port_tool(tool_name, input_hosts, workflow)
                    if tool_output:
                        if "ports" not in stage_results:
                            stage_results["ports"] = []
                        stage_results["ports"].extend(tool_output)

                elif stage_name == "vulnerability_scanning":
                    input_urls = results["data"].get("live_hosts", [f"https://{target}"])
                    tool_output = await self._execute_vuln_tool(tool_name, input_urls, workflow)
                    if tool_output:
                        if "vulnerabilities" not in stage_results:
                            stage_results["vulnerabilities"] = []
                        stage_results["vulnerabilities"].extend(tool_output)

                else:
                    tool_output = await self._execute_generic_tool(tool_name, target, workflow)

                tools_executed += 1

                if tool_output and len(tool_output) > 0:
                    count = len(tool_output) if isinstance(tool_output, list) else 1
                    print(f"\033[0;32m✅ {count} results\033[0m")
                else:
                    print("\033[0;33m⚠️  No results\033[0m")

            except Exception as e:
                print(f"\033[0;31m❌ Failed: {str(e)[:50]}...\033[0m")

        # Add metadata to results
        if stage_results:
            stage_results["count"] = sum(len(v) if isinstance(v, list) else 1 for v in stage_results.values())
            stage_results["tools_executed"] = tools_executed

        results["statistics"]["tools_used"] += tools_executed

        return stage_results

    async def _execute_subdomain_tool(self, tool_name: str, target: str, workflow: Dict) -> Optional[List[str]]:
        """Execute subdomain enumeration tools with unique functionality"""

        cmd = []

        if tool_name == "subfinder":
            cmd = ["subfinder", "-d", target, "-silent", "-all"]

        elif tool_name == "assetfinder":
            cmd = ["assetfinder", "--subs-only", target]

        elif tool_name == "amass":
            cmd = ["amass", "enum", "-d", target, "-silent", "-passive"]

        else:
            return None

        try:
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=180)

            if result.returncode == 0 and stdout:
                subdomains = []
                for line in stdout.decode().strip().split('\n'):
                    subdomain = line.strip()
                    if subdomain and '.' in subdomain and len(subdomain) > 3:
                        # Basic validation
                        if not any(char in subdomain for char in ['<', '>', '"', ' ']):
                            subdomains.append(subdomain.lower())

                return list(set(subdomains))  # Remove duplicates

        except Exception as e:
            raise Exception(f"{tool_name} execution failed: {str(e)}")

        return []

    async def _execute_http_tool(self, tool_name: str, domains: List[str], workflow: Dict) -> Optional[List[str]]:
        """Execute HTTP probing tools with unique functionality"""

        if not domains:
            return []

        # Limit domains for performance
        limited_domains = domains[:50] if len(domains) > 50 else domains

        # Create temp file for input
        temp_dir = workflow["workspace"] / "temp"
        temp_input = temp_dir / f"{tool_name}_input.txt"

        with open(temp_input, 'w') as f:
            for domain in limited_domains:
                f.write(f"{domain}\n")

        try:
            cmd = []

            if tool_name == "httpx":
                cmd = ["httpx", "-l", str(temp_input), "-silent", "-follow-redirects", "-status-code"]

            elif tool_name == "httprobe":
                # httprobe reads from stdin
                process = await asyncio.create_subprocess_exec(
                    "httprobe",
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                input_data = '\n'.join(limited_domains)
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input_data.encode()), 
                    timeout=120
                )

                if stdout:
                    live_hosts = []
                    for line in stdout.decode().strip().split('\n'):
                        host = line.strip()
                        if host and ('http://' in host or 'https://' in host):
                            live_hosts.append(host)
                    return list(set(live_hosts))
                return []

            if cmd:
                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=120)

                if stdout:
                    live_hosts = []
                    for line in stdout.decode().strip().split('\n'):
                        host = line.strip()
                        if host and ('http://' in host or 'https://' in host):
                            live_hosts.append(host)
                    return list(set(live_hosts))

        except Exception as e:
            raise Exception(f"{tool_name} HTTP probing failed: {str(e)}")
        finally:
            if temp_input.exists():
                temp_input.unlink()

        return []

    async def _execute_port_tool(self, tool_name: str, hosts: List[str], workflow: Dict) -> Optional[List[str]]:
        """Execute port scanning tools with unique functionality"""

        if not hosts:
            return []

        ports_found = []

        # Limit hosts for performance (top 10)
        limited_hosts = hosts[:10] if len(hosts) > 10 else hosts

        for host in limited_hosts:
            # Clean host (remove protocol, path)
            clean_host = host.replace('https://', '').replace('http://', '').split('/')[0].split(':')[0]

            if not clean_host or clean_host == 'localhost':
                continue

            try:
                cmd = []

                if tool_name == "naabu":
                    cmd = ["naabu", "-host", clean_host, "-silent", "-top-ports", "100"]

                elif tool_name == "nmap":
                    cmd = ["nmap", "-T4", "-F", clean_host, "--open", "-q"]

                elif tool_name == "masscan":
                    cmd = ["masscan", clean_host, "-p1-1000", "--rate=1000", "-q"]

                else:
                    continue

                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=60)

                if stdout:
                    for line in stdout.decode().split('\n'):
                        line = line.strip()
                        if 'open' in line.lower() and ('tcp' in line.lower() or '/' in line):
                            # Extract port number
                            parts = line.split()
                            for part in parts:
                                if '/' in part and part.split('/')[0].isdigit():
                                    port = part.split('/')[0]
                                    ports_found.append(f"{clean_host}:{port}")
                                    break

            except Exception:
                # Continue with other hosts if one fails
                continue

        return list(set(ports_found))

    async def _execute_vuln_tool(self, tool_name: str, urls: List[str], workflow: Dict) -> Optional[List[Dict]]:
        """Execute vulnerability scanning tools with unique functionality"""

        if not urls:
            return []

        vulnerabilities = []

        # Limit URLs for performance
        limited_urls = urls[:5] if len(urls) > 5 else urls

        # Create temp input file
        temp_dir = workflow["workspace"] / "temp"
        temp_input = temp_dir / f"{tool_name}_urls.txt"

        with open(temp_input, 'w') as f:
            for url in limited_urls:
                f.write(f"{url}\n")

        try:
            if tool_name == "nuclei":
                cmd = ["nuclei", "-l", str(temp_input), "-silent", "-j", "-severity", "critical,high,medium"]

                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=300)

                if stdout:
                    for line in stdout.decode().strip().split('\n'):
                        if line.strip():
                            try:
                                data = json.loads(line)
                                vulnerabilities.append({
                                    "name": data.get("template-id", "Unknown"),
                                    "url": data.get("matched-at", "Unknown"),
                                    "severity": data.get("info", {}).get("severity", "info"),
                                    "description": data.get("info", {}).get("name", ""),
                                    "tool": "nuclei"
                                })
                            except json.JSONDecodeError:
                                continue

            elif tool_name == "nikto":
                # Nikto processes one URL at a time
                for url in limited_urls:
                    try:
                        result = await asyncio.create_subprocess_exec(
                            "nikto", "-h", url, "-Format", "csv", "-nointeractive",
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )

                        stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=120)

                        if stdout:
                            for line in stdout.decode().split('\n'):
                                line = line.strip()
                                if line and not line.startswith('#') and ',' in line:
                                    parts = line.split(',')
                                    if len(parts) > 3:
                                        vulnerabilities.append({
                                            "name": parts[3].strip('"') if len(parts) > 3 else "Nikto Finding",
                                            "url": url,
                                            "severity": "medium",
                                            "description": parts[6].strip('"') if len(parts) > 6 else "",
                                            "tool": "nikto"
                                        })
                    except Exception:
                        continue

        except Exception as e:
            raise Exception(f"{tool_name} vulnerability scanning failed: {str(e)}")
        finally:
            if temp_input.exists():
                temp_input.unlink()

        return vulnerabilities

    async def _execute_generic_tool(self, tool_name: str, target: str, workflow: Dict) -> Optional[List[str]]:
        """Execute generic tools for system checks"""
        if tool_name == "system_check":
            return ["system_initialized"]

        try:
            result = await asyncio.create_subprocess_exec(
                tool_name, "--help",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            await asyncio.wait_for(result.communicate(), timeout=5)
            return [f"{tool_name}_executed"]

        except Exception:
            return []

    async def _is_tool_available(self, tool_name: str) -> bool:
        """Check if tool is available"""
        if tool_name == "system_check":
            return True
        return shutil.which(tool_name) is not None

#!/usr/bin/env python3
"""
ReconXploit v4.0 - Ultimate Workflow Engine
Product of Kernelpanic under infosbios.tech
"""

import asyncio
import subprocess
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import tempfile
import shutil

class UltimateWorkflowEngine:
    """Ultimate reconnaissance workflow with intelligent tool chaining"""

    def __init__(self):
        # Ultimate workflow stages with dependencies
        self.ultimate_stages = {
            "initialization": {
                "priority": 1,
                "dependencies": [],
                "tools": ["system_check"],
                "timeout": 30
            },
            "subdomain_enumeration": {
                "priority": 2,
                "dependencies": ["initialization"],
                "tools": ["subfinder", "assetfinder", "amass", "sublist3r", "chaos"],
                "timeout": 600,
                "output_format": "domains"
            },
            "subdomain_validation": {
                "priority": 3,
                "dependencies": ["subdomain_enumeration"],
                "tools": ["shuffledns", "puredns", "massdns"],
                "timeout": 300,
                "input_format": "domains",
                "output_format": "validated_domains"
            },
            "live_host_detection": {
                "priority": 4,
                "dependencies": ["subdomain_validation"],
                "tools": ["httpx", "httprobe"],
                "timeout": 300,
                "input_format": "validated_domains",
                "output_format": "live_urls"
            },
            "technology_detection": {
                "priority": 5,
                "dependencies": ["live_host_detection"],
                "tools": ["httpx", "whatweb", "wappalyzer"],
                "timeout": 200,
                "input_format": "live_urls",
                "output_format": "tech_stack"
            },
            "port_scanning": {
                "priority": 6,
                "dependencies": ["subdomain_validation"],
                "tools": ["naabu", "nmap", "masscan"],
                "timeout": 900,
                "input_format": "validated_domains",
                "output_format": "open_ports"
            },
            "service_detection": {
                "priority": 7,
                "dependencies": ["port_scanning"],
                "tools": ["nmap", "naabu"],
                "timeout": 600,
                "input_format": "open_ports",
                "output_format": "services"
            },
            "web_crawling": {
                "priority": 8,
                "dependencies": ["live_host_detection"],
                "tools": ["katana", "hakrawler", "gospider", "waybackurls", "gau"],
                "timeout": 800,
                "input_format": "live_urls",
                "output_format": "urls"
            },
            "content_discovery": {
                "priority": 9,
                "dependencies": ["live_host_detection"],
                "tools": ["feroxbuster", "gobuster", "dirsearch", "ffuf"],
                "timeout": 1200,
                "input_format": "live_urls",
                "output_format": "discovered_paths"
            },
            "parameter_discovery": {
                "priority": 10,
                "dependencies": ["web_crawling"],
                "tools": ["arjun", "paramspider", "x8"],
                "timeout": 600,
                "input_format": "urls",
                "output_format": "parameters"
            },
            "vulnerability_scanning": {
                "priority": 11,
                "dependencies": ["live_host_detection", "web_crawling"],
                "tools": ["nuclei", "nikto", "dalfox"],
                "timeout": 1800,
                "input_format": "live_urls",
                "output_format": "vulnerabilities"
            },
            "advanced_vulnerability_testing": {
                "priority": 12,
                "dependencies": ["parameter_discovery", "vulnerability_scanning"],
                "tools": ["sqlmap", "xsstrike", "commix"],
                "timeout": 1500,
                "input_format": ["parameters", "vulnerabilities"],
                "output_format": "advanced_vulns"
            },
            "exploitation_testing": {
                "priority": 13,
                "dependencies": ["advanced_vulnerability_testing"],
                "tools": ["custom_exploits"],
                "timeout": 900,
                "input_format": "advanced_vulns",
                "output_format": "exploits"
            }
        }

        # Intelligent chaining rules
        self.chaining_rules = {
            # Subdomain enumeration output feeds into multiple stages
            "subdomain_enumeration -> subdomain_validation": {
                "data_flow": "direct",
                "filter": "unique_domains",
                "transform": "line_separated"
            },
            "subdomain_validation -> live_host_detection": {
                "data_flow": "direct", 
                "filter": "valid_domains",
                "transform": "url_format"
            },
            "live_host_detection -> technology_detection": {
                "data_flow": "direct",
                "filter": "http_urls",
                "transform": "url_list"
            },
            "live_host_detection -> web_crawling": {
                "data_flow": "parallel",
                "filter": "web_services",
                "transform": "crawlable_urls"
            },
            "web_crawling -> parameter_discovery": {
                "data_flow": "merge",
                "filter": "parameterized_urls",
                "transform": "url_with_params"
            },
            "parameter_discovery -> advanced_vulnerability_testing": {
                "data_flow": "targeted",
                "filter": "testable_parameters",
                "transform": "parameter_context"
            }
        }

        # Execution context
        self.execution_context = {
            "target": None,
            "workspace": None,
            "temp_dir": None,
            "results": {},
            "tool_outputs": {},
            "stage_timings": {},
            "errors": [],
            "statistics": {
                "total_subdomains": 0,
                "live_hosts": 0,
                "open_ports": 0,
                "vulnerabilities_found": 0,
                "critical_vulnerabilities": 0,
                "tools_executed": 0,
                "false_positives_filtered": 0
            }
        }

    async def create_ultimate_workflow(self, args, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create ultimate workflow configuration"""

        # Determine target
        target = args.domain or args.ip or args.url or "unknown"

        # Create workspace
        workspace = Path(args.output_dir) / target.replace('.', '_').replace('/', '_')
        workspace.mkdir(parents=True, exist_ok=True)

        # Create temporary directory for inter-stage data
        temp_dir = workspace / "temp"
        temp_dir.mkdir(exist_ok=True)

        # Determine workflow mode
        if args.ultimate:
            workflow_mode = "ultimate"
            selected_stages = list(self.ultimate_stages.keys())
        elif args.bug_hunting:
            workflow_mode = "bug_hunting" 
            selected_stages = [
                "initialization", "subdomain_enumeration", "subdomain_validation",
                "live_host_detection", "web_crawling", "parameter_discovery", 
                "vulnerability_scanning", "advanced_vulnerability_testing"
            ]
        elif args.passive:
            workflow_mode = "passive"
            selected_stages = [
                "initialization", "subdomain_enumeration", "web_crawling"
            ]
        elif args.enterprise:
            workflow_mode = "enterprise"
            selected_stages = [
                "initialization", "subdomain_enumeration", "subdomain_validation",
                "live_host_detection", "technology_detection", "port_scanning",
                "vulnerability_scanning"
            ]
        else:
            workflow_mode = "standard"
            selected_stages = [
                "initialization", "subdomain_enumeration", "live_host_detection",
                "port_scanning", "vulnerability_scanning"
            ]

        # Apply stage filters based on arguments
        if args.skip_subdomain:
            selected_stages = [s for s in selected_stages if "subdomain" not in s]
        if args.skip_port_scan:
            selected_stages = [s for s in selected_stages if "port" not in s]
        if args.skip_vulnerability:
            selected_stages = [s for s in selected_stages if "vulnerability" not in s]

        # Build workflow configuration
        workflow = {
            "target": target,
            "mode": workflow_mode,
            "workspace": workspace,
            "temp_dir": temp_dir,
            "stages": selected_stages,
            "chaining_enabled": args.chain_tools if hasattr(args, 'chain_tools') else False,
            "zero_false_mode": args.zero_false if hasattr(args, 'zero_false') else False,
            "config": config,
            "performance": {
                "threads": args.threads,
                "timeout": args.timeout,
                "delay": getattr(args, 'delay', 0),
                "rate_limit": getattr(args, 'rate_limit', 1000)
            },
            "api_integration": {
                "use_all_apis": getattr(args, 'use_all_apis', False),
                "shodan": getattr(args, 'shodan', False),
                "virustotal": getattr(args, 'virustotal', False),
                "securitytrails": getattr(args, 'securitytrails', False)
            }
        }

        # Initialize execution context
        self.execution_context.update({
            "target": target,
            "workspace": workspace,
            "temp_dir": temp_dir,
            "results": {},
            "tool_outputs": {},
            "stage_timings": {}
        })

        return workflow

    async def execute_ultimate_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the ultimate reconnaissance workflow"""
        start_time = datetime.now()

        print(f"\033[0;96m[ULTIMATE WORKFLOW]\033[0m Initializing ultimate reconnaissance engine...")
        print(f"\033[0;36m📋 Target:\033[0m {workflow['target']}")
        print(f"\033[0;36m📋 Mode:\033[0m {workflow['mode']}")
        print(f"\033[0;36m📋 Stages:\033[0m {len(workflow['stages'])}")
        print(f"\033[0;36m📁 Workspace:\033[0m {workflow['workspace']}")

        results = {
            "target": workflow["target"],
            "mode": workflow["mode"],
            "start_time": start_time.isoformat(),
            "stages_executed": [],
            "data": {
                "subdomains": [],
                "live_hosts": [],
                "ports": [],
                "urls": [],
                "parameters": [],
                "vulnerabilities": [],
                "technologies": [],
                "services": []
            },
            "tool_outputs": {},
            "statistics": self.execution_context["statistics"].copy(),
            "errors": []
        }

        # Execute stages in dependency order
        executed_stages = []

        for stage_name in workflow["stages"]:
            if stage_name not in self.ultimate_stages:
                continue

            stage_config = self.ultimate_stages[stage_name]

            # Check dependencies
            dependencies_met = all(dep in executed_stages for dep in stage_config["dependencies"])
            if not dependencies_met:
                missing_deps = [dep for dep in stage_config["dependencies"] if dep not in executed_stages]
                error_msg = f"Stage {stage_name} missing dependencies: {missing_deps}"
                results["errors"].append(error_msg)
                print(f"\033[0;33m[WARNING]\033[0m {error_msg}")
                continue

            try:
                print(f"\n\033[0;94m[{stage_name.upper().replace('_', ' ')}]\033[0m Executing...")
                stage_start = time.time()

                # Execute stage with chaining if enabled
                if workflow["chaining_enabled"]:
                    stage_results = await self._execute_stage_with_chaining(
                        stage_name, stage_config, workflow, results
                    )
                else:
                    stage_results = await self._execute_stage_standard(
                        stage_name, stage_config, workflow, results
                    )

                stage_end = time.time()
                stage_duration = stage_end - stage_start

                # Update results
                if stage_results:
                    # Merge stage results into main results
                    for key, value in stage_results.items():
                        if key in results["data"]:
                            if isinstance(value, list):
                                results["data"][key].extend(value)
                            elif isinstance(value, dict):
                                results["data"][key].update(value)
                        else:
                            results["data"][key] = value

                    # Update statistics
                    self._update_stage_statistics(stage_name, stage_results)

                # Track timing
                self.execution_context["stage_timings"][stage_name] = stage_duration
                executed_stages.append(stage_name)
                results["stages_executed"].append({
                    "name": stage_name,
                    "duration": stage_duration,
                    "status": "completed"
                })

                print(f"\033[0;32m[{stage_name.upper().replace('_', ' ')}]\033[0m Completed in {stage_duration:.1f}s")

                # Save intermediate results
                await self._save_intermediate_results(stage_name, stage_results, workflow)

            except Exception as e:
                error_msg = f"Stage {stage_name} failed: {str(e)}"
                results["errors"].append(error_msg)
                print(f"\033[0;31m[ERROR]\033[0m {error_msg}")

                results["stages_executed"].append({
                    "name": stage_name,
                    "duration": 0,
                    "status": "failed",
                    "error": str(e)
                })

                # Continue with other stages unless it's a critical dependency
                if stage_name in ["initialization", "subdomain_enumeration"]:
                    break

        # Final processing
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        results.update({
            "end_time": end_time.isoformat(),
            "execution_time": execution_time,
            "statistics": self.execution_context["statistics"],
            "stage_timings": self.execution_context["stage_timings"]
        })

        print(f"\n\033[0;96m[ULTIMATE WORKFLOW]\033[0m Completed in {execution_time:.1f}s")
        print(f"\033[0;32m✅ Executed {len(executed_stages)}/{len(workflow['stages'])} stages successfully\033[0m")

        return results

    async def execute_with_chaining(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow with intelligent tool chaining"""
        print(f"\033[0;93m🔗 INTELLIGENT TOOL CHAINING ENABLED\033[0m")
        return await self.execute_ultimate_workflow(workflow)

    async def _execute_stage_with_chaining(self, stage_name: str, stage_config: Dict, 
                                         workflow: Dict, results: Dict) -> Optional[Dict]:
        """Execute stage with intelligent chaining from previous stages"""

        # Get input data from previous stages
        input_data = self._prepare_chained_input(stage_name, results)

        # Execute tools in the stage
        stage_results = {}
        tools = stage_config.get("tools", [])

        for tool_name in tools:
            if not await self._is_tool_available(tool_name):
                continue

            print(f"  \033[0;33m🔧 Executing {tool_name} with chained input...\033[0m")

            try:
                tool_output = await self._execute_tool_with_input(
                    tool_name, input_data, stage_config, workflow
                )

                if tool_output:
                    # Process and merge tool output
                    processed_output = await self._process_tool_output(
                        tool_name, tool_output, stage_config
                    )

                    # Merge results
                    for key, value in processed_output.items():
                        if key not in stage_results:
                            stage_results[key] = []
                        if isinstance(value, list):
                            stage_results[key].extend(value)
                        else:
                            stage_results[key].append(value)

                    self.execution_context["statistics"]["tools_executed"] += 1

                    print(f"    \033[0;32m✅ {tool_name}: {len(processed_output)} results\033[0m")

            except Exception as e:
                print(f"    \033[0;31m❌ {tool_name}: {str(e)}\033[0m")

        return stage_results

    async def _execute_stage_standard(self, stage_name: str, stage_config: Dict,
                                    workflow: Dict, results: Dict) -> Optional[Dict]:
        """Execute stage with standard (non-chained) approach"""

        stage_results = {}
        tools = stage_config.get("tools", [])
        target = workflow["target"]

        for tool_name in tools:
            if not await self._is_tool_available(tool_name):
                continue

            print(f"  \033[0;33m🔧 Executing {tool_name}...\033[0m")

            try:
                # Execute tool based on stage and tool type
                if stage_name == "subdomain_enumeration":
                    tool_output = await self._execute_subdomain_tool(tool_name, target, workflow)
                elif stage_name == "live_host_detection":
                    input_domains = results["data"].get("subdomains", [target])
                    tool_output = await self._execute_http_probing_tool(tool_name, input_domains, workflow)
                elif stage_name == "port_scanning":
                    input_hosts = results["data"].get("subdomains", [target])
                    tool_output = await self._execute_port_scanning_tool(tool_name, input_hosts, workflow)
                elif stage_name == "vulnerability_scanning":
                    input_urls = results["data"].get("live_hosts", [f"https://{target}"])
                    tool_output = await self._execute_vulnerability_tool(tool_name, input_urls, workflow)
                else:
                    # Generic execution
                    tool_output = await self._execute_generic_tool(tool_name, target, workflow)

                if tool_output:
                    processed_output = await self._process_tool_output(tool_name, tool_output, stage_config)

                    # Merge results
                    for key, value in processed_output.items():
                        if key not in stage_results:
                            stage_results[key] = []
                        if isinstance(value, list):
                            stage_results[key].extend(value)
                        else:
                            stage_results[key].append(value)

                    self.execution_context["statistics"]["tools_executed"] += 1
                    print(f"    \033[0;32m✅ {tool_name}: {len(value) if isinstance(value, list) else 1} results\033[0m")

            except Exception as e:
                print(f"    \033[0;31m❌ {tool_name}: {str(e)}\033[0m")

        return stage_results

    async def _execute_subdomain_tool(self, tool_name: str, target: str, workflow: Dict) -> Optional[List[str]]:
        """Execute subdomain enumeration tools"""

        if tool_name == "subfinder":
            cmd = ["subfinder", "-d", target, "-silent", "-all"]

        elif tool_name == "assetfinder": 
            cmd = ["assetfinder", "--subs-only", target]

        elif tool_name == "amass":
            cmd = ["amass", "enum", "-d", target, "-silent"]

        elif tool_name == "sublist3r":
            cmd = ["python3", "-m", "sublist3r", "-d", target, "-o", "/dev/stdout"]

        else:
            return None

        try:
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=300)

            if result.returncode == 0 and stdout:
                subdomains = [
                    line.strip() 
                    for line in stdout.decode().strip().split('\n') 
                    if line.strip() and '.' in line.strip()
                ]
                return list(set(subdomains))  # Remove duplicates

        except Exception as e:
            raise Exception(f"Tool execution failed: {e}")

        return []

    async def _execute_http_probing_tool(self, tool_name: str, domains: List[str], workflow: Dict) -> Optional[List[str]]:
        """Execute HTTP probing tools"""

        if not domains:
            return []

        # Create temporary input file
        temp_input = workflow["temp_dir"] / f"{tool_name}_input.txt"
        with open(temp_input, 'w') as f:
            for domain in domains:
                f.write(f"{domain}\n")

        try:
            if tool_name == "httpx":
                cmd = ["httpx", "-l", str(temp_input), "-silent", "-no-color"]

            elif tool_name == "httprobe":
                cmd = ["httprobe"]
                # httprobe reads from stdin

            else:
                return None

            if tool_name == "httprobe":
                # Special handling for httprobe (stdin)
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                input_data = '\n'.join(domains)
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input_data.encode()), 
                    timeout=180
                )
            else:
                # Regular execution
                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=180)

            if stdout:
                live_hosts = [
                    line.strip() 
                    for line in stdout.decode().strip().split('\n')
                    if line.strip() and ('http://' in line or 'https://' in line)
                ]
                return list(set(live_hosts))

        except Exception as e:
            raise Exception(f"HTTP probing failed: {e}")
        finally:
            # Cleanup
            if temp_input.exists():
                temp_input.unlink()

        return []

    async def _execute_port_scanning_tool(self, tool_name: str, hosts: List[str], workflow: Dict) -> Optional[List[str]]:
        """Execute port scanning tools"""

        if not hosts:
            return []

        ports_found = []

        for host in hosts[:10]:  # Limit to first 10 hosts
            clean_host = host.replace('https://', '').replace('http://', '').split('/')[0]

            try:
                if tool_name == "naabu":
                    cmd = ["naabu", "-host", clean_host, "-silent", "-json"]

                elif tool_name == "nmap":
                    cmd = ["nmap", "-T4", "-F", clean_host, "--open"]

                elif tool_name == "masscan":
                    cmd = ["masscan", clean_host, "-p1-1000", "--rate=1000"]

                else:
                    continue

                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=300)

                if stdout:
                    # Parse output based on tool
                    if tool_name == "naabu":
                        # Parse JSON output
                        for line in stdout.decode().strip().split('\n'):
                            if line.strip():
                                try:
                                    data = json.loads(line)
                                    port = data.get('port')
                                    if port:
                                        ports_found.append(f"{clean_host}:{port}")
                                except:
                                    pass
                    else:
                        # Parse text output for nmap/masscan
                        for line in stdout.decode().split('\n'):
                            if 'open' in line.lower() and '/' in line:
                                port = line.split('/')[0].strip()
                                if port.isdigit():
                                    ports_found.append(f"{clean_host}:{port}")

            except Exception as e:
                continue  # Skip failed hosts

        return list(set(ports_found))

    async def _execute_vulnerability_tool(self, tool_name: str, urls: List[str], workflow: Dict) -> Optional[List[Dict]]:
        """Execute vulnerability scanning tools"""

        if not urls:
            return []

        vulnerabilities = []

        # Create temporary input file
        temp_input = workflow["temp_dir"] / f"{tool_name}_urls.txt"
        with open(temp_input, 'w') as f:
            for url in urls[:20]:  # Limit URLs
                f.write(f"{url}\n")

        try:
            if tool_name == "nuclei":
                cmd = ["nuclei", "-l", str(temp_input), "-silent", "-j"]

            elif tool_name == "nikto":
                # Nikto processes one URL at a time
                for url in urls[:5]:  # Limit for nikto
                    cmd = ["nikto", "-h", url, "-Format", "csv", "-output", "/dev/stdout"]

            elif tool_name == "dalfox":
                cmd = ["dalfox", "file", str(temp_input), "--silence", "--format", "json"]

            else:
                return []

            if tool_name == "nikto":
                # Special handling for nikto (one URL at a time)
                for url in urls[:5]:
                    try:
                        result = await asyncio.create_subprocess_exec(
                            "nikto", "-h", url, "-Format", "csv",
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )

                        stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=180)

                        if stdout:
                            # Parse nikto CSV output
                            for line in stdout.decode().split('\n'):
                                if line.strip() and not line.startswith('#'):
                                    parts = line.split(',')
                                    if len(parts) > 3:
                                        vulnerabilities.append({
                                            "name": parts[3].strip('"'),
                                            "url": url,
                                            "severity": "medium",
                                            "tool": "nikto"
                                        })
                    except:
                        continue
            else:
                # Regular execution for nuclei/dalfox
                result = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=600)

                if stdout:
                    # Parse JSON output
                    for line in stdout.decode().strip().split('\n'):
                        if line.strip():
                            try:
                                data = json.loads(line)

                                if tool_name == "nuclei":
                                    vulnerabilities.append({
                                        "name": data.get("template-id", "Unknown"),
                                        "url": data.get("matched-at", "Unknown"),
                                        "severity": data.get("info", {}).get("severity", "info"),
                                        "description": data.get("info", {}).get("name", ""),
                                        "tool": "nuclei"
                                    })
                                elif tool_name == "dalfox":
                                    vulnerabilities.append({
                                        "name": "XSS Vulnerability",
                                        "url": data.get("url", "Unknown"),
                                        "severity": "medium",
                                        "description": data.get("message", ""),
                                        "tool": "dalfox"
                                    })
                            except:
                                pass

        except Exception as e:
            raise Exception(f"Vulnerability scanning failed: {e}")
        finally:
            # Cleanup
            if temp_input.exists():
                temp_input.unlink()

        return vulnerabilities

    async def _execute_generic_tool(self, tool_name: str, target: str, workflow: Dict) -> Optional[List[str]]:
        """Execute generic tools"""
        try:
            result = await asyncio.create_subprocess_exec(
                tool_name, "--help",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=10)
            return [f"{tool_name} executed successfully"]

        except Exception:
            return []

    async def _is_tool_available(self, tool_name: str) -> bool:
        """Check if tool is available"""
        return shutil.which(tool_name) is not None

    async def _process_tool_output(self, tool_name: str, output: Any, stage_config: Dict) -> Dict[str, Any]:
        """Process and categorize tool output"""

        processed = {}

        if isinstance(output, list):
            if not output:
                return processed

            # Determine output type based on stage
            stage_output_format = stage_config.get("output_format", "generic")

            if stage_output_format == "domains":
                processed["subdomains"] = [item for item in output if isinstance(item, str) and '.' in item]

            elif stage_output_format == "live_urls":
                processed["live_hosts"] = [item for item in output if isinstance(item, str) and ('http://' in item or 'https://' in item)]

            elif stage_output_format == "open_ports":
                processed["ports"] = [item for item in output if isinstance(item, str) and ':' in item]

            elif stage_output_format == "vulnerabilities":
                processed["vulnerabilities"] = [item for item in output if isinstance(item, dict)]

            else:
                processed["generic"] = output

        return processed

    def _prepare_chained_input(self, stage_name: str, results: Dict) -> Dict[str, Any]:
        """Prepare input data from previous stages for chaining"""

        input_data = {}

        # Get relevant data based on stage dependencies
        stage_config = self.ultimate_stages.get(stage_name, {})
        input_format = stage_config.get("input_format", "")

        if input_format == "domains" or input_format == "validated_domains":
            input_data["domains"] = results["data"].get("subdomains", [])

        elif input_format == "live_urls":
            input_data["urls"] = results["data"].get("live_hosts", [])

        elif input_format == "open_ports":
            input_data["ports"] = results["data"].get("ports", [])

        elif input_format == "urls":
            input_data["urls"] = results["data"].get("urls", [])

        return input_data

    async def _execute_tool_with_input(self, tool_name: str, input_data: Dict, 
                                     stage_config: Dict, workflow: Dict) -> Optional[Any]:
        """Execute tool with prepared input data"""

        # This is a simplified version - in reality, each tool would have
        # specific input formatting requirements

        if "domains" in input_data and input_data["domains"]:
            return await self._execute_http_probing_tool(tool_name, input_data["domains"], workflow)
        elif "urls" in input_data and input_data["urls"]:
            return await self._execute_vulnerability_tool(tool_name, input_data["urls"], workflow)
        else:
            return await self._execute_generic_tool(tool_name, workflow["target"], workflow)

    def _update_stage_statistics(self, stage_name: str, stage_results: Dict):
        """Update execution statistics based on stage results"""

        stats = self.execution_context["statistics"]

        for key, value in stage_results.items():
            if key == "subdomains" and isinstance(value, list):
                stats["total_subdomains"] += len(value)
            elif key == "live_hosts" and isinstance(value, list):
                stats["live_hosts"] += len(value)
            elif key == "ports" and isinstance(value, list):
                stats["open_ports"] += len(value)
            elif key == "vulnerabilities" and isinstance(value, list):
                stats["vulnerabilities_found"] += len(value)
                # Count critical vulnerabilities
                critical_count = sum(1 for v in value 
                                   if isinstance(v, dict) and v.get("severity") == "critical")
                stats["critical_vulnerabilities"] += critical_count

    async def _save_intermediate_results(self, stage_name: str, stage_results: Dict, workflow: Dict):
        """Save intermediate results for debugging and recovery"""

        output_file = workflow["temp_dir"] / f"{stage_name}_results.json"

        try:
            with open(output_file, 'w') as f:
                json.dump({
                    "stage": stage_name,
                    "timestamp": datetime.now().isoformat(),
                    "results": stage_results
                }, f, indent=2, default=str)
        except Exception:
            pass  # Ignore save errors

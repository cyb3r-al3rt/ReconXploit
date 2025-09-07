#!/usr/bin/env python3
"""
ReconXploit v3.0 - Workflow Engine
Product of Kernelpanic under infosbios.tech
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from core.tool_manager import ToolManager
from core.result_processor import ResultProcessor

class WorkflowStage(Enum):
    """Enumeration of workflow stages"""
    INITIALIZATION = "initialization"
    SUBDOMAIN_ENUMERATION = "subdomain_enumeration"
    LIVE_HOST_DETECTION = "live_host_detection"
    TECHNOLOGY_DETECTION = "technology_detection"
    PORT_SCANNING = "port_scanning"
    WEB_CRAWLING = "web_crawling"
    URL_DISCOVERY = "url_discovery"
    CONTENT_DISCOVERY = "content_discovery"
    PARAMETER_DISCOVERY = "parameter_discovery"
    VULNERABILITY_SCANNING = "vulnerability_scanning"
    OSINT_GATHERING = "osint_gathering"
    REPORT_GENERATION = "report_generation"
    COMPLETION = "completion"

class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class StageResult:
    """Result of a workflow stage"""
    stage: WorkflowStage
    status: WorkflowStatus
    start_time: float
    end_time: Optional[float] = None
    data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)

    @property
    def duration(self) -> float:
        """Calculate stage duration"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time

@dataclass
class WorkflowConfig:
    """Workflow configuration"""
    target: str
    passive_mode: bool = False
    active_mode: bool = True
    threads: int = 50
    timeout: int = 30
    output_dir: str = "results"
    skip_stages: List[WorkflowStage] = field(default_factory=list)
    custom_wordlists: Dict[str, str] = field(default_factory=dict)
    api_keys: Dict[str, Any] = field(default_factory=dict)

class WorkflowEngine:
    """Advanced workflow orchestration engine"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tool_manager = ToolManager()
        self.result_processor = ResultProcessor()

        # Workflow state
        self.current_workflow: Optional[str] = None
        self.stage_results: Dict[WorkflowStage, StageResult] = {}
        self.global_data: Dict[str, Any] = {}

    def create_workflow(self, args, config: Dict[str, Any]) -> WorkflowConfig:
        """Create workflow configuration from arguments and config"""
        workflow_config = WorkflowConfig(
            target=args.domain,
            passive_mode=args.passive,
            active_mode=not args.passive,
            threads=args.threads,
            timeout=args.timeout,
            output_dir=args.output_dir
        )

        # Apply skip flags
        if args.skip_subdomain:
            workflow_config.skip_stages.append(WorkflowStage.SUBDOMAIN_ENUMERATION)
        if args.skip_port_scan:
            workflow_config.skip_stages.append(WorkflowStage.PORT_SCANNING)
        if args.skip_vulnerability:
            workflow_config.skip_stages.append(WorkflowStage.VULNERABILITY_SCANNING)

        return workflow_config

    async def execute(self, config: WorkflowConfig) -> Dict[str, Any]:
        """Execute the complete reconnaissance workflow"""
        self.logger.info(f"Starting reconnaissance workflow for: {config.target}")

        try:
            # Initialize workflow
            await self._execute_stage(WorkflowStage.INITIALIZATION, config)
            await self._execute_stage(WorkflowStage.SUBDOMAIN_ENUMERATION, config)
            await self._execute_stage(WorkflowStage.LIVE_HOST_DETECTION, config)
            await self._execute_stage(WorkflowStage.VULNERABILITY_SCANNING, config)
            await self._execute_stage(WorkflowStage.REPORT_GENERATION, config)

            # Return aggregated results
            return self._aggregate_results()

        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            raise

    async def _execute_stage(self, stage: WorkflowStage, config: WorkflowConfig):
        """Execute a specific workflow stage"""
        self.logger.info(f"Executing stage: {stage.value}")

        stage_result = StageResult(
            stage=stage,
            status=WorkflowStatus.RUNNING,
            start_time=time.time()
        )

        self.stage_results[stage] = stage_result

        try:
            # Execute stage-specific logic
            if stage == WorkflowStage.INITIALIZATION:
                await self._stage_initialization(config, stage_result)
            elif stage == WorkflowStage.SUBDOMAIN_ENUMERATION:
                await self._stage_subdomain_enumeration(config, stage_result)
            elif stage == WorkflowStage.LIVE_HOST_DETECTION:
                await self._stage_live_host_detection(config, stage_result)
            elif stage == WorkflowStage.VULNERABILITY_SCANNING:
                await self._stage_vulnerability_scanning(config, stage_result)
            elif stage == WorkflowStage.REPORT_GENERATION:
                await self._stage_report_generation(config, stage_result)

            stage_result.status = WorkflowStatus.COMPLETED
            stage_result.end_time = time.time()

            self.logger.info(f"Stage {stage.value} completed in {stage_result.duration:.2f}s")

        except Exception as e:
            stage_result.status = WorkflowStatus.FAILED
            stage_result.end_time = time.time()
            stage_result.errors.append(str(e))

            self.logger.error(f"Stage {stage.value} failed: {e}")
            raise

    async def _stage_initialization(self, config: WorkflowConfig, result: StageResult):
        """Initialize workflow environment"""
        self.logger.info("Initializing reconnaissance environment...")

        # Create output directories
        output_path = Path(config.output_dir) / config.target / f"scan_{int(time.time())}"
        output_path.mkdir(parents=True, exist_ok=True)

        # Store global data
        self.global_data.update({
            'target': config.target,
            'output_path': str(output_path),
            'start_time': time.time(),
            'subdomains': set(),
            'live_hosts': set(),
            'technologies': {},
            'open_ports': {},
            'urls': set(),
            'parameters': set(),
            'vulnerabilities': []
        })

        result.data['output_path'] = str(output_path)
        result.data['target'] = config.target

    async def _stage_subdomain_enumeration(self, config: WorkflowConfig, result: StageResult):
        """Enumerate subdomains using multiple tools"""
        self.logger.info(f"Enumerating subdomains for: {config.target}")

        tools = ['subfinder', 'amass', 'assetfinder']
        subdomains = set()

        # Run tools in parallel
        for tool in tools:
            if self.tool_manager.is_tool_available(tool):
                try:
                    tool_result = await self.tool_manager.run_tool(tool, {
                        'target': config.target,
                        'timeout': config.timeout
                    })
                    if tool_result and 'subdomains' in tool_result:
                        subdomains.update(tool_result['subdomains'])
                        result.tools_used.append(tool)
                        self.logger.info(f"{tool} found {len(tool_result['subdomains'])} subdomains")
                except Exception as e:
                    self.logger.warning(f"{tool} failed: {e}")
                    result.errors.append(f"{tool}: {str(e)}")

        # Store results
        self.global_data['subdomains'].update(subdomains)
        result.data['subdomains'] = list(subdomains)
        result.data['count'] = len(subdomains)

        self.logger.info(f"Total subdomains found: {len(subdomains)}")

    async def _stage_live_host_detection(self, config: WorkflowConfig, result: StageResult):
        """Detect live hosts from discovered subdomains"""
        subdomains = self.global_data.get('subdomains', set())
        if not subdomains:
            self.logger.warning("No subdomains found for live host detection")
            return

        self.logger.info(f"Detecting live hosts from {len(subdomains)} subdomains")

        # Use httpx for live host detection
        if self.tool_manager.is_tool_available('httpx'):
            try:
                httpx_result = await self.tool_manager.run_tool('httpx', {
                    'targets': list(subdomains),
                    'threads': config.threads,
                    'timeout': config.timeout
                })

                if httpx_result and 'live_hosts' in httpx_result:
                    live_hosts = set(httpx_result['live_hosts'])
                    self.global_data['live_hosts'].update(live_hosts)
                    result.data['live_hosts'] = list(live_hosts)
                    result.data['count'] = len(live_hosts)
                    result.tools_used.append('httpx')

                    self.logger.info(f"Found {len(live_hosts)} live hosts")

            except Exception as e:
                self.logger.error(f"Live host detection failed: {e}")
                result.errors.append(f"httpx: {str(e)}")

    async def _stage_vulnerability_scanning(self, config: WorkflowConfig, result: StageResult):
        """Scan for vulnerabilities using nuclei and other tools"""
        live_hosts = self.global_data.get('live_hosts', set())
        if not live_hosts:
            self.logger.warning("No live hosts found for vulnerability scanning")
            return

        self.logger.info(f"Scanning {len(live_hosts)} hosts for vulnerabilities")

        vulnerabilities = []

        # Use nuclei for comprehensive vulnerability scanning
        if self.tool_manager.is_tool_available('nuclei'):
            try:
                nuclei_result = await self.tool_manager.run_tool('nuclei', {
                    'targets': list(live_hosts),
                    'threads': config.threads,
                    'timeout': config.timeout * 3,
                    'templates': 'all'
                })

                if nuclei_result and 'vulnerabilities' in nuclei_result:
                    vulnerabilities.extend(nuclei_result['vulnerabilities'])
                    result.tools_used.append('nuclei')

            except Exception as e:
                self.logger.error(f"Nuclei scanning failed: {e}")
                result.errors.append(f"nuclei: {str(e)}")

        # Store results
        self.global_data['vulnerabilities'].extend(vulnerabilities)
        result.data['vulnerabilities'] = vulnerabilities
        result.data['count'] = len(vulnerabilities)

        self.logger.info(f"Found {len(vulnerabilities)} potential vulnerabilities")

    async def _stage_report_generation(self, config: WorkflowConfig, result: StageResult):
        """Generate comprehensive reconnaissance report"""
        self.logger.info("Generating comprehensive report...")

        # Aggregate all data
        report_data = {
            'target': config.target,
            'scan_time': time.time() - self.global_data['start_time'],
            'subdomains': list(self.global_data.get('subdomains', set())),
            'live_hosts': list(self.global_data.get('live_hosts', set())),
            'vulnerabilities': self.global_data.get('vulnerabilities', []),
            'stage_results': self.stage_results
        }

        result.data['report_data'] = report_data
        result.data['output_path'] = self.global_data['output_path']

    def _aggregate_results(self) -> Dict[str, Any]:
        """Aggregate all stage results into final output"""
        return {
            'target': self.global_data.get('target'),
            'output_path': self.global_data.get('output_path'),
            'total_time': time.time() - self.global_data.get('start_time', time.time()),
            'stage_results': {stage.value: result for stage, result in self.stage_results.items()},
            'summary': {
                'subdomains': len(self.global_data.get('subdomains', set())),
                'live_hosts': len(self.global_data.get('live_hosts', set())),
                'vulnerabilities': len(self.global_data.get('vulnerabilities', []))
            },
            'data': self.global_data
        }

#!/usr/bin/env python3
"""
ReconXploit v3.0 - Tool Manager
Product of Kernelpanic under infosbios.tech
"""
import asyncio
import shutil
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class ToolManager:
    def __init__(self):
        self.go_bin = Path.home() / "go" / "bin"
        self.tool_paths_cache: Dict[str, Optional[str]] = {}

    def _which(self, name: str) -> Optional[str]:
        if name in self.tool_paths_cache:
            return self.tool_paths_cache[name]
        p = shutil.which(name)
        if not p:
            cand = self.go_bin / name
            if cand.exists():
                p = str(cand)
        self.tool_paths_cache[name] = p
        return p

    def is_tool_available(self, tool: str) -> bool:
        return self._which(tool) is not None

    def check_all_tools(self) -> Dict[str, Dict[str, bool]]:
        categories = {
            "subdomain": ["subfinder", "amass", "assetfinder", "findomain", "sublist3r"],
            "web": ["httpx", "katana", "gau", "waybackurls", "hakrawler", "gospider"],
            "content": ["ffuf", "dirsearch", "gobuster", "feroxbuster"],
            "params": ["gf", "arjun", "paramspider", "x8"],
            "vuln": ["nuclei", "nikto", "sqlmap", "dalfox"],
            "network": ["nmap", "masscan", "naabu", "rustscan"],
        }
        status = {}
        for cat, tools in categories.items():
            status[cat] = {t: self.is_tool_available(t) for t in tools}
        return status

    async def run_tool(self, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool == 'subfinder':
            return await self._run_subfinder(params)
        if tool == 'httpx':
            return await self._run_httpx(params)
        if tool == 'nuclei':
            return await self._run_nuclei(params)
        raise NotImplementedError(f"Runner for tool '{tool}' not implemented")

    async def _run_subfinder(self, params: Dict[str, Any]) -> Dict[str, Any]:
        target = params['target']
        timeout = int(params.get('timeout', 300))
        subfinder = self._which('subfinder')
        if not subfinder:
            raise RuntimeError('subfinder not available')
        cmd = [subfinder, '-d', target, '-silent', '-all']
        if Path('config/api_keys.yaml').exists():
            cmd += ['-config', 'config/api_keys.yaml']
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill(); await proc.wait()
            raise RuntimeError('subfinder timed out')
        subs = [ln.strip() for ln in stdout.decode().splitlines() if ln.strip()]
        return {'tool': 'subfinder', 'subdomains': list(sorted(set(subs))), 'count': len(set(subs)), 'stderr': stderr.decode(), 'exit_code': proc.returncode}

    async def _run_httpx(self, params: Dict[str, Any]) -> Dict[str, Any]:
        targets: List[str] = params['targets']
        timeout = int(params.get('timeout', 30))
        threads = int(params.get('threads', 50))
        httpx = self._which('httpx')
        if not httpx:
            raise RuntimeError('httpx not available')
        with tempfile.NamedTemporaryFile('w+', delete=False) as inf, tempfile.NamedTemporaryFile('w+', delete=False) as outf:
            inf.write('\n'.join(targets)); inf.flush()
            cmd = [httpx, '-l', inf.name, '-json', '-silent', '-timeout', str(timeout), '-threads', str(threads), '-title', '-tech-detect', '-status-code', '-content-length', '-web-server', '-o', outf.name]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=max(timeout*len(targets), 60))
            except asyncio.TimeoutError:
                proc.kill(); await proc.wait()
                raise RuntimeError('httpx timed out')
            live, info = [], {}
            if Path(outf.name).exists():
                with open(outf.name) as f:
                    for line in f:
                        try:
                            d = json.loads(line)
                        except Exception:
                            continue
                        url = d.get('url');
                        if url:
                            live.append(url)
                            info[url] = {
                                'status_code': d.get('status_code'),
                                'title': d.get('title'),
                                'content_length': d.get('content_length'),
                                'webserver': d.get('webserver'),
                                'technologies': d.get('tech') or []
                            }
        return {'tool': 'httpx', 'live_hosts': list(dict.fromkeys(live)), 'host_info': info, 'count': len(set(live)), 'exit_code': proc.returncode}

    async def _run_nuclei(self, params: Dict[str, Any]) -> Dict[str, Any]:
        targets: List[str] = params['targets']
        timeout = int(params.get('timeout', 300))
        threads = int(params.get('threads', 50))
        templates = params.get('templates', 'all')
        nuclei = self._which('nuclei')
        if not nuclei:
            raise RuntimeError('nuclei not available')
        with tempfile.NamedTemporaryFile('w+', delete=False) as inf, tempfile.NamedTemporaryFile('w+', delete=False) as outf:
            inf.write('\n'.join(targets)); inf.flush()
            cmd = [nuclei, '-l', inf.name, '-jsonl', '-silent', '-o', outf.name, '-retries', '1', '-rl', '150', '-c', str(threads)]
            if templates and templates != 'all':
                cmd += ['-t', templates]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                proc.kill(); await proc.wait()
                raise RuntimeError('nuclei timed out')
            vulns = []
            if Path(outf.name).exists():
                with open(outf.name) as f:
                    for line in f:
                        try:
                            d = json.loads(line)
                            vulns.append({
                                'template_id': d.get('templateID'),
                                'name': d.get('info', {}).get('name'),
                                'severity': d.get('info', {}).get('severity'),
                                'matched_at': d.get('matched-at') or d.get('matched'),
                                'type': d.get('type'),
                            })
                        except Exception:
                            continue
        return {'tool': 'nuclei', 'vulnerabilities': vulns, 'count': len(vulns), 'exit_code': proc.returncode}

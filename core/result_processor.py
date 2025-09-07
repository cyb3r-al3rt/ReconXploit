#!/usr/bin/env python3
"""
ReconXploit v3.0 - Result Processor
Product of Kernelpanic under infosbios.tech
"""
from typing import Dict, Any
from collections import Counter

class ResultProcessor:
    def __init__(self):
        pass

    def process(self, results: Dict[str, Any]) -> Dict[str, Any]:
        data = results.get('data', {})
        subs = sorted(set(data.get('subdomains', []))) if isinstance(data.get('subdomains'), list) else list(data.get('subdomains', set()))
        live = sorted(set(data.get('live_hosts', []))) if isinstance(data.get('live_hosts'), list) else list(data.get('live_hosts', set()))
        urls = sorted(set(data.get('urls', []))) if isinstance(data.get('urls'), list) else list(data.get('urls', set()))
        params = sorted(set(data.get('parameters', []))) if isinstance(data.get('parameters'), list) else list(data.get('parameters', set()))
        vulns = data.get('vulnerabilities', [])
        sev_weight = {'critical':5,'high':4,'medium':3,'low':2,'info':1,None:1}
        risk_score = sum(sev_weight.get(v.get('severity'),1) for v in vulns)
        sev_counts = Counter(v.get('severity') for v in vulns)
        summary = {
            'subdomains': len(subs),
            'live_hosts': len(live),
            'urls': len(urls),
            'parameters': len(params),
            'vulnerabilities': len(vulns),
            'risk_score': risk_score,
            'severity_breakdown': dict(sev_counts)
        }
        processed = {
            'summary': summary,
            'subdomains': subs,
            'live_hosts': live,
            'urls': urls,
            'parameters': params,
            'vulnerabilities': vulns,
        }
        return processed

#!/usr/bin/env python3
"""
ReconXploit v3.0 - Report Generator
Product of Kernelpanic under infosbios.tech
"""
import json, csv, os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class ReportGenerator:
    def __init__(self):
        pass

    async def generate(self, processed: Dict[str, Any], args) -> None:
        base_dir = Path(args.output_dir) / (args.domain or 'scan')
        base_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # JSON
        with open(base_dir / f"report_{stamp}.json", 'w') as jf:
            json.dump(processed, jf, indent=2)

        # CSV summaries
        with open(base_dir / f"summary_{stamp}.csv", 'w', newline='') as cf:
            w = csv.writer(cf)
            w.writerow(['metric','value'])
            for k,v in processed['summary'].items():
                if isinstance(v, dict):
                    w.writerow([k, json.dumps(v)])
                else:
                    w.writerow([k,v])

        # HTML (basic)
        html = self._render_html(processed, args)
        with open(base_dir / f"report_{stamp}.html", 'w') as hf:
            hf.write(html)

    def _render_html(self, processed: Dict[str, Any], args) -> str:
        s = processed['summary']
        def li(items):
            return ''.join(f"<li>{x}</li>" for x in items[:200])
        return f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'/>
<title>ReconXploit Report - {args.domain}</title>
<style>
body {{ font-family: Arial, sans-serif; background:#0b0e12; color:#e6e6e6; }}
.box {{ background:#12161c; padding:16px; margin:12px 0; border-radius:8px; }}
h1, h2 {{ color:#6ee7ff; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:6px; background:#1f2937; margin-right:6px; }}
.sev-high {{ background:#b91c1c; }} .sev-med {{ background:#ca8a04; }} .sev-low {{ background:#065f46; }}
</style>
</head>
<body>
<h1>ReconXploit v3.0 — {args.domain}</h1>
<p>Product of Kernelpanic under infosbios.tech</p>
<div class='box'>
  <h2>Summary</h2>
  <div class='badge'>Subdomains: {s.get('subdomains')}</div>
  <div class='badge'>Live Hosts: {s.get('live_hosts')}</div>
  <div class='badge'>URLs: {s.get('urls')}</div>
  <div class='badge'>Parameters: {s.get('parameters')}</div>
  <div class='badge'>Vulnerabilities: {s.get('vulnerabilities')}</div>
  <div class='badge'>Risk Score: {s.get('risk_score')}</div>
</div>
<div class='box'>
  <h2>Subdomains</h2>
  <ul>{li(processed.get('subdomains', []))}</ul>
</div>
<div class='box'>
  <h2>Live Hosts</h2>
  <ul>{li(processed.get('live_hosts', []))}</ul>
</div>
<div class='box'>
  <h2>Vulnerabilities</h2>
  <ul>{li([v.get('name') or v.get('template_id') or v.get('matched_at') for v in processed.get('vulnerabilities', [])])}</ul>
</div>
</body>
</html>"""

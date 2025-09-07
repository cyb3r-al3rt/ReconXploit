#!/usr/bin/env python3
"""
ReconXploit v3.0 - Report Generator
Product of Kernelpanic under infosbios.tech
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class ReportGenerator:
    """Generate comprehensive reports in multiple formats"""

    async def generate(self, processed: Dict[str, Any], args) -> None:
        """Generate reports in specified format"""
        target = processed.get('target', args.domain or 'unknown')
        base_dir = Path(args.output_dir) / target.replace('.', '_')
        base_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if args.output == 'html':
            await self._generate_html(processed, base_dir, timestamp, args)
        elif args.output == 'json':
            await self._generate_json(processed, base_dir, timestamp, args)
        elif args.output == 'csv':
            await self._generate_csv(processed, base_dir, timestamp, args)

        if args.output != 'json':
            await self._generate_json(processed, base_dir, timestamp, args)

        print(f"\033[0;32m[REPORTS]\033[0m Generated in: {base_dir}")

    async def _generate_html(self, processed: Dict[str, Any], base_dir: Path, timestamp: str, args) -> None:
        """Generate HTML dashboard"""
        html_file = base_dir / f"reconxploit_report_{timestamp}.html"

        target = processed.get('target', 'Unknown')
        summary = processed.get('summary', {})
        data = processed.get('data', {})

        # Simple HTML template
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReconXploit Report - {target}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #0d1117;
            color: #e6edf3;
            margin: 0;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            text-align: center;
            padding: 30px;
            background: #161b22;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid #30363d;
        }}
        .header h1 {{ color: #58a6ff; font-size: 3rem; margin-bottom: 10px; }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric {{
            background: #161b22;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #30363d;
        }}
        .metric-number {{ font-size: 2rem; color: #58a6ff; font-weight: bold; }}
        .metric-label {{ color: #8b949e; margin-top: 5px; }}
        .section {{
            background: #161b22;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #30363d;
        }}
        .section h2 {{ color: #58a6ff; margin-bottom: 15px; }}
        .data-list {{ list-style: none; padding: 0; }}
        .data-list li {{
            padding: 8px;
            margin: 4px 0;
            background: #0d1117;
            border-left: 3px solid #58a6ff;
            font-family: monospace;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            margin-top: 30px;
            border-top: 1px solid #30363d;
            color: #8b949e;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 ReconXploit Report</h1>
            <p>Target: <strong>{target}</strong></p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="metrics">
            <div class="metric">
                <div class="metric-number">{summary.get('subdomains_found', 0)}</div>
                <div class="metric-label">Subdomains</div>
            </div>
            <div class="metric">
                <div class="metric-number">{summary.get('live_hosts_found', 0)}</div>
                <div class="metric-label">Live Hosts</div>
            </div>
            <div class="metric">
                <div class="metric-number">{summary.get('vulnerabilities_found', 0)}</div>
                <div class="metric-label">Vulnerabilities</div>
            </div>
            <div class="metric">
                <div class="metric-number">{summary.get('risk_score', 0)}</div>
                <div class="metric-label">Risk Score</div>
            </div>
        </div>

        <div class="section">
            <h2>🌐 Subdomains Found</h2>
            <ul class="data-list">
"""

        # Add subdomains
        subdomains = data.get('subdomains', {}).get('list', [])
        if subdomains:
            for subdomain in subdomains[:20]:  # Limit to 20
                html_content += f"                <li>{subdomain}</li>\n"
        else:
            html_content += "                <li>No subdomains found</li>\n"

        html_content += """            </ul>
        </div>

        <div class="section">
            <h2>✅ Live Hosts</h2>
            <ul class="data-list">
"""

        # Add live hosts
        live_hosts = data.get('live_hosts', {}).get('list', [])
        if live_hosts:
            for host in live_hosts[:20]:  # Limit to 20
                html_content += f"                <li>{host}</li>\n"
        else:
            html_content += "                <li>No live hosts found</li>\n"

        html_content += """            </ul>
        </div>

        <div class="section">
            <h2>⚠️ Vulnerabilities</h2>
            <ul class="data-list">
"""

        # Add vulnerabilities
        vulnerabilities = data.get('vulnerabilities', {}).get('list', [])
        if vulnerabilities:
            for vuln in vulnerabilities[:10]:  # Limit to 10
                name = vuln.get('name', 'Unknown')
                severity = vuln.get('severity', 'info').upper()
                url = vuln.get('url', 'N/A')
                html_content += f"                <li>[{severity}] {name} - {url}</li>\n"
        else:
            html_content += "                <li>No vulnerabilities found</li>\n"

        html_content += """            </ul>
        </div>

        <div class="footer">
            <p><strong>ReconXploit v3.0 - Advanced Reconnaissance Framework</strong></p>
            <p>Product of Kernelpanic under infosbios.tech</p>
            <p><em>"Control is an illusion, but reconnaissance is power."</em></p>
        </div>
    </div>
</body>
</html>"""

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"\033[0;36m[HTML]\033[0m {html_file}")

    async def _generate_json(self, processed: Dict[str, Any], base_dir: Path, timestamp: str, args) -> None:
        """Generate JSON data export"""
        json_file = base_dir / f"reconxploit_data_{timestamp}.json"

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(processed, f, indent=2, default=str)

        print(f"\033[0;36m[JSON]\033[0m {json_file}")

    async def _generate_csv(self, processed: Dict[str, Any], base_dir: Path, timestamp: str, args) -> None:
        """Generate CSV summary"""
        csv_file = base_dir / f"reconxploit_summary_{timestamp}.csv"

        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])

            summary = processed.get('summary', {})
            for key, value in summary.items():
                writer.writerow([key.replace('_', ' ').title(), value])

        print(f"\033[0;36m[CSV]\033[0m {csv_file}")

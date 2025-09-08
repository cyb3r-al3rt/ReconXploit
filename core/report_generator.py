#!/usr/bin/env python3
"""
ReconXploit v3.0 - Professional Report Generator
Product of Kernelpanic under infosbios.tech
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import os

class ReportGenerator:
    """Professional report generation system with visible HTML reports"""

    def __init__(self):
        pass

    async def generate_reports(self, processed_results: Dict[str, Any], args) -> None:
        """Generate all requested reports with proper naming"""

        print(f"\033[0;36m[REPORTS]\033[0m Generating professional reports with target+timestamp naming...")

        # Ensure output directory exists
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create proper report name with target and timestamp
        target = processed_results.get('target', 'unknown')
        clean_target = target.replace('.', '_').replace('/', '_').replace(':', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_base_name = f"{clean_target}_{timestamp}"

        # Store report info for later reference
        processed_results['report_info'] = {
            'target': target,
            'clean_target': clean_target,
            'timestamp': timestamp,
            'report_base_name': report_base_name,
            'output_dir': str(output_dir)
        }

        # Always generate HTML report (main feature)
        await self._generate_html_report(processed_results, output_dir, report_base_name, args)

        # Generate additional formats if requested
        if args.output == 'json':
            await self._generate_json_report(processed_results, output_dir, report_base_name, args)
        elif args.output == 'csv':
            await self._generate_csv_reports(processed_results, output_dir, report_base_name, args)

        # Always generate summary files
        await self._generate_summary_files(processed_results, output_dir, report_base_name)

        print(f"\033[0;32m[REPORTS]\033[0m Reports generated successfully in {output_dir}")
        print(f"\033[0;32m[REPORTS]\033[0m Main HTML Report: {report_base_name}_report.html")

    async def _generate_html_report(self, results: Dict[str, Any], output_dir: Path, report_name: str, args):
        """Generate professional HTML report that's actually visible"""

        # Prepare data for template
        summary = results.get('summary', {})
        data = results.get('data', {})
        security_score = results.get('security_score', 0)

        # Security score class determination
        if security_score >= 90:
            score_class = "score-excellent"
        elif security_score >= 70:
            score_class = "score-good"
        elif security_score >= 50:
            score_class = "score-average"
        elif security_score >= 30:
            score_class = "score-poor"
        else:
            score_class = "score-critical"

        # Generate subdomain list
        subdomains_list = ""
        subdomain_data = data.get('subdomains', {})
        for subdomain in subdomain_data.get('list', [])[:100]:
            subdomains_list += f'<div class="item">🌐 {subdomain}</div>'

        if not subdomains_list:
            subdomains_list = '<div class="item">🔍 No subdomains discovered</div>'

        # Generate live hosts list
        live_hosts_list = ""
        live_hosts_data = data.get('live_hosts', {})
        for host in live_hosts_data.get('list', [])[:100]:
            protocol_class = "success" if host.startswith('https://') else "medium"
            icon = "🔒" if host.startswith('https://') else "🌐"
            live_hosts_list += f'<div class="item"><span class="{protocol_class}">{icon} {host}</span></div>'

        if not live_hosts_list:
            live_hosts_list = '<div class="item">🔍 No live hosts detected</div>'

        # Generate ports list
        ports_list = ""
        ports_data = data.get('ports', {})
        for port_info in ports_data.get('list', [])[:100]:
            if isinstance(port_info, dict):
                port_display = f"🔌 {port_info['host']}:{port_info['port']}"
            else:
                port_display = f"🔌 {port_info}"
            ports_list += f'<div class="item">{port_display}</div>'

        if not ports_list:
            ports_list = '<div class="item">🔍 No open ports detected</div>'

        # Generate vulnerabilities content
        vulnerabilities_content = ""
        vulns_data = data.get('vulnerabilities', {})
        vulns_list = vulns_data.get('list', [])

        if vulns_list:
            vulnerabilities_content = "<table><thead><tr><th>🚨 Vulnerability</th><th>🎯 Target URL</th><th>⚡ Severity</th><th>🔧 Detection Tool</th></tr></thead><tbody>"

            for vuln in vulns_list[:50]:
                severity = vuln.get('severity', 'info').lower()
                severity_class = severity
                severity_display = severity.upper()

                vulnerabilities_content += f"<tr><td><strong>{vuln.get('name', 'Unknown Vulnerability')}</strong></td><td><code>{vuln.get('url', 'N/A')}</code></td><td><span class='{severity_class}'><strong>{severity_display}</strong></span></td><td>{vuln.get('tool', 'unknown')}</td></tr>"

            vulnerabilities_content += "</tbody></table>"
        else:
            vulnerabilities_content = '<div style="text-align: center; padding: 40px; background: rgba(16, 185, 129, 0.1); border-radius: 10px; border: 2px solid #10b981;"><h3 class="success">✅ No Security Vulnerabilities Detected!</h3><p>The target appears to have good security posture based on automated scanning.</p></div>'

        # Generate report ID and timestamps
        generation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        report_id = f"RX3-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Complete HTML template
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReconXploit v3.0 Professional - {results.get('target', 'Unknown')} Reconnaissance Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #0a0e27; 
            color: #e4e4e7; 
            line-height: 1.6;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}

        .header {{ 
            background: linear-gradient(135deg, #1f2937, #374151); 
            padding: 40px; 
            border-radius: 15px; 
            margin-bottom: 30px; 
            text-align: center; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        .header h1 {{ 
            color: #10b981; 
            font-size: 3em; 
            margin-bottom: 10px; 
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .header .subtitle {{ 
            color: #6b7280; 
            font-size: 1.3em; 
            margin-bottom: 20px;
        }}
        .target-info {{ 
            background: rgba(31, 41, 55, 0.8); 
            padding: 25px; 
            border-radius: 10px; 
            margin: 20px 0; 
            border: 1px solid #374151;
        }}
        .target-info h3 {{ color: #10b981; margin-bottom: 15px; }}

        .stats-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 25px; 
            margin: 40px 0; 
        }}
        .stat-card {{ 
            background: linear-gradient(145deg, #1f2937, #111827); 
            padding: 30px; 
            border-radius: 15px; 
            text-align: center; 
            border: 1px solid #374151; 
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        }}
        .stat-card:hover {{ 
            transform: translateY(-5px); 
            box-shadow: 0 8px 32px rgba(16, 185, 129, 0.2);
        }}
        .stat-number {{ 
            font-size: 3.2em; 
            font-weight: bold; 
            margin-bottom: 15px; 
        }}
        .stat-label {{ 
            color: #9ca3af; 
            text-transform: uppercase; 
            font-size: 0.95em; 
            letter-spacing: 1.5px; 
            font-weight: 600;
        }}

        .critical {{ color: #ef4444; }}
        .high {{ color: #f97316; }}
        .medium {{ color: #eab308; }}
        .low {{ color: #22c55e; }}
        .info {{ color: #3b82f6; }}
        .success {{ color: #10b981; }}

        .section {{ 
            background: linear-gradient(145deg, #1f2937, #111827); 
            margin: 30px 0; 
            border-radius: 15px; 
            overflow: hidden; 
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            border: 1px solid #374151;
        }}
        .section-header {{ 
            background: linear-gradient(90deg, #374151, #4b5563); 
            padding: 25px; 
            border-bottom: 2px solid #10b981;
        }}
        .section-header h2 {{ 
            color: #10b981; 
            font-size: 1.6em; 
            font-weight: 600;
        }}
        .section-content {{ padding: 30px; }}

        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 20px; 
            background: rgba(31, 41, 55, 0.5);
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{ 
            padding: 15px; 
            text-align: left; 
            border-bottom: 1px solid #374151; 
        }}
        th {{ 
            background: linear-gradient(90deg, #374151, #4b5563); 
            color: #10b981; 
            font-weight: 700; 
            text-transform: uppercase; 
            letter-spacing: 0.5px;
        }}
        tr:hover {{ background: rgba(55, 65, 81, 0.5); }}
        tr:nth-child(even) {{ background: rgba(17, 24, 39, 0.3); }}

        .item-list {{ 
            max-height: 400px; 
            overflow-y: auto; 
            border: 1px solid #374151; 
            border-radius: 8px;
        }}
        .item {{ 
            padding: 12px 20px; 
            border-bottom: 1px solid #374151; 
            transition: background-color 0.2s ease;
        }}
        .item:hover {{ background: rgba(55, 65, 81, 0.5); }}
        .item:last-child {{ border-bottom: none; }}

        .security-score {{ 
            text-align: center; 
            margin: 40px 0; 
            padding: 30px;
        }}
        .score-circle {{ 
            width: 150px; 
            height: 150px; 
            border-radius: 50%; 
            margin: 0 auto 25px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 2.5em; 
            font-weight: bold; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        .score-excellent {{ background: linear-gradient(135deg, #10b981, #059669); }}
        .score-good {{ background: linear-gradient(135deg, #22c55e, #16a34a); }}
        .score-average {{ background: linear-gradient(135deg, #eab308, #ca8a04); }}
        .score-poor {{ background: linear-gradient(135deg, #f97316, #ea580c); }}
        .score-critical {{ background: linear-gradient(135deg, #ef4444, #dc2626); }}

        .footer {{ 
            text-align: center; 
            margin-top: 60px; 
            padding: 40px; 
            background: linear-gradient(145deg, #1f2937, #111827); 
            border-radius: 15px; 
            border: 1px solid #374151;
        }}
        .footer .quote {{ 
            font-style: italic; 
            color: #10b981; 
            font-size: 1.2em; 
            margin-bottom: 20px; 
            font-weight: 500;
        }}
        .footer .credits {{ 
            color: #6b7280; 
            line-height: 1.8;
        }}

        @media (max-width: 768px) {{
            .stats-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 2.2em; }}
            .container {{ padding: 15px; }}
        }}

        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: #1f2937; }}
        ::-webkit-scrollbar-thumb {{ background: #10b981; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #059669; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 ReconXploit v3.0 Professional Report</h1>
            <div class="subtitle">Professional Reconnaissance Analysis</div>
            <div class="target-info">
                <h3>🎯 Target: <span class="success">{results.get('target', 'Unknown')}</span></h3>
                <p><strong>Report Generated:</strong> {generation_time}</p>
                <p><strong>Scan Completed:</strong> {results.get('end_time', 'Unknown')}</p>
                <p><strong>Total Execution Time:</strong> {results.get('execution_time', 0):.1f} seconds</p>
            </div>
        </div>

        <div class="security-score">
            <div class="score-circle {score_class}">
                {security_score}
            </div>
            <h3>Overall Security Score</h3>
            <p>Comprehensive security assessment based on reconnaissance findings</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number success">{summary.get('subdomains_found', 0)}</div>
                <div class="stat-label">Subdomains Discovered</div>
            </div>
            <div class="stat-card">
                <div class="stat-number info">{summary.get('live_hosts_found', 0)}</div>
                <div class="stat-label">Live Hosts Active</div>
            </div>
            <div class="stat-card">
                <div class="stat-number medium">{summary.get('open_ports_found', 0)}</div>
                <div class="stat-label">Open Ports Found</div>
            </div>
            <div class="stat-card">
                <div class="stat-number critical">{summary.get('vulnerabilities_found', 0)}</div>
                <div class="stat-label">Vulnerabilities Detected</div>
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <h2>🌐 Subdomain Discovery Results ({subdomain_data.get('total', 0)})</h2>
            </div>
            <div class="section-content">
                <p>Complete subdomain enumeration results using multiple reconnaissance tools:</p>
                <div class="item-list">{subdomains_list}</div>
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <h2>✅ Live Host Analysis ({live_hosts_data.get('total', 0)})</h2>
            </div>
            <div class="section-content">
                <p>Active HTTP/HTTPS services discovered and verified:</p>
                <div class="item-list">{live_hosts_list}</div>
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <h2>⚠️ Security Vulnerability Assessment ({vulns_data.get('total', 0)})</h2>
            </div>
            <div class="section-content">
                <p>Professional vulnerability analysis using industry-standard tools:</p>
                {vulnerabilities_content}
            </div>
        </div>

        <div class="section">
            <div class="section-header">
                <h2>🔌 Network Port Analysis ({ports_data.get('total', 0)})</h2>
            </div>
            <div class="section-content">
                <p>Comprehensive port scanning and service detection results:</p>
                <div class="item-list">{ports_list}</div>
            </div>
        </div>

        <div class="footer">
            <div class="quote">"Control is an illusion, but reconnaissance is power."</div>
            <div class="credits">
                <strong>Generated by ReconXploit v3.0 Professional Edition</strong><br>
                Product of Kernelpanic under infosbios.tech<br>
                Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)<br><br>
                <small>Report ID: {report_id}<br>
                Generated on: {generation_time}</small>
            </div>
        </div>
    </div>
</body>
</html>"""

        # Write HTML report to file
        html_file = output_dir / f"{report_name}_report.html"

        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Verify file was created and is readable
            if html_file.exists() and html_file.stat().st_size > 0:
                print(f"\033[0;32m  ✅ HTML Report Created: {html_file}\033[0m")
                print(f"\033[0;32m  📊 Report Size: {html_file.stat().st_size:,} bytes\033[0m")
            else:
                print(f"\033[0;31m  ❌ HTML Report Creation Failed: {html_file}\033[0m")
        except Exception as e:
            print(f"\033[0;31m  ❌ HTML Report Error: {str(e)}\033[0m")

    async def _generate_json_report(self, results: Dict[str, Any], output_dir: Path, report_name: str, args):
        """Generate JSON report with proper naming"""

        json_file = output_dir / f"{report_name}_report.json"

        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str, ensure_ascii=False)

            if json_file.exists():
                print(f"\033[0;32m  ✅ JSON Report Created: {json_file}\033[0m")
            else:
                print(f"\033[0;31m  ❌ JSON Report Creation Failed\033[0m")
        except Exception as e:
            print(f"\033[0;31m  ❌ JSON Report Error: {str(e)}\033[0m")

    async def _generate_csv_reports(self, results: Dict[str, Any], output_dir: Path, report_name: str, args):
        """Generate CSV reports with proper naming"""

        data = results.get('data', {})

        # Subdomains CSV
        subdomains_data = data.get('subdomains', {})
        if subdomains_data.get('list'):
            subdomains_file = output_dir / f"{report_name}_subdomains.csv"
            try:
                with open(subdomains_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Subdomain', 'Category', 'Discovery_Time'])

                    categories = subdomains_data.get('categories', {})
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    for category, subdomains in categories.items():
                        for subdomain in subdomains:
                            writer.writerow([subdomain, category, timestamp])

                if subdomains_file.exists():
                    print(f"\033[0;32m  ✅ Subdomains CSV: {subdomains_file}\033[0m")
            except Exception as e:
                print(f"\033[0;31m  ❌ Subdomains CSV Error: {str(e)}\033[0m")

        # Vulnerabilities CSV
        vulns_data = data.get('vulnerabilities', {})
        vulns_list = vulns_data.get('list', [])
        if vulns_list:
            vulns_file = output_dir / f"{report_name}_vulnerabilities.csv"
            try:
                with open(vulns_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Vulnerability_Name', 'Target_URL', 'Severity', 'Description', 'Detection_Tool', 'Discovery_Time'])

                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    for vuln in vulns_list:
                        writer.writerow([
                            vuln.get('name', ''),
                            vuln.get('url', ''),
                            vuln.get('severity', ''),
                            vuln.get('description', ''),
                            vuln.get('tool', ''),
                            timestamp
                        ])

                if vulns_file.exists():
                    print(f"\033[0;32m  ✅ Vulnerabilities CSV: {vulns_file}\033[0m")
            except Exception as e:
                print(f"\033[0;31m  ❌ Vulnerabilities CSV Error: {str(e)}\033[0m")

    async def _generate_summary_files(self, results: Dict[str, Any], output_dir: Path, report_name: str):
        """Generate quick summary files"""

        summary = results.get('summary', {})

        # Generate quick summary text file
        summary_file = output_dir / f"{report_name}_summary.txt"

        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"ReconXploit v3.0 Professional - Quick Summary\n")
                f.write(f"=" * 50 + "\n")
                f.write(f"Target: {results.get('target', 'Unknown')}\n")
                f.write(f"Scan Time: {results.get('end_time', 'Unknown')}\n")
                f.write(f"Execution Time: {results.get('execution_time', 0):.1f} seconds\n")
                f.write(f"\n")
                f.write(f"Results Summary:\n")
                f.write(f"- Subdomains Found: {summary.get('subdomains_found', 0)}\n")
                f.write(f"- Live Hosts: {summary.get('live_hosts_found', 0)}\n")
                f.write(f"- Open Ports: {summary.get('open_ports_found', 0)}\n")
                f.write(f"- URLs Discovered: {summary.get('urls_discovered', 0)}\n")
                f.write(f"- Vulnerabilities: {summary.get('vulnerabilities_found', 0)}\n")
                f.write(f"- Security Score: {results.get('security_score', 0)}/100\n")
                f.write(f"\n")
                f.write(f"Generated by ReconXploit v3.0 Professional Edition\n")
                f.write(f"Product of Kernelpanic under infosbios.tech\n")

            if summary_file.exists():
                print(f"\033[0;32m  ✅ Summary File: {summary_file}\033[0m")
        except Exception as e:
            print(f"\033[0;31m  ❌ Summary File Error: {str(e)}\033[0m")

#!/usr/bin/env python3
"""
Report Generator for ReconXploit
Generate comprehensive HTML and JSON reports
"""

import json
import time
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from colorama import Fore, Style

class ReportGenerator:
    def __init__(self, target, output_dir, results_data):
        self.target = target
        self.output_dir = Path(output_dir)
        self.results_data = results_data
        self.timestamp = datetime.now()
    
    def generate_json_report(self):
        """Generate detailed JSON report"""
        print(f"{Fore.CYAN}[*] Generating JSON report...{Style.RESET_ALL}")
        
        report_data = {
            "metadata": {
                "target": self.target,
                "timestamp": self.timestamp.isoformat(),
                "tool": "ReconXploit",
                "version": "1.0.0",
                "author": "kernelpanic"
            },
            "summary": self.results_data,
            "findings": self._analyze_findings(),
            "recommendations": self._generate_recommendations()
        }
        
        json_file = self.output_dir / "reports" / "detailed_report.json"
        with open(json_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return json_file
    
    def generate_html_report(self):
        """Generate HTML report"""
        print(f"{Fore.CYAN}[*] Generating HTML report...{Style.RESET_ALL}")
        
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReconXploit Report - {{ target }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: #0f0f0f;
            color: #00ff41;
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            border: 2px solid #00ff41;
            padding: 20px;
            background: rgba(0, 255, 65, 0.1);
        }
        
        .ascii-art {
            font-size: 8px;
            white-space: pre;
            color: #ff0040;
            margin-bottom: 20px;
        }
        
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .card {
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid #00ff41;
            padding: 20px;
            text-align: center;
        }
        
        .card h3 {
            color: #ff0040;
            margin-bottom: 10px;
        }
        
        .card .number {
            font-size: 2em;
            font-weight: bold;
        }
        
        .section {
            margin-bottom: 40px;
            border: 1px solid #00ff41;
            padding: 20px;
        }
        
        .section h2 {
            color: #ff0040;
            margin-bottom: 20px;
            border-bottom: 2px solid #00ff41;
            padding-bottom: 10px;
        }
        
        .findings-list {
            list-style: none;
        }
        
        .findings-list li {
            padding: 10px;
            margin: 5px 0;
            background: rgba(0, 255, 65, 0.05);
            border-left: 3px solid #00ff41;
        }
        
        .high-risk {
            border-left-color: #ff0040 !important;
            background: rgba(255, 0, 64, 0.1) !important;
        }
        
        .medium-risk {
            border-left-color: #ffff00 !important;
            background: rgba(255, 255, 0, 0.1) !important;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            border-top: 2px solid #00ff41;
            color: #888;
        }
        
        .quote {
            font-style: italic;
            color: #ff0040;
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="ascii-art">
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
            </div>
            <h1>Reconnaissance Report</h1>
            <p><strong>Target:</strong> {{ target }}</p>
            <p><strong>Date:</strong> {{ timestamp }}</p>
            <p><strong>Product of kernelpanic</strong></p>
        </div>

        <div class="quote">
            "Control is an illusion." - Mr. Robot
        </div>

        <div class="summary">
            {% for key, value in summary.items() %}
            <div class="card">
                <h3>{{ key.replace('_', ' ').title() }}</h3>
                <div class="number">{{ value }}</div>
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>Key Findings</h2>
            <ul class="findings-list">
                {% for finding in findings %}
                <li class="{{ finding.risk_level }}">
                    <strong>{{ finding.title }}</strong><br>
                    {{ finding.description }}
                </li>
                {% endfor %}
            </ul>
        </div>

        <div class="section">
            <h2>Recommendations</h2>
            <ul class="findings-list">
                {% for rec in recommendations %}
                <li>{{ rec }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="footer">
            <p>Generated by ReconXploit v1.0.0</p>
            <p>"The only way to patch a vulnerability is by exposing it first."</p>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            target=self.target,
            timestamp=self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            summary=self.results_data,
            findings=self._analyze_findings(),
            recommendations=self._generate_recommendations()
        )
        
        html_file = self.output_dir / "reports" / "report.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return html_file
    
    def _analyze_findings(self):
        """Analyze results and generate findings"""
        findings = []
        
        # Analyze subdomain count
        subdomain_count = self.results_data.get('subdomains', 0)
        if subdomain_count > 100:
            findings.append({
                'title': 'Large Attack Surface',
                'description': f'Found {subdomain_count} subdomains, indicating a large attack surface that requires thorough testing.',
                'risk_level': 'medium-risk'
            })
        
        # Analyze alive subdomains
        alive_count = self.results_data.get('alive_subdomains', 0)
        if alive_count > 50:
            findings.append({
                'title': 'High Number of Live Services',
                'description': f'{alive_count} live subdomains found. Each should be individually assessed for vulnerabilities.',
                'risk_level': 'medium-risk'
            })
        
        # Analyze JavaScript files
        js_count = self.results_data.get('js_files', 0)
        if js_count > 20:
            findings.append({
                'title': 'JavaScript File Exposure',
                'description': f'{js_count} JavaScript files discovered. These may contain sensitive information or endpoints.',
                'risk_level': 'medium-risk'
            })
        
        # Analyze API endpoints
        api_count = self.results_data.get('api_endpoints', 0)
        if api_count > 10:
            findings.append({
                'title': 'API Endpoints Discovered',
                'description': f'{api_count} API endpoints found. These require security testing for authentication bypasses and injection vulnerabilities.',
                'risk_level': 'high-risk'
            })
        
        # Analyze cloud services
        cloud_count = self.results_data.get('cloud_services', 0)
        if cloud_count > 0:
            findings.append({
                'title': 'Cloud Services Identified',
                'description': f'{cloud_count} cloud services found. Check for misconfigurations and exposed storage.',
                'risk_level': 'high-risk'
            })
        
        return findings
    
    def _generate_recommendations(self):
        """Generate security recommendations"""
        recommendations = [
            "Implement proper subdomain lifecycle management to reduce attack surface",
            "Regularly audit and decommission unused subdomains and services",
            "Ensure all API endpoints have proper authentication and authorization",
            "Review JavaScript files for hardcoded secrets and sensitive information",
            "Implement Content Security Policy (CSP) to prevent XSS attacks",
            "Configure cloud services with least privilege principles",
            "Enable logging and monitoring for all discovered services",
            "Perform regular vulnerability assessments on all live services",
            "Implement rate limiting and DDoS protection",
            "Use HTTPS everywhere and implement HSTS headers"
        ]
        
        return recommendations
    
    def generate_executive_summary(self):
        """Generate executive summary"""
        print(f"{Fore.CYAN}[*] Generating executive summary...{Style.RESET_ALL}")
        
        summary_text = f"""
EXECUTIVE SUMMARY - RECONNAISSANCE REPORT
==========================================

Target: {self.target}
Date: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Tool: ReconXploit v1.0.0

DISCOVERY OVERVIEW:
------------------
• Subdomains Discovered: {self.results_data.get('subdomains', 0)}
• Live Services: {self.results_data.get('alive_subdomains', 0)}
• URLs Found: {self.results_data.get('urls', 0)}
• JavaScript Files: {self.results_data.get('js_files', 0)}
• API Endpoints: {self.results_data.get('api_endpoints', 0)}
• Cloud Services: {self.results_data.get('cloud_services', 0)}

RISK ASSESSMENT:
---------------
The reconnaissance revealed a {'large' if self.results_data.get('subdomains', 0) > 50 else 'moderate'} attack surface 
with multiple entry points for potential security testing. Key areas of focus should include:

1. API Security Testing
2. Cloud Configuration Review
3. JavaScript Security Analysis
4. Subdomain Takeover Prevention

NEXT STEPS:
----------
1. Prioritize testing of live services
2. Focus on API endpoints for injection vulnerabilities
3. Review cloud services for misconfigurations
4. Analyze JavaScript files for sensitive data exposure

---
"Control is an illusion." - Mr. Robot
Product of kernelpanic
        """
        
        summary_file = self.output_dir / "reports" / "executive_summary.txt"
        with open(summary_file, 'w') as f:
            f.write(summary_text)
        
        return summary_file
    
    def generate_all_reports(self):
        """Generate all report formats"""
        print(f"{Fore.YELLOW}[*] Generating comprehensive reports...{Style.RESET_ALL}")
        
        reports = {}
        
        # Generate JSON report
        reports['json'] = self.generate_json_report()
        
        # Generate HTML report
        reports['html'] = self.generate_html_report()
        
        # Generate executive summary
        reports['summary'] = self.generate_executive_summary()
        
        print(f"{Fore.GREEN}[✓] All reports generated successfully{Style.RESET_ALL}")
        
        return reports
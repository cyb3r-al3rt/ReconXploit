#!/usr/bin/env python3
"""
ReconXploit v3.0 - Professional Result Processor
Product of Kernelpanic under infosbios.tech
"""

from typing import Dict, Any, List
from collections import Counter
import re
from datetime import datetime

class ResultProcessor:
    """Professional result processing with advanced analysis"""

    def __init__(self):
        self.severity_weights = {
            'critical': 100,
            'high': 70,
            'medium': 40,
            'low': 20,
            'info': 10
        }

    async def process_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Process results with professional-grade analysis"""

        print(f"\033[0;36m[PROCESSOR]\033[0m Processing reconnaissance results with professional analysis...")

        data = results.get('data', {})

        # Process each data type with advanced analysis
        processed_data = {
            'subdomains': await self._process_subdomains(data.get('subdomains', [])),
            'live_hosts': await self._process_live_hosts(data.get('live_hosts', [])),
            'ports': await self._process_ports(data.get('ports', [])),
            'urls': await self._process_urls(data.get('urls', [])),
            'vulnerabilities': await self._process_vulnerabilities(data.get('vulnerabilities', []))
        }

        # Generate comprehensive summary
        summary = await self._generate_summary(processed_data)

        # Calculate professional security score
        security_score = await self._calculate_security_score(processed_data)

        # Advanced threat analysis
        threat_assessment = await self._perform_threat_assessment(processed_data)

        return {
            'target': results.get('target', 'unknown'),
            'start_time': results.get('start_time'),
            'end_time': results.get('end_time'),
            'execution_time': results.get('execution_time', 0),
            'summary': summary,
            'security_score': security_score,
            'threat_assessment': threat_assessment,
            'data': processed_data,
            'statistics': results.get('statistics', {}),
            'stage_timings': results.get('stage_timings', {}),
            'errors': results.get('errors', [])
        }

    async def _process_subdomains(self, subdomains: List[str]) -> Dict[str, Any]:
        """Process subdomain data with professional categorization"""

        unique_subdomains = list(set([s.strip().lower() for s in subdomains if s and s.strip()]))

        # Professional categorization
        categories = {
            'administration': [],
            'api_services': [],
            'development': [],
            'mail_services': [],
            'cdn_assets': [],
            'databases': [],
            'monitoring': [],
            'www_services': [],
            'other': []
        }

        # Advanced subdomain analysis
        high_value_patterns = {
            'administration': ['admin', 'administrator', 'panel', 'dashboard', 'control', 'manage'],
            'api_services': ['api', 'rest', 'graphql', 'webhook', 'service', 'gateway'],
            'development': ['dev', 'test', 'staging', 'beta', 'qa', 'sandbox', 'demo'],
            'mail_services': ['mail', 'smtp', 'imap', 'webmail', 'exchange'],
            'cdn_assets': ['cdn', 'static', 'assets', 'media', 'img', 'css', 'js'],
            'databases': ['db', 'database', 'mysql', 'postgres', 'mongo', 'redis'],
            'monitoring': ['monitor', 'status', 'health', 'metrics', 'logs']
        }

        for subdomain in unique_subdomains:
            categorized = False

            for category, patterns in high_value_patterns.items():
                if any(pattern in subdomain for pattern in patterns):
                    categories[category].append(subdomain)
                    categorized = True
                    break

            if not categorized:
                if 'www' in subdomain:
                    categories['www_services'].append(subdomain)
                else:
                    categories['other'].append(subdomain)

        # Calculate risk scores
        risk_analysis = {
            'high_value_targets': len(categories['administration']) + len(categories['api_services']) + len(categories['development']),
            'exposed_services': len(categories['mail_services']) + len(categories['databases']),
            'total_attack_surface': len(unique_subdomains)
        }

        return {
            'total': len(unique_subdomains),
            'list': sorted(unique_subdomains),
            'categories': categories,
            'high_value': categories['administration'] + categories['api_services'] + categories['development'],
            'risk_analysis': risk_analysis,
            'analysis_timestamp': datetime.now().isoformat()
        }

    async def _process_live_hosts(self, live_hosts: List[str]) -> Dict[str, Any]:
        """Process live host data with security analysis"""

        unique_hosts = list(set([h.strip() for h in live_hosts if h and h.strip()]))

        # Protocol and security analysis
        protocols = Counter()
        security_features = {
            'https_hosts': [],
            'http_only_hosts': [],
            'mixed_content_risk': []
        }

        for host in unique_hosts:
            if host.startswith('https://'):
                protocols['https'] += 1
                security_features['https_hosts'].append(host)
            elif host.startswith('http://'):
                protocols['http'] += 1
                security_features['http_only_hosts'].append(host)
                # Check for mixed content risk
                domain = host.replace('http://', '').split('/')[0]
                https_equivalent = f"https://{domain}"
                if https_equivalent in unique_hosts:
                    security_features['mixed_content_risk'].append(host)

        # Security metrics calculation
        total_hosts = len(unique_hosts)
        https_ratio = protocols.get('https', 0) / max(total_hosts, 1)

        return {
            'total': total_hosts,
            'list': sorted(unique_hosts),
            'protocols': dict(protocols),
            'https_ratio': https_ratio,
            'security_features': security_features,
            'security_metrics': {
                'https_adoption': f"{https_ratio:.1%}",
                'insecure_count': len(security_features['http_only_hosts']),
                'mixed_content_risks': len(security_features['mixed_content_risk']),
                'security_score': min(100, int(https_ratio * 100) + (10 if https_ratio > 0.8 else 0))
            }
        }

    async def _process_ports(self, ports: List[str]) -> Dict[str, Any]:
        """Process port scanning data with service analysis"""

        port_data = []
        service_categories = {
            'web_services': [],
            'database_services': [],
            'mail_services': [],
            'remote_access': [],
            'file_services': [],
            'other_services': []
        }

        # Service port mappings
        service_ports = {
            'web_services': [80, 443, 8080, 8443, 8000, 8008, 9000, 3000],
            'database_services': [3306, 5432, 1433, 27017, 6379, 5984],
            'mail_services': [25, 587, 465, 993, 995, 110, 143],
            'remote_access': [22, 3389, 5900, 23],
            'file_services': [21, 22, 139, 445, 2049]
        }

        for port_str in ports:
            if ':' in port_str:
                try:
                    host, port = port_str.rsplit(':', 1)
                    port_num = int(port.split('/')[0])

                    port_info = {
                        'host': host,
                        'port': port_num,
                        'service': self._identify_service(port_num),
                        'risk_level': self._assess_port_risk(port_num),
                        'full': port_str
                    }

                    # Categorize by service type
                    categorized = False
                    for category, port_list in service_ports.items():
                        if port_num in port_list:
                            service_categories[category].append(port_info)
                            categorized = True
                            break

                    if not categorized:
                        service_categories['other_services'].append(port_info)

                    port_data.append(port_info)

                except (ValueError, IndexError):
                    continue

        # Risk assessment
        risk_analysis = {
            'critical_exposures': len([p for p in port_data if p['risk_level'] == 'critical']),
            'database_exposure': len(service_categories['database_services']),
            'remote_access_exposure': len(service_categories['remote_access']),
            'web_services': len(service_categories['web_services']),
            'total_exposed_services': len(port_data),
            'risk_score': sum(self._get_risk_weight(p['risk_level']) for p in port_data)
        }

        return {
            'total': len(port_data),
            'list': port_data,
            'service_categories': service_categories,
            'unique_ports': list(set(p['port'] for p in port_data)),
            'risk_analysis': risk_analysis,
            'security_recommendations': self._generate_port_recommendations(risk_analysis)
        }

    def _identify_service(self, port: int) -> str:
        """Identify service by port number"""
        common_services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 993: 'IMAPS',
            995: 'POP3S', 1433: 'MSSQL', 3306: 'MySQL', 3389: 'RDP',
            5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis', 8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt', 27017: 'MongoDB'
        }
        return common_services.get(port, f'Unknown ({port})')

    def _assess_port_risk(self, port: int) -> str:
        """Assess security risk level for a port"""
        critical_ports = [21, 23, 135, 139, 445, 1433, 3306, 3389, 5432, 27017]
        high_ports = [22, 25, 53, 110, 143, 993, 995, 6379]
        medium_ports = [80, 443, 8080, 8443]

        if port in critical_ports:
            return 'critical'
        elif port in high_ports:
            return 'high'
        elif port in medium_ports:
            return 'medium'
        else:
            return 'low'

    def _get_risk_weight(self, risk_level: str) -> int:
        """Get numeric weight for risk level"""
        weights = {'critical': 10, 'high': 7, 'medium': 4, 'low': 1}
        return weights.get(risk_level, 1)

    def _generate_port_recommendations(self, risk_analysis: Dict) -> List[str]:
        """Generate security recommendations based on port analysis"""
        recommendations = []

        if risk_analysis['database_exposure'] > 0:
            recommendations.append("Database services detected. Ensure proper access controls and firewall rules.")

        if risk_analysis['remote_access_exposure'] > 0:
            recommendations.append("Remote access services exposed. Implement strong authentication and monitoring.")

        if risk_analysis['critical_exposures'] > 0:
            recommendations.append("Critical service exposures detected. Review necessity and implement security hardening.")

        return recommendations

    async def _process_urls(self, urls: List[str]) -> Dict[str, Any]:
        """Process URL data with categorization"""
        unique_urls = list(set([u.strip() for u in urls if u and u.strip()]))

        return {
            'total': len(unique_urls),
            'list': unique_urls[:200],  # Limit for performance
            'analysis_timestamp': datetime.now().isoformat()
        }

    async def _process_vulnerabilities(self, vulnerabilities: List[Dict]) -> Dict[str, Any]:
        """Process vulnerability data with professional assessment"""

        if not vulnerabilities:
            return {
                'total': 0,
                'list': [],
                'by_severity': {},
                'by_tool': {},
                'risk_score': 0,
                'threat_level': 'minimal'
            }

        # Deduplicate vulnerabilities
        seen = set()
        unique_vulns = []
        for vuln in vulnerabilities:
            vuln_id = (vuln.get('name', ''), vuln.get('url', ''))
            if vuln_id not in seen:
                seen.add(vuln_id)
                unique_vulns.append(vuln)

        # Categorize by severity
        by_severity = {'critical': [], 'high': [], 'medium': [], 'low': [], 'info': []}
        for vuln in unique_vulns:
            severity = vuln.get('severity', 'info').lower()
            if severity in by_severity:
                by_severity[severity].append(vuln)

        # Categorize by tool
        by_tool = {}
        for vuln in unique_vulns:
            tool = vuln.get('tool', 'unknown')
            if tool not in by_tool:
                by_tool[tool] = []
            by_tool[tool].append(vuln)

        # Calculate comprehensive risk score
        risk_score = 0
        for severity, vulns in by_severity.items():
            count = len(vulns)
            weight = self.severity_weights.get(severity, 10)
            risk_score += count * weight

        # Determine threat level
        threat_level = self._determine_threat_level(by_severity, risk_score)

        return {
            'total': len(unique_vulns),
            'list': unique_vulns,
            'by_severity': by_severity,
            'by_tool': by_tool,
            'risk_score': risk_score,
            'threat_level': threat_level,
            'severity_distribution': {k: len(v) for k, v in by_severity.items() if v},
            'recommendations': self._generate_vuln_recommendations(by_severity)
        }

    def _determine_threat_level(self, by_severity: Dict, risk_score: int) -> str:
        """Determine overall threat level"""
        critical_count = len(by_severity.get('critical', []))
        high_count = len(by_severity.get('high', []))

        if critical_count > 5 or risk_score > 500:
            return 'critical'
        elif critical_count > 0 or high_count > 3 or risk_score > 200:
            return 'high'
        elif high_count > 0 or risk_score > 50:
            return 'medium'
        elif risk_score > 0:
            return 'low'
        else:
            return 'minimal'

    def _generate_vuln_recommendations(self, by_severity: Dict) -> List[str]:
        """Generate security recommendations based on vulnerabilities"""
        recommendations = []

        if by_severity.get('critical'):
            recommendations.append("CRITICAL: Immediate remediation required for critical vulnerabilities.")

        if by_severity.get('high'):
            recommendations.append("HIGH: Address high-severity vulnerabilities within 24-48 hours.")

        if by_severity.get('medium'):
            recommendations.append("MEDIUM: Plan remediation for medium-severity vulnerabilities within 1 week.")

        return recommendations

    async def _generate_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive professional summary"""

        return {
            'subdomains_found': data.get('subdomains', {}).get('total', 0),
            'live_hosts_found': data.get('live_hosts', {}).get('total', 0),
            'open_ports_found': data.get('ports', {}).get('total', 0),
            'urls_discovered': data.get('urls', {}).get('total', 0),
            'vulnerabilities_found': data.get('vulnerabilities', {}).get('total', 0),

            # Advanced metrics
            'high_value_subdomains': len(data.get('subdomains', {}).get('high_value', [])),
            'critical_vulnerabilities': data.get('vulnerabilities', {}).get('by_severity', {}).get('critical', []),
            'database_exposure': data.get('ports', {}).get('risk_analysis', {}).get('database_exposure', 0),
            'insecure_hosts': len(data.get('live_hosts', {}).get('security_features', {}).get('http_only_hosts', [])),

            # Security metrics
            'https_adoption': data.get('live_hosts', {}).get('security_metrics', {}).get('https_adoption', '0%'),
            'threat_level': data.get('vulnerabilities', {}).get('threat_level', 'minimal'),
            'risk_score': data.get('vulnerabilities', {}).get('risk_score', 0),

            # Analysis metadata
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_quality': 'professional'
        }

    async def _calculate_security_score(self, data: Dict[str, Any]) -> int:
        """Calculate comprehensive professional security score (0-100, higher is better)"""

        base_score = 100

        # Deduct for vulnerabilities (weighted)
        vulns = data.get('vulnerabilities', {}).get('by_severity', {})
        base_score -= len(vulns.get('critical', [])) * 30
        base_score -= len(vulns.get('high', [])) * 20
        base_score -= len(vulns.get('medium', [])) * 10
        base_score -= len(vulns.get('low', [])) * 5

        # Deduct for exposed services
        ports_risk = data.get('ports', {}).get('risk_analysis', {})
        base_score -= ports_risk.get('database_exposure', 0) * 15
        base_score -= ports_risk.get('remote_access_exposure', 0) * 10
        base_score -= ports_risk.get('critical_exposures', 0) * 20

        # Deduct for insecure protocols
        live_hosts = data.get('live_hosts', {})
        insecure_count = len(live_hosts.get('security_features', {}).get('http_only_hosts', []))
        base_score -= insecure_count * 5

        # Add bonus for good security practices
        https_ratio = live_hosts.get('https_ratio', 0)
        base_score += https_ratio * 15

        # Deduct for large attack surface
        subdomain_count = data.get('subdomains', {}).get('total', 0)
        if subdomain_count > 50:
            base_score -= min(20, (subdomain_count - 50) // 10)

        return max(0, min(100, base_score))

    async def _perform_threat_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced threat assessment"""

        threat_vectors = []

        # Check for common threat vectors
        if data.get('vulnerabilities', {}).get('by_severity', {}).get('critical'):
            threat_vectors.append("Critical vulnerabilities present")

        if data.get('ports', {}).get('risk_analysis', {}).get('database_exposure', 0) > 0:
            threat_vectors.append("Database services exposed")

        if data.get('subdomains', {}).get('categories', {}).get('administration'):
            threat_vectors.append("Administrative interfaces exposed")

        attack_surface_score = (
            data.get('subdomains', {}).get('total', 0) * 0.1 +
            data.get('live_hosts', {}).get('total', 0) * 0.5 +
            data.get('ports', {}).get('total', 0) * 1.0
        )

        return {
            'threat_vectors': threat_vectors,
            'attack_surface_score': min(100, attack_surface_score),
            'overall_risk': data.get('vulnerabilities', {}).get('threat_level', 'minimal'),
            'assessment_timestamp': datetime.now().isoformat()
        }

# ReconXploit Configuration Guide

This guide covers the configuration options and API key setup for ReconXploit to maximize its effectiveness.

## API Keys Configuration

### Subfinder Configuration

Create the configuration directory and file:

```bash
mkdir -p ~/.config/subfinder
```

Create the provider configuration file:

```yaml
# ~/.config/subfinder/provider-config.yaml

binaryedge:
  - "YOUR_BINARYEDGE_API_KEY"

censys:
  - "YOUR_CENSYS_API_ID:YOUR_CENSYS_SECRET"

chaos:
  - "YOUR_CHAOS_API_KEY"

fofa:
  - "YOUR_FOFA_EMAIL:YOUR_FOFA_KEY"

shodan:
  - "YOUR_SHODAN_API_KEY"

spyse:
  - "YOUR_SPYSE_API_TOKEN"

virustotal:
  - "YOUR_VIRUSTOTAL_API_KEY"

zoomeye:
  - "YOUR_ZOOMEYE_API_KEY"

securitytrails:
  - "YOUR_SECURITYTRAILS_API_KEY"

passivetotal:
  - "YOUR_PASSIVETOTAL_USERNAME:YOUR_PASSIVETOTAL_API_KEY"

github:
  - "YOUR_GITHUB_TOKEN"

intelx:
  - "YOUR_INTELX_API_KEY:YOUR_INTELX_UUID"
```

### Amass Configuration

Create the Amass configuration directory:

```bash
mkdir -p ~/.config/amass
```

Create the configuration file:

```ini
# ~/.config/amass/config.ini

[data_sources]

[data_sources.Chaos]
[data_sources.Chaos.Credentials]
apikey = "YOUR_CHAOS_API_KEY"

[data_sources.Shodan]
[data_sources.Shodan.Credentials]
apikey = "YOUR_SHODAN_API_KEY"

[data_sources.VirusTotal]
[data_sources.VirusTotal.Credentials]
apikey = "YOUR_VIRUSTOTAL_API_KEY"

[data_sources.SecurityTrails]
[data_sources.SecurityTrails.Credentials]
apikey = "YOUR_SECURITYTRAILS_API_KEY"

[data_sources.PassiveTotal]
[data_sources.PassiveTotal.Credentials]
username = "YOUR_PASSIVETOTAL_USERNAME"
apikey = "YOUR_PASSIVETOTAL_API_KEY"

[data_sources.BinaryEdge]
[data_sources.BinaryEdge.Credentials]
apikey = "YOUR_BINARYEDGE_API_KEY"

[data_sources.Censys]
[data_sources.Censys.Credentials]
apikey = "YOUR_CENSYS_API_KEY"
secret = "YOUR_CENSYS_SECRET"

[data_sources.GitHub]
[data_sources.GitHub.Credentials]
apikey = "YOUR_GITHUB_TOKEN"

[data_sources.ZoomEye]
[data_sources.ZoomEye.Credentials]
username = "YOUR_ZOOMEYE_USERNAME"
password = "YOUR_ZOOMEYE_PASSWORD"
```

### Nuclei Configuration

Nuclei templates are automatically updated, but you can configure custom templates:

```bash
# Download templates
nuclei -update-templates

# Custom templates directory
mkdir -p ~/.nuclei-templates/custom
```

### GAU Configuration

Configure GAU providers:

```bash
# Set environment variables
export ALIEN_VAULT_OTX_KEY="YOUR_OTX_API_KEY"
export GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
```

## Environment Variables

Create a `.env` file in the ReconXploit directory:

```bash
# .env file

# API Keys
SHODAN_API_KEY="your_shodan_api_key"
VIRUSTOTAL_API_KEY="your_virustotal_api_key"
CHAOS_API_KEY="your_chaos_api_key"
SECURITYTRAILS_API_KEY="your_securitytrails_api_key"
BINARYEDGE_API_KEY="your_binaryedge_api_key"
CENSYS_API_ID="your_censys_api_id"
CENSYS_SECRET="your_censys_secret"
GITHUB_TOKEN="your_github_token"

# Proxy Configuration
HTTP_PROXY="http://proxy.example.com:8080"
HTTPS_PROXY="https://proxy.example.com:8080"

# Rate Limiting
REQUEST_DELAY=1
MAX_THREADS=50

# Timeout Settings
REQUEST_TIMEOUT=30
TOOL_TIMEOUT=300
```

## Configuration File

Create a YAML configuration file for ReconXploit:

```yaml
# config.yaml

# General Settings
general:
  threads: 50
  timeout: 30
  delay: 1
  retries: 3
  user_agent: "ReconXploit/1.0.0"

# Tool Configuration
tools:
  amass:
    enabled: true
    timeout: 300
    brute: true
    wordlist: "wordlists/common_subdomains.txt"
  
  subfinder:
    enabled: true
    timeout: 180
    all_sources: true
  
  httpx:
    enabled: true
    status_code: true
    title: true
    tech_detect: true
  
  nuclei:
    enabled: true
    templates: ["cves", "exposures", "misconfigurations"]
    severity: ["critical", "high", "medium"]

# Output Configuration
output:
  format: ["json", "txt", "html"]
  screenshots: true
  verbose: true

# Proxy Configuration
proxy:
  enabled: false
  http: "http://proxy.example.com:8080"
  https: "https://proxy.example.com:8080"

# Rate Limiting
rate_limit:
  requests_per_second: 10
  burst: 20
  delay: 0.1

# Wordlists
wordlists:
  subdomains: "wordlists/common_subdomains.txt"
  directories: "wordlists/common_directories.txt"
  files: "wordlists/common_files.txt"

# Cloud Configuration
cloud:
  aws:
    check_s3: true
    regions: ["us-east-1", "us-west-2", "eu-west-1"]
  
  azure:
    check_blob: true
    check_functions: true
  
  gcp:
    check_storage: true
    check_functions: true

# Notification Settings
notifications:
  enabled: false
  slack:
    webhook_url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
  
  discord:
    webhook_url: "https://discord.com/api/webhooks/YOUR/DISCORD/WEBHOOK"
  
  email:
    smtp_server: "smtp.gmail.com"
    port: 587
    username: "your_email@gmail.com"
    password: "your_app_password"
    to: "recipient@example.com"
```

## API Key Sources

### Free API Keys

1. **VirusTotal** - https://www.virustotal.com/gui/join-us
2. **Shodan** - https://www.shodan.io/ (100 free searches/month)
3. **GitHub** - https://github.com/settings/tokens
4. **Chaos** - https://chaos.projectdiscovery.io/

### Paid API Keys

1. **SecurityTrails** - https://securitytrails.com/
2. **BinaryEdge** - https://www.binaryedge.io/
3. **Censys** - https://search.censys.io/
4. **PassiveTotal** - https://community.riskiq.com/

## Performance Tuning

### Thread Configuration

```yaml
# High-performance configuration
threads: 100
concurrent_tools: 5
batch_size: 1000

# Conservative configuration
threads: 20
concurrent_tools: 2
batch_size: 100
```

### Memory Optimization

```yaml
# Memory-efficient settings
cache_results: false
stream_output: true
compress_files: true
cleanup_temp: true
```

### Network Optimization

```yaml
# Network settings
keep_alive: true
connection_pool: 50
dns_servers: ["8.8.8.8", "1.1.1.1"]
resolve_timeout: 5
```

## Troubleshooting

### Common Issues

1. **Rate Limiting**
   - Increase delays between requests
   - Reduce thread count
   - Use proxy rotation

2. **API Quota Exceeded**
   - Check API usage limits
   - Rotate API keys
   - Enable caching

3. **Tool Not Found**
   - Verify PATH configuration
   - Check tool installation
   - Update binary paths

### Debug Mode

Enable debug mode for troubleshooting:

```bash
reconxploit -d example.com --debug -v
```

### Log Configuration

```yaml
logging:
  level: INFO
  file: "reconxploit.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_size: "10MB"
  backup_count: 5
```

## Security Considerations

### API Key Security

1. **Never commit API keys to version control**
2. **Use environment variables or secure configuration files**
3. **Rotate API keys regularly**
4. **Monitor API key usage**

### Proxy Configuration

```yaml
proxy:
  enabled: true
  rotation: true
  list: [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080"
  ]
  authentication:
    username: "proxy_user"
    password: "proxy_password"
```

### SSL/TLS Configuration

```yaml
ssl:
  verify: true
  cert_file: "/path/to/client.crt"
  key_file: "/path/to/client.key"
  ca_bundle: "/path/to/ca-bundle.crt"
```

## Advanced Configuration

### Custom Scripts

```yaml
custom_scripts:
  pre_scan: "/path/to/pre_scan.sh"
  post_scan: "/path/to/post_scan.sh"
  notification: "/path/to/notify.py"
```

### Database Configuration

```yaml
database:
  enabled: true
  type: "sqlite"  # or postgresql, mysql
  path: "reconxploit.db"
  # For PostgreSQL/MySQL
  host: "localhost"
  port: 5432
  username: "reconxploit"
  password: "secure_password"
  database: "reconxploit_db"
```

### Integration with Other Tools

```yaml
integrations:
  burp_suite:
    enabled: true
    api_url: "http://localhost:1337"
    api_key: "your_burp_api_key"
  
  defectdojo:
    enabled: true
    url: "https://defectdojo.example.com"
    api_key: "your_defectdojo_api_key"
  
  jira:
    enabled: true
    url: "https://your-domain.atlassian.net"
    username: "your_email@example.com"
    api_token: "your_jira_api_token"
    project_key: "RECON"
```

---

Remember to keep your configuration files secure and never share API keys publicly!
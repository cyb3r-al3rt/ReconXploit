# ReconXploit Installation Guide

## Quick Start for Kali Linux

### Automatic Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/kernelpanic/reconxploit.git
cd reconxploit

# Run the automated installer
chmod +x install.sh
./install.sh

# Test the installation
reconxploit --check-tools
```

### Manual Installation

If you prefer manual installation or the automatic installer fails:

#### 1. System Requirements

- **OS**: Kali Linux, Ubuntu 20.04+, Debian 11+
- **Python**: 3.8 or higher
- **Go**: 1.19 or higher
- **Memory**: Minimum 4GB RAM
- **Storage**: At least 10GB free space

#### 2. Install System Dependencies

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    python3-dev \
    golang-go \
    npm \
    nodejs \
    build-essential \
    unzip \
    masscan \
    nmap

# Install Go (if not latest version)
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
```

#### 3. Install Python Dependencies

```bash
# Install required Python packages
pip3 install -r requirements.txt

# Or install manually
pip3 install colorama requests urllib3 dnspython jinja2 \
             beautifulsoup4 lxml pandas numpy plotly \
             click python-dateutil psutil netifaces \
             netaddr validators python-whois
```

#### 4. Install Go-based Tools

```bash
# Create tools directory
mkdir -p ~/tools
export PATH=$PATH:~/go/bin

# Install reconnaissance tools
echo "Installing Go-based tools..."

# Amass - OWASP subdomain enumeration
go install -v github.com/owasp-amass/amass/v4/cmd/amass@latest

# Subfinder - Fast subdomain discovery
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Httpx - HTTP toolkit
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Nuclei - Vulnerability scanner
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Katana - Web crawler
go install github.com/projectdiscovery/katana/cmd/katana@latest

# GAU - Get All URLs
go install github.com/lc/gau/v2/cmd/gau@latest

# Waybackurls - Wayback Machine URLs
go install github.com/tomnomnom/waybackurls@latest

# Assetfinder - Domain/subdomain finder
go install github.com/tomnomnom/assetfinder@latest

# GF - Grep on steroids
go install github.com/tomnomnom/gf@latest

# FFUF - Web fuzzer
go install github.com/ffuf/ffuf/v2@latest

# Gospider - Web spider
go install github.com/jaeles-project/gospider@latest

echo "Go tools installation completed!"
```

#### 5. Install Python-based Tools

```bash
cd ~/tools

# Sublist3r
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r
pip3 install -r requirements.txt
sudo ln -sf $PWD/sublist3r.py /usr/local/bin/sublist3r
cd ..

# Dirsearch
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch
pip3 install -r requirements.txt
sudo ln -sf $PWD/dirsearch.py /usr/local/bin/dirsearch
cd ..

echo "Python tools installation completed!"
```

#### 6. Install Additional Tools

```bash
# Findomain
wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip
unzip findomain-linux.zip
chmod +x findomain
sudo mv findomain /usr/local/bin/

# Aquatone (for screenshots)
wget https://github.com/michenriksen/aquatone/releases/latest/download/aquatone_linux_amd64_1.7.0.zip
unzip aquatone_linux_amd64_1.7.0.zip
chmod +x aquatone
sudo mv aquatone /usr/local/bin/

# Clean up
rm -f *.zip

echo "Additional tools installation completed!"
```

#### 7. Setup GF Patterns

```bash
# Create GF directory
mkdir -p ~/.gf

# Install community patterns
git clone https://github.com/1ndianl33t/Gf-Patterns.git
cp Gf-Patterns/*.json ~/.gf/

# Install official patterns
git clone https://github.com/tomnomnom/gf.git
cp gf/examples/*.json ~/.gf/

# Clean up
rm -rf Gf-Patterns gf

echo "GF patterns installed!"
```

#### 8. Configure Environment

```bash
# Add Go and local bin to PATH
echo 'export PATH=$PATH:~/go/bin:/usr/local/bin' >> ~/.bashrc
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
source ~/.bashrc

# Download Nuclei templates
nuclei -update-templates

# Create ReconXploit symlink
cd /path/to/reconxploit
chmod +x reconxploit.py
sudo ln -sf $PWD/reconxploit.py /usr/local/bin/reconxploit

echo "Environment configuration completed!"
```

## API Keys Configuration

### Essential API Keys (Free)

1. **VirusTotal API Key**
   ```bash
   # Register at https://www.virustotal.com/gui/join-us
   mkdir -p ~/.config/subfinder
   echo 'virustotal: ["YOUR_VT_API_KEY"]' >> ~/.config/subfinder/provider-config.yaml
   ```

2. **GitHub Token**
   ```bash
   # Create at https://github.com/settings/tokens
   echo 'github: ["YOUR_GITHUB_TOKEN"]' >> ~/.config/subfinder/provider-config.yaml
   ```

3. **Chaos API Key**
   ```bash
   # Register at https://chaos.projectdiscovery.io/
   echo 'chaos: ["YOUR_CHAOS_API_KEY"]' >> ~/.config/subfinder/provider-config.yaml
   ```

### Advanced API Keys (Optional)

1. **Shodan API Key**
   ```bash
   # Register at https://www.shodan.io/
   echo 'shodan: ["YOUR_SHODAN_API_KEY"]' >> ~/.config/subfinder/provider-config.yaml
   ```

2. **SecurityTrails API Key**
   ```bash
   # Register at https://securitytrails.com/
   echo 'securitytrails: ["YOUR_ST_API_KEY"]' >> ~/.config/subfinder/provider-config.yaml
   ```

## Verification

### Test Installation

```bash
# Check tool availability
reconxploit --check-tools

# Test with domain (dry run)
reconxploit -d example.com --quick

# Verify individual tools
amass version
subfinder -version
httpx -version
nuclei -version
```

### Expected Output

```
[✓] amass - Available
[✓] subfinder - Available
[✓] sublist3r - Available
[✓] waybackurls - Available
[✓] gau - Available
[✓] gf - Available
[✓] katana - Available
[✓] httpx - Available
[✓] nuclei - Available
[✓] ffuf - Available
[✓] dirsearch - Available
[✓] gospider - Available
[✓] assetfinder - Available
[✓] findomain - Available
[✓] aquatone - Available
[✓] masscan - Available
[✓] nmap - Available
```

## Troubleshooting

### Common Issues

#### 1. Go Tools Not Found

```bash
# Check Go installation
go version

# Check GOPATH
echo $GOPATH

# Reinstall Go tools
go clean -modcache
go install -v github.com/owasp-amass/amass/v4/cmd/amass@latest
```

#### 2. Python Module Errors

```bash
# Update pip
pip3 install --upgrade pip

# Reinstall requirements
pip3 install -r requirements.txt --upgrade --force-reinstall
```

#### 3. Permission Errors

```bash
# Fix permissions
sudo chown -R $USER:$USER ~/go
chmod +x reconxploit.py

# Fix PATH issues
echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
source ~/.bashrc
```

#### 4. DNS Resolution Issues

```bash
# Configure DNS
echo 'nameserver 8.8.8.8' | sudo tee -a /etc/resolv.conf
echo 'nameserver 1.1.1.1' | sudo tee -a /etc/resolv.conf
```

### Performance Optimization

#### For High-Performance Systems

```bash
# Increase file limits
echo '* soft nofile 65536' | sudo tee -a /etc/security/limits.conf
echo '* hard nofile 65536' | sudo tee -a /etc/security/limits.conf

# Optimize network settings
echo 'net.core.rmem_max = 134217728' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

#### For Low-Resource Systems

```bash
# Use fewer threads
reconxploit -d example.com --threads 10

# Enable quick mode
reconxploit -d example.com --quick
```

## Docker Installation

### Using Docker (Alternative)

```bash
# Build Docker image
docker build -t reconxploit .

# Run container
docker run -it --rm -v $(pwd)/results:/app/results reconxploit -d example.com
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  reconxploit:
    build: .
    volumes:
      - ./results:/app/results
      - ./wordlists:/app/wordlists
    environment:
      - VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}
      - SHODAN_API_KEY=${SHODAN_API_KEY}
```

## Next Steps

After successful installation:

1. **Configure API Keys** - See [CONFIGURATION.md](docs/CONFIGURATION.md)
2. **Run First Scan** - `reconxploit -d example.com`
3. **Review Output** - Check `results/` directory
4. **Customize Settings** - Edit configuration files
5. **Join Community** - Report bugs and contribute

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/kernelpanic/reconxploit/issues)
- **Community**: [Discussions](https://github.com/kernelpanic/reconxploit/discussions)

---

*"Control is an illusion." - Mr. Robot*
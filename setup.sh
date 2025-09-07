#!/bin/bash
# ReconXploit v3.0 - Setup Script

echo "🔧 ReconXploit v3.0 Setup"
echo "========================="

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install colorama pyyaml requests aiohttp beautifulsoup4 lxml dnspython click jinja2

# Set permissions
echo "Setting permissions..."
chmod +x reconxploit

# Create directories
echo "Creating directories..."
mkdir -p {config,logs,results,wordlists}

echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Test with: ./reconxploit --check-tools"
echo "2. Run scan: ./reconxploit -d example.com"

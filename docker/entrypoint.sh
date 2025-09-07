#!/bin/bash
# ReconXploit v3.0 - Docker Entrypoint
# Product of Kernelpanic under infosbios.tech

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
cat << "EOF"
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   

                      ReconXploit v3.0 - Docker Container
                   Product of Kernelpanic under infosbios.tech
EOF
echo -e "${NC}"

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

export PATH=$PATH:$GOPATH/bin
export PYTHONPATH=$RECONXPLOIT_HOME

source $RECONXPLOIT_HOME/venv/bin/activate

mkdir -p $RECONXPLOIT_HOME/results
mkdir -p $RECONXPLOIT_HOME/logs
mkdir -p $RECONXPLOIT_HOME/config

chmod -R 755 $RECONXPLOIT_HOME/results
chmod -R 755 $RECONXPLOIT_HOME/logs

NUCLEI_TEMPLATES_DIR="$HOME/.nuclei-templates"
if [[ ! -d "$NUCLEI_TEMPLATES_DIR" ]] || [[ $(find "$NUCLEI_TEMPLATES_DIR" -mtime +1) ]]; then
    print_status "Updating nuclei templates..."
    nuclei -update-templates -silent
fi

if [[ -f "$RECONXPLOIT_HOME/config/api_keys.yaml" ]]; then
    print_status "API keys configuration found"
else
    print_status "No API keys configured. Some features may be limited."
fi

case "$1" in
    --setup-keys)
        print_status "Starting API key setup..."
        python3 $RECONXPLOIT_HOME/scripts/setup_api_keys.py
        ;;
    --check-tools)
        print_status "Checking tool installation..."
        python3 $RECONXPLOIT_HOME/core/reconxploit.py --check-tools
        ;;
    --shell)
        print_status "Starting interactive shell..."
        exec /bin/bash
        ;;
    --help|help)
        echo -e "${CYAN}ReconXploit v3.0 - Docker Usage${NC}"
        echo
        echo "Basic usage:"
        echo "  docker run kernelpanic/reconxploit:3.0.0 -d example.com"
        echo
        echo "Docker-specific commands:"
        echo "  --setup-keys       Setup API keys interactively" 
        echo "  --check-tools      Check tool installation"
        echo "  --shell            Start interactive shell"
        echo "  --help             Show this help"
        echo
        ;;
    *)
        print_status "Starting ReconXploit with arguments: $*"
        exec python3 $RECONXPLOIT_HOME/core/reconxploit.py "$@"
        ;;
esac

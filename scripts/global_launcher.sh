#!/bin/bash
# ReconXploit v3.0 - Fixed Global Launcher
# Product of Kernelpanic under infosbios.tech

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Auto-detect ReconXploit installation directory
detect_reconxploit_dir() {
    # Check environment variable first
    if [[ -n "$RECONXPLOIT_HOME" && -f "$RECONXPLOIT_HOME/core/reconxploit.py" ]]; then
        echo "$RECONXPLOIT_HOME"
        return 0
    fi

    # Common installation locations
    POSSIBLE_DIRS=(
        "$HOME/ReconXploit"
        "$HOME/reconxploit"
        "$HOME/tools/ReconXploit"
        "$HOME/tools/reconxploit"
        "/opt/reconxploit"
        "/opt/ReconXploit"
        "/usr/local/share/reconxploit"
        "/usr/local/share/ReconXploit"
    )

    # Check each possible directory
    for dir in "${POSSIBLE_DIRS[@]}"; do
        if [[ -f "$dir/core/reconxploit.py" ]]; then
            echo "$dir"
            return 0
        fi
    done

    # Search in user's home directory
    if command -v find >/dev/null 2>&1; then
        local found_dirs=$(find "$HOME" -name "reconxploit.py" -path "*/core/*" -type f 2>/dev/null | head -1)
        if [[ -n "$found_dirs" ]]; then
            # Extract directory (remove /core/reconxploit.py)
            local dir=$(dirname "$(dirname "$found_dirs")")
            if [[ -f "$dir/core/reconxploit.py" ]]; then
                echo "$dir"
                return 0
            fi
        fi
    fi

    return 1
}

# Detect ReconXploit installation
print_info "Detecting ReconXploit installation..."
RECONXPLOIT_DIR=$(detect_reconxploit_dir)

if [[ -z "$RECONXPLOIT_DIR" ]]; then
    print_error "ReconXploit installation not found!"
    echo ""
    echo "Please ensure ReconXploit is installed in one of these locations:"
    echo "  $HOME/ReconXploit"
    echo "  $HOME/tools/ReconXploit"  
    echo "  /opt/reconxploit"
    echo ""
    echo "Or set the RECONXPLOIT_HOME environment variable:"
    echo "  export RECONXPLOIT_HOME=/path/to/reconxploit"
    echo "  echo 'export RECONXPLOIT_HOME=/path/to/reconxploit' >> ~/.bashrc"
    echo ""
    echo "To install ReconXploit:"
    echo "  git clone https://github.com/your-repo/ReconXploit.git $HOME/ReconXploit"
    echo "  cd $HOME/ReconXploit && ./setup.sh"
    exit 1
fi

print_success "Found ReconXploit at: $RECONXPLOIT_DIR"

# Change to ReconXploit directory
cd "$RECONXPLOIT_DIR"

# Check virtual environment
if [[ ! -f "$RECONXPLOIT_DIR/venv/bin/activate" ]]; then
    print_error "Python virtual environment not found!"
    print_warning "Expected: $RECONXPLOIT_DIR/venv/bin/activate"
    echo ""
    echo "To fix this, run:"
    echo "  cd $RECONXPLOIT_DIR"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"  
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source "$RECONXPLOIT_DIR/venv/bin/activate"

# Set up environment
export PATH="$PATH:$HOME/go/bin:$HOME/.cargo/bin"
export PYTHONPATH="$RECONXPLOIT_DIR:$PYTHONPATH"
export RECONXPLOIT_HOME="$RECONXPLOIT_DIR"

# Debug mode
if [[ "$1" == "--debug" ]]; then
    echo ""
    print_info "Debug Information:"
    echo "  ReconXploit Directory: $RECONXPLOIT_DIR"
    echo "  Virtual Environment: $VIRTUAL_ENV"
    echo "  Python Path: $PYTHONPATH"
    echo "  Current Directory: $(pwd)"
    echo "  Python Version: $(python3 --version 2>/dev/null || echo 'Not found')"
    echo ""
fi

# Launch ReconXploit
print_success "Launching ReconXploit v3.0..."
exec python3 "$RECONXPLOIT_DIR/core/reconxploit.py" "$@"

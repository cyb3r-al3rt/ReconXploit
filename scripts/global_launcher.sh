#!/bin/bash
# ReconXploit v3.0 - Fixed Global Launcher
# Product of Kernelpanic under infosbios.tech

set -e

# Detect ReconXploit installation directory
POSSIBLE_DIRS=(
    "$HOME/ReconXploit"
    "$HOME/reconxploit"
    "/opt/reconxploit"
    "/usr/local/share/reconxploit"
)

RECONXPLOIT_DIR=""
for dir in "${POSSIBLE_DIRS[@]}"; do
    if [[ -f "$dir/core/reconxploit.py" ]]; then
        RECONXPLOIT_DIR="$dir"
        break
    fi
done

# If not found, check current user's home for common locations
if [[ -z "$RECONXPLOIT_DIR" ]]; then
    for dir in "$HOME"/*/core/reconxploit.py; do
        if [[ -f "$dir" ]]; then
            RECONXPLOIT_DIR="$(dirname "$(dirname "$dir")")"
            break
        fi
    done
fi

# Final fallback - check if RECONXPLOIT_HOME is set
if [[ -z "$RECONXPLOIT_DIR" && -n "$RECONXPLOIT_HOME" && -f "$RECONXPLOIT_HOME/core/reconxploit.py" ]]; then
    RECONXPLOIT_DIR="$RECONXPLOIT_HOME"
fi

# Error if still not found
if [[ -z "$RECONXPLOIT_DIR" ]]; then
    echo "\033[0;31m[ERROR]\033[0m ReconXploit installation not found!"
    echo ""
    echo "\033[0;33m[FIX]\033[0m Please ensure ReconXploit is installed in one of:"
    echo "  $HOME/ReconXploit"
    echo "  /opt/reconxploit"
    echo ""
    echo "Or set RECONXPLOIT_HOME environment variable:"
    echo "  export RECONXPLOIT_HOME=/path/to/reconxploit"
    exit 1
fi

# Change to ReconXploit directory
cd "$RECONXPLOIT_DIR"

# Check virtual environment
if [[ ! -f "$RECONXPLOIT_DIR/venv/bin/activate" ]]; then
    echo "\033[0;31m[ERROR]\033[0m Python virtual environment not found!"
    echo "\033[0;33m[FIX]\033[0m Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source "$RECONXPLOIT_DIR/venv/bin/activate"

# Set environment variables
export PATH="$PATH:$HOME/go/bin"
export PYTHONPATH="$RECONXPLOIT_DIR:$PYTHONPATH"
export RECONXPLOIT_HOME="$RECONXPLOIT_DIR"

# Run ReconXploit
python3 "$RECONXPLOIT_DIR/core/reconxploit.py" "$@"

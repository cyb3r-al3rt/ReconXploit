#!/usr/bin/env python3
import os, sys, subprocess
from pathlib import Path

def main():
    print("ReconXploit Framework Setup")
    packages = ['asyncio', 'aiohttp', 'requests', 'dnspython', 'colorama']
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], capture_output=True)
        except:
            pass
    for directory in ['plugins', 'custom_plugins', 'config', 'results', 'logs']:
        Path(directory).mkdir(exist_ok=True)
    print("Setup completed!")

if __name__ == '__main__':
    main()

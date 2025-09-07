#!/usr/bin/env python3
import yaml
from pathlib import Path

class ConfigManager:
    def __init__(self):
        pass

    def load_config(self, path: str):
        p = Path(path)
        if not p.exists():
            return {}
        with open(p,'r') as f:
            return yaml.safe_load(f) or {}

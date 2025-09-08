"""
ReconXploit v3.0 Professional Edition - Core Package
Product of Kernelpanic under infosbios.tech
Author: cyb3r-ssrf (Muhammad Ismaeel Shareef S S)
"""

__version__ = "3.0.0"
__edition__ = "Professional Edition"
__author__ = "cyb3r-ssrf (Muhammad Ismaeel Shareef S S)"
__organization__ = "Kernelpanic"
__website__ = "infosbios.tech"

# Core module imports
try:
    from .banner_system import BannerSystem
    from .tool_manager import ToolManager
    from .workflow_engine import WorkflowEngine
    from .result_processor import ResultProcessor
    from .report_generator import ReportGenerator
    from .config_manager import ConfigManager
except ImportError as e:
    print(f"Warning: Failed to import core module: {e}")

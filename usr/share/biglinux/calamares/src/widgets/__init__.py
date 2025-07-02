# src/widgets/__init__.py

"""
Widgets package for BigLinux Calamares Configuration Tool
Custom GTK4 widgets and UI components
"""

import logging

# Import all widget classes
from .system_info import SystemInfoWidget
from .package_row import PackageRowWidget
from .option_card import OptionCard

# Package metadata
__version__ = "1.0.0"
__author__ = "BigLinux Team"

# Logger for the widgets package
logger = logging.getLogger(__name__)

# Expose main widget classes
__all__ = [
    "SystemInfoWidget",
    "PackageRowWidget",
    "OptionCard"
]


def initialize_widgets():
    """Initialize widgets package - call this at application startup"""
    logger.info("Widgets package initialized")


def cleanup_widgets():
    """Cleanup widgets package - call this at application shutdown"""
    logger.info("Widgets package cleaned up")

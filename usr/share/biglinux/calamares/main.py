#!/usr/bin/env python3
"""
BigLinux Calamares Configuration Tool
Main entry point for the GTK4 application
"""

import sys
import os
import logging
import gettext
import gi

# Ensure we're using the correct GTK version
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk
from src.app import CalamaresApp


def setup_logging():
    """Configure logging for the application"""
    handlers = [logging.StreamHandler(sys.stdout)]

    # Try to add file handler, but don't fail if can't create log file
    try:
        handlers.append(logging.FileHandler("/tmp/calamares-config.log", mode="a"))
    except PermissionError:
        print("Warning: Could not create log file, using console only")
    except Exception as e:
        print(f"Warning: Log file error: {e}")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


def setup_translations():
    """Setup gettext translations"""
    try:
        # Set up translations
        gettext.bindtextdomain("calamares-biglinux", "/usr/share/locale")
        gettext.textdomain("calamares-biglinux")
        gettext.install("calamares-biglinux")

        # Also bind for Gtk
        import locale

        locale.setlocale(locale.LC_ALL, "")

    except Exception as e:
        logging.warning(f"Failed to setup translations: {e}")
        # Fallback to English
        import builtins

        builtins.__dict__["_"] = lambda x: x


def check_dependencies():
    """Check if required system dependencies are available"""
    required_commands = ["pacman", "calamares"]
    missing = []

    for cmd in required_commands:
        if os.system(f"command -v {cmd} >/dev/null 2>&1") != 0:
            missing.append(cmd)

    if missing:
        logging.error(f"Missing required commands: {', '.join(missing)}")
        return False

    return True


def load_custom_css():
    """Load custom CSS for application-wide styling."""
    css_provider = Gtk.CssProvider()
    # The CSS rule to make the window background slightly transparent.
    # This creates a "frosted glass" effect on desktops that support it.
    css_data = b"""
    window.background {
        background-color: alpha(@theme_bg_color, 0.97);
    }
    """
    css_provider.load_from_data(css_data)

    display = Gdk.Display.get_default()
    if display:
        Gtk.StyleContext.add_provider_for_display(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


def main():
    """Main application entry point"""
    # Setup logging first
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting BigLinux Calamares Configuration Tool")

        # Setup translations
        setup_translations()

        # Check system dependencies
        if not check_dependencies():
            logger.error("System dependencies check failed")
            sys.exit(1)

        # Initialize Adwaita
        Adw.init()

        # Load custom application styling for effects like transparency.
        load_custom_css()

        # Create and run the application
        app = CalamaresApp()
        exit_code = app.run(sys.argv)

        logger.info(f"Application exited with code: {exit_code}")
        sys.exit(exit_code)

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

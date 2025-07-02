"""
Utilities package for BigLinux Calamares Configuration Tool
Provides common functionality used across the application
"""

# Import translation function
from .i18n import _, setup_i18n

# Import constants
from .constants import (
    APP_NAME,
    APP_ID,
    APP_VERSION,
    DATA_DIR,
    CALAMARES_CONFIG_DIR,
    CALAMARES_MODULES_DIR,
    ICON_MAPPING_FILE,
    MINIMAL_PACKAGES_FILE,
    BIGBASHVIEW_APPS_DIR,
    TEMP_FILES,
    COMMANDS,
    DEFAULTS,
    CALAMARES_CONFIGS,
    UI_SETTINGS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
)

# Import helper functions
from .helpers import (
    load_json_file,
    save_json_file,
    ensure_directory,
    file_exists,
    copy_file_safe,
    write_text_file,
    read_text_file,
    parse_package_list,
    format_package_list,
    human_readable_size,
    cleanup_temp_files,
    validate_package_name,
    truncate_text,
)

# Import shell execution utilities
from .shell import (
    CommandResult,
    ShellExecutor,
    execute_command,
    execute_command_async,
    check_command_exists,
    get_command_output,
    run_command_simple,
    cleanup_shell_resources,
    pacman_query_installed,
    check_package_installed,
    get_system_info,
    get_package_icon,
)

# Package metadata
__version__ = APP_VERSION
__author__ = "BigLinux Team"
__email__ = "contact@biglinux.com.br"

# Expose main utilities for easy importing
__all__ = [
    # Translation
    "_",
    "setup_i18n",
    # Constants (most commonly used)
    "APP_NAME",
    "APP_ID",
    "APP_VERSION",
    "DATA_DIR",
    "CALAMARES_CONFIG_DIR",
    "BIGBASHVIEW_APPS_DIR",
    "ICON_MAPPING_FILE",
    "MINIMAL_PACKAGES_FILE",
    "COMMANDS",
    "DEFAULTS",
    "ERROR_MESSAGES",
    "SUCCESS_MESSAGES",
    # Helper functions
    "load_json_file",
    "save_json_file",
    "ensure_directory",
    "file_exists",
    "copy_file_safe",
    "write_text_file",
    "read_text_file",
    "parse_package_list",
    "format_package_list",
    "human_readable_size",
    "cleanup_temp_files",
    "validate_package_name",
    "truncate_text",
    # Shell utilities
    "CommandResult",
    "ShellExecutor",
    "execute_command",
    "execute_command_async",
    "check_command_exists",
    "get_command_output",
    "run_command_simple",
    "cleanup_shell_resources",
    "pacman_query_installed",
    "check_package_installed",
    "get_system_info",
    "get_package_icon",
]


def initialize_utils():
    """Initialize utilities package - call this at application startup"""
    # Setup translations
    setup_i18n()

    # Ensure required directories exist
    ensure_directory(DATA_DIR)

    # Log initialization
    import logging

    logger = logging.getLogger(__name__)
    logger.info("Utils package initialized")


def cleanup_utils():
    """Cleanup utilities package - call this at application shutdown"""
    # Cleanup shell resources
    cleanup_shell_resources()

    # Cleanup any temporary files if needed
    temp_file_list = list(TEMP_FILES.values())
    cleanup_temp_files(temp_file_list)

    # Log cleanup
    import logging

    logger = logging.getLogger(__name__)
    logger.info("Utils package cleaned up")

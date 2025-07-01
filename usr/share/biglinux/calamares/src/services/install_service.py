"""
Install Service for BigLinux Calamares Configuration Tool
Handles Calamares configuration and installation process
"""

import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from ..utils import (
    _,
    execute_command,
    get_command_output,
    run_command_simple,
    copy_file_safe,
    write_text_file,
    read_text_file,
    ensure_directory,
    file_exists,
    CALAMARES_CONFIG_DIR,
    CALAMARES_MODULES_DIR,
    CALAMARES_CONFIGS,
    INSTALLATION_OPTIONS,
    BIGBASHVIEW_APPS_DIR,
    TEMP_FILES,
    COMMANDS
)


class InstallationConfig:
    """Configuration for Calamares installation"""
    
    def __init__(self):
        self.filesystem_type = "btrfs"
        self.packages_to_remove = []
        self.packages_to_install = []
        self.custom_desktop = False
        self.login_manager = ""
        self.use_minimal = False
        self.sfs_folder = ""
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            'filesystem_type': self.filesystem_type,
            'packages_to_remove': self.packages_to_remove,
            'packages_to_install': self.packages_to_install,
            'custom_desktop': self.custom_desktop,
            'login_manager': self.login_manager,
            'use_minimal': self.use_minimal,
            'sfs_folder': self.sfs_folder
        }


class InstallService:
    """Service for installation configuration and process management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._current_config = InstallationConfig()
        self._is_initialized = False
    
    def initialize(self):
        """Initialize the install service"""
        if self._is_initialized:
            return
        
        self.logger.info("Initializing InstallService")
        self._ensure_directories()
        self._is_initialized = True
        self.logger.info("InstallService initialized successfully")
    
    def cleanup(self):
        """Cleanup install service resources"""
        self.logger.info("Cleaning up InstallService")
        self._cleanup_temp_files()
        self._is_initialized = False
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        ensure_directory(CALAMARES_CONFIG_DIR)
        ensure_directory(CALAMARES_MODULES_DIR)
    
    def _cleanup_temp_files(self):
        """Clean up temporary installation files"""
        temp_files = [
            TEMP_FILES['wait_install'],
            TEMP_FILES['start_calamares']
        ]
        
        for temp_file in temp_files:
            try:
                if temp_file.exists():
                    temp_file.unlink()
            except Exception as e:
                self.logger.warning(f"Failed to cleanup temp file {temp_file}: {e}")
    
    def configure_installation(self, config: InstallationConfig) -> bool:
        """
        Configure Calamares for installation
        
        Args:
            config: Installation configuration
            
        Returns:
            True if configuration was successful
        """
        self.logger.info(f"Configuring installation with: {config.to_dict()}")
        self._current_config = config
        
        try:
            # Create wait file
            TEMP_FILES['wait_install'].touch()
            
            # Remove old start file
            if TEMP_FILES['start_calamares'].exists():
                TEMP_FILES['start_calamares'].unlink()
            
            # Configure partition settings
            if not self._configure_partition_settings():
                return False
            
            # Configure unpack settings
            if not self._configure_unpack_settings():
                return False
            
            # Configure package settings if needed
            if config.packages_to_remove or config.use_minimal:
                if not self._configure_package_settings():
                    return False
            
            # Configure main settings
            if not self._configure_main_settings():
                return False
            
            # Configure shell processes
            if not self._configure_shell_processes():
                return False
            
            # Create start file to signal configuration complete
            TEMP_FILES['start_calamares'].touch()
            
            self.logger.info("Installation configuration completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure installation: {e}")
            return False
    
    def _configure_partition_settings(self) -> bool:
        """Configure partition.conf for Calamares"""
        try:
            source_config = BIGBASHVIEW_APPS_DIR / "partition.conf"
            
            if not source_config.exists():
                self.logger.error(f"Partition config template not found: {source_config}")
                return False
            
            # Copy base configuration
            if not copy_file_safe(source_config, CALAMARES_CONFIGS['partition']):
                return False
            
            # Modify for ext4 if needed
            if self._current_config.filesystem_type == "ext4":
                config_content = read_text_file(CALAMARES_CONFIGS['partition'])
                if config_content:
                    # Replace default filesystem type
                    modified_content = config_content.replace(
                        'defaultFileSystemType:  "btrfs"',
                        'defaultFileSystemType:  "ext4"'
                    )
                    write_text_file(modified_content, CALAMARES_CONFIGS['partition'])
            
            self.logger.debug("Partition configuration completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure partition settings: {e}")
            return False
    
    def _configure_unpack_settings(self) -> bool:
        """Configure unpackfs.conf for Calamares"""
        try:
            # Get SFS folder from system service
            from . import get_system_service
            system_service = get_system_service()
            sfs_folder = system_service.get_sfs_folder()
            
            if not sfs_folder:
                self.logger.error("SFS folder not detected")
                return False
            
            self._current_config.sfs_folder = sfs_folder
            
            # Create unpack configuration
            config_content = f"""---
unpack:
    - source: "/run/miso/bootmnt/{sfs_folder}/x86_64/rootfs.sfs"
      sourcefs: "squashfs"
      destination: ""
"""
            
            # Add desktop SFS if not using custom desktop
            if not self._current_config.custom_desktop:
                config_content += f"""    - source: "/run/miso/bootmnt/{sfs_folder}/x86_64/desktopfs.sfs"
      sourcefs: "squashfs"
      destination: ""
"""
            
            write_text_file(config_content, CALAMARES_CONFIGS['unpackfs'])
            self.logger.debug("Unpack configuration completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure unpack settings: {e}")
            return False
    
    def _configure_package_settings(self) -> bool:
        """Configure packages.conf for Calamares"""
        try:
            packages_to_remove = self._current_config.packages_to_remove
            packages_to_install = self._current_config.packages_to_install
            
            if not packages_to_remove and not packages_to_install:
                return True
            
            # Base configuration
            config_content = """---

backend: pacman

skip_if_no_internet: false
update_db: true
update_system: true

pacman:
    num_retries: 10
    disable_download_timeout: true
    needed_only: true

operations:
"""
            
            # Add remove operations
            if packages_to_remove:
                config_content += "    - remove:\n"
                for package in packages_to_remove:
                    config_content += f"        - {package}\n"
            
            # Add install operations
            if packages_to_install:
                config_content += "    - install:\n"
                for package in packages_to_install:
                    config_content += f"        - {package}\n"
            
            write_text_file(config_content, CALAMARES_CONFIGS['packages'])
            self.logger.debug("Package configuration completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure package settings: {e}")
            return False
    
    def _configure_main_settings(self) -> bool:
        """Configure main settings.conf for Calamares"""
        try:
            config_content = """---
modules-search: [ local ]

instances:

- id:       initialize_pacman
  module:   shellprocess
  config:   shellprocess_initialize_pacman.conf

- id:       displaymanager_biglinux
  module:   shellprocess
  config:   shellprocess_displaymanager_biglinux.conf

sequence:
    - show:
        - welcome
        - locale
        - keyboard
        - partition
        - users
        - summary
    - exec:
        - partition
        - mount
        - unpackfs
        - networkcfg
        - machineid
        - fstab
        - locale
        - keyboard
"""
            
            # Add package operations if needed
            if (self._current_config.packages_to_remove or 
                self._current_config.packages_to_install or 
                self._current_config.use_minimal):
                config_content += """        - shellprocess@initialize_pacman
        - packages
"""
            
            # Add display manager configuration if custom desktop
            if self._current_config.custom_desktop and self._current_config.login_manager:
                config_content += "        - shellprocess@displaymanager_biglinux\n"
            
            # Add remaining steps
            config_content += """        - localecfg
        - luksopenswaphookcfg
        - luksbootkeyfile
        - initcpiocfg
        - initcpio
        - users
        - displaymanager
        - mhwdcfg
        - hwclock
        - services
        - grubcfg
        - grubcfg-fix
        - bootloader
        - postcfg
        - btrfs-fix
        - umount
    - show:
        - finished

branding: biglinux

prompt-install: true

dont-chroot: false
oem-setup: false
disable-cancel: false
disable-cancel-during-exec: false
quit-at-end: false
"""
            
            write_text_file(config_content, CALAMARES_CONFIGS['settings'])
            self.logger.debug("Main settings configuration completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure main settings: {e}")
            return False
    
    def _configure_shell_processes(self) -> bool:
        """Configure shell process modules"""
        try:
            # Configure pacman initialization
            pacman_config = """---

dontChroot: false

script:
    - "pacman-key --init"
    - command: "pacman-key --populate archlinux manjaro biglinux"
      timeout: 1200

i18n:
    name: "Init pacman-key"
"""
            write_text_file(pacman_config, CALAMARES_CONFIGS['shellprocess_pacman'])
            
            # Configure display manager if needed
            if self._current_config.login_manager:
                display_config = f"""---

dontChroot: false

script:
    - "systemctl enable {self._current_config.login_manager}"

i18n:
    name: "Enable login manager"
"""
                write_text_file(display_config, CALAMARES_CONFIGS['shellprocess_display'])
            
            self.logger.debug("Shell process configuration completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to configure shell processes: {e}")
            return False
    
    def start_installation(self, filesystem_type: str = "btrfs", 
                          packages_to_remove: List[str] = None) -> bool:
        """
        Start the installation process
        
        Args:
            filesystem_type: Type of filesystem (btrfs or ext4)
            packages_to_remove: List of packages to remove
            
        Returns:
            True if installation started successfully
        """
        try:
            # Prepare configuration
            config = InstallationConfig()
            config.filesystem_type = filesystem_type
            config.packages_to_remove = packages_to_remove or []
            config.use_minimal = bool(packages_to_remove)
            
            # Configure Calamares
            if not self.configure_installation(config):
                return False
            
            # Start Calamares
            self.logger.info("Starting Calamares installation")
            result = execute_command(COMMANDS['calamares'], timeout=None)
            
            if not result.success:
                self.logger.error(f"Failed to start Calamares: {result.stderr}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start installation: {e}")
            return False
    
    def start_maintenance_tool(self, tool_name: str) -> bool:
        """
        Start a maintenance tool
        
        Args:
            tool_name: Name of the maintenance tool
            
        Returns:
            True if tool started successfully
        """
        tools = {
            'grub_restore': COMMANDS['grub_restore'],
            'timeshift': COMMANDS['timeshift'],
            'efi_manager': COMMANDS['efi_manager']
        }
        
        if tool_name not in tools:
            self.logger.error(f"Unknown maintenance tool: {tool_name}")
            return False
        
        try:
            command = tools[tool_name]
            self.logger.info(f"Starting maintenance tool: {tool_name}")
            
            result = execute_command(command, timeout=None)
            return result.success
            
        except Exception as e:
            self.logger.error(f"Failed to start maintenance tool {tool_name}: {e}")
            return False
    
    def get_installation_status(self) -> Dict[str, Any]:
        """
        Get current installation status
        
        Returns:
            Dictionary with installation status information
        """
        status = {
            'configured': TEMP_FILES['start_calamares'].exists(),
            'in_progress': TEMP_FILES['wait_install'].exists(),
            'config': self._current_config.to_dict()
        }
        
        return status
    
    def check_installation_requirements(self) -> Dict[str, bool]:
        """
        Check installation requirements
        
        Returns:
            Dictionary with requirement check results
        """
        requirements = {}
        
        # Check Calamares availability
        requirements['calamares'] = run_command_simple("command -v calamares")
        
        # Check required directories
        requirements['config_dir'] = CALAMARES_CONFIG_DIR.exists()
        requirements['modules_dir'] = CALAMARES_MODULES_DIR.exists()
        
        # Check partition config template
        requirements['partition_template'] = (BIGBASHVIEW_APPS_DIR / "partition.conf").exists()
        
        # Check system requirements
        from . import get_system_service
        system_service = get_system_service()
        requirements['sfs_detected'] = system_service.get_sfs_folder() is not None
        requirements['live_mode'] = system_service.is_live_mode()
        
        return requirements
    
    def get_current_config(self) -> InstallationConfig:
        """Get current installation configuration"""
        return self._current_config
    
    def reset_configuration(self):
        """Reset installation configuration to defaults"""
        self.logger.info("Resetting installation configuration")
        self._current_config = InstallationConfig()
        self._cleanup_temp_files()
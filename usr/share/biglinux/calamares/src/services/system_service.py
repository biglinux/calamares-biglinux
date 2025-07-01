"""
System Service for BigLinux Calamares Configuration Tool
Handles system detection and information gathering
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional, List
from ..utils import (
    _,
    execute_command,
    get_command_output,
    check_command_exists,
    COMMANDS
)


class SystemService:
    """Service for system information detection and management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._system_info = {}
        self._is_initialized = False
    
    def initialize(self):
        """Initialize the system service"""
        if self._is_initialized:
            return
        
        self.logger.info("Initializing SystemService")
        self._detect_system_info()
        self._is_initialized = True
        self.logger.info("SystemService initialized successfully")
    
    def cleanup(self):
        """Cleanup system service resources"""
        self.logger.info("Cleaning up SystemService")
        self._system_info.clear()
        self._is_initialized = False
    
    def _detect_system_info(self):
        """Detect and cache system information"""
        self.logger.debug("Detecting system information")
        
        self._system_info = {
            'boot_mode': self._detect_boot_mode(),
            'kernel_version': self._detect_kernel_version(),
            'session_type': self._detect_session_type(),
            'architecture': self._detect_architecture(),
            'hostname': self._detect_hostname(),
            'live_mode': self._detect_live_mode(),
            'efi_available': self._is_efi_system(),
            'sfs_folder': self._detect_sfs_folder()
        }
        
        self.logger.info(f"System detected: {self._system_info}")
    
    def _detect_boot_mode(self) -> str:
        """Detect boot mode (UEFI or BIOS)"""
        try:
            efi_path = Path("/sys/firmware/efi")
            if efi_path.exists() and efi_path.is_dir():
                return "UEFI"
            return "BIOS (Legacy)"
        except Exception as e:
            self.logger.warning(f"Failed to detect boot mode: {e}")
            return "Unknown"
    
    def _detect_kernel_version(self) -> str:
        """Detect kernel version"""
        try:
            # Execute: uname -r | cut -f1 -d-
            full_version = get_command_output("uname -r")
            if full_version:
                # Extract version before first dash
                kernel_version = full_version.split('-')[0]
                return kernel_version
            return "Unknown"
        except Exception as e:
            self.logger.warning(f"Failed to detect kernel version: {e}")
            return "Unknown"
    
    def _detect_session_type(self) -> str:
        """Detect graphical session type"""
        try:
            session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
            if session_type == 'wayland':
                return "Wayland"
            elif session_type == 'x11':
                return "X11"
            elif session_type:
                return session_type.title()
            return "Unknown"
        except Exception as e:
            self.logger.warning(f"Failed to detect session type: {e}")
            return "Unknown"
    
    def _detect_architecture(self) -> str:
        """Detect system architecture"""
        try:
            arch = get_command_output("uname -m")
            return arch if arch else "Unknown"
        except Exception as e:
            self.logger.warning(f"Failed to detect architecture: {e}")
            return "Unknown"
    
    def _detect_hostname(self) -> str:
        """Detect system hostname"""
        try:
            hostname = os.environ.get('HOSTNAME')
            if not hostname:
                hostname = get_command_output("hostname")
            return hostname if hostname else "Unknown"
        except Exception as e:
            self.logger.warning(f"Failed to detect hostname: {e}")
            return "Unknown"
    
    def _detect_live_mode(self) -> bool:
        """Detect if system is running in live mode"""
        try:
            # Check for live environment indicators
            live_indicators = [
                Path("/run/miso"),
                Path("/live"),
                Path("/lib/live"),
                Path("/run/live")
            ]
            
            for indicator in live_indicators:
                if indicator.exists():
                    return True
            
            return False
        except Exception as e:
            self.logger.warning(f"Failed to detect live mode: {e}")
            return False
    
    def _is_efi_system(self) -> bool:
        """Check if EFI system is available"""
        return self._system_info.get('boot_mode') == 'UEFI'
    
    def _detect_sfs_folder(self) -> Optional[str]:
        """Detect SFS folder for live system"""
        try:
            boot_mount = Path("/run/miso/bootmnt")
            if not boot_mount.exists():
                return None
            
            # Try manjaro folder first
            manjaro_path = boot_mount / "manjaro" / "x86_64"
            if manjaro_path.exists():
                return "manjaro"
            
            # Try hostname folder
            hostname = self.get_hostname()
            if hostname and hostname != "Unknown":
                hostname_path = boot_mount / hostname / "x86_64"
                if hostname_path.exists():
                    return hostname
            
            # Try to find any folder excluding efi and boot
            try:
                for item in boot_mount.iterdir():
                    if (item.is_dir() and 
                        item.name not in ['efi', 'boot'] and
                        (item / "x86_64").exists()):
                        return item.name
            except Exception:
                pass
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to detect SFS folder: {e}")
            return None
    
    def get_boot_mode(self) -> str:
        """Get boot mode (UEFI or BIOS)"""
        return self._system_info.get('boot_mode', 'Unknown')
    
    def get_kernel_version(self) -> str:
        """Get kernel version"""
        return self._system_info.get('kernel_version', 'Unknown')
    
    def get_session_type(self) -> str:
        """Get session type (Wayland/X11)"""
        return self._system_info.get('session_type', 'Unknown')
    
    def get_architecture(self) -> str:
        """Get system architecture"""
        return self._system_info.get('architecture', 'Unknown')
    
    def get_hostname(self) -> str:
        """Get system hostname"""
        return self._system_info.get('hostname', 'Unknown')
    
    def is_live_mode(self) -> bool:
        """Check if running in live mode"""
        return self._system_info.get('live_mode', False)
    
    def is_efi_system(self) -> bool:
        """Check if EFI system"""
        return self._system_info.get('efi_available', False)
    
    def get_sfs_folder(self) -> Optional[str]:
        """Get SFS folder name for live system"""
        return self._system_info.get('sfs_folder')
    
    def get_system_summary(self) -> str:
        """Get formatted system summary"""
        boot_mode = self.get_boot_mode()
        kernel = self.get_kernel_version()
        session = self.get_session_type()
        
        return f"{_('The system is in')} {boot_mode}, Linux {kernel} {_('and graphical mode')} {session}."
    
    def get_all_info(self) -> Dict[str, any]:
        """Get all system information"""
        return self._system_info.copy()
    
    def refresh_system_info(self):
        """Force refresh of system information"""
        self.logger.info("Refreshing system information")
        self._detect_system_info()
    
    def check_required_commands(self) -> Dict[str, bool]:
        """Check availability of required system commands"""
        required_commands = ['pacman', 'calamares', 'geticons']
        availability = {}
        
        for cmd in required_commands:
            availability[cmd] = check_command_exists(cmd)
            if not availability[cmd]:
                self.logger.warning(f"Required command not found: {cmd}")
        
        return availability
    
    def get_efi_entries_command(self) -> Optional[str]:
        """Get command to manage EFI entries if available"""
        if not self.is_efi_system():
            return None
        
        if check_command_exists("efibootmgr"):
            return "efibootmgr"
        elif check_command_exists("QEFIEntryManager"):
            return "sudo QEFIEntryManager"
        
        return None
    
    def can_manage_efi_entries(self) -> bool:
        """Check if EFI entries can be managed"""
        return self.is_efi_system() and self.get_efi_entries_command() is not None
    
    def get_live_system_paths(self) -> Dict[str, Path]:
        """Get important paths for live system"""
        paths = {}
        
        boot_mount = Path("/run/miso/bootmnt")
        sfs_folder = self.get_sfs_folder()
        
        if boot_mount.exists() and sfs_folder:
            base_path = boot_mount / sfs_folder / "x86_64"
            paths.update({
                'boot_mount': boot_mount,
                'sfs_folder_path': boot_mount / sfs_folder,
                'rootfs_sfs': base_path / "rootfs.sfs",
                'desktopfs_sfs': base_path / "desktopfs.sfs"
            })
        
        return paths
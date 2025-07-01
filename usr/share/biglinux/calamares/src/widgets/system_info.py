"""
System Info Widget for BigLinux Calamares Configuration Tool
Displays system information and EFI manager button
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GLib
from ..utils.i18n import _
from ..services import get_system_service, get_install_service


class SystemInfoWidget(Gtk.Box):
    """Widget that displays system information and EFI management"""
    
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        self.logger = logging.getLogger(__name__)
        self.system_service = get_system_service()
        self.install_service = get_install_service()
        
        # Add CSS classes for styling
        self.add_css_class("system-info-widget")
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(18)
        self.set_margin_end(18)
        
        # Create main info card
        self.create_info_card()
        
        # Create EFI manager section (conditional)
        self.create_efi_section()
        
        # Create forum link
        self.create_forum_link()
        
        self.logger.debug("SystemInfoWidget initialized")
    
    def create_info_card(self):
        """Create the main system information card"""
        # Create card container
        info_card = Adw.Bin()
        info_card.add_css_class("card")
        info_card.add_css_class("system-info-card")
        
        # Create content box
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER
        )
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        content_box.set_margin_start(18)
        content_box.set_margin_end(18)
        
        # Get system information
        boot_mode = self.system_service.get_boot_mode()
        kernel_version = self.system_service.get_kernel_version()
        session_type = self.system_service.get_session_type()
        
        # Create info labels
        info_parts = [
            (_("The system is in"), ""),
            (boot_mode, "bold-text"),
            (_(", Linux"), ""),
            (kernel_version, "bold-text"),
            (_("and graphical mode"), ""),
            (f"{session_type}.", "bold-text")
        ]
        
        for text, css_class in info_parts:
            label = Gtk.Label(label=text)
            if css_class:
                label.add_css_class(css_class)
            content_box.append(label)
        
        info_card.set_child(content_box)
        self.append(info_card)
    
    def create_efi_section(self):
        """Create EFI manager section (only for EFI systems)"""
        if not self.system_service.can_manage_efi_entries():
            return
        
        # Create EFI section card
        efi_card = Adw.Bin()
        efi_card.add_css_class("card")
        efi_card.add_css_class("efi-section")
        efi_card.set_margin_top(6)
        
        # Create content box
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER
        )
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        content_box.set_margin_start(18)
        content_box.set_margin_end(18)
        
        # Create description label
        description_label = Gtk.Label(
            label=_("Manage EFI entries on the motherboard (NVRAM):")
        )
        description_label.set_halign(Gtk.Align.CENTER)
        content_box.append(description_label)
        
        # Create EFI manager button
        efi_button = Gtk.Button(
            label=_("EFI Entry Manager"),
            halign=Gtk.Align.CENTER
        )
        efi_button.add_css_class("suggested-action")
        efi_button.connect("clicked", self.on_efi_button_clicked)
        content_box.append(efi_button)
        
        efi_card.set_child(content_box)
        self.append(efi_card)
    
    def create_forum_link(self):
        """Create forum support link"""
        # Create forum section card
        forum_card = Adw.Bin()
        forum_card.add_css_class("card")
        forum_card.add_css_class("forum-section")
        forum_card.set_margin_top(6)
        
        # Create content box
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER
        )
        content_box.set_margin_top(18)
        content_box.set_margin_bottom(18)
        content_box.set_margin_start(18)
        content_box.set_margin_end(18)
        
        # Create forum link button
        forum_link = Gtk.LinkButton(
            uri="https://forum.biglinux.com.br",
            label=_("This is a collaborative system, if you need help consult our forum: https://forum.biglinux.com.br.")
        )
        forum_link.set_halign(Gtk.Align.CENTER)
        forum_link.add_css_class("forum-link")
        
        content_box.append(forum_link)
        forum_card.set_child(content_box)
        self.append(forum_card)
    
    def on_efi_button_clicked(self, button):
        """Handle EFI manager button click"""
        self.logger.info("EFI Entry Manager button clicked")
        
        try:
            # Show loading state
            button.set_sensitive(False)
            button.set_label(_("Starting..."))
            
            # Start EFI manager tool
            def on_tool_finished():
                # Reset button state
                GLib.idle_add(lambda: self.reset_efi_button(button))
            
            # Start tool in background
            success = self.install_service.start_maintenance_tool('efi_manager')
            
            if success:
                self.show_success_message(_("EFI Entry Manager started successfully"))
            else:
                self.show_error_message(_("Failed to start EFI Entry Manager"))
                
            # Reset button after short delay
            GLib.timeout_add_seconds(2, lambda: self.reset_efi_button(button))
            
        except Exception as e:
            self.logger.error(f"Failed to start EFI manager: {e}")
            self.show_error_message(_("Error starting EFI Entry Manager"))
            self.reset_efi_button(button)
    
    def reset_efi_button(self, button):
        """Reset EFI button to normal state"""
        button.set_sensitive(True)
        button.set_label(_("EFI Entry Manager"))
        return False  # Don't repeat timeout
    
    def refresh_system_info(self):
        """Refresh system information display"""
        self.logger.debug("Refreshing system information")
        
        # Refresh system service data
        self.system_service.refresh_system_info()
        
        # Rebuild the widget content
        # Clear current children
        child = self.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.remove(child)
            child = next_child
        
        # Recreate content
        self.create_info_card()
        self.create_efi_section()
        self.create_forum_link()
    
    def show_success_message(self, message):
        """Show success message via toast"""
        # Get the main window to show toast
        toplevel = self.get_root()
        if hasattr(toplevel, 'show_success_toast'):
            toplevel.show_success_toast(message)
    
    def show_error_message(self, message):
        """Show error message via toast"""
        # Get the main window to show toast
        toplevel = self.get_root()
        if hasattr(toplevel, 'show_error_toast'):
            toplevel.show_error_toast(message)
    
    def get_system_summary(self) -> str:
        """Get formatted system summary"""
        return self.system_service.get_system_summary()
    
    def set_compact_mode(self, compact: bool):
        """Set compact display mode"""
        if compact:
            self.add_css_class("compact-mode")
        else:
            self.remove_css_class("compact-mode")
    
    def update_system_info(self, info: dict):
        """Update system info with new data"""
        self.logger.debug(f"Updating system info: {info}")
        # This could be used to update specific info without full refresh
        # Implementation depends on specific needs
        pass
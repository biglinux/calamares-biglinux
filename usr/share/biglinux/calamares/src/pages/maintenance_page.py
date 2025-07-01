"""
Maintenance Page for BigLinux Calamares Configuration Tool
System maintenance and restore tools page
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject, GLib
from ..utils.i18n import _
from ..services import get_system_service, get_install_service


class MaintenancePage(Gtk.Box):
    """Page with system maintenance and restore options"""
    
    # Define signals for navigation
    __gsignals__ = {
        'navigate': (GObject.SignalFlags.RUN_FIRST, None, (str, object))
    }
    
    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
        )
        
        self.logger = logging.getLogger(__name__)
        self.system_service = get_system_service()
        self.install_service = get_install_service()
        
        # Add CSS class for styling
        self.add_css_class("maintenance-page")
        
        # Set margins
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)
        
        # Create content
        self.create_content()
        
        self.logger.debug("MaintenancePage initialized")
    
    def create_content(self):
        """Create the maintenance page content"""
        # Create main container with centering
        main_container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            hexpand=True,
            vexpand=True
        )
        
        # Create page title
        self.create_page_title(main_container)
        
        # Create maintenance options
        self.create_maintenance_options(main_container)
        
        # Create back button
        self.create_back_button(main_container)
        
        self.append(main_container)
    
    def create_page_title(self, parent):
        """Create page title"""
        title_label = Gtk.Label(label=_("System Maintenance"))
        title_label.add_css_class("title-1")
        title_label.set_halign(Gtk.Align.CENTER)
        title_label.set_margin_bottom(12)
        parent.append(title_label)
    
    def create_maintenance_options(self, parent):
        """Create maintenance options grid"""
        # Create grid container
        grid_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=24,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            homogeneous=True
        )
        
        # Create restore system card
        self.create_restore_card(grid_box)
        
        # Create snapshot backup card
        self.create_snapshot_card(grid_box)
        
        parent.append(grid_box)
    
    def create_restore_card(self, parent):
        """Create system restore card"""
        card = self.create_maintenance_card(
            icon_name="document-revert",
            title=_("Restore system settings"),
            description=_("Utility that facilitates the restoration of the installed system, especially the restoration of the system boot (Grub)."),
            description2=_("It can also be used to access the package manager and terminal of the installed system."),
            button_text=_("Start"),
            button_style="suggested-action",
            action_callback=self.on_restore_clicked
        )
        parent.append(card)
    
    def create_snapshot_card(self, parent):
        """Create snapshot backup card"""
        card = self.create_maintenance_card(
            icon_name="document-save-as",
            title=_("Snapshot and backups"),
            description=_("Restore restore points of the installed system."),
            button_text=_("Start"),
            button_style="secondary",
            action_callback=self.on_snapshot_clicked
        )
        parent.append(card)
    
    def create_maintenance_card(self, icon_name, title, description, button_text, 
                               button_style, action_callback, description2=None):
        """
        Create a maintenance option card
        
        Args:
            icon_name: Icon name for the card
            title: Card title
            description: Card description
            button_text: Button text
            button_style: Button CSS style class
            action_callback: Callback for button click
            description2: Optional second description line
            
        Returns:
            Adw.Bin containing the card
        """
        # Create card container
        card = Adw.Bin()
        card.add_css_class("card")
        card.add_css_class("maintenance-card")
        card.set_size_request(320, 280)
        
        # Create card content
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=16,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER
        )
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        
        # Create icon
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(64)
        icon.add_css_class("maintenance-icon")
        content_box.append(icon)
        
        # Create title
        title_label = Gtk.Label(label=title)
        title_label.add_css_class("title-3")
        title_label.add_css_class("maintenance-title")
        title_label.set_halign(Gtk.Align.CENTER)
        title_label.set_wrap(True)
        title_label.set_max_width_chars(30)
        content_box.append(title_label)
        
        # Create description
        desc_label = Gtk.Label(
            label=description,
            wrap=True,
            justify=Gtk.Justification.CENTER,
            halign=Gtk.Align.CENTER
        )
        desc_label.add_css_class("body")
        desc_label.add_css_class("maintenance-description")
        desc_label.set_max_width_chars(40)
        content_box.append(desc_label)
        
        # Add second description if provided
        if description2:
            desc2_label = Gtk.Label(
                label=description2,
                wrap=True,
                justify=Gtk.Justification.CENTER,
                halign=Gtk.Align.CENTER
            )
            desc2_label.add_css_class("body")
            desc2_label.add_css_class("maintenance-description")
            desc2_label.add_css_class("dim-label")
            desc2_label.set_max_width_chars(40)
            content_box.append(desc2_label)
        
        # Add spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        content_box.append(spacer)
        
        # Create action button
        button = Gtk.Button(label=button_text)
        button.add_css_class(button_style)
        button.add_css_class("pill")
        button.set_halign(Gtk.Align.CENTER)
        button.connect("clicked", action_callback)
        content_box.append(button)
        
        card.set_child(content_box)
        return card
    
    def create_back_button(self, parent):
        """Create back navigation button"""
        back_button = Gtk.Button(label=_("Back"))
        back_button.add_css_class("outlined")
        back_button.set_halign(Gtk.Align.CENTER)
        back_button.set_margin_top(24)
        back_button.connect("clicked", self.on_back_clicked)
        parent.append(back_button)
    
    def on_restore_clicked(self, button):
        """Handle system restore button click"""
        self.logger.info("System restore tool requested")
        
        try:
            # Show loading state
            button.set_sensitive(False)
            button.set_label(_("Starting..."))
            
            # Start restore tool
            success = self.install_service.start_maintenance_tool('grub_restore')
            
            if success:
                self.show_success_message(_("System restore tool started successfully"))
            else:
                self.show_error_message(_("Failed to start system restore tool"))
            
            # Reset button state after delay
            GLib.timeout_add_seconds(2, lambda: self.reset_button_state(button, _("Start")))
            
        except Exception as e:
            self.logger.error(f"Failed to start restore tool: {e}")
            self.show_error_message(_("Error starting system restore tool"))
            self.reset_button_state(button, _("Start"))
    
    def on_snapshot_clicked(self, button):
        """Handle snapshot backup button click"""
        self.logger.info("Snapshot backup tool requested")
        
        try:
            # Show loading state
            button.set_sensitive(False)
            button.set_label(_("Starting..."))
            
            # Start timeshift tool
            success = self.install_service.start_maintenance_tool('timeshift')
            
            if success:
                self.show_success_message(_("Snapshot backup tool started successfully"))
            else:
                self.show_error_message(_("Failed to start snapshot backup tool"))
            
            # Reset button state after delay
            GLib.timeout_add_seconds(2, lambda: self.reset_button_state(button, _("Start")))
            
        except Exception as e:
            self.logger.error(f"Failed to start timeshift: {e}")
            self.show_error_message(_("Error starting snapshot backup tool"))
            self.reset_button_state(button, _("Start"))
    
    def on_back_clicked(self, button):
        """Handle back button click"""
        self.logger.info("Back to main page requested")
        self.emit('navigate', 'back', None)
    
    def reset_button_state(self, button, original_text):
        """Reset button to original state"""
        button.set_sensitive(True)
        button.set_label(original_text)
        return False  # Don't repeat timeout
    
    def show_success_message(self, message):
        """Show success message via toast"""
        toplevel = self.get_root()
        if hasattr(toplevel, 'show_success_toast'):
            toplevel.show_success_toast(message)
    
    def show_error_message(self, message):
        """Show error message via toast"""
        toplevel = self.get_root()
        if hasattr(toplevel, 'show_error_toast'):
            toplevel.show_error_toast(message)
    
    def on_page_activated(self):
        """Called when page becomes active"""
        self.logger.debug("MaintenancePage activated")
        
        # Check if maintenance tools are available
        self.check_tool_availability()
    
    def check_tool_availability(self):
        """Check availability of maintenance tools"""
        try:
            # Check if required tools are available
            requirements = self.install_service.check_installation_requirements()
            
            # Log warnings for missing tools
            if not requirements.get('grub_restore_available', True):
                self.logger.warning("Grub restore tool not available")
            
            if not requirements.get('timeshift_available', True):
                self.logger.warning("Timeshift tool not available")
                
        except Exception as e:
            self.logger.error(f"Failed to check tool availability: {e}")
    
    def cleanup(self):
        """Cleanup page resources"""
        self.logger.debug("MaintenancePage cleanup")
        # No specific cleanup needed for maintenance page
        pass


# Register the signal
GObject.type_register(MaintenancePage)
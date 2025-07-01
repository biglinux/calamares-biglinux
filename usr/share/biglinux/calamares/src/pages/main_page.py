"""
Main Page for BigLinux Calamares Configuration Tool
Initial page with three main options: Maintenance, Installation, and Minimal
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject
from ..utils.i18n import _
from ..services import get_system_service, get_install_service


class MainPage(Gtk.Box):
    """Main page with three installation/maintenance options"""
    
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
        self.add_css_class("main-page")
        
        # Set margins
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)
        
        # Create content
        self.create_content()
        
        self.logger.debug("MainPage initialized")
    
    def create_content(self):
        """Create the main page content"""
        # Create main container with centering
        main_container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            hexpand=True,
            vexpand=True
        )
        
        # Create cards grid
        self.create_options_grid(main_container)
        
        self.append(main_container)
    
    def create_options_grid(self, parent):
        """Create the grid with the three main options"""
        # Create grid container
        grid_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=24,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            homogeneous=True
        )
        
        # Create the three option cards
        self.create_maintenance_card(grid_box)
        self.create_installation_card(grid_box)
        self.create_minimal_card(grid_box)
        
        parent.append(grid_box)
    
    def create_maintenance_card(self, parent):
        """Create maintenance option card"""
        card = self.create_option_card(
            icon_name="applications-utilities",
            title=_("Maintenance"),
            description=_("Tools that facilitate the maintenance of the installed system."),
            button_text=_("Restore"),
            button_style="secondary",
            action_callback=self.on_maintenance_clicked
        )
        parent.append(card)
    
    def create_installation_card(self, parent):
        """Create installation option card"""
        card = self.create_option_card(
            icon_name="system-software-install",
            title=_("Installation"),
            description=_("The system is in live mode, which has limitations."),
            description2=_("Install it for a complete experience."),
            button_text=_("Install"),
            button_style="suggested-action",
            action_callback=self.on_installation_clicked
        )
        parent.append(card)
    
    def create_minimal_card(self, parent):
        """Create minimal installation option card"""
        card = self.create_option_card(
            icon_name="preferences-system",
            title=_("Minimal"),
            description=_("Choose which programs to install, ensuring a highly customized experience."),
            button_text=_("Continue"),
            button_style="secondary",
            action_callback=self.on_minimal_clicked
        )
        parent.append(card)
    
    def create_option_card(self, icon_name, title, description, button_text, 
                          button_style, action_callback, description2=None):
        """
        Create a generic option card
        
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
        card.add_css_class("option-card")
        card.set_size_request(280, 320)
        
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
        icon.add_css_class("option-icon")
        content_box.append(icon)
        
        # Create title
        title_label = Gtk.Label(label=title)
        title_label.add_css_class("title-2")
        title_label.add_css_class("option-title")
        title_label.set_halign(Gtk.Align.CENTER)
        content_box.append(title_label)
        
        # Create description
        desc_label = Gtk.Label(
            label=description,
            wrap=True,
            justify=Gtk.Justification.CENTER,
            halign=Gtk.Align.CENTER
        )
        desc_label.add_css_class("body")
        desc_label.add_css_class("option-description")
        desc_label.set_max_width_chars(35)
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
            desc2_label.add_css_class("option-description")
            desc2_label.add_css_class("dim-label")
            desc2_label.set_max_width_chars(35)
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
    
    def on_maintenance_clicked(self, button):
        """Handle maintenance option click"""
        self.logger.info("Maintenance option selected")
        self.emit('navigate', 'maintenance', None)
    
    def on_installation_clicked(self, button):
        """Handle installation option click"""
        self.logger.info("Installation option selected")
        
        # Start installation with BTRFS
        try:
            # Show loading state
            button.set_sensitive(False)
            button.set_label(_("Starting..."))
            
            # Check installation requirements
            requirements = self.install_service.check_installation_requirements()
            missing_requirements = [k for k, v in requirements.items() if not v]
            
            if missing_requirements:
                self.show_error_message(
                    _("Installation requirements not met: {}").format(
                        ", ".join(missing_requirements)
                    )
                )
                self.reset_button_state(button, _("Install"))
                return
            
            # Start installation process
            success = self.install_service.start_installation("btrfs")
            
            if success:
                self.show_success_message(_("Installation started successfully"))
                # Navigate to tips page
                self.emit('navigate', 'tips', None)
            else:
                self.show_error_message(_("Failed to start installation"))
                
            self.reset_button_state(button, _("Install"))
            
        except Exception as e:
            self.logger.error(f"Installation start failed: {e}")
            self.show_error_message(_("Error starting installation"))
            self.reset_button_state(button, _("Install"))
    
    def on_minimal_clicked(self, button):
        """Handle minimal installation option click"""
        self.logger.info("Minimal installation option selected")
        self.emit('navigate', 'minimal', None)
    
    def reset_button_state(self, button, original_text):
        """Reset button to original state"""
        button.set_sensitive(True)
        button.set_label(original_text)
    
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
        self.logger.debug("MainPage activated")
        
        # Refresh system information if needed
        # This could trigger updates in system info widget
        pass
    
    def cleanup(self):
        """Cleanup page resources"""
        self.logger.debug("MainPage cleanup")
        # No specific cleanup needed for main page
        pass


# Register the signal
GObject.type_register(MainPage)
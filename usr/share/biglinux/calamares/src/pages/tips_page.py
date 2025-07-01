"""
Tips Page for BigLinux Calamares Configuration Tool
Installation tips and guidance page
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject
from ..utils.i18n import _


class TipsPage(Gtk.Box):
    """Page displaying installation tips and guidance"""
    
    # Define signals for navigation
    __gsignals__ = {
        'navigate': (GObject.SignalFlags.RUN_FIRST, None, (str, object))
    }
    
    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
        )
        
        self.logger = logging.getLogger(__name__)
        
        # Add CSS class for styling
        self.add_css_class("tips-page")
        
        # Create content
        self.create_content()
        
        self.logger.debug("TipsPage initialized")
    
    def create_content(self):
        """Create the tips page content"""
        # Create main container with centering
        main_container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            hexpand=True,
            vexpand=True
        )
        
        # Create tips card
        self.create_tips_card(main_container)
        
        self.append(main_container)
    
    def create_tips_card(self, parent):
        """Create the main tips card"""
        # Create tips card container
        tips_card = Adw.Bin()
        tips_card.add_css_class("card")
        tips_card.add_css_class("tips-card")
        tips_card.set_size_request(600, 500)
        
        # Create main content box
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )
        
        # Create header section
        self.create_header_section(content_box)
        
        # Create tips content section
        self.create_tips_content(content_box)
        
        # Create continue button section
        self.create_continue_section(content_box)
        
        tips_card.set_child(content_box)
        parent.append(tips_card)
    
    def create_header_section(self, parent):
        """Create header section with title and subtitle"""
        # Create header container
        header_container = Adw.Bin()
        header_container.add_css_class("card")
        header_container.add_css_class("tips-header")
        
        header_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER
        )
        header_box.set_margin_top(24)
        header_box.set_margin_bottom(24)
        header_box.set_margin_start(24)
        header_box.set_margin_end(24)
        
        # Main title
        title_label = Gtk.Label(label=_("Important tips for manual partitioning"))
        title_label.add_css_class("title-2")
        title_label.add_css_class("tips-title")
        title_label.set_halign(Gtk.Align.CENTER)
        title_label.set_wrap(True)
        header_box.append(title_label)
        
        # Subtitle
        subtitle_label = Gtk.Label(
            label=_("If you opt for automatic partitioning, these tips will be applied.")
        )
        subtitle_label.add_css_class("body")
        subtitle_label.add_css_class("dim-label")
        subtitle_label.set_halign(Gtk.Align.CENTER)
        subtitle_label.set_wrap(True)
        header_box.append(subtitle_label)
        
        header_container.set_child(header_box)
        parent.append(header_container)
    
    def create_tips_content(self, parent):
        """Create tips content section"""
        # Create tips content box
        tips_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=18
        )
        tips_box.set_margin_top(24)
        tips_box.set_margin_bottom(24)
        tips_box.set_margin_start(32)
        tips_box.set_margin_end(32)
        
        # Create tips list
        tips_data = [
            {
                'title': _("Use BTRFS."),
                'description': _("This file system allows for automatic compression and restore points.")
            },
            {
                'title': _("Keep /boot within the / partition."),
                'description': _("Placing it in a separate partition hampers BTRFS snapshots.")
            },
            {
                'title': _("Do not create a SWAP partition."),
                'description': _("We have implemented dynamic virtual memory management with Zram and SWAP files.") + "\n" + _("SWAP partitions will not be used.")
            }
        ]
        
        for tip_data in tips_data:
            tip_widget = self.create_tip_item(tip_data['title'], tip_data['description'])
            tips_box.append(tip_widget)
        
        parent.append(tips_box)
    
    def create_tip_item(self, title, description):
        """
        Create a single tip item
        
        Args:
            title: Tip title (bold text)
            description: Tip description
            
        Returns:
            Gtk.Box containing the tip item
        """
        tip_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8,
            halign=Gtk.Align.START
        )
        
        # Create bullet point and title container
        title_container = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
            halign=Gtk.Align.START
        )
        
        # Bullet point
        bullet_label = Gtk.Label(label="•")
        bullet_label.add_css_class("title-3")
        bullet_label.add_css_class("accent")
        bullet_label.set_valign(Gtk.Align.START)
        title_container.append(bullet_label)
        
        # Title label
        title_label = Gtk.Label(label=title)
        title_label.add_css_class("title-4")
        title_label.add_css_class("tip-title")
        title_label.set_halign(Gtk.Align.START)
        title_label.set_wrap(True)
        title_label.set_max_width_chars(50)
        title_container.append(title_label)
        
        tip_box.append(title_container)
        
        # Description with indentation
        desc_container = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8
        )
        
        # Spacer for indentation
        spacer = Gtk.Box()
        spacer.set_size_request(24, -1)  # Same width as bullet + spacing
        desc_container.append(spacer)
        
        # Description label
        desc_label = Gtk.Label(label=description)
        desc_label.add_css_class("body")
        desc_label.add_css_class("tip-description")
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_wrap(True)
        desc_label.set_max_width_chars(60)
        desc_label.set_xalign(0.0)  # Left align
        desc_container.append(desc_label)
        
        tip_box.append(desc_container)
        
        return tip_box
    
    def create_continue_section(self, parent):
        """Create continue button section"""
        # Create continue section box
        continue_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.END
        )
        continue_box.set_margin_top(32)
        continue_box.set_margin_bottom(24)
        
        # Continue button
        continue_button = Gtk.Button(label=_("Continue"))
        continue_button.add_css_class("suggested-action")
        continue_button.add_css_class("pill")
        continue_button.set_size_request(140, 40)
        continue_button.connect("clicked", self.on_continue_clicked)
        continue_box.append(continue_button)
        
        parent.append(continue_box)
    
    def on_continue_clicked(self, button):
        """Handle continue button click"""
        self.logger.info("Continue from tips page - closing application")
        
        try:
            # Show confirmation message
            self.show_success_message(_("Installation process will continue with Calamares"))
            
            # Close the application to let Calamares take over
            application = self.get_root().get_application()
            if application:
                application.quit()
            
        except Exception as e:
            self.logger.error(f"Error closing application: {e}")
            self.show_error_message(_("Error proceeding to installation"))
    
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
        self.logger.debug("TipsPage activated")
        
        # Log that we've reached the final step
        self.logger.info("User reached tips page - installation configured")
    
    def cleanup(self):
        """Cleanup page resources"""
        self.logger.debug("TipsPage cleanup")
        # No specific cleanup needed for tips page
        pass


# Register the signal
GObject.type_register(TipsPage)
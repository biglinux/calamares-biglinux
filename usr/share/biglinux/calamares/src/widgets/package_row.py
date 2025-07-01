"""
Package Row Widget for BigLinux Calamares Configuration Tool
Individual package item with icon, name, and checkbox
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject, Gio, GdkPixbuf
from ..utils.i18n import _
from ..services.package_service import Package


class PackageRowWidget(Gtk.Box):
    """Widget representing a single package in the selection list"""
    
    # Define signals
    __gsignals__ = {
        'toggled': (GObject.SignalFlags.RUN_FIRST, None, (bool,)),
        'info-requested': (GObject.SignalFlags.RUN_FIRST, None, ())
    }
    
    def __init__(self, package: Package):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.CENTER
        )
        
        self.logger = logging.getLogger(__name__)
        self._package = package
        self._checkbox = None
        self._icon_image = None
        self._name_label = None
        self._info_button = None
        
        # Add CSS classes for styling
        self.add_css_class("package-row")
        self.add_css_class("card")
        
        # Set margins and padding
        self.set_margin_top(6)
        self.set_margin_bottom(6)
        self.set_margin_start(12)
        self.set_margin_end(12)
        
        # Create the widget content
        self.create_content()
        
        self.logger.debug(f"PackageRowWidget created for: {package.name}")
    
    def create_content(self):
        """Create the widget content"""
        # Create main content box with padding
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.CENTER
        )
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        content_box.set_margin_start(16)
        content_box.set_margin_end(16)
        
        # Create package icon
        self.create_icon(content_box)
        
        # Create package name label
        self.create_name_label(content_box)
        
        # Create spacer to push checkbox to the right
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        content_box.append(spacer)
        
        # Create info button (optional)
        self.create_info_button(content_box)
        
        # Create checkbox
        self.create_checkbox(content_box)
        
        self.append(content_box)
    
    def create_icon(self, parent_box):
        """Create package icon"""
        self._icon_image = Gtk.Image()
        self._icon_image.set_pixel_size(48)
        self._icon_image.add_css_class("package-icon")
        
        # Load icon
        self.load_package_icon()
        
        parent_box.append(self._icon_image)
    
    def create_name_label(self, parent_box):
        """Create package name label"""
        self._name_label = Gtk.Label(
            label=self._package.name,
            halign=Gtk.Align.START,
            valign=Gtk.Align.CENTER,
            ellipsize=3  # ELLIPSIZE_END
        )
        self._name_label.add_css_class("package-name")
        self._name_label.add_css_class("heading")
        self._name_label.set_hexpand(True)
        
        parent_box.append(self._name_label)
    
    def create_info_button(self, parent_box):
        """Create optional info button"""
        self._info_button = Gtk.Button()
        self._info_button.set_icon_name("dialog-information-symbolic")
        self._info_button.add_css_class("flat")
        self._info_button.add_css_class("circular")
        self._info_button.set_tooltip_text(_("Package Information"))
        self._info_button.set_valign(Gtk.Align.CENTER)
        self._info_button.connect("clicked", self.on_info_button_clicked)
        
        # Hide info button for now (can be enabled later)
        self._info_button.set_visible(False)
        
        parent_box.append(self._info_button)
    
    def create_checkbox(self, parent_box):
        """Create selection checkbox"""
        self._checkbox = Gtk.CheckButton()
        self._checkbox.set_active(self._package.selected)
        self._checkbox.add_css_class("selection-check")
        self._checkbox.set_valign(Gtk.Align.CENTER)
        self._checkbox.connect("toggled", self.on_checkbox_toggled)
        
        # Add accessibility label
        self._checkbox.set_tooltip_text(
            _("Select {} for removal").format(self._package.name)
        )
        
        parent_box.append(self._checkbox)
    
    def load_package_icon(self):
        """Load package icon from file or fallback"""
        try:
            icon_path = self._package.icon
            
            if icon_path and icon_path.startswith('/'):
                # Absolute path - load from file
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        icon_path, 48, 48, True
                    )
                    self._icon_image.set_from_pixbuf(pixbuf)
                    return
                except Exception as e:
                    self.logger.warning(f"Failed to load icon from {icon_path}: {e}")
            
            # Try to load as icon name
            if icon_path:
                self._icon_image.set_from_icon_name(icon_path)
            else:
                # Fallback to generic package icon
                self._icon_image.set_from_icon_name("package-x-generic")
                
        except Exception as e:
            self.logger.warning(f"Failed to load icon for {self._package.name}: {e}")
            self._icon_image.set_from_icon_name("package-x-generic")
    
    def on_checkbox_toggled(self, checkbox):
        """Handle checkbox toggle"""
        selected = checkbox.get_active()
        self._package.selected = selected
        
        self.logger.debug(f"Package {self._package.name} toggled: {selected}")
        
        # Update visual state
        self.update_selection_state(selected)
        
        # Emit signal
        self.emit('toggled', selected)
    
    def on_info_button_clicked(self, button):
        """Handle info button click"""
        self.logger.debug(f"Info requested for package: {self._package.name}")
        self.emit('info-requested')
    
    def update_selection_state(self, selected: bool):
        """Update visual state based on selection"""
        if selected:
            self.remove_css_class("package-unselected")
            self.add_css_class("package-selected")
        else:
            self.remove_css_class("package-selected")
            self.add_css_class("package-unselected")
    
    def set_selected(self, selected: bool):
        """Set package selection state"""
        self._package.selected = selected
        if self._checkbox:
            self._checkbox.set_active(selected)
        self.update_selection_state(selected)
    
    def get_selected(self) -> bool:
        """Get package selection state"""
        return self._package.selected
    
    def get_package(self) -> Package:
        """Get the package object"""
        return self._package
    
    def get_package_name(self) -> str:
        """Get package name"""
        return self._package.name
    
    def set_sensitive(self, sensitive: bool):
        """Set widget sensitivity"""
        super().set_sensitive(sensitive)
        if self._checkbox:
            self._checkbox.set_sensitive(sensitive)
        if self._info_button:
            self._info_button.set_sensitive(sensitive)
    
    def refresh_icon(self):
        """Refresh package icon"""
        if self._icon_image:
            self.load_package_icon()
    
    def set_show_info_button(self, show: bool):
        """Show or hide the info button"""
        if self._info_button:
            self._info_button.set_visible(show)
    
    def update_package_data(self, package: Package):
        """Update widget with new package data"""
        self._package = package
        
        # Update name label
        if self._name_label:
            self._name_label.set_text(package.name)
        
        # Update checkbox
        if self._checkbox:
            self._checkbox.set_active(package.selected)
        
        # Update icon
        self.refresh_icon()
        
        # Update selection state
        self.update_selection_state(package.selected)
        
        self.logger.debug(f"PackageRowWidget updated for: {package.name}")
    
    def set_compact_mode(self, compact: bool):
        """Set compact display mode"""
        if compact:
            self.add_css_class("compact")
            if self._icon_image:
                self._icon_image.set_pixel_size(32)
        else:
            self.remove_css_class("compact")
            if self._icon_image:
                self._icon_image.set_pixel_size(48)
    
    def animate_selection_change(self):
        """Animate selection state change"""
        # Add a subtle animation class that can be styled with CSS
        self.add_css_class("selection-changed")
        
        # Remove the class after animation duration
        def remove_animation_class():
            self.remove_css_class("selection-changed")
            return False
        
        from gi.repository import GLib
        GLib.timeout_add(300, remove_animation_class)


# Register the signal
GObject.type_register(PackageRowWidget)
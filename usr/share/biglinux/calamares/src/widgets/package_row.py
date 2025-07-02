# src/widgets/package_row.py

"""
Package Row Widget for BigLinux Calamares Configuration Tool
Individual package item using Adw.ActionRow for a native look and feel.
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject, GdkPixbuf
from ..utils.i18n import _
from ..services.package_service import Package

class PackageRowWidget(Adw.ActionRow):
    """Widget representing a single package using Adw.ActionRow."""

    # Define signals
    __gsignals__ = {
        'toggled': (GObject.SignalFlags.RUN_FIRST, None, (bool,)),
    }

    def __init__(self, package: Package):
        super().__init__()

        self.logger = logging.getLogger(__name__)
        self._package = package
        self.icon_size = 36 # Define icon size for consistency

        self.set_title(package.name)
        self.set_title_lines(1)
        # Subtitle removed for a cleaner UI, as the instruction is now in the window title.
        self.set_subtitle("")

        self.add_css_class("package-row")

        # Create and add the icon as a prefix widget
        self._icon_image = Gtk.Image()
        self._icon_image.set_pixel_size(self.icon_size)
        self.load_package_icon()
        self.add_prefix(self._icon_image)

        # Use Gtk.Switch for the selection.
        self._switch = Gtk.Switch()
        self._switch.set_valign(Gtk.Align.CENTER)
        self._switch.set_active(self._package.selected)
        self._switch.connect("notify::active", self.on_switch_toggled)
        self.add_suffix(self._switch)
        self.set_activatable_widget(self._switch)

        self.update_selection_state(self._package.selected)
        self.logger.debug(f"PackageRowWidget created for: {package.name}")

    def load_package_icon(self):
        """Load package icon from file or fallback."""
        try:
            icon_path = self._package.icon
            if icon_path and icon_path.startswith('/'):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, self.icon_size, self.icon_size, True)
                self._icon_image.set_from_pixbuf(pixbuf)
            elif icon_path:
                self._icon_image.set_from_icon_name(icon_path)
            else:
                self._icon_image.set_from_icon_name("package-x-generic")
        except Exception as e:
            self.logger.warning(f"Failed to load icon for {self._package.name}: {e}")
            self._icon_image.set_from_icon_name("package-x-generic")

    def on_switch_toggled(self, switch, _):
        """Handle switch toggle."""
        to_keep = switch.get_active()
        self._package.selected = to_keep
        self.logger.debug(f"Package {self._package.name} will be kept: {to_keep}")
        self.update_selection_state(to_keep)
        self.emit('toggled', to_keep)

    def update_selection_state(self, to_keep: bool):
        """Update visual state. Dim items that will be REMOVED (switch is OFF)."""
        if to_keep:
            self.remove_css_class("dim-label")
        else:
            self.add_css_class("dim-label")

    def set_selected(self, to_keep: bool):
        """Programmatically set the package selection state."""
        if self._switch.get_active() != to_keep:
            self._switch.set_active(to_keep)

    def get_selected(self) -> bool:
        """Get package selection state (True means 'to keep')."""
        return self._switch.get_active()

    def get_package_name(self) -> str:
        """Get package name."""
        return self.get_title()

    def update_package_data(self, package: Package):
        """Update widget with new package data."""
        self._package = package
        self.set_title(package.name)
        self.set_selected(package.selected)
        self.load_package_icon()
        self.update_selection_state(package.selected)
        self.logger.debug(f"PackageRowWidget updated for: {package.name}")

# Register the widget
GObject.type_register(PackageRowWidget)

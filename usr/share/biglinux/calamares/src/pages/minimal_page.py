# src/pages/minimal_page.py

"""
Minimal Page for BigLinux Calamares Configuration Tool
Package selection page for minimal installation
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject, GLib
from ..utils.i18n import _
from ..services import get_package_service, get_install_service
from ..widgets import PackageRowWidget


class MinimalPage(Gtk.Box):
    """Page for selecting packages to remove in minimal installation"""

    __gsignals__ = {
        'navigate': (GObject.SignalFlags.RUN_FIRST, None, (str, object))
    }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.logger = logging.getLogger(__name__)
        self.package_service = get_package_service()
        self.install_service = get_install_service()
        self.packages = []
        self.package_widgets = []
        self.loading_box = None
        self.packages_listbox = None
        self.add_css_class("minimal-page")
        self.create_content()
        self.load_packages()
        self.logger.debug("MinimalPage initialized")

    def create_content(self):
        """Create the minimal page content with proper Adwaita layout."""
        # The instructional text is now moved to the window title, so the header box is removed.
        scrolled = Gtk.ScrolledWindow(vexpand=True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.append(scrolled)

        clamp = Adw.Clamp(maximum_size=800)
        scrolled.set_child(clamp)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        clamp.set_child(content_box)

        self.loading_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, visible=True, margin_top=48)
        spinner = Gtk.Spinner(halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER, hexpand=True, vexpand=True)
        spinner.start()
        status_label = Gtk.Label(label=_("Loading packages..."), halign=Gtk.Align.CENTER)
        status_label.add_css_class("dim-label")
        self.loading_box.append(spinner)
        self.loading_box.append(status_label)
        content_box.append(self.loading_box)

        self.packages_listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, visible=False)
        self.packages_listbox.add_css_class("boxed-list")
        # Add vertical spacing for a cleaner layout
        self.packages_listbox.set_margin_top(12)
        self.packages_listbox.set_margin_bottom(12)
        content_box.append(self.packages_listbox)

    def load_packages(self):
        """Load packages asynchronously."""
        def load_async():
            try:
                packages = self.package_service.get_minimal_packages()
                GLib.idle_add(self.on_packages_loaded, packages)
            except Exception as e:
                self.logger.error(f"Failed to load packages: {e}")
                GLib.idle_add(self.on_packages_load_error, str(e))
        import threading
        threading.Thread(target=load_async, daemon=True).start()

    def on_packages_loaded(self, packages):
        self.packages = packages
        self.logger.info(f"Loaded {len(packages)} packages")
        self.loading_box.set_visible(False)
        self.packages_listbox.set_visible(True)
        for package in self.packages:
            # Default to all packages being kept (switch ON).
            package.selected = True
            package_widget = PackageRowWidget(package)
            self.packages_listbox.append(package_widget)
            self.package_widgets.append(package_widget)

    def on_packages_load_error(self, error_message):
        self.loading_box.get_first_child().stop()
        self.loading_box.get_last_child().set_text(_("Failed to load packages: {}").format(error_message))
        self.loading_box.get_last_child().add_css_class("error")

    def on_check_all_clicked(self, button):
        """Corresponds to 'Keep All'"""
        self.set_all_selected(True)
        self.show_success_message(_("All optional programs will be kept"))

    def on_uncheck_all_clicked(self, button):
        """Corresponds to 'Remove All'"""
        self.set_all_selected(False)
        self.show_success_message(_("All optional programs selected for removal"))

    def set_all_selected(self, selected):
        for widget in self.package_widgets:
            widget.set_selected(selected)

    def do_continue_action(self, button):
        """This method is called by the main window's continue button."""
        self.logger.info("Continue with minimal installation")
        # Collect packages where the switch is OFF (selected=False means 'do not keep')
        packages_to_remove = [w.get_package_name() for w in self.package_widgets if not w.get_selected()]

        if not packages_to_remove:
            self.show_success_message(_("No programs selected for removal. Proceeding with standard installation."))
        
        button.set_sensitive(False)
        button.set_label(_("Starting..."))

        def reset_button_state():
            button.set_sensitive(True)
            button.set_label(_("Continue"))

        try:
            success = self.install_service.start_installation(
                filesystem_type="btrfs",
                packages_to_remove=packages_to_remove
            )
            if success:
                self.show_success_message(_("Minimal installation started successfully"))
                self.emit('navigate', 'tips', None)
            else:
                self.show_error_message(_("Failed to start minimal installation"))
                reset_button_state()
        except Exception as e:
            self.logger.error(f"Failed to start minimal installation: {e}", exc_info=True)
            self.show_error_message(_("Error starting minimal installation"))
            reset_button_state()

    def show_success_message(self, message):
        toplevel = self.get_root()
        if hasattr(toplevel, 'show_success_toast'):
            toplevel.show_success_toast(message)

    def show_error_message(self, message):
        toplevel = self.get_root()
        if hasattr(toplevel, 'show_error_toast'):
            toplevel.show_error_toast(message)

    def on_page_activated(self):
        self.logger.debug("MinimalPage activated")
        if not self.packages:
            self.load_packages()

    def cleanup(self):
        self.logger.debug("MinimalPage cleanup")
        self.package_widgets.clear()
        self.packages.clear()

GObject.type_register(MinimalPage)

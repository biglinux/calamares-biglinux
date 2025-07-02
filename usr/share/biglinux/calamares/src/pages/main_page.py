# src/pages/main_page.py

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
from ..widgets import OptionCard, SystemInfoWidget


class MainPage(Gtk.Box):
    """Main page with three installation/maintenance options"""

    __gsignals__ = {
        'navigate': (GObject.SignalFlags.RUN_FIRST, None, (str, object))
    }

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,  # Adds space between the main cards and the bottom info bar
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL,
            hexpand=True,
            vexpand=True
        )

        self.logger = logging.getLogger(__name__)
        self.system_service = get_system_service()
        self.install_service = get_install_service()

        self.add_css_class("main-page")
        
        # Design Justification: Add margins around the entire page content
        # to prevent elements from touching the window edges, creating a more
        # balanced and professional layout as seen in the reference image.
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)

        self.create_content()
        self.logger.debug("MainPage initialized")

    def create_content(self):
        """Create the main page content."""
        main_content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.CENTER,
            vexpand=True
        )
        self.append(main_content_box)

        clamp = Adw.Clamp(maximum_size=1000)
        main_content_box.append(clamp)

        grid_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=24,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            homogeneous=True
        )
        clamp.set_child(grid_box)

        maintenance_card = OptionCard(
            icon_name="applications-utilities",
            title=_("Maintenance"),
            description=_("Tools that facilitate the maintenance of the installed system."),
            button_text=_("Restore"),
            button_style="secondary"
        )
        maintenance_card.connect('clicked', self.on_maintenance_clicked)
        grid_box.append(maintenance_card)

        installation_card = OptionCard(
            icon_name="system-software-install",
            title=_("Installation"),
            description=_("The system is in live mode, which has limitations."),
            description2=_("Install it for a complete experience."),
            button_text=_("Install"),
            button_style="suggested-action"
        )
        installation_card.connect('clicked', self.on_installation_clicked)
        grid_box.append(installation_card)

        minimal_card = OptionCard(
            icon_name="preferences-system",
            title=_("Minimal"),
            description=_("Remove pre-selected software to create a lean, personalized system."),
            button_text=_("Continue"),
            button_style="secondary"
        )
        minimal_card.connect('clicked', self.on_minimal_clicked)
        grid_box.append(minimal_card)
        
        # Add system info widget at the bottom
        system_info_container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.END,
            vexpand=False
        )
        self.append(system_info_container)
        system_info_widget = SystemInfoWidget()
        system_info_container.append(system_info_widget)


    def on_maintenance_clicked(self, card):
        self.logger.info("Maintenance option selected")
        self.emit('navigate', 'maintenance', None)

    def on_installation_clicked(self, card):
        self.logger.info("Installation option selected")
        button = card.get_action_button()
        try:
            button.set_sensitive(False)
            button.set_label(_("Starting..."))
            requirements = self.install_service.check_installation_requirements()
            missing = [k for k, v in requirements.items() if not v]
            if missing:
                self.show_error_message(_("Installation requirements not met: {}").format(", ".join(missing)))
                self.reset_button_state(button, _("Install"))
                return
            if self.install_service.start_installation("btrfs"):
                self.show_success_message(_("Installation started successfully"))
                self.emit('navigate', 'tips', None)
            else:
                self.show_error_message(_("Failed to start installation"))
            self.reset_button_state(button, _("Install"))
        except Exception as e:
            self.logger.error(f"Installation start failed: {e}")
            self.show_error_message(_("Error starting installation"))
            self.reset_button_state(button, _("Install"))

    def on_minimal_clicked(self, card):
        self.logger.info("Minimal installation option selected")
        self.emit('navigate', 'minimal', None)

    def reset_button_state(self, button, original_text):
        button.set_sensitive(True)
        button.set_label(original_text)

    def show_success_message(self, message):
        toplevel = self.get_root()
        if hasattr(toplevel, 'show_success_toast'):
            toplevel.show_success_toast(message)

    def show_error_message(self, message):
        toplevel = self.get_root()
        if hasattr(toplevel, 'show_error_toast'):
            toplevel.show_error_toast(message)

    def on_page_activated(self):
        self.logger.debug("MainPage activated")

    def cleanup(self):
        self.logger.debug("MainPage cleanup")

GObject.type_register(MainPage)

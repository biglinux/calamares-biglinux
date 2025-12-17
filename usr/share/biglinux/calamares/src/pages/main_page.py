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


class MainPage(Gtk.Box):
    """Main page with three installation/maintenance options"""

    __gsignals__ = {
        'navigate': (GObject.SignalFlags.RUN_FIRST, None, (str, object))
    }

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL,
            hexpand=True,
            vexpand=True
        )

        self.logger = logging.getLogger(__name__)
        self.system_service = get_system_service()
        self.install_service = get_install_service()

        self.add_css_class("main-page")
        
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)

        self.create_content()
        self.logger.debug("MainPage initialized")

    def _create_option_card(self, icon_name, title, description, button_text, button_style, callback, description2=None):
        """Factory function to create a card widget."""
        card_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        card_box.set_size_request(280, 320)
        card_box.set_valign(Gtk.Align.CENTER)
        card_box.set_halign(Gtk.Align.CENTER)

        card_bin = Adw.Bin()
        card_bin.add_css_class("card")
        card_box.append(card_bin)

        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=16,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL,
            hexpand=True,
            vexpand=True,
            margin_top=24, margin_bottom=24, margin_start=24, margin_end=24
        )
        card_bin.set_child(content_box)

        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(64)
        icon.add_css_class("option-icon")
        content_box.append(icon)

        title_label = Gtk.Label(label=title, halign=Gtk.Align.CENTER)
        title_label.add_css_class("title-2")
        content_box.append(title_label)

        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, vexpand=True, valign=Gtk.Align.CENTER)
        content_box.append(desc_box)
        
        desc_label = Gtk.Label(
            label=description, wrap=True, justify=Gtk.Justification.CENTER,
            halign=Gtk.Align.CENTER, max_width_chars=35
        )
        desc_label.add_css_class("body")
        desc_box.append(desc_label)

        if description2:
            desc2_label = Gtk.Label(
                label=description2, wrap=True, justify=Gtk.Justification.CENTER,
                halign=Gtk.Align.CENTER, max_width_chars=35
            )
            desc2_label.add_css_class("body")
            desc_box.append(desc2_label)

        button = Gtk.Button(label=button_text, halign=Gtk.Align.CENTER, valign=Gtk.Align.END)
        button.add_css_class(button_style)
        button.add_css_class("pill")
        button.connect("clicked", callback)
        content_box.append(button)
        
        # Store button for later access if needed
        card_box.action_button = button
        return card_box

    def _create_system_info_bar(self):
        """Factory function to create the system info bar."""
        system_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        system_info_box.set_margin_top(8)
        system_info_box.set_margin_bottom(8)
        system_info_box.set_margin_start(12)
        system_info_box.set_margin_end(12)

        boot_mode = self.system_service.get_boot_mode()
        kernel_version = self.system_service.get_kernel_version()
        session_type = self.system_service.get_session_type()
        
        markup = (
            f"{_('The system is in')} <b>{boot_mode}</b>, "
            f"Linux <b>{kernel_version}</b> {_('and graphical mode')} <b>{session_type}</b>."
        )
        
        info_label = Gtk.Label(
            use_markup=True, label=markup, wrap=True,
            justify=Gtk.Justification.CENTER, halign=Gtk.Align.CENTER
        )
        system_info_box.append(info_label)

        forum_link = Gtk.LinkButton(
            uri="https://forum.biglinux.com.br",
            label=_("This is a collaborative system, if you need help consult our forum.")
        )
        forum_link.set_halign(Gtk.Align.CENTER)
        system_info_box.append(forum_link)
        
        return system_info_box

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

        maintenance_card = self._create_option_card(
            icon_name="applications-utilities",
            title=_("Maintenance"),
            description=_("Tools that facilitate the maintenance of the installed system."),
            button_text=_("Restore"),
            button_style="secondary",
            callback=self.on_maintenance_clicked
        )
        grid_box.append(maintenance_card)

        self.installation_card = self._create_option_card(
            icon_name="system-software-install",
            title=_("Installation"),
            description=_("The system is in live mode, which has limitations."),
            description2=_("Install it for a complete experience."),
            button_text=_("Install"),
            button_style="suggested-action",
            callback=self.on_installation_clicked
        )
        grid_box.append(self.installation_card)

        minimal_card = self._create_option_card(
            icon_name="preferences-system",
            title=_("Minimal"),
            description=_("Remove pre-selected software to create a lean, personalized system."),
            button_text=_("Continue"),
            button_style="secondary",
            callback=self.on_minimal_clicked
        )
        grid_box.append(minimal_card)
        
        system_info_container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.END,
            vexpand=False
        )
        self.append(system_info_container)
        system_info_widget = self._create_system_info_bar()
        system_info_container.append(system_info_widget)

    def on_maintenance_clicked(self, button):
        self.logger.info("Maintenance option selected")
        self.emit('navigate', 'maintenance', None)

    def on_installation_clicked(self, button):
        self.logger.info("Installation option selected")
        try:
            button.set_sensitive(False)
            button.set_label(_("Starting..."))
            requirements = self.install_service.check_installation_requirements()
            missing = [k for k, v in requirements.items() if not v]
            if missing:
                self.show_error_message(_("Installation requirements not met: {}").format(", ".join(missing)))
                self.reset_button_state(button, _("Install"))
                return
            # Configure for a standard installation and then navigate to the tips page.
            # The application will close from the tips page, and Calamares is expected to be launched externally.
            if self.install_service.start_installation("btrfs", packages_to_remove=[]):
                self.show_success_message(_("Installation configured successfully"))
                self.emit('navigate', 'tips', None)
            else:
                self.show_error_message(_("Failed to configure installation"))
                self.reset_button_state(button, _("Install"))
        except Exception as e:
            self.logger.error(f"Installation configuration failed: {e}")
            self.show_error_message(_("Error configuring installation"))
            self.reset_button_state(button, _("Install"))

    def on_minimal_clicked(self, button):
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

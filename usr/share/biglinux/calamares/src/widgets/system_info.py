# src/widgets/system_info.py

"""
System Info Widget for BigLinux Calamares Configuration Tool
Displays system information in a cohesive bar.
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from ..utils.i18n import _
from ..services import get_system_service

class SystemInfoWidget(Gtk.Box):
    """A bar-styled widget that displays system information."""
    
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.logger = logging.getLogger(__name__)
        self.system_service = get_system_service()
        
        self.set_margin_top(8)
        self.set_margin_bottom(8)
        self.set_margin_start(12)
        self.set_margin_end(12)
        
        self.create_info_label(self)
        self.create_forum_link(self)
        
        self.logger.debug("SystemInfoWidget initialized")
    
    def create_info_label(self, parent):
        """Create a single label for system info using Pango markup."""
        boot_mode = self.system_service.get_boot_mode()
        kernel_version = self.system_service.get_kernel_version()
        session_type = self.system_service.get_session_type()
        
        markup = (
            f"{_('The system is in')} <b>{boot_mode}</b>, "
            f"Linux <b>{kernel_version}</b> {_('and graphical mode')} <b>{session_type}</b>."
        )
        
        info_label = Gtk.Label(
            use_markup=True,
            label=markup,
            wrap=True,
            justify=Gtk.Justification.CENTER,
            halign=Gtk.Align.CENTER
        )
        parent.append(info_label)

    def create_forum_link(self, parent):
        """Create the forum support link."""
        forum_link = Gtk.LinkButton(
            uri="https://forum.biglinux.com.br",
            label=_("This is a collaborative system, if you need help consult our forum.")
        )
        forum_link.set_halign(Gtk.Align.CENTER)
        parent.append(forum_link)

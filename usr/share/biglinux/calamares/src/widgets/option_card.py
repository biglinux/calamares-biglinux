# src/widgets/option_card.py

"""
Option Card Widget for BigLinux Calamares Configuration Tool
A reusable card for main navigation options.
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject

class OptionCard(Gtk.Box):
    """A clickable card widget with an icon, title, description, and button."""

    __gsignals__ = {
        'clicked': (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, icon_name, title, description, button_text, button_style, description2=None, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)

        self.logger = logging.getLogger(__name__)

        self.set_size_request(280, 320)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        self.set_spacing(16)

        card_bin = Adw.Bin()
        card_bin.add_css_class("card")
        self.append(card_bin)

        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=16,
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL,
            hexpand=True,
            vexpand=True
        )
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        card_bin.set_child(content_box)

        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(64)
        icon.add_css_class("option-icon")
        content_box.append(icon)

        title_label = Gtk.Label(label=title)
        title_label.add_css_class("title-2")
        title_label.set_halign(Gtk.Align.CENTER)
        content_box.append(title_label)

        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, vexpand=True, valign=Gtk.Align.CENTER)
        content_box.append(desc_box)
        
        desc_label = Gtk.Label(
            label=description,
            wrap=True,
            justify=Gtk.Justification.CENTER,
            halign=Gtk.Align.CENTER
        )
        desc_label.add_css_class("body")
        desc_label.set_max_width_chars(35)
        desc_box.append(desc_label)

        if description2:
            desc2_label = Gtk.Label(
                label=description2,
                wrap=True,
                justify=Gtk.Justification.CENTER,
                halign=Gtk.Align.CENTER
            )
            desc2_label.add_css_class("body")
            desc2_label.set_max_width_chars(35)
            desc_box.append(desc2_label)

        # Restore the .pill class for a rounded button style.
        self.action_button = Gtk.Button(label=button_text)
        self.action_button.add_css_class(button_style)
        self.action_button.add_css_class("pill")
        self.action_button.set_halign(Gtk.Align.CENTER)
        self.action_button.set_valign(Gtk.Align.END)
        self.action_button.connect("clicked", self.on_button_clicked)
        content_box.append(self.action_button)

    def on_button_clicked(self, button):
        """Emit the 'clicked' signal."""
        self.emit('clicked')

    def get_action_button(self):
        """Provides a robust way to access the action button."""
        return self.action_button

# Register the widget and its signal
GObject.type_register(OptionCard)

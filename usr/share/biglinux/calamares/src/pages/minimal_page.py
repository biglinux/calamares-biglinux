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
        self.package_service = get_package_service()
        self.install_service = get_install_service()
        
        # Package data
        self.packages = []
        self.package_widgets = []
        
        # UI components
        self.header_bar = None
        self.packages_listbox = None
        self.controls_bar = None
        self.loading_spinner = None
        self.status_label = None
        
        # Add CSS class for styling
        self.add_css_class("minimal-page")
        
        # Create content
        self.create_content()
        
        # Load packages
        self.load_packages()
        
        self.logger.debug("MinimalPage initialized")
    
    def create_content(self):
        """Create the minimal page content"""
        # Create header with title and description
        self.create_header()
        
        # Create main content area
        self.create_main_content()
        
        # Create controls bar
        self.create_controls_bar()
    
    def create_header(self):
        """Create page header with title and description"""
        header_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            halign=Gtk.Align.CENTER
        )
        header_box.set_margin_top(24)
        header_box.set_margin_bottom(18)
        header_box.set_margin_start(24)
        header_box.set_margin_end(24)
        
        # Page title
        title_label = Gtk.Label(label=_("Package Selection"))
        title_label.add_css_class("title-1")
        title_label.set_halign(Gtk.Align.CENTER)
        header_box.append(title_label)
        
        # Page description
        desc_label = Gtk.Label(
            label=_("Uncheck the programs you want to remove"),
            wrap=True,
            justify=Gtk.Justification.CENTER
        )
        desc_label.add_css_class("title-4")
        desc_label.add_css_class("dim-label")
        desc_label.set_halign(Gtk.Align.CENTER)
        header_box.append(desc_label)
        
        self.append(header_box)
    
    def create_main_content(self):
        """Create main content area with package list"""
        # Create scrolled window for package list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.set_margin_start(24)
        scrolled.set_margin_end(24)
        
        # Create content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        # Create loading spinner (initially visible)
        self.loading_spinner = Gtk.Spinner()
        self.loading_spinner.start()
        self.loading_spinner.set_halign(Gtk.Align.CENTER)
        self.loading_spinner.set_valign(Gtk.Align.CENTER)
        self.loading_spinner.set_size_request(48, 48)
        content_box.append(self.loading_spinner)
        
        # Create status label
        self.status_label = Gtk.Label(label=_("Loading packages..."))
        self.status_label.add_css_class("body")
        self.status_label.add_css_class("dim-label")
        self.status_label.set_halign(Gtk.Align.CENTER)
        content_box.append(self.status_label)
        
        # Create packages listbox (initially hidden)
        self.packages_listbox = Gtk.ListBox()
        self.packages_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.packages_listbox.add_css_class("content")
        self.packages_listbox.add_css_class("packages-list")
        self.packages_listbox.set_visible(False)
        content_box.append(self.packages_listbox)
        
        scrolled.set_child(content_box)
        self.append(scrolled)
    
    def create_controls_bar(self):
        """Create bottom controls bar"""
        # Create controls card
        controls_card = Adw.Bin()
        controls_card.add_css_class("card")
        controls_card.set_margin_start(24)
        controls_card.set_margin_end(24)
        controls_card.set_margin_bottom(24)
        
        # Create controls box
        controls_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            halign=Gtk.Align.CENTER
        )
        controls_box.set_margin_top(12)
        controls_box.set_margin_bottom(12)
        controls_box.set_margin_start(18)
        controls_box.set_margin_end(18)
        
        # Back button
        back_button = Gtk.Button(label=_("Back"))
        back_button.add_css_class("outlined")
        back_button.connect("clicked", self.on_back_clicked)
        controls_box.append(back_button)
        
        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        controls_box.append(spacer)
        
        # Uncheck all button
        uncheck_button = Gtk.Button(label=_("Uncheck All"))
        uncheck_button.connect("clicked", self.on_uncheck_all_clicked)
        controls_box.append(uncheck_button)
        
        # Check all button
        check_button = Gtk.Button(label=_("Check All"))
        check_button.connect("clicked", self.on_check_all_clicked)
        controls_box.append(check_button)
        
        # Spacer
        spacer2 = Gtk.Box()
        spacer2.set_hexpand(True)
        controls_box.append(spacer2)
        
        # Continue button
        continue_button = Gtk.Button(label=_("Continue"))
        continue_button.add_css_class("suggested-action")
        continue_button.connect("clicked", self.on_continue_clicked)
        controls_box.append(continue_button)
        
        controls_card.set_child(controls_box)
        self.append(controls_card)
    
    def load_packages(self):
        """Load packages asynchronously"""
        def load_packages_async():
            try:
                # Get minimal packages from service
                packages = self.package_service.get_minimal_packages()
                
                # Update UI in main thread
                GLib.idle_add(self.on_packages_loaded, packages)
                
            except Exception as e:
                self.logger.error(f"Failed to load packages: {e}")
                GLib.idle_add(self.on_packages_load_error, str(e))
        
        # Start loading in background thread
        import threading
        thread = threading.Thread(target=load_packages_async, daemon=True)
        thread.start()
    
    def on_packages_loaded(self, packages):
        """Handle packages loaded successfully"""
        self.packages = packages
        self.logger.info(f"Loaded {len(packages)} packages")
        
        # Hide loading spinner and status
        self.loading_spinner.stop()
        self.loading_spinner.set_visible(False)
        self.status_label.set_visible(False)
        
        # Show packages list
        self.packages_listbox.set_visible(True)
        
        # Populate packages list
        self.populate_packages_list()
        
        # Update status
        self.update_selection_status()
    
    def on_packages_load_error(self, error_message):
        """Handle packages loading error"""
        self.logger.error(f"Package loading error: {error_message}")
        
        # Hide spinner
        self.loading_spinner.stop()
        self.loading_spinner.set_visible(False)
        
        # Show error message
        self.status_label.set_text(_("Failed to load packages: {}").format(error_message))
        self.status_label.add_css_class("error")
    
    def populate_packages_list(self):
        """Populate the packages list"""
        self.package_widgets.clear()
        
        for package in self.packages:
            # Create package row widget
            package_widget = PackageRowWidget(package)
            package_widget.connect('toggled', self.on_package_toggled)
            
            # Add to listbox
            self.packages_listbox.append(package_widget)
            self.package_widgets.append(package_widget)
    
    def on_package_toggled(self, package_widget, selected):
        """Handle package selection toggle"""
        package_name = package_widget.get_package_name()
        self.logger.debug(f"Package {package_name} toggled: {selected}")
        
        # Update selection status
        self.update_selection_status()
    
    def update_selection_status(self):
        """Update selection status display"""
        if not self.packages:
            return
        
        selected_count = sum(1 for pkg in self.packages if pkg.selected)
        total_count = len(self.packages)
        
        # Could add a status label showing selection count
        # For now, just log it
        self.logger.debug(f"Selection: {selected_count}/{total_count} packages")
    
    def on_back_clicked(self, button):
        """Handle back button click"""
        self.logger.info("Back to main page requested")
        self.emit('navigate', 'back', None)
    
    def on_check_all_clicked(self, button):
        """Handle check all button click"""
        self.logger.info("Check all packages requested")
        
        for package_widget in self.package_widgets:
            package_widget.set_selected(True)
        
        self.update_selection_status()
        self.show_success_message(_("All packages selected"))
    
    def on_uncheck_all_clicked(self, button):
        """Handle uncheck all button click"""
        self.logger.info("Uncheck all packages requested")
        
        for package_widget in self.package_widgets:
            package_widget.set_selected(False)
        
        self.update_selection_status()
        self.show_success_message(_("All packages deselected"))
    
    def on_continue_clicked(self, button):
        """Handle continue button click"""
        self.logger.info("Continue with minimal installation")
        
        try:
            # Get selected packages for removal
            selected_packages = []
            for package_widget in self.package_widgets:
                if package_widget.get_selected():
                    selected_packages.append(package_widget.get_package_name())
            
            if not selected_packages:
                self.show_error_message(_("No packages selected for removal"))
                return
            
            # Show loading state
            button.set_sensitive(False)
            button.set_label(_("Starting..."))
            
            # Validate package selection
            validation = self.package_service.validate_package_selection(selected_packages)
            
            if validation['invalid'] or validation['not_installed'] or validation['not_removable']:
                error_msg = _("Invalid package selection")
                if validation['invalid']:
                    error_msg += f"\n{_('Invalid packages')}: {', '.join(validation['invalid'])}"
                if validation['not_installed']:
                    error_msg += f"\n{_('Not installed')}: {', '.join(validation['not_installed'])}"
                if validation['not_removable']:
                    error_msg += f"\n{_('Not removable')}: {', '.join(validation['not_removable'])}"
                
                self.show_error_message(error_msg)
                self.reset_button_state(button, _("Continue"))
                return
            
            # Start installation with package removal
            success = self.install_service.start_installation(
                filesystem_type="btrfs",
                packages_to_remove=validation['valid']
            )
            
            if success:
                self.show_success_message(_("Minimal installation started successfully"))
                # Navigate to tips page
                self.emit('navigate', 'tips', None)
            else:
                self.show_error_message(_("Failed to start minimal installation"))
            
            self.reset_button_state(button, _("Continue"))
            
        except Exception as e:
            self.logger.error(f"Failed to start minimal installation: {e}")
            self.show_error_message(_("Error starting minimal installation"))
            self.reset_button_state(button, _("Continue"))
    
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
        self.logger.debug("MinimalPage activated")
        
        # Refresh packages if needed
        if not self.packages:
            self.load_packages()
    
    def cleanup(self):
        """Cleanup page resources"""
        self.logger.debug("MinimalPage cleanup")
        
        # Clear package widgets
        self.package_widgets.clear()
        self.packages.clear()


# Register the signal
GObject.type_register(MinimalPage)
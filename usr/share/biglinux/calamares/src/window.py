"""
Main Window class for BigLinux Calamares Configuration Tool
Manages navigation between different pages using Gtk.Stack
"""

import logging
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GLib
from .utils.i18n import _
from .pages.main_page import MainPage
from .pages.maintenance_page import MaintenancePage
from .pages.minimal_page import MinimalPage
from .pages.tips_page import TipsPage
from .widgets.system_info import SystemInfoWidget


class CalamaresWindow(Adw.ApplicationWindow):
    """Main application window with navigation stack"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.logger = logging.getLogger(__name__)
        self.toast_overlay = None
        
        # Setup window properties
        self.setup_window()
        
        # Create main layout
        self.create_layout()
        
        # Create pages
        self.create_pages()
        
        # Setup navigation
        self.setup_navigation()
        
        self.logger.info("Main window initialized")
    
    def setup_window(self):
        """Configure window properties"""
        self.set_title(_("BigLinux Calamares Config"))
        self.set_default_size(800, 600)
        self.set_size_request(600, 400)
        
        # Set window icon
        self.set_icon_name("system-software-install")
        
        # Enable window controls
        self.set_deletable(True)
    
    def create_layout(self):
        """Create the main window layout"""
        # Create toast overlay for notifications
        self.toast_overlay = Adw.ToastOverlay()
        self.set_content(self.toast_overlay)
        
        # Create main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.toast_overlay.set_child(main_box)
        
        # Create header bar
        self.header_bar = Adw.HeaderBar()
        self.header_bar.set_decoration_layout(":close")
        main_box.append(self.header_bar)
        
        # Create navigation buttons (initially hidden)
        self.back_button = Gtk.Button(
            icon_name="go-previous-symbolic",
            tooltip_text=_("Back")
        )
        self.back_button.connect("clicked", self.on_back_clicked)
        self.back_button.set_visible(False)
        self.header_bar.pack_start(self.back_button)
        
        # Create stack for page navigation
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)
        main_box.append(self.stack)
        
        # Create system info widget
        self.system_info = SystemInfoWidget()
        main_box.append(self.system_info)
    
    def create_pages(self):
        """Create and add all pages to the stack"""
        # Main page (initial page)
        self.main_page = MainPage()
        self.main_page.connect("navigate", self.on_navigate_requested)
        self.stack.add_named(self.main_page, "main")
        
        # Maintenance page
        self.maintenance_page = MaintenancePage()
        self.maintenance_page.connect("navigate", self.on_navigate_requested)
        self.stack.add_named(self.maintenance_page, "maintenance")
        
        # Minimal installation page
        self.minimal_page = MinimalPage()
        self.minimal_page.connect("navigate", self.on_navigate_requested)
        self.stack.add_named(self.minimal_page, "minimal")
        
        # Tips page
        self.tips_page = TipsPage()
        self.tips_page.connect("navigate", self.on_navigate_requested)
        self.stack.add_named(self.tips_page, "tips")
    
    def setup_navigation(self):
        """Setup initial navigation state"""
        # Show main page initially
        self.stack.set_visible_child_name("main")
        self.update_navigation_state("main")
    
    def on_navigate_requested(self, widget, page_name, data=None):
        """Handle navigation requests from pages"""
        self.logger.info(f"Navigation requested to: {page_name}")
        
        if page_name == "back":
            self.navigate_back()
        else:
            self.navigate_to(page_name)
    
    def navigate_to(self, page_name, show_back=True):
        """Navigate to a specific page"""
        if not self.stack.get_child_by_name(page_name):
            self.logger.error(f"Page '{page_name}' not found")
            return
        
        # Update stack
        self.stack.set_visible_child_name(page_name)
        
        # Update navigation state
        self.update_navigation_state(page_name, show_back)
        
        # Notify page it became active
        current_page = self.stack.get_visible_child()
        if hasattr(current_page, 'on_page_activated'):
            current_page.on_page_activated()
    
    def navigate_back(self):
        """Navigate back to main page"""
        self.navigate_to("main", show_back=False)
    
    def update_navigation_state(self, page_name, show_back=True):
        """Update navigation UI state"""
        # Update back button visibility
        is_main_page = page_name == "main"
        self.back_button.set_visible(not is_main_page and show_back)
        
        # Update window title based on current page
        titles = {
            "main": _("BigLinux Calamares Config"),
            "maintenance": _("System Maintenance"),
            "minimal": _("Package Selection"),
            "tips": _("Installation Tips")
        }
        
        self.set_title(titles.get(page_name, _("BigLinux Calamares Config")))
    
    def on_back_clicked(self, button):
        """Handle back button click"""
        self.navigate_back()
    
    def show_toast(self, toast):
        """Show a toast notification"""
        if self.toast_overlay:
            self.toast_overlay.add_toast(toast)
    
    def show_error_toast(self, message, timeout=5):
        """Show error toast notification"""
        toast = Adw.Toast(
            title=message,
            timeout=timeout
        )
        self.show_toast(toast)
    
    def show_success_toast(self, message, timeout=3):
        """Show success toast notification"""
        toast = Adw.Toast(
            title=message,
            timeout=timeout
        )
        self.show_toast(toast)
    
    def show_loading_toast(self, message):
        """Show loading toast (indefinite)"""
        toast = Adw.Toast(
            title=message,
            timeout=0  # Indefinite
        )
        self.show_toast(toast)
        return toast
    
    def get_current_page(self):
        """Get the currently visible page"""
        return self.stack.get_visible_child()
    
    def get_current_page_name(self):
        """Get the name of currently visible page"""
        return self.stack.get_visible_child_name()
    
    def cleanup(self):
        """Cleanup resources before window closes"""
        self.logger.info("Window cleanup started")
        
        # Cleanup pages
        for page_name in ["main", "maintenance", "minimal", "tips"]:
            page = self.stack.get_child_by_name(page_name)
            if page and hasattr(page, 'cleanup'):
                page.cleanup()
        
        self.logger.info("Window cleanup completed")
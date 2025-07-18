"""
Juan - Maps Scraper & WhatsApp Blaster - Professional Edition
Main application entry point with tabbed interface, AI integration, and dark mode
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Import custom modules
from scraper_tab import ScraperTab
from whatsapp_tab import WhatsAppTab
from ai_tab import AITab
from settings_tab import SettingsTab
from language_manager import LanguageManager
from theme_manager import ThemeManager


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.language_manager = LanguageManager()
        self.theme_manager = ThemeManager()
        
        self.setup_window()
        self.apply_theme()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window properties"""
        self.root.title("Juan - Maps Scraper & WhatsApp Blaster v2.0")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configure window icon (if available)
        try:
            # You can add an icon file here
            pass
        except:
            pass
            
    def apply_theme(self):
        """Apply current theme to the application"""
        self.colors = self.theme_manager.apply_theme(self.root)
        
    def create_widgets(self):
        """Create the main interface widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header section
        self.create_header(main_frame)
        
        # Language and theme controls
        self.create_controls(main_frame)
        
        # Create notebook with tabs
        self.create_notebook(main_frame)
        
    def create_header(self, parent):
        """Create application header"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(0, weight=1)
        
        # Application title
        title_label = ttk.Label(
            header_frame, 
            text="Juan - Maps Scraper & WhatsApp Blaster",
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Professional Edition v2.0 - AI-Powered Business Data & Communication Tool",
            font=('Arial', 10, 'italic')
        )
        subtitle_label.grid(row=1, column=0)
        
    def create_controls(self, parent):
        """Create control section"""
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        controls_frame.columnconfigure(2, weight=1)
        
        # Language selector
        ttk.Label(controls_frame, text="Language:").grid(row=0, column=0, padx=(0, 5))
        
        self.language_var = tk.StringVar(value=self.language_manager.get_current_language())
        language_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.language_var,
            values=list(self.language_manager.get_available_languages().keys()),
            state="readonly",
            width=15
        )
        language_combo.grid(row=0, column=1, padx=(0, 20))
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Theme toggle button
        theme_text = "🌙 Dark" if not self.theme_manager.is_dark_mode() else "☀️ Light"
        self.theme_button = ttk.Button(
            controls_frame,
            text=f"Theme: {theme_text}",
            command=self.toggle_theme
        )
        self.theme_button.grid(row=0, column=3, padx=(20, 0))
        
    def create_notebook(self, parent):
        """Create notebook with all tabs"""
        # Create notebook
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure notebook styling
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[15, 8])
        
        # Create tabs
        try:
            # Google Maps Scraper Tab
            self.scraper_tab = ScraperTab(self.notebook, self.language_manager, self.theme_manager)
            
            # WhatsApp Blaster Tab  
            self.whatsapp_tab = WhatsAppTab(self.notebook, self.language_manager, self.theme_manager)
            
            # AI Message Generator Tab
            self.ai_tab = AITab(self.notebook, self.language_manager, self.theme_manager)
            
            # Settings Tab
            self.settings_tab = SettingsTab(self.notebook, self.language_manager, self.theme_manager)
            
        except Exception as e:
            error_msg = f"Error creating tabs: {str(e)}"
            messagebox.showerror("Initialization Error", error_msg)
            print(error_msg)
            
    def on_language_change(self, event=None):
        """Handle language change"""
        selected_language = self.language_var.get()
        self.language_manager.set_language(selected_language)
        
        # Update window title
        self.root.title(self.language_manager.get_text("app_title"))
        
        messagebox.showinfo(
            "Language Changed",
            "Language will be fully applied when you restart the application."
        )
        
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.theme_manager.toggle_dark_mode()
        
        # Update button text
        theme_text = "🌙 Dark" if not self.theme_manager.is_dark_mode() else "☀️ Light"
        self.theme_button.config(text=f"Theme: {theme_text}")
        
        messagebox.showinfo(
            "Theme Changed",
            "Theme will be fully applied when you restart the application."
        )
        
    def run(self):
        """Start the application"""
        try:
            # Set up error handling
            self.root.report_callback_exception = self.handle_exception
            
            # Start main loop
            self.root.mainloop()
            
        except Exception as e:
            error_msg = f"Application error: {str(e)}"
            print(error_msg)
            messagebox.showerror("Application Error", error_msg)
            
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        import traceback
        
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(f"Uncaught exception: {error_msg}")
        
        # Show user-friendly error message
        messagebox.showerror(
            "Unexpected Error",
            "An unexpected error occurred. Please check the console for details."
        )


def main():
    """Main entry point"""
    try:
        # Create and run application
        app = MainApplication()
        app.run()
        
    except Exception as e:
        error_msg = f"Failed to start application: {str(e)}"
        print(error_msg)
        
        # Try to show error with basic tkinter
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Startup Error", error_msg)
        except:
            print("Could not display error dialog")


if __name__ == "__main__":
    main()
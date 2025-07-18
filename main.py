"""
Juan - Maps Scraper & WhatsApp Blaster
Main application entry point with tabbed interface
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


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.language_manager = LanguageManager()
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window properties"""
        self.root.title("Juan - Maps Scraper & WhatsApp Blaster")
        self.root.geometry("950x750")
        self.root.minsize(850, 650)
        
        # Configure colors and style
        self.root.configure(bg='#f0f0f0')
        
        # Configure ttk style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom color scheme
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[20, 10])
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', foreground='#333333')
        style.configure('TButton', padding=[10, 5])
        
    def create_widgets(self):
        """Create the main interface widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Top frame for title and language selector
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        top_frame.columnconfigure(0, weight=1)
        
        # Application title
        title_label = ttk.Label(
            top_frame, 
            text="Juan - Maps Scraper & WhatsApp Blaster",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Language selector
        language_frame = ttk.Frame(top_frame)
        language_frame.grid(row=1, column=0, pady=(0, 10))
        
        ttk.Label(language_frame, text="Language:").grid(row=0, column=0, padx=(0, 5))
        
        self.language_var = tk.StringVar(value=self.language_manager.get_current_language())
        language_combo = ttk.Combobox(
            language_frame,
            textvariable=self.language_var,
            values=list(self.language_manager.get_available_languages().keys()),
            state="readonly",
            width=15
        )
        language_combo.grid(row=0, column=1)
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Create notebook with tabs
        self.create_notebook(main_frame)
        
    def create_notebook(self, parent):
        """Create notebook with all tabs"""
        # Create notebook
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        try:
            # Maps Scraper Tab
            self.scraper_tab = ScraperTab(self.notebook, self.language_manager)
            
            # WhatsApp Blaster Tab  
            self.whatsapp_tab = WhatsAppTab(self.notebook, self.language_manager)
            
            # AI Message Generator Tab
            self.ai_tab = AITab(self.notebook, self.language_manager)
            
            # Settings Tab
            self.settings_tab = SettingsTab(self.notebook, self.language_manager)
            
        except Exception as e:
            error_msg = f"Error creating tabs: {str(e)}"
            messagebox.showerror("Initialization Error", error_msg)
            print(error_msg)
            
    def on_language_change(self, event=None):
        """Handle language change"""
        selected_language = self.language_var.get()
        self.language_manager.set_language(selected_language)
        
        # Update all UI elements immediately
        self.update_ui_language()
        
    def update_ui_language(self):
        """Update all UI elements with new language"""
        # Update window title
        self.root.title(self.language_manager.get_text("app_title"))
        
        # Update tab names
        if hasattr(self, 'scraper_tab'):
            self.notebook.tab(self.scraper_tab.frame, text=self.language_manager.get_text("scraper_tab"))
        if hasattr(self, 'whatsapp_tab'):
            self.notebook.tab(self.whatsapp_tab.frame, text=self.language_manager.get_text("whatsapp_tab"))
        if hasattr(self, 'ai_tab'):
            self.notebook.tab(self.ai_tab.frame, text="AI Generator")
        if hasattr(self, 'settings_tab'):
            self.notebook.tab(self.settings_tab.frame, text="Settings")
        
        # Trigger update in each tab
        try:
            self.scraper_tab.update_language()
            self.whatsapp_tab.update_language()
        except:
            pass
        
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
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
from language_manager import LanguageManager

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.language_manager = LanguageManager()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window properties"""
        self.root.title(self.language_manager.get_text("app_title"))
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
            text=self.language_manager.get_text("app_title"),
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Language selector
        language_frame = ttk.Frame(top_frame)
        language_frame.grid(row=1, column=0, pady=(0, 10))
        
        ttk.Label(language_frame, text=self.language_manager.get_text("language") + ":").grid(row=0, column=0, padx=(0, 5))
        
        self.language_var = tk.StringVar(value=self.language_manager.get_current_language())
        language_combo = ttk.Combobox(
            language_frame,
            textvariable=self.language_var,
            values=list(self.language_manager.get_languages().keys()),
            state="readonly",
            width=10
        )
        language_combo.grid(row=0, column=1)
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Update combobox display values
        for i, (code, name) in enumerate(self.language_manager.get_languages().items()):
            language_combo.set(code)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and add tabs
        self.scraper_tab = ScraperTab(self.notebook, self.language_manager)
        self.whatsapp_tab = WhatsAppTab(self.notebook, self.language_manager)
        
        self.notebook.add(self.scraper_tab.frame, text=self.language_manager.get_text("scraper_tab"))
        self.notebook.add(self.whatsapp_tab.frame, text=self.language_manager.get_text("whatsapp_tab"))
        
    def on_language_change(self, event):
        """Handle language change"""
        new_language = self.language_var.get()
        self.language_manager.set_language(new_language)
        self.refresh_ui()
        
    def refresh_ui(self):
        """Refresh UI text with new language"""
        # Update window title
        self.root.title(self.language_manager.get_text("app_title"))
        
        # Update tab titles
        self.notebook.tab(0, text=self.language_manager.get_text("scraper_tab"))
        self.notebook.tab(1, text=self.language_manager.get_text("whatsapp_tab"))
        
        # Update tabs content
        self.scraper_tab.update_language()
        self.whatsapp_tab.update_language()
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            
    def on_closing(self):
        """Handle application closing"""
        try:
            # Clean up any running threads or processes
            if hasattr(self.scraper_tab, 'stop_scraping'):
                self.scraper_tab.stop_scraping()
            if hasattr(self.whatsapp_tab, 'stop_sending'):
                self.whatsapp_tab.stop_sending()
        except:
            pass
        finally:
            self.root.destroy()

def main():
    """Main entry point"""
    try:
        app = MainApplication()
        app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

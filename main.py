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

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window properties"""
        self.root.title("Juan - Maps Scraper & WhatsApp Blaster")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
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
        main_frame.rowconfigure(1, weight=1)
        
        # Application title
        title_label = ttk.Label(
            main_frame, 
            text="Juan - Maps Scraper & WhatsApp Blaster",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and add tabs
        self.scraper_tab = ScraperTab(self.notebook)
        self.whatsapp_tab = WhatsAppTab(self.notebook)
        
        self.notebook.add(self.scraper_tab.frame, text="Google Maps Scraper")
        self.notebook.add(self.whatsapp_tab.frame, text="WhatsApp Blaster")
        
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

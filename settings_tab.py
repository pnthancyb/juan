"""
Settings Tab
Handles application settings including Groq AI configuration and theme settings
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from groq_ai import GroqAI


class SettingsTab:
    def __init__(self, parent_notebook, language_manager, theme_manager):
        self.language_manager = language_manager
        self.theme_manager = theme_manager
        self.groq_ai = GroqAI()
        
        # Create the tab frame
        self.frame = ttk.Frame(parent_notebook, padding="20")
        parent_notebook.add(self.frame, text=self.language_manager.get_text("settings"))
        
        # Variables
        self.api_key_var = tk.StringVar()
        self.dark_mode_var = tk.BooleanVar(value=self.theme_manager.is_dark_mode())
        
        self.create_widgets()
        self.load_settings()
        
    def create_widgets(self):
        """Create settings interface"""
        # Main container with scrollbar
        canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Settings sections
        self.create_ai_settings(scrollable_frame)
        self.create_theme_settings(scrollable_frame)
        self.create_app_settings(scrollable_frame)
        self.create_credits_section(scrollable_frame)
        
    def create_ai_settings(self, parent):
        """Create AI settings section"""
        # AI Settings Section
        ai_frame = ttk.LabelFrame(parent, text="🤖 Groq AI Configuration", padding="15")
        ai_frame.pack(fill="x", pady=(0, 20))
        
        # API Key input
        ttk.Label(ai_frame, text="Groq API Key:", font=('Arial', 10, 'bold')).pack(anchor="w")
        ttk.Label(ai_frame, text="Get your free API key from: https://console.groq.com/keys", 
                 foreground="blue", font=('Arial', 8)).pack(anchor="w", pady=(0, 5))
        
        key_frame = ttk.Frame(ai_frame)
        key_frame.pack(fill="x", pady=(0, 10))
        
        self.api_key_entry = ttk.Entry(key_frame, textvariable=self.api_key_var, show="*", width=50)
        self.api_key_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Show/Hide key button
        self.show_key_var = tk.BooleanVar()
        show_key_btn = ttk.Checkbutton(
            key_frame, 
            text="Show", 
            variable=self.show_key_var,
            command=self.toggle_api_key_visibility
        )
        show_key_btn.pack(side="right")
        
        # API Key buttons
        btn_frame = ttk.Frame(ai_frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        save_key_btn = ttk.Button(
            btn_frame, 
            text="💾 Save API Key", 
            command=self.save_api_key
        )
        save_key_btn.pack(side="left", padx=(0, 10))
        
        test_key_btn = ttk.Button(
            btn_frame, 
            text="🧪 Test API Key", 
            command=self.test_api_key
        )
        test_key_btn.pack(side="left", padx=(0, 10))
        
        clear_key_btn = ttk.Button(
            btn_frame, 
            text="🗑️ Clear Key", 
            command=self.clear_api_key
        )
        clear_key_btn.pack(side="left")
        
        # Status indicator
        self.api_status_var = tk.StringVar(value="❌ Not configured")
        status_label = ttk.Label(ai_frame, textvariable=self.api_status_var, font=('Arial', 9))
        status_label.pack(anchor="w", pady=(5, 0))
        
        # AI Models info
        models_frame = ttk.LabelFrame(ai_frame, text="Available AI Personas", padding="10")
        models_frame.pack(fill="x", pady=(10, 0))
        
        personas_text = """
🏢 Official: Professional business communication with formal tone
🎯 Spam: High-converting direct marketing with urgency and action triggers  
💼 Marketer: Expert marketing messages with emotional triggers and storytelling
        """
        ttk.Label(models_frame, text=personas_text.strip(), justify="left").pack(anchor="w")
        
    def create_theme_settings(self, parent):
        """Create theme settings section"""
        theme_frame = ttk.LabelFrame(parent, text="🎨 Theme Settings", padding="15")
        theme_frame.pack(fill="x", pady=(0, 20))
        
        # Dark mode toggle
        dark_mode_frame = ttk.Frame(theme_frame)
        dark_mode_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(dark_mode_frame, text="Appearance:", font=('Arial', 10, 'bold')).pack(side="left")
        
        dark_mode_btn = ttk.Checkbutton(
            dark_mode_frame,
            text="🌙 Dark Mode",
            variable=self.dark_mode_var,
            command=self.toggle_dark_mode
        )
        dark_mode_btn.pack(side="left", padx=(20, 0))
        
        # Theme info
        theme_info = ttk.Label(
            theme_frame, 
            text="Dark mode provides a modern, eye-friendly interface for extended use.",
            font=('Arial', 8),
            foreground="gray"
        )
        theme_info.pack(anchor="w")
        
    def create_app_settings(self, parent):
        """Create application settings section"""
        app_frame = ttk.LabelFrame(parent, text="⚙️ Application Settings", padding="15")
        app_frame.pack(fill="x", pady=(0, 20))
        
        # Performance settings
        ttk.Label(app_frame, text="Performance:", font=('Arial', 10, 'bold')).pack(anchor="w")
        
        perf_info = ttk.Label(
            app_frame,
            text="• Chrome WebDriver: Required for real scraping and WhatsApp automation\n• Mock Mode: Uses simulated data when Chrome is not available\n• Smart Delays: Prevents rate limiting with adaptive timing",
            justify="left",
            font=('Arial', 8)
        )
        perf_info.pack(anchor="w", pady=(5, 10))
        
        # Reset button
        reset_btn = ttk.Button(
            app_frame,
            text="🔄 Reset All Settings",
            command=self.reset_settings
        )
        reset_btn.pack(anchor="w")
        
    def create_credits_section(self, parent):
        """Create credits section"""
        credits_frame = ttk.LabelFrame(parent, text="👨‍💻 Credits", padding="15")
        credits_frame.pack(fill="x", pady=(0, 20))
        
        # Credits title
        title_label = ttk.Label(
            credits_frame, 
            text="Juan - Maps Scraper & WhatsApp Blaster", 
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Credits list
        credits_text = """
🎬 Producer: Han
💻 Software Engineer: Han  
🔧 Integrator: Han
🎨 UI Designer: Han
🧠 AI Specialist: Han
🚀 Performance Optimizer: Han
📱 WhatsApp Expert: Han
🗺️ Maps Scraping Expert: Han
        """
        
        credits_label = ttk.Label(
            credits_frame,
            text=credits_text.strip(),
            justify="center",
            font=('Arial', 9)
        )
        credits_label.pack()
        
        # Version info
        version_label = ttk.Label(
            credits_frame,
            text="Version 2.0 - Professional Edition",
            font=('Arial', 8, 'italic'),
            foreground="gray"
        )
        version_label.pack(pady=(10, 0))
        
    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
            
    def save_api_key(self):
        """Save API key"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("Warning", "Please enter an API key")
            return
            
        # Set environment variable
        os.environ['GROQ_API_KEY'] = api_key
        self.groq_ai.set_api_key(api_key)
        
        # Update status
        if self.groq_ai.is_configured():
            self.api_status_var.set("✅ API Key saved")
            messagebox.showinfo("Success", "API key saved successfully!")
        else:
            self.api_status_var.set("❌ Failed to save")
            
    def test_api_key(self):
        """Test API key functionality"""
        if not self.groq_ai.is_configured():
            messagebox.showwarning("Warning", "Please save an API key first")
            return
            
        # Test with a simple request
        self.api_status_var.set("🧪 Testing...")
        
        try:
            result = self.groq_ai.generate_message(
                'official', 
                'Generate a simple greeting message', 
                'This is a test'
            )
            
            if result['success']:
                self.api_status_var.set("✅ API Key working")
                messagebox.showinfo(
                    "Success", 
                    f"API key is working!\n\nTest message generated:\n\"{result['message'][:100]}...\""
                )
            else:
                self.api_status_var.set("❌ API Key failed")
                messagebox.showerror("Error", f"API test failed:\n{result['error']}")
                
        except Exception as e:
            self.api_status_var.set("❌ Test failed")
            messagebox.showerror("Error", f"Test failed: {str(e)}")
            
    def clear_api_key(self):
        """Clear API key"""
        if messagebox.askyesno("Confirm", "Clear the saved API key?"):
            self.api_key_var.set("")
            if 'GROQ_API_KEY' in os.environ:
                del os.environ['GROQ_API_KEY']
            self.groq_ai.set_api_key("")
            self.api_status_var.set("❌ Not configured")
            messagebox.showinfo("Success", "API key cleared")
            
    def toggle_dark_mode(self):
        """Toggle dark mode"""
        self.theme_manager.toggle_dark_mode()
        messagebox.showinfo(
            "Theme Changed", 
            "Theme will be applied when you restart the application."
        )
        
    def reset_settings(self):
        """Reset all settings"""
        if messagebox.askyesno("Confirm Reset", "Reset all settings to default?"):
            self.clear_api_key()
            self.dark_mode_var.set(False)
            self.theme_manager.set_dark_mode(False)
            messagebox.showinfo("Success", "Settings reset to default")
            
    def load_settings(self):
        """Load saved settings"""
        # Load API key from environment
        api_key = os.getenv('GROQ_API_KEY', '')
        if api_key:
            self.api_key_var.set(api_key)
            self.groq_ai.set_api_key(api_key)
            self.api_status_var.set("✅ API Key loaded")
        
        # Load theme settings
        self.dark_mode_var.set(self.theme_manager.is_dark_mode())
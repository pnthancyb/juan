"""
Theme Manager
Handles dark mode and light mode themes for the application
"""

import tkinter as tk
from tkinter import ttk
import json
import os


class ThemeManager:
    def __init__(self):
        self.settings_file = "theme_settings.json"
        self.current_theme = "light"
        self.load_theme_settings()
        
        # Define color schemes
        self.themes = {
            'light': {
                'bg': '#f0f0f0',
                'fg': '#333333',
                'select_bg': '#0078d4',
                'select_fg': '#ffffff',
                'entry_bg': '#ffffff',
                'entry_fg': '#333333',
                'button_bg': '#e1e1e1',
                'button_fg': '#333333',
                'frame_bg': '#f0f0f0',
                'label_bg': '#f0f0f0',
                'label_fg': '#333333',
                'notebook_bg': '#f0f0f0',
                'scrollbar_bg': '#cccccc',
                'text_bg': '#ffffff',
                'text_fg': '#333333'
            },
            'dark': {
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'select_bg': '#0078d4',
                'select_fg': '#ffffff',
                'entry_bg': '#404040',
                'entry_fg': '#ffffff',
                'button_bg': '#404040',
                'button_fg': '#ffffff',
                'frame_bg': '#2b2b2b',
                'label_bg': '#2b2b2b',
                'label_fg': '#ffffff',
                'notebook_bg': '#2b2b2b',
                'scrollbar_bg': '#404040',
                'text_bg': '#404040',
                'text_fg': '#ffffff'
            }
        }
    
    def load_theme_settings(self):
        """Load theme settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get('theme', 'light')
        except Exception as e:
            print(f"Error loading theme settings: {e}")
            self.current_theme = 'light'
    
    def save_theme_settings(self):
        """Save theme settings to file"""
        try:
            settings = {'theme': self.current_theme}
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving theme settings: {e}")
    
    def get_current_theme(self):
        """Get current theme name"""
        return self.current_theme
    
    def is_dark_mode(self):
        """Check if current theme is dark mode"""
        return self.current_theme == 'dark'
    
    def set_dark_mode(self, enabled):
        """Set dark mode on/off"""
        self.current_theme = 'dark' if enabled else 'light'
        self.save_theme_settings()
    
    def toggle_dark_mode(self):
        """Toggle between dark and light mode"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.save_theme_settings()
    
    def get_colors(self):
        """Get color scheme for current theme"""
        return self.themes[self.current_theme]
    
    def apply_theme(self, root):
        """Apply theme to the application"""
        colors = self.get_colors()
        
        # Configure root window
        root.configure(bg=colors['bg'])
        
        # Configure ttk style
        style = ttk.Style()
        
        # Choose appropriate theme
        if self.current_theme == 'dark':
            try:
                style.theme_use('clam')
            except:
                style.theme_use('default')
        else:
            try:
                style.theme_use('clam')
            except:
                style.theme_use('default')
        
        # Configure ttk widgets
        style.configure('TFrame', background=colors['frame_bg'])
        style.configure('TLabel', background=colors['label_bg'], foreground=colors['label_fg'])
        style.configure('TButton', background=colors['button_bg'], foreground=colors['button_fg'])
        style.configure('TEntry', fieldbackground=colors['entry_bg'], foreground=colors['entry_fg'])
        style.configure('TText', fieldbackground=colors['text_bg'], foreground=colors['text_fg'])
        style.configure('TNotebook', background=colors['notebook_bg'])
        style.configure('TNotebook.Tab', background=colors['button_bg'], foreground=colors['button_fg'])
        style.configure('TLabelFrame', background=colors['frame_bg'], foreground=colors['label_fg'])
        style.configure('TCheckbutton', background=colors['frame_bg'], foreground=colors['label_fg'])
        style.configure('TRadiobutton', background=colors['frame_bg'], foreground=colors['label_fg'])
        style.configure('TSpinbox', fieldbackground=colors['entry_bg'], foreground=colors['entry_fg'])
        style.configure('TCombobox', fieldbackground=colors['entry_bg'], foreground=colors['entry_fg'])
        style.configure('TScale', background=colors['frame_bg'])
        style.configure('TProgressbar', background=colors['select_bg'])
        
        # Configure scrollbar
        style.configure('TScrollbar', 
                       background=colors['scrollbar_bg'],
                       darkcolor=colors['scrollbar_bg'],
                       lightcolor=colors['scrollbar_bg'],
                       troughcolor=colors['bg'],
                       bordercolor=colors['scrollbar_bg'],
                       arrowcolor=colors['fg'])
        
        # Map widget states
        style.map('TButton',
                 background=[('active', colors['select_bg']),
                           ('pressed', colors['select_bg'])],
                 foreground=[('active', colors['select_fg']),
                           ('pressed', colors['select_fg'])])
        
        style.map('TEntry',
                 focuscolor=[('!focus', colors['select_bg'])])
        
        style.map('TNotebook.Tab',
                 background=[('selected', colors['select_bg']),
                           ('active', colors['button_bg'])],
                 foreground=[('selected', colors['select_fg']),
                           ('active', colors['button_fg'])])
        
        return colors
    
    def configure_text_widget(self, text_widget):
        """Configure text widget with current theme"""
        colors = self.get_colors()
        text_widget.configure(
            bg=colors['text_bg'],
            fg=colors['text_fg'],
            insertbackground=colors['fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg']
        )
    
    def configure_listbox(self, listbox):
        """Configure listbox with current theme"""
        colors = self.get_colors()
        listbox.configure(
            bg=colors['text_bg'],
            fg=colors['text_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg']
        )
    
    def configure_canvas(self, canvas):
        """Configure canvas with current theme"""
        colors = self.get_colors()
        canvas.configure(bg=colors['bg'])
"""
AI Message Generator Tab
Handles AI-powered message generation using Groq AI with multiple personas
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from groq_ai import GroqAI


class AITab:
    def __init__(self, parent_notebook, language_manager, theme_manager):
        self.language_manager = language_manager
        self.theme_manager = theme_manager
        self.groq_ai = GroqAI()
        
        # Create the tab frame
        self.frame = ttk.Frame(parent_notebook, padding="20")
        parent_notebook.add(self.frame, text="🤖 AI Generator")
        
        # Variables
        self.persona_var = tk.StringVar(value="official")
        self.request_var = tk.StringVar()
        self.context_var = tk.StringVar()
        self.generated_message_var = tk.StringVar()
        self.is_generating = False
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create AI message generator interface"""
        # Main container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill="both", expand=True)
        
        # Configure grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Header section
        self.create_header(main_container)
        
        # Input section
        self.create_input_section(main_container)
        
        # Output section
        self.create_output_section(main_container)
        
        # Control buttons
        self.create_control_buttons(main_container)
        
    def create_header(self, parent):
        """Create header section"""
        header_frame = ttk.LabelFrame(parent, text="🤖 AI Message Generator", padding="15")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        # Description
        desc_text = """Generate professional messages using AI personas:
🏢 Official - Professional business communication
🎯 Spam - High-converting direct marketing  
💼 Marketer - Expert marketing with storytelling"""
        
        ttk.Label(header_frame, text=desc_text, justify="left").pack(anchor="w")
        
        # Persona selection
        persona_frame = ttk.Frame(header_frame)
        persona_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(persona_frame, text="AI Persona:", font=('Arial', 10, 'bold')).pack(side="left")
        
        # Persona radio buttons
        personas = [
            ("official", "🏢 Official"),
            ("spam", "🎯 Spam Expert"),
            ("marketer", "💼 Marketer")
        ]
        
        for value, text in personas:
            ttk.Radiobutton(
                persona_frame,
                text=text,
                variable=self.persona_var,
                value=value
            ).pack(side="left", padx=(20, 0))
        
    def create_input_section(self, parent):
        """Create input section"""
        input_frame = ttk.LabelFrame(parent, text="📝 Message Request", padding="15")
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        
        # Request input
        ttk.Label(input_frame, text="What message do you need?", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 5)
        )
        
        self.request_entry = ttk.Entry(input_frame, textvariable=self.request_var, width=60)
        self.request_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Context input
        ttk.Label(input_frame, text="Additional context (optional):", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(0, 5)
        )
        
        self.context_entry = ttk.Entry(input_frame, textvariable=self.context_var, width=60)
        self.context_entry.grid(row=3, column=0, columnspan=2, sticky="ew")
        
        # Examples
        examples_text = """💡 Examples:
• "Create a welcome message for new customers"
• "Write a promotion for 50% off sale ending tomorrow"  
• "Generate a follow-up message for interested prospects"
• "Create an appointment reminder message"
        """
        
        examples_label = ttk.Label(input_frame, text=examples_text, justify="left", font=('Arial', 8))
        examples_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
    def create_output_section(self, parent):
        """Create output section"""
        output_frame = ttk.LabelFrame(parent, text="✨ Generated Message", padding="15")
        output_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to generate messages")
        status_label = ttk.Label(output_frame, textvariable=self.status_var, font=('Arial', 9))
        status_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Generated message display
        self.message_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            width=80,
            wrap=tk.WORD,
            font=('Arial', 11)
        )
        self.message_text.grid(row=1, column=0, sticky="nsew")
        
        # Apply theme to text widget
        self.theme_manager.configure_text_widget(self.message_text)
        
        # Message stats
        self.stats_var = tk.StringVar(value="Character count: 0")
        stats_label = ttk.Label(output_frame, textvariable=self.stats_var, font=('Arial', 8))
        stats_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
        
    def create_control_buttons(self, parent):
        """Create control buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, sticky="ew")
        
        # Generate button
        self.generate_button = ttk.Button(
            button_frame,
            text="🚀 Generate Message",
            command=self.generate_message
        )
        self.generate_button.pack(side="left", padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹️ Stop",
            command=self.stop_generation,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=(0, 10))
        
        # Copy button
        copy_button = ttk.Button(
            button_frame,
            text="📋 Copy Message",
            command=self.copy_message
        )
        copy_button.pack(side="left", padx=(0, 10))
        
        # Clear button
        clear_button = ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_output
        )
        clear_button.pack(side="left", padx=(0, 10))
        
        # Use in WhatsApp button
        use_button = ttk.Button(
            button_frame,
            text="📱 Use in WhatsApp",
            command=self.use_in_whatsapp
        )
        use_button.pack(side="right")
        
    def generate_message(self):
        """Generate message using AI"""
        if self.is_generating:
            return
            
        # Validate inputs
        request = self.request_var.get().strip()
        if not request:
            messagebox.showwarning("Warning", "Please enter a message request")
            return
            
        # Check if API is configured
        if not self.groq_ai.is_configured():
            messagebox.showwarning(
                "API Key Required", 
                "Please configure your Groq API key in the Settings tab first."
            )
            return
        
        # Start generation in thread
        self.is_generating = True
        self.generate_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_var.set("🤖 Generating message...")
        
        # Clear previous output
        self.message_text.delete(1.0, tk.END)
        self.stats_var.set("Generating...")
        
        # Start worker thread
        self.generation_thread = threading.Thread(
            target=self._generation_worker,
            args=(self.persona_var.get(), request, self.context_var.get()),
            daemon=True
        )
        self.generation_thread.start()
        
    def _generation_worker(self, persona, request, context):
        """Worker thread for message generation"""
        try:
            result = self.groq_ai.generate_message(persona, request, context)
            
            # Update UI in main thread
            self.frame.after(0, self._generation_finished, result)
            
        except Exception as e:
            error_result = {
                'success': False,
                'message': '',
                'error': f'Generation failed: {str(e)}'
            }
            self.frame.after(0, self._generation_finished, error_result)
            
    def _generation_finished(self, result):
        """Handle generation completion"""
        self.is_generating = False
        self.generate_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
        if result['success']:
            # Display generated message
            message = result['message']
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(1.0, message)
            
            # Update stats
            char_count = len(message)
            word_count = len(message.split())
            self.stats_var.set(f"Characters: {char_count} | Words: {word_count}")
            
            # Update status
            persona_name = result.get('persona', 'AI')
            tokens_used = result.get('tokens_used', 0)
            self.status_var.set(f"✅ Generated by {persona_name} | Tokens used: {tokens_used}")
            
        else:
            # Display error
            error_msg = result['error']
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(1.0, f"❌ Error: {error_msg}")
            self.status_var.set("❌ Generation failed")
            self.stats_var.set("Error occurred")
            
    def stop_generation(self):
        """Stop message generation"""
        self.is_generating = False
        self.generate_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_var.set("⏹️ Generation stopped")
        
    def copy_message(self):
        """Copy generated message to clipboard"""
        message = self.message_text.get(1.0, tk.END).strip()
        if message:
            self.frame.clipboard_clear()
            self.frame.clipboard_append(message)
            self.status_var.set("📋 Message copied to clipboard")
            messagebox.showinfo("Success", "Message copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No message to copy")
            
    def clear_output(self):
        """Clear output area"""
        self.message_text.delete(1.0, tk.END)
        self.stats_var.set("Character count: 0")
        self.status_var.set("Ready to generate messages")
        
    def use_in_whatsapp(self):
        """Use generated message in WhatsApp tab"""
        message = self.message_text.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "No message to use")
            return
            
        # Try to find WhatsApp tab and set message
        try:
            # Get parent notebook
            notebook = self.frame.master
            
            # Find WhatsApp tab
            for tab_id in notebook.tabs():
                tab_text = notebook.tab(tab_id, "text")
                if "WhatsApp" in tab_text:
                    # Switch to WhatsApp tab
                    notebook.select(tab_id)
                    
                    # Get the WhatsApp tab widget
                    whatsapp_frame = notebook.nametowidget(tab_id)
                    
                    # Find message text widget and set message
                    for widget in whatsapp_frame.winfo_children():
                        if hasattr(widget, 'message_text') and hasattr(widget.message_text, 'delete'):
                            widget.message_text.delete(1.0, tk.END)
                            widget.message_text.insert(1.0, message)
                            messagebox.showinfo("Success", "Message added to WhatsApp tab!")
                            return
                    
            messagebox.showinfo("Info", "WhatsApp tab not found. Message copied to clipboard instead.")
            self.copy_message()
            
        except Exception as e:
            print(f"Error using message in WhatsApp: {e}")
            messagebox.showinfo("Info", "Message copied to clipboard instead.")
            self.copy_message()
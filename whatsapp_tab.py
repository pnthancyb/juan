"""
WhatsApp Blaster Tab
Handles bulk messaging interface and functionality
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import csv
import re
from datetime import datetime

from data_processor import DataProcessor
from utils import format_duration, validate_phone_number

class WhatsAppTab:
    def __init__(self, parent):
        self.parent = parent
        self.data_processor = DataProcessor()
        self.is_sending = False
        self.phone_numbers = []
        self.valid_numbers = []
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the WhatsApp tab interface"""
        self.frame = ttk.Frame(self.parent, padding="20")
        
        # Configure grid weights
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(6, weight=1)
        
        # CSV Import section
        import_frame = ttk.LabelFrame(self.frame, text="Phone Numbers Import", padding="10")
        import_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        import_frame.columnconfigure(1, weight=1)
        
        ttk.Label(import_frame, text="CSV File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.csv_path_var = tk.StringVar()
        self.csv_entry = ttk.Entry(import_frame, textvariable=self.csv_path_var, state="readonly")
        self.csv_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(
            import_frame, 
            text="Browse CSV", 
            command=self.browse_csv_file
        ).grid(row=0, column=2, padx=(0, 10))
        
        ttk.Button(
            import_frame, 
            text="Load Numbers", 
            command=self.load_phone_numbers
        ).grid(row=0, column=3)
        
        # Phone validation section
        validation_frame = ttk.LabelFrame(self.frame, text="Phone Validation", padding="10")
        validation_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        validation_frame.columnconfigure(1, weight=1)
        
        ttk.Label(validation_frame, text="Total Numbers:").grid(row=0, column=0, sticky=tk.W)
        self.total_numbers_var = tk.StringVar(value="0")
        ttk.Label(validation_frame, textvariable=self.total_numbers_var).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(validation_frame, text="Valid Numbers:").grid(row=1, column=0, sticky=tk.W)
        self.valid_numbers_var = tk.StringVar(value="0")
        ttk.Label(validation_frame, textvariable=self.valid_numbers_var, foreground="green").grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(validation_frame, text="Invalid Numbers:").grid(row=2, column=0, sticky=tk.W)
        self.invalid_numbers_var = tk.StringVar(value="0")
        ttk.Label(validation_frame, textvariable=self.invalid_numbers_var, foreground="red").grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Button(
            validation_frame, 
            text="Validate Numbers", 
            command=self.validate_numbers
        ).grid(row=0, column=2, rowspan=3, padx=(20, 0))
        
        # Message template section
        message_frame = ttk.LabelFrame(self.frame, text="Message Template", padding="10")
        message_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        message_frame.columnconfigure(0, weight=1)
        message_frame.rowconfigure(1, weight=1)
        
        ttk.Label(message_frame, text="Message Content:").grid(row=0, column=0, sticky=tk.W)
        
        # Message text area
        text_frame = ttk.Frame(message_frame)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.message_text = tk.Text(
            text_frame, 
            height=6, 
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.message_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        message_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.message_text.yview)
        message_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.message_text.configure(yscrollcommand=message_scrollbar.set)
        
        # Insert default message
        default_message = "Hello! This is a business inquiry message. Please let me know if you're interested in our services."
        self.message_text.insert(1.0, default_message)
        
        # Sending controls section
        controls_frame = ttk.LabelFrame(self.frame, text="Sending Controls", padding="10")
        controls_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        controls_grid = ttk.Frame(controls_frame)
        controls_grid.grid(row=0, column=0)
        
        self.send_button = ttk.Button(
            controls_grid, 
            text="Start Sending", 
            command=self.start_sending,
            style="Accent.TButton"
        )
        self.send_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_send_button = ttk.Button(
            controls_grid, 
            text="Stop Sending", 
            command=self.stop_sending,
            state="disabled"
        )
        self.stop_send_button.grid(row=0, column=1, padx=(0, 10))
        
        # Delay settings
        ttk.Label(controls_grid, text="Delay (seconds):").grid(row=0, column=2, padx=(20, 5))
        self.delay_var = tk.StringVar(value="5")
        delay_spinbox = ttk.Spinbox(
            controls_grid, 
            from_=1, 
            to=60, 
            width=5, 
            textvariable=self.delay_var
        )
        delay_spinbox.grid(row=0, column=3)
        
        # Sending status section
        status_frame = ttk.LabelFrame(self.frame, text="Sending Status", padding="10")
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        self.send_status_var = tk.StringVar(value="Ready")
        ttk.Label(status_frame, textvariable=self.send_status_var).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(status_frame, text="Progress:").grid(row=1, column=0, sticky=tk.W)
        self.send_progress_var = tk.StringVar(value="0 / 0")
        ttk.Label(status_frame, textvariable=self.send_progress_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Progress bar for sending
        self.send_progress_bar_var = tk.DoubleVar()
        self.send_progress_bar = ttk.Progressbar(
            status_frame, 
            variable=self.send_progress_bar_var, 
            mode='determinate'
        )
        self.send_progress_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status log
        log_frame = ttk.LabelFrame(self.frame, text="Status Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text widget with scrollbar
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_text_frame.columnconfigure(0, weight=1)
        log_text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(
            log_text_frame, 
            height=10, 
            wrap=tk.WORD,
            bg='#f8f8f8',
            font=('Arial', 9)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Clear log button
        ttk.Button(
            log_frame, 
            text="Clear Log", 
            command=self.clear_log
        ).grid(row=1, column=0, pady=(10, 0))
        
    def browse_csv_file(self):
        """Browse for CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_path_var.set(file_path)
            
    def load_phone_numbers(self):
        """Load phone numbers from CSV file"""
        csv_file = self.csv_path_var.get()
        
        if not csv_file:
            messagebox.showwarning("Warning", "Please select a CSV file first")
            return
            
        try:
            self.phone_numbers = []
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                
                for row in csv_reader:
                    # Look for phone number in common column names
                    phone = None
                    for col in ['Phone', 'phone', 'Phone Number', 'phone_number', 'PhoneNumber']:
                        if col in row and row[col]:
                            phone = row[col]
                            break
                            
                    if phone:
                        self.phone_numbers.append(phone.strip())
                        
            self.total_numbers_var.set(str(len(self.phone_numbers)))
            self.valid_numbers_var.set("0")
            self.invalid_numbers_var.set("0")
            
            self.log_message(f"Loaded {len(self.phone_numbers)} phone numbers from CSV")
            
            if self.phone_numbers:
                messagebox.showinfo("Success", f"Loaded {len(self.phone_numbers)} phone numbers")
            else:
                messagebox.showwarning("Warning", "No phone numbers found in the CSV file")
                
        except Exception as e:
            error_msg = f"Failed to load CSV file: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def validate_numbers(self):
        """Validate loaded phone numbers"""
        if not self.phone_numbers:
            messagebox.showwarning("Warning", "No phone numbers loaded")
            return
            
        self.valid_numbers = []
        invalid_count = 0
        
        for phone in self.phone_numbers:
            if validate_phone_number(phone):
                # Clean and format the number
                cleaned = re.sub(r'[^\d+]', '', phone)
                self.valid_numbers.append(cleaned)
            else:
                invalid_count += 1
                
        self.valid_numbers_var.set(str(len(self.valid_numbers)))
        self.invalid_numbers_var.set(str(invalid_count))
        
        self.log_message(f"Validation complete: {len(self.valid_numbers)} valid, {invalid_count} invalid")
        
        if self.valid_numbers:
            messagebox.showinfo("Validation Complete", f"Found {len(self.valid_numbers)} valid phone numbers")
        else:
            messagebox.showwarning("Validation Complete", "No valid phone numbers found")
            
    def start_sending(self):
        """Start the message sending process"""
        if not self.valid_numbers:
            messagebox.showwarning("Warning", "No valid phone numbers available")
            return
            
        message = self.message_text.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message")
            return
            
        # Confirm sending
        result = messagebox.askyesno(
            "Confirm Sending", 
            f"Send message to {len(self.valid_numbers)} phone numbers?\n\nThis will simulate the sending process."
        )
        
        if not result:
            return
            
        # Start sending
        self.is_sending = True
        
        # Update UI
        self.send_button.configure(state="disabled")
        self.stop_send_button.configure(state="normal")
        self.send_status_var.set("Sending...")
        self.send_progress_bar_var.set(0)
        
        self.log_message(f"Starting to send messages to {len(self.valid_numbers)} numbers")
        
        # Start sending thread
        self.sending_thread = threading.Thread(
            target=self._sending_worker, 
            args=(self.valid_numbers, message),
            daemon=True
        )
        self.sending_thread.start()
        
    def _sending_worker(self, numbers, message):
        """Worker thread for sending messages"""
        try:
            total_numbers = len(numbers)
            delay = int(self.delay_var.get())
            sent_count = 0
            
            for i, number in enumerate(numbers):
                if not self.is_sending:
                    break
                    
                # Simulate sending message
                self.log_message(f"Sending message to {number}")
                
                # Simulate processing delay
                time.sleep(delay)
                
                sent_count += 1
                
                # Update progress
                progress = ((i + 1) / total_numbers) * 100
                self.send_progress_bar_var.set(progress)
                self.send_progress_var.set(f"{sent_count} / {total_numbers}")
                
                self.log_message(f"Message sent to {number} successfully")
                
            if self.is_sending:
                self.log_message(f"Sending completed. {sent_count} messages sent.")
                self.send_status_var.set("Completed")
            else:
                self.log_message("Sending stopped by user.")
                self.send_status_var.set("Stopped")
                
        except Exception as e:
            self.log_message(f"Error during sending: {str(e)}")
            self.send_status_var.set("Error")
        finally:
            # Update UI
            self.frame.after(0, self._sending_finished)
            
    def _sending_finished(self):
        """Handle sending completion"""
        self.is_sending = False
        self.send_button.configure(state="normal")
        self.stop_send_button.configure(state="disabled")
        
    def stop_sending(self):
        """Stop the sending process"""
        self.is_sending = False
        self.log_message("Stopping message sending...")
        
    def log_message(self, message):
        """Add message to status log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.log_text.update()
        
    def clear_log(self):
        """Clear the status log"""
        self.log_text.delete(1.0, tk.END)

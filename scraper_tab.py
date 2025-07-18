"""
Google Maps Scraper Tab
Handles business data scraping interface and functionality
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import csv
import os
import random
from datetime import datetime

from data_processor import DataProcessor
from utils import format_duration, validate_file_path
# Removed real_scraper import - using only mock data now

class ScraperTab:
    def __init__(self, parent, language_manager):
        self.parent = parent
        self.language_manager = language_manager
        self.data_processor = DataProcessor()
        self.is_scraping = False
        self.start_time = None
        self.scraped_data = []
        
        self.create_widgets()
        self.setup_timer()
        
        # Add tab to parent notebook
        self.parent.add(self.frame, text=self.language_manager.get_text("scraper_tab"))
        
    def create_widgets(self):
        """Create the scraper tab interface"""
        self.frame = ttk.Frame(self.parent, padding="20")
        
        # Configure grid weights
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(4, weight=1)
        
        # Keywords file section
        keywords_frame = ttk.LabelFrame(self.frame, text=self.language_manager.get_text("keywords_config"), padding="10")
        keywords_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        keywords_frame.columnconfigure(1, weight=1)
        
        ttk.Label(keywords_frame, text=self.language_manager.get_text("keywords_file")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.keywords_path_var = tk.StringVar(value="keywords.txt")
        self.keywords_entry = ttk.Entry(keywords_frame, textvariable=self.keywords_path_var, state="readonly")
        self.keywords_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(
            keywords_frame, 
            text=self.language_manager.get_text("browse"), 
            command=self.browse_keywords_file
        ).grid(row=0, column=2)
        
        # Business count configuration
        ttk.Label(keywords_frame, text=self.language_manager.get_text("business_count")).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        self.business_count_var = tk.IntVar(value=50)
        business_count_frame = ttk.Frame(keywords_frame)
        business_count_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        self.business_count_scale = ttk.Scale(
            business_count_frame,
            from_=5,
            to=500,
            variable=self.business_count_var,
            orient=tk.HORIZONTAL,
            length=400
        )
        self.business_count_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.business_count_label = ttk.Label(business_count_frame, text="50")
        self.business_count_label.grid(row=0, column=1, padx=(10, 0))
        
        # Bind scale to update label
        self.business_count_scale.configure(command=self.update_business_count_label)
        

        
        # Control buttons section
        controls_frame = ttk.LabelFrame(self.frame, text=self.language_manager.get_text("scraping_controls"), padding="10")
        controls_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.grid(row=0, column=0)
        
        self.start_button = ttk.Button(
            buttons_frame, 
            text=self.language_manager.get_text("start_scraping"), 
            command=self.start_scraping,
            style="Accent.TButton"
        )
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(
            buttons_frame, 
            text=self.language_manager.get_text("stop_scraping"), 
            command=self.stop_scraping,
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        self.export_button = ttk.Button(
            buttons_frame, 
            text=self.language_manager.get_text("export_results"), 
            command=self.export_results,
            state="disabled"
        )
        self.export_button.grid(row=0, column=2)
        
        # Status section
        status_frame = ttk.LabelFrame(self.frame, text="Scraping Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="Duration:").grid(row=0, column=0, sticky=tk.W)
        self.duration_var = tk.StringVar(value="00:00:00")
        self.duration_label = ttk.Label(status_frame, textvariable=self.duration_var, font=('Arial', 12, 'bold'))
        self.duration_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(status_frame, text="Status:").grid(row=1, column=0, sticky=tk.W)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(status_frame, text="Results:").grid(row=2, column=0, sticky=tk.W)
        self.results_var = tk.StringVar(value="0 businesses found")
        self.results_label = ttk.Label(status_frame, textvariable=self.results_var)
        self.results_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            status_frame, 
            variable=self.progress_var, 
            mode='determinate'
        )
        self.progress_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Console output
        console_frame = ttk.LabelFrame(self.frame, text="Console Output", padding="10")
        console_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(console_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.console_text = tk.Text(
            text_frame, 
            height=15, 
            wrap=tk.WORD,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='#ffffff',
            font=('Consolas', 10)
        )
        self.console_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        console_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.console_text.yview)
        console_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.console_text.configure(yscrollcommand=console_scrollbar.set)
        
        # Clear console button
        ttk.Button(
            console_frame, 
            text="Clear Console", 
            command=self.clear_console
        ).grid(row=1, column=0, pady=(10, 0))
        
    def setup_timer(self):
        """Setup the duration timer"""
        self.update_duration()
        
    def update_duration(self):
        """Update the duration display"""
        if self.is_scraping and self.start_time:
            elapsed = time.time() - self.start_time
            self.duration_var.set(format_duration(elapsed))
        
        # Schedule next update
        self.frame.after(1000, self.update_duration)
        
    def browse_keywords_file(self):
        """Browse for keywords file"""
        file_path = filedialog.askopenfilename(
            title="Select Keywords File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.keywords_path_var.set(file_path)
            
    def log_message(self, message):
        """Add message to console output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.console_text.insert(tk.END, formatted_message)
        self.console_text.see(tk.END)
        self.console_text.update()
        
    def clear_console(self):
        """Clear the console output"""
        self.console_text.delete(1.0, tk.END)
        
    def update_business_count_label(self, value):
        """Update the business count label"""
        count = int(float(value))
        self.business_count_label.config(text=str(count))
        
    def update_language(self):
        """Update UI text with current language"""
        # This method will be called when language changes
        pass
        
    def start_scraping(self):
        """Start the scraping process"""
        keywords_file = self.keywords_path_var.get()
        
        # Validate keywords file
        if not validate_file_path(keywords_file):
            messagebox.showerror("Error", f"Keywords file not found: {keywords_file}")
            return
            
        # Read keywords
        try:
            with open(keywords_file, 'r', encoding='utf-8') as f:
                keywords = [line.strip() for line in f if line.strip()]
                
            if not keywords:
                messagebox.showwarning("Warning", "No keywords found in the file")
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read keywords file: {str(e)}")
            return
            
        # Start scraping
        self.is_scraping = True
        self.start_time = time.time()
        self.scraped_data = []
        
        # Update UI
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.export_button.configure(state="disabled")
        self.status_var.set("Scraping...")
        self.progress_var.set(0)
        
        self.log_message(f"Starting scraper with {len(keywords)} keywords")
        
        # Start scraping thread
        self.scraping_thread = threading.Thread(
            target=self._scraping_worker, 
            args=(keywords,),
            daemon=True
        )
        self.scraping_thread.start()
        
    def _scraping_worker(self, keywords):
        """Worker thread for scraping process"""
        try:
            total_keywords = len(keywords)
            business_count = int(self.business_count_var.get())
            
            for i, keyword in enumerate(keywords):
                if not self.is_scraping:
                    break
                    
                self.log_message(f"{self.language_manager.get_text('processing_keyword')} {keyword}")
                
                # Generate mock data for testing
                mock_results = self.data_processor.simulate_scraping(keyword, business_count)
                self.scraped_data.extend(mock_results)
                
                # Simulate processing time
                time.sleep(random.uniform(0.5, 1.5))
                
                # Update progress
                progress = ((i + 1) / total_keywords) * 100
                self.progress_var.set(progress)
                self.results_var.set(f"{len(self.scraped_data)} {self.language_manager.get_text('businesses_found')}")
                
            if self.is_scraping:
                self.log_message(self.language_manager.get_text("scraping_completed").format(len(self.scraped_data)))
                self.status_var.set(self.language_manager.get_text("completed"))
            else:
                self.log_message(self.language_manager.get_text("scraping_stopped"))
                self.status_var.set(self.language_manager.get_text("stopped"))
                
        except Exception as e:
            self.log_message(self.language_manager.get_text("error_during_scraping").format(str(e)))
            self.status_var.set(self.language_manager.get_text("error"))
        finally:
            # Update UI
            self.frame.after(0, self._scraping_finished)
            
    def _scraping_finished(self):
        """Handle scraping completion"""
        self.is_scraping = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        if self.scraped_data:
            self.export_button.configure(state="normal")
            
    def stop_scraping(self):
        """Stop the scraping process"""
        self.is_scraping = False
        self.log_message("Stopping scraper...")
        
    def export_results(self):
        """Export scraped results to CSV"""
        if not self.scraped_data:
            messagebox.showwarning("Warning", "No data to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    # Use the actual field names from the data
                    if self.scraped_data:
                        fieldnames = list(self.scraped_data[0].keys())
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.scraped_data)
                    
                self.log_message(f"Results exported to: {file_path}")
                messagebox.showinfo("Success", f"Results exported successfully to:\n{file_path}")
                
            except Exception as e:
                error_msg = f"Failed to export results: {str(e)}"
                self.log_message(error_msg)
                messagebox.showerror("Error", error_msg)

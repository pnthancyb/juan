"""
WhatsApp Web Automation
Handles real WhatsApp Web messaging using Chrome WebDriver
"""

import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import undetected_chromedriver as uc
from typing import List, Dict, Optional, Callable

class WhatsAppAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.is_sending = False
        self.smart_delay = SmartWhatsAppDelay()
        
    def setup_driver(self, headless=False):
        """Setup Chrome WebDriver for WhatsApp Web"""
        try:
            # Check if Chrome is available
            import subprocess
            try:
                subprocess.run(['google-chrome', '--version'], capture_output=True, check=True)
                chrome_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                chrome_available = False
            
            if not chrome_available:
                print("Chrome browser not found. Please install Chrome for WhatsApp Web automation.")
                return False
            
            chrome_options = Options()
            
            # WhatsApp Web requires a visible browser for QR code scanning
            if not headless:
                chrome_options.add_argument("--start-maximized")
            else:
                chrome_options.add_argument("--headless=new")
                
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Add user data directory to persist login
            chrome_options.add_argument("--user-data-dir=./chrome_profile")
            
            # Try to use undetected-chromedriver, fall back to regular webdriver
            try:
                self.driver = uc.Chrome(options=chrome_options)
            except Exception as e:
                print(f"Failed to use undetected-chromedriver: {e}")
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.driver.set_window_size(1920, 1080)
            
            # Set up WebDriverWait
            self.wait = WebDriverWait(self.driver, 30)
            
            return True
            
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            return False
    
    def open_whatsapp_web(self, progress_callback: Optional[Callable] = None):
        """Open WhatsApp Web and wait for login"""
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            if progress_callback:
                progress_callback("Opening WhatsApp Web...")
            
            # Navigate to WhatsApp Web
            self.driver.get("https://web.whatsapp.com")
            
            if progress_callback:
                progress_callback("Waiting for WhatsApp Web to load...")
            
            # Wait for either QR code or chat interface
            try:
                # Check if already logged in
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-ref]"))  # QR code
                    )
                )
                
                # Check if QR code is present
                qr_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-ref]")
                if qr_elements:
                    if progress_callback:
                        progress_callback("Please scan QR code in the opened Chrome window to login to WhatsApp Web")
                    
                    # Wait for login completion
                    self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']"))
                    )
                
                if progress_callback:
                    progress_callback("WhatsApp Web logged in successfully!")
                
                return True
                
            except TimeoutException:
                if progress_callback:
                    progress_callback("Timeout waiting for WhatsApp Web login")
                return False
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error opening WhatsApp Web: {e}")
            return False
    
    def send_message(self, phone_number: str, message: str, progress_callback: Optional[Callable] = None) -> bool:
        """Send message to a phone number"""
        if not self.driver:
            return False
        
        try:
            # Clean phone number
            clean_phone = re.sub(r'[^\d+]', '', phone_number)
            
            if progress_callback:
                progress_callback(f"Sending message to {clean_phone}")
            
            # Create WhatsApp Web URL with phone number
            url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={message}"
            self.driver.get(url)
            
            # Wait for chat to load
            time.sleep(3)
            
            # Look for send button
            send_button = None
            try:
                # Try different selectors for send button
                send_selectors = [
                    "[data-testid='send']",
                    "[data-icon='send']",
                    "button[aria-label*='Send']",
                    "span[data-icon='send']"
                ]
                
                for selector in send_selectors:
                    try:
                        send_button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        break
                    except TimeoutException:
                        continue
                
                if send_button:
                    send_button.click()
                    
                    if progress_callback:
                        progress_callback(f"Message sent to {clean_phone}")
                    
                    # Smart delay to avoid rate limiting
                    delay = self.smart_delay.get_smart_delay()
                    time.sleep(delay)
                    
                    return True
                else:
                    if progress_callback:
                        progress_callback(f"Could not find send button for {clean_phone}")
                    return False
                    
            except TimeoutException:
                if progress_callback:
                    progress_callback(f"Timeout sending message to {clean_phone}")
                return False
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error sending message to {phone_number}: {e}")
            return False
    
    def send_bulk_messages(self, phone_numbers: List[str], message: str, 
                          progress_callback: Optional[Callable] = None,
                          status_callback: Optional[Callable] = None) -> Dict[str, int]:
        """Send bulk messages to multiple phone numbers"""
        if not self.driver:
            return {"success": 0, "failed": 0}
        
        self.is_sending = True
        results = {"success": 0, "failed": 0}
        
        total_numbers = len(phone_numbers)
        
        for i, phone_number in enumerate(phone_numbers):
            if not self.is_sending:
                break
            
            # Update progress
            if status_callback:
                status_callback(i + 1, total_numbers)
            
            # Send message
            success = self.send_message(phone_number, message, progress_callback)
            
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
            
            # Additional delay between messages
            if i < total_numbers - 1:  # Don't delay after last message
                extra_delay = random.uniform(2, 5)
                time.sleep(extra_delay)
        
        return results
    
    def stop_sending(self):
        """Stop the sending process"""
        self.is_sending = False
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        self.wait = None
    
    def __del__(self):
        """Destructor to clean up resources"""
        self.cleanup()


class SmartWhatsAppDelay:
    """Smart delay management for WhatsApp to avoid rate limiting"""
    
    def __init__(self):
        self.message_times = []
        self.base_delay = 8.0  # Base delay between messages (8 seconds)
        self.max_delay = 30.0  # Maximum delay (30 seconds)
        self.adaptive_delay = self.base_delay
        self.consecutive_failures = 0
        
    def get_smart_delay(self) -> float:
        """Calculate smart delay based on sending patterns and WhatsApp limits"""
        current_time = time.time()
        
        # Clean old message times (keep last 20 messages)
        self.message_times = [t for t in self.message_times if current_time - t < 300]  # 5 minutes
        
        # Calculate adaptive delay based on recent activity
        if len(self.message_times) >= 10:
            # If we have many recent messages, increase delay significantly
            recent_messages = len([t for t in self.message_times if current_time - t < 60])  # Last minute
            
            if recent_messages >= 5:
                # Very aggressive rate limiting
                self.adaptive_delay = min(self.max_delay, self.adaptive_delay * 1.5)
            elif recent_messages >= 3:
                # Moderate rate limiting
                self.adaptive_delay = min(self.max_delay, self.adaptive_delay * 1.2)
            else:
                # Reduce delay if we're not sending too fast
                self.adaptive_delay = max(self.base_delay, self.adaptive_delay * 0.95)
        
        # Increase delay if we had consecutive failures
        if self.consecutive_failures > 0:
            self.adaptive_delay = min(self.max_delay, self.adaptive_delay * (1 + self.consecutive_failures * 0.1))
        
        # Add randomness to avoid pattern detection
        delay = self.adaptive_delay + random.uniform(-2.0, 3.0)
        delay = max(self.base_delay, min(self.max_delay, delay))
        
        # Record this message
        self.message_times.append(current_time)
        
        return delay
    
    def report_failure(self):
        """Report a sending failure to adjust delays"""
        self.consecutive_failures += 1
        
    def report_success(self):
        """Report a sending success to adjust delays"""
        self.consecutive_failures = max(0, self.consecutive_failures - 1)
    
    def get_hourly_limit_delay(self) -> float:
        """Get delay to respect WhatsApp's hourly limits"""
        # WhatsApp typically allows around 60-80 messages per hour
        # We'll aim for 50 messages per hour to be safe
        return 3600 / 50  # 72 seconds between messages
    
    def wait_smart_delay(self):
        """Wait for the calculated smart delay"""
        delay = self.get_smart_delay()
        time.sleep(delay)
        return delay
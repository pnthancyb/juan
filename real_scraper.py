"""
Real Google Maps Scraper
Uses Chrome WebDriver to scrape actual Google Maps business data
"""

import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Optional

class GoogleMapsScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.is_scraping = False
        
    def setup_driver(self):
        """Setup Chrome WebDriver with optimal settings"""
        try:
            # Check if Chrome is available
            import subprocess
            try:
                subprocess.run(['google-chrome', '--version'], capture_output=True, check=True)
                chrome_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                chrome_available = False
            
            if not chrome_available:
                print("Chrome browser not found. Please install Chrome for real scraping.")
                return False
            
            chrome_options = Options()
            
            # High-performance Chrome flags
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-field-trial-config")
            chrome_options.add_argument("--disable-component-update")
            chrome_options.add_argument("--disable-background-networking")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
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
            self.wait = WebDriverWait(self.driver, 10)
            
            return True
            
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            return False
    
    def search_businesses(self, keyword: str, max_results: int = 50) -> List[Dict[str, str]]:
        """Search for businesses on Google Maps"""
        if not self.driver:
            if not self.setup_driver():
                return []
        
        try:
            # Navigate to Google Maps
            self.driver.get("https://www.google.com/maps")
            time.sleep(2)
            
            # Find search box and enter keyword
            search_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "searchboxinput"))
            )
            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            time.sleep(3)
            
            # Collect business data
            businesses = []
            seen_names = set()
            
            # Scroll to load more results
            for _ in range(max_results // 10):  # Approximate pagination
                if not self.is_scraping:
                    break
                    
                # Find business elements
                business_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, "[data-result-index]"
                )
                
                for element in business_elements:
                    if len(businesses) >= max_results:
                        break
                    
                    try:
                        business_data = self._extract_business_data(element, keyword)
                        if business_data and business_data['Business Name'] not in seen_names:
                            businesses.append(business_data)
                            seen_names.add(business_data['Business Name'])
                            
                    except Exception as e:
                        continue
                
                # Scroll to load more results
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            return businesses
            
        except Exception as e:
            print(f"Error searching businesses: {e}")
            return []
    
    def _extract_business_data(self, element, keyword: str) -> Optional[Dict[str, str]]:
        """Extract business data from a single element"""
        try:
            # Get business name
            name_element = element.find_element(By.CSS_SELECTOR, "[data-value='Name']")
            business_name = name_element.text.strip()
            
            if not business_name:
                return None
            
            # Get address
            address = ""
            try:
                address_element = element.find_element(By.CSS_SELECTOR, "[data-value='Address']")
                address = address_element.text.strip()
            except NoSuchElementException:
                pass
            
            # Get phone number
            phone = ""
            try:
                phone_element = element.find_element(By.CSS_SELECTOR, "[data-value='Phone']")
                phone = phone_element.text.strip()
            except NoSuchElementException:
                pass
            
            # Get website
            website = ""
            try:
                website_element = element.find_element(By.CSS_SELECTOR, "[data-value='Website']")
                website = website_element.get_attribute("href")
            except NoSuchElementException:
                pass
            
            # Get rating and reviews
            rating = ""
            try:
                rating_element = element.find_element(By.CSS_SELECTOR, "[data-value='Rating']")
                rating = rating_element.text.strip()
            except NoSuchElementException:
                pass
            
            return {
                "Keyword": keyword,
                "Business Name": business_name,
                "Address": address,
                "Phone": phone,
                "Website": website,
                "Rating": rating
            }
            
        except Exception as e:
            return None
    
    def scrape_with_fallback(self, keyword: str, max_results: int = 50) -> List[Dict[str, str]]:
        """Scrape with fallback methods if primary method fails"""
        try:
            # Try primary method first
            results = self.search_businesses(keyword, max_results)
            
            if results:
                return results
            
            # Fallback to alternative scraping method
            return self._fallback_scrape(keyword, max_results)
            
        except Exception as e:
            print(f"Error in scrape_with_fallback: {e}")
            return self._fallback_scrape(keyword, max_results)
    
    def _fallback_scrape(self, keyword: str, max_results: int) -> List[Dict[str, str]]:
        """Fallback scraping method using requests and BeautifulSoup"""
        try:
            # Use Google Maps search URL
            search_url = f"https://www.google.com/maps/search/{keyword.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract business data from HTML
            businesses = []
            
            # Look for business listings in the HTML
            business_divs = soup.find_all('div', class_='lI9IFe')
            
            for div in business_divs[:max_results]:
                try:
                    # Extract business name
                    name_elem = div.find('div', class_='qBF1Pd')
                    if name_elem:
                        name = name_elem.text.strip()
                        
                        # Create basic business entry
                        business = {
                            "Keyword": keyword,
                            "Business Name": name,
                            "Address": "",
                            "Phone": "",
                            "Website": "",
                            "Rating": ""
                        }
                        
                        businesses.append(business)
                        
                except Exception as e:
                    continue
            
            return businesses
            
        except Exception as e:
            print(f"Error in fallback scrape: {e}")
            return []
    
    def stop_scraping(self):
        """Stop the scraping process"""
        self.is_scraping = False
    
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


class SmartDelayScraper:
    """Smart delay management to avoid rate limiting"""
    
    def __init__(self):
        self.request_times = []
        self.min_delay = 1.0  # Minimum delay between requests
        self.max_delay = 5.0  # Maximum delay between requests
        self.adaptive_delay = 2.0  # Current adaptive delay
    
    def get_smart_delay(self) -> float:
        """Calculate smart delay based on recent request patterns"""
        current_time = time.time()
        
        # Clean old request times (keep last 10 requests)
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        # Calculate adaptive delay based on request frequency
        if len(self.request_times) >= 5:
            # If we have many recent requests, increase delay
            recent_requests = len([t for t in self.request_times if current_time - t < 10])
            if recent_requests >= 3:
                self.adaptive_delay = min(self.max_delay, self.adaptive_delay * 1.2)
            else:
                self.adaptive_delay = max(self.min_delay, self.adaptive_delay * 0.9)
        
        # Add some randomness to avoid pattern detection
        delay = self.adaptive_delay + random.uniform(-0.5, 0.5)
        delay = max(self.min_delay, min(self.max_delay, delay))
        
        # Record this request
        self.request_times.append(current_time)
        
        return delay
    
    def wait_smart_delay(self):
        """Wait for the calculated smart delay"""
        delay = self.get_smart_delay()
        time.sleep(delay)
        return delay
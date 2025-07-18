"""
Data Processing Module
Handles data manipulation and mock business data generation
"""

import random
import time
from typing import List, Dict

class DataProcessor:
    def __init__(self):
        # Mock business data for simulation
        self.business_types = [
            "Restaurant", "Cafe", "Shop", "Store", "Market", "Boutique",
            "Office", "Clinic", "Salon", "Gym", "Garage", "Studio"
        ]
        
        self.street_names = [
            "Main St", "Oak Ave", "Park Rd", "First St", "Second Ave",
            "Elm St", "Maple Ave", "Cedar Rd", "Pine St", "Washington Ave"
        ]
        
        self.business_suffixes = [
            "LLC", "Inc", "Co", "& Associates", "Group", "Services",
            "Solutions", "Center", "Place", "House"
        ]
        
        self.area_codes = ["555", "123", "456", "789", "321", "654"]
        
    def simulate_scraping(self, keyword: str) -> List[Dict[str, str]]:
        """
        Simulate business data scraping for a given keyword
        Returns mock business data
        """
        # Random number of results (1-5 businesses per keyword)
        num_results = random.randint(1, 5)
        results = []
        
        for i in range(num_results):
            business = self._generate_mock_business(keyword, i + 1)
            results.append(business)
            
        # Simulate processing time
        time.sleep(random.uniform(0.5, 2.0))
        
        return results
        
    def _generate_mock_business(self, keyword: str, index: int) -> Dict[str, str]:
        """Generate a single mock business entry"""
        # Generate business name
        business_type = random.choice(self.business_types)
        suffix = random.choice(self.business_suffixes)
        business_name = f"{keyword.title()} {business_type} {suffix}"
        
        # Generate address
        street_number = random.randint(100, 9999)
        street_name = random.choice(self.street_names)
        city = f"{keyword.title()}ville"
        state = random.choice(["CA", "NY", "TX", "FL", "IL", "PA"])
        zip_code = f"{random.randint(10000, 99999)}"
        address = f"{street_number} {street_name}, {city}, {state} {zip_code}"
        
        # Generate phone
        area_code = random.choice(self.area_codes)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        phone = f"({area_code}) {exchange}-{number}"
        
        # Generate website
        business_slug = keyword.lower().replace(" ", "")
        website = f"https://www.{business_slug}{business_type.lower()}{index}.com"
        
        return {
            "Keyword": keyword,
            "Business Name": business_name,
            "Address": address,
            "Phone": phone,
            "Website": website
        }
        
    def clean_phone_number(self, phone: str) -> str:
        """
        Clean and format phone number
        Remove non-numeric characters except +
        """
        import re
        # Remove all non-numeric characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        return cleaned
        
    def validate_business_data(self, data: Dict[str, str]) -> bool:
        """
        Validate business data entry
        Check if all required fields are present and valid
        """
        required_fields = ["Keyword", "Business Name", "Address", "Phone", "Website"]
        
        for field in required_fields:
            if field not in data or not data[field].strip():
                return False
                
        return True
        
    def export_to_csv(self, data: List[Dict[str, str]], filename: str) -> bool:
        """
        Export business data to CSV file
        """
        try:
            import csv
            
            if not data:
                return False
                
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ["Keyword", "Business Name", "Address", "Phone", "Website"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for row in data:
                    if self.validate_business_data(row):
                        writer.writerow(row)
                        
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
            
    def load_from_csv(self, filename: str) -> List[Dict[str, str]]:
        """
        Load business data from CSV file
        """
        try:
            import csv
            data = []
            
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if self.validate_business_data(row):
                        data.append(row)
                        
            return data
            
        except Exception as e:
            print(f"Error loading from CSV: {e}")
            return []

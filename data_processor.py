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
        
    def simulate_scraping(self, keyword: str, max_results: int = 50) -> List[Dict[str, str]]:
        """
        Simulate business data scraping for a given keyword
        Returns mock business data with specified number of results
        """
        # Generate exactly the number of results requested (with some variation)
        # Use 80-100% of requested results to simulate real-world variance
        min_results = max(1, int(max_results * 0.8))
        max_results_actual = max_results
        num_results = random.randint(min_results, max_results_actual)
        
        results = []
        
        for i in range(num_results):
            business = self._generate_mock_business(keyword, i + 1)
            results.append(business)
            
        # Simulate processing time based on number of results
        processing_time = random.uniform(1.0, 3.0) + (num_results * 0.1)
        time.sleep(processing_time)
        
        return results
        
    def _generate_mock_business(self, keyword: str, index: int) -> Dict[str, str]:
        """Generate a single mock business entry"""
        # Generate more realistic business names
        business_type = random.choice(self.business_types)
        suffix = random.choice(self.business_suffixes)
        
        # Create more varied business names
        name_patterns = [
            f"{keyword.title()} {business_type} {suffix}",
            f"{keyword.title()} {business_type}",
            f"Best {keyword.title()} {business_type}",
            f"{keyword.title()} Pro {business_type}",
            f"Elite {keyword.title()} {suffix}",
            f"{keyword.title()} Express {business_type}",
            f"Premium {keyword.title()} {suffix}",
            f"{keyword.title()} Plus {business_type}"
        ]
        
        business_name = random.choice(name_patterns)
        
        # Generate more realistic addresses
        street_number = random.randint(100, 9999)
        street_name = random.choice(self.street_names)
        cities = [f"{keyword.title()}ville", f"{keyword.title()}town", f"{keyword.title()} City", 
                 f"New {keyword.title()}", f"{keyword.title()} Heights", f"{keyword.title()} Park"]
        city = random.choice(cities)
        state = random.choice(["CA", "NY", "TX", "FL", "IL", "PA", "OH", "MI", "GA", "NC"])
        zip_code = f"{random.randint(10000, 99999)}"
        address = f"{street_number} {street_name}, {city}, {state} {zip_code}"
        
        # Generate phone with more variety
        area_code = random.choice(self.area_codes)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        phone_formats = [
            f"({area_code}) {exchange}-{number}",
            f"{area_code}-{exchange}-{number}",
            f"+1 {area_code} {exchange} {number}",
            f"{area_code}.{exchange}.{number}"
        ]
        phone = random.choice(phone_formats)
        
        # Generate website with more variety
        business_slug = keyword.lower().replace(" ", "").replace("-", "")
        domain_types = [".com", ".net", ".org", ".biz"]
        domain_patterns = [
            f"{business_slug}{business_type.lower()}{index}",
            f"{business_slug}-{business_type.lower()}",
            f"{business_type.lower()}-{business_slug}",
            f"{business_slug}{index}",
            f"best{business_slug}{business_type.lower()}",
            f"{business_slug}pro"
        ]
        domain = random.choice(domain_patterns)
        extension = random.choice(domain_types)
        website = f"https://www.{domain}{extension}"
        
        # Generate rating (for enhanced data)
        rating = round(random.uniform(3.0, 5.0), 1)
        reviews = random.randint(5, 500)
        
        return {
            "Keyword": keyword,
            "Business Name": business_name,
            "Address": address,
            "Phone": phone,
            "Website": website,
            "Rating": f"{rating} ({reviews} reviews)"
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

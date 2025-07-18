"""
Utility Functions
Common helper functions for the application
"""

import os
import re
import time
from typing import Union

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to HH:MM:SS format
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def validate_file_path(file_path: str) -> bool:
    """
    Validate if file path exists and is readable
    """
    try:
        return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
    except:
        return False

def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format using regex
    Accepts international format with optional + prefix
    """
    if not phone or not isinstance(phone, str):
        return False
        
    # Remove all whitespace and special characters except +
    cleaned = re.sub(r'[^\d+]', '', phone.strip())
    
    # Check if it matches international phone format
    # + followed by 1-3 digits (country code) and 4-14 digits (number)
    pattern = r'^\+?[1-9]\d{1,14}$'
    
    return bool(re.match(pattern, cleaned)) and len(cleaned) >= 7

def clean_phone_number(phone: str) -> str:
    """
    Clean phone number by removing non-numeric characters except +
    """
    if not phone or not isinstance(phone, str):
        return ""
        
    # Remove all non-numeric characters except +
    cleaned = re.sub(r'[^\d+]', '', phone.strip())
    
    return cleaned

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    """
    if not filename:
        return "untitled"
        
    # Remove invalid filename characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip('. ')
    
    # Ensure filename is not empty
    if not sanitized:
        sanitized = "untitled"
        
    return sanitized

def create_backup_filename(original_path: str) -> str:
    """
    Create a backup filename with timestamp
    """
    import datetime
    
    base, ext = os.path.splitext(original_path)
    timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")
    
    return f"{base}_backup{timestamp}{ext}"

def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure directory exists, create if it doesn't
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Failed to create directory {directory_path}: {e}")
        return False

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except:
        return 0.0

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def is_valid_url(url: str) -> bool:
    """
    Basic URL validation
    """
    if not url or not isinstance(url, str):
        return False
        
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
    return bool(url_pattern.match(url))

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length with ellipsis
    """
    if not text or len(text) <= max_length:
        return text
        
    return text[:max_length - 3] + "..."

def get_timestamp() -> str:
    """
    Get current timestamp in readable format
    """
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_cast(value, target_type, default=None):
    """
    Safely cast value to target type with default fallback
    """
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return default

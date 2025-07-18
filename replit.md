# Juan - Maps Scraper & WhatsApp Blaster

## Overview

Juan is a desktop application built with Python and Tkinter that combines Google Maps business data scraping with WhatsApp bulk messaging capabilities. The application provides a tabbed interface for two main functions: scraping business data from maps and sending bulk WhatsApp messages to collected phone numbers.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **GUI Framework**: Tkinter with ttk (themed widgets)
- **Design Pattern**: Tab-based interface with modular components
- **Layout**: Grid-based layout management for responsive design
- **Styling**: Custom ttk styling with consistent color scheme (#f0f0f0 background)

### Backend Architecture
- **Language**: Python 3.x
- **Architecture Pattern**: Modular design with separate concerns
- **Threading**: Multi-threaded for non-blocking UI operations
- **Data Processing**: Mock data generation for business simulation

## Key Components

### 1. Main Application (`main.py`)
- **Purpose**: Entry point and main window setup
- **Responsibilities**: Window configuration, tab container management, style setup
- **Key Features**: 900x700 resizable window, custom ttk styling

### 2. Scraper Tab (`scraper_tab.py`)
- **Purpose**: Business data scraping interface
- **Key Features**: 
  - Keywords file configuration
  - Scraping progress tracking with timer
  - Data export to CSV
  - Multi-threaded scraping operations

### 3. WhatsApp Tab (`whatsapp_tab.py`)
- **Purpose**: Bulk messaging interface
- **Key Features**:
  - CSV import for phone numbers
  - Phone number validation
  - Message template configuration
  - Bulk sending with progress tracking

### 4. Data Processor (`data_processor.py`)
- **Purpose**: Mock business data generation
- **Key Features**:
  - Simulates Google Maps scraping
  - Generates realistic business data (names, addresses, phones)
  - Configurable delay simulation
  - Support for multiple business types

### 5. Utilities (`utils.py`)
- **Purpose**: Common helper functions
- **Key Functions**:
  - Duration formatting (HH:MM:SS)
  - File path validation
  - Phone number validation and cleaning
  - Regex-based phone number format checking

## Data Flow

### Scraping Workflow
1. User selects keywords file (default: `keywords.txt`)
2. Application reads keywords line by line
3. For each keyword, `DataProcessor` generates mock business data
4. Results are displayed in real-time in the GUI
5. Data can be exported to CSV format

### WhatsApp Workflow
1. User imports CSV file containing phone numbers
2. Phone numbers are validated using regex patterns
3. User configures message template
4. Messages are sent in bulk with progress tracking
5. Results are logged and displayed

## External Dependencies

### Core Dependencies
- **tkinter**: Built-in Python GUI framework
- **threading**: For non-blocking operations
- **csv**: For data import/export
- **re**: For phone number validation
- **random**: For mock data generation
- **time**: For timing and delays
- **datetime**: For timestamps
- **os**: For file operations

### Data Sources
- **keywords.txt**: Text file containing search keywords (one per line)
- **CSV files**: For phone number import (user-provided)

## Deployment Strategy

### Current Setup
- **Platform**: Desktop application (cross-platform Python)
- **Distribution**: Source code distribution
- **Dependencies**: Python standard library only
- **Installation**: No special installation required

### File Structure
```
juan/
├── main.py                 # Application entry point
├── scraper_tab.py         # Maps scraping interface
├── whatsapp_tab.py        # WhatsApp messaging interface
├── data_processor.py      # Mock data generation
├── utils.py               # Utility functions
└── keywords.txt           # Default keywords file
```

### Key Architectural Decisions

1. **Tkinter Choice**: Chosen for zero external dependencies and cross-platform compatibility
2. **Mock Data Simulation**: Uses simulated data instead of real scraping to avoid legal/technical complications
3. **Modular Design**: Separate files for each major component for maintainability
4. **Threading Model**: Non-blocking UI operations using Python threading
5. **CSV-Based Data Exchange**: Simple, universal format for data import/export
6. **Regex Phone Validation**: Flexible international phone number format support

### Performance Considerations
- Simulated delays (0.5-2.0 seconds) for realistic scraping simulation
- Progressive UI updates to maintain responsiveness
- Memory-efficient data structures for handling business listings
- Thread-safe operations for concurrent data processing

### Security Considerations
- File path validation to prevent directory traversal
- Phone number sanitization and validation
- Read-only file access patterns
- No external network connections in current implementation
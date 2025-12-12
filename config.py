"""
Configuration settings for Gambia Price Tracker
"""
import os
from pathlib import Path

# App Configuration
APP_NAME = "Gambia Price Tracker"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Track and compare prices of common goods across The Gambia"

# File Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CSV_FILE = DATA_DIR / "prices.csv"
BACKUP_DIR = DATA_DIR / "backups"

# Data Configuration
COLUMNS = ['Item', 'Price', 'Location',
           'Date', 'Timestamp', 'Currency', 'Unit']
DEFAULT_CURRENCY = "GMD"
DEFAULT_UNIT = "piece"

# Common items in The Gambia
COMMON_ITEMS = [
    'Rice (1kg)', 'Bread', 'Sugar (1kg)', 'Oil (1L)', 'Onions (1kg)',
    'Tomatoes (1kg)', 'Fish (1kg)', 'Chicken (1kg)', 'Milk (1L)', 'Eggs (dozen)',
    'Potatoes (1kg)', 'Cassava (1kg)', 'Groundnuts (1kg)', 'Millet (1kg)',
    'Flour (1kg)', 'Salt (1kg)', 'Soap', 'Detergent', 'Cooking Gas', 'Mango',
    'Banana', 'Orange', 'Lemon', 'Garlic (1kg)', 'Ginger (1kg)', 'Pepper (1kg)',
    'Beans (1kg)', 'Lentils (1kg)', 'Tea', 'Coffee', 'Cocoa'
]

# Gambian locations
GAMBIAN_LOCATIONS = [
    'Banjul', 'Serekunda', 'Sukuta', 'Bakau', 'Fajara', 'Kairaba', 'Kololi',
    'Brikama', 'Soma', 'Farafenni', 'Basse', 'Janjanbureh', 'Gunjur', 'Tanji',
    'Lamin', 'Brufut', 'Tujereng', 'Sanyang', 'Kartong', 'Gunjur', 'Bintang',
    'Kerewan', 'Mansa Konko', 'Kuntaur', 'Barra', 'Essau', 'Bwiam'
]

# Alert Configuration
PRICE_CHANGE_THRESHOLD = 15.0  # Percentage
MAX_ALERTS_DISPLAY = 5

# Chart Configuration
CHART_HEIGHT = 400
CHART_THEME = "plotly_white"

# Validation Rules
MIN_PRICE = 0.01
MAX_PRICE = 10000.00
MAX_ITEM_LENGTH = 100
MAX_LOCATION_LENGTH = 50

# Export Configuration
EXPORT_FORMATS = ['csv', 'excel', 'json']
DEFAULT_EXPORT_FORMAT = 'csv'

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

"""
Data management utilities for Gambia Price Tracker
"""
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from pathlib import Path
import logging
from typing import Optional, List, Dict, Any, Tuple
import streamlit as st

from config import CSV_FILE, COLUMNS, DEFAULT_CURRENCY, DEFAULT_UNIT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataManager:
    """Handles all data operations for the price tracker"""

    def __init__(self, csv_file: Path = CSV_FILE):
        self.csv_file = csv_file
        self.csv_file.parent.mkdir(exist_ok=True)

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def load_data(_self) -> pd.DataFrame:
        """Load data from CSV with caching and error handling"""
        try:
            if _self.csv_file.exists() and _self.csv_file.stat().st_size > 0:
                df = pd.read_csv(_self.csv_file)

                # Ensure all required columns exist
                for col in COLUMNS:
                    if col not in df.columns:
                        df[col] = None

                # Convert dates properly
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df = df.dropna(subset=['Date'])

                # Set default values for missing currency/unit
                df['Currency'] = df.get('Currency', DEFAULT_CURRENCY)
                df['Unit'] = df.get('Unit', DEFAULT_UNIT)

                return df.sort_values('Date', ascending=False)
            else:
                return pd.DataFrame(columns=COLUMNS)

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            st.error(f"Error loading data: {e}")
            return pd.DataFrame(columns=COLUMNS)

    def save_data(self, df: pd.DataFrame) -> bool:
        """Save dataframe to CSV with error handling"""
        try:
            # Create backup before saving
            if self.csv_file.exists():
                backup_file = self.csv_file.parent / "backups" / \
                    f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                backup_file.parent.mkdir(exist_ok=True)
                df.to_csv(backup_file, index=False)

            # Save current data
            df.to_csv(self.csv_file, index=False)

            # Clear cache so data refreshes
            st.cache_data.clear()
            logger.info("Data saved successfully")
            return True

        except Exception as e:
            logger.error(f"Error saving data: {e}")
            st.error(f"Error saving data: {e}")
            return False

    def add_entry(self, item: str, price: float, location: str,
                  entry_date: date, currency: str = DEFAULT_CURRENCY,
                  unit: str = DEFAULT_UNIT) -> bool:
        """Add a new price entry"""
        try:
            df = self.load_data()

            new_entry = pd.DataFrame([{
                'Item': item.title().strip(),
                'Price': float(price),
                'Location': location.strip(),
                'Date': pd.Timestamp(entry_date),
                'Timestamp': datetime.now(),
                'Currency': currency,
                'Unit': unit
            }])

            updated_df = pd.concat([df, new_entry], ignore_index=True)
            return self.save_data(updated_df)

        except Exception as e:
            logger.error(f"Error adding entry: {e}")
            return False

    def validate_entry(self, item: str, price: float, location: str) -> List[str]:
        """Validate form entry and return list of errors"""
        errors = []

        if not item or not item.strip():
            errors.append("Item name is required")
        elif len(item.strip()) > 100:
            errors.append("Item name is too long (max 100 characters)")

        if price <= 0:
            errors.append("Price must be greater than 0")
        elif price > 10000:
            errors.append("Price seems too high (max GMD 10,000)")

        if not location or not location.strip():
            errors.append("Location is required")
        elif len(location.strip()) > 50:
            errors.append("Location name is too long (max 50 characters)")

        return errors

    def get_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive statistics from the data"""
        if df.empty:
            return {
                'total_entries': 0,
                'unique_items': 0,
                'locations_covered': 0,
                'date_range': None,
                'avg_price': 0,
                'price_range': (0, 0)
            }

        stats = {
            'total_entries': len(df),
            'unique_items': df['Item'].nunique(),
            'locations_covered': df['Location'].nunique(),
            'date_range': (df['Date'].min(), df['Date'].max()),
            'avg_price': df['Price'].mean(),
            'price_range': (df['Price'].min(), df['Price'].max()),
            'most_expensive_item': df.loc[df['Price'].idxmax(), 'Item'],
            'cheapest_item': df.loc[df['Price'].idxmin(), 'Item'],
            'most_tracked_item': df['Item'].mode().iloc[0] if not df['Item'].mode().empty else None,
            'most_tracked_location': df['Location'].mode().iloc[0] if not df['Location'].mode().empty else None
        }

        return stats

    def calculate_price_changes(self, df: pd.DataFrame, threshold: float = 15.0) -> List[Dict[str, Any]]:
        """Calculate significant price changes for alerts"""
        alerts = []

        if df.empty or len(df) < 2:
            return alerts

        # Group by item and calculate changes
        for item in df['Item'].unique():
            item_df = df[df['Item'] == item].sort_values('Date')

            if len(item_df) >= 2:
                latest = item_df.iloc[-1]
                previous = item_df.iloc[-2]

                price_change = (
                    (latest['Price'] - previous['Price']) / previous['Price']) * 100

                if abs(price_change) > threshold:
                    alerts.append({
                        'item': item,
                        'change': price_change,
                        'latest_price': latest['Price'],
                        'previous_price': previous['Price'],
                        'location': latest['Location'],
                        'date': latest['Date'].strftime('%Y-%m-%d'),
                        'trend': 'increase' if price_change > 0 else 'decrease'
                    })

        # Sort by absolute change magnitude
        alerts.sort(key=lambda x: abs(x['change']), reverse=True)
        return alerts

    def get_price_trends(self, df: pd.DataFrame, item: str, days: int = 30) -> pd.DataFrame:
        """Get price trends for a specific item over time"""
        if df.empty:
            return pd.DataFrame()

        item_df = df[df['Item'] == item].copy()
        if item_df.empty:
            return pd.DataFrame()

        # Calculate moving averages
        item_df = item_df.sort_values('Date')
        item_df['7_day_avg'] = item_df['Price'].rolling(
            window=7, min_periods=1).mean()
        item_df['30_day_avg'] = item_df['Price'].rolling(
            window=30, min_periods=1).mean()

        return item_df

    def export_data(self, df: pd.DataFrame, format: str = 'csv') -> Tuple[str, str]:
        """Export data in various formats"""
        try:
            if format == 'csv':
                data = df.to_csv(index=False)
                filename = f"gambia_prices_{date.today()}.csv"
                mime_type = "text/csv"
            elif format == 'excel':
                # Note: This would require openpyxl in requirements
                data = df.to_excel(index=False)
                filename = f"gambia_prices_{date.today()}.xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif format == 'json':
                data = df.to_json(orient='records', date_format='iso')
                filename = f"gambia_prices_{date.today()}.json"
                mime_type = "application/json"
            else:
                raise ValueError(f"Unsupported format: {format}")

            return data, filename, mime_type

        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            raise


# Global data manager instance
data_manager = DataManager()

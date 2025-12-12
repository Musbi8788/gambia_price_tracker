"""
Data Migration Script for Gambia Price Tracker
Migrates data from old format to new format with additional columns
"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import shutil


def migrate_old_data():
    """Migrate data from old format to new format"""

    # Check if old data exists
    old_csv = 'prices.csv'
    new_csv = 'data/prices.csv'

    if not os.path.exists(old_csv):
        print("✅ No old data found to migrate")
        return True

    try:
        # Read old data
        print("📖 Reading old data...")
        old_df = pd.read_csv(old_csv)

        # Check if migration is needed
        if 'Currency' in old_df.columns and 'Unit' in old_df.columns:
            print("✅ Data already in new format")
            return True

        # Create new dataframe with additional columns
        new_df = old_df.copy()

        # Add missing columns with default values
        if 'Currency' not in new_df.columns:
            new_df['Currency'] = 'GMD'
            print("➕ Added Currency column")

        if 'Unit' not in new_df.columns:
            new_df['Unit'] = 'piece'
            print("➕ Added Unit column")

        # Ensure all required columns exist
        required_columns = ['Item', 'Price', 'Location',
                            'Date', 'Timestamp', 'Currency', 'Unit']
        for col in required_columns:
            if col not in new_df.columns:
                new_df[col] = None
                print(f"➕ Added {col} column")

        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)

        # Save new data
        new_df.to_csv(new_csv, index=False)
        print(f"💾 Saved migrated data to {new_csv}")

        # Create backup of old data
        backup_file = f"data/backup_old_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        shutil.copy2(old_csv, backup_file)
        print(f"📦 Created backup: {backup_file}")

        # Optionally remove old file
        remove_old = input(
            "🗑️ Remove old prices.csv file? (y/n): ").lower().strip()
        if remove_old == 'y':
            os.remove(old_csv)
            print("🗑️ Removed old prices.csv")

        print("✅ Migration completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


def validate_data():
    """Validate the migrated data"""
    try:
        df = pd.read_csv('data/prices.csv')

        print("\n📊 Data Validation Results:")
        print(f"Total entries: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Unique items: {df['Item'].nunique()}")
        print(f"Unique locations: {df['Location'].nunique()}")

        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            print("\n⚠️ Missing data found:")
            print(missing_data[missing_data > 0])
        else:
            print("✅ No missing data found")

        return True

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False


def main():
    """Main migration function"""
    print("🔄 Gambia Price Tracker - Data Migration")
    print("=" * 50)

    # Perform migration
    if migrate_old_data():
        # Validate migrated data
        validate_data()

        print("\n🎉 Migration completed!")
        print("You can now run the new app with: streamlit run app_v2.py")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")


if __name__ == "__main__":
    main()

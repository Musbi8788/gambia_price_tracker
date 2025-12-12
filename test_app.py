"""
Test script for Gambia Price Tracker
Verifies that all components work correctly
"""

import sys
import os
import pandas as pd
from datetime import date, datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")

    try:
        from config import APP_NAME, APP_VERSION, COMMON_ITEMS, GAMBIAN_LOCATIONS
        print("✅ Config module imported successfully")

        from utils.data_manager import data_manager
        print("✅ Data manager imported successfully")

        from utils.visualizations import chart_manager
        print("✅ Chart manager imported successfully")

        from utils.ui_components import ui_components
        print("✅ UI components imported successfully")

        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_data_manager():
    """Test data manager functionality"""
    print("\n🧪 Testing data manager...")

    try:
        from utils.data_manager import data_manager

        # Test loading data
        df = data_manager.load_data()
        print(f"✅ Data loaded: {len(df)} rows")

        # Test validation
        errors = data_manager.validate_entry("Test Item", 10.0, "Banjul")
        if not errors:
            print("✅ Validation working correctly")
        else:
            print(f"❌ Validation failed: {errors}")
            return False

        # Test statistics
        stats = data_manager.get_statistics(df)
        print(f"✅ Statistics calculated: {stats['total_entries']} entries")

        return True

    except Exception as e:
        print(f"❌ Data manager test failed: {e}")
        return False


def test_chart_manager():
    """Test chart manager functionality"""
    print("\n🧪 Testing chart manager...")

    try:
        from utils.visualizations import chart_manager

        # Create sample data
        sample_data = pd.DataFrame([
            {'Item': 'Rice (1kg)', 'Price': 35.0, 'Location': 'Serekunda',
             'Date': pd.Timestamp('2024-01-15')},
            {'Item': 'Rice (1kg)', 'Price': 32.0, 'Location': 'Banjul',
             'Date': pd.Timestamp('2024-01-15')},
            {'Item': 'Bread', 'Price': 15.0, 'Location': 'Serekunda',
                'Date': pd.Timestamp('2024-01-15')},
        ])

        # Test trend chart
        trend_chart = chart_manager.create_price_trend_chart(
            sample_data, 'Rice (1kg)')
        if trend_chart:
            print("✅ Trend chart created successfully")
        else:
            print("❌ Trend chart creation failed")
            return False

        # Test comparison chart
        comp_chart = chart_manager.create_location_comparison_chart(
            sample_data, 'Rice (1kg)')
        if comp_chart:
            print("✅ Comparison chart created successfully")
        else:
            print("❌ Comparison chart creation failed")
            return False

        # Test statistics
        stats = chart_manager.create_statistics_dashboard(sample_data)
        if stats:
            print("✅ Statistics dashboard created successfully")
        else:
            print("❌ Statistics dashboard creation failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Chart manager test failed: {e}")
        return False


def test_config():
    """Test configuration settings"""
    print("\n🧪 Testing configuration...")

    try:
        from config import APP_NAME, APP_VERSION, COMMON_ITEMS, GAMBIAN_LOCATIONS

        print(f"✅ App name: {APP_NAME}")
        print(f"✅ App version: {APP_VERSION}")
        print(f"✅ Common items: {len(COMMON_ITEMS)} items")
        print(f"✅ Gambian locations: {len(GAMBIAN_LOCATIONS)} locations")

        # Check that required items exist
        required_items = ['Rice (1kg)', 'Bread', 'Sugar (1kg)']
        for item in required_items:
            if item in COMMON_ITEMS:
                print(f"✅ Required item found: {item}")
            else:
                print(f"❌ Required item missing: {item}")
                return False

        # Check that required locations exist
        required_locations = ['Banjul', 'Serekunda', 'Brikama']
        for location in required_locations:
            if location in GAMBIAN_LOCATIONS:
                print(f"✅ Required location found: {location}")
            else:
                print(f"❌ Required location missing: {location}")
                return False

        return True

    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_data_structure():
    """Test data directory structure"""
    print("\n🧪 Testing data structure...")

    try:
        # Check if data directory exists
        if os.path.exists('data'):
            print("✅ Data directory exists")
        else:
            print("📁 Creating data directory...")
            os.makedirs('data', exist_ok=True)
            print("✅ Data directory created")

        # Check if backup directory exists
        if os.path.exists('data/backups'):
            print("✅ Backup directory exists")
        else:
            print("📁 Creating backup directory...")
            os.makedirs('data/backups', exist_ok=True)
            print("✅ Backup directory created")

        # Check if prices.csv exists
        if os.path.exists('data/prices.csv'):
            print("✅ Prices CSV file exists")

            # Test reading the file
            df = pd.read_csv('data/prices.csv')
            print(f"✅ CSV file readable: {len(df)} rows")
        else:
            print("📄 Creating empty prices CSV file...")
            empty_df = pd.DataFrame(
                columns=['Item', 'Price', 'Location', 'Date', 'Timestamp', 'Currency', 'Unit'])
            empty_df.to_csv('data/prices.csv', index=False)
            print("✅ Empty CSV file created")

        return True

    except Exception as e:
        print(f"❌ Data structure test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 Gambia Price Tracker - Component Tests")
    print("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Data Structure", test_data_structure),
        ("Data Manager", test_data_manager),
        ("Chart Manager", test_chart_manager),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The app is ready to run.")
        print("Run the app with: streamlit run app_v2.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

    return passed == total


if __name__ == "__main__":
    main()

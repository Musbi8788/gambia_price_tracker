"""
UI Components for Gambia Price Tracker
"""
import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import pandas as pd

from config import COMMON_ITEMS, GAMBIAN_LOCATIONS, DEFAULT_CURRENCY, DEFAULT_UNIT


class UIComponents:
    """Handles all UI components and styling"""

    @staticmethod
    def load_custom_css():
        """Load custom CSS for better styling"""
        st.markdown("""
        <style>
            /* Main header styling */
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 1rem;
                color: white;
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .main-header h1 {
                margin: 0;
                font-size: 2.5rem;
                font-weight: 700;
            }
            
            .main-header p {
                margin: 0.5rem 0 0 0;
                font-size: 1.1rem;
                opacity: 0.9;
            }
            
            /* Metric cards */
            .metric-card {
                background: white;
                padding: 1.5rem;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;
                margin-bottom: 1rem;
                transition: transform 0.2s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            
            /* Alert boxes */
            .alert-box {
                background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                border: 1px solid #f59e0b;
                padding: 1rem;
                border-radius: 0.75rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .success-box {
                background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
                border: 1px solid #10b981;
                padding: 1rem;
                border-radius: 0.75rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .error-box {
                background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
                border: 1px solid #ef4444;
                padding: 1rem;
                border-radius: 0.75rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            /* Form styling */
            .form-container {
                background: white;
                padding: 1.5rem;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
            }
            
            /* Chart containers */
            .chart-container {
                background: white;
                padding: 1rem;
                border-radius: 0.75rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
            }
            
            /* Mobile responsiveness */
            @media (max-width: 768px) {
                .main-header h1 {
                    font-size: 2rem;
                }
                
                .main-header p {
                    font-size: 1rem;
                }
                
                .metric-card {
                    padding: 1rem;
                }
            }
            
            /* Custom button styling */
            .stButton > button {
                border-radius: 0.5rem;
                font-weight: 600;
                transition: all 0.2s ease;
            }
            
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            
            /* Dataframe styling */
            .dataframe {
                border-radius: 0.5rem;
                overflow: hidden;
            }
            
            /* Sidebar styling */
            .css-1d391kg {
                background-color: #f8fafc;
            }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_header():
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🛒 Gambia Price Tracker</h1>
            <p>Track and compare prices of common goods across The Gambia</p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_metrics(stats: Dict[str, Any]):
        """Render key metrics in a grid"""
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Entries",
                f"{stats['total_entries']:,}",
                help="Total number of price entries"
            )

        with col2:
            st.metric(
                "Unique Items",
                f"{stats['unique_items']:,}",
                help="Number of different items tracked"
            )

        with col3:
            st.metric(
                "Locations",
                f"{stats['locations_covered']:,}",
                help="Number of locations covered"
            )

        with col4:
            avg_price = stats.get('avg_price', 0)
            st.metric(
                "Avg Price",
                f"GMD {avg_price:.2f}",
                help="Average price across all items"
            )

    @staticmethod
    def render_price_form(df: pd.DataFrame) -> Dict[str, Any]:
        """Render the price entry form"""
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.subheader("➕ Add New Price Entry")

        # Form inputs
        col1, col2 = st.columns(2)

        with col1:
            # Item selection
            item_input = st.selectbox(
                "Select Item",
                options=COMMON_ITEMS,
                help="Choose from common items or enter custom below"
            )

            custom_item = st.text_input(
                "Or enter custom item:",
                placeholder="e.g., Local Fish (500g)",
                help="Enter a custom item name"
            )

            final_item = custom_item.strip() if custom_item.strip() else item_input

            # Price input
            price_input = st.number_input(
                f"Price ({DEFAULT_CURRENCY})",
                min_value=0.01,
                max_value=10000.00,
                value=10.0,
                step=0.50,
                format="%.2f",
                help="Enter the price in Gambian Dalasi"
            )

        with col2:
            # Location selection
            location_input = st.selectbox(
                "Location",
                options=GAMBIAN_LOCATIONS,
                help="Select the location where you found this price"
            )

            # Date input
            date_input = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today(),
                help="Select the date when you observed this price"
            )

            # Unit selection
            unit_input = st.selectbox(
                "Unit",
                options=["piece", "kg", "L", "dozen", "pack", "bundle"],
                index=0,
                help="Select the unit of measurement"
            )

        # Submit button
        submitted = st.button(
            "💾 Save Entry",
            type="primary",
            use_container_width=True,
            help="Save this price entry to the database"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        return {
            'submitted': submitted,
            'item': final_item,
            'price': price_input,
            'location': location_input,
            'date': date_input,
            'unit': unit_input
        }

    @staticmethod
    def render_filters(df: pd.DataFrame) -> Dict[str, Any]:
        """Render filtering options in sidebar"""
        st.sidebar.header("🔍 Filters")

        # Item filter
        all_items = [
            'All'] + sorted(df['Item'].unique().tolist()) if not df.empty else ['All']
        selected_item_filter = st.sidebar.selectbox(
            "Filter by Item",
            all_items,
            help="Filter data by specific item"
        )

        # Location filter
        all_locations = [
            'All'] + sorted(df['Location'].unique().tolist()) if not df.empty else ['All']
        selected_location_filter = st.sidebar.selectbox(
            "Filter by Location",
            all_locations,
            help="Filter data by specific location"
        )

        # Date range filter
        if not df.empty:
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            date_range = st.sidebar.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_date=max_date,
                help="Filter data by date range"
            )
        else:
            date_range = None

        # Price range filter
        if not df.empty:
            min_price = float(df['Price'].min())
            max_price = float(df['Price'].max())
            price_range = st.sidebar.slider(
                "Price Range (GMD)",
                min_value=min_price,
                max_value=max_price,
                value=(min_price, max_price),
                help="Filter data by price range"
            )
        else:
            price_range = None

        return {
            'item_filter': selected_item_filter,
            'location_filter': selected_location_filter,
            'date_range': date_range,
            'price_range': price_range
        }

    @staticmethod
    def render_alerts(alerts: List[Dict[str, Any]], max_display: int = 5):
        """Render price alerts"""
        if not alerts:
            return

        st.sidebar.header("🚨 Price Alerts")

        for i, alert in enumerate(alerts[:max_display]):
            change_emoji = "📈" if alert['change'] > 0 else "📉"
            change_color = "red" if alert['change'] > 0 else "green"

            st.sidebar.markdown(f"""
            <div class="alert-box">
                <strong>{change_emoji} {alert['item']}</strong><br>
                <span style="color: {change_color}; font-weight: bold;">
                    {abs(alert['change']):.1f}% {'increase' if alert['change'] > 0 else 'decrease'}
                </span><br>
                GMD {alert['previous_price']:.2f} → {alert['latest_price']:.2f}<br>
                <small>📍 {alert['location']} | 📅 {alert['date']}</small>
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def render_data_table(df: pd.DataFrame, show_all: bool = False):
        """Render the data table with options"""
        st.subheader("📊 Price History")

        # Display options
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            show_all = st.checkbox("Show all entries", value=show_all)

        with col2:
            sort_by = st.selectbox(
                "Sort by",
                ["Date (Newest)", "Date (Oldest)", "Price (High-Low)",
                 "Price (Low-High)", "Item", "Location"]
            )

        with col3:
            if st.button("📥 Download Data"):
                return "download"

        # Sort data
        if sort_by == "Date (Newest)":
            display_df = df.sort_values('Date', ascending=False)
        elif sort_by == "Date (Oldest)":
            display_df = df.sort_values('Date', ascending=True)
        elif sort_by == "Price (High-Low)":
            display_df = df.sort_values('Price', ascending=False)
        elif sort_by == "Price (Low-High)":
            display_df = df.sort_values('Price', ascending=True)
        elif sort_by == "Item":
            display_df = df.sort_values('Item')
        elif sort_by == "Location":
            display_df = df.sort_values('Location')
        else:
            display_df = df

        # Limit display
        if not show_all:
            display_df = display_df.head(50)

        # Format display
        display_df_formatted = display_df.copy()
        display_df_formatted['Price'] = display_df_formatted['Price'].apply(
            lambda x: f"GMD {x:.2f}")
        display_df_formatted['Date'] = display_df_formatted['Date'].dt.strftime(
            '%Y-%m-%d')

        # Show data
        st.dataframe(
            display_df_formatted[['Item', 'Price', 'Location', 'Date']],
            use_container_width=True,
            hide_index=True
        )

        if not show_all and len(df) > 50:
            st.info(
                f"Showing 50 of {len(df)} entries. Check 'Show all entries' to see more.")

        return None

    @staticmethod
    def render_chart_selector():
        """Render chart type selector"""
        chart_types = [
            "Price Trends",
            "Location Comparison",
            "Price Distribution",
            "Monthly Trends",
            "Price Heatmap"
        ]

        selected_chart = st.selectbox(
            "Select Chart Type",
            chart_types,
            help="Choose the type of visualization to display"
        )

        return selected_chart

    @staticmethod
    def render_success_message(message: str):
        """Render success message"""
        st.markdown(f"""
        <div class="success-box">
            ✅ {message}
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_error_message(message: str):
        """Render error message"""
        st.markdown(f"""
        <div class="error-box">
            ❌ {message}
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_info_message(message: str):
        """Render info message"""
        st.info(message)

    @staticmethod
    def render_welcome_screen():
        """Render welcome screen for empty data"""
        st.markdown("""
        <div class="form-container">
            <h2>🎉 Welcome to Gambia Price Tracker!</h2>
            <p>This app helps you track and compare prices of common goods across The Gambia.</p>
            
            <h3>📋 How to get started:</h3>
            <ol>
                <li>Add your first price entry using the form on the right</li>
                <li>View price trends and comparisons in the charts</li>
                <li>Use filters to analyze specific items or locations</li>
                <li>Download your data for further analysis</li>
            </ol>
            
            <h3>💡 Tips:</h3>
            <ul>
                <li>Be consistent with units (kg, L, piece, etc.)</li>
                <li>Record prices from different locations for better comparisons</li>
                <li>Check the alerts section for significant price changes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Show sample data
        st.subheader("📝 Sample Data Format")
        sample_data = pd.DataFrame([
            {'Item': 'Rice (1kg)', 'Price': 'GMD 35.00',
             'Location': 'Serekunda', 'Date': '2024-01-15'},
            {'Item': 'Bread', 'Price': 'GMD 15.00',
                'Location': 'Banjul', 'Date': '2024-01-15'},
            {'Item': 'Sugar (1kg)', 'Price': 'GMD 25.00',
             'Location': 'Sukuta', 'Date': '2024-01-14'},
        ])
        st.dataframe(sample_data, use_container_width=True, hide_index=True)


# Global UI components instance
ui_components = UIComponents()

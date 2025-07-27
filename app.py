import streamlit as st
import pandas as pd
import os
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Gambia Price Tracker",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better mobile experience
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #16a34a 0%, #059669 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #16a34a;
    }
    .alert-box {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #d1fae5;
        border: 1px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_alerts' not in st.session_state:
    st.session_state.show_alerts = True

# Constants
CSV_FILE = 'data/prices.csv'
COLUMNS = ['Item', 'Price', 'Location', 'Date', 'Timestamp']

# Common items and locations in The Gambia
COMMON_ITEMS = [
    'Rice (1kg)', 'Bread', 'Sugar (1kg)', 'Oil (1L)', 'Onions (1kg)',
    'Tomatoes (1kg)', 'Fish (1kg)', 'Chicken (1kg)', 'Milk (1L)', 'Eggs (dozen)',
    'Potatoes (1kg)', 'Cassava (1kg)', 'Groundnuts (1kg)', 'Millet (1kg)',
    'Flour (1kg)', 'Salt (1kg)', 'Soap', 'Detergent', 'Cooking Gas', 'Mango'
]

GAMBIAN_LOCATIONS = [
    'Banjul', 'Serekunda', 'Sukuta', 'Bakau', 'Fajara', 'Kairaba', 'Kololi',
    'Brikama', 'Soma', 'Farafenni', 'Basse', 'Janjanbureh', 'Gunjur', 'Tanji',
    'Lamin', 'Brufut', 'Tujereng', 'Sanyang'
]

# Utility functions


@st.cache_data
def load_data():
    """Load data from CSV with caching"""
    try:
        if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
            df = pd.read_csv(CSV_FILE)
            # Ensure all required columns exist
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = None

            # Convert dates properly
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date'])

            return df.sort_values('Date', ascending=False)
        else:
            return pd.DataFrame(columns=COLUMNS)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=COLUMNS)


def save_data(df):
    """Save dataframe to CSV"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        df.to_csv(CSV_FILE, index=False)
        # Clear cache so data refreshes
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False


def validate_entry(item, price, location):
    """Validate form entry"""
    errors = []
    if not item.strip():
        errors.append("Item name is required")
    if price <= 0:
        errors.append("Price must be greater than 0")
    if not location.strip():
        errors.append("Location is required")
    return errors


def calculate_price_changes(df):
    """Calculate price changes for alerts"""
    alerts = []

    if df.empty:
        return alerts

    # Group by item and calculate changes
    for item in df['Item'].unique():
        item_df = df[df['Item'] == item].sort_values('Date')

        if len(item_df) >= 2:
            latest = item_df.iloc[-1]
            previous = item_df.iloc[-2]

            price_change = (
                (latest['Price'] - previous['Price']) / previous['Price']) * 100

            if abs(price_change) > 15:  # Alert for >15% change
                alerts.append({
                    'item': item,
                    'change': price_change,
                    'latest_price': latest['Price'],
                    'previous_price': previous['Price'],
                    'location': latest['Location'],
                    'date': latest['Date'].strftime('%Y-%m-%d')
                })

    return alerts


def create_price_trend_chart(df, selected_item):
    """Create interactive price trend chart"""
    item_df = df[df['Item'] == selected_item].sort_values('Date')

    if item_df.empty:
        return None

    fig = px.line(
        item_df,
        x='Date',
        y='Price',
        color='Location',
        title=f'{selected_item} - Price Trends by Location',
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (GMD)",
        height=400,
        showlegend=True
    )

    return fig


def create_location_comparison_chart(df, selected_item):
    """Create location comparison bar chart"""
    item_df = df[df['Item'] == selected_item]

    if item_df.empty:
        return None

    # Calculate average price by location
    avg_prices = item_df.groupby('Location')['Price'].agg(
        ['mean', 'count']).reset_index()
    avg_prices = avg_prices[avg_prices['count'] >= 1]  # At least 1 entry

    fig = px.bar(
        avg_prices,
        x='Location',
        y='mean',
        title=f'{selected_item} - Average Price by Location',
        labels={'mean': 'Average Price (GMD)'}
    )

    fig.update_layout(height=400)
    return fig

# Main app


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🇬🇲 Gambia Price Tracker</h1>
        <p>Track and compare prices of common goods across The Gambia</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    df = load_data()

    # Sidebar for controls
    with st.sidebar:
        st.header("📊 Controls")

        # Data summary
        st.metric("Total Entries", len(df))
        if not df.empty:
            st.metric("Unique Items", df['Item'].nunique())
            st.metric("Locations Covered", df['Location'].nunique())
            st.metric("Latest Entry", df['Date'].max().strftime('%Y-%m-%d'))

        st.divider()

        # Filters
        st.subheader("🔍 Filters")

        # Item filter
        all_items = [
            'All'] + sorted(df['Item'].unique().tolist()) if not df.empty else ['All']
        selected_item_filter = st.selectbox("Filter by Item", all_items)

        # Location filter
        all_locations = [
            'All'] + sorted(df['Location'].unique().tolist()) if not df.empty else ['All']
        selected_location_filter = st.selectbox(
            "Filter by Location", all_locations)

        # Date range filter
        if not df.empty:
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        else:
            date_range = None

        # Apply filters
        filtered_df = df.copy()
        if selected_item_filter != 'All':
            filtered_df = filtered_df[filtered_df['Item']
                                    == selected_item_filter]
        if selected_location_filter != 'All':
            filtered_df = filtered_df[filtered_df['Location']
                                    == selected_location_filter]
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df['Date'].dt.date >= start_date) &
                (filtered_df['Date'].dt.date <= end_date)
            ]

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col2:
        # Add new entry form
        st.subheader("➕ Add New Price")

        with st.container():
            # Form inputs
            item_input = st.selectbox(
                "Item",
                options=COMMON_ITEMS,
                help="Select a common item or type your own"
            )

            custom_item = st.text_input("Or enter custom item:")
            final_item = custom_item if custom_item else item_input

            price_input = st.number_input(
                "Price (GMD)",
                min_value=0.01,
                value=10.0,
                step=0.50,
                format="%.2f"
            )

            location_input = st.selectbox(
                "Location",
                options=GAMBIAN_LOCATIONS # diplay gambain locations
            )

            date_input = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today()
            )

            # Submit button
            if st.button("💾 Save Entry", type="primary", use_container_width=True):
                errors = validate_entry(
                    final_item, price_input, location_input)

                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Create new entry
                    new_entry = pd.DataFrame([{
                        'Item': final_item.title(),
                        'Price': price_input,
                        'Location': location_input,
                        'Date': pd.Timestamp(date_input),
                        'Timestamp': datetime.now()
                    }])

                    # Add to dataframe
                    updated_df = pd.concat([df, new_entry], ignore_index=True)

                    # Save to CSV
                    if save_data(updated_df):
                        st.success(
                            f"✅ Saved: {final_item} at GMD {price_input}")
                        st.rerun()  # Refresh the app
                    else:
                        st.error("❌ Failed to save entry")

        # Price alerts
        if not df.empty and st.session_state.show_alerts:
            alerts = calculate_price_changes(df)
            if alerts:
                st.subheader("⚠️ Price Alerts")
                for alert in alerts[:3]:  # Show max 3 alerts
                    change_emoji = "📈" if alert['change'] > 0 else "📉"
                    st.markdown(f"""
                    <div class="alert-box">
                        <strong>{change_emoji} {alert['item']}</strong><br>
                        {abs(alert['change']):.1f}% {'increase' if alert['change'] > 0 else 'decrease'}<br>
                        GMD {alert['previous_price']:.2f} → {alert['latest_price']:.2f}
                    </div>
                    """, unsafe_allow_html=True)

    with col1:
        # Charts and data display
        if not filtered_df.empty:
            # Quick stats
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

            with col_stat1:
                st.metric("Entries", len(filtered_df))
            with col_stat2:
                avg_price = filtered_df['Price'].mean()
                st.metric("Avg Price", f"GMD {avg_price:.2f}")
            with col_stat3:
                min_price = filtered_df['Price'].min()
                st.metric("Min Price", f"GMD {min_price:.2f}")
            with col_stat4:
                max_price = filtered_df['Price'].max()
                st.metric("Max Price", f"GMD {max_price:.2f}")

            st.divider()

            # Charts
            if selected_item_filter != 'All':
                # Price trend chart
                trend_chart = create_price_trend_chart(
                    filtered_df, selected_item_filter)
                if trend_chart:
                    st.plotly_chart(trend_chart, use_container_width=True)

                # Location comparison chart
                comparison_chart = create_location_comparison_chart(
                    df, selected_item_filter)
                if comparison_chart:
                    st.plotly_chart(comparison_chart, use_container_width=True)

            # Data table
            st.subheader("📋 Price History")

            # Display options
            col_display1, col_display2 = st.columns(2)
            with col_display1:
                show_all = st.checkbox("Show all entries", value=False)
            with col_display2:
                if st.button("📥 Download CSV"):
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="Download filtered data",
                        data=csv,
                        file_name=f"gambia_prices_{date.today()}.csv",
                        mime="text/csv"
                    )

            # Show data
            display_df = filtered_df if show_all else filtered_df.head(20)

            # Format the display
            display_df_formatted = display_df.copy()
            display_df_formatted['Price'] = display_df_formatted['Price'].apply(
                lambda x: f"GMD {x:.2f}")
            display_df_formatted['Date'] = display_df_formatted['Date'].dt.strftime(
                '%Y-%m-%d')

            st.dataframe(
                display_df_formatted[['Item', 'Price', 'Location', 'Date']],
                use_container_width=True,
                hide_index=True
            )

            if not show_all and len(filtered_df) > 20:
                st.info(
                    f"Showing 20 of {len(filtered_df)} entries. Check 'Show all entries' to see more.")

        else:
            st.info(
                "📊 No data matches your current filters. Add some price entries to get started!")

            # Show sample data format
            st.subheader("Sample Data")
            sample_data = pd.DataFrame([
                {'Item': 'Rice (1kg)', 'Price': 'GMD 35.00',
                 'Location': 'Serekunda', 'Date': '2024-01-15'},
                {'Item': 'Bread', 'Price': 'GMD 15.00',
                    'Location': 'Banjul', 'Date': '2024-01-15'},
                {'Item': 'Sugar (1kg)', 'Price': 'GMD 25.00',
                 'Location': 'Sukuta', 'Date': '2024-01-14'},
            ])
            st.dataframe(sample_data, use_container_width=True,
                         hide_index=True)


if __name__ == "__main__":
    main()

"""
Gambia Price Tracker v2.0
A comprehensive price tracking application for The Gambia
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime
import numpy as np
from typing import Dict, Any, Optional

# Import our custom modules
from config import APP_NAME, APP_VERSION, PRICE_CHANGE_THRESHOLD, MAX_ALERTS_DISPLAY
from utils.data_manager import data_manager
from utils.visualizations import chart_manager
from utils.ui_components import ui_components


def initialize_app():
    """Initialize the Streamlit app configuration"""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load custom CSS
    ui_components.load_custom_css()

    # Initialize session state
    if 'show_alerts' not in st.session_state:
        st.session_state.show_alerts = True
    if 'selected_chart' not in st.session_state:
        st.session_state.selected_chart = "Price Trends"


def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """Apply filters to the dataframe"""
    filtered_df = df.copy()

    # Item filter
    if filters['item_filter'] != 'All':
        filtered_df = filtered_df[filtered_df['Item']
                                  == filters['item_filter']]

    # Location filter
    if filters['location_filter'] != 'All':
        filtered_df = filtered_df[filtered_df['Location']
                                  == filters['location_filter']]

    # Date range filter
    if filters['date_range'] and len(filters['date_range']) == 2:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) &
            (filtered_df['Date'].dt.date <= end_date)
        ]

    # Price range filter
    if filters['price_range']:
        min_price, max_price = filters['price_range']
        filtered_df = filtered_df[
            (filtered_df['Price'] >= min_price) &
            (filtered_df['Price'] <= max_price)
        ]

    return filtered_df


def render_sidebar(df: pd.DataFrame) -> Dict[str, Any]:
    """Render sidebar with filters and alerts"""
    with st.sidebar:
        # App info
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <h3>🛒 {APP_NAME}</h3>
            <p style="font-size: 0.8rem; color: #666;">v{APP_VERSION}</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Data summary
        if not df.empty:
            stats = data_manager.get_statistics(df)
            st.metric("📊 Total Entries", f"{stats['total_entries']:,}")
            st.metric("🏷️ Unique Items", f"{stats['unique_items']:,}")
            st.metric("📍 Locations", f"{stats['locations_covered']:,}")
            st.metric("📅 Latest Entry", df['Date'].max().strftime('%Y-%m-%d'))

        st.divider()

        # Filters
        filters = ui_components.render_filters(df)

        st.divider()

        # Price alerts
        if not df.empty and st.session_state.show_alerts:
            alerts = data_manager.calculate_price_changes(
                df, PRICE_CHANGE_THRESHOLD)
            ui_components.render_alerts(alerts, MAX_ALERTS_DISPLAY)

        # Alert toggle
        st.session_state.show_alerts = st.checkbox(
            "Show Price Alerts",
            value=st.session_state.show_alerts,
            help="Toggle price change alerts"
        )

        st.divider()

        # Export options
        if not df.empty:
            st.subheader("📤 Export Data")
            export_format = st.selectbox(
                "Format",
                ["csv", "json"],
                help="Choose export format"
            )

            if st.button("Download", use_container_width=True):
                try:
                    data, filename, mime_type = data_manager.export_data(
                        df, export_format)
                    st.download_button(
                        label=f"Download {export_format.upper()}",
                        data=data,
                        file_name=filename,
                        mime=mime_type,
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Export failed: {e}")

    return filters


def render_main_content(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Render the main content area"""
    # Header
    ui_components.render_header()

    # Main layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Main content area
        if not filtered_df.empty:
            # Statistics dashboard
            stats = data_manager.get_statistics(filtered_df)
            ui_components.render_metrics(stats)

            st.divider()

            # Charts section
            st.subheader("📈 Data Visualizations")

            # Chart selector
            chart_type = ui_components.render_chart_selector()

            # Render selected chart
            if chart_type == "Price Trends" and filtered_df['Item'].nunique() > 0:
                if filtered_df['Item'].nunique() == 1:
                    selected_item = filtered_df['Item'].iloc[0]
                else:
                    selected_item = st.selectbox(
                        "Select Item for Trend Analysis",
                        sorted(filtered_df['Item'].unique())
                    )

                trend_chart = chart_manager.create_price_trend_chart(
                    filtered_df, selected_item)
                if trend_chart:
                    st.plotly_chart(trend_chart, use_container_width=True)

            elif chart_type == "Location Comparison" and filtered_df['Item'].nunique() > 0:
                if filtered_df['Item'].nunique() == 1:
                    selected_item = filtered_df['Item'].iloc[0]
                else:
                    selected_item = st.selectbox(
                        "Select Item for Location Comparison",
                        sorted(filtered_df['Item'].unique())
                    )

                comparison_chart = chart_manager.create_location_comparison_chart(
                    filtered_df, selected_item)
                if comparison_chart:
                    st.plotly_chart(comparison_chart, use_container_width=True)

            elif chart_type == "Price Distribution" and filtered_df['Item'].nunique() > 0:
                if filtered_df['Item'].nunique() == 1:
                    selected_item = filtered_df['Item'].iloc[0]
                else:
                    selected_item = st.selectbox(
                        "Select Item for Distribution Analysis",
                        sorted(filtered_df['Item'].unique())
                    )

                dist_chart = chart_manager.create_price_distribution_chart(
                    filtered_df, selected_item)
                if dist_chart:
                    st.plotly_chart(dist_chart, use_container_width=True)

            elif chart_type == "Monthly Trends":
                monthly_chart = chart_manager.create_monthly_trend_chart(
                    filtered_df)
                if monthly_chart:
                    st.plotly_chart(monthly_chart, use_container_width=True)

            elif chart_type == "Price Heatmap":
                heatmap_chart = chart_manager.create_heatmap_chart(filtered_df)
                if heatmap_chart:
                    st.plotly_chart(heatmap_chart, use_container_width=True)

            # Data table
            download_requested = ui_components.render_data_table(filtered_df)

            if download_requested == "download":
                try:
                    data, filename, mime_type = data_manager.export_data(
                        filtered_df, 'csv')
                    st.download_button(
                        label="Download Filtered Data",
                        data=data,
                        file_name=filename,
                        mime=mime_type
                    )
                except Exception as e:
                    st.error(f"Download failed: {e}")

        else:
            # Welcome screen for empty data
            ui_components.render_welcome_screen()

    with col2:
        # Add new entry form
        form_data = ui_components.render_price_form(df)

        if form_data['submitted']:
            # Validate entry
            errors = data_manager.validate_entry(
                form_data['item'],
                form_data['price'],
                form_data['location']
            )

            if errors:
                for error in errors:
                    ui_components.render_error_message(error)
            else:
                # Add entry
                success = data_manager.add_entry(
                    item=form_data['item'],
                    price=form_data['price'],
                    location=form_data['location'],
                    entry_date=form_data['date'],
                    unit=form_data['unit']
                )

                if success:
                    ui_components.render_success_message(
                        f"✅ Saved: {form_data['item']} at GMD {form_data['price']:.2f}"
                    )
                    st.rerun()  # Refresh the app
                else:
                    ui_components.render_error_message(
                        "❌ Failed to save entry")


def render_insights(df: pd.DataFrame):
    """Render insights and analysis"""
    if df.empty:
        return

    st.subheader("💡 Insights & Analysis")

    # Get comprehensive statistics
    stats = data_manager.get_statistics(df)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Price Statistics</h4>
        </div>
        """, unsafe_allow_html=True)

        if stats['most_expensive']:
            st.metric(
                "Most Expensive Item",
                f"{stats['most_expensive']['Item']}",
                f"GMD {stats['most_expensive']['Price']:.2f} at {stats['most_expensive']['Location']}"
            )

        if stats['cheapest']:
            st.metric(
                "Cheapest Item",
                f"{stats['cheapest']['Item']}",
                f"GMD {stats['cheapest']['Price']:.2f} at {stats['cheapest']['Location']}"
            )

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🎯 Popular Items & Locations</h4>
        </div>
        """, unsafe_allow_html=True)

        if stats['most_tracked_item']:
            st.metric(
                "Most Tracked Item",
                stats['most_tracked_item'],
                f"{df[df['Item'] == stats['most_tracked_item']].shape[0]} entries"
            )

        if stats['most_tracked_location']:
            st.metric(
                "Most Tracked Location",
                stats['most_tracked_location'],
                f"{df[df['Location'] == stats['most_tracked_location']].shape[0]} entries"
            )


def main():
    """Main application function"""
    # Initialize app
    initialize_app()

    # Load data
    df = data_manager.load_data()

    # Render sidebar and get filters
    filters = render_sidebar(df)

    # Apply filters
    filtered_df = apply_filters(df, filters)

    # Render main content
    render_main_content(df, filtered_df)

    # Render insights if there's data
    if not df.empty:
        st.divider()
        render_insights(df)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>🛒 Gambia Price Tracker v{version} | Built with ❤️ for The Gambia</p>
        <p>Track prices, make informed decisions, and contribute to price transparency</p>
    </div>
    """.format(version=APP_VERSION), unsafe_allow_html=True)


if __name__ == "__main__":
    main()

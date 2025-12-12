"""
Visualization utilities for Gambia Price Tracker
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List, Dict, Any
import streamlit as st
import numpy as np

from config import CHART_HEIGHT, CHART_THEME


class ChartManager:
    """Handles all chart creation and visualization logic"""

    @staticmethod
    def create_price_trend_chart(df: pd.DataFrame, selected_item: str) -> Optional[go.Figure]:
        """Create interactive price trend chart with multiple locations"""
        item_df = df[df['Item'] == selected_item].sort_values('Date')

        if item_df.empty:
            return None

        fig = px.line(
            item_df,
            x='Date',
            y='Price',
            color='Location',
            title=f'{selected_item} - Price Trends by Location',
            markers=True,
            template=CHART_THEME
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (GMD)",
            height=CHART_HEIGHT,
            showlegend=True,
            hovermode='x unified'
        )

        # Add trend line
        if len(item_df) > 1:
            z = np.polyfit(range(len(item_df)), item_df['Price'], 1)
            p = np.poly1d(z)
            fig.add_trace(
                go.Scatter(
                    x=item_df['Date'],
                    y=p(range(len(item_df))),
                    mode='lines',
                    name='Trend Line',
                    line=dict(dash='dash', color='red'),
                    showlegend=True
                )
            )

        return fig

    @staticmethod
    def create_location_comparison_chart(df: pd.DataFrame, selected_item: str) -> Optional[go.Figure]:
        """Create location comparison bar chart with statistics"""
        item_df = df[df['Item'] == selected_item]

        if item_df.empty:
            return None

        # Calculate statistics by location
        location_stats = item_df.groupby('Location').agg({
            'Price': ['mean', 'min', 'max', 'count']
        }).reset_index()

        location_stats.columns = ['Location',
                                  'Average', 'Minimum', 'Maximum', 'Count']
        location_stats = location_stats[location_stats['Count'] >= 1]

        # Create subplot with average prices and count
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Average Price by Location',
                            'Number of Entries by Location'),
            vertical_spacing=0.1
        )

        # Average price chart
        fig.add_trace(
            go.Bar(
                x=location_stats['Location'],
                y=location_stats['Average'],
                name='Average Price',
                marker_color='lightblue',
                text=location_stats['Average'].round(2),
                textposition='auto'
            ),
            row=1, col=1
        )

        # Count chart
        fig.add_trace(
            go.Bar(
                x=location_stats['Location'],
                y=location_stats['Count'],
                name='Entry Count',
                marker_color='lightgreen',
                text=location_stats['Count'],
                textposition='auto'
            ),
            row=2, col=1
        )

        fig.update_layout(
            height=CHART_HEIGHT * 1.5,
            showlegend=False,
            template=CHART_THEME
        )

        fig.update_yaxes(title_text="Price (GMD)", row=1, col=1)
        fig.update_yaxes(title_text="Number of Entries", row=2, col=1)

        return fig

    @staticmethod
    def create_price_distribution_chart(df: pd.DataFrame, selected_item: str) -> Optional[go.Figure]:
        """Create price distribution histogram"""
        item_df = df[df['Item'] == selected_item]

        if item_df.empty:
            return None

        fig = px.histogram(
            item_df,
            x='Price',
            nbins=20,
            title=f'{selected_item} - Price Distribution',
            template=CHART_THEME
        )

        fig.update_layout(
            xaxis_title="Price (GMD)",
            yaxis_title="Frequency",
            height=CHART_HEIGHT
        )

        # Add mean line
        mean_price = item_df['Price'].mean()
        fig.add_vline(
            x=mean_price,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: GMD {mean_price:.2f}"
        )

        return fig

    @staticmethod
    def create_monthly_trend_chart(df: pd.DataFrame) -> Optional[go.Figure]:
        """Create monthly price trends for all items"""
        if df.empty:
            return None

        # Group by month and item
        df_monthly = df.copy()
        df_monthly['Month'] = df_monthly['Date'].dt.to_period('M')
        monthly_avg = df_monthly.groupby(['Month', 'Item'])[
            'Price'].mean().reset_index()
        monthly_avg['Month'] = monthly_avg['Month'].astype(str)

        # Get top 10 most tracked items
        top_items = df['Item'].value_counts().head(10).index

        fig = px.line(
            monthly_avg[monthly_avg['Item'].isin(top_items)],
            x='Month',
            y='Price',
            color='Item',
            title='Monthly Price Trends - Top 10 Items',
            template=CHART_THEME
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Average Price (GMD)",
            height=CHART_HEIGHT,
            showlegend=True
        )

        return fig

    @staticmethod
    def create_heatmap_chart(df: pd.DataFrame) -> Optional[go.Figure]:
        """Create price heatmap by location and item"""
        if df.empty:
            return None

        # Calculate average prices by location and item
        pivot_data = df.pivot_table(
            values='Price',
            index='Location',
            columns='Item',
            aggfunc='mean'
        ).fillna(0)

        # Get top items and locations
        top_items = df['Item'].value_counts().head(15).index
        top_locations = df['Location'].value_counts().head(10).index

        pivot_filtered = pivot_data.loc[top_locations, top_items]

        fig = px.imshow(
            pivot_filtered,
            title='Price Heatmap by Location and Item',
            template=CHART_THEME,
            color_continuous_scale='RdYlBu_r'
        )

        fig.update_layout(
            height=CHART_HEIGHT,
            xaxis_title="Items",
            yaxis_title="Locations"
        )

        return fig

    @staticmethod
    def create_statistics_dashboard(df: pd.DataFrame) -> Dict[str, Any]:
        """Create comprehensive statistics dashboard"""
        if df.empty:
            return {
                'total_entries': 0,
                'unique_items': 0,
                'locations_covered': 0,
                'avg_price': 0,
                'price_range': (0, 0),
                'most_expensive': None,
                'cheapest': None,
                'most_tracked': None
            }

        stats = {
            'total_entries': len(df),
            'unique_items': df['Item'].nunique(),
            'locations_covered': df['Location'].nunique(),
            'avg_price': df['Price'].mean(),
            'price_range': (df['Price'].min(), df['Price'].max()),
            'most_expensive': df.loc[df['Price'].idxmax(), ['Item', 'Price', 'Location']].to_dict(),
            'cheapest': df.loc[df['Price'].idxmin(), ['Item', 'Price', 'Location']].to_dict(),
            'most_tracked_item': df['Item'].mode().iloc[0] if not df['Item'].mode().empty else None,
            'most_tracked_location': df['Location'].mode().iloc[0] if not df['Location'].mode().empty else None,
            'recent_activity': len(df[df['Date'] >= pd.Timestamp.now() - pd.Timedelta(days=7)])
        }

        return stats

    @staticmethod
    def create_price_alert_chart(alerts: List[Dict[str, Any]]) -> Optional[go.Figure]:
        """Create chart showing price alerts"""
        if not alerts:
            return None

        # Prepare data for chart
        alert_df = pd.DataFrame(alerts)
        alert_df['abs_change'] = alert_df['change'].abs()

        fig = px.bar(
            alert_df.head(10),  # Show top 10 alerts
            x='item',
            y='abs_change',
            color='change',
            title='Significant Price Changes',
            template=CHART_THEME,
            color_continuous_scale='RdYlGn'
        )

        fig.update_layout(
            xaxis_title="Item",
            yaxis_title="Price Change (%)",
            height=CHART_HEIGHT,
            showlegend=False
        )

        # Add hover text
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
            "Change: %{y:.1f}%<br>" +
            "Latest: GMD %{customdata[0]:.2f}<br>" +
            "Previous: GMD %{customdata[1]:.2f}<br>" +
            "Location: %{customdata[2]}<extra></extra>",
            customdata=alert_df[['latest_price',
                                 'previous_price', 'location']].values
        )

        return fig


# Global chart manager instance
chart_manager = ChartManager()

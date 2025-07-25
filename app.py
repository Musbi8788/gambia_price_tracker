import streamlit as st
import pandas as pd
import os
from datetime import date
import plotly.express as px

# Title
st.title("Gambia Price Tracker")
st.caption("Track prices of common goods over time.")

# File setup
csv_file = 'prices.csv'
columns = ['Item', 'Price', 'Location', 'Date']

# Safely load or create CSV
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    df = pd.read_csv(csv_file)
    # If the loaded CSV has wrong columns, reset it
    if not all(col in df.columns for col in columns):
        df = pd.DataFrame(columns=columns)
else:
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file, index=False)

# Convert 'Date' column to datetime - FIXED VERSION
if 'Date' in df.columns and not df.empty:
    # Convert all date entries to pandas datetime, handling various formats
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    # Drop rows where date conversion failed
    df = df.dropna(subset=['Date'])

# Form to add new price
st.header("Add New Entry")
with st.form("entry_form"):
    item = st.text_input("Item name (e.g. Sugar, Bread)")
    price = st.number_input("Price in GMD", min_value=10, value=10, step=1)
    location = st.text_input("Location name (e.g. Sukuta, Banjul)")
    date_selected = st.date_input('Date', value=date.today())

    submitted = st.form_submit_button("Save Entry")

    if submitted and item:
        # Convert date_selected to pandas Timestamp to match existing data
        date_as_timestamp = pd.Timestamp(date_selected)

        new_entry = pd.DataFrame(
            [[item.title(), price, location.title(), date_as_timestamp]], columns=df.columns)
        df = pd.concat([df, new_entry], ignore_index=True)

        # Ensure all dates are pandas Timestamps
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])

        df.to_csv(csv_file, index=False)
        st.success(f"Saved: {item.title()} at {price} GMD")

# Display full table
st.header("Price History Table")
if not df.empty:
    # Sort by date (now all dates are datetime objects)
    df_sorted = df.sort_values(by="Date", ascending=False)
    st.dataframe(df_sorted, use_container_width=True)
else:
    st.info("No data to display yet.")

# Plot chart
st.header("Price Chart")
if not df.empty:
    item_list = df['Item'].unique().tolist()

    if item_list:
        selected_item = st.selectbox('Select item to view chart', item_list)
        filtered_df = df[df['Item'] == selected_item]

        chart = px.line(filtered_df, x="Date", y='Price',
                        title=f"{selected_item} Price Over Time")
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("No items available for chart.")
else:
    st.info("No data to display chart yet.")

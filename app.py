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
    
# Convert 'Date' column to datetime
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')


# Form to ad new price
st.header("Add New Entry")
with st.form("entry_form"):
    item = st.text_input("Item name (e.g. Sugar, Bread)")
    price = st.number_input("Price in GMD", min_value=10, value=10, step=1)
    location = st.text_input("Location name (e.g. Sukuta, Banjul)")
    date_selected = st.date_input('Date', value=date.today())

    submitted = st.form_submit_button("Save Entry")
    print(df.columns)

    if submitted and item:
        new_entry = pd.DataFrame(
            [[item.title(), price, location.title(), date_selected]], columns=df.columns)
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.success(f"Saved: {item.title()} at {price} GMD")
        

# Display full table
st.header("Price History Table")
st.dataframe(df.sort_values(by="Date", ascending=False),
            use_container_width=True)


# Plot chart
st.header("Price Chart")
item_list = df['Item'].unique().tolist()

if item_list:
    selected_item = st.selectbox('Select item ot view chart', item_list)
    filtered_df = df[df['Item'] == selected_item]

    chart = px.line(filtered_df, x="Date", y='Price',
                    title=f"{selected_item} Price Over Time")
    st.plotly_chart(chart, use_container_width=True)

else:
    st.info("No data to display chart yet.")

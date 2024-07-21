import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.olympics
collection = db.medal_tally

# Fetch data
data = list(collection.find({}, {"_id": 0}))  # Exclude the _id field

# Check if data is fetched correctly
if data:
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Ensure all column names are strings and clean them
    df.columns = df.columns.astype(str).str.strip()

    # Ensure only the desired columns are included
    required_columns = ['Rank', 'Nation', 'Gold', 'Silver', 'Bronze', 'Total']
    df = df[required_columns]

    # Custom CSS for background image
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("https://cloudfront-us-east-2.images.arcpublishing.com/reuters/OE623QT6EFKU3LY5GUDL4FW2AA.jpg");
    background-size: cover;
    }
    </style>
    '''

    # Insert the background image CSS
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Set 'Rank' column as the index
    df.set_index('Rank', inplace=True)

    # Show top N countries based on the total medals
    st.subheader("Olympics Wrestling Total Medals")
    top_n = st.slider("Select number of top countries to display", min_value=1, max_value=75, value=10)
    top_countries = df.nlargest(top_n, 'Total')
    st.dataframe(top_countries, width=1200)
else:
    st.error("No data found in the MongoDB collection.")

import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

# Configuration
API_KEY = os.getenv("API_KEY")
base_url = os.getenv("base_url")
country_url = os.getenv("country_url")

# Get country names
country_list = requests.get(country_url).json()
countries = [country_list['data'][i]['country'] for i in range(len(country_list['data']))]

st.markdown("<h1 style='text-align: center; color: red;'>Weather Application</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i.ytimg.com/vi/fxJSXBr5hVg/maxresdefault_live.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Country Input ---
selected_countries = st.multiselect("Select Countries:", countries)

# --- Fetch Cities for Selected Countries ---
cities_data = {}
for selected_country in selected_countries:
    country_url = 'https://countriesnow.space/api/v0.1/countries/cities'
    cities_response = requests.post(country_url, json={'country': selected_country})
    cities_data[selected_country] = cities_response.json()['data']

# --- City Input ---
selected_cities = {}
for selected_country in selected_countries:
    if selected_country in cities_data:
        selected_cities[selected_country] = st.multiselect(f"Select Cities in {selected_country}:", cities_data[selected_country])

# --- Fetch Weather Data ---
weather_data = []
if st.button("Get Weather Data"):
    for selected_country in selected_countries:
        if selected_country in selected_cities:
            for selected_city in selected_cities[selected_country]:
                complete_url = f"{base_url}q={selected_city}&appid={API_KEY}&units=metric"
                # Send the GET request
                response = requests.get(complete_url)
                data = response.json()

                # Check if the request was successful
                if response.status_code == 200:
                    # Extract temperature from the response
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']
                    weather_data.append({
                        'country': selected_country,
                        'city': selected_city,
                        'temperature': temperature,
                        'humidity': humidity
                    })

# --- Scatter Plot ---
if weather_data:
    df = pd.DataFrame(weather_data)
    # Calculate min/max humidity with padding
    min_humidity = df['humidity'].min() - df['humidity'].min() * 0.075
    max_humidity = df['humidity'].max() + df['humidity'].max() * 0.075

    fig = px.scatter(df, x='temperature', y='humidity', color='country', title='Temperature vs. Humidity', labels={'temperature': 'Temperature (°C)', 'humidity': 'Humidity (%)'})
    fig.update_layout(yaxis_range=[min_humidity, max_humidity])
    st.plotly_chart(fig)


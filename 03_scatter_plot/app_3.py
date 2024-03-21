import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv("API_KEY")
base_url = os.getenv("base_url")

# --- App Title ---
st.title("Weather Comparison App")

# --- City Input ---
cities = []
for i in range(5):
    city_input = st.text_input(f"Enter City {i+1}:")
    cities.append(city_input)

# --- Fetch Weather Data ---
if st.button("Get Weather Data"):
    weather_data = []
    for city in cities:
        complete_url = f"{base_url}q={city}&appid={API_KEY}&units=metric"
        # Send the GET request
        response = requests.get(complete_url)
        data = response.json()

        # Check if the request was successful
        if response.status_code == 200:
            # Extract temperature from the response
            temperature = data['main']['temp']
            weather_data.append({
                'city': city,
                'temperature': temperature,
                'humidity': "pippo"
            })


# --- Scatter Plot ---
if weather_data:
    import pandas as pd
    df = pd.DataFrame(weather_data)
    st.plotly_chart(df.plot(kind='scatter', x='temperature', y='humidity', title='Temperature vs. Humidity'))

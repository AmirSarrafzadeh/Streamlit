import streamlit as st
import requests

# Configuration
API_KEY = "6931081f8e74ccd1b3b003e99c454c1d"
owm = OpenWeatherMap(API_KEY)

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
        try:
            mgr = owm.weather_at_place(city)
            weather = mgr.weather()
            weather_data.append({
                'city': city,
                'temperature': weather.temperature('celsius')['temp'],
                'humidity': weather.humidity
            })
        except Exception as e:
            st.error(f"Error fetching data for {city}: {e}")

# --- Scatter Plot ---
if weather_data:
    import pandas as pd
    df = pd.DataFrame(weather_data)
    st.plotly_chart(df.plot(kind='scatter', x='temperature', y='humidity', title='Temperature vs. Humidity'))

import streamlit as st
import geopandas as gpd
import pydeck as pdk



st.markdown("<h1 style='text-align: center; color: red;'>Country Map Explorer</h1>", unsafe_allow_html=True)
st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.hdqwalls.com/download/blue-abstract-4k-s6-2880x1800.jpg"); 
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

basemap_styles = {
    "mapbox://styles/mapbox/streets-v11": "Streets",
    "mapbox://styles/mapbox/satellite-streets-v11": "Satellite Streets",
    "mapbox://styles/mapbox/light-v10": "Light",
    "mapbox://styles/mapbox/dark-v10": "Dark"
}

# Dropdown for basemap selection
selected_basemap = st.selectbox("Select basemap style:", list(basemap_styles.values()))

# Get the selected basemap style URL
selected_basemap_url = [k for k, v in basemap_styles.items() if v == selected_basemap][0]

# Load world map data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create a list of unique country names
country_list = sorted(world['name'].unique())

# Dropdown for country selection
selected_country = st.selectbox("Select a country:", country_list)

# Filter for the selected country
country = world[world['name'] == selected_country]

# Ensure a valid country was entered
if not country.empty:
    # Calculate center coordinates of the country
    center_latitude = country.geometry.centroid.y.iloc[0]
    center_longitude = country.geometry.centroid.x.iloc[0]

    # Create the map view
    view_state = pdk.ViewState(
        latitude=center_latitude,
        longitude=center_longitude,
        zoom=4
    )

    # Create the country layer
    layer = pdk.Layer(
        "GeoJsonLayer",
        data=country,
        opacity=0.8,
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="properties.pop_est / 100000",
        get_fill_color="[255, 140, 0]",
        get_line_color="[0, 0, 0]",
    )

    # Render the map
    render_map = pdk.Deck(
        map_style=selected_basemap_url,
        initial_view_state=view_state,
        layers=[layer],
    )
    st.pydeck_chart(render_map)

    caption_style = """
            <style>
            div.caption {
                text-align: center;
                position: absolute;
                bottom: -10px;      
                left: 50%;
                transform: translateX(-50%); 
            }
            </style>
            """

    st.markdown(caption_style, unsafe_allow_html=True)
    st.markdown(f"<div class='caption'>Made with ❤️ by Amir</div>", unsafe_allow_html=True)
else:
    st.error("Country not found. Please try a different one.")

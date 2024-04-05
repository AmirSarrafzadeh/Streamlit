# Importing required libraries
import os
import re
import pandas as pd
import pydeck as pdk
import streamlit as st
import geopandas as gpd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Pattern to extract coordinates
pattern = r'(\d+\.\d+) (\d+\.\d+)'
ICON_URL1 = "https://raw.githubusercontent.com/AmirSarrafzadeh/Streamlit/main/04_routing_app/red_star.png"
ICON_URL2 = "https://img.icons8.com/external-flat-icons-inmotus-design/67/external-Point-road-sign-flat-icons-inmotus-design.png"


# Icon data for the starting and other points
icon_data1 = {
    "url": ICON_URL1,
    "width": 250,
    "height": 250,
    "anchorY": 250,
}

icon_data2 = {
    "url": ICON_URL2,
    "width": 150,
    "height": 150,
    "anchorY": 150,
}

# Functions to extract coordinates from the geometry column of the GeoDataFrame and convert them to a list of lists
def extract_coordinates(line):
    coordinates = re.findall(pattern, str(line))
    formatted_coordinates = [f'[{coord[0]} {coord[1]}]' for coord in coordinates]
    return ', '.join(formatted_coordinates)

# Function to extract the float coordinates from the string coordinates and convert them to a list of lists
def extract_coordinates_1(string):
    coords = string.strip("[]").split("], [")
    return [[float(coord.split()[0]), float(coord.split()[1])] for coord in coords]

# Defining the file paths
file_path = os.path.dirname(__file__)
network_path = os.path.join(file_path, r"shape_files\network\network.shp")
shortest_path = os.path.join(file_path, r"shape_files\shortest_path\shortest_path.shp")

# Reading the data
points_data = pd.read_csv('points.csv')
# roads_data = gpd.read_file(network_path)
shortest_data = gpd.read_file(shortest_path)


shortest_data['formatted_geometry'] = shortest_data['geometry'].apply(extract_coordinates)
all_coordinates = [coordinate for sublist in shortest_data['formatted_geometry'].apply(extract_coordinates_1) for coordinate in sublist]

data = {'path': [all_coordinates], 'color': '[(255, 0, 0)]', 'name': 'Shortest Path'}
shortest_road = pd.DataFrame(data)
shortest_road['color'] = [(0, 0, 255)] * len(shortest_road)

st.markdown("<h1 style='text-align: center; color: red;'>Shortest Path Map</h1>", unsafe_allow_html=True)

# Add a background image to the app
st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://i.pinimg.com/originals/46/2f/56/462f56d9c11e41741daae2c35c70f069.jpg");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Basemap styles
basemap_styles = {
    "mapbox://styles/mapbox/streets-v11": "Streets",
    "mapbox://styles/mapbox/satellite-streets-v11": "Satellite Streets",
    "mapbox://styles/mapbox/light-v10": "Light",
    "mapbox://styles/mapbox/dark-v10": "Dark"
}


points_data["icon_data"] = [icon_data1 if i == 0 else icon_data2 for i in range(len(points_data))]

# Dropdown for basemap selection
selected_basemap = st.selectbox("Select basemap style:", list(basemap_styles.values()))

# Get the selected basemap style URL
selected_basemap_url = [k for k, v in basemap_styles.items() if v == selected_basemap][0]

# Load world map data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Calculate center coordinates of Rome
center_latitude = shortest_data.geometry.centroid.y.mean()
center_longitude = shortest_data.geometry.centroid.x.mean()

# Default map view focused on Rome
view_state = pdk.ViewState(
    latitude=center_latitude,
    longitude=center_longitude,
    zoom=11  # Adjust zoom level as needed
)

circle_layer = pdk.Layer(
    type="IconLayer",
    data=points_data,
    get_position=["lon", "lat"],
    get_icon="icon_data",
    get_size=1.5,
    size_scale=10,
    pickable=True,
)


shortest_layer = pdk.Layer(
    type="PathLayer",
    data=shortest_road,
    pickable=True,
    get_color="color",
    width_scale=2,
    width_min_pixels=2,
    get_path="path",
    get_width=0.5,
)

# If you want to add the network layer, uncomment the code below
# Create the roads layer
# roads_layer = pdk.Layer(
#     "GeoJsonLayer",
#     data=roads_data,
#     opacity=0.8,
#     stroked=True,
#     filled=False,
#     lineWidthMinPixels=0.5,
#     get_line_color=[255, 100, 100],
#     get_line_width=1,
# )

# Add the circle layer to the map
# render_map = pdk.Deck(
#     map_style=selected_basemap_url,
#     initial_view_state=view_state,
#     layers=[shortest_layer, roads_layer, circle_layer],
# )

# If you uncommented the code above, comment the code below
render_map = pdk.Deck(
    map_style=selected_basemap_url,
    initial_view_state=view_state,
    layers=[circle_layer, shortest_layer]
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









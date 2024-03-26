# Shortest Path Mapping Application

This Python application visualizes the shortest path on a map, allowing users to customize the basemap and view points of interest. Key technologies include:

* **Streamlit:** For building the web application interface.
* **Pandas:** For data manipulation and preprocessing.
* **PyDeck:** For generating the interactive map visualization.
* **GeoPandas:** For working with geospatial data.

## Project Structure

* **app.py (or similar):** The main Python script containing the Streamlit application code.
* **points.csv:** A CSV file containing the latitude and longitude coordinates of points of interest.
* **shape_files/network/network.shp:** A Shapefile representing the road network (if used for visualization).
* **shape_files/shortest_path/shortest_path.shp:** A Shapefile containing the geometry of the shortest path.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your_username>/<repository_name>.git
    ```

2. **Navigate to the Project Directory:**
3. **Install the Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Run the Application:**
   ```bash
    streamlit run app_4.py
    ```


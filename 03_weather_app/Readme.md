# Weather Application

A Streamlit-powered web application to visualize and compare weather data for multiple countries and cities.

## Features

* **Interactive Country and City Selection:**  Dynamically fetch and display lists of countries and cities, allowing users to select their desired locations.
* **Weather Data Acquisition:** Retrieves real-time weather information from an external API, including temperature and humidity.
* **Temperature and Humidity Visualization:** Generates a scatter plot to visualize the relationship between temperature and humidity across selected cities and countries.

## Setup

1. **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)<your_username>/<repository_name>.git
    ```

2. **Install Dependencies:**
   ```bash
   cd <repository_name>
   pip install -r requirements.txt 
   

## API Key:

* Obtain a free API key from a weather data provider (e.g., OpenWeatherMap).
* Create a .env file in the project's root directory.
* Add the following lines, replacing the placeholders with your actual API key and any other base URLs used by the application:
```bash 
API_KEY=<your_api_key>

base_url=<api_base_url>

country_url=<api_country_lookup_url> 
```
## Usage

### Start the Application:

```bash
streamlit run app.py 

```

### Interact with the Application:

1. Select a country from the dropdown list.
2. Select a city from the dropdown list.
3. Click the "Get Weather Data" button to fetch and display the weather information.
4. View the scatter plot to visualize the relationship between temperature and humidity for the selected city and country.
5. Repeat the process to compare weather data across multiple locations.
6. Enjoy exploring the weather data!
7. Press `Ctrl+C` in the terminal to stop the application.

## License

Distributed under the MIT License. See `LICENSE` for more information.

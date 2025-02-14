
## Requirements

- Python 3.11
- `requests` library
- `python-dotenv` library
- InfluxDB

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/fvgm-spec/weather-to-influx.git
    cd weather-to-influx
    ```

2. Create a `.env` file in the [src](http://_vscodecontentref_/1) directory with the following content:
    ```env
    OPENWEATHER_API_KEY=your_openweather_api_key
    INFLUXDB_HOST=http://localhost:8086
    INFLUXDB_DATABASE=weather_data
    ```

3. Install the required Python packages:
    ```bash
    pip install requests python-dotenv
    ```

## Usage

### Collect Weather Data

To collect weather data and write it to InfluxDB, run the [weather_collector.py](http://_vscodecontentref_/2) script:

```bash 
python src/weather_collector.py
```

### Fetch Weather Data for Testing
To fetch weather data for a specific city and print it, run the scripts/fetch_weather_test.py script:

```bash 
python src/fetch_weather_test.py
```

### Run Weather Collector Service

To run the weather collector service that collects data at regular intervals, run the `weather_collector_service.py` script:

#### File Descriptions
* weather_collector.py: Main script to collect weather data and write it to InfluxDB.
* weather_collector_service.py: Service script to run the weather collector at regular intervals.
* scripts/fetch_weather_test.py: Script to fetch weather data for a specific city for testing purposes.

#### How It Works
* WeatherCollector Class: This class is responsible for fetching weather data from the OpenWeather API. It uses the API key stored in the .env file to authenticate requests.
* get_weather Method: This method takes a city name as input, constructs the API request, and returns the weather data in JSON format.
* escape_string Function: This function escapes special characters in string values to ensure they are properly formatted for InfluxDB.
* convert_to_line_protocol Function: This function converts the weather data into the InfluxDB line protocol format. It extracts tags (metadata) and fields (measurements) from the data and constructs a line protocol string.
* main Function: This function initializes the WeatherCollector class, iterates over a list of cities, fetches weather data for each city, converts the data to line protocol format, and writes the results to a text file.
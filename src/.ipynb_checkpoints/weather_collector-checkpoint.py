import os
import requests
from datetime import datetime
from dotenv import load_dotenv
#from influxdb3 import InfluxDBClient3, Point
from influxdb_client_3 import InfluxDBClient3, Point

load_dotenv()

class WeatherCollector:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.influx_host = os.getenv('INFLUXDB_HOST', 'http://localhost:8086')
        self.database = os.getenv('INFLUXDB_DATABASE', 'weather_data')

        # InfluxDB Core does not use authentication by default
        self.client = InfluxDBClient3(
            host=self.influx_host,
            database=self.database
        )

    def get_weather(self, city):
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error fetching data for {city}: {response.json().get('message', 'Unknown error')}")
            return None
        return response.json()

    def write_to_influx(self, data):
        if not data or "main" not in data:
            print(f"Skipping InfluxDB write due to invalid data: {data}")
            return

        point = Point("weather") \
            .tag("city", data['name']) \
            .field("temperature", data['main']['temp']) \
            .field("humidity", data['main']['humidity']) \
            .field("pressure", data['main']['pressure']) \
            .time(datetime.utcnow())

        self.client.write(point)
        print(f"Weather data written for {data['name']}")

    def close(self):
        self.client.close()

def main():
    collector = WeatherCollector()
    cities = ["London", "New York", "Tokyo"]

    for city in cities:
        try:
            data = collector.get_weather(city)
            if data:
                collector.write_to_influx(data)
        except Exception as e:
            print(f"Error collecting data for {city}: {e}")

    collector.close()

if __name__ == "__main__":
    main()
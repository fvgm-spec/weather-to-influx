import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class WeatherCollector:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        
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

def escape_string(value):
    """Escape special characters in string values"""
    if isinstance(value, str):
        # Escape spaces and commas in string values
        if ' ' in value or ',' in value:
            return f'"{value}"'
    return str(value)

def convert_to_line_protocol(data):
    """Convert weather data to InfluxDB line protocol format"""
    if not data:
        return None
    
    try:
        # Extract tags (metadata that you want to index)
        tags = {
            'name': escape_string(data['name']),
            'id': str(data['id']),
            'country': data['sys']['country']
        }
        
        # Extract fields (actual measurements)
        fields = {
            'longitude': float(data['coord']['lon']),
            'latitude': float(data['coord']['lat']),
            'temperature': float(data['main']['temp']),
            'feels_like': float(data['main']['feels_like']),
            'temp_min': float(data['main']['temp_min']),
            'temp_max': float(data['main']['temp_max']),
            'pressure': int(data['main']['pressure']),
            'humidity': int(data['main']['humidity']),
            'wind_speed': float(data['wind']['speed']),
            'wind_deg': int(data['wind']['deg']),
            'clouds': int(data['clouds']['all']),
            'visibility': int(data['visibility'])
        }
        
        # Construct tags string - escape any special characters
        tags_str = ','.join(f"{k}={v}" for k, v in tags.items())
        
        # Construct fields string - add proper type suffixes
        fields_str = ','.join(
            f"{k}={v}i" if isinstance(v, int) else f"{k}={v}"
            for k, v in fields.items()
        )
        
        # Get current timestamp in nanoseconds
        timestamp = int(datetime.utcnow().timestamp() * 1e9)
        
        # Construct the line protocol string
        # Format: measurement,tags fields timestamp
        return f"weather_data,{tags_str} {fields_str} {timestamp}"
    
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error converting data for {data.get('name', 'unknown city')}: {str(e)}")
        return None

def main():
    collector = WeatherCollector()
    cities = ["Montevideo", "Sao Paulo", "Caracas", "Santiago", "Medellin", "Quito", "Brasilia"]  # Replace with your full city list
        
    # Open file to write line protocol data
    with open('weather_data.txt', 'w') as f:
        for city in cities:
            try:
                data = collector.get_weather(city)
                if data:
                    line_protocol = convert_to_line_protocol(data)
                    if line_protocol:
                        f.write(line_protocol + '\n')
                        print(f"Data written for {city}")
            except Exception as e:
                print(f"Error collecting data for {city}: {e}")

if __name__ == "__main__":
    main()
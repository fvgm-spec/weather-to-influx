import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Make sure you have a .env file with OPENWEATHER_API_KEY set.")

    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))  # Pretty-print the JSON response
        return data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Read city name from command-line argument
if len(sys.argv) > 1:
    city_name = sys.argv[1]
else:
    city_name = input("Enter city name: ")

weather_data = get_weather(city_name)

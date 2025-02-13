import requests
import json

url = "http://api.openweathermap.org/data/2.5/weather"
api_key='bbf79e1e8eec67b0931be0b930ddb346'
city = "Montevideo"
params = {
             'q': city,
             'appid': api_key,
             'units': 'metric'
         }

response = requests.get(url, params=params)
if response.status_code != 200:
    print(f"Error fetching data for {city}: {response.json().get('message', 'Unknown error')}")
else:
    print(response.json())
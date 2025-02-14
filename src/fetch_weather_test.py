 
import os
import requests 
from dotenv 
import load_dotenv 

# Load environment variables 
load_dotenv() 

def get_weather(city): 
    api_key = os.getenv("OPENWEATHER_API_KEY") # Load API key from .env 
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
        return response.json() 
    else: 
        print(f"Error: {response.status_code}, {response.text}") 
        return None
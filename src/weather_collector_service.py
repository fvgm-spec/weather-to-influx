#!/usr/bin/env python3
import time
import subprocess
import sys
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    filename='weather_collector.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_weather_collector():
    try:
        # Run the weather collector script
        subprocess.run(['python3', 'weather_collector.py'], check=True)
        
        # Write to InfluxDB
        result = subprocess.run(
            ['influxdb3', 'write', '--database=mydb', '--file=weather_data.txt'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Log success
        logging.info("Data collection and write successful")
        
        # Clean up the temporary file
        if os.path.exists('weather_data.txt'):
            os.remove('weather_data.txt')
            
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running collection process: {e.output}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def main():
    logging.info("Weather collector service started")
    
    while True:
        start_time = time.time()
        
        # Run the collection process
        run_weather_collector()
        
        # Calculate sleep time to maintain 5-second intervals
        elapsed_time = time.time() - start_time
        sleep_time = max(0, 5 - elapsed_time)  # Ensure non-negative sleep time
        
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
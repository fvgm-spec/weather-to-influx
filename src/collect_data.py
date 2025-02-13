from weather_collector import WeatherCollector

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
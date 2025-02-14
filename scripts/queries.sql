##Get the Average Temperature Per Country

influxdb3 query --database=mydb \
"SELECT country, AVG(temperature) AS avg_temp FROM weather_data GROUP BY country"

## Get the Maximum and Minimum Temperature
influxdb3 query --database=mydb \
"SELECT MAX(temperature) AS max_temp, MIN(temperature) AS min_temp FROM weather_data"

## Find the Windiest City
influxdb3 query --database=mydb \
"SELECT name, MAX(wind_speed) AS max_wind FROM weather_data GROUP BY name ORDER BY max_wind DESC LIMIT 1"

## Count the Number of Entries Per Country
influxdb3 query --database=mydb \
"SELECT country, COUNT(*) AS data_points FROM weather_data GROUP BY country ORDER BY data_points DESC"

## Find the Most Humid City
influxdb3 query --database=mydb \
"SELECT name, MAX(humidity) AS max_humidity FROM weather_data GROUP BY name ORDER BY max_humidity DESC LIMIT 1"

## Get the Latest Weather Data
influxdb3 query --database=mydb \
"SELECT * FROM weather_data ORDER BY time DESC LIMIT 10"

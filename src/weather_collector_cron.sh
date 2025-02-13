#!/bin/bash
while true
do
    python /home/felix/weather-to-influx/src/weather_collector.py
    sleep 5
done

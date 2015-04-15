#!/usr/bin/python

# System libraries

import RPi.GPIO as GPIO
import time

# Custom libraries

import dht11

while True:
    temperature = getTemperatureHumidity(4, 0)
    humidity = getTemperatureHumidity(4, 1)
    # pressure = getPressure(pin)

    print("Temperature: " + temperature + "°C")
    print("Humidity: " + humidity + "%")
    print("Pressure: " + pressure + "hPa")

    request = "{'temperature': " + temperature + ", 'humidity': " + humidity + ", 'pressure': " + pressure + "}"

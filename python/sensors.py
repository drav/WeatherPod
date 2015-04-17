#!/usr/bin/python

# System libraries

import RPi.GPIO as GPIO
import time
import sys

# Custom libraries

import dht11
import bmp180

# Pins arguments

try:
    dht11Pin = int(sys.argv[1])
    bmp180Pin = int(sys.argv[2])

except:
    print("Usage: " + sys.argv[0] + " [DHT11 Pin] [BMP180 Pin]")
    sys.exit(0)


while True:
    temperature = getTemperatureHumidity(dht11Pin, "temp")
    humidity = getTemperatureHumidity(dht11Pin, "hum")
    # pressure = getPressure(pin)

    print("Temperature: " + temperature + "°C")
    print("Humidity: " + humidity + "%")
    print("Pressure: " + pressure + "hPa")

    request = "{'temperature': " + temperature + ", 'humidity': " + humidity + ", 'pressure': " + pressure + "}"

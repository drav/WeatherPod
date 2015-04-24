#!/usr/bin/python

# Import libraries

import argparse
import requests
import threading

# Pins arguments

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", help = "sends fake random data to the server for testing purposes", action = "store_true")
parser.add_argument("-v", "--verbose", help = "increases command line verbosity", action = "store_true")
parser.add_argument("dht11Pin", help = "DHT11 data pin number", type = int)
parser.add_argument("serverURL", help = "WeatherPod server URL/IP", type = str)
args = parser.parse_args()

# Import random if random mode is enable, GPIO library if not

if args.random:
    import random

else:
    import RPi.GPIO as GPIO
    import dht11
    # import bmp180

def sendData():
    threading.Timer(1.0, sendData).start()

    if args.random:
        # Randomly generate fake data

        temp = random.randint(1, 40)
        hum = random.randint(0, 90)
        pres = random.randint(1000, 1090)
        alti = random.randint(100, 300)

    else:
        temp = int(dht11.getData(int(args.dht11Pin))[temp])
        hum = int(dht11.getData(int(args.dht11Pin))[hum])
        # pres = int(bpm180.getData()[pres])
        # alti = int(bmp180.getData()[alti])

    # Output data to the console if verbose mode enabled

    if args.verbose:
        print(u"Temperature: " + str(temp) + u"°C")
        print(u"Humidity: " + str(hum) + u"%")
        # print("Pressure: " + str(pres) + "hPa")
        # print("Altitude: " + str(alti) + "m")

    # Send data to the server using an HTTP GET request

    try:
        requests.get("http://" + args.serverURL + "/newdata/" + str(temp) + "/" + str(hum) + "/" + str(pres) + "/" + str(alti))

        if args.verbose:
            print("Data sent.")

    except requests.exceptions.RequestException as e:
        print("HTTP GET request error: " + str(e))

    pass

sendData()

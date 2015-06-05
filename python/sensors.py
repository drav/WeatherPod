#!/usr/bin/env python
# coding: utf-8

""" An open-source connected sensors board for weather balloons. Uses Python, Node.JS, a Raspberry Pi and a little bit of solder. """

# Import libraries

import argparse
import requests
import threading
import signal
import sys
import time

__author__ = "Loan Laux"
__copyright__ = "Copyright 2015"
__credits__ = ["Julie Dubois", "Daniel Sanchez-Palma", "Rafael Magisson", "Bruno Masi"]
__license__ = "MIT"
__maintainer__ = "Loan Laux"
__email__ = "contact@loanlaux.fr"
__status__ = "Development"

# Arguments parsing

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", help = "sends fake random data to the server for testing purposes", action = "store_true")
parser.add_argument("-v", "--verbose", help = "increases command line verbosity", action = "store_true")
parser.add_argument("--led", nargs = "?", help = "Status LED pin number (in board mode)", type = int)
parser.add_argument("dht11Pin", help = "DHT11 data pin number (in board mode)", type = int)
parser.add_argument("serverURL", help = "WeatherPod server URL/IP", type = str)
args = parser.parse_args()

# Import random if random mode is enable, GPIO and sensors modules if not

if args.random:
    import random

    if args.led:
        import RPi.GPIO as GPIO

else:
    import RPi.GPIO as GPIO
    import dht11
    import Adafruit_BMP.BMP085 as BMP085

    BMP180 = BMP085.BMP085()

def signalHandler(signal, frame):
    if args.led:
        GPIO.cleanup()

    sys.exit(0)

signal.signal(signal.SIGINT, signalHandler)

def ledSetup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(args.led, GPIO.OUT)
    GPIO.output(args.led, GPIO.LOW)

def sendData():
    """ Sends data to server using an HTTP GET request every second. """

    dataLoop = threading.Timer(1.0, sendData)
    dataLoop.setDaemon(True)
    dataLoop.start()

    if args.random:
        # Randomly generate fake data

        temp = random.randint(1, 40)
        hum = random.randint(0, 90)
        pres = random.randint(1000, 1090)
        alti = random.randint(100, 300)

    else:
        # Acquire data from the sensors

        try:
            hum = int(dht11.getData(int(args.dht11Pin)))

        except:
            hum = None

        temp = int(BMP180.read_temperature())
        pres = int(BMP180.read_pressure() / 100)
        alti = int(BMP180.read_altitude())

    # Output data to the console if verbose mode enabled

    if args.verbose:
        if hum:
            print(u"Humidity: " + str(hum) + u"%")

        print(u"Temperature: " + str(temp) + u"C")
        print(u"Pressure: " + str(pres) + u"hPa")
        print(u"Altitude: " + str(alti) + u"m")

    # Send data to the server using an HTTP GET request

    try:
        requests.get("http://" + args.serverURL + "/newdata/" + str(temp) + "/" + str(hum) + "/" + str(pres) + "/" + str(alti))

        if args.led:
            GPIO.output(args.led, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(args.led, GPIO.LOW)

        if args.verbose:
            print("Data sent.")

    except requests.exceptions.RequestException as e:
        print("HTTP GET request error: " + str(e))

    pass

if args.led:
    ledSetup()

sendData()
signal.pause()

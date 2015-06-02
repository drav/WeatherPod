#!/usr/bin/env python
# coding: utf-8

import argparse
import Adafruit_BMP.BMP085 as BMP085

# Arguments parsing

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--temperature", help = "returns temperature in Celcius", action = "store_true")
parser.add_argument("-p", "--pressure", help = "returns atmospheric pressure in Pascals", action = "store_true")
parser.add_argument("-a", "--altitude", help = "returns absolute altitude in meters", action = "store_true")
args = parser.parse_args()

BMP180 = BMP085.BMP085()

if args.temperature:
    print(BMP180.read_temperature())

elif args.pressure:
    print(BMP180.read_pressure())

elif args.altitude:
    print(BMP180.read_altitude())

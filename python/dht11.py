#!/usr/bin/python

import RPi.GPIO as GPIO
import time

def bin2dec(string_num):
    return str(int(string_num, 2))

class RangeError(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)


def getData(pin):

    # if (not pin) or (type(pin) != "int"):
    #    raise ValueError("Bad argument. Usage: getData(<pin>)")

    data = []

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.025)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.02)

    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for i in range(0, 500):
        data.append(GPIO.input(pin))

    bit_count = 0
    tmp = 0
    count = 0
    humidityBit = ""
    temperatureBit = ""
    crc = ""

    try:
    	while data[count] == 1:
    		tmp = 1
    		count = count + 1

    	for i in range(0, 32):
    		bit_count = 0

    		while data[count] == 0:
    			tmp = 1
    			count = count + 1

    		while data[count] == 1:
    			bit_count = bit_count + 1
    			count = count + 1

    		if bit_count > 3:
    			if i>=0 and i<8:
    				humidityBit = humidityBit + "1"
    			if i>=16 and i<24:
    				temperatureBit = temperatureBit + "1"
    		else:
    			if i>=0 and i<8:
    				humidityBit = humidityBit + "0"
    			if i>=16 and i<24:
    				temperatureBit = temperatureBit + "0"

    except:
    	raise RangeError("Range Error occured.")

    try:
    	for i in range(0, 8):
    		bit_count = 0

    		while data[count] == 0:
    			tmp = 1
    			count = count + 1

    		while data[count] == 1:
    			bit_count = bit_count + 1
    			count = count + 1

    		if bit_count > 3:
    			crc = crc + "1"
    		else:
    			crc = crc + "0"
    except:
    	raise RangeError("Range Error occured.")

    humidity = bin2dec(humidityBit)
    temperature = bin2dec(temperatureBit)

    if int(humidity) + int(temperature) - int(bin2dec(crc)) == 0:
        return "{ 'temp': " + str(temperature) + ", 'hum': " + str(humidity) + " }"

    else:
    	print("ERR_CRC")

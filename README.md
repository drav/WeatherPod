# WeatherPod

## A lightweight, open-source and easy to setup sensors board for weather balloons

This source code is released as part of a 12th grade engineering sciences project. The goal was to provide an open-source, affordable, and easy to setup sensors pod for weather balloons enthusiasts with a bit of knowledge in electronics.

WeatherPod is designed to work on a Raspberry Pi (or a similar nano-computer if you feel like tweaking the code a little!) with a Bosh BMP180 I2C pressure and temperature sensor, as well as a DHT11 for humidity measurements. On the server side, it features a Node.JS app that -using Socket.io- displays the values sent by the embedded system on a comprehensive web interface. The link between these two is made thanks to a 3G modem.

Python script should be used this way:

    sudo python sensors.py [-h] [-r] [-v] [--led [LEDPin]] dht11Pin serverURL

More info by displaying the help section using -h.

Node.JS app only takes one argument needed to work properly:

    node app.js portNumber

So that you can choose which port to run the server on.

What are you waiting for? Go build your balloon and have some fun!

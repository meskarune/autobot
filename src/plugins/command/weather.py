#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that gives the weather"""

import configparser
import json
from urllib.parse import quote_plus
from requests import get


def getweather(city, location=''):
    """Get wearther and return the result"""
    config = configparser.ConfigParser()
    config.read("plugins/command/weather.conf")
    api = config.get("Key", "api_key")
    try:
        query = "http://api.openweathermap.org/data/2.5/weather?q={0},{1}&units=imperial&APPID={2}".format(quote_plus(city), quote_plus(location), api)
        response = json.loads(get(query).text)
        if response:
            location = response['name']
            conditions = response["weather"][0]["main"]
            tempurature = float(response['main']['temp'])
            tempC = (tempurature - 32.0) / (9.0/5.0)
            humidity = float(response['main']['humidity'])
            windspeed = response['wind']['speed']
            if tempurature:
                return "The current weather for {0} is {1}°F ({2}°C) {3} {4}% humidity with {5}mph winds".format(location, round(tempurature), round(tempC), conditions, round(humidity), round(windspeed))
            else:
                return "Not found, please try again with new parameters"
    except:
        return

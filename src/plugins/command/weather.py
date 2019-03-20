#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that gives the weather"""

import configparser
import json
from urllib.parse import quote_plus
from requests import get


def parseweather(url, units):
    icon_list = {
        "01": "☀",
        "02": "🌤",
        "03": "🌥",
        "04": "☁",
        "09": "🌧",
        "10": "🌦",
        "11": "🌩",
        "13": "🌨",
        "50": "🌫",
    }
    if units == "imperial":
        measure = "°F"
        speed = "mph"
    else:
        measure = "°C"
        speed = "kph"
    try:
        weather_response = json.loads(get(url).text)
        if weather_response:
            location = weather_response["name"]
            conditions = weather_response["weather"][0]["main"]
            tempurature = float(weather_response['main']['temp'])
            icon = weather_response["weather"][0]["icon"]
            humidity = float(weather_response['main']['humidity'])
            windspeed = weather_response['wind']['speed']
            if tempurature:
                return "The current weather for {0} is {1}{2} {3}  {4}, {5}% humidity with {6}{7} winds".format(
                    location, round(tempurature), measure,
                    icon_list.get(icon[:2]), conditions, round(humidity),
                    round(windspeed), speed)
    except:
        return "There was an error getting the weather data."

def getweather(location):
    """Get wearther and return the result"""
    config = configparser.ConfigParser()
    config.read("plugins/command/weather.conf")
    geocode_api = config.get("Key", "api_key_geocode")
    weather_api = config.get("Key", "api_key_weather")
    geocode_url = "http://open.mapquestapi.com/geocoding/v1/address?key={0}&location={1}".format(
        geocode_api, quote_plus(location))
    try:
        geocode_response = json.loads(get(geocode_url).text)
        if geocode_response:
            lat = geocode_response["results"][0]["locations"][0]["latLng"]["lat"]
            lon = geocode_response["results"][0]["locations"][0]["latLng"]["lng"]
            country = geocode_response["results"][0]["locations"][0]["adminArea1"]
            if country == "US":
                cf = "imperial"
            else:
                cf = "metric"
    except:
        return
    weather_url = "https://api.openweathermap.org/data/2.5/weather?appid={0}&units={1}&lat={2}&lon={3}".format(
        weather_api, cf, lat, lon)
    reply = parseweather(weather_url, cf)
    return reply

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that returns a search result"""

import re
import json
from urllib.parse import quote_plus
from requests import get
from bs4 import BeautifulSoup

def ddg(search):
    """Search duck duck go and return the first url from the restuls"""
    if search[0].startswith("!"):
        try:
            query = "http://api.duckduckgo.com/?q={0}&format=json&no_html=1&no_redirect=1".format(quote_plus(search))
            results = json.loads(get(query).text)
            if results['Redirect']:
                link = results['Redirect']
            else:
                link = "None"
        except:
            return
    else:
        try:
            site = get("http://duckduckgo.com/lite/?q={0}&kl=us-en".format(search + " -site:yahoo.com")).text
        except:
            return
        try:
            parsed = BeautifulSoup(site, "html.parser")
        except:
            return
        try:
            link = parsed.findAll('a', {'class': 'result-link'})[0]['href']
        except:
            return
    if len(link) > 250:
        return "{0}…".format(link[0:250])
    else:
        return link

def wiki(search):
    """Search Wikipedia and return a short description and Link to the result"""
    try:
        query = "https://en.wikipedia.org/w/api.php?action=opensearch&search={0}&format=json".format(quote_plus(search))
        results = json.loads(get(query).text)
        link = results[3][0]
        description = results[2][0]
        if description:
            if len(description) > 250:
                data = "{0}… - {1}".format(description[0:250],link)
            else:
                data = "{0} - {1}".format(description,link)
        else:
            data = link
    except:
        return
    return data

def alwiki(search):
    """Search the arch linux wiki and return a Link to the result"""
    try:
        query = "https://wiki.archlinux.org/api.php?action=opensearch&search={0}&format=json".format(quote_plus(search))
        results = json.loads(get(query).text)
        description = results[1][0]
        link = results[3][0]
        if description:
            if len(description) > 250:
                data = "{0}… - {1}".format(description[0:250],link)
            else:
                data = "{0} - {1}".format(description,link)
        else:
            data = link
    except:
        return
    return data

def github(search):
    """Search github repositories"""
    try:
        query = "https://api.github.com/search/repositories?q={0}".format(quote_plus(search))
        results = json.loads(get(query).text)
        description = results['items'][0]['description']
        link = results['items'][0]['html_url']
        if description:
            if len(description) > 250:
                data = "{0}… - {1}".format(description[0:250],link)
            else:
                data = "{0} - {1}".format(description,link)
        else:
            data = link
    except:
        return
    return data

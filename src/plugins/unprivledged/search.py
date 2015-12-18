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
            site = get("http://duckduckgo.com/html/?q={0}&kl=us-en".format(search + " -site:yahoo.com")).text
        except:
            return
        try:
            parsed = BeautifulSoup(site, "html.parser")
        except:
            return
        try:
            link = parsed.findAll('div', {'class': re.compile('links_main*')})[0].a['href']
        except:
            return
    if len(link) > 250:
        return link[0:250] + '…'
    else:
        return link

def wiki(search):
    """Search Wikipedia and return a short description and Link to the result"""
    try:
        query = "https://en.wikipedia.org/w/api.php?action=opensearch&search={0}&format=json".format(quote_plus(search))
        results = json.loads(get(query).text)
        description = results[2][0]
        if description:
            if len(description) > 250:
                data = description[0:250] + '…' + " - " + results[3][0]
            else:
                data = description + " - " + results[3][0]
        else:
            data = results[3][0]
    except:
        return
    return data

def alwiki(search):
    """Search the arch linux wiki and return a Link to the result"""
    try:
        query = "https://wiki.archlinux.org/api.php?action=opensearch&search={0}&format=json".format(quote_plus(search))
        results = json.loads(get(query).text)
        description = results[1][0]
        if description:
            if len(description) > 250:
                data = description[0:250] + '…' + " - " + results[3][0]
            else:
                data = description + " - " + results[3][0]
        else:
            data = results[3][0]
    except:
        return
    return data

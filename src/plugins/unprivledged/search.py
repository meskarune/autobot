#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that returns a search result"""

import re
import json
from requests import get
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

def ddg(search):
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
            site = get("http://duckduckgo.com/html/?q={0}&kl=us-en".format(search)).text
        except:
            return
        try:
            parsed = BeautifulSoup(site)
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

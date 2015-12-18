#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that returns a search result"""

import re
from requests import get
from bs4 import BeautifulSoup

def ddg(search):
    try:
        site = get("http://duckduckgo.com/html/?q={0}&kl=us-en".format(search)).text
    except:
        return
    try:
        parsed = BeautifulSoup(site)
    except:
        return
    return parsed.findAll('div', {'class': re.compile('links_main*')})[0].a['href']

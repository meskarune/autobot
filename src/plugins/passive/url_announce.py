#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that announces the title for urls in IRC channels"""

import encodings
from requests import get
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

def parse_url(url):
    """Say Website Title information in channel"""
    #if urlopen(url).getcode() == 200:
    baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=urlsplit(url))
    path = urlsplit(url).path
    query = '?{uri.query}'.format(uri=urlsplit(url))
    try:
        headers = {'Accept-Encoding': 'utf-8',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'}
        response = get(baseurl + path + query, headers=headers)
    except:
        return
    try:
        URL = BeautifulSoup(response.text, "html.parser")
    except:
        return
    if not URL.title:
        return
    if URL.title.string is None:
        return
    if len(URL.title.string) > 250:
        title=URL.title.string[0:250] + '…'
    else:
        title=URL.title.string
    return title.replace('\n', ' ').strip() + " (" + urlsplit(url).netloc + ")"

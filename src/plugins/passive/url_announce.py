#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that announces the title for urls in IRC channels"""

import encodings
from urllib.request import urlopen, Request
from urllib.parse   import quote, urlsplit
from urllib.error import URLError
from bs4 import BeautifulSoup

def parse_url(url):
    """Say Website Title information in channel"""
    #if urlopen(url).getcode() == 200:
    baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=urlsplit(url))
    path = urlsplit(url).path
    query = '?{uri.query}'.format(uri=urlsplit(url))
    try:
        request = Request(baseurl.encode("idna").decode("idna") + path + query)
        request.add_header('Accept-Encoding', 'utf-8')
        request.add_header('User-Agent', 'Mozilla/5.0')
        response = urlopen(request)
    except UnicodeEncodeError:
        request = Request(baseurl.encode("idna").decode("idna") + quote(path + query, safe='/#:=&?'))
        request.add_header('Accept-Encoding', 'utf-8')
        response = urlopen(request)
    except:
        return
    try:
        URL = BeautifulSoup(response.read(), "html.parser")
    except URLError as e:
        sys.stderr.write("Error when fetching " + url + ": %s\n" % (e))
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

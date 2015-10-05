#!/usr/bin/python

#import re
import urllib.request
from bs4 import BeautifulSoup

#string = "This is a link http.google.com"

#regex = re.compile(
#        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)'
#        r'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))'
#        r'+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|'
#        r'''[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', re.IGNORECASE)

#match = regex.search(string)

#url = urllib.request.urlopen(match.group(0).strip())

#if url is not None and url.group(0) is not None:
#    print (url.group(0).strip())
#else:
#    print ("There are no urls in the text")

url = urllib.request.urlopen("http://www.pinterest.com")
soup = BeautifulSoup(url, "html.parser")
print (soup.title.string)

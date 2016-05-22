#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that stores keyword/response pairs and returns them"""

import json
import os.path

class FactInfo(object):
    def __init__(self):
        """Create the db if it doesn't exist"""
        self.schema = {"admins":[],"factinfo":{}}
        self.db = "factinfo.json"
        if os.path.isfile(db) is False:
            """create the json file"""
            jsonData = schema
            with open(db, 'w') as jsonFile:
                json.dump(jsonData,jsonFile, sort_keys = True,
                          indent = 4, ensure_ascii=False)
        try:
            with open(db, encoding='utf-8') as jsonFile:
                self.results = json.loads(jsonFile.read())
        except ValueError as err:
            sys.stderr.write("Error with factinfo.json: " + err + " \n")
        except:
            return
    def fcaddadmin(nick):
        """Add nick to admins: list"""

    def fcaddkey(keyword,response):
        """Add a factinfo entry"""

    def fcget(keyword, user):
        """Pull factinfo response from the database"""
        try:
            response = self.results['factinfo'][keyword]
            return response.format(user)
        except:
            return False

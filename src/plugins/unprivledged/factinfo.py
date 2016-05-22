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
            with open(db, 'w') as outfile
                json.dump(jsonData, outfile, sort_keys = True,
                          indent = 4, ensure_ascii=False)
        try:
            self.results = json.loads(get(self.db).text)
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
            return

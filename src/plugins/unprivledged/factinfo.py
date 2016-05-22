#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that returns a search result"""

import json

class FactInfo(object):
    def __init__(self):
        """Create the db if it doesn't exist"""
        self.schema = {"admins":[],"factinfo":{}}
        self.db = "factinfo.json"
        if os.path.exists(db) is False:
            """create the json file"""
            jsonData = schema
            with open(db, 'w') as outfile
                json.dump(jsonData, outfile, sort_keys = True,
                          indent = 4, ensure_ascii=False)
    def fcaddadmin(nick):
        """Add nick to admins: list"""

    def fcaddkey(keyword,response):
        """Add a factinfo entry"""

    def fcget(keyword, user):
        """Pull factinfo response from the database"""
        try:
            db = "factinfo.json"
            results = json.loads(get(db).text)
            response = results['factinfo'][keyword]
            return response.format(user)
        except ValueError as err:
            sys.stderr.write("Error with factinfo.json: " + err + " \n")
        except:
            return

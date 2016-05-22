#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A plugin for Autobot that returns a search result"""

import json

class FactInfo(object):
    def __init__(self):
        """Create the db if it doesn't exist and check for errors if it does"""
        self.schema = {"admins":[],"factinfo":{}}
        self.db = "factinfo.json"
        if os.path.exists(db) is False:
            """create the json file"""
            jsonData = schema
            with open(db, 'w') as outfile
                json.dump(jsonData, outfile, sort_keys = True,
                          indent = 4, ensure_ascii=False)
        else:
            results = json.loads(get(self.db).text)
            """check for errors and say something useful"""
            try:
                sys.stderr.write("Json database initiated \n")
            except:
                sys.stderr.write("Json database has errors \n")
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
        except:
            return

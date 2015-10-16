#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Handle Log Files"""

import datetime


class handle_log():
"""Open, write and close files"""
    def __init__(self, log):
        """open files"""
        self.log = open(log_file, 'a')

    def write(self, logs):
        """write to files"""
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.log.write("%s <%s> %s\n" % (timestamp, nick, message))

    def close(self, logs):
        """close files"""
        self.log.close()

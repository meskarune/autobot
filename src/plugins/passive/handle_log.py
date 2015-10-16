#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Handle Log Files"""

import sys
import os
import datetime


class handle_logs(object):
    """Open, write and close files"""
    def __init__(self, path):
        """Create dirs if they don't exist and open files"""
        if os.path.exists(path) is False:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
            except OSError as err:
                sys.stderr.write("Error when making log path for " + path + ": %s\n" % (path, err))
        try:
            self.log = open(path, 'a')
        except PermissionError as err:
            sys.stderr.write("Permission error: " + err)
        except:
            sys.stderr.write("Error opening log " + path)

    def write(self, message):
        """write to files"""
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.log.write("%s %s\n" % (timestamp, message))
        except:
            sys.stderr.write("Error writting to log " + path)

    def close(self, path):
        """close files"""
        self.log.close(path)

#def logmessage(self, channel, nick, message):
#    """Create IRC logs"""
#    self.logs = {}
#    for ch in self.channels:
#        log_path = datetime.datetime.utcnow().strftime("./logs/%%s") % (channel)
#        log_name = datetime.datetime.utcnow().strftime("%Y-%m-%%s.log") % (channel)
#        log_file = log_path + "/" + log_name
#        self.logs[ch] = handle_logs(log_file)
#
#    self.logs[channel].write("<%s> %s" % (nick, message))
#
#def log_close(self):
#    for ch in self.channels:
#        self.logs[ch].close()

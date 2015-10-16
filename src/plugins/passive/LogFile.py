#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create log file objects"""

import sys
import os
import datetime


class LogFile(object):
    """Handle open/write/close of file with error checking"""
    def __init__(self, path):
        """Create dirs if they don't exist and open file"""
        self.path = path
        if os.path.exists(path) is False:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
            except OSError as err:
                sys.stderr.write("Error when making log path for {0} - {1}\n".format(path, err))
        try:
            self.log = open(path, 'a')
        except PermissionError as err:
            sys.stderr.write("Permission error: " + err)
        except:
            sys.stderr.write("Error opening log " + path)

    def write(self, message):
        """write to file"""
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.log.write("{0} {1}\n".format(timestamp, message))
        except:
            sys.stderr.write("Error writting to log " + self.path)

    def close(self):
        """close file"""
        self.log.close(self.path)

#def logmessage(self, channel, nick, message):
#    """Create IRC logs"""
#    self.logs = {}
#    for ch in self.channels:
#        log_file = datetime.datetime.utcnow().strftime("./logs/{channel}/%Y-%m-{channel}.log").format(channel=ch)
#        self.logs[ch] = LogFile(log_file)
#
#    self.logs[channel].write("<{0}> {1}".format(nick, message))
#
#def log_close(self):
#    for channel in self.channels:
#        self.logs[channel].close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create log file objects"""

import sys
import os
import datetime
import time


class LogFile(object):
    """Handle open/write/close of file with error checking"""
    def __init__(self, path):
        """Create dirs if they don't exist and open file"""
        self.path = path
        self.last_write = 0
        if os.path.exists(path) is False:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
            except OSError as err:
                sys.stderr.write("Error when making log path for {0} - {1}\n".format(path, err))
        self.open()

    def open(self):
        try:
            self.log = open(self.path, 'a')
            sys.stderr.write("opening " + self.path + "\n")
        except PermissionError as err:
            sys.stderr.write("Permission error: " + err + "\n")
        except:
            sys.stderr.write("Error opening log " + self.path + "\n")

    def write(self, message):
        """write to file"""
        if self.log.closed:
            self.open()
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.log.write("{0} {1}\n".format(timestamp, message))
            self.last_write = int(time.time())
        except:
            sys.stderr.write("Error writting to log " + self.path + "\n")

    def is_stale(self, timestamp):
        if timestamp - self.last_write <= 900:
            return False
        else:
            return True

    def close(self):
        """close file"""
        if not self.log.closed:
            self.log.close()
            sys.stderr.write("Log closed " + self.path + "\n")
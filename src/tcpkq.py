#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import select
import threading
import sys


class announce():
    """ Return message uppercase """
    def __init__(self):
        """Start the tcp server in a new thread"""
        host = "localhost"
        port = 8888
        new_thread = TCPserver(self, host, port)
        new_thread.start()
        print("started tcp listener")
    def uppercase(self, message):
        print (message.upper())

class TCPserver(threading.Thread):
    def __init__(self, announce, host, port):
        threading.Thread.__init__(self)
        self.announce = announce
        self.host = host
        self.port = port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self._socket.settimeout(None)
        self._socket.setblocking(0)
        self._socket.bind((self.host, self.port))
        self._socket.listen(5)

        self.kq = select.kqueue()

        self.kevent = [
                   select.kevent(self._socket.fileno(),
                   filter=select.KQ_FILTER_READ,
                   flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE)
        ]

        self.connections = {}

    def run(self):
        try:
            while True:
                events = self.kq.control(self.kevent, 5, None)
                for event in events:
                    if event.ident == self._socket.fileno():
                        try:
                            conn, addr = self._socket.accept()
                        except (IOError, OSError) as e:
                            if e.args[0] == errno.EINTR:
                                continue
                            else:
                                yield data
                        new_event = [
                                 select.kevent(conn.fileno(),
                                 filter=select.KQ_FILTER_READ,
                                 flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE)
                        ]
                        self.kq.control(new_event, 0, 0)
                        self.connections[conn.fileno()] = conn
                    else:
                        conn = self.connections[event.ident]
                        buf = conn.recv(1024)
                        if not buf:
                            conn.close()
                            continue
                        self.announce.uppercase(buf.decode("utf-8", "replace").strip())
        finally:
            self.kq.control([select.kevent(self._socket.fileno(), filter=select.KQ_FILTER_READ, flags=select.KQ_EV_DELETE)], 0, None)
            self.kq.close()
            self._socket.close()

class TCPrequestHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):

def main():
    announce()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio


class announce():
    """ Return message uppercase """
    def __init__(self, host, port):
        """ Start the tcp server """
        print("starting the TCP listener on port {0}".format(port))
        TCPserver(self, host, port)
    def msg(self, message):
        print (message)

class TCPserver():
    def __init__(self, announce, host, port):
        self.announce = announce
        self.host = host
        self.port = port
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle_echo, self.host, self.port, loop=loop)
        server = loop.run_until_complete(coro)
        try:
            loop.run_forever()
        except:
            server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    @asyncio.coroutine
    def handle_echo(self, reader, writer):
        data = yield from reader.read(100)
        message = data.decode("utf-8")
        addr = writer.get_extra_info('peername')
        self.announce.msg("Received {0} from {1}".format(message,addr))
        writer.write(data.upper())
        yield from writer.drain()
        writer.close()

def main():
    announce("127.0.0.1", 2000)

if __name__ == "__main__":
    main()

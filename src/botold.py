#!/usr/bin/env python

import configparser, socket, select, sys, ssl, time
import irc.bot
from threading import Thread

# Create our bot class
class AutoBot ( irc.bot.SingleServerIRCBot ):
    def __init__(self, nick, name, channels, network, listenhost, listenport, port=6667, usessl=False):
        if usessl:
            factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        else:
            factory = irc.connection.Factory()
        irc.bot.SingleServerIRCBot.__init__(self, [(network, port)], nick, name, connect_factory = factory)

        self.nick = nick
        self.channel_list = channels

        self.inputthread = TCPinput(self.connection, self, listenhost, listenport)
        self.inputthread.start()

    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")

    def on_welcome ( self, connection, event ):
        for channel in self.channel_list:
            connection.join(channel)

    def on_pubmsg (self, connection, event):
        channel = event.target
        if event.arguments[0].startswith("!"):
            if self.channels[channel].is_oper(event.source.nick):
                self.do_command(event, True, channel, event.arguments[0].lstrip("!").lower())
            else:
                self.do_command(event, False, channel, event.arguments[0].lstrip("!").lower())

    def do_command (self, event, isOper, source, command):
        user = event.source.nick
        if command == "hello":
            self.say(source, "hello " + user)
        elif command == "goodbye":
            self.say(source, "goodbye " + user)
        elif command == "help":
            self.say(source, "Available commands: ![hello, goodbye, die, help]")
        elif command == "die":
            if isOper:
                self.die(msg="Bye, cruel world!")
            else:
                self.say(source, "You don't have permission to do that")
        else:
            self.connection.notice( user, "I'm sorry, " + user + ". I'm afraid I can't do that")

    def announce (self, connection, text):
        for channel in self.channel_list:
            connection.notice(channel, text)

    def say(self, target, text):
        """Send message to IRC and log it"""
        self.connection.privmsg(target, text)

class TCPinput (Thread):
    def __init__(self, connection, AutoBot, listenhost, listenport):
        Thread.__init__(self)
        self.setDaemon(1)
        self.AutoBot = AutoBot
        self.listenport = listenport
        self.connection = connection

        self.accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accept_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.accept_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.accept_socket.bind((listenhost, listenport))
        self.accept_socket.listen(10)
        self.accept_socket.setblocking(False)
        #self.accept_socket.settimeout(None)

        #for bsd
        self.kq = select.kqueue()
        self.kevent = [
                   select.kevent(self.accept_socket.fileno(),
                   filter=select.KQ_FILTER_READ,
                   flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE)
        ]

        #for linux
        #self.epoll = select.epoll()
        #self.epoll.register(self.accept_socket.fileno(), select.EPOLLIN)

        self.stuff = {}

    def run(self):
        #for bsd
        while True:
            events = self.kq.control(self.kevent, 5, None)
            for event in events:
                if event.ident == self.accept_socket.fileno():
                    # Accept connection
                    conn, addr = self.accept_socket.accept()
                    # Create new event
                    new_event = [
                             select.kevent(conn.fileno(),
                             filter=select.KQ_FILTER_READ,
                             flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE)
                    ]
                    # Register event
                    self.kq.control(new_event, 0, 0)
                    # Add connection to dictionary
                    self.stuff[conn.fileno()] = conn
                else:
                    conn = self.stuff[event.ident]
                    buf = conn.recv(1024)
                    if not buf:
                        conn.close()
                        continue
                    self.AutoBot.announce(self.connection, buf.decode("utf-8", "replace").strip())

#        #for linux
#        while True:
#            for sfd, ev in self.epoll.poll():
#                if sfd == self.accept_socket.fileno():
#                    conn, addr = self.accept_socket.accept()
#                    # Register new event
#                    self.epoll.register(conn.fileno(), select.EPOLLIN)
#                    # Add connection to dictionary
#                    self.stuff[conn.fileno()] = conn
#
#                else:
#                    conn = self.stuff[sfd]
#                    buf = conn.recv(1024)
#                    if not buf:
#                        conn.close()
#                        continue
#                    self.AutoBot.announce(self.connection, buf.decode("utf-8", "replace").strip())

def main():
    network = "irc.freenode.net"
    port = 7000
    channels = ["##test","##meskarune"]
    nick = "autobot2001"
    name = "AutoBot"
    listenhost = "localhost"
    listenport = 8888
    _ssl = True

    bot = AutoBot (nick, name, channels, network, listenhost, listenport, port, _ssl)
    bot.start()

if __name__ == "__main__":
    main()

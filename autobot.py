#!/usr/bin/python

import configparser, socket, ssl, time
import irc.bot
from threading import Thread

# Create our bot class
class AutoBot ( irc.bot.SingleServerIRCBot ):
    def __init__(self, nick, name, nickpass, channel, network, listenhost, listenport, port=6667, usessl=False):
        if usessl:
            factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        else:
            factory = irc.connection.Factory()

        irc.bot.SingleServerIRCBot.__init__(self, [(network, port)], nick, name, connect_factory = factory)

        self.nick = nick
        self.channel = channel
        self.nickpass = nickpass

        self.inputthread = TCPinput(self, listenhost, listenport)
        self.inputthread.start()

    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")

    def on_welcome ( self, connection, event ):
        connection.join(self.channel)
        if self.nickpass and connection.get_nickname() != self.nick:
            connection.privmsg("nickserv", "ghost %s %s" % (self.nick, self.nickpass))

    def on_privnotice(self, connection, event):
        source = event.source.nick
        if source and source.lower()  == "nickserv":
            if event.arguments[0].lower().find("identify") >= 0:
                if self.nickpass and self.nick == connection.get_nickname():
                    connection.privmsg("nickserv", "identify %s %s" % (self.nick, self.nickpass))

    def on_kick(self, connection, event):
        kickedNick = event.arguments[0]
        if kickedNick == self.nick:
            time.sleep(10) #waits 10 seconds
            connection.join(self.channel)

    def on_pubmsg (self, connection, event):
        if event.arguments[0].startswith("!"):
            self.do_command(event, self.channel, event.arguments[0].lstrip("!").lower())

    def on_privmsg(self, connection, event):
        if event.arguments[0].startswith("!"):
            self.do_command(event, event.source.nick, event.arguments[0].lstrip("!").lower())

    def do_command (self, event, source, command):
        user = event.source.nick
        isOper = self.channels[self.channel].is_oper(user)
        connection = self.connection
        if command == "hello":
            connection.privmsg(source, "hello " + user)
        elif command == "goodbye":
            connection.privmsg(source, "goodbye " + user)
        elif command == "disconnect":
            if isOper:
                self.disconnect()
            else:
                connection.privmsg(source, "You don't have permission to do that")
        elif command == "die":
            if isOper:
                self.die()
            else:
                connection.privmsg(source, "You don't have permission to do that")
        elif command == "help":
            connection.privmsg(source, "Available commands: !{hello, goodbye, disconnect, die, help}")
        else:
            connection.notice( user, "I'm sorry, " + user + ". I'm afraid I can't do that")

    def announce (self, connection, text):
        connection.privmsg(self.channel, text)

class TCPinput (Thread):
    def __init__(self, connection, AutoBot, listenhost, listenport):
        Thread.__init__(self)
        self.setDaemon(1)
        self.AutoBot = Autobot
        self.listenport = listenport

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.bind((host, port))

        self.AutoBot.announce("I've created the socket")

    #def _listen(self):
    #    self.socket.listen(5)
    #    while 1:
    #        #data, host = self.socket.recvfrom(1024)
    #        data, host = self.socket.accept()
    #        bot.connection.privmsg("meskarune", data)

    def run(self):
        while 1:
            data, self.listenport = self.socket.recvfrom(1024)
            self.AutoBot.announce(data)

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind(( config.get("tcp", "host").get('iface', ''), int(config.get("tcp", "port"))))
    #s.listen(5)
    #data = s.recv(1024)

def main():
    config = configparser.ConfigParser()
    config.read("autobot.conf")
    network = config.get("irc", "network")
    port = int(config.get("irc", "port"))
    channel = config.get("irc","channel")
    nick = config.get("irc", "nick")
    nickpass = config.get("irc", "nickpass")
    name = config.get("irc", "name")
    listenhost = config.get("tcp", "host")
    listenport = int(config.get("tcp", "port"))
    _ssl = config.getboolean("irc", "ssl")

    bot = AutoBot (nick, name, nickpass, channel, network, listenhost, listenport, port, _ssl)
    bot.start()

if __name__ == "__main__":
    main()

#!/usr/bin/python

import configparser, socket, ssl, time, datetime
import select
import re
import irc.bot
from threading import Thread

# Create our bot class
class AutoBot ( irc.bot.SingleServerIRCBot ):
    def __init__(self, nick, name, nickpass, channels, network, listenhost, listenport, port=6667, usessl=False):
        if usessl:
            factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        else:
            factory = irc.connection.Factory()

        irc.bot.SingleServerIRCBot.__init__(self, [(network, port)], nick, name, connect_factory = factory)

        self.nick = nick
        self.channel_list = channels
        self.nickpass = nickpass

        self.inputthread = TCPinput(self.connection, self, listenhost, listenport)
        self.inputthread.start()

    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")

    def on_welcome ( self, connection, event ):
        for channel in self.channel_list:
            connection.join(channel)
            self.logmessage("autobot", "info", "Joined channel %s" % (channel))
        if self.nickpass and connection.get_nickname() != self.nick:
            connection.privmsg("nickserv", "ghost %s %s" % (self.nick, self.nickpass))
            self.logmessage("autobot", "nickserv", "Recovered nick")

    def on_privnotice(self, connection, event):
        if not event.source:
            return
        source = event.source.nick
        if source and source.lower()  == "nickserv":
            if event.arguments[0].lower().find("identify") >= 0:
                if self.nickpass and self.nick == connection.get_nickname():
                    connection.privmsg("nickserv", "identify %s %s" % (self.nick, self.nickpass))
                    self.logmessage("autobot", "nickserv", "Identified to nickserv")

    def on_kick(self, connection, event):
        kickedNick = event.arguments[0]
        if kickedNick == self.nick:
            time.sleep(10) #waits 10 seconds
            for channel in self.channel_list:
                connection.join(channel)

    def on_pubmsg (self, connection, event):
        channel = event.target
        nick = event.source.nick
        message = event.arguments[0]
        self.logmessage(channel, nick, message)
        if message.startswith("!"):
            if self.channels[channel].is_oper(nick):
                self.do_command(event, True, channel, message.lstrip("!").lower())
            else:
                self.do_command(event, False, channel, message.lstrip("!").lower())

    def on_privmsg(self, connection, event):
        if event.arguments[0].startswith("!"):
            self.do_command(event, False, event.source.nick, event.arguments[0].lstrip("!").lower())

    def do_command (self, event, isOper, source, command):
        user = event.source.nick
        connection = self.connection
        if command == "hello":
            connection.privmsg(source, "hello " + user)
        elif command == "goodbye":
            connection.privmsg(source, "goodbye " + user)
        elif command == "ugm":
            connection.privmsg(source, "good (UGT) morning to all from " + user)
        elif command == "ugn":
            connection.privmsg(source, "good (UGT) night to all from " + user)
        elif command == "slap":
            connection.action(source, "slaps " + user + " around a bit with a large trout")
        elif command == "help":
            connection.privmsg(source, "Available commands: ![hello, goodbye, ugm, ugn, slap, disconnect, die, help]")
        elif command == "disconnect":
            if isOper:
                self.disconnect(msg="I'll be back!")
            else:
                connection.privmsg(source, "You don't have permission to do that")
        elif command == "die":
            if isOper:
                self.die(msg="Bye, cruel world!")
            else:
                connection.privmsg(source, "You don't have permission to do that")
        else:
            connection.notice( user, "I'm sorry, " + user + ". I'm afraid I can't do that")

    def announce (self, connection, text):
        for channel in self.channel_list:
            connection.notice(channel, text)

    def logmessage (self, channel, nick, message):
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with open(channel + '.log', 'a') as log:
            log.write("%s <%s> %s\n" % (timestamp, nick, message))

class TCPinput (Thread):
    def __init__(self, connection, AutoBot, listenhost, listenport):
        Thread.__init__(self)
        self.setDaemon(1)
        self.AutoBot = AutoBot
        self.listenport = listenport
        self.connection = connection

        self.accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accept_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.accept_socket.bind((listenhost, listenport))
        self.accept_socket.listen(10)

        self.accept_socket.setblocking(False)

        self.epoll = select.epoll()
        self.epoll.register(self.accept_socket.fileno(), select.EPOLLIN)

        self.stuff = {}

    def run(self):
        while True:
            for sfd, ev in self.epoll.poll():
                if sfd == self.accept_socket.fileno():
                    conn, addr = self.accept_socket.accept()
                    self.epoll.register(conn.fileno(), select.EPOLLIN)
                    self.stuff[conn.fileno()] = conn

                else:
                    conn = self.stuff[sfd]

                    buf = conn.recv(1024)
                    if not buf:
                        conn.close()
                        continue

                    self.AutoBot.announce(self.connection, buf.decode("utf-8", "replace").strip())

def main():
    config = configparser.ConfigParser()
    config.read("autobot.conf")
    network = config.get("irc", "network")
    port = int(config.get("irc", "port"))
    _ssl = config.getboolean("irc", "ssl")
    channels = [channel.strip() for channel in config.get("irc", "channels").split(",")]
    nick = config.get("irc", "nick")
    nickpass = config.get("irc", "nickpass")
    name = config.get("irc", "name")
    listenhost = config.get("tcp", "host")
    listenport = int(config.get("tcp", "port"))

    #FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    #logging.basicConfig(format=FORMAT)

    bot = AutoBot (nick, name, nickpass, channels, network, listenhost, listenport, port, _ssl)
    bot.start()

if __name__ == "__main__":
    main()

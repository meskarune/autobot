#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A full featured python IRC bot"""

import configparser, sys, socket, ssl, time, datetime, re
import select
import irc.bot
import encodings
import codecs
from urllib.request import urlopen, Request
from urllib.parse   import quote, urlsplit
from urllib.error import URLError
from bs4 import BeautifulSoup
from threading import Thread

# Create our bot class
class AutoBot(irc.bot.SingleServerIRCBot):
    """Create the single server irc bot"""
    def __init__(self, nick, name, nickpass, channels, network, listenhost, listenport, port=6667, usessl=False):
        """Connect to the IRC server"""
        if usessl:
            factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        else:
            factory = irc.connection.Factory()

        irc.bot.SingleServerIRCBot.__init__(self, [(network, port)], nick, name, connect_factory = factory)

        self.nick = nick
        self.channel_list = channels
        self.nickpass = nickpass

        self.connection.add_global_handler("quit", self.alt_on_quit, -30)

        self.inputthread = TCPinput(self.connection, self, listenhost, listenport)
        self.inputthread.start()

    def say(self, target, text):
        self.connection.privmsg(target, text)

    def on_nicknameinuse(self, connection, event):
        """If the nick is in use, get nick_"""
        connection.nick(connection.get_nickname() + "_")

    def on_welcome(self, connection, event):
        """Join channels and regain nick"""
        for channel in self.channel_list:
            connection.join(channel)
            self.logmessage("autobot", "info", "Joined channel %s" % (channel))
        if self.nickpass and connection.get_nickname() != self.nick:
            connection.privmsg("nickserv", "ghost %s %s" % (self.nick, self.nickpass))
            self.logmessage("autobot", "info", "Recovered nick")

    def get_version(self):
        """CTCP version reply"""
        return "AUTOBOT IRC BOT"

    def on_privnotice(self, connection, event):
        """Identify to nickserv and log privnotices"""
        self.logmessage("autobot", event.source, event.arguments[0])
        if not event.source:
            return
        source = event.source.nick
        if source and source.lower() == "nickserv":
            if event.arguments[0].lower().find("identify") >= 0:
                if self.nickpass and self.nick == connection.get_nickname():
                    connection.privmsg("nickserv", "identify %s %s" % (self.nick, self.nickpass))
                    self.logmessage("autobot", "info", "Identified to nickserv")

    #def on_disconnect(self, connection, event):

    def on_pubnotice(self, connection, event):
        self.logmessage(event.target, "notice", event.source + ": " + event.arguments[0])

    def on_kick(self, connection, event):
        """Log kicked nicks and rejoin channels if bot is kicked"""
        kickedNick = event.arguments[0]
        kicker = event.source.nick
        self.logmessage(event.target, "info", "%s was kicked from the channel by %s" % (kickedNick, kicker))
        if kickedNick == self.nick:
            time.sleep(10) #waits 10 seconds
            for channel in self.channel_list:
                connection.join(channel)

    def alt_on_quit(self, connection, event):
        """Log when users quit"""
        for channel in self.channels:
            if self.channels[channel].has_user(event.source.nick):
                self.logmessage(channel, "info", "%s has quit" % (event.source))

    def on_join(self, connection, event):
        """Log channel joins"""
        self.logmessage(event.target, "info", "%s joined the channel" % (event.source))
        if event.source.nick == self.nick:
            self.say(event.target, "Autobots, roll out!")

    def on_part(self, connection, event):
        """Log channel parts"""
        self.logmessage(event.target, "info", "%s left the channel" % (event.source))

    def on_nick(self, connection, event):
        """Log nick changes"""
        oldNick = event.source.nick
        newNick = event.target
        for channel in self.channels:
            if self.channels[channel].has_user(newNick):
                self.logmessage(channel, "info", "%s changed their nick to %s" % (event.source, newNick))

    def on_mode(self, connection, event):
        """Log mode changes"""
        mode = " ".join(event.arguments)
        self.logmessage(event.target, "info", "mode changed to %s by %s" % (mode, event.source.nick))

    def on_topic(self, connection, event):
        """Log topic changes"""
        self.logmessage(event.target, "info", 'topic changed to "%s" by %s' % (event.arguments[0], event.source.nick))

    def urlannounce(self, url, source):
        """Say Website Title information in channel"""
        #if urlopen(url).getcode() == 200:
        baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=urlsplit(url))
        path = urlsplit(url).path
        query = '?{uri.query}'.format(uri=urlsplit(url))
        try:
            parsedurl = baseurl.encode("idna").decode("idna") + quote(path + query, safe='/#:=&?')
        except:
            return
        try:
            request = Request(parsedurl)
            request.add_header('Accept-Encoding', 'utf-8')
            request.add_header('User-Agent', 'Mozilla/5.0')
            response = urlopen(request)
        except:
            return
        try:
            URL = BeautifulSoup(response.read(), "html.parser")
        except URLError as e:
            sys.stderr.write("Error when fetching " + url + ": %s\n" % (e))
            return
        if not URL.title:
            return
        if URL.title.string is None:
            return
        if len(URL.title.string) > 250:
            title=URL.title.string[0:250] + '…'
        else:
            title=URL.title.string
        self.connection.privmsg(source, title.replace('\n', ' ').strip() + " (" + urlsplit(url).netloc + ")")

    def on_pubmsg(self, connection, event):
        """Log public messages and respond to command requests"""
        channel = event.target
        nick = event.source.nick
        message = event.arguments[0]
        self.logmessage(channel, nick, message)

        url_regex = re.compile(
            r'(?i)\b((?:https?://|[a-z0-9.\-]+[.][a-z]{2,4}/)'
            r'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))'
            r'+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|'
            r'''[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', re.IGNORECASE)

        if url_regex.search(message):
            messageList = message.split(' ')
            for element in messageList:
                if url_regex.match(element):
                    self.urlannounce(element, channel)

        command_regex = re.compile(
            r'^(' + re.escape(self.nick) + '( |[:,] ?)|'
            r'!)'
            r'(.*$)', re.IGNORECASE)

        if command_regex.match(message):
            command = command_regex.match(message).group(3)
            if self.channels[channel].is_oper(nick):
                self.do_command(event, True, channel, command)
            else:
                self.do_command(event, False, channel, command)

    def on_privmsg(self, connection, event):
        """Log private messages and respond to command requests"""
        channel = event.target
        nick = event.source.nick
        message = event.arguments[0]
        self.logmessage(channel, nick, message)
        self.do_command(event, False, nick, message)

    def do_command(self, event, isOper, source, command):
        """Commands the bot will respond to"""
        user = event.source.nick
        connection = self.connection
        message = event.arguments[0]
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
        elif command.startswith("rot13"):
            if all(message.partition(' ')) and message.partition(' ')[0] == "!rot13":
                connection.privmsg(source, codecs.encode(message.partition(' ')[2], 'rot13'))
            else:
                connection.privmsg(source, "I'm sorry, I need a message to cipher, try \"!rot13 message\"")
        elif command == "help":
            connection.privmsg(source, "Available commands: ![hello, goodbye, "
                                       "ugm, ugn, slap, rot13 <message>, "
                                       "disconnect, die, help]")
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
            connection.notice(user, "I'm sorry, " + user + ". I'm afraid I can't do that")

    def announce(self, connection, text):
        """Send notice to joined channels"""
        for channel in self.channel_list:
            connection.notice(channel, text)
            logmessage(channel, "notice", connection.get_nickname() + ": " + text)

    def logmessage(self, channel, nick, message):
        """Create IRC logs"""
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with open(channel + '.log', 'a') as log:
            log.write("%s <%s> %s\n" % (timestamp, nick, message))

class TCPinput(Thread):
    """Listen for data on a port and send it to Autobot.announce"""
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

    bot = AutoBot(nick, name, nickpass, channels, network, listenhost, listenport, port, _ssl)
    bot.start()

if __name__ == "__main__":
    main()

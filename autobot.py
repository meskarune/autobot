import irc.bot

# Connection information

# Create our bot class
class AutoBot ( irc.bot.SingleServerIRCBot ):
    def __init__(self, nick, name, nickpass, channel, network, port=6667, usessl=False):
        if usessl:
            import ssl
            factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        else:
            factory = irc.connection.Factory()
        irc.bot.SingleServerIRCBot.__init__(self, [(network, port)], nick, name, connect_factory = factory)
        self.channel = channel
        self.nickpass = nickpass

    def on_welcome ( self, connection, event ):
        connection.join ( self.channel )

    #def on_privnotice(self, connection, event):
    #    source = event.source.nick
    #    if source and irc_lower(nm_to_n(source)) == "nickserv":
    #        if event.arguments[0].find("IDENTIFY") >= 0:
    #            connection.privmsg("nickserv", "identify" + self.nickpass)

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

# Create TCP socket
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((listenhost.get('iface', ''), listenport))
#s.listen(5)
#data = s.recv(1024)
#if data:
#    connection.privmsg(channel, data)

def main():
    import configparser
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

    bot = AutoBot (nick, name, nickpass, channel, network, port, _ssl)
    bot.start()

if __name__ == "__main__":
    main()

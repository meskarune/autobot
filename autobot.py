import irc.bot

# Connection information
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
listenport = int(config.get("tcp", "port")

# Create our bot class
class AutoBot ( irc.bot.SingleServerIRCBot ):
    def on_welcome ( self, connection, event ):
        connection.join ( channel )

    def on_pubmsg ( self, connection, event ):
        command = event.arguments[0].lstrip("!")
        self.do_command(event, command)

    def do_command (self, event, command):
        nick = event.source.nick
        connection = self.connection
        if command == "hello":
            connection.privmsg( channel, "hello" + nick)
        elif command == "goodbye":
            connection.privmsg( channel, "goodbye" + nick)
        else:
            connection.privmsg( channel, "no")

# Create the bot
bot = AutoBot ( [( network, port )], nick, name )
bot.start()

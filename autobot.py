import irc.bot

# Connection information
network = "irc.freenode.net"
port = 6667
channel = "##meskarune"
nick = "starscream6000"
name = "Python Test Bot"

# Create our bot class
class AutoBot ( irc.bot.SingleServerIRCBot ):
    def on_welcome ( self, connection, event ):
        connection.join ( channel )

    def on_pubmsg ( self, connection, event ):
        #user = event.source.split("!")[0]
        command = event.arguments[0].lstrip("!")
        self.do_command(event, command)
        #if event.arguments[0].lower() == "!hello":
        #    connection.privmsg( channel, "hello " + user + " you said " + command)

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

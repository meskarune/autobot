autobot
=======

A python IRC bot

This is a full featured python irc bot that uses the python-irc library

Features
--------

* Configuration options in a single config file
* Joins a single irc server with support for SSL
* Joins multiple channels
* Listens on a port for messages and then announces the messages in IRC
    * The port and host are set in the configuration file
    * you can send a test message with "netcat host port" then type the message
      and hit enter.
* Identifies to nickserv
* Rejoins channels on kick or disconnect
* Has some basic commands that are listed with !help

Configuration
-------------

Copy the autobot.conf.template to autobot.conf and update the settings for your
personal use. Then run the bot with ```python autobot.py```

To-do
-----

* encrypt nick password so it isn't plaintext in the config
* SASL auth
* CertFP auth
* Add logger
    * Log Kick - done
    * Log Join/Part - done
    * *Log nick changes* - logs but saves to autobot.log , need to check all
      channels
    * *Log topic changes*
    * Log privmsg - done
    * Log pubmsg - done
    * Log public and private notice - done
    * *Log mode changes* - logs but does not have complete information for +q +b
    * *Log quit* - need to check over all channels
* Make modular so scripts can be loaded from a directory and be used by the bot

Refactor irc channel OP check to loop through connected channels and check if the user has
OPs in any of them, if yes, then isOper is True - maybe should skip this and just have a mod list in configuration?

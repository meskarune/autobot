autobot
=======

Python IRC bot

This is a simple python irc bot that uses the python-irc library

Configuration:

Copy the autobot.conf.template to autobot.conf and update the settings for your
personal use. Then run the bot with ```python autobot.py```

To-do:

* SASL auth
* CertFP auth
* Add logger
* Make modular so scripts can be loaded from a directory and be used by the bot

Refactor irc channel OP check to loop through connected channels and check if the user has
OPs in any of them, if yes, then isOper is True - maybe should skip this and just have a mod list in configuration?

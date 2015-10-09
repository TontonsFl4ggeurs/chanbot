# -*- coding: utf-8 -*-
# http://openclassrooms.com/courses/programmer-un-bot-irc
# -simplement-avec-ircbot

import irclib
import ircbot
import time
import sys

server = "irc.root-me.org"
channel = "Bots_room"
admin = "TiWim"
robNick = "jeannot"
helloMsg = "Hi!"


def logs(message):
    print "=>", message


class Bot(ircbot.SingleServerIRCBot):
    def __init__(self):
        logs("Connecting to server '" + server + "'")
        ircbot.SingleServerIRCBot.__init__(self, [(server, 6667)], robNick, robNick)
        logs("Connected")

    def on_welcome(self, serv, ev):
        logs("joining a channel")
        serv.join(channel)
        logs("Joined channel '" + channel + "' with nickname '" +
                robNick + "'")
#        time.sleep(1)
#        serv.privmsg(channel, helloMsg)

    def on_privmsg(self, serv, ev):
        author = irclib.nm_to_n(ev.source())
        message = ev.arguments()[0]
        print(author + " >> " + message)

        if author == admin:
            serv.privmsg(channel, message)
            logs("Message '" + message + "' transfered to '" + channel + "'")

            if "kitt!" in message:
                serv.privmsg(channel, "Bye!")
                serv.disconnect()
                logs("Received disconnection msg from: '" + author)
                sys.exit()

    def on_pubmsg(self, serv, ev):
        author = irclib.nm_to_n(ev.source())
        channel = ev.target()
        message = ev.arguments()[0]

        if robNick in message:
            logs("Received message '" + message + "' from '" + author +
                    "' on '" + channel + "'")
            if "kitt!" in message:
                serv.privmsg(channel, "Bye!")
                serv.disconnect()
                logs("Received disconnection msg from: '" + author)
                sys.exit()


if __name__ == "__main__":
    Bot().start()

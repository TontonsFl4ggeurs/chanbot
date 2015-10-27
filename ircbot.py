# -*- coding: utf-8 -*-
# http://openclassrooms.com/courses/programmer-un-bot-irc-simplement-avec-ircbot
# http://www.devshed.com/c/a/Python/IRC-on-a-Higher-Level-Concluded/
# https://user.oc-static.com/pdf/102516-programmer-un-bot-irc-simplement-avec-ircbot.pdf

# TODO move logs to modules

from lib import irclib
from lib import ircbot
import time
import requests
import re
from modules import Parler as Mod
from modules import Interact

admin = ["TiWim"]
serveur = "irc.root-me.org"
canal = "#tontons_fl4ggeurs"
robNick = "Maistre_Folace"
port = 6667
helloMsg = "Touche pas au grisbi salope!!!"
log_fileName = "bot.log"
log_file = open(log_fileName, "a")


class Bot(ircbot.SingleServerIRCBot):

    def on_welcome(self, serv, ev):
        print "welcome"
        serv.join(canal)
        logs("Joined channel '" + canal, robNick)
        serv.privmsg(canal, helloMsg)

    def on_kick(self, serv, ev):
        serv.join(canal)

    def on_privmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        message = ev.arguments()[0]
        print(auteur + " >> " + message)

        if auteur in admin:
            serv.privmsg(canal, message)
            logs("Message '" + message + "' transfered to '" + canal + "'")

        elif auteur == "BotInfo":
            print "sending", message
            serv.privmsg(canal, message)
        else:
            serv.privmsg(auteur, "bonjour, merci de m'envoyer des messages privés")
            logs("Message '" + message + "' received and answered", auteur, "\33[01;31mmsg\33[0m")

    def on_pubmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]
        if "!reload" in message and auteur in admin:
            reload(Mod)
            reload(Interact)
            serv.privmsg(canal, "I g0t m0r3 P0w4!")
        else:
            Interact.public(self, serv, ev)

    def on_close(self, serv, canal, auteur):
        serv.privmsg(canal, "ok je me casse alors!")
        logs("Received disconnection msg from: '" + auteur + "'")
        log_file.close()
        serv.disconnect()
        self.die()

#    def public(self, serv, ev):
#        auteur = irclib.nm_to_n(ev.source())
#        canal = ev.target()
#        message = ev.arguments()[0]
#        if "!" in message:
#            serv.privmsg("BotInfo", message)
#
#        if "!apero" in message:
#            logs("Requested Apero", auteur)
#            try:
#                serv.privmsg(canal, Mod.apero())
#                logs("Command answered")
#            except:
#                serv.privmsg(canal, "Je n'ai pas pu récupérer correctement l'info, mais vous pouvez la trouver sur ce site: http://estcequecestlapero.fr")
#                logs("Command unsuccessful", author=auteur, info="WARN")
#        elif "!weekend" in message:
#            try:
#                logs("requested Weekend", auteur)
#                serv.privmsg(canal, Mod.weekend())
#            except:
#                logs("Failure!", info="Debug")
#                serv.privmsg(canal, "marche pas :(")
#        elif message == "!ctfs":
#            liste = Mod.ctf()
#            for elt in liste:
#                serv.privmsg(canal, elt)
#        elif "!help" == message:
#            logs("Requested Help from: '" + auteur)
#            serv.privmsg(canal, "!help !ctf !ctfs !reload !apero !weekend")
#        elif "!ctf" == message.split(" ")[0]:
#            logs("Requested ctf score")
#            try:
#                serv.privmsg(canal, Mod.score(message.split(" ")[1]))
#            except:
#                serv.privmsg(canal, Mod.score())
#        elif robNick in message:
#            if "stop" in message:
#                if auteur in admin:
#                    logs("Received message '" + message + "' from '" + auteur + "' on '" + canal + "'")
#                    self.on_close(serv, canal, auteur)
#                else:
#                    serv.privmsg(canal, "Méchant " + auteur + " tu voulais me faire partir?")
#                    logs("sent stop signal!", auteur, "\33[01;31mWARN\33[0m")
#            elif "bonjour" in message:
#                logs("Received Bonjour from: '" + auteur)
#                serv.privmsg(canal, "bonjour " + auteur)
#            elif "!reload" in message and auteur in admin:
#                logs("Requested reload")
#                reload(Mod)
#                serv.privmsg(canal, "rechargement de mes facultés")
#            else:
#                logs("Received '" + message + "' from: '" + auteur)
#        else:
#            logs(message, auteur)


def logs(message, author="", info="info"):
    print time.strftime("%m-%d %H:%M:%S"), info, author + ":", message
    log_file.write(time.strftime("%m-%d %H:%M:%S") + " " + message + "\n")


if __name__ == "__main__":
    try:
        logs("Connecting to server '" + serveur + "'")
        Bot([(serveur, port)], robNick, robNick).start()
    except KeyboardInterrupt:
        print "\ruser interruption"
        print "closing log file and shutting down"
        log_file.close()

#! /usr/env/python
# coding: utf-8
import sys, traceback
import requests
import re
import string
try:
    from bs4 import BeautifulSoup
except:
    print 'Vous devez installer le paquet python-bs4'


def apero():
    """
    take the content of the website and print it on the chan
    """
    page = "http://estcequecestbientotlapero.fr"
    resultat = BeautifulSoup(requests.get(page).text, "lxml")
    return resultat.h2.text.encode('utf-8').replace(".", ". ").strip()


def weekend():
    """
    take the content of the website and print it on the chan
    """
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text.encode('utf-8')
    return re.search(ur'<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()


def score(team='Tontons'):
    """
    This class has to be changed before each new ctf.
    get param: page and verify=False for corrupted ssl certs
    """
    try:
        page = "https://school.fluxfingers.net/scoreboard"
        p = re.compile(ur'number">(.*?)<.*>(.*?)<\/a.*number">(.*?)<\/td><\/tr>')
        resultat = requests.get(page).content.replace("\n", "").replace(" ", "").split("<tr")
        for i in resultat:
            if team.lower() in i.lower():
                print i
                a = re.search(p, i)
                b = int(a.group(1))
                string = "Classement: " + a.group(2) + " " + str(b)
                if b == 1:
                    string += "ers avec "
                else:
                    string += "èmes avec "

                return string + a.group(3) + " points!"
    except:
        traceback.print_exc(file=sys.stdout)
        return "failure"


def ctf():
    """
    returns a list of ctfs
    """
    try:
        page = "https://ctftime.org/event/list/upcoming/rss/"
        p = re.compile(ur'<item><title>(.*?)<.*?Date(.*?)\&.*?sh;(.*?) &.*?at: (.*?)&lt.*?b&gt;(.*?)&.*?href="(.*?)"')
        test_str = unicode(requests.get(page).content.strip(), errors='ignore').replace("\n", "")
        liste = re.findall(p, test_str)
        compteur = 0
        string = []
        while liste:
            compteur += 1
            elt = liste.pop(0)
            line = "\33[01;31m" + elt[0] + "\33[0m Dates\33[00;34m" + elt[1]
            line += "-" + elt[2] + "\033[0m type: \033[02;34m" + elt[3] + " "
            line += elt[4] + ".\033[0m Site web: \033[01;35m" + elt[5]
            string.append(line)
            if compteur == 5:
                break
        return string
    except:
        traceback.print_exc(file=sys.stdout)
        return "failure"

#! /usr/env/python
# coding: utf-8
import sys, traceback
import requests
import re
try:
    from bs4 import BeautifulSoup
except:
    print 'Vous devez installer le paquet python-bs4'


def apero():
    page = "http://estcequecestbientotlapero.fr"
    resultat = BeautifulSoup(requests.get(page).text)
    return resultat.h2.text.encode('utf-8').replace(".", ". ").strip()


def weekend():
    # TODO verify the format of this site
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text
    try:
        return re.search('<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()
    except:
        print "exception"  # print stacktrace
        return "Une erreur s'est produite"


def score():
    """
    This class has to be changed before each new ctf.
    """
    try:
        string = ''
        page = "https://ctf.hackover.de/ranking"
        p = re.compile(ur'<td>(.*?)<.*?France<\/td><td>(.*?)<')
        resultat = requests.get(page,verify=False).content.replace("\n", "").replace(" ", "").split("<tr>")
        print resultat

        for i in resultat:
            if 'Tontons' in i:
                a = re.search(p, i)
                return "Classement: " + a.group(1) + "èmes avec " + a.group(2) + " points!"
    except:
        traceback.print_exc(file=sys.stdout)
        return "failure"


def ctf():
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
            line = "\033[01;31m" + elt[0] + "\033[0m Dates\033[00;34m" + elt[1]
            line += "-" + elt[2] + "\033[0m type: \033[02;34m" + elt[3] + " "
            line += elt[4] + ".\033[0m Site web: \033[01;35m" + elt[5]
            string.append(line)
            if compteur == 5:
                break
        return string
    except:
        return "failure"

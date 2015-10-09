#! /usr/env/python
# coding: utf-8

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
    # TODO verify the format of this site
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text
    try:
        return re.search('<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()
    except:
        print "exception"  # print stacktrace
        return "Une erreur s'est produite"

def score():
    try:
        string = ''
        page = "http://asis-ctf.ir/contestants/"
        resultat = requests.get(page).content.split("<tr>")
#        print resultat
        for i in resultat:
            if 'Tontons' in i:
                print i
                string = i.replace ( "\n", "" )
                return "ctf: >" + string.strip() + "< !" # string  # Classement: " # + a.group(1) + " avec " + a.group(2) + "points"
    except:
        return "fail"  # "Score: 410! gg vic511! Vous pouvez aussi le consulter ici: http://score.mmactf.link/problems?locale=en"

def ctf():
    try:
        page = "https://ctftime.org/event/list/upcoming/rss/"
        p = re.compile(ur'<item><title>(.*?)<.*?Date(.*?)\&.*?sh;(.*?) &.*?at: (.*?)&lt.*?b&gt;(.*?)&.*?href="(.*?)"')
        test_str = unicode(requests.get(page).content.strip(), errors='ignore').replace ( "\n", "" )
        liste = list()
        liste = re.findall(p, test_str)
        compteur = 0
        string = []
        while liste:
            compteur += 1
            elt = liste.pop(0)
            string.append("\033[01;31m" + elt[0] + "\033[0m Dates\033[00;34m" + elt[1] + "-" + elt[2] + "\033[0m type: " + elt[3] +" " + elt[4] + ". Site web: " + elt[5])
            if compteur == 5:
                break
        print string
        return string
    except:
        pass

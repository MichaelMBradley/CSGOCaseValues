from bs4 import BeautifulSoup as bs
from constants import *
import re
from urllib.request import urlopen, Request
from status import *


def caseLinks():
    mainFile = urlopen(Request(SITE, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")  # Reads main page
    cases = [l.start() for l in re.finditer(SITE + "/case/", mainFile)]  # Retrieves positions of links to cases

    for i in range(len(cases)):
        cases[i] = mainFile[cases[i] : mainFile.find('"', cases[i])]  # Formats case links

    k = 0
    while k < len(cases):  # Must iterate with while loop to avoid skipping elements
        if "Knives=1" in cases[k] or "Gloves=1" in cases[k] or cases[k] in cases[k + 1 :]:  # Pops invalid elements
            cases.pop(k)
        else:
            k += 1  # If current index is valid check next index

    return cases


def skinLinks(caseLinks):
    skins = []
    caseCost = []
    progress = statusbar(len(caseLinks), "Finding skins")
    t = timer(["Retrieving webpage", "Analyzing data"])

    for link in caseLinks:
        t.swapto(0)
        caseFile = urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")  # Reads case page
        t.swapto(1)
        skins.append([l.start() for l in re.finditer(SITE + "/skin/", caseFile)])  # Retrieves positions of links to skins
        priceStart = caseFile.find("CDN$ ") + 5
        caseCost.append(float(caseFile[priceStart : caseFile.find(" ", priceStart)]))

        for i in range(len(skins[-1])):
            skins[-1][i] = caseFile[skins[-1][i] : caseFile.find('"', skins[-1][i])]  # Formats skin links
            # String casefile indeces [start index: first " after start index]
        if not caseFile.find("?Knives=1") == -1:
            special = "Knives"
            iden = "/skin/"
        else:
            special = "Gloves"
            iden = "/glove/"

        t.swapto(0)
        knifeFile = urlopen(Request(link + "?" + special + "=1", headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")  # Reads knife/glove page
        t.swapto(1)

        knifePageLinks = [l.start() for l in re.finditer(link + "?" + special + "=1&page=", knifeFile)]  # Retrieves positions of links to other special pages, original page
        knifePageLinks.insert(0, knifeFile)

        for i in range(len(knifePageLinks)):
            if not i == 0:
                t.swapto(0)
                knifePageLinks[i] = urlopen(Request(knifeFile[knifePageLinks[i] : knifeFile.find("&", knifePageLinks[i]) + 7], headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")  # If not last index (already file), open webpage with formatted link
                t.swapto(1)
            knives = [l.start() for l in re.finditer(SITE + iden, knifePageLinks[i])]  # Retrieves positions of links to knives
            for j in range(len(knives)):
                knives[j] = knifePageLinks[i][knives[j] : knifePageLinks[i].find('"', knives[j])]  # Formats knife links
            skins[-1] += knives  # Combines knife list with skin list

        k = 0
        while k < len(skins[-1]):  # Must iterate with while loop to avoid skipping elements
            if skins[-1][k] in skins[-1][k + 1 :]:  # Pops invalid elements
                skins[-1].pop(k)
            else:
                k += 1  # If current index is valid check next index
        progress.incrementandprint()
    t.results()

    return skins, caseCost


def getPrices(skinLinks):
    prices = []
    skinfo = []
    progress = statusbar(sum([len(l) for l in skinLinks]), "Getting prices")
    t = timer(["Retrieving webpage", "Analyzing data"])

    for box in skinLinks:
        case = []
        casefo = []
        for skin in box:
            t.swapto(0)
            loadpage = urlopen(Request(skin, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")  # Reads page
            t.swapto(1)

            if not loadpage.find("★") == -1:  # Determines if skin is a knife or glove
                res = 2
            elif (not loadpage.find("Gloves |") == -1) or (not loadpage.find("Wraps |") == -1):
                res = 5
            else:
                res = 10

            page = bs(loadpage, "html.parser")
            wear = [p.get_text() for p in page.findAll("span", class_="pull-right")][:res]  # Gets the first (res) wear prices
            wearfo = [float(p.get_text()) for p in page.findAll("div", class_="marker-value cursor-default")]  # Finds max and min wear
            if wearfo == []:
                wearfo = [-1, -1]  # If skin is vanilla

            for i in range(len(wear)):
                if wear[i].find(".") != -1:  # If wear is a number
                    num = wear[i][wear[i].find(" ") + 1 :]
                    if num.find(",") != -1:  # Deals with thousands
                        num = num[: num.find(",")] + num[num.find(",") + 1 :]
                    wear[i] = float(num)
                elif wear[i].find("Possible") != -1:  # If wear is impossible
                    wear[i] = -2
                else:  # If no price available
                    wear[i] = -1

            quals = [i.get_text() for i in page.findAll("p", class_="nomargin")][0]
            quality = ""
            for r in range(len(RARITY)):
                if quals.find(FULLRARITY[r]) != -1:  # Finds quality of skin
                    quality = RARITY[r]
                    break
            if quality == "" and quals.find("Contraband"):  # Makes the Howl a Covert skin to simplify calculations
                quality = "C"
            elif quality == "":  # If hand wraps, assign glove quality
                quality = "G"
            wearfo.append(quality)
            case.append(wear)
            casefo.append(wearfo)
            progress.incrementandprint()
        prices.append(case)
        skinfo.append(casefo)
    t.results()

    return prices, skinfo

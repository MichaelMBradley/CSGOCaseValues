from bs4 import BeautifulSoup as bs
from constants import *
from misc import status
import re
import time
from urllib.request import urlopen, Request

def caseLinks():
    """
    Returns
    -------
    cases : List of Strings
        List of links to cases on csgostash.com.
    """
    mainFile = (
        urlopen(Request(SITE, headers={"User-Agent": "Mozilla/5.0"}))
        .read()
        .decode("utf-8")
    )  # Reads main page
    cases = [
        l.start() for l in re.finditer(SITE + "/case/", mainFile)
    ]  # Retrieves positions of links to cases

    for i in range(len(cases)):
        cases[i] = mainFile[
            cases[i] : mainFile.find('"', cases[i])
        ]  # Formats case links

    k = 0
    while k < len(cases):  # Must iterate with while loop to avoid skipping elements
        if (
            "Knives=1" in cases[k]
            or "Gloves=1" in cases[k]
            or cases[k] in cases[k + 1 :]
        ):  # Pops invalid elements
            cases.pop(k)
        else:
            k += 1  # If current index is valid check next index

    return cases


def skinLinks(caseLinks, testTime=False):
    """
    Parameters
    ----------
    caseLinks : List of Strings
        Obtained using caseLinks(), but will accept any number of links.
    testTime : Boolean, optional
        Records the time taken to read and download pages. The default is False.

    Returns
    -------
    skins : List of Lists of Strings
        Links to each weapons organized in the same order the case links were given.
    """
    skins = []
    t = []
    caseCost = []
    length = len(caseLinks)
    curr = 0
    webp = 0
    status(curr, length, "Finding skins: ")

    for link in caseLinks:
        t.append([time.time(), False] if testTime else 0)
        caseFile = (
            urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"}))
            .read()
            .decode("utf-8")
        )  # Reads case page
        t.append([time.time(), True] if testTime else 0)
        webp += 1
        skins.append(
            [l.start() for l in re.finditer(SITE + "/skin/", caseFile)]
        )  # Retrieves positions of links to skins
        priceStart = caseFile.find("CDN$ ") + 5
        caseCost.append(float(caseFile[priceStart : caseFile.find(" ", priceStart)]))

        for i in range(len(skins[-1])):
            skins[-1][i] = caseFile[
                skins[-1][i] : caseFile.find('"', skins[-1][i])
            ]  # Formats skin links
            # String casefile indeces [start index: first " after start index]
        if not caseFile.find("?Knives=1") == -1:
            special = "Knives"
            iden = "/skin/"
        else:
            special = "Gloves"
            iden = "/glove/"

        t.append([time.time(), False] if testTime else 0)
        knifeFile = (
            urlopen(
                Request(
                    link + "?" + special + "=1", headers={"User-Agent": "Mozilla/5.0"}
                )
            )
            .read()
            .decode("utf-8")
        )  # Reads knife/glove page
        t.append([time.time(), True] if testTime else 0)
        webp += 1

        knifePageLinks = [
            l.start() for l in re.finditer(link + "?" + special + "=1&page=", knifeFile)
        ]  # Retrieves positions of links to other special pages, original page
        print(
            knifePageLinks,
            link + "?" + special + "=1&page=",
            knifeFile.find(
                "https://csgostash.com/case/277/Shattered-Web-Case?Knives=1&page=2"
            ),
        )
        knifePageLinks.insert(0, knifeFile)

        for i in range(len(knifePageLinks)):
            if not i == 0:
                t.append([time.time(), False] if testTime else 0)
                knifePageLinks[i] = (
                    urlopen(
                        Request(
                            knifeFile[
                                knifePageLinks[i] : knifeFile.find(
                                    "&", knifePageLinks[i]
                                )
                                + 7
                            ],
                            headers={"User-Agent": "Mozilla/5.0"},
                        )
                    )
                    .read()
                    .decode("utf-8")
                )  # If not last index (already file), open webpage with formatted link
                t.append([time.time(), True] if testTime else 0)
                webp += 1
            knives = [
                l.start() for l in re.finditer(SITE + iden, knifePageLinks[i])
            ]  # Retrieves positions of links to knives
            for j in range(len(knives)):
                knives[j] = knifePageLinks[i][
                    knives[j] : knifePageLinks[i].find('"', knives[j])
                ]  # Formats knife links
            skins[-1] += knives  # Combines knife list with skin list

        k = 0
        while k < len(
            skins[-1]
        ):  # Must iterate with while loop to avoid skipping elements
            if skins[-1][k] in skins[-1][k + 1 :]:  # Pops invalid elements
                skins[-1].pop(k)
            else:
                k += 1  # If current index is valid check next index
        curr += 1
        status(curr, length, "Finding skins: ")

    if testTime:
        web = 0
        func = 0
        for i in range(1, len(t)):
            ti = t[i][0] - t[i - 1][0]
            if t[i][1]:
                web += ti
            else:
                func += ti
        p = web / webp
        print(
            f"Webpage retrieval: {web:.2f}s ({p:.3f}s/page)\nCalculations: {func:.2f}s"
        )

    return skins, caseCost


def getPrices(skinLinks, testTime=False):
    """
    Parameters
    ----------
    skinLinks : List of Lists of Strings
        Links to weapons in cases.
    testTime : Boolean, optional
        Record the amount of time taken to run. The default is False.

    Returns
    -------
    prices : List of Lists of Floats
        Prices given in same order as skin links.
    skinfo : List of Lists
        Contains info about floats.
    """
    prices = []
    skinfo = []
    length = sum([len(l) for l in skinLinks])
    curr = 0
    webp = 0
    status(curr, length, "Getting prices: ")
    t = []

    for box in skinLinks:
        case = []
        casefo = []
        for skin in box:
            t.append([time.time(), False] if testTime else 0)
            loadpage = (
                urlopen(Request(skin, headers={"User-Agent": "Mozilla/5.0"}))
                .read()
                .decode("utf-8")
            )  # Reads page
            t.append([time.time(), True] if testTime else 0)

            if not loadpage.find("★") == -1:  # Determines if skin is a knife or glove
                res = 2
            elif (not loadpage.find("Gloves |") == -1) or (
                not loadpage.find("Wraps |") == -1
            ):
                res = 5
            else:
                res = 10

            page = bs(loadpage, "html.parser")
            webp += 1
            wear = [p.get_text() for p in page.findAll("span", class_="pull-right")][
                :res
            ]  # Gets the first (res) wear prices
            wearfo = [
                float(p.get_text())
                for p in page.findAll("div", class_="marker-value cursor-default")
            ]  # Finds max and min wear
            if wearfo == []:
                wearfo = [-1, -1]  # If skin is vanilla
            curr += 1
            status(curr, length, "Getting prices: ")

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
            if quality == "" and quals.find(
                "Contraband"
            ):  # Makes the Howl a Covert skin to simplify calculations
                quality = "C"
            elif quality == "":  # If hand wraps, assign glove quality
                quality = "G"
            wearfo.append(quality)
            case.append(wear)
            casefo.append(wearfo)
        prices.append(case)
        skinfo.append(casefo)

    if testTime:  # Prints time information
        web = 0
        func = 0
        for i in range(1, len(t)):
            ti = t[i][0] - t[i - 1][0]
            if t[i][1]:
                web += ti
            else:
                func += ti
        p = web / webp
        print(f"Price retrieval: {web:.2f}s ({p:.3f}s/page)\nCalculations: {func:.2f}s")

    return prices, skinfo
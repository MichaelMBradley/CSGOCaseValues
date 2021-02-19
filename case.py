from urllib.request import urlopen, Request
import re
import json
from bs4 import BeautifulSoup as bs
import time
import matplotlib.pyplot as mp

SITE = "https://csgostash.com"
WEBTIME = (2 / 7) + 0.1  # Estimate
CONDITIONS = ["FN", "MW", "FT", "WW", "BS"]
CONDITIONS = ["ST-" + CONDITION for CONDITION in CONDITIONS] + CONDITIONS
FULLCONDITIONS = [
    "Factory New",
    "Minimal Wear",
    "Field Tested",
    "Well Worn",
    "Battle Scarred",
]
FULLCONDITIONS = [
    "StatTrak " + CONDITION for CONDITION in FULLCONDITIONS
] + FULLCONDITIONS
RARITY = ["K", "G", "C", "Cl", "R", "MS"]
FULLRARITY = ["Knife", "Gloves", "Covert", "Classified", "Restricted", "Mil-Spec"]
KEYCOST = 3.16
WEIGHTS = {
    "K": 1 / 391,
    "G": 1 / 391,
    "C": 5 / 782,
    "Cl": 25 / 782,
    "R": 125 / 782,
    "MS": 625 / 782,
}
FLOATS = (0, 0.7, 0.15, 0.38, 0.45, 1)


class skin:
    def __init__(self, skinLink, skinPrices, skinInfo):
        self.link = skinLink
        self.name = getName(skinLink)
        self.prices = skinPrices
        self.rarity = skinInfo[2]
        self.wear = (skinInfo[0], skinInfo[1])
        self.wearRange = self.wear[1] - self.wear[0]
        self.value = self.calcValue()

    def calcValue(self):
        v = 0
        vs = 0
        if self.wear[0] == -1:
            return (self.prices[0] * 0.1) + (self.prices[1] * 0.9)
        else:
            for i in range(-5, 0):
                v += self.prices[i] * self.wearWeight(i + 5)
            if not (self.rarity == "G"):
                for i in range(5):
                    vs += self.prices[i] * self.wearWeight(i)
                v *= 0.9
                vs *= 0.1
            return v + vs

    def wearWeight(self, wearNum):
        if self.wear[0] > FLOATS[wearNum + 1] or self.wear[1] < FLOATS[wearNum]:
            return 0
        else:
            return (
                min(self.wear[1], FLOATS[wearNum + 1])
                - max(self.wear[0], FLOATS[wearNum])
            ) / self.wearRange


class case:
    def __init__(self, caseLink, casePrice, skinLinks, skinsPrices, skinsInfo):
        self.link = caseLink
        self.name = getName(caseLink)
        self.price = casePrice
        self.skins = []
        self.skinRarities = {"K": 0, "G": 0, "C": 0, "Cl": 0, "R": 0, "MS": 0}
        self.addSkins(skinLinks, skinsPrices, skinsInfo)
        self.value = self.calcValue()
        self.EV = self.value - (self.price + KEYCOST)

    def addSkins(self, skinLinks, skinsPrices, skinsInfo):
        for i in range(len(skinLinks)):
            self.skins.append(skin(skinLinks[i], skinsPrices[i], skinsInfo[i]))
            self.skinRarities[skinsInfo[i][2]] += 1

    def calcValue(self):
        v = 0
        for s in self.skins:
            v += s.value * WEIGHTS[s.rarity] / self.skinRarities[s.rarity]
        return v


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


def saveInfo(testTime=False):
    """
    Parameters
    ----------
    currPrice : Boolean, optional
        Saves the current price of skins to file. The default is False.
    testTime : Boolean, optional
        Records the time taken to read and download pages. The default is False.

    Returns
    -------
    cases : List of Strings
        List of links to cases on csgostash.com.
    skins : List of Lists of Strings
        Links to each weapons organized in the same order the case links were given.
    skinfo : List of Lists of Lists of Floats
        Float values and skin rarity for each weapon, organized in the same structure as the skin links.
    prices : List of Lists of Lists of Floats
        Prices for each wear rating for each weapon, organized in the same structure as the skin links.
    """
    cases = caseLinks()
    skins, caseCost = skinLinks(cases, testTime)
    prices, skinfo = getPrices(skins, testTime)

    with open("csgo/cases.json", "w") as filec:
        json.dump(cases, filec, indent=6)
    with open("csgo/skins.json", "w") as files:
        json.dump(skins, files, indent=6)
    with open("csgo/skinfo.json", "w") as filei:
        json.dump(skinfo, filei, indent=6)
    with open("csgo/prices.json", "w") as filep:
        json.dump(prices, filep, indent=6)
    with open("csgo/casePrices.json", "w") as filecp:
        json.dump(caseCost, filecp, indent=6)

    return cases, skins, skinfo, prices, caseCost


def readInfo():
    """
    Parameters
    ----------
    currPrice : Boolean, optional
        Reads the current price of skins from file. The default is False.

    Returns
    -------
    cases : List of Strings
        List of links to cases on csgostash.com.
    skins : List of Lists of Strings
        Links to each weapons organized in the same order the case links were given.
    skinfo : List of Lists of Lists of Floats
        Float values and skin rarity for each weapon, organized in the same structure as the skin links.
    prices : List of Lists of Lists of Floats
        Prices for each wear rating for each weapon, organized in the same structure as the skin links.
    """
    with open("csgo/cases.json", "r") as filec:
        cases = json.load(filec)
    with open("csgo/skins.json", "r") as files:
        skins = json.load(files)
    with open("csgo/skinfo.json", "r") as filei:
        skinfo = json.load(filei)
    with open("csgo/prices.json", "r") as filep:
        prices = json.load(filep)
    with open("csgo/casePrices.json", "r") as filecp:
        caseCost = json.load(filecp)

    return cases, skins, skinfo, prices, caseCost


def printPage(link):
    """
    Parameters
    ----------
    link : String
        Link to webpage.

    Returns
    -------
    None.
    """
    print(
        urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"}))
        .read()
        .decode("utf-8")
    )
    print("\n" + link)


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


def trackWorth(cases, prices, skinfo):
    pass  # Read historical data from file, update with new data, plot


def status(curr, length, msg=""):
    """
    Parameters
    ----------
    curr : Integer
        Current completion.
    length : Integer
        Total to be completed.
    msg : String, optional
        Message to display. The default is "".

    Returns
    -------
    None.
    """
    percent = curr / length
    t = (length - curr) * WEBTIME  # Time remaining
    if t < 60:
        t = str(round(t, 2)) + "s"  # Display in seconds or minutes
    else:
        t = str(int(t / 60)) + "m" + str(round(t % 60, 2)) + "s"
    print(
        f"\r{msg} Completed {curr:2}/{length:2} |"  # Completed/total
        + "█" * int(20 * curr / length)
        + "░" * int(20 * (length - curr) / length)  # Status bar
        + f"| {percent:.0%} | Remaining: {t}"
        + " " * 5,
        end="",
    )  #% done, time remaining
    if curr == length:
        print()  # Prints new line


def getName(link):
    """
    Parameters
    ----------
    name : String
        Link to case or skin.

    Return
    -------
    name : String
        Name of link.
    """
    return link[[i.start() for i in re.finditer("/", link)][-1] + 1 :].replace(
        "-", " "
    )  # Returns name from the last '/' until the end, replacing '-' with ' '


def info(skins, skinfo, prices):
    rel = []
    for i in range(6):
        rel.append([0] * 10)
    del rel[1][
        5:
    ]  # Initialize jagged 2d array, delete unnecessary values (no stattrak gloves)
    for case in range(len(prices)):
        for skin in range(len(prices[case])):
            if (
                (len(prices[case][skin]) == 10 or len(prices[case][skin]) == 5)
                and (not -1 in prices[case][skin])
                and (not -2 in prices[case][skin])
            ):  # If all skins accounted for
                for wear in range(len(prices[case][skin])):
                    rel[RARITY.index(skinfo[case][skin][-1])][wear] += (
                        prices[case][skin][wear] / prices[case][skin][-1]
                    )  # rel[rarity][wear] += (skin cost)/(BS skin cost)
    rel = [
        [round(i / relr[-1], 2) for i in relr][::-1] for relr in rel
    ]  # [[(price of wear)/(price of BS)]for each wear]

    return rel


def fillData(prices, skinfo, skins):
    rel = info(skins, skinfo, prices)
    for c in range(len(prices)):
        for s in range(len(prices[c])):
            for w in range(len(prices[c][s])):
                if prices[c][s][w] == -1:
                    i = 0
                    t = 0
                    qual = RARITY.index(skinfo[c][s][-1])
                    n = 5 if qual == 1 else 0
                    for j in range(len(prices[c][s])):
                        if prices[c][s][j] >= 0:
                            i += 1
                            t += (rel[qual][9 - w - n] / rel[qual][9 - j - n]) * prices[
                                c
                            ][s][j]
                    if i > 0:
                        prices[c][s][w] = round(t / i, 2)
                    else:
                        prices[c][s][w] = 0
    return prices


def calcWeights():
    weights = [2, 2, 5]
    for i in range(len(RARITY) - len(weights)):
        weights.append(weights[-1] * 5)
    total = str(sum(weights[1:]))
    print([str(w) + "/" + total for w in weights])


def plotInfo(rel):
    # Unnecessary
    mp.plot([0])
    for i in range(len(rel)):
        ax = mp.subplot(
            3, 2, i + 1, ylabel=FULLRARITY[i]
        )  # New subplot for each rarity level
        ax.plot(CONDITIONS[5:][::-1], rel[i][:5], label="Normal")

        for x, y in zip(CONDITIONS[5:][::-1], rel[i][:5]):  # Plots normal prices
            ax.annotate(str(y), xy=(x, y))  # Prints relative price for each data point

        if i != 1:
            ax.plot(CONDITIONS[5:][::-1], rel[i][5:], label="StatTrak")
            for x, y in zip(CONDITIONS[5:][::-1], rel[i][5:]):  # Plots StatTrak prices
                ax.annotate(str(y), xy=(x, y))
        mp.subplot(ax)

    mp.legend()
    mp.tight_layout()
    mp.figure(figsize=(20, 20), clear=True)
    mp.show()


def completeInfo(rel, prices, skins):
    # Unnecessary
    for c in range(len(prices)):
        for s in range(len(prices[c])):
            info = False
            for price in prices[c][s]:
                if not (price == -1 or price == -2):
                    info = True
                    break
            if not info:
                print(skins[c][s])


def toClass(cases, skins, skinfo, prices, caseCost):
    properCases = []
    for c in range(len(cases)):
        properCases.append(case(cases[c], caseCost[c], skins[c], prices[c], skinfo[c]))
    return properCases


def main():
    cases, skins, skinfo, prices, caseCost = readInfo()
    prices = fillData(prices, skinfo, skins)
    properCases = toClass(cases, skins, skinfo, prices, caseCost)
    for c in properCases:
        print(
            "{name}\nValue: {value:.2f}\nEV: {EV:.2f}".format(
                name=c.name, value=c.value, EV=c.EV
            )
        )


if __name__ == "__main__":
    main()
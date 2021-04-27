import re
from urllib.request import urlopen, Request
from filemanager import constants

[RARITY] = constants(["RARITY"])


def calcWeights():
    weights = [2, 2, 5]
    for i in range(len(RARITY) - len(weights)):
        weights.append(weights[-1] * 5)
    total = str(sum(weights[1:]))
    print([str(w) + "/" + total for w in weights])


def hasCompleteInfo(prices, skins):
    for c in range(len(prices)):
        for s in range(len(prices[c])):
            info = False
            for price in prices[c][s]:
                if not (price == -1 or price == -2):
                    info = True
                    break
            if not info:
                print(skins[c][s])


def getName(link):
    return link[[i.start() for i in re.finditer("/", link)][-1] + 1 :].replace("-", " ")  # Returns name from the last '/' until the end, replacing '-' with ' '


def printpage(link):
    print(f'{urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")}\n{link}')

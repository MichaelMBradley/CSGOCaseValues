import json
import os
from webreader import *

FILEDEST = os.path.dirname(__file__) + "\\caseinfo\\"


def saveInfo(testTime=False):
    cases = caseLinks()
    skins, caseCost = skinLinks(cases, testTime)
    prices, skinfo = getPrices(skins, testTime)

    with open(FILEDEST + "cases.json", "w") as filec:
        json.dump(cases, filec, indent=6)
    with open(FILEDEST + "skins.json", "w") as files:
        json.dump(skins, files, indent=6)
    with open(FILEDEST + "skinfo.json", "w") as filei:
        json.dump(skinfo, filei, indent=6)
    with open(FILEDEST + "prices.json", "w") as filep:
        json.dump(prices, filep, indent=6)
    with open(FILEDEST + "casePrices.json", "w") as filecp:
        json.dump(caseCost, filecp, indent=6)

    return cases, skins, skinfo, prices, caseCost


def readInfo():
    with open(FILEDEST + "cases.json", "r") as filec:
        cases = json.load(filec)
    with open(FILEDEST + "skins.json", "r") as files:
        skins = json.load(files)
    with open(FILEDEST + "skinfo.json", "r") as filei:
        skinfo = json.load(filei)
    with open(FILEDEST + "prices.json", "r") as filep:
        prices = json.load(filep)
    with open(FILEDEST + "casePrices.json", "r") as filecp:
        caseCost = json.load(filecp)

    return cases, skins, skinfo, prices, caseCost
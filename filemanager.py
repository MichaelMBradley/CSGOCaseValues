import json
import os
from webreader import *

FILEDEST = os.path.dirname(__file__) + "\\caseinfo\\"


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
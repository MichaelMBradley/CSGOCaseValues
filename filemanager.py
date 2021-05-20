import json
import os
from datetime import date

OPDN = os.path.dirname(__file__)


def constants(keys=[]):
    with open(f"{OPDN}\\constants.json", "r") as const:
        c = json.load(const)
    if keys == []:
        return c
    else:
        v = []
        for k in keys:
            v.append(c.get(k, None))
        return v


from webreader import *


def saveinfo(sampledata=False, overwrite=True):
    cases = caseLinks()
    skins, caseCost = skinLinks(cases)
    prices, skinfo = getPrices(skins)

    if sampledata:  # If writing new sample data
        FILEDEST = OPDN + "\\sampledata\\"
    else:
        FILEDEST = OPDN + "\\data\\" + f"{date.today()}"
        if not os.path.exists(FILEDEST):  # Data for new day -> create day directory
            os.makedirs(FILEDEST)
            FILEDEST = FILEDEST + "\\"
        else:  # Data already exists for today
            if overwrite:
                FILEDEST = FILEDEST + "\\"
            else:
                print("File already exists.")
                return [], [], [], [], []

    with open(FILEDEST + "cases.json", "w") as filec:
        json.dump(cases, filec, indent=6)
    with open(FILEDEST + "skins.json", "w") as files:
        json.dump(skins, files, indent=6)
    with open(FILEDEST + "skinfo.json", "w") as filei:
        json.dump(skinfo, filei, indent=6)
    with open(FILEDEST + "prices.json", "w") as filep:
        json.dump(prices, filep, indent=6)
    with open(FILEDEST + "caseprices.json", "w") as filecp:
        json.dump(caseCost, filecp, indent=6)

    return cases, skins, skinfo, prices, caseCost


def readinfo(filename=""):
    if filename == "":  # Default to reading sample data
        FILEDEST = OPDN + "\\sampledata\\"
    else:
        if len(filename.split("\\")) == 1:  # If only day is provideed
            FILEDEST = OPDN + "\\data\\" + filename
        else:  # If full filename is provided
            FILEDEST = filename
        if os.path.exists(FILEDEST):
            FILEDEST = FILEDEST + "\\"
        else:
            print("No such file.")
            return [], [], [], [], []
    with open(FILEDEST + "cases.json", "r") as filec:
        cases = json.load(filec)
    with open(FILEDEST + "skins.json", "r") as files:
        skins = json.load(files)
    with open(FILEDEST + "skinfo.json", "r") as filei:
        skinfo = json.load(filei)
    with open(FILEDEST + "prices.json", "r") as filep:
        prices = json.load(filep)
    with open(FILEDEST + "caseprices.json", "r") as filecp:
        caseCost = json.load(filecp)

    return cases, skins, skinfo, prices, caseCost

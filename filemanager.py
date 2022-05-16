import glob
import json
import os
from datetime import date

import orjson

from webreader import *

OPDN = os.path.dirname(__file__)


def jsonload(file):
    with open(file, "r") as f:
        return json.load(f)


def jsondump(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=6)


def orjsonload(file):
    with open(file, "rb") as f:
        return json.loads(f.read())


def orjsondump(file, data):
    with open(file, "wb") as f:
        f.write(orjson.dumps(data))


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

    cases = orjsonload(FILEDEST + "cases.json")
    skins = orjsonload(FILEDEST + "skins.json")
    skinfo = orjsonload(FILEDEST + "skinfo.json")
    prices = orjsonload(FILEDEST + "prices.json")
    caseprices = orjsonload(FILEDEST + "caseprices.json")

    return cases, skins, skinfo, prices, caseprices


def saveinfo(sampledata=False, overwrite=True):
    cases = get_case_urls()
    skins, caseprices = get_skin_links(cases)
    prices, skinfo = get_prices(skins)

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

    orjsondump(FILEDEST + "cases.json", cases)
    orjsondump(FILEDEST + "skins.json", skins)
    orjsondump(FILEDEST + "skinfo.json", skinfo)
    orjsondump(FILEDEST + "prices.json", prices)
    orjsondump(FILEDEST + "caseprices.json", caseprices)

    return cases, skins, skinfo, prices, caseprices

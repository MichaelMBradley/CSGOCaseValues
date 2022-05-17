import json
import os
from datetime import date

import orjson

from webreader import *

OPDN = os.path.dirname(__file__)


def json_load(file):
    with open(file, "r") as f:
        return json.load(f)


def json_dump(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=6)


def orjson_load(file):
    with open(file, "rb") as f:
        return json.loads(f.read())


def orjson_dump(file, data):
    with open(file, "wb") as f:
        f.write(orjson.dumps(data))


def read_info(filename=""):
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

    cases = orjson_load(FILEDEST + "cases.json")
    skins = orjson_load(FILEDEST + "skins.json")
    skinfo = orjson_load(FILEDEST + "skinfo.json")
    prices = orjson_load(FILEDEST + "prices.json")
    caseprices = orjson_load(FILEDEST + "caseprices.json")

    return cases, skins, skinfo, prices, caseprices


def save_info(sampledata=False, overwrite=True):
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

    orjson_dump(FILEDEST + "cases.json", cases)
    orjson_dump(FILEDEST + "skins.json", skins)
    orjson_dump(FILEDEST + "skinfo.json", skinfo)
    orjson_dump(FILEDEST + "prices.json", prices)
    orjson_dump(FILEDEST + "caseprices.json", caseprices)

    return cases, skins, skinfo, prices, caseprices

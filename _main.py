from case import case
from filemanager import *
from value import fillData


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
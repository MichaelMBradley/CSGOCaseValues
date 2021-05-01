from filemanager import *
from vis import *


def main():
    # saveinfo()
    # plotcases(readhistoricaldata())
    # printhistoricaldata(mostrecent=True, value=lambda case: case.EV)
    # dropped(recentcases())
    cases, skins, skinfo, prices, caseCost = readinfo()
    plotRelativePrices(prices, skinfo, skins)


if __name__ == "__main__":
    main()

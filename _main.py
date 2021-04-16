from case import *
from filemanager import *
from value import *
from vis import *


def main():
    cases, skins, skinfo, prices, caseCost = saveinfo(testTime=True)
    printhistoricaldata()


if __name__ == "__main__":
    main()

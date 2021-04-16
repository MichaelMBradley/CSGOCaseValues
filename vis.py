from case import toClass
from constants import *
from filemanager import readinfo
import glob
import matplotlib.pyplot as mp
import os
from value import analysis, fillData
from misc import status


def casesort(c):
    # Used only for sorting cases
    return c.EV


def plotRelativePrices(rel):
    # Plots the relative prices of different wear values, seperated by rarity
    mp.plot([0])
    for i in range(len(rel)):
        ax = mp.subplot(3, 2, i + 1, ylabel=FULLRARITY[i])  # New subplot for each rarity level
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


def printhistoricaldata():
    caselist = readhistoricaldata()
    for (date, cases) in caselist:
        print(f"\n{date}")
        printsortedcaselist(cases)


def printsortedcaselist(caselist):
    cases = caselist.copy()
    cases.sort(key=casesort, reverse=True)
    print(f"EV\t(Value\tPrice)\tName")
    for c in cases:
        print(f"{c.EV:.4f}\t({c.value:>5.2f}\t{c.totalprice:>5.2f})\t{c.name}")


def readhistoricaldata():
    caselist = []
    files = glob.glob(os.path.dirname(__file__) + "\\data\\*")
    curr = 0
    total = len(files)
    status(curr, total, "Reading and analyzing files")
    for fname in files:
        caselist.append((fname.split("\\")[-1], analysis(fname)))
        curr += 1
        status(curr, total, "Reading and analyzing files")
    return caselist

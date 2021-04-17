from case import toClass
from constants import *
from filemanager import readinfo
import glob
import matplotlib.pyplot as mp
import os
from value import analysis, fillData
from status import *


def casesort(c):
    # Used only for sorting cases
    return c.EV


def dropped(cases):
    p = []
    np = []
    for case in cases:
        if case.name in PRIMECASES:
            p.append(case)
        if case.name in NONPRIMECASES:
            np.append(case)
    print(f"{'':>20} \t(Drop) (Bought)")
    print("Prime drops expected value:")
    for case in p:
        print(f"{case.name:>20}:\t{case.EVNK:.4f}\t{case.EV:.4f}")
    print("Non-Prime drops expected value:")
    for case in np:
        print(f"{case.name:>20}:\t{case.EVNK:.4f}\t{case.EV:.4f}")


def plotcases(datecases):
    dates = []
    cases = {}
    for comb in datecases:
        dates.append(comb[0])
        for case in comb[1]:
            if case.name in cases.keys():
                cases[case.name].append(case.EV)
            else:
                cases[case.name] = [case.EV]
    # mp.subplot(1, 2, 1)
    for case in cases.keys():
        mp.plot(dates, cases[case], label=case)
        mp.text(dates[-1], cases[case][-1], case, horizontalalignment="right")
    # mp.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=2)
    mp.title("CSGO Case Unboxing Expected Values")
    mp.xlabel("Date")
    mp.ylabel("Expected Value")
    mp.ylim([0, 1])
    mp.show()


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
    progress = statusbar(len(files), "Reading and analyzing files")
    for fname in files:
        caselist.append((fname.split("\\")[-1], analysis(fname)))
        progress.incrementandprint()
    return caselist

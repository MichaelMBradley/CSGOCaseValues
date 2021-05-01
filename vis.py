from case import toClass
from filemanager import readinfo
import glob
import matplotlib.pyplot as mp
from matplotlib.ticker import MultipleLocator
import os
from value import *
from status import *
from filemanager import constants

[CASEGROUPS, FULLRARITY, CONDITIONS] = constants(["CASEGROUPS", "FULLRARITY", "CONDITIONS"])


def dropped(cases):
    p = []
    np = []
    r = []
    for case in cases:
        if case.name in CASEGROUPS["Prime"]:
            p.append(case)
        if case.name in CASEGROUPS["Non-Prime"]:
            np.append(case)
        if case.name in CASEGROUPS["Rare"]:
            r.append(case)
    print(f"{'':>35} \t(Drop) (Bought)\t(Probability of getting an item worth more than a key)")
    print("Prime drops expected value:")
    for case in p:
        print(f"{case.name:>35}:\t{case.EVD:.4f}\t{case.EV:.4f}\t{case.probdrop:.4f}")
    print("Non-Prime drops expected value:")
    for case in np:
        print(f"{case.name:>35}:\t{case.EVD:.4f}\t{case.EV:.4f}\t{case.probdrop:.4f}")
    print("Rare drops expected value:")
    for case in r:
        print(f"{case.name:>35}:\t{case.EVD:.4f}\t{case.EV:.4f}\t{case.probdrop:.4f}")


def groups(datecases, allowed):
    """
    Groups:

    Chroma
    Weapon
    eSports
    Gamma
    Operation
    Spectrum
    Other
    All

    Prime
    Non-Prime
    Rare
    Drops
    """
    if "All" in allowed:
        return datecases
    if allowed == ["Drops"]:
        allowed = ["Prime", "Non-Prime", "Rare"]
    for date in datecases:
        cases = date[1]
        newcases = []
        for case in cases:
            for g in allowed:
                if case.name in CASEGROUPS[g]:
                    newcases.append(case)
                    break
        date[1] = newcases
    return datecases


def plotcases(datecases, value=lambda case: case.EV, legend=False, colour=True, area=(0, 1), about="Expected Value"):
    # ---ANALYSIS---
    if area != None:
        textsize = 0.012 * (area[1] - area[0])
    else:
        textsize = 0.012
    dates = []
    cases = {}
    for comb in datecases:
        dates.append(comb[0])
        sort = sortcases(comb[1], value=value)
        for case in sort:
            ev = value(case)
            if case.name in cases.keys():
                cases[case.name].append(ev)
            else:
                cases[case.name] = [ev]
    # ---SPACING---
    names = []
    for casename in cases.keys():
        names.append([casename, cases[casename][-1] - (textsize / 2)])
    names.sort(key=lambda t: t[1], reverse=True)
    namesl = names[::2]
    namesr = names[1::2]
    spread(namesl, textsize)
    spread(namesr, textsize)
    if legend:
        mp.subplot(1, 2, 1)
    for casename in cases.keys():
        mp.plot(dates, cases[casename], label=casename)
    if legend:
        mp.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)  # Useless, too many colours
    colours = [line.get_color() if colour else "000000" for line in mp.gca().lines]
    start = [case.name for case in sortcases(datecases[0][1], value=value)]
    end = [case.name for case in sortcases(datecases[-1][1], value=value)]
    fixed = [""] * len(colours)
    for i in range(len(colours)):
        fixed[end.index(start[i])] = colours[i]
    # ---PLOTTING---
    if not legend:
        for (i, t) in zip(range(len(namesl)), namesl):
            ind = t[0].index(" Case")
            t[0] = t[0][:ind] + t[0][ind + 5 :]
            mp.text(dates[-1], t[1], t[0], horizontalalignment="left", color=fixed[i * 2])
        for (i, t) in zip(range(len(namesr)), namesr):
            ind = t[0].index(" Case")
            t[0] = t[0][:ind] + t[0][ind + 5 :]
            onleft = True in [abs(t[1] - n[1]) <= textsize for n in namesl]
            mp.text(dates[-1], t[1], t[0], horizontalalignment="right" if onleft else "left", color="000000" if onleft else fixed[i * 2 + 1])
    mp.title("CSGO Case Unboxing")
    mp.xlabel("Date")
    mp.ylabel(about)
    if area != None:
        mp.ylim(area)
    mp.grid(axis="y")
    mp.show()


def plotRelativePrices(prices, skinfo, skins):
    rel = info(prices, skinfo, skins)
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


def printhistoricaldata(value=lambda case: case.EV, mostrecent=False):
    if mostrecent:
        caselist = [["Most recent", recentcases()]]
    else:
        caselist = readhistoricaldata()
    print(caselist)
    for [date, cases] in caselist:
        print(f"\n{date}")
        printsortedcaselist(cases, value)


def printsortedcaselist(caselist, value=lambda case: case.EV):
    cases = sortcases(caselist)
    print(f"EV\t(Value\tPrice)\tName")
    for c in cases:
        print(f"{value(c):.4f}\t({c.value:>5.2f}\t{c.totalprice:>5.2f})\t{c.name}")


def readhistoricaldata():
    caselist = []
    files = glob.glob(os.path.dirname(__file__) + "\\data\\*")
    progress = statusbar(len(files), "Reading and analyzing files")
    for fname in files:
        caselist.append([fname.split("\\")[-1], analysis(fname)])
        progress.incrementandprint()
    return caselist


def recentcases():
    return analysis(glob.glob(os.path.dirname(__file__) + "\\data\\*")[-1])


def sortcases(caselist, value=lambda case: case.EV, descending=True):
    cases = caselist.copy()
    cases.sort(key=value, reverse=descending)
    return cases


def spread(names, textsize):
    settled = False
    while not settled:
        settled = True
        for i in range(len(names) - 1):
            diff = abs(names[i][1] - names[i + 1][1])
            if diff < textsize:
                settled = False
                move = (textsize - diff) / 2 + 0.001
                names[i][1] += move
                for j in range(i - 1, -1, -1):
                    if names[j][1] < names[j + 1][1]:
                        names[j][1] += move
                    else:
                        break
                names[i + 1][1] -= move
                for j in range(i + 1, len(names)):
                    if names[j][1] > names[j - 1][1]:
                        names[j][1] += move
                    else:
                        break

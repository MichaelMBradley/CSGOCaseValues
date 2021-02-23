from constants import *
import matplotlib.pyplot as mp
import re
from urllib.request import urlopen, Request


def calcWeights():
    weights = [2, 2, 5]
    for i in range(len(RARITY) - len(weights)):
        weights.append(weights[-1] * 5)
    total = str(sum(weights[1:]))
    print([str(w) + "/" + total for w in weights])


def hasCompleteInfo(prices, skins):
    for c in range(len(prices)):
        for s in range(len(prices[c])):
            info = False
            for price in prices[c][s]:
                if not (price == -1 or price == -2):
                    info = True
                    break
            if not info:
                print(skins[c][s])


def getName(link):
    """
    Parameters
    ----------
    name : String
        Link to case or skin.

    Return
    -------
    name : String
        Name of link.
    """
    return link[[i.start() for i in re.finditer("/", link)][-1] + 1 :].replace(
        "-", " "
    )  # Returns name from the last '/' until the end, replacing '-' with ' '


def plotInfo(rel):
    # Unnecessary
    mp.plot([0])
    for i in range(len(rel)):
        ax = mp.subplot(
            3, 2, i + 1, ylabel=FULLRARITY[i]
        )  # New subplot for each rarity level
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


def printPage(link):
    """
    Parameters
    ----------
    link : String
        Link to webpage.

    Returns
    -------
    None.
    """
    print(
        urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"}))
        .read()
        .decode("utf-8")
    )
    print("\n" + link)


def status(curr, length, msg=""):
    """
    Parameters
    ----------
    curr : Integer
        Current completion.
    length : Integer
        Total to be completed.
    msg : String, optional
        Message to display. The default is "".

    Returns
    -------
    None.
    """
    percent = curr / length
    t = (length - curr) * WEBTIME  # Time remaining
    if t < 60:
        t = str(round(t, 2)) + "s"  # Display in seconds or minutes
    else:
        t = str(int(t / 60)) + "m" + str(round(t % 60, 2)) + "s"
    print(
        f"\r{msg} Completed {curr:2}/{length:2} |"  # Completed/total
        + "█" * int(20 * curr / length)
        + "░" * int(20 * (length - curr) / length)  # Status bar
        + f"| {percent:.0%} | Remaining: {t}"
        + " " * 5,
        end="",
    )  #% done, time remaining
    if curr == length:
        print()  # Prints new line
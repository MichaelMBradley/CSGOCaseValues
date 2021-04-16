from constants import *
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
    return link[[i.start() for i in re.finditer("/", link)][-1] + 1 :].replace("-", " ")  # Returns name from the last '/' until the end, replacing '-' with ' '


def printpage(link):
    print(f'{urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")}\n{link}')


def printtesttime(t, webp):
    web = 0
    func = 0
    for i in range(1, len(t)):
        ti = t[i][0] - t[i - 1][0]
        if t[i][1]:
            web += ti
        else:
            func += ti
    pw = web / webp
    pc = func / webp
    print(f"Webpage retrieval: {web:.2f}s ({pw:.3f}s/page)\nCalculations: {func:.2f}s ({pc:.2f}s/page)")


def status(curr, length, msg=""):
    percent = curr / length
    t = (length - curr) * WEBTIME  # Time remaining
    if t < 60:
        t = str(round(t, 2)) + "s"  # Display in seconds or minutes
    else:
        t = str(int(t / 60)) + "m" + str(round(t % 60, 2)) + "s"
    print(f"\r{msg} Completed {curr:2}/{length:2} |" + "█" * int(20 * curr / length) + "░" * int(20 * (length - curr) / length) + f"| {percent:.0%} | Remaining: {t}" + " " * 5, end="")
    if curr == length:
        print()  # Prints new line

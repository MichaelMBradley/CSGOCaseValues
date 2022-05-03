from re import finditer
from urllib.request import urlopen, Request
from filemanager import constants

[RARITY] = constants(["RARITY"])


def calc_weights():
    weights = [2, 2, 5]
    for i in range(len(RARITY) - len(weights)):
        weights.append(weights[-1] * 5)
    total = str(sum(weights[1:]))
    print([str(w) + "/" + total for w in weights])


def has_complete_info(prices, skins):
    for c in range(len(prices)):
        for s in range(len(prices[c])):
            info = False
            for price in prices[c][s]:
                if not (price == -1 or price == -2):
                    info = True
                    break
            if not info:
                print(skins[c][s])


def get_name(link):
    return link[[i.start() for i in finditer("/", link)][-1] + 1 :].replace("-", " ")  # Returns name from the last '/' until the end, replacing '-' with ' '


def print_page(link):
    print(f'{urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")}\n{link}')

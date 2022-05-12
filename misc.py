from re import finditer
from urllib.request import urlopen, Request
from filemanager import constants

[RARITY] = constants(["RARITY"])


def calc_weights() -> None:
    weights = [2, 2, 5]
    for i in range(len(RARITY) - len(weights)):
        weights.append(weights[-1] * 5)
    total = str(sum(weights[1:]))
    print([str(w) + "/" + total for w in weights])


def has_complete_info(prices: list[list[list[float]]], skins: list[list[str]]) -> None:
    # TODO: avoid `range(len(...))`
    for c in range(len(prices)):
        for s in range(len(prices[c])):
            info = False
            for price in prices[c][s]:
                if not (price == -1 or price == -2):
                    info = True
                    break
            if not info:
                print(skins[c][s])


def get_name(link: str) -> str:
    # Returns name from the last '/' until the end, replacing '-' with ' '
    return link[[i.start() for i in finditer("/", link)][-1] + 1 :].replace("-", " ")


def print_page(link: str) -> None:
    print(f'{urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8")}\n{link}')

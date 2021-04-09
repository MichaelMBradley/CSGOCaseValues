from constants import *
from case import case


def fillData(prices, skinfo, skins):
    rel = info(skins, skinfo, prices)
    for c in range(len(prices)):
        for s in range(len(prices[c])):
            for w in range(len(prices[c][s])):
                if prices[c][s][w] == -1:
                    i = 0
                    t = 0
                    qual = RARITY.index(skinfo[c][s][-1])
                    n = 5 if qual == 1 else 0
                    for j in range(len(prices[c][s])):
                        if prices[c][s][j] >= 0:
                            i += 1
                            t += (rel[qual][9 - w - n] / rel[qual][9 - j - n]) * prices[c][s][j]
                    if i > 0:
                        prices[c][s][w] = round(t / i, 2)
                    else:
                        prices[c][s][w] = 0
    return prices


def info(skins, skinfo, prices):
    rel = []
    for i in range(6):
        rel.append([0] * 10)
    del rel[1][5:]  # Initialize jagged 2d array, delete unnecessary values (no stattrak gloves)
    for case in range(len(prices)):
        for skin in range(len(prices[case])):
            if (len(prices[case][skin]) == 10 or len(prices[case][skin]) == 5) and (not -1 in prices[case][skin]) and (not -2 in prices[case][skin]):  # If all skins accounted for
                for wear in range(len(prices[case][skin])):
                    rel[RARITY.index(skinfo[case][skin][-1])][wear] += prices[case][skin][wear] / prices[case][skin][-1]  # rel[rarity][wear] += (skin cost)/(BS skin cost)
    rel = [[round(i / relr[-1], 2) for i in relr][::-1] for relr in rel]  # [[(price of wear)/(price of BS)]for each wear]

    return rel
from misc import getName
from skin import skin
from constants import KEYCOST, WEIGHTS


class case:
    def __init__(self, caseLink, casePrice, skinLinks, skinsPrices, skinsInfo):
        self.link = caseLink
        self.name = getName(caseLink)
        self.price = casePrice
        self.totalprice = self.price + KEYCOST
        self.skins = []
        self.skinRarities = {"K": 0, "G": 0, "C": 0, "Cl": 0, "R": 0, "MS": 0}
        self.addSkins(skinLinks, skinsPrices, skinsInfo)
        self.value = self.calcValue()
        self.EV = self.value / self.totalprice
        self.EVNK = self.value / KEYCOST

    def addSkins(self, skinLinks, skinsPrices, skinsInfo):
        for i in range(len(skinLinks)):
            self.skins.append(skin(skinLinks[i], skinsPrices[i], skinsInfo[i]))
            self.skinRarities[skinsInfo[i][2]] += 1

    def calcValue(self, info=False):
        v = 0
        if info:
            print(f"CASE: {self.name}\nCost\tWeight\tRarity\tValue\tName")
        for s in self.skins:
            if info:
                print(f"{s.value:.2f}\t{WEIGHTS[s.rarity]:.4f}\t{self.skinRarities[s.rarity]:.2f}\t{s.value * WEIGHTS[s.rarity] / self.skinRarities[s.rarity]:.2f}\t{s.name}")
            v += s.value * WEIGHTS[s.rarity] / self.skinRarities[s.rarity]
        if info:
            print(f"{v:.2f}")
        return v

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} with an EV of {self.EV:.2f}"


def toClass(cases, skins, skinfo, prices, caseCost):
    properCases = []
    for c in range(len(cases)):
        properCases.append(case(cases[c], caseCost[c], skins[c], prices[c], skinfo[c]))
    return properCases

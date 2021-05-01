from misc import getName
from skin import skin
from filemanager import constants

[KEYCOST, WEIGHTS] = constants(["KEYCOST", "WEIGHTS"])


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
        self.valuens = self.calcValue(special=False)
        self.EV = self.value / self.totalprice
        self.EVD = self.value / KEYCOST  # Expected value if recieved as a drop
        self.EVNS = self.valuens / self.totalprice  # Expected value without knives/gloves
        self.prob = self.calcProbability()
        self.probdrop = self.calcProbability(drop=True)

    def addSkins(self, skinLinks, skinsPrices, skinsInfo):
        for i in range(len(skinLinks)):
            self.skins.append(skin(skinLinks[i], skinsPrices[i], skinsInfo[i]))
            self.skinRarities[skinsInfo[i][2]] += 1

    def calcProbability(self, info=False, drop=False):
        p = 0
        if info:
            print(f"CASE: {self.name}\nCost\tWeight\tValue\tName")
        for s in self.skins:
            if info:
                print(f"{s.value:.2f}\t{WEIGHTS[s.rarity] / self.skinRarities[s.rarity]:.4f}\t{(WEIGHTS[s.rarity] / self.skinRarities[s.rarity]) * s.calcProbability(KEYCOST if drop else self.totalprice):.4f}\t{s.name}")
            p += (WEIGHTS[s.rarity] / self.skinRarities[s.rarity]) * s.calcProbability(KEYCOST if drop else self.totalprice, info=info)
        if info:
            print(f"Probability of making a profit (Dropped: {drop}): {p}")
        return p

    def calcValue(self, info=False, special=True):
        v = 0
        if info:
            print(f"CASE: {self.name}\nCost\tWeight\tValue\tName")
        for s in self.skins:
            if info and (special or s.rarity not in ["K", "G"]):
                print(f"{s.value:.2f}\t{WEIGHTS[s.rarity] / self.skinRarities[s.rarity]:.4f}\t{s.value * WEIGHTS[s.rarity] / self.skinRarities[s.rarity]:.2f}\t{s.name}")
            if special or s.rarity not in ["K", "G"]:
                v += s.value * WEIGHTS[s.rarity] / self.skinRarities[s.rarity]
        if info:
            print(f"Total Value: {v:.2f}\nExpected Value: {v/self.totalprice:.2f}")
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

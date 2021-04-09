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

    def addSkins(self, skinLinks, skinsPrices, skinsInfo):
        for i in range(len(skinLinks)):
            self.skins.append(skin(skinLinks[i], skinsPrices[i], skinsInfo[i]))
            self.skinRarities[skinsInfo[i][2]] += 1

    def calcValue(self):
        v = 0
        # print(f"CASE: {self.name}\nCost\tWeight\tRarity\tValue\tName")
        for s in self.skins:
            # print(f"{s.value:.2f}\t{WEIGHTS[s.rarity]:.4f}\t{self.skinRarities[s.rarity]:.2f}\t{s.value * WEIGHTS[s.rarity] / self.skinRarities[s.rarity]:.2f}\t{s.name}")
            v += s.value * WEIGHTS[s.rarity] / self.skinRarities[s.rarity]
        # print(f"{v:.2f}")
        return v

class case:
    def __init__(self, caseLink, casePrice, skinLinks, skinsPrices, skinsInfo):
        self.link = caseLink
        self.name = getName(caseLink)
        self.price = casePrice
        self.skins = []
        self.skinRarities = {"K": 0, "G": 0, "C": 0, "Cl": 0, "R": 0, "MS": 0}
        self.addSkins(skinLinks, skinsPrices, skinsInfo)
        self.value = self.calcValue()
        self.EV = self.value - (self.price + KEYCOST)

    def addSkins(self, skinLinks, skinsPrices, skinsInfo):
        for i in range(len(skinLinks)):
            self.skins.append(skin(skinLinks[i], skinsPrices[i], skinsInfo[i]))
            self.skinRarities[skinsInfo[i][2]] += 1

    def calcValue(self):
        v = 0
        for s in self.skins:
            v += s.value * WEIGHTS[s.rarity] / self.skinRarities[s.rarity]
        return v
from constants import *
from misc import getName


class skin:
    def __init__(self, skinLink, skinPrices, skinInfo):
        self.link = skinLink
        self.name = getName(skinLink)
        self.prices = skinPrices
        self.rarity = skinInfo[2]
        self.wear = (skinInfo[0], skinInfo[1])
        self.wearRange = self.wear[1] - self.wear[0]
        self.value = self.calcValue()

    def calcValue(self):
        v = 0
        vs = 0
        if self.wear[0] == -1:
            return (self.prices[0] * 0.1) + (self.prices[1] * 0.9)
        else:
            for i in range(-5, 0):
                v += self.prices[i] * self.wearWeight(i + 5)
            if not (self.rarity == "G"):
                for i in range(5):
                    vs += self.prices[i] * self.wearWeight(i)
                v *= 0.9
                vs *= 0.1
            return v + vs

    def wearWeight(self, wearNum):
        if self.wear[0] > FLOATS[wearNum + 1] or self.wear[1] < FLOATS[wearNum]:
            return 0
        else:
            return (min(self.wear[1], FLOATS[wearNum + 1]) - max(self.wear[0], FLOATS[wearNum])) / self.wearRange

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} with a value of {self.value:.2f}"

from misc import getName
from filemanager import constants

[FLOATS] = constants(["FLOATS"])


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

    def calcProbability(self, price, info=False):
        p = 0
        ps = 0
        if self.wear[0] == -1:
            return (0.1 if self.prices[0] >= price else 0) + (0.9 if self.prices[1] >= price else 0)
        else:
            if info:
                print(f"{self.name}\nNon-ST:")
            for i in range(-5, 0):
                if info:
                    print(f"{self.wearWeight(i + 5):.4f}\t{self.prices[i]}\t{price}")
                p += self.wearWeight(i + 5) if self.prices[i] >= price else 0
            if not (self.rarity == "G"):
                if info:
                    print("ST:")
                for i in range(5):
                    if info:
                        print(f"{self.wearWeight(i):.4f}\t{self.prices[i]}\t{price}")
                    ps += self.wearWeight(i) if self.prices[i] >= price else 0
                p *= 0.9
                ps *= 0.1
            if info:
                print(f"{p+ps}")
            return p + ps

    def wearWeight(self, wearNum):
        if self.wear[0] > FLOATS[wearNum + 1] or self.wear[1] < FLOATS[wearNum]:
            return 0
        else:
            return (min(self.wear[1], FLOATS[wearNum + 1]) - max(self.wear[0], FLOATS[wearNum])) / self.wearRange

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} with a value of {self.value:.2f}"

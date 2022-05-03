from misc import get_name
from filemanager import constants

[FLOATS] = constants(["FLOATS"])


class Skin:
    def __init__(self, skin_link, skin_prices, skin_info):
        self.link = skin_link
        self.name = get_name(skin_link)
        self.prices = skin_prices
        self.rarity = skin_info[2]
        self.wear = (skin_info[0], skin_info[1])
        self.wearRange = self.wear[1] - self.wear[0]
        self.value = self.calc_value()

    def calc_value(self):
        v = 0
        vs = 0
        if self.wear[0] == -1:
            return (self.prices[0] * 0.1) + (self.prices[1] * 0.9)
        else:
            for i in range(-5, 0):
                v += self.prices[i] * self.wear_weight(i + 5)
            if not (self.rarity == "G"):
                for i in range(5):
                    vs += self.prices[i] * self.wear_weight(i)
                v *= 0.9
                vs *= 0.1
            return v + vs

    def calc_probability(self, price, info=False):
        p = 0
        ps = 0
        if self.wear[0] == -1:
            return (0.1 if self.prices[0] >= price else 0) + (0.9 if self.prices[1] >= price else 0)
        else:
            if info:
                print(f"{self.name}\nNon-ST:")
            for i in range(-5, 0):
                if info:
                    print(f"{self.wear_weight(i + 5):.4f}\t{self.prices[i]}\t{price}")
                p += self.wear_weight(i + 5) if self.prices[i] >= price else 0
            if not (self.rarity == "G"):
                if info:
                    print("ST:")
                for i in range(5):
                    if info:
                        print(f"{self.wear_weight(i):.4f}\t{self.prices[i]}\t{price}")
                    ps += self.wear_weight(i) if self.prices[i] >= price else 0
                p *= 0.9
                ps *= 0.1
            if info:
                print(f"{p+ps}")
            return p + ps

    def wear_weight(self, wear_num):
        if self.wear[0] > FLOATS[wear_num + 1] or self.wear[1] < FLOATS[wear_num]:
            return 0
        else:
            return (min(self.wear[1], FLOATS[wear_num + 1]) - max(self.wear[0], FLOATS[wear_num])) / self.wearRange

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} with a value of {self.value:.2f}"

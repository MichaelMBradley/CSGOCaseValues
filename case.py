from misc import get_name
from skin import Skin
from filemanager import constants

[KEYCOST, WEIGHTS] = constants(["KEYCOST", "WEIGHTS"])


class Case:
    def __init__(self, case_link: str, case_price: float, skin_links: list[str], skins_prices, skins_info):
        self.link = case_link
        self.name = get_name(case_link)
        self.price = case_price
        self.total_price = self.price + KEYCOST
        self.skins = []
        self.skinRarities = {"K": 0, "G": 0, "C": 0, "Cl": 0, "R": 0, "MS": 0}
        self.add_skins(skin_links, skins_prices, skins_info)
        self.value = self.calc_value()
        self.value_ns = self.calc_value(special=False)
        self.EV = self.value / self.total_price
        self.EV_D = self.value / KEYCOST  # Expected value if received as a drop
        self.EV_NS = self.value_ns / self.total_price  # Expected value without knives/gloves
        self.prob = self.calc_probability()
        self.prob_drop = self.calc_probability(drop=True)

    def add_skins(self, skin_links, skins_prices, skins_info):
        for i in range(len(skin_links)):
            self.skins.append(Skin(skin_links[i], skins_prices[i], skins_info[i]))
            self.skinRarities[skins_info[i][2]] += 1

    def calc_probability(self, info=False, drop=False):
        p = 0
        if info:
            print(f"CASE: {self.name}\nCost\tWeight\tValue\tName")
        for s in self.skins:
            if info:
                print(f"{s.value:.2f}\t{WEIGHTS[s.RARITY] / self.skinRarities[s.RARITY]:.4f}\t{(WEIGHTS[s.RARITY] / self.skinRarities[s.RARITY]) * s.calc_probability(KEYCOST if drop else self.total_price):.4f}\t{s.name}")
            p += (WEIGHTS[s.RARITY] / self.skinRarities[s.RARITY]) * s.calc_probability(KEYCOST if drop else self.total_price, info=info)
        if info:
            print(f"Probability of making a profit (Dropped: {drop}): {p}")
        return p

    def calc_value(self, info=False, special=True):
        v = 0
        if info:
            print(f"CASE: {self.name}\nCost\tWeight\tValue\tName")
        for s in self.skins:
            if info and (special or s.RARITY not in ["K", "G"]):
                print(f"{s.value:.2f}\t{WEIGHTS[s.RARITY] / self.skinRarities[s.RARITY]:.4f}\t{s.value * WEIGHTS[s.RARITY] / self.skinRarities[s.RARITY]:.2f}\t{s.name}")
            if special or s.RARITY not in ["K", "G"]:
                v += s.value * WEIGHTS[s.RARITY] / self.skinRarities[s.RARITY]
        if info:
            print(f"Total Value: {v:.2f}\nExpected Value: {v/self.total_price:.2f}")
        return v

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} with an EV of {self.EV:.2f}"


def to_class(cases, skins, skinfo, prices, case_cost) -> list[Case]:
    return [Case(*info) for info in zip(cases, case_cost, skins, prices, skinfo)]

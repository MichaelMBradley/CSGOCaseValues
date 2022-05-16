from constants import Constants
from skin import Skin
from webreader import get_name_from_url, get_skins, read_page


class Case:
    def __init__(self, link: str):
        self.link = link
        self.name = get_name_from_url(link)

        case_page = read_page(link)
        self.price = get_case_price(case_page)
        self.total_price = self.price + Constants.KEY_COST
        self.skins = get_skins(case_page)

        self.skinRarities: dict[str: int] = {}
        self.count_rarities()

        # Expected value
        self.value = self.calc_value()
        self.value_ns = self.calc_value(special=False)

        # Expected value, compensating for price
        self.EV = self.value / self.total_price
        self.EV_D = self.value / Constants.KEY_COST  # Expected value if received as a drop
        self.EV_NS = self.value_ns / self.total_price  # Expected value without knives/gloves

        # Probability of making money on a drop
        self.prob = self.calc_probability()
        self.prob_drop = self.calc_probability(drop=True)

    def count_rarities(self) -> None:
        self.skinRarities = {"K": 0, "G": 0, "C": 0, "Cl": 0, "R": 0, "MS": 0}

    def calc_probability(self, info: bool = False, drop: bool = False) -> float:
        p = 0
        if info:
            print(f"CASE: {self.name}\nCost\tWeight\tValue\tName")
        for s in self.skins:
            if info:
                print(f"{s.value:.2f}\t{Constants.WEIGHTS[s.rarity] / self.skinRarities[s.rarity]:.4f}\t{(Constants.WEIGHTS[s.rarity] / self.skinRarities[s.rarity]) * s.calc_probability(Constants.KEY_COST if drop else self.total_price):.4f}\t{s.name}")
            p += (Constants.WEIGHTS[s.rarity] / self.skinRarities[s.rarity]) * s.calc_probability(Constants.KEY_COST if drop else self.total_price, info=info)
        if info:
            print(f"Probability of making a profit (Dropped: {drop}): {p}")
        return p

    def calc_value(self, info: bool = False, special: bool = True) -> float:
        v = 0
        if info:
            print(f"CASE: {self.name}\nCost\tWeight\tValue\tName")
        for s in self.skins:
            if info and (special or s.rarity not in ["K", "G"]):
                print(f"{s.value:.2f}\t{Constants.WEIGHTS[s.rarity] / self.skinRarities[s.rarity]:.4f}\t{s.value * Constants.WEIGHTS[s.rarity] / self.skinRarities[s.rarity]:.2f}\t{s.name}")
            if special or s.rarity not in ["K", "G"]:
                v += s.value * Constants.WEIGHTS[s.rarity] / self.skinRarities[s.rarity]
        if info:
            print(f"Total Value: {v:.2f}\nExpected Value: {v/self.total_price:.2f}")
        return v

    def convert_to_dict(self) -> dict:
        """
        Converts the instance to a dictionary for ease of output.
        """
        pass

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} with an EV of {self.EV:.2f}"


def get_case_price(case_page: str) -> float:
    pass


def to_class(cases, skins, skinfo, prices, case_cost) -> list[Case]:
    return [Case(*info) for info in zip(cases, case_cost, skins, prices, skinfo)]

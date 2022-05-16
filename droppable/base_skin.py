from constants import Constants
from droppable.droppable import Droppable
from webreader import read_page


class Skin(Droppable):
    def __init__(self, url: str, delay_init: bool):
        super().__init__(url, delay_init)

        if delay_init:
            return

        page = read_page(url)
        self.prices: list[float] = get_skin_prices(page)
        self.rarity: str = get_skin_rarity(page)
        self.float_range: tuple[float, float] = get_skin_float_range(page)

        self.wearRange: float = self.float_range[1] - self.float_range[0]
        self.value: float = self.calc_value()

    def calc_value(self) -> float:
        """
        Calculate the expected value of this skin.
        """
        value = 0
        value_st = 0
        if self.float_range[0] == -1:
            return (self.prices[0] * 0.1) + (self.prices[1] * 0.9)
        else:
            for i in range(-5, 0):
                value += self.prices[i] * self.wear_weight(i + 5)
            if self.rarity != "G":
                for i in range(5):
                    value_st += self.prices[i] * self.wear_weight(i)
                value *= 0.9
                value_st *= 0.1
            return value + value_st

    def calc_probability(self, price: float, info=False) -> float:
        """
        Calculate the probability that any given opening will turn a profit.
        """
        probability = 0
        probability_st = 0
        if self.float_range[0] == -1:
            return (0.1 if self.prices[0] >= price else 0) + (0.9 if self.prices[1] >= price else 0)
        else:
            if info:
                print(f"{self.name}\nNon-ST:")
            for i in range(-5, 0):
                if info:
                    print(f"{self.wear_weight(i + 5):.4f}\t{self.prices[i]}\t{price}")
                probability += self.wear_weight(i + 5) if self.prices[i] >= price else 0
            if not (self.rarity == "G"):
                if info:
                    print("ST:")
                for i in range(5):
                    if info:
                        print(f"{self.wear_weight(i):.4f}\t{self.prices[i]}\t{price}")
                    probability_st += self.wear_weight(i) if self.prices[i] >= price else 0
                probability *= 0.9
                probability_st *= 0.1
            if info:
                print(f"{probability+probability_st}")
            return probability + probability_st

    def wear_weight(self, wear_num: int) -> float:
        """
        Calculate the chance a given wear of this skin will be dropped.
        """
        if self.float_range[0] > Constants.FLOATS[wear_num + 1] or self.float_range[1] < Constants.FLOATS[wear_num]:
            return 0
        else:
            return (min(self.float_range[1], Constants.FLOATS[wear_num + 1]) - max(self.float_range[0], Constants.FLOATS[wear_num])) / self.wearRange

    def __repr__(self):
        return self.name

    def __str__(self):
        return f"{self.name} with a value of {self.value:.2f}"


def get_skin_float_range(skin_page: str) -> tuple[float, float]:
    """
    Gets the range of possible floats for the skin.
    Takes the content of the page, not the URL.
    """
    pass


def get_skin_rarity(skin_page: str) -> str:
    """
    Gets the rarity of the skin.
    Takes the content of the page, not the URL.
    """
    pass


def get_skin_prices(skin_page: str) -> list[int]:
    """
    Returns the price for each wear available on this skin
    """
    # TODO: maybe swap to dict?
    pass

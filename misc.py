def calc_fractions() -> tuple[str]:
    """
    Calculate the string formatted fraction representing the probability of getting dropped each possible rarity.
    Will always return: ('  2/782', '  2/782', '  5/782', ' 25/782', '125/782', '625/782')
    """
    weights = calc_weights()
    total = sum(weights[1:])
    return tuple([f"{w:>3}/{total}" for w in weights])


def calc_probability() -> tuple[float]:
    """
    Calculate the probability of getting dropped each possible rarity.
    Will always return roughly: (0.0026, 0.0026, 0.0064, 0.0320, 0.1598, 0.7992)
    """
    weights = calc_weights()
    total = sum(weights[1:])
    # float(...) not necessary but PyCharm gets mad at me if I don't
    return tuple((float(weight / total) for weight in weights))


def calc_weights() -> tuple[int]:
    """
    Calculate the weighting of each possible rarity.
    Knife and gloves counted separately for organizational purposes, despite having the same value
    Will always return: (2, 2, 5, 25, 125, 625)
    """
    weights = [2, 2, 5]
    # 3 = len(Constants.RARITY) - len(weights)
    for _ in range(3):
        weights.append(weights[-1] * 5)
    # int(...) not necessary but PyCharm gets mad at me if I don't
    return tuple((int(weight) for weight in weights))


def has_incomplete_info(prices: list[list[list[float]]], skins: list[list[str]]) -> list[str]:
    """
    prices: jagged 3d list ordered by [case][skin][wear/st]
    skins: jagged 2d list of skin names ordered by [case][skin]

    Returns list of skins with missing prices.
    """
    incomplete: list[str] = []
    for (i, case) in enumerate(prices):
        for (j, skin) in enumerate(case):
            if any([price in (-1, -2) for price in skin]):
                incomplete.append(skins[i][j])
    return incomplete


def get_name(link: str) -> str:
    """
    Formats the url into a case/skin name.
    """
    return link[-link[::-1].index('/'):].replace("-", " ")

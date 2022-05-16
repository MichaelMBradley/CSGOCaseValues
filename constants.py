from frozendict import frozendict


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


class Constants:
    """
    Class containing all constants. Cannot be instantiated.
    """

    SITE: str = "https://csgostash.com"
    """
    URL of CSGOStash
    """

    CONDITIONS: tuple[str] = (
        "FN",
        "MW",
        "FT",
        "WW",
        "BS",
        "ST-FN",
        "ST-MW",
        "ST-FT",
        "ST-WW",
        "ST-BS"
    )
    """
    Shortened names of the existing conditions.
    """

    FULL_CONDITIONS: tuple[str] = (
                                      "Factory New",
                                      "Minimal Wear",
                                      "Field Tested",
                                      "Well Worn",
                                      "Battle Scarred",
                                      "StatTrak Factory New",
                                      "StatTrak Minimal Wear",
                                      "StatTrak Field Tested",
                                      "StatTrak Well Worn",
                                      "StatTrak Battle Scarred"
                                  ),
    """
    Full names of the existing conditions.
    """

    RARITY: tuple[str] = (
        "K",
        "G",
        "C",
        "Cl",
        "R",
        "MS"
    )
    """
    Shortened names of the existing rarities.
    """

    FULL_RARITY: tuple[str] = (
        "Knife",
        "Gloves",
        "Covert",
        "Classified",
        "Restricted",
        "Mil-Spec"
    )
    """
    Full names of the existing rarities.
    """

    KEY_COST: float = 3.16
    """
    Cost of a key, in CAD.
    """

    WEIGHTS: dict[str: float] = frozendict(
        {
            rarity: probability for (rarity, probability) in zip(RARITY, calc_probability())
        }
    )
    """
    Probability of each rarity being dropped.
    Can be calculated using misc.calc_weights()
    """

    FLOATS: tuple[float] = (
        0,
        0.07,
        0.15,
        0.38,
        0.45,
        1
    )
    """
    Stopping points between skin wears.
    """

    CASE_GROUPS: dict[str: tuple[str]] = frozendict({
        "Chroma": (
            "Chroma Case",
            "Chroma 2 Case",
            "Chroma 3 Case"
        ),
        "Weapon": (
            "CS:GO Weapon Case",
            "CS:GO Weapon Case 2",
            "CS:GO Weapon Case 3"
        ),
        "eSports": (
            "eSports 2013 Case",
            "eSports 2013 Winter Case",
            "eSports 2014 Summer Case"
        ),
        "Gamma": (
            "Gamma Case",
            "Gamma Case 2"
        ),
        "Operation": (
            "Operation Bravo Case",
            "Operation Breakout Weapon Case",
            "Operation Hydra Case",
            "Operation Phoenix Weapon Case",
            "Operation Vanguard Weapon Case",
            "Operation Wildfire Case"
        ),
        "Spectrum": (
            "Spectrum Case",
            "Spectrum 2 Case"
        ),
        "Other": (
            "Clutch Case",
            "Danger Zone Case",
            "Falchion Case",
            "Glove Case",
            "Horizon Case",
            "Huntsman Weapon Case",
            "Revolver Case",
            "Shadow Case",
            "Winter Offensive Weapon Case"
        ),
        "Prime": (
            "Fracture Case",
            "Prisma 2 Case",
            "Prisma Case",
            "Danger Zone Case",
            "Clutch Case"
        ),
        "Non-Prime": (
            "CS20 Case",
            "Horizon Case",
            "Spectrum 2 Case",
            "Gamma 2 Case",
            "Chroma 3 Case",
            "Revolver Case"
        ),
        "Rare": (
            "CS:GO Weapon Case",
            "Operation Bravo Case",
            "CS:GO Weapon Case 2",
            "Winter Offensive Weapon Case",
            "CS:GO Weapon Case 3",
            "Operation Phoenix Weapon Case",
            "Huntsman Weapon Case",
            "Operation Breakout Weapon Case",
            "Operation Vanguard Weapon Case",
            "Chroma Case",
            "Chroma 2 Case",
            "Falchion Case",
            "Shadow Case",
            "Operation Wildfire Case",
            "Gamma Case",
            "Glove Case",
            "Spectrum Case",
            "Operation Hydra Case",
            "Snakebite Case"
        )
    })
    """
    Groupings of cases. Some are arbitrary, but it helps for graphing.
    """

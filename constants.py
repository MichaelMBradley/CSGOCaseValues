from frozendict import frozendict

from misc import calc_probability


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
            "Operation Pheonix Weapon Case",
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
            "Hunstman Weapon Case",
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
            "Operation Pheonix Weapon Case",
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


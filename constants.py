# A set of useful constants

SITE = "https://csgostash.com"
WEBTIME = 0.255  # Estimate
CONDITIONS = ["FN", "MW", "FT", "WW", "BS"]
CONDITIONS = ["ST-" + CONDITION for CONDITION in CONDITIONS] + CONDITIONS
FULLCONDITIONS = ["Factory New", "Minimal Wear", "Field Tested", "Well Worn", "Battle Scarred"]
FULLCONDITIONS = ["StatTrak " + CONDITION for CONDITION in FULLCONDITIONS] + FULLCONDITIONS
RARITY = ["K", "G", "C", "Cl", "R", "MS"]
FULLRARITY = ["Knife", "Gloves", "Covert", "Classified", "Restricted", "Mil-Spec"]
KEYCOST = 3.16
WEIGHTS = {"K": 1 / 391, "G": 1 / 391, "C": 5 / 782, "Cl": 25 / 782, "R": 125 / 782, "MS": 625 / 782}
FLOATS = (0, 0.07, 0.15, 0.38, 0.45, 1)
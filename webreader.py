from re import finditer
from urllib.request import Request, urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup

from case import Case
from constants import Constants
from skin import Skin
from status import *


def get_cases() -> list[Case]:
    """
    Returns the cases in the game right now.
    """
    return [*map(Case, get_case_urls())]


def get_case_urls() -> list[str]:
    """
    Returns a list of links to the pages of cases on CSGOStash.
    """
    # [*{...}] <- Take the list of links, put it into a set (remove duplicates), and then turn it back into a list
    return [*{link.group() for link in finditer(fr"({Constants.SITE}/case/\d+/[\w\-:&;]+)", read_page(Constants.SITE))}]


def get_name_from_url(url: str) -> str:
    """
    Formats the url into a case/skin name.
    """
    return url[-url[::-1].index('/'):].replace("-", " ")


def get_skins(case_page: str) -> list[Skin]:
    """
    Returns the skins associated with a given case.
    """
    pass


def read_page(url: str, status_bar: StatusBar | None = None) -> str:
    """
    Returns a string containing the contents of the page specified by the url.
    """
    # TODO: There's gotta be a better way
    for i in range(5):
        try:
            return urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=5).read().decode("utf-8")
        except URLError:
            if status_bar:
                status_bar.warn(f"!Retrying page! ({i})")
    exit("Could not download webpage")


def get_skin_links(case_links: list[str]) -> tuple[list[list[int]], list[float]]:
    skins = []
    case_cost = []
    progress = StatusBar(len(case_links), "Finding skins")
    t = Timer(["Retrieving webpage", "Analyzing data"])

    for link in case_links:
        t.swap_to(0)
        case_file = read_page(link, progress)  # Reads case page
        t.swap_to(1)
        skins.append([links.start() for links in finditer(Constants.SITE + "/skin/", case_file)])  # Retrieve positions of links to skins
        price_start = case_file.find("CDN$ ") + 5
        case_cost.append(float(case_file[price_start: min(case_file.find(" ", price_start), case_file.find("\n", price_start))]))

        for i in range(len(skins[-1])):
            skins[-1][i] = case_file[skins[-1][i] : case_file.find('"', skins[-1][i])]  # Formats skin links
            # String case file indexes [start index: first " after start index]
        if not case_file.find("?Knives=1") == -1:
            special = "Knives"
            iden = "/skin/"
        else:
            special = "Gloves"
            iden = "/glove/"

        t.swap_to(0)
        knife_file = read_page(f"{link}?{special}=1", progress)
        t.swap_to(1)

        knife_page_links = [link.start() for link in finditer(link + "?" + special + "=1&page=", knife_file)]  # Retrieves positions of links to other special pages, original page
        knife_page_links.insert(0, knife_file)

        for i in range(len(knife_page_links)):
            if i != 0:
                t.swap_to(0)
                knife_page_links[i] = read_page(knife_file[knife_page_links[i]: knife_file.find("&", knife_page_links[i]) + 7], progress)  # If not last index (already file), open webpage with formatted link
                t.swap_to(1)
            knives = [link.start() for link in finditer(Constants.SITE + iden, knife_page_links[i])]  # Retrieves positions of links to knives
            for j in range(len(knives)):
                knives[j] = knife_page_links[i][knives[j]: knife_page_links[i].find('"', knives[j])]  # Formats knife links
            skins[-1] += knives  # Combines knife list with skin list

        k = 0
        while k < len(skins[-1]):  # Must iterate with while loop to avoid skipping elements
            if skins[-1][k] in skins[-1][k + 1:]:  # Pops invalid elements
                skins[-1].pop(k)
            else:
                k += 1  # If current index is valid check next index
        progress.increment_and_print()
    t.results()

    return skins, case_cost


def get_prices(skin_links: list[list[str]]) -> tuple[list[list[list[float]]], list[list[list[float | str]]]]:
    prices: list[list[list[float]]] = []
    skin_info = []
    cache = {}
    progress = StatusBar(sum([len(l) for l in skin_links]), "Getting prices")
    t = Timer(["Retrieving webpage", "Analyzing data"])

    for box in skin_links:
        case = []
        case_info = []
        for skin in box:
            (wear, wear_info) = cache.get(skin, (None, None))
            if (wear, wear_info) == (None, None):
                t.swap_to(0)
                load_page = read_page(skin, progress)  # Reads page
                t.swap_to(1)

                if not load_page.find("★") == -1:  # Determines if skin is a knife or glove
                    res = 2
                elif (not load_page.find("Gloves |") == -1) or (not load_page.find("Wraps |") == -1):
                    res = 5
                else:
                    res = 10

                page = BeautifulSoup(load_page, "html.parser")
                wear = [p.get_text() for p in page.findAll("span", class_="pull-right")][:res]  # Gets the first (res) wear prices
                wear_info: list[float | str] = [float(p.get_text()) for p in page.findAll("div", class_="marker-value cursor-default")]  # Finds max and min wear
                if not wear_info:
                    wear_info = [-1, -1]  # If skin is vanilla

                for i in range(len(wear)):
                    if wear[i].find(".") != -1:  # If wear is a number
                        num = wear[i][wear[i].find(" ") + 1 :]
                        if num.find(",") != -1:  # Deals with thousands
                            num = num[: num.find(",")] + num[num.find(",") + 1 :]
                        wear[i] = float(num)
                    elif wear[i].find("Possible") != -1:  # If wear is impossible
                        wear[i] = -2
                    else:  # If no price available
                        wear[i] = -1

                quals = [i.get_text() for i in page.findAll("p", class_="nomargin")][0]
                quality = ""
                for r in range(len(Constants.RARITY)):
                    if quals.find(Constants.FULL_RARITY[r]) != -1:  # Finds quality of skin
                        quality = Constants.RARITY[r]
                        break
                if quality == "" and quals.find("Contraband"):  # Makes the Howl a Covert skin to simplify calculations
                    quality = "C"
                elif quality == "":  # If hand wraps, assign glove quality
                    quality = "G"
                wear_info.append(quality)
                cache[skin] = (wear, wear_info)
            case.append(wear)
            case_info.append(wear_info)
            progress.increment_and_print()
        prices.append(case)
        skin_info.append(case_info)
    t.stop()
    t.results()

    return prices, skin_info

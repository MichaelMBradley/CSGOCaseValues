import glob
import matplotlib.pyplot as plt
import os
from value import *
from status import *
from constants import Constants


def dropped(cases):
    def print_case(case): print(f"{case.name:>35}:\t{case.EV_D:.4f}\t{case.EV:.4f}\t{case.prob_drop:.4f}")
    p = []
    np = []
    r = []
    for case in cases:
        if case.name in Constants.CASE_GROUPS["Prime"]:
            p.append(case)
        if case.name in Constants.CASE_GROUPS["Non-Prime"]:
            np.append(case)
        if case.name in Constants.CASE_GROUPS["Rare"]:
            r.append(case)
    print(f"{'':>35} \t(Drop) (Bought)\t(Probability of getting an item worth more than a key)")
    print("Prime drops expected value:")
    for case in p:
        print_case(case)
    print("Non-Prime drops expected value:")
    for case in np:
        print_case(case)
    print("Rare drops expected value:")
    for case in r:
        print_case(case)


def groups(datecases, allowed):
    """
    Groups:

    Chroma
    Weapon
    eSports
    Gamma
    Operation
    Spectrum
    Other
    All

    Prime
    Non-Prime
    Rare
    Drops
    """
    if "All" in allowed:
        return datecases
    if allowed == ["Drops"]:
        allowed = ["Prime", "Non-Prime", "Rare"]
    for date in datecases:
        cases = date[1]
        new_cases = []
        for case in cases:
            for g in allowed:
                if case.name in Constants.CASE_GROUPS[g]:
                    new_cases.append(case)
                    break
        date[1] = new_cases
    return datecases


def plot_cases(date_cases, value=lambda case: case.EV, legend=False, colour=True, area=(0, 1), about="Expected Value"):
    # ---ANALYSIS---
    if area is not None:
        text_size = 0.012 * (area[1] - area[0])
    else:
        text_size = 0.012
    dates = []
    cases = {}
    for comb in date_cases:
        dates.append(comb[0])
        sort = sort_cases(comb[1], value=value)
        for case in sort:
            ev = value(case)
            if case.name in cases.keys():
                cases[case.name].append(ev)
            else:
                cases[case.name] = [ev]
    # ---SPACING---
    names = []
    for case_name in cases.keys():
        names.append([case_name, cases[case_name][-1] - (text_size / 2)])
    names.sort(key=lambda t: t[1], reverse=True)
    names_l = names[::2]
    names_r = names[1::2]
    spread(names_l, text_size)
    spread(names_r, text_size)
    if legend:
        plt.subplot(1, 2, 1)
    for case_name in cases.keys():
        plt.plot(dates[-len(cases[case_name]):], cases[case_name], label=case_name)
    if legend:
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)  # Useless, too many colours
    colours = [line.get_color() if colour else "000000" for line in plt.gca().lines]
    start = [case.name for case in sort_cases(date_cases[0][1], value=value)]
    end = [case.name for case in sort_cases(date_cases[-1][1], value=value)]
    for case in end:
        if case not in start:
            start.append(case)
    fixed = [""] * len(colours)
    for i in range(len(colours)):
        fixed[end.index(start[i])] = colours[i]
    # ---PLOTTING---
    if not legend:
        for (i, t) in zip(range(len(names_l)), names_l):
            ind = t[0].index(" Case")
            t[0] = t[0][:ind] + t[0][ind + 5 :]
            plt.text(dates[-1], t[1], t[0], horizontalalignment="left", color=fixed[i * 2])
        for (i, t) in zip(range(len(names_r)), names_r):
            ind = t[0].index(" Case")
            t[0] = t[0][:ind] + t[0][ind + 5 :]
            on_left = any([abs(t[1] - n[1]) <= text_size for n in names_l])
            plt.text(dates[-1], t[1], t[0], horizontalalignment="right" if on_left else "left", color="000000" if on_left else fixed[i * 2 + 1])
    plt.title("CSGO Case Unboxing")
    plt.xlabel("Date")
    plt.ylabel(about)
    if area is not None:
        plt.ylim(area)
    plt.grid(axis="y")
    ax = plt.gca()
    ax.set_xticklabels(dates, rotation=90)
    plt.show()


def plot_relative_prices(prices, skinfo, skins):
    # Plots the relative prices of different wear values, seperated by rarity
    rel = info(prices, skinfo, skins)
    plt.plot([0])
    for i in range(len(rel)):
        ax = plt.subplot(3, 2, i + 1, ylabel=Constants.FULL_RARITY[i])  # New subplot for each rarity level
        ax.plot(Constants.CONDITIONS[5:][::-1], rel[i][:5], label="Normal")

        for x, y in zip(Constants.CONDITIONS[5:][::-1], rel[i][:5]):  # Plots normal prices
            ax.annotate(str(y), xy=(x, y))  # Prints relative price for each data point

        if i != 1:
            ax.plot(Constants.CONDITIONS[5:][::-1], rel[i][5:], label="StatTrak")
            for x, y in zip(Constants.CONDITIONS[5:][::-1], rel[i][5:]):  # Plots StatTrak prices
                ax.annotate(str(y), xy=(x, y))
        plt.subplot(ax)

    plt.legend()
    plt.tight_layout()
    plt.figure(figsize=(20, 20), clear=True)
    plt.xticks(rotation=90)
    plt.show()


def print_historical_data(value=lambda case: case.EV, most_recent=False):
    if most_recent:
        case_list = [["Most recent", recent_cases()]]
    else:
        case_list = read_historical_data()
    for [date, cases] in case_list:
        print(f"\n{date}")
        print_sorted_case_list(cases, value)


def print_sorted_case_list(case_list, value=lambda case: case.EV):
    cases = sort_cases(case_list)
    print(f"EV\t(Value\tPrice)\tName")
    for c in cases:
        print(f"{value(c):.4f}\t({c.value:>5.2f}\t{c.total_price:>5.2f})\t{c.name}")


def read_historical_data():
    case_list = []
    files = glob.glob(os.path.dirname(__file__) + "\\data\\*")
    progress = StatusBar(len(files), "Reading and analyzing files")
    timing = Timer(["Reading JSON", "Filling data", "Analyzing"])
    for fname in files:
        case_list.append([fname.split("\\")[-1], analysis(fname, timing)])
        progress.increment_and_print()
    timing.results()
    return case_list


def recent_cases():
    return analysis(glob.glob(os.path.dirname(__file__) + "\\data\\*")[-1])


def sort_cases(case_list, value=lambda case: case.EV, descending=True):
    cases = case_list.copy()
    cases.sort(key=value, reverse=descending)
    return cases


def spread(names, text_size):
    settled = False
    while not settled:
        settled = True
        for i in range(len(names) - 1):
            diff = abs(names[i][1] - names[i + 1][1])
            if diff < text_size:
                settled = False
                move = (text_size - diff) / 2 + 0.001
                names[i][1] += move
                for j in range(i - 1, -1, -1):
                    if names[j][1] < names[j + 1][1]:
                        names[j][1] += move
                    else:
                        break
                names[i + 1][1] -= move
                for j in range(i + 1, len(names)):
                    if names[j][1] > names[j - 1][1]:
                        names[j][1] += move
                    else:
                        break


def weekly(cases: list[Case]) -> list[Case]:
    return cases[(len(cases) - 1) % 7::7]

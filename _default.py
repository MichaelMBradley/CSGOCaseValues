from filemanager import *
from vis import *


def main():
    saveinfo()
    plot_cases(read_historical_data())
    dropped(recent_cases())


if __name__ == "__main__":
    main()

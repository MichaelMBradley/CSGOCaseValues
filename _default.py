from filemanager import *
from vis import *


def main():
    saveinfo()
    plotcases(readhistoricaldata())
    dropped(recentcases())


if __name__ == "__main__":
    main()

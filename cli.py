from argparse import ArgumentParser
import logging

from filemanager import saveinfo
from vis import dropped, plot_cases, read_historical_data, recent_cases


def handle_cli() -> None:
    parser = ArgumentParser()
    parser.parse_args()


def download_display_print() -> None:
    """
    Download current data, then graph and print it.
    """
    logging.info("Downloading information")
    saveinfo()
    logging.info("Information downloaded")
    plot_cases(read_historical_data())
    dropped(recent_cases())


if __name__ == "__main__":
    handle_cli()

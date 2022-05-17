from argparse import ArgumentParser
import logging
from sys import argv

from filemanager import save_info
from vis import dropped, plot_cases, read_historical_data, recent_cases


def handle_cli() -> None:
    parser = ArgumentParser()

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="download latest information"
    )

    arguments = parser.parse_args(argv[1:])

    if arguments.download:
        logging.info("Downloading information")
        # save_info()


def download_display_print() -> None:
    """
    Download current data, then graph and print it.
    """
    logging.info("Downloading information")
    save_info()
    logging.info("Information downloaded")
    plot_cases(read_historical_data())
    dropped(recent_cases())


if __name__ == "__main__":
    handle_cli()

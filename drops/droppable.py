from abc import ABC
import logging


def get_name_from_url(url: str) -> str:
    """
    Formats the url into a case/skin name.
    """
    return url[-url[::-1].index('/'):].replace("-", " ")


class Droppable(ABC):
    def __init__(self, url: str, delay_init: bool):
        self.url: str = url
        self.name: str = get_name_from_url(url)

        logging.info(f"Initializing logging, {delay_init=}")

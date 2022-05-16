from abc import ABC


def get_name_from_url(url: str) -> str:
    """
    Formats the url into a case/skin name.
    """
    return url[-url[::-1].index('/'):].replace("-", " ")


class Droppable(ABC):
    pass

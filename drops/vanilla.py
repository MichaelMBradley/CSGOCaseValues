from drops.base_skin import Skin


class Vanilla(Skin):
    def __init__(self, url: str, delay_init: bool):
        super().__init__(url, delay_init)

        if delay_init:
            return

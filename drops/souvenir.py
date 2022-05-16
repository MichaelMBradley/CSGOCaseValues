from base_skin import Skin


class Souvenir(Skin):
    def __init__(self, url: str, delay_init: bool):
        super().__init__(url, delay_init)

        if delay_init:
            return

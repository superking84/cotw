from game_objects.item import Item


class Equipment(Item):
    """
    Any item that the player may wear. Optionally alters the player's stats.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        super().__init__(img_src, center_x, center_y)

        self.wear_location = None

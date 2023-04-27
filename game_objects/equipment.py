from typing import List

from game_objects.item import Item
from utils.enums import WearLocation


class Equipment(Item):
    """
    Any item that the player may wear. Optionally alters the player's stats.
    """

    def __init__(self, name: str, img_src: str, center_x: int, center_y: int, wear_locations: List[WearLocation]):
        super().__init__(name, img_src, center_x, center_y)

        if wear_locations is not None:
            self.valid_wear_locations = wear_locations

from typing import List

from game_objects.item import Item
from utils.enums import WearLocation


class Container(Item):
    """
    Items such as backpacks and chests that may contain other items.
    May or may not be wearable.
    """

    def __init__(self, name: str, img_src: str, center_x: int, center_y: int, wear_locations: List[WearLocation]):
        super().__init__(name, img_src, center_x, center_y)

        self.size_capacity = 0
        if wear_locations is not None:
            self.valid_wear_locations = wear_locations

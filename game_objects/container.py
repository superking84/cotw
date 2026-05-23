from typing import List

from game_objects.item import Item
from utils.enums import WearLocation


class Container(Item):
    def __init__(self, name: str, img_src: str, wear_locations: List[WearLocation]):
        super().__init__(name, img_src)

        self.contents: List[Item] = []
        self.size_capacity = 0
        if wear_locations is not None:
            self.valid_wear_locations = wear_locations

    def add_item(self, item: Item):
        self.contents.append(item)

    def remove_item(self, item: Item):
        self.contents.remove(item)

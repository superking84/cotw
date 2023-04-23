import arcade

import constants
from game_objects.wear_location import WearLocation


class Item(arcade.Sprite):
    """
    Any in-game object that the player may carry and interact with in some way.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        super().__init__(img_src, constants.CHARACTER_SCALING, center_x=center_x, center_y=center_y)
        self.weight = 0
        self.size = 0

        self.wearable_locations = []


class Equipment(Item):
    """
    Any item that the player may wear. Optionally alters the player's stats.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        super().__init__(img_src, center_x=center_x, center_y=center_y)

        self.wear_location = None


class Consumable(Item):
    """
    Items such as potions, scrolls and wands that can be used one or
    more times.  May either disappear or convert into a "dead"
    version of the item upon depletion.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        super().__init__(img_src, center_x=center_x, center_y=center_y)

        self.num_uses = 0
        self.wearable_locations = [WearLocation.RIGHT_HAND, WearLocation.LEFT_HAND]


class Container(Item):
    """
    Items such as backpacks and chests that may contain other items.
    May or may not be wearable.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        super().__init__(img_src, center_x=center_x, center_y=center_y)

        self.size_capacity = 0

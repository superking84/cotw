import arcade

import constants
from ui.draggable_tile import DraggableTile


class Item:
    """
    Any in-game object that the player may carry and interact with in some way.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        self.sprite = arcade.Sprite(img_src, constants.CHARACTER_SCALING, center_x=center_x, center_y=center_y)
        self.inventory_tile = DraggableTile(self.sprite)

        self.weight = 0
        self.size = 0

        self.wearable_locations = []

from typing import List

import arcade

import constants
from utils.enums import WearLocation


class Item:
    """
    Any in-game object that the player may carry and interact with in some way.
    """

    def __init__(self, name: str, img_src: str):
        self.sprite = arcade.Sprite(img_src, constants.CHARACTER_SCALING)

        self.name = name
        self.weight = 0
        self.size = 0

        self.valid_wear_locations: List[WearLocation] = [WearLocation.LEFT_HAND, WearLocation.RIGHT_HAND]

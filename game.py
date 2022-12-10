import arcade

import constants
from views.inventory_view import InventoryView
from views.world_view import WorldView


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
        self.views = {"world": WorldView(), "inventory": InventoryView()}
        for _, view in self.views.items():
            view.setup()

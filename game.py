import arcade

import constants
from game_objects.player import Player
from views.inventory_view import InventoryView
from views.world_view import WorldView


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        image_source = "./resources/images/femaleAdventurer_idle.png"
        self.player = Player(image_source, constants.PLAYER_START_X, constants.PLAYER_START_Y)
        self.player.setup(
            strength=10,
            dexterity=10,
            intelligence=10,
            constitution=10,
            health=50,
            mana=25
        )

        self.views = {"world": WorldView(self.player), "inventory": InventoryView(self.player)}
        for view in self.views.values():
            view.setup()

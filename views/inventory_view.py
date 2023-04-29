from typing import Dict

import arcade
from arcade.gui import UILabel

import constants
from game_objects.player import Player
from ui.inventory_slot_widget import InventorySlotWidget
from ui.inventory_ui_manager import InventoryUIManager
from utils.enums import WearLocation

coin_img_src = "resources/images/coinGold.png"

INVENTORY_SLOT_BORDER = 2
INVENTORY_SLOT_HEIGHT = (constants.SCREEN_HEIGHT / 6) - (INVENTORY_SLOT_BORDER * 2)
INVENTORY_SLOT_WIDTH = (INVENTORY_SLOT_HEIGHT * (4 / 5.0)) - (INVENTORY_SLOT_BORDER * 2)

inventory_slot_data = [
    {"wear_location": WearLocation.ARMOR, "name": "Armor", "row": 5, "column": 0},
    {"wear_location": WearLocation.NECKWEAR, "name": "Neckwear", "row": 5, "column": 1},
    {"wear_location": WearLocation.CLOAK, "name": "Overgarment", "row": 5, "column": 2},
    {"wear_location": WearLocation.HELMET, "name": "Helmet", "row": 5, "column": 3},
    {"wear_location": WearLocation.SHIELD, "name": "Shield", "row": 5, "column": 4},
    {"wear_location": WearLocation.BRACERS, "name": "Bracers", "row": 4, "column": 0},
    {"wear_location": WearLocation.GAUNTLETS, "name": "Gauntlets", "row": 4, "column": 4},
    {"wear_location": WearLocation.RIGHT_HAND, "name": "right hand", "row": 3, "column": 0},
    {"wear_location": WearLocation.LEFT_HAND, "name": "left hand", "row": 3, "column": 4},
    {"wear_location": WearLocation.RIGHT_RING, "name": "Right Ring", "row": 2, "column": 0},
    {"wear_location": WearLocation.LEFT_RING, "name": "Left Ring", "row": 2, "column": 4},
    {"wear_location": WearLocation.BELT, "name": "Belt", "row": 1, "column": 0},
    {"wear_location": WearLocation.BOOTS, "name": "Boots", "row": 1, "column": 4},
    {"wear_location": WearLocation.BACKPACK, "name": "Backpack", "row": 0, "column": 0},
    {"wear_location": WearLocation.PURSE, "name": "Purse", "row": 0, "column": 4}
]


class InventoryView(arcade.View):
    def __init__(self, player: Player):
        super().__init__()

        self.player = player
        self.manager = InventoryUIManager(player)

        self.inventory: Dict[str, InventorySlotWidget] = {}

        for slot_data in inventory_slot_data:
            x = slot_data["column"] * INVENTORY_SLOT_WIDTH
            y = slot_data["row"] * INVENTORY_SLOT_HEIGHT
            widget = InventorySlotWidget(x, y, INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT,
                                         slot_data["wear_location"])
            label = UILabel(x, y, INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT, text=slot_data["name"], font_size=10,
                            text_color=arcade.color.BLACK, align='center')

            widget.add(label)
            self.manager.add(widget)

            self.inventory[slot_data["name"]] = widget

    def setup(self):
        for (wear_location, item) in self.player.inventory.items():
            print(wear_location)
            if item is not None:
                print(item.name)
            else:
                print("None")

        # slot1 = self.inventory["left hand"]
        # test_item1 = Item(coin_img_src, slot1.center_x, slot1.center_y)
        # slot1.item = test_item1
        # test_item1.sprite.center_x = slot1.center_x
        # test_item1.sprite.center_y = slot1.center_y
        # self.manager.add(test_item1.inventory_tile)
        #
        # slot2 = self.inventory["Belt"]
        # test_item2 = Item(coin_img_src, slot2.center_x, slot2.center_y)
        # slot2.item = test_item1
        # test_item2.sprite.center_x = slot2.center_x
        # test_item2.sprite.center_y = slot2.center_y
        # self.manager.add(test_item2.inventory_tile)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, key: int, modifiers: int):
        match key:
            case arcade.key.ESCAPE:
                self.window.show_view(self.window.views["world"])

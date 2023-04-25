from typing import Dict

import arcade
from arcade.gui import UILabel

import constants
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
    def __init__(self):
        super().__init__()

        self.manager = InventoryUIManager()
        self.inventory: Dict[str, InventorySlotWidget] = {}

        for slot_data in inventory_slot_data:
            x = slot_data["column"] * INVENTORY_SLOT_WIDTH
            y = slot_data["row"] * INVENTORY_SLOT_HEIGHT
            slot = InventorySlotWidget(x, y, INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT,
                                       slot_data["name"])  # .with_border()
            label = UILabel(x, y, INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT, text=slot_data["name"], font_size=10,
                            text_color=arcade.color.BLACK, align='center')

            slot.add(label)
            self.manager.add(slot)

            self.inventory[slot_data["name"]] = slot

    def setup(self):
        slot = self.inventory["Free Hand"]
        test_item = Item(coin_img_src, slot.center_x, slot.center_y)
        slot.item = test_item
        test_item.sprite.center_x = slot.center_x
        test_item.sprite.center_y = slot.center_y
        self.manager.add(test_item.inventory_tile)

        pass

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

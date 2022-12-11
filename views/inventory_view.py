import arcade
from arcade.gui import UILabel

import constants
from ui.inventory_slot_widget import InventorySlotWidget
from ui.inventory_ui_manager import InventoryUIManager

enemy_img_src = "resources/images/zombie_idle.png"

INVENTORY_SLOT_BORDER = 2
INVENTORY_SLOT_HEIGHT = (constants.SCREEN_HEIGHT / 6) - (INVENTORY_SLOT_BORDER * 2)
INVENTORY_SLOT_WIDTH = (INVENTORY_SLOT_HEIGHT * (4 / 5.0)) - (INVENTORY_SLOT_BORDER * 2)

inventory_slot_data = [
    {"name": "Armor", "row": 5, "column": 0},
    {"name": "Neckwear", "row": 5, "column": 1},
    {"name": "Overgarment", "row": 5, "column": 2},
    {"name": "Helmet", "row": 5, "column": 3},
    {"name": "Shield", "row": 5, "column": 4},
    {"name": "Bracers", "row": 4, "column": 0},
    {"name": "Gauntlets", "row": 4, "column": 4},
    {"name": "Weapon Hand", "row": 3, "column": 0},
    {"name": "Free Hand", "row": 3, "column": 4},
    {"name": "Right Ring", "row": 2, "column": 0},
    {"name": "Left Ring", "row": 2, "column": 4},
    {"name": "Belt", "row": 1, "column": 0},
    {"name": "Boots", "row": 1, "column": 4},
    {"name": "Backpack", "row": 0, "column": 0},
    {"name": "Purse", "row": 0, "column": 4}
]


class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = InventoryUIManager()

        for slot_data in inventory_slot_data:
            x = slot_data["column"] * INVENTORY_SLOT_WIDTH
            y = slot_data["row"] * INVENTORY_SLOT_HEIGHT
            slot = InventorySlotWidget(x, y, INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT,
                                       slot_data["name"])  # .with_border()
            label = UILabel(x, y, INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT, text=slot_data["name"], font_size=10,
                            text_color=arcade.color.BLACK, align='center')

            slot.add(label)
            self.manager.add(slot)

    def setup(self):
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

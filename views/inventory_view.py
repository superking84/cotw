from typing import Dict

import arcade
from arcade.gui import UILabel

import constants
from game_objects.player import Player
from ui.inventory_slot_widget import InventorySlotWidget
from ui.inventory_ui_manager import InventoryUIManager
from ui.inventory_view_tile import InventoryViewTile
from utils.enums import WearLocation

coin_img_src = "resources/images/coinGold.png"

inventory_slot_data = [
    {"wear_location": WearLocation.ARMOR, "name": "Armor", "row": 5, "column": 0},
    {"wear_location": WearLocation.NECKWEAR, "name": "Neckwear", "row": 5, "column": 1},
    {"wear_location": WearLocation.CLOAK, "name": "Overgarment", "row": 5, "column": 2},
    {"wear_location": WearLocation.HELMET, "name": "Helmet", "row": 5, "column": 3},
    {"wear_location": WearLocation.SHIELD, "name": "Shield", "row": 5, "column": 4},
    {"wear_location": WearLocation.BRACERS, "name": "Bracers", "row": 4, "column": 0},
    {"wear_location": WearLocation.GAUNTLETS, "name": "Gauntlets", "row": 4, "column": 4},
    {"wear_location": WearLocation.RIGHT_HAND, "name": "R Hand", "row": 3, "column": 0},
    {"wear_location": WearLocation.LEFT_HAND, "name": "L Hand", "row": 3, "column": 4},
    {"wear_location": WearLocation.RIGHT_RING, "name": "R Ring", "row": 2, "column": 0},
    {"wear_location": WearLocation.LEFT_RING, "name": "L Ring", "row": 2, "column": 4},
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

        self.inventory: Dict[WearLocation, InventorySlotWidget] = {}

        for slot_data in inventory_slot_data:
            x = slot_data["column"] * constants.INVENTORY_SLOT_WIDTH
            y = slot_data["row"] * constants.INVENTORY_SLOT_HEIGHT
            widget = InventorySlotWidget(x, y, constants.INVENTORY_SLOT_WIDTH, constants.INVENTORY_SLOT_HEIGHT,
                                         slot_data["wear_location"])
            label = UILabel(x, y, constants.INVENTORY_SLOT_WIDTH, constants.INVENTORY_SLOT_HEIGHT, text=slot_data["name"], font_size=10,
                            text_color=arcade.color.BLACK, align='center')

            widget.add(label)
            self.manager.add(widget)

            self.inventory[slot_data["wear_location"]] = widget
            item = self.player.inventory[slot_data["wear_location"]]
            if item is not None:
                item.sprite.center_x = widget.center_x
                item.sprite.center_y = widget.center_y
                tile = InventoryViewTile(item)
                widget.item_tile = tile

                self.manager.add(widget.item_tile)

    def setup(self):
        pass

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        if self.manager.open_container is not None:
            arcade.draw_lrtb_rectangle_outline(
                constants.CONTAINER_PANEL_X,
                constants.CONTAINER_PANEL_X + constants.CONTAINER_PANEL_WIDTH,
                constants.CONTAINER_PANEL_Y + constants.CONTAINER_PANEL_HEIGHT,
                constants.CONTAINER_PANEL_Y,
                color=arcade.color.WHITE,
                border_width=constants.CONTAINER_PANEL_BORDER
            )

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, key: int, modifiers: int):
        match key:
            case arcade.key.ESCAPE:
                self.window.show_view(self.window.views["world"])

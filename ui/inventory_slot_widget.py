from typing import Optional

from arcade.gui import UIWidget

from game_objects.item import Item


class InventorySlotWidget(UIWidget):
    def __init__(self, x: float, y: float, width: float, height: float, name: str):
        super().__init__(x, y, width, height)

        self.name = name
        self.item: Optional[Item] = None  # the item being held in the inventory slot

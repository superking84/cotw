from typing import Optional

from arcade.gui import UIWidget

from game_objects.item import Item
from utils.enums import WearLocation


class InventorySlotWidget(UIWidget):
    def __init__(self, x: float, y: float, width: float, height: float, wear_location: WearLocation):
        super().__init__(x, y, width, height)

        self.wear_location: WearLocation = wear_location
        self.item: Optional[Item] = None  # the item being held in the inventory slot

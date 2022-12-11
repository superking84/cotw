from arcade.gui import UIWidget


class InventorySlotWidget(UIWidget):
    def __init__(self, x: float, y: float, width: float, height: float, name: str):
        super().__init__(x, y, width, height)

        self.name = name
        self.item = None  # the item being held in the inventory slot

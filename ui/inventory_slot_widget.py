from arcade.gui import UIWidget


class InventorySlotWidget(UIWidget):
    def __init__(self, x: float, y: float, width: float, height: float):
        super().__init__(x, y, width, height)

        self.item = None  # the item being held in the inventory slot

from arcade.gui import UISpriteWidget

from game_objects.item import Item
from ui.mixins import UIWindowLikeMixin


class InventoryViewTile(UISpriteWidget, UIWindowLikeMixin):
    def __init__(self, item: Item):
        self.item = item
        sprite = item.sprite

        super().__init__(x=sprite.left, y=sprite.bottom, width=sprite.width, height=sprite.height, sprite=sprite)

        self.total_dx = 0
        self.total_dy = 0

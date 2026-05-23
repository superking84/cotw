from arcade.gui import UISpriteWidget, UIWidget
from arcade.sprite import Sprite

from game_objects.item import Item
from ui.mixins import UIDraggableMixin


class InventoryViewTile(UISpriteWidget, UIDraggableMixin, UIWidget):
    def __init__(self, item: Item):
        self.item = item
        sprite = item.sprite

        super().__init__(x=sprite.left, y=sprite.bottom, width=sprite.width, height=sprite.height, sprite=sprite)

        self.total_dx = 0
        self.total_dy = 0


class GhostTile(UISpriteWidget, UIWidget):
    def __init__(self, item: Item, x: float, y: float, width: float, height: float, alpha: int = 128):
        ghost_sprite = Sprite()
        ghost_sprite.texture = item.sprite.texture
        ghost_sprite.alpha = alpha
        super().__init__(x=x, y=y, width=width, height=height, sprite=ghost_sprite)

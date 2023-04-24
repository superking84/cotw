from arcade.gui import UISpriteWidget
from arcade.sprite import Sprite

from ui.mixins import UIWindowLikeMixin


class DraggableTile(UISpriteWidget, UIWindowLikeMixin):
    def __init__(self, sprite: Sprite):
        super().__init__(x=sprite.left, y=sprite.bottom, width=sprite.width, height=sprite.height, sprite=sprite)

        # self.is_dragging = False
        self.total_dx = 0
        self.total_dy = 0
        self.home_x = sprite.center_x
        self.home_y = sprite.center_y

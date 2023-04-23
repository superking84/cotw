from arcade.gui import UISpriteWidget, UIWindowLikeMixin
from arcade.sprite import Sprite


class DraggableTile(UISpriteWidget, UIWindowLikeMixin):
    def __init__(self, sprite: Sprite):
        super().__init__(x=sprite.left, y=sprite.bottom, width=sprite.width, height=sprite.height, sprite=sprite)

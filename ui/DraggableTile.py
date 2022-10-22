from typing import Optional

from arcade.gui import UIDraggableMixin, UISpriteWidget
from arcade.sprite import Sprite


class DraggableTile(UISpriteWidget, UIDraggableMixin):
    def __init__(self, x: float = 0, y: float = 0, width: float = 100, height: float = 50,
                 sprite: Optional[Sprite] = None, size_hint=None, size_hint_min=None, size_hint_max=None, style=None):
        super(DraggableTile, self).__init__(x=x, y=y, width=width, height=height, sprite=sprite, size_hint=size_hint,
                                            size_hint_min=size_hint_min, size_hint_max=size_hint_max, style=style)

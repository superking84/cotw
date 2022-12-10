from typing import Optional

from arcade.gui import UISpriteWidget, UIWindowLikeMixin, UIMousePressEvent
from arcade.sprite import Sprite


class DraggableTile(UISpriteWidget, UIWindowLikeMixin):
    def __init__(self, x: float = 0, y: float = 0, width: float = 48, height: float = 80,
                 sprite: Optional[Sprite] = None, size_hint=None, size_hint_min=None, size_hint_max=None, style=None):
        super(DraggableTile, self).__init__(x=x, y=y, width=width, height=height, sprite=sprite, size_hint=size_hint,
                                            size_hint_min=size_hint_min, size_hint_max=size_hint_max, style=style)

        self.center_on_screen()

    # TODO: Implement custom handlers for DraggableTile
    def on_event(self, event) -> Optional[bool]:
        if isinstance(event, UIMousePressEvent):
            print(event.button)

        return super().on_event(event)

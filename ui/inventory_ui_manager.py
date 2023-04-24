import arcade.gui

from ui.draggable_tile import DraggableTile
from ui.inventory_slot_widget import InventorySlotWidget


class InventoryUIManager(arcade.gui.UIManager):
    def __init__(self):
        super().__init__()

        self.dragged_tile: DraggableTile = None

    def on_event(self, event) -> bool:
        if isinstance(event, arcade.gui.UIMousePressEvent):
            for widget in self.get_widgets_at(event.pos):
                if isinstance(widget, DraggableTile):
                    self.dragged_tile = widget
                    break

        if isinstance(event, arcade.gui.events.UIMouseDragEvent):
            if self.dragged_tile is not None:
                self.dragged_tile.total_dx += event.dx
                self.dragged_tile.total_dy += event.dy
        if isinstance(event, arcade.gui.UIMouseReleaseEvent):
            if self.dragged_tile is not None:
                if not any([isinstance(widget, InventorySlotWidget) for widget in self.get_widgets_at(event.pos)]):
                    self.dragged_tile.move(-self.dragged_tile.total_dx, -self.dragged_tile.total_dy)
                self.dragged_tile.total_dx = 0
                self.dragged_tile.total_dy = 0
                self.dragged_tile = None

        return super().on_event(event)

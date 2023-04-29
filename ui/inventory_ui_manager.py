from typing import Optional

import arcade.gui

from game_objects.player import Player
from ui.inventory_slot_widget import InventorySlotWidget
from ui.inventory_view_tile import InventoryViewTile


class InventoryUIManager(arcade.gui.UIManager):
    def __init__(self, player: Player):
        super().__init__()

        self.player = player
        self.dragged_tile: Optional[InventoryViewTile] = None

    def on_event(self, event) -> bool:
        if isinstance(event, arcade.gui.UIMousePressEvent):
            for widget in self.get_widgets_at(event.pos):
                if isinstance(widget, InventoryViewTile):
                    self.dragged_tile = widget
                    break

        if isinstance(event, arcade.gui.events.UIMouseDragEvent):
            if self.dragged_tile is not None:
                self.dragged_tile.total_dx += event.dx
                self.dragged_tile.total_dy += event.dy

        if isinstance(event, arcade.gui.UIMouseReleaseEvent):
            return_tile = True
            if self.dragged_tile is not None:
                for widget in self.get_widgets_at(event.pos):
                    if isinstance(widget, InventorySlotWidget):
                        if self.slot_can_receive_item(widget, self.dragged_tile):
                            diff_x = self.dragged_tile.center_x - widget.center_x
                            diff_y = self.dragged_tile.center_y - widget.center_y
                            self.dragged_tile.move(diff_x, diff_y)
                            return_tile = False

                if return_tile:
                    self.dragged_tile.move(-self.dragged_tile.total_dx, -self.dragged_tile.total_dy)

                self.dragged_tile.total_dx = 0
                self.dragged_tile.total_dy = 0
                self.dragged_tile = None

        return super().on_event(event)

    def slot_can_receive_item(self, slot: InventorySlotWidget, dragged_tile: InventoryViewTile):
        return self.player.can_wear_item(dragged_tile.item, slot.wear_location)

from typing import Optional

import arcade.gui

from game_objects.container import Container
from game_objects.player import Player
from ui.inventory_slot_widget import InventorySlotWidget
from ui.inventory_view_tile import InventoryViewTile, GhostTile


class InventoryUIManager(arcade.gui.UIManager):
    def __init__(self, player: Player):
        super().__init__()

        self.player = player
        self.dragged_tile: Optional[InventoryViewTile] = None
        self.origin_slot: Optional[InventorySlotWidget] = None

    def on_event(self, event) -> bool:
        if isinstance(event, arcade.gui.UIMousePressEvent):
            for widget in self.get_widgets_at(event.pos):
                if isinstance(widget, InventoryViewTile):
                    self.dragged_tile = widget

                if isinstance(widget, InventorySlotWidget):
                    self.origin_slot = widget

            if self.dragged_tile is not None and self.origin_slot is not None:
                ghost = GhostTile(
                    self.dragged_tile.item,
                    x=self.dragged_tile.rect.x,
                    y=self.dragged_tile.rect.y,
                    width=self.dragged_tile.rect.width,
                    height=self.dragged_tile.rect.height
                )
                self.origin_slot.ghost_tile = ghost
                self.add(ghost)

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
                            diff_x = widget.center_x - self.dragged_tile.center_x
                            diff_y = widget.center_y - self.dragged_tile.center_y
                            self.dragged_tile.move(diff_x, diff_y)
                            return_tile = False
                            self.move_tile(self.dragged_tile, self.origin_slot, widget)
                        elif self.slot_has_container(widget):
                            return_tile = False
                            self.drop_tile_into_container(self.dragged_tile, self.origin_slot, widget)

                if return_tile:
                    self.dragged_tile.move(-self.dragged_tile.total_dx, -self.dragged_tile.total_dy)

                if self.origin_slot is not None and self.origin_slot.ghost_tile is not None:
                    self.remove(self.origin_slot.ghost_tile)
                    self.origin_slot.ghost_tile = None

                self.dragged_tile.total_dx = 0
                self.dragged_tile.total_dy = 0
                self.dragged_tile = None
                self.origin_slot = None  # ADD THIS: reset origin_slot too

        return super().on_event(event)

    def slot_can_receive_item(self, slot: InventorySlotWidget, dragged_tile: InventoryViewTile):
        return self.player.can_wear_item(dragged_tile.item, slot.wear_location)

    def move_tile(self, tile: InventoryViewTile, from_slot: InventorySlotWidget, to_slot: InventorySlotWidget):
        from_slot.item_tile = None
        to_slot.item_tile = tile

        self.player.inventory[from_slot.wear_location] = None
        self.player.inventory[to_slot.wear_location] = tile.item

    def slot_has_container(self, slot: InventorySlotWidget) -> bool:
        item = self.player.inventory[slot.wear_location]
        return isinstance(item, Container)

    def drop_tile_into_container(self, tile: InventoryViewTile, from_slot: InventorySlotWidget,
                                 container_slot: InventorySlotWidget):
        container: Container = self.player.inventory[container_slot.wear_location]
        container.add_item(tile.item)

        self.player.inventory[from_slot.wear_location] = None
        from_slot.item_tile = None
        self.remove(tile)

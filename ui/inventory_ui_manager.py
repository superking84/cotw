import time
from typing import Optional, Union, List

import arcade.gui
from pyglet.event import EVENT_HANDLED

import constants
from game_objects.container import Container
from game_objects.player import Player
from ui.container_slot_widget import ContainerSlotWidget
from ui.inventory_slot_widget import InventorySlotWidget
from ui.inventory_view_tile import InventoryViewTile, GhostTile

AnySlot = Union[InventorySlotWidget, ContainerSlotWidget]


class InventoryUIManager(arcade.gui.UIManager):
    def __init__(self, player: Player):
        super().__init__()

        self.player = player
        self.dragged_tile: Optional[InventoryViewTile] = None
        self.origin_slot: Optional[AnySlot] = None

        # Double-click tracking
        self._last_click_time: float = 0
        self._last_click_tile: Optional[InventoryViewTile] = None

        # Container panel state
        self.open_container: Optional[Container] = None
        self.container_slots: List[ContainerSlotWidget] = []

    def on_event(self, event) -> bool:
        if isinstance(event, arcade.gui.UIMousePressEvent):
            for widget in self.get_widgets_at(event.pos):
                if isinstance(widget, InventoryViewTile):
                    self.dragged_tile = widget
                if isinstance(widget, (InventorySlotWidget, ContainerSlotWidget)):
                    self.origin_slot = widget

            if self.dragged_tile is not None:
                now = time.time()
                is_double_click = (
                    now - self._last_click_time < 0.3 and
                    self._last_click_tile is self.dragged_tile
                )
                self._last_click_time = now
                self._last_click_tile = self.dragged_tile

                if is_double_click and isinstance(self.dragged_tile.item, Container):
                    container = self.dragged_tile.item
                    self.dragged_tile = None
                    self.origin_slot = None
                    self._toggle_container_panel(container)
                    return EVENT_HANDLED

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
                        elif self.slot_has_container(widget) and widget.item_tile is not self.dragged_tile:
                            if self.origin_slot is not None and isinstance(self.origin_slot, InventorySlotWidget):
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
                self.origin_slot = None

        return super().on_event(event)

    def slot_can_receive_item(self, slot: InventorySlotWidget, dragged_tile: InventoryViewTile) -> bool:
        return self.player.can_wear_item(dragged_tile.item, slot.wear_location)

    def move_tile(self, tile: InventoryViewTile, from_slot: AnySlot, to_slot: InventorySlotWidget):
        if isinstance(from_slot, ContainerSlotWidget):
            from_slot.container.remove_item(tile.item)
            from_slot.item_tile = None
            self._refresh_container_panel()
        else:
            from_slot.item_tile = None
            self.player.inventory[from_slot.wear_location] = None

        to_slot.item_tile = tile
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

        if self.open_container is container:
            self._refresh_container_panel()

    # ------------------------------------------------------------------
    # Container panel
    # ------------------------------------------------------------------

    def _toggle_container_panel(self, container: Container):
        if self.open_container is container:
            self._close_container_panel()
        else:
            if self.open_container is not None:
                self._close_container_panel()
            self._open_container_panel(container)

    def _open_container_panel(self, container: Container):
        self.open_container = container

        inner_x = constants.CONTAINER_PANEL_X + constants.CONTAINER_PANEL_BORDER
        inner_y = constants.CONTAINER_PANEL_Y + constants.CONTAINER_PANEL_BORDER
        inner_w = constants.CONTAINER_PANEL_WIDTH - 2 * constants.CONTAINER_PANEL_BORDER
        cols = max(1, int(inner_w // constants.INVENTORY_SLOT_WIDTH))

        for i, item in enumerate(container.contents):
            col = i % cols
            row = i // cols
            x = inner_x + col * constants.INVENTORY_SLOT_WIDTH
            y = inner_y + row * constants.INVENTORY_SLOT_HEIGHT

            slot = ContainerSlotWidget(
                x, y,
                constants.INVENTORY_SLOT_WIDTH,
                constants.INVENTORY_SLOT_HEIGHT,
                container, i
            )
            item.sprite.center_x = slot.center_x
            item.sprite.center_y = slot.center_y
            tile = InventoryViewTile(item)
            slot.item_tile = tile

            self.add(slot)
            self.add(tile)
            self.container_slots.append(slot)

    def _close_container_panel(self):
        for slot in self.container_slots:
            if slot.item_tile is not None:
                self.remove(slot.item_tile)
                slot.item_tile = None
            self.remove(slot)
        self.container_slots.clear()
        self.open_container = None

    def _refresh_container_panel(self):
        if self.open_container is not None:
            container = self.open_container
            self._close_container_panel()
            self._open_container_panel(container)

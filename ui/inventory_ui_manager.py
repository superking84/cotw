import arcade.gui

from ui.inventory_slot_widget import InventorySlotWidget


class InventoryUIManager(arcade.gui.UIManager):
    def __init__(self):
        super().__init__()

    def on_event(self, event) -> bool:
        if isinstance(event, arcade.gui.UIMouseReleaseEvent):
            mouse_event: arcade.gui.UIMouseReleaseEvent = event
            for widget in self.get_widgets_at(mouse_event.pos):
                if isinstance(widget, InventorySlotWidget):
                    print("Inventory slot widget")

        return super().on_event(event)

from typing import Optional, TYPE_CHECKING

from arcade.gui import UIWidget

from ui.inventory_view_tile import InventoryViewTile, GhostTile

if TYPE_CHECKING:
    from game_objects.container import Container


class ContainerSlotWidget(UIWidget):
    """
    A slot widget representing a single position inside an open container's
    contents panel.  Holds a reference to the container and the index of the
    item it displays so the manager can remove the item on a successful drag-out.
    """

    def __init__(self, x: float, y: float, width: float, height: float,
                 container: "Container", index: int):
        super().__init__(x, y, width, height)

        self.container = container
        self.index = index
        self.item_tile: Optional[InventoryViewTile] = None
        self.ghost_tile: Optional[GhostTile] = None

from game_objects.item import Item
from game_objects.wear_location import WearLocation


class Consumable(Item):
    """
    Items such as potions, scrolls and wands that can be used one or
    more times.  May either disappear or convert into a "dead"
    version of the item upon depletion.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        super().__init__(img_src, center_x, center_y)

        self.num_uses = 0
        self.wearable_locations = [WearLocation.RIGHT_HAND, WearLocation.LEFT_HAND]
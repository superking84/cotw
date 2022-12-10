from game_objects.wear_location import WearLocation


class Item:
    """
    Any in-game object that the player may carry and interact with in some way.
    """

    def __init__(self):
        self.weight = 0
        self.size = 0

        self.wearable_locations = []


class Equipment(Item):
    """
    Any item that the player may wear. Optionally alters the player's stats.
    """

    def __init__(self):
        super(Equipment, self).__init__()

        self.wear_location = None


class Consumable(Item):
    """
    Items such as potions, scrolls and wands that can be used one or
    more times.  May either disappear or convert into a "dead"
    version of the item upon depletion.
    """

    def __init__(self):
        super(Consumable, self).__init__()

        self.num_uses = 0
        self.wearable_locations = [WearLocation.RIGHT_HAND, WearLocation.LEFT_HAND]


class Container(Item):
    """
    Items such as backpacks and chests that may contain other items.
    May or may not be wearable.
    """

    def __init__(self):
        super(Container, self).__init__()

        self.size_capacity = 0

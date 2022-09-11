from enum import Enum


class WearLocation(Enum):
    TORSO = 1
    NECK = 2
    BACK = 3
    HEAD = 4
    SHIELD = 5
    LEGS = 6
    HANDS = 7
    RIGHT_HAND = 8
    LEFT_HAND = 9
    RIGHT_RING = 10
    LEFT_RING = 10
    WAIST = 11
    FEET = 12
    BACKPACK = 13
    PURSE = 14


class Item:
    def __init__(self):
        self.weight = 0
        self.size = 0

        self.wearable_locations = []


class Equipment(Item):
    """
    Any wearable item that provides a boost in stats to the player.
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

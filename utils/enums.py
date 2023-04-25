from enum import Enum


class ActionType(Enum):
    MOVE = 1
    MOVE_DIAGONAL = 2
    ATTACK = 3


class WearLocation(Enum):
    ARMOR = 1
    NECKWEAR = 2
    CLOAK = 3
    HELMET = 4
    SHIELD = 5
    BRACERS = 6
    GAUNTLETS = 7
    RIGHT_HAND = 8
    LEFT_HAND = 9
    RIGHT_RING = 10
    LEFT_RING = 10
    BELT = 11
    BOOTS = 12
    BACKPACK = 13
    PURSE = 14

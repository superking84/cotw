from enum import Enum


class ActionType(Enum):
    MOVE = 1
    MOVE_DIAGONAL = 2
    ATTACK = 3


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

import arcade
import constants
from constants import ActionType, MOVEMENT_TIMES


class Character:
    """
    The base class for all characters in the game.
    Base functionality is inherited by Player, Enemy
    and any other "character"-type entities in the game.
    """

    def __init__(self):
        self.sprite = None

        self.level = 1

        # base stats
        self.strength = 0
        self.dexterity = 0
        self.intelligence = 0
        self.constitution = 0

        # calculated stats
        self.health = 100
        self.mana = 0
        self.speed = 1.00

    def setup(self, strength: int, dexterity: int, intelligence: int,
              constitution: int):
        # base stats
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.constitution = constitution

        # calculated stats

    def calculate_action_time(self, base_completion_time: float):
        """
        Determine the time the character will take to complete
        a given action.
        """
        return base_completion_time / self.speed
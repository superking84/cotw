from GameTimer import GameTimer
from constants import BASE_MOVEMENT_TIME


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
        self.health = 0
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


class Enemy(Character):
    def __init__(self):
        super(Enemy, self).__init__()

        self.target = None
        self.next_action = None  # represents the next action the enemy wants to take
        # how many seconds to complete that action?
        # if the Enemy wants to do something that takes 5 seconds but only
        # one second has passed, they will need to wait
        self.time_to_next_action = 0

    def setup(self, strength: int, dexterity: int, intelligence: int,
              constitution: int, health: int, mana: int, target: Character):
        super(Enemy, self).setup(strength, dexterity, intelligence,
                                 constitution, health, mana)

        self.target = target

    def process_time(self, elapsed_time: int):
        """
        TODO: Think about an enemy being able to change actions? Cash in elapsed time toward new action
        TODO: That is, if move takes 5 and they decide to change to attack which takes 6,
        TODO: they should only have to wait 1 more second
        TODO: this makes sense to me since actions are discrete and not continuous in this game engine.

        :param elapsed_time: driven by game timer ticks, this is the amount of time that has
        passed since the last tick
        :return: None
        """
        self.time_to_next_action -= elapsed_time

        if self.time_to_next_action <= 0:
            # perform next action
            # select new action
            # reset timer based on time needed
            return


class Player(Character):
    def __init__(self):
        super(Player, self).__init__()

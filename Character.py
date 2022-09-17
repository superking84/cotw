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


class Enemy(Character):
    def __init__(self):
        super(Enemy, self).__init__()

        self.target = None
        self.next_action = None  # represents the next action the enemy wants to take
        # how many seconds to complete that action?
        # if the Enemy wants to do something that takes 5 seconds but only
        # one second has passed, they will need to wait
        self.time_to_next_action = 0
        self.time_since_last_action = 0

    def setup(self, strength: int, dexterity: int, intelligence: int,
              constitution: int, health: int, mana: int, target: Character):
        super(Enemy, self).setup(strength, dexterity, intelligence,
                                 constitution)

        self.health = health
        self.mana = mana
        self.target = target
        self.select_next_action()

        self.speed = 0.5

    def is_next_to_target(self):
        if not self.sprite:
            return

        target_x = self.target.sprite.center_x
        target_y = self.target.sprite.center_y

        self_x = self.sprite.center_x
        self_y = self.sprite.center_y

        return abs(self_x - target_x) <= constants.PLAYER_MOVEMENT_SPEED and \
            abs(self_y - target_y) <= constants.PLAYER_MOVEMENT_SPEED

    def select_next_action(self):
        if self.is_next_to_target():
            self.next_action = ActionType.ATTACK
        else:
            self.next_action = ActionType.MOVE

        self.time_to_next_action = (MOVEMENT_TIMES[self.next_action] - self.time_since_last_action) / self.speed

        self.time_since_last_action = 0

    def process_time(self, elapsed_time: int):
        """
        :param elapsed_time: driven by game timer ticks, this is the amount of time that has
        passed since the last tick
        :return: None
        """
        self.time_to_next_action -= elapsed_time
        self.time_since_last_action += elapsed_time

        if self.time_to_next_action <= 0:
            self.execute_next_action()
            self.select_next_action()

    def execute_next_action(self):
        if self.next_action == ActionType.MOVE:
            self.move()
        else:
            self.attack_target()

        self.time_since_last_action = 0

    def attack_target(self):
        # TODO: placeholder
        self.target.health -= 1

    def move(self):
        target_x = self.target.sprite.center_x
        target_y = self.target.sprite.center_y
        start_x = self.sprite.center_x
        start_y = self.sprite.center_y

        move_x = constants.PLAYER_MOVEMENT_SPEED \
            if target_x > self.sprite.center_x \
            else -constants.PLAYER_MOVEMENT_SPEED \
            if target_x < self.sprite.center_x else 0
        move_y = constants.PLAYER_MOVEMENT_SPEED \
            if target_y > self.sprite.center_y \
            else -constants.PLAYER_MOVEMENT_SPEED \
            if target_y < self.sprite.center_y else 0

        did_collide_with_enemy = arcade.check_for_collision(self.sprite, self.target.sprite)

        self.sprite.center_x += move_x
        self.sprite.center_y += move_y
        if did_collide_with_enemy:
            print("Collision")
            self.sprite.center_x = start_x
            self.sprite.center_y = start_y
            self.select_next_action()


class Player(Character):
    def __init__(self):
        super(Player, self).__init__()

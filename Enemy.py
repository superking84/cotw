import arcade

import constants
from ActionTypes import ActionType
from Character import Character


class Enemy(Character):
    def __init__(self):
        super(Enemy, self).__init__()

        self.target = None
        self.destination = (None, None)

        self.next_action = None
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
        if not (self.target and self.sprite):
            return

        if self.is_next_to_target():
            self.next_action = ActionType.ATTACK
        else:
            target_x = self.target.sprite.center_x
            target_y = self.target.sprite.center_y

            move_x = constants.PLAYER_MOVEMENT_SPEED \
                if target_x > self.sprite.center_x \
                else -constants.PLAYER_MOVEMENT_SPEED \
                if target_x < self.sprite.center_x else 0
            move_y = constants.PLAYER_MOVEMENT_SPEED \
                if target_y > self.sprite.center_y \
                else -constants.PLAYER_MOVEMENT_SPEED \
                if target_y < self.sprite.center_y else 0

            if move_x == 0 or move_y == 0:
                self.next_action = ActionType.MOVE
            else:
                self.next_action = ActionType.MOVE_DIAGONAL

            self.destination = (move_x, move_y)

        self.time_to_next_action = (constants.MOVEMENT_TIMES[self.next_action] -
                                    self.time_since_last_action) / self.speed

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
        if self.next_action in [ActionType.MOVE, ActionType.MOVE_DIAGONAL]:
            self.move()
        else:
            self.attack_target()

        self.time_since_last_action = 0

    def attack_target(self):
        # TODO: Implement combat and remove this placeholder line
        self.target.health -= 1

    def move(self):
        # TODO: Address issue with movement between tiles, as enemy currently seems to get out of alignment
        start_x = self.sprite.center_x
        start_y = self.sprite.center_y

        self.sprite.center_x += self.destination[0]
        self.sprite.center_y += self.destination[1]

        did_collide_with_enemy = arcade.check_for_collision(self.sprite, self.target.sprite)
        if did_collide_with_enemy:
            self.sprite.center_x = start_x
            self.sprite.center_y = start_y
            self.select_next_action()

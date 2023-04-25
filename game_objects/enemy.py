import arcade

import constants
from game_objects.character import Character
from utils.enums import ActionType


class Enemy(Character):
    def __init__(self, img_src: str, center_x: int, center_y: int):
        super(Enemy, self).__init__(img_src, center_x, center_y)

        self.scene = None
        self.target = None
        self.destination = (None, None)

        self.next_action = None
        self.time_since_last_action = 0

    def setup(self, strength: int, dexterity: int, intelligence: int,
              constitution: int, health: int, mana: int, scene: arcade.Scene, target: Character):
        super().setup(strength, dexterity, intelligence,
                      constitution)

        self.scene = scene
        self.health = health
        self.mana = mana
        self.target = target

        self.select_next_action()

        self.speed = 0.5

    def is_next_to_target(self):
        target_x = self.target.sprite.center_x
        target_y = self.target.sprite.center_y

        self_x = self.sprite.center_x
        self_y = self.sprite.center_y

        return abs(self_x - target_x) <= constants.PLAYER_MOVEMENT_SPEED and abs(
            self_y - target_y) <= constants.PLAYER_MOVEMENT_SPEED

    def select_next_action(self):
        if not self.target:
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

    def process_time(self, elapsed_time: int):
        """
        Check if it is time to perform the next action, and do so if possible.
        :param elapsed_time: driven by game timer ticks, this is the amount of time that has
        passed since the last tick
        :return: None
        """
        if not self.next_action:
            self.select_next_action()

        self.time_since_last_action += elapsed_time
        while True:
            action_time = self.calculate_action_time(constants.ACTION_TIMES[self.next_action])
            if self.time_since_last_action >= action_time:
                self.time_since_last_action -= action_time
                self.execute_next_action()
                self.select_next_action()
            else:
                break

    def execute_next_action(self):
        if self.next_action in [ActionType.MOVE, ActionType.MOVE_DIAGONAL]:
            self.move()
        elif self.next_action == ActionType.ATTACK:
            self.attack_target()
        else:
            return

        self.next_action = None

    def attack_target(self):
        # TODO: Implement combat and remove this placeholder line
        self.target.health -= 1

    def move(self):
        # TODO: Address issue with movement between tiles, as enemy currently seems to get out of alignment
        start_x = self.sprite.center_x
        start_y = self.sprite.center_y

        self.sprite.center_x += self.destination[0]
        self.sprite.center_y += self.destination[1]

        did_collide_with_target = arcade.check_for_collision(self.sprite, self.target.sprite)
        wall_hit_list = arcade.check_for_collision_with_lists(self.sprite, [self.scene[constants.LAYER_NAME_FOREGROUND],
                                                                            self.scene[constants.LAYER_NAME_WALLS]])
        enemy_hit_list = arcade.check_for_collision_with_list(self.sprite, self.scene[constants.LAYER_NAME_ENEMIES])

        if did_collide_with_target or len(wall_hit_list) > 0 or len(enemy_hit_list) > 0:
            self.sprite.center_x = start_x
            self.sprite.center_y = start_y
            # if did_collide_with_target:
            #     self.select_next_action()

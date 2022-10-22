import arcade

import constants
from game_objects.Character import Character
from game_objects.Item import WearLocation


class Player(Character):
    def __init__(self, img_src: str, center_x: int, center_y: int):
        super(Player, self).__init__(img_src, center_x, center_y)

        self.is_moving = False
        self.first_move_complete = False
        self.move_wait_elapsed = 0
        self.move_delay = constants.FIRST_MOVE_DELAY_SECONDS

        self.equipment = dict()

    def setup(self, strength: int, dexterity: int, intelligence: int,
              constitution: int, health: int, mana: int):
        super(Player, self).setup(strength, dexterity, intelligence, constitution)

        for wearable_location in WearLocation:
            self.equipment[wearable_location] = None

    def on_key_press(self, key: arcade.key):
        if key in constants.MOVEMENT_KEYS:
            self.is_moving = True
            self.move_delay = constants.FIRST_MOVE_DELAY_SECONDS
            self.first_move_complete = True
            self.move_wait_elapsed = 0

    def on_key_release(self, keys_pressed: list):
        if not any([_key in constants.MOVEMENT_KEYS for _key in keys_pressed]):
            self.first_move_complete = False
            self.move_wait_elapsed = 0
            self.is_moving = False

    @staticmethod
    def get_movement_direction(keys_pressed: list):
        """
        :return: A 2-tuple (x, y) which represents the direction of movement resulting
        from the keypress.
        """
        last_key = keys_pressed[-1]

        move_x = 0
        move_y = 0
        match last_key:
            case arcade.key.UP | arcade.key.NUM_8 | arcade.key.W:
                move_y = 1
            case arcade.key.DOWN | arcade.key.NUM_2 | arcade.key.S:
                move_y = -1
            case arcade.key.LEFT | arcade.key.NUM_4 | arcade.key.A:
                move_x = -1
            case arcade.key.RIGHT | arcade.key.NUM_6 | arcade.key.D:
                move_x = 1
            case arcade.key.NUM_1 | arcade.key.Z:
                move_x = -1
                move_y = -1
            case arcade.key.NUM_3 | arcade.key.C:
                move_x = 1
                move_y = -1
            case arcade.key.NUM_7 | arcade.key.Q:
                move_x = -1
                move_y = 1
            case arcade.key.NUM_9 | arcade.key.E:
                move_x = 1
                move_y = 1

        return move_x, move_y

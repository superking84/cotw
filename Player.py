import arcade
import constants
from Character import Character
from Enemy import Enemy


class Player(Character):
    def __init__(self):
        super(Player, self).__init__()

        self.is_moving = False
        self.first_move_complete = False
        self.move_wait_elapsed = 0
        self.move_delay = constants.FIRST_MOVE_DELAY_SECONDS

    def on_key_press(self, key: arcade.key):
        if key in constants.MOVEMENT_KEYS:
            self.is_moving = True
            self.move_delay = constants.FIRST_MOVE_DELAY_SECONDS
            self.first_move_complete = True
            self.move_wait_elapsed = 0

    def on_key_release(self, key: arcade.key, keys_pressed: list):
        if not any([_key in constants.MOVEMENT_KEYS for _key in keys_pressed]):
            self.first_move_complete = False
            self.move_wait_elapsed = 0
            self.is_moving = False

    def process_movement(self, keys_pressed: list, scene: arcade.Scene, enemy: Enemy):
        last_key = keys_pressed[-1]

        previous_location = [self.sprite.center_x, self.sprite.center_y]
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

        self.sprite.center_x += constants.PLAYER_MOVEMENT_SPEED * move_x
        self.sprite.center_y += constants.PLAYER_MOVEMENT_SPEED * move_y

        wall_hit_list = arcade.check_for_collision_with_lists(self.sprite,
                                                              [scene[constants.LAYER_NAME_FOREGROUND],
                                                               scene[constants.LAYER_NAME_WALLS]])
        # TODO: Plugging in enemy movement to wall collision
        did_collide_with_enemy = arcade.check_for_collision(self.sprite, enemy.sprite)

        if len(wall_hit_list) > 0:
            self.sprite.center_x = previous_location[0]
            self.sprite.center_y = previous_location[1]
            return 0
        elif did_collide_with_enemy:
            self.sprite.center_x = previous_location[0]
            self.sprite.center_y = previous_location[1]
            action_type = constants.ActionType.ATTACK
            enemy.health -= 1
        else:
            if move_x == 0 or move_y == 0:
                action_type = constants.ActionType.MOVE
            else:
                action_type = constants.ActionType.MOVE_DIAGONAL

        return self.calculate_action_time(constants.MOVEMENT_TIMES[action_type])


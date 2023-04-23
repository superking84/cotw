import random

import arcade

import constants
from game_objects.action_type import ActionType
from game_objects.enemy import Enemy
from game_objects.game_timer import GameTimer
from game_objects.player import Player

enemy_img_src = "resources/images/zombie_idle.png"


class WorldView(arcade.View):
    def __init__(self):
        super().__init__()

        self.camera = None
        self.gui_camera = None
        self.scene = None
        self.tile_map = None

        self.player = None
        self.enemy = None

        self.keys_pressed = []

        self.timer = GameTimer()

    def setup(self):
        self.camera = arcade.Camera(self.window.width, self.window.height)

        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        map_name = f"./resources/map1.json"

        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options=None)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list_after(constants.LAYER_NAME_PLAYER, constants.LAYER_NAME_WALLS)
        self.scene.add_sprite_list_after(constants.LAYER_NAME_ENEMIES, constants.LAYER_NAME_PLAYER)
        image_source = "./resources/images/femaleAdventurer_idle.png"
        self.player = Player(image_source, constants.PLAYER_START_X, constants.PLAYER_START_Y)
        self.player.setup(
            strength=10,
            dexterity=10,
            intelligence=10,
            constitution=10,
            health=50,
            mana=25
        )

        self.scene.add_sprite(constants.LAYER_NAME_PLAYER, self.player)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        else:
            arcade.set_background_color(arcade.csscolor.GRAY)

        self.add_enemy_to_scene()
        self.add_enemy_to_scene()
        self.center_camera_to_player()

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our scene
        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()
        score_text = f"Game time: {self.timer.get_game_time()}"

        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18
        )

    def on_key_press(self, key: int, modifiers: int):
        if key not in self.keys_pressed:
            self.keys_pressed.append(key)

            self.player.on_key_press(key)
            if key in constants.MOVEMENT_KEYS:
                self.process_movement()
                self.center_camera_to_player()

            match key:
                case arcade.key.ESCAPE:
                    arcade.exit()
                case arcade.key.I:
                    self.window.show_view(self.window.views["inventory"])

    def on_key_release(self, key: int, modifiers: int):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

            self.player.on_key_release(self.keys_pressed)

    def on_hide_view(self):
        self.keys_pressed = []

    def on_update(self, delta_time: float):
        if self.player.is_moving and (self.player.move_wait_elapsed >= self.player.move_delay):
            if self.player.move_wait_elapsed >= self.player.move_delay:
                self.player.move_delay = constants.MOVE_DELAY_SECONDS

            self.player.move_wait_elapsed = 0
            self.process_movement()
            self.center_camera_to_player()

        if self.player.is_moving:
            self.player.move_wait_elapsed += delta_time

    def add_enemy_to_scene(self):
        enemy_location = self.get_random_placement_location()
        enemy = Enemy(enemy_img_src, enemy_location[0], enemy_location[1])
        enemy.setup(
            strength=10,
            dexterity=10,
            intelligence=10,
            constitution=10,
            health=5,
            mana=5,
            scene=self.scene,
            target=self.player
        )

        self.scene.add_sprite(constants.LAYER_NAME_ENEMIES, enemy)
        self.timer.register_listener(enemy)

    def get_random_placement_location(self):
        map_width = self.tile_map.tiled_map.map_size.width
        map_height = self.tile_map.tiled_map.map_size.height

        x = (random.randint(0, map_width) * constants.SCALED_SPRITE_PIXEL_SIZE) + (16 * constants.TILE_SCALING)
        y = (random.randint(0, map_height) * constants.SCALED_SPRITE_PIXEL_SIZE) - (16 * constants.TILE_SCALING)

        return x, y

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def process_movement(self):
        (move_x, move_y) = self.player.get_movement_direction(self.keys_pressed)

        previous_location = [self.player.center_x, self.player.center_y]
        self.player.set_position(
            self.player.center_x + (move_x * constants.PLAYER_MOVEMENT_SPEED),
            self.player.center_y + (move_y * constants.PLAYER_MOVEMENT_SPEED)
        )

        wall_hit_list = arcade.check_for_collision_with_lists(self.player,
                                                              [self.scene[constants.LAYER_NAME_FOREGROUND],
                                                               self.scene[constants.LAYER_NAME_WALLS]])
        enemy_hit_list = arcade.check_for_collision_with_list(self.player,
                                                              self.scene[constants.LAYER_NAME_ENEMIES])

        action_type = ActionType.MOVE if move_x == 0 or move_y == 0 else ActionType.MOVE_DIAGONAL
        if len(wall_hit_list) > 0:
            self.player.set_position(previous_location[0], previous_location[1])
        elif len(enemy_hit_list) > 0:
            self.player.set_position(previous_location[0], previous_location[1])
            action_type = ActionType.ATTACK
            
            # noinspection PyTypeChecker
            enemy: Enemy = enemy_hit_list[0]
            enemy.health -= 1

        action_time = self.player.calculate_action_time(constants.ACTION_TIMES[action_type])
        if action_time > 0:
            self.timer.advance_time(action_time)

            for enemy in self.scene[constants.LAYER_NAME_ENEMIES]:
                if enemy.health <= 0:
                    self.timer.unregister_listener(enemy)
                    enemy.kill()

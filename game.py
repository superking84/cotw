import arcade
import constants
from Enemy import Enemy
from GameTimer import GameTimer
from Player import Player


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        self.camera = None
        self.gui_camera = None
        self.scene = None
        self.tile_map = None

        self.player = None
        self.enemy = None

        self.ticks = 0  # seconds

        self.keys_pressed = []

        self.is_moving = False
        self.first_move_complete = False
        self.move_wait_elapsed = 0
        self.move_delay = constants.FIRST_MOVE_DELAY_SECONDS

        self.level = 1

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.collect_last_coin_sound = arcade.load_sound(":resources:sounds/coin2.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        self.score = 0
        self.reset_score = True

        self.timer = GameTimer()

    def setup(self):
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        map_name = f"map1.json"

        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options=None)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        if self.reset_score:
            self.score = 0
        self.reset_score = True

        self.scene.add_sprite_list_after("Player", constants.LAYER_NAME_WALLS)

        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player = Player()
        self.player.setup(10, 10, 10, 10)
        self.player.sprite = arcade.Sprite(image_source, constants.CHARACTER_SCALING)

        self.player.sprite.center_x = 48
        self.player.sprite.center_y = 48
        self.scene.add_sprite("Player", self.player.sprite)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        else:
            arcade.set_background_color(arcade.csscolor.GRAY)

        enemy_img_src = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.enemy = Enemy()
        self.enemy.setup(10, 10, 10, 10, 20, 5, self.player)
        self.enemy.sprite = arcade.Sprite(enemy_img_src, constants.CHARACTER_SCALING)
        self.enemy.sprite.center_x = 240
        self.enemy.sprite.center_y = 120
        self.scene.add_sprite("Enemy", self.enemy.sprite)
        self.timer.register_listener(self.enemy)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our scene
        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()
        score_text = f"Game time: {self.timer.get_game_time()}"
        # score_text = f"Player Health: {self.player.health}.  Enemy Health: {self.enemy.health}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18
        )

    def on_key_press(self, key: int, modifiers: int):
        self.keys_pressed.append(key)

        if key in constants.MOVEMENT_KEYS:
            self.process_movement()
            self.center_camera_to_player()
            self.is_moving = True
            self.move_delay = constants.FIRST_MOVE_DELAY_SECONDS
            self.first_move_complete = True
            self.move_wait_elapsed = 0

        match key:
            case arcade.key.ESCAPE:
                arcade.exit()

    def on_key_release(self, key: int, modifiers: int):
        self.keys_pressed.remove(key)

        if not any([_key in constants.MOVEMENT_KEYS for _key in self.keys_pressed]):
            self.first_move_complete = False
            self.move_wait_elapsed = 0
            self.is_moving = False

    def process_movement(self):
        last_key = self.keys_pressed[-1]

        previous_location = [self.player.sprite.center_x, self.player.sprite.center_y]
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

        self.player.sprite.center_x += constants.PLAYER_MOVEMENT_SPEED * move_x
        self.player.sprite.center_y += constants.PLAYER_MOVEMENT_SPEED * move_y

        wall_hit_list = arcade.check_for_collision_with_lists(self.player.sprite,
                                                              [self.scene[constants.LAYER_NAME_FOREGROUND],
                                                               self.scene[constants.LAYER_NAME_WALLS]])
        # TODO: Plugging in enemy movement to wall collision
        did_collide_with_enemy = arcade.check_for_collision(self.player.sprite, self.enemy.sprite)

        if len(wall_hit_list) > 0 or did_collide_with_enemy:
            self.player.sprite.center_x = previous_location[0]
            self.player.sprite.center_y = previous_location[1]

            if did_collide_with_enemy:
                self.enemy.health -= 1
        else:
            print(move_x)
            print(move_y)
            if move_x == 0 or move_y == 0:
                action_type = constants.ActionType.MOVE
            else:
                action_type = constants.ActionType.MOVE_DIAGONAL

            movement_time = self.player.calculate_action_time(constants.MOVEMENT_TIMES[action_type])
            self.timer.advance_time(movement_time)

    def on_update(self, delta_time: float):
        if self.is_moving and (self.move_wait_elapsed >= self.move_delay):
            if self.move_wait_elapsed >= self.move_delay:
                self.move_delay = constants.MOVE_DELAY_SECONDS

            self.move_wait_elapsed = 0
            self.process_movement()
            self.center_camera_to_player()

        if self.is_moving:
            self.move_wait_elapsed += delta_time

    def center_camera_to_player(self):
        screen_center_x = self.player.sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.sprite.center_y - (self.camera.viewport_height / 2)

        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

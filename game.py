import arcade
import constants


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

        self.player_sprite = None

        self.keys_pressed = []

        self.is_moving = False
        self.first_move_complete = False
        self.move_wait_elapsed = 0
        self.move_delay = constants.FIRST_MOVE_DELAY_SECONDS

        self.end_of_map = 0
        self.level = 1

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.collect_last_coin_sound = arcade.load_sound(":resources:sounds/coin2.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        self.score = 0
        self.reset_score = True

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
        self.player_sprite = arcade.Sprite(image_source, constants.CHARACTER_SCALING)
        self.player_sprite.center_x = 48
        self.player_sprite.center_y = 48
        self.scene.add_sprite("Player", self.player_sprite)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        else:
            arcade.set_background_color(arcade.csscolor.GRAY)

        self.end_of_map = self.tile_map.width * constants.GRID_PIXEL_SIZE

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our scene
        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()
        score_text = f"Score: {self.score}"
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

        previous_location = [self.player_sprite.center_x, self.player_sprite.center_y]
        match last_key:
            case arcade.key.UP | arcade.key.NUM_8:
                self.player_sprite.center_y += constants.PLAYER_MOVEMENT_SPEED
            case arcade.key.DOWN | arcade.key.NUM_2:
                self.player_sprite.center_y -= constants.PLAYER_MOVEMENT_SPEED
            case arcade.key.LEFT | arcade.key.NUM_4:
                self.player_sprite.center_x -= constants.PLAYER_MOVEMENT_SPEED
            case arcade.key.RIGHT | arcade.key.NUM_6:
                self.player_sprite.center_x += constants.PLAYER_MOVEMENT_SPEED
            case arcade.key.NUM_1:
                self.player_sprite.center_x -= constants.PLAYER_MOVEMENT_SPEED
                self.player_sprite.center_y -= constants.PLAYER_MOVEMENT_SPEED
            case arcade.key.NUM_3:
                self.player_sprite.center_x += constants.PLAYER_MOVEMENT_SPEED
                self.player_sprite.center_y -= constants.PLAYER_MOVEMENT_SPEED
            case arcade.key.NUM_7:
                self.player_sprite.center_x -= constants.PLAYER_MOVEMENT_SPEED
                self.player_sprite.center_y += constants.PLAYER_MOVEMENT_SPEED
            case arcade.key.NUM_9:
                self.player_sprite.center_x += constants.PLAYER_MOVEMENT_SPEED
                self.player_sprite.center_y += constants.PLAYER_MOVEMENT_SPEED

        wall_hit_list = arcade.check_for_collision_with_lists(self.player_sprite,
                                                              [self.scene[constants.LAYER_NAME_FOREGROUND],
                                                               self.scene[constants.LAYER_NAME_WALLS]])

        if len(wall_hit_list) > 0:
            self.player_sprite.center_x = previous_location[0]
            self.player_sprite.center_y = previous_location[1]

    def on_update(self, delta_time: float):
        # self.physics_engine.update()

        if self.is_moving and (self.move_wait_elapsed >= self.move_delay):
            if self.move_wait_elapsed >= self.move_delay:
                self.move_delay = constants.MOVE_DELAY_SECONDS

            self.move_wait_elapsed = 0
            self.process_movement()
            self.center_camera_to_player()

        if self.is_moving:
            self.move_wait_elapsed += delta_time

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
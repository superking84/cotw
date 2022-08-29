import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Scaling constants
CHARACTER_SCALING = 0.5
TILE_SCALING = 1
COIN_SCALING = 0.5

SPRITE_PIXEL_SIZE = 32
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_MOVEMENT_SPEED = 32

PLAYER_START_X = 64
PLAYER_START_Y = 225

LAYER_NAME_BACKGROUND = "Floor"
LAYER_NAME_FOREGROUND = "Scenery"
LAYER_NAME_WALLS = "Walls"

FIRST_MOVE_DELAY_SECONDS = 0.5
MOVE_DELAY_SECONDS = 0.125

MOVEMENT_KEYS = [
    arcade.key.UP,
    arcade.key.DOWN,
    arcade.key.LEFT,
    arcade.key.RIGHT,
    arcade.key.W,
    arcade.key.A,
    arcade.key.S,
    arcade.key.D,
    arcade.key.NUM_1,
    arcade.key.NUM_2,
    arcade.key.NUM_3,
    arcade.key.NUM_4,
    arcade.key.NUM_6,
    arcade.key.NUM_7,
    arcade.key.NUM_8,
    arcade.key.NUM_9
]
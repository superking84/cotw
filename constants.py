import arcade

from ActionTypes import ActionType

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer"

# Scaling constants
TILE_SCALING = 1
CHARACTER_SCALING = TILE_SCALING / 4

SPRITE_PIXEL_SIZE = 32 * TILE_SCALING
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_MOVEMENT_SPEED = SPRITE_PIXEL_SIZE
DIAGONAL_MOVEMENT_MODIFIER = 1.41421356237

PLAYER_START_X = (SPRITE_PIXEL_SIZE * 5) + (16 * TILE_SCALING)
PLAYER_START_Y = (SPRITE_PIXEL_SIZE * 12) - (16 * TILE_SCALING)

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
    arcade.key.Q,
    arcade.key.E,
    arcade.key.Z,
    arcade.key.C,
    arcade.key.NUM_1,
    arcade.key.NUM_2,
    arcade.key.NUM_3,
    arcade.key.NUM_4,
    arcade.key.NUM_6,
    arcade.key.NUM_7,
    arcade.key.NUM_8,
    arcade.key.NUM_9
]

MOVEMENT_TIMES = {
    ActionType.MOVE: 4.0,
    ActionType.ATTACK: 5.0
}
MOVEMENT_TIMES[ActionType.MOVE_DIAGONAL] = MOVEMENT_TIMES[ActionType.MOVE] * DIAGONAL_MOVEMENT_MODIFIER

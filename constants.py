import arcade

from game_objects.action_type import ActionType

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer"

# Scaling constants
TILE_SCALING = 1
CHARACTER_SCALING = TILE_SCALING / 4

SPRITE_PIXEL_SIZE = 32
SCALED_SPRITE_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
GRID_PIXEL_SIZE = SCALED_SPRITE_PIXEL_SIZE
PLAYER_MOVEMENT_SPEED = SCALED_SPRITE_PIXEL_SIZE
DIAGONAL_MOVEMENT_MODIFIER = 1.41421356237

PLAYER_START_X = (SCALED_SPRITE_PIXEL_SIZE * 4) + (16 * TILE_SCALING)
PLAYER_START_Y = (SCALED_SPRITE_PIXEL_SIZE * 12) - (16 * TILE_SCALING)
ENEMY_START_X = (SCALED_SPRITE_PIXEL_SIZE * 8) + (16 * TILE_SCALING)
ENEMY_START_Y = (SCALED_SPRITE_PIXEL_SIZE * 8) - (16 * TILE_SCALING)

LAYER_NAME_BACKGROUND = "Floor"
LAYER_NAME_FOREGROUND = "Scenery"
LAYER_NAME_WALLS = "Walls"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"

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

ACTION_TIMES = {
    ActionType.MOVE: 4.0,
    ActionType.ATTACK: 5.0
}
ACTION_TIMES[ActionType.MOVE_DIAGONAL] = ACTION_TIMES[ActionType.MOVE] * DIAGONAL_MOVEMENT_MODIFIER

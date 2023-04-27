import arcade

import constants


class Character:
    """
    The base class for all characters in the game.
    Base functionality is inherited by Player, Enemy
    and any other "character"-type entities in the game.
    """

    def __init__(self, img_src: str, center_x: int, center_y: int):
        self.sprite = arcade.Sprite(img_src, constants.CHARACTER_SCALING, center_x=center_x, center_y=center_y)
        self.level = 1

        # base stats
        self.strength = 0
        self.dexterity = 0
        self.intelligence = 0
        self.constitution = 0

        # calculated stats
        self.health = 100
        self.mana = 0
        self.speed = 1.00

    def calculate_action_time(self, base_completion_time: float):
        """
        Determine the time the character will take to complete
        a given action.
        :param base_completion_time: The amount of time an action normally
        takes to complete, before modification.
        :return: The amount of time the action will take to complete given
        other factors affecting the character.
        """
        return base_completion_time / self.speed

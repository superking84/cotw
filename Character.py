class Character:
    """
    The base class for all characters in the game.
    Base functionality is inherited by Player, Enemy
    and any other "character"-type entities in the game.
    """
    def __init__(self):
        self.sprite = None

        self.strength = 0
        self.dexterity = 0
        self.intelligence = 0
        self.constitution = 0

        self.health = 0
        self.mana = 0
        self.level = 1

    def setup(self, strength: int, dexterity: int, intelligence: int,
              constitution: int, health: int, mana: int):
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.constitution = constitution
        self.health = health
        self.mana = mana


class Enemy(Character):
    def __init__(self):
        super(Enemy, self).__init__()

        self.target = None

    def setup(self, strength: int, dexterity: int, intelligence: int,
              constitution: int, health: int, mana: int, target: Character):
        super(Enemy, self).setup(strength, dexterity, intelligence,
                                 constitution, health, mana)

        self.target = target


class Player(Character):
    def __init__(self):
        super(Player, self).__init__()


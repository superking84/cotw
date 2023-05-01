from typing import List, Optional

from game_objects.enemy import Enemy
from game_objects.item import Item


class Room:
    def __init__(self, enemy: Optional[Enemy], contents: List[Item]):
        self.enemy = enemy
        self.contents = contents

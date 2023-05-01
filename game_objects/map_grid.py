from typing import List

from game_objects.room import Room


class MapGrid:
    def __init__(self, rooms: List[List[Room]]):
        self.rooms = rooms

    def get_room_at(self, row: int, col: int):
        return self.rooms[row][col]

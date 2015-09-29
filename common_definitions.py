#!python3

# common_definitions.py

from enum import IntEnum, unique


class BoardFieldType(IntEnum):
    HOME = 0
    FIELD = 1
    FINISH = 2


# Players
@unique
class Players(IntEnum):
    black = 0
    yellow = 1
    green = 2
    red = 3

    @staticmethod
    def next(current):
        if current == Players.red:
            return Players.black
        return Players(current + 1)

PlayerCount = 4
PawnCount = 4
BoardFieldCount = 40

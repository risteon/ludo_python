### Board

# enum
from enum import Enum, unique

@unique
class FieldType(Enum):
    simple = 0
    start = 1
    finish = 2

class Player:

    def __init__(self, number):
        self.number = number
        print("New player: ", number)

    def get_number(self):
        return self.number


class BoardField:

    def __init__(self):
        self.field_type = FieldType.simple
        self.pawn = 0

    def get_field_type(self):
        return self.field_type


class Board:
    def __init__(self):
        print("yay")
        self.field = [[BoardField() for j in range(10)] for i in range(4)]
        self.finish = [[BoardField() for j in range(4)] for i in range(4)]

    def move_pawn(self):
        print("blubb")

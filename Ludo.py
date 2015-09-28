#!/usr/bin/env python3

### Ludo.py

from die import Die
from board import Board
from board import BoardField
from board import Player

from BoardDrawer import BoardDrawer
from BoardDrawer import BoardFieldType
from BoardDrawer import Players

print("Welcome to a game of ludo!")

print("Let's test the die:")
the_die = Die()
print(the_die.roll())

print("Let's create a playing board:")
the_board = Board()

# field type test
board_field = BoardField()
print(board_field.get_field_type())

# player test
player = Player(0)

# print board
board_drawer = BoardDrawer()
board_drawer.show_board()

# move pawn around
# board_drawer.move_player(4, BoardFieldType.FIELD, Players.black, 0)
#board_drawer.show_board()

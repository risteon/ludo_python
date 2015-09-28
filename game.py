#!/usr/bin/env python3

### game.py

from die import Die
from board import Board
from board import BoardField
from board import Player

from BoardDrawer import BoardDrawer

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
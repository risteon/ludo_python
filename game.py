### game.py

from die import Die
from board import Board

print("Welcome to a game of ludo!")

print("Let's test the die:")
the_die = Die()
print(the_die.roll())

print("Let's create a playing board:")
the_board = Board()

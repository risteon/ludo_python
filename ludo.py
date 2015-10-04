#!/usr/bin/env python3
import time
from board import Field

from common_definitions import BoardFieldType, Players, BOARD_FIELD_COUNT
from game import Game

print("Welcome to a game of ludo!")

# Create game instance
game = Game()

# Show board state
game.update_canvas()

user_continue = 'y'

while user_continue == 'y':
    game.next_move()
    game.update_canvas()
    user_continue = input("Input 'y' to continue...")


game.event_finished.set()

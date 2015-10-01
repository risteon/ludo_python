#!/usr/bin/env python3
import time

from common_definitions import BoardFieldType, Players, BOARD_FIELD_COUNT
from game import Game

print("Welcome to a game of ludo!")

# Create game instance
game = Game()

# call test function
game.board.move_pawn(Players.black, 1, (BoardFieldType.FINISH, Players.black, 3))

# Show board state
game.update_canvas()

new_field = game.board.get_next_field(Players.red, 0, 6)
game.board.move_pawn(Players.red, 0, new_field)

while True:
    new_field = game.board.get_next_field(Players.red, 0, 1)
    if not new_field:
        break
    game.board.move_pawn(Players.red, 0, new_field)
    time.sleep(0.25)
    game.update_canvas()

# Show board state
game.update_canvas()

game.event_finished.set()
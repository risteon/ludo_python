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

new_field = game.board.get_next_field(Players.red, 0, 6)
game.board.move_pawn(Players.red, 2, new_field)

# print(game.move_manager.get_valid_moves(Players.yellow, 5))
# print(game.move_manager.get_valid_moves(Players.black, 5))
# print(game.move_manager.get_valid_moves(Players.red, 5))

game.update_canvas()

input("Press Enter to continue...")

game.board.send_home(new_field)

#while True:
#    new_field = game.board.get_next_field(Players.red, 0, 1)
#    if not new_field:
#        break
#    game.board.move_pawn(Players.red, 0, new_field)
#    time.sleep(0.25)
#    game.update_canvas()

# Show board state
game.update_canvas()

game.event_finished.set()

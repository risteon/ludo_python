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

for i in range(BOARD_FIELD_COUNT):
    game.board.move_pawn(Players.black, 0, (BoardFieldType.FIELD, len(Players), i))
    game.board.move_pawn(Players.black, 2, (BoardFieldType.FIELD,
                                            len(Players),
                                            (i+20) % BOARD_FIELD_COUNT))

    game.board.move_pawn(Players.green, 1, (BoardFieldType.FIELD,
                                            len(Players),
                                            (i+30) % BOARD_FIELD_COUNT))
    game.board.move_pawn(Players.green, 3, (BoardFieldType.FIELD,
                                            len(Players),
                                            (i+10) % BOARD_FIELD_COUNT))
    time.sleep(0.25)
    game.update_canvas()

# Show board state
game.update_canvas()

game.event_finished.set()
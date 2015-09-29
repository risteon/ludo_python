#!/usr/bin/env python3

from game import Game

print("Welcome to a game of ludo!")

# Create game instance
game = Game()

# Show board state
game.update_canvas()

# make moves
for i in range(10):
    game.next_move()

# Show board state
game.update_canvas()

# call test function
#game.test_pawn_movement()

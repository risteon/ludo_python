#!/usr/bin/env python3
from game import Game
from common_definitions import Players

print("Welcome to a game of ludo!")

average_throw_counter = 0
min_throws_per_game = 10000000
max_throws_per_game = 0
NUM_GAMES = 100

for i in range(0, NUM_GAMES):

    game = Game()
    throw_counter = 0

    while game.next_move():
        throw_counter += 1

    average_throw_counter += throw_counter
    if throw_counter < min_throws_per_game:
        min_throws_per_game = throw_counter
    if throw_counter > max_throws_per_game:
        max_throws_per_game = throw_counter

    print("Game:", i+1)

print("Average throws:", average_throw_counter/NUM_GAMES)
print("Min", min_throws_per_game)
print("Max", max_throws_per_game)
player = game.players[0]
print("Stats for player number 1:")
print(player.move_stats)
print(player.move_counter)



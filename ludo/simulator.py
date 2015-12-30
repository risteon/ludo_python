#!/usr/bin/env python3
from game import Game
from common_definitions import Players

print("Welcome to a game of ludo!")

average_throw_counter = 0
min_throws_per_game = 10000000
max_throws_per_game = 0
NUM_GAMES = 100

ratio_average = 0
player_win_counter = [0 for player in Players]

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

    for player in game.players:
        ratio = (player.move_stats[1] + player.move_stats[2] + player.move_stats[3])/player.move_counter
        ratio_average += ratio

    player_win_counter[game.finishers[0]] += 1

    print("Game:", i+1)

print("Average throws:", average_throw_counter/NUM_GAMES)
print("Min", min_throws_per_game)
print("Max", max_throws_per_game)

print("Average decisions:", ratio_average/NUM_GAMES/len(game.players))

print("Wins:")
for player in Players:
    print(player, game.players[player].get_desc(), "Wins:", player_win_counter[player])

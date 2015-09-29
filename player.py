# Player

from common_definitions import BoardFieldType, BoardFieldCount, PlayerCount, PawnCount, Players


class Player:

    def __init__(self, player):
        self.player = player
        print("New player: ", player)

    def move(self, number):
        pass
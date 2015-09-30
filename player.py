# Player

from common_definitions import Players


class Player:

    def __init__(self, player):
        assert player in Players

        self.player = player
        print("New player: ", player)

    def move(self, number):
        pass
# Player

from common_definitions import Players
import abc


class PlayerBase:
    __metaclass__ = abc.ABCMeta

    def __init__(self, player, board):
        assert player in Players

        self.player = player
        self.board = board
        print("New player", player, "- Description:", self.get_desc())

    @abc.abstractmethod
    def get_desc(self):
        """"Return description string"""""
        return

    @abc.abstractmethod
    def choose_move(self, moves):
        """"Return chosen pawn to move"""""
        return

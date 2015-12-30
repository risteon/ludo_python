# Player

from common_definitions import Players, PAWN_COUNT
from board import BoardFieldType
from abc import ABCMeta
from abc import abstractmethod


class PlayerBase:
    __metaclass__ = ABCMeta

    def __init__(self, player, board):
        assert player in Players

        self.player = player
        self.board = board

        self.move_stats = [0 for x in range(0, PAWN_COUNT)]
        self.move_counter = 0

        print("New player", player, "- Description:", self.get_desc())

    @abstractmethod
    def get_desc(self):
        return "<ERROR>"

    def choose_move(self, moves):
        self.move_counter += 1
        if not moves:
            self.move_stats[0] += 1
        else:
            # discard come out moves with different pawns
            pawn_ids = [s.pawn_id for s in moves]
            num_from_start = len([True for p in pawn_ids if self.board.pawns[self.player][p].type is BoardFieldType.HOME])
            number_different_moves = len(moves) - num_from_start if num_from_start > 0 else len(moves) - 1
            self.move_stats[number_different_moves] += 1

        return self._choose_move_impl(moves)

    @abstractmethod
    def _choose_move_impl(self, moves):
        """"Return chosen pawn to move"""""
        return

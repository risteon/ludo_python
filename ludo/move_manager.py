#!/usr/bin/env python3

"""
MoveManager class
"""

from enum import IntEnum
from operator import itemgetter
from collections import namedtuple

from board import Board, Field
from common_definitions import PAWN_COUNT, BoardFieldType


""" Priority rules:
    1. Check for hits
    2. Check for setting pawns on board
    3. Check blocked pawns
"""


class MoveType(IntEnum):
    """
    Order!
    """
    HIT = 1
    SET_ON_START = 3
    MOVE_FROM_START = 4
    NORMAL = 5
    NO_MOVE = 6


"""
Move definition: (Pawn-ID | MoveType | NumberOfPoints | To-Field)
"""
Move = namedtuple('Move', ['pawn_id', 'move_type', 'number_of_points', 'to_field'])


class MoveManager:
    def __init__(self, _board):
        self.board = _board

    def get_valid_moves(self, player, number_of_points):

        moves = []

        for pawn_id in range(PAWN_COUNT):
            from_field = self.board.pawns[player][pawn_id]
            to_field = self.board.get_next_field(player, pawn_id, number_of_points)

            move_type = self._check_pawn_move(player, from_field, to_field)

            moves.append(Move(pawn_id, move_type, number_of_points, to_field))

        if not moves:
            return False

        # order and use maximum MoveType value
        moves = sorted(moves, key=itemgetter(1))
        max_value = moves[0].move_type
        if max_value is MoveType.NO_MOVE:
            return False

        return [s for s in moves if s[1] is max_value]

    def perform_move(self, player, move):
        assert move.move_type is not MoveType.NO_MOVE

        if move.move_type is MoveType.HIT:
            self.board.send_home(move.to_field)

        self.board.move_pawn(player, move.pawn_id, move.to_field)

    def _check_pawn_move(self, player, from_field, to_field):

        # pawn cannot move
        if not to_field:
            return MoveType.NO_MOVE

        target_field_occupation = self.board.get_board_field_desc(to_field)

        # occupied by same player - not valid
        if target_field_occupation.player == player:
            return MoveType.NO_MOVE

        # empty, this pawn can move there
        if target_field_occupation.is_occupied():
            return MoveType.HIT

        if self.board.is_player_start_field(player, to_field):
            return MoveType.SET_ON_START

        if self.board.is_player_start_field(player, from_field):
            return MoveType.MOVE_FROM_START

        return MoveType.NORMAL



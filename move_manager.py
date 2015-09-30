#!/usr/bin/env python3

"""
MoveManager class
"""

from board import Board
from common_definitions import PAWN_COUNT


class MoveManager:
    def __init__(self, _board):
        self.board = _board

    """ Rules:
    1. Check for strikes
    2. Check for setting pawns on board
    3. Check blocked pawns
    """
    def check_valid_moves(self, player, die_number):

        #iterate over players pawns:
        for pawn_id in range(PAWN_COUNT):
            pass

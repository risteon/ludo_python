from move_manager import MoveManager, Move
from board import Board, Field
from common_definitions import BoardFieldType, BOARD_FIELD_COUNT,\
                               PAWN_COUNT, Players, MAX_DICE_NUMBER_OF_POINTS

import unittest


class TestMoves(unittest.TestCase):

    def test_valid_moves_in_finish(self):
        board = Board()
        move_manager = MoveManager(board)

        target = Field(type=BoardFieldType.FINISH, player=Players.green, field_index=0)
        board.move_pawn(Players.green, 0, target)

        moves = move_manager.get_valid_moves(Players.green, 1)

        self.assertNotEqual(moves, False, "No valid moves found")


if __name__ == '__main__':
    unittest.main()
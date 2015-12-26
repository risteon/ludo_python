from move_manager import MoveManager, Move, MoveType
from board import Board, Field
from common_definitions import BoardFieldType, BOARD_FIELD_COUNT,\
                               PAWN_COUNT, Players, MAX_DICE_NUMBER_OF_POINTS

import unittest


class TestMoves(unittest.TestCase):

    def test_valid_moves_finish(self):
        board = Board()
        move_manager = MoveManager(board)

        for player in Players:
            self.valid_moves_finish_for_player(board, move_manager, player)

    def valid_moves_finish_for_player(self, board, move_manager, player):
        # set board
        target = Field(type=BoardFieldType.FINISH, player=player, field_index=0)
        board.move_pawn(player, 0, target)

        moves = move_manager.get_valid_moves(player, 1)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=1,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=1))
        self.assertNotEqual(moves, False, "No valid moves found")
        self.assertEquals(moves[0], expected_move)
        moves = move_manager.get_valid_moves(player, 3)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=3,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=3))
        self.assertEquals(moves[0], expected_move)
        moves = move_manager.get_valid_moves(player, 4)
        self.assertEquals(moves, False)
        moves = move_manager.get_valid_moves(player, 5)
        self.assertEquals(moves, False)

        # set board
        target = Field(type=BoardFieldType.FINISH, player=player, field_index=2)
        board.move_pawn(player, 1, target)

        moves = move_manager.get_valid_moves(player, 2)
        self.assertEquals(moves, False)
        moves = move_manager.get_valid_moves(player, 1)
        self.assertEquals(len(moves), 2)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=1,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=1))
        self.assertIn(expected_move, moves)
        expected_move = Move(pawn_id=1, move_type=MoveType.NORMAL, number_of_points=1,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=3))
        self.assertIn(expected_move, moves)

        # set board
        target = Field(type=BoardFieldType.FIELD, player=len(Players),
                       field_index=board._make_global_field_counter(player, BOARD_FIELD_COUNT-1))
        board.move_pawn(player, 0, target)

        moves = move_manager.get_valid_moves(player, 1)
        self.assertEquals(len(moves), 2)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=1,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=0))
        self.assertIn(expected_move, moves)
        expected_move = Move(pawn_id=1, move_type=MoveType.NORMAL, number_of_points=1,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=3))
        self.assertIn(expected_move, moves)
        moves = move_manager.get_valid_moves(player, 2)
        self.assertEquals(len(moves), 1)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=2,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=1))
        self.assertIn(expected_move, moves)
        moves = move_manager.get_valid_moves(player, 3)
        self.assertEquals(moves, False)
        moves = move_manager.get_valid_moves(player, 4)
        self.assertEquals(moves, False)


if __name__ == '__main__':
    unittest.main()
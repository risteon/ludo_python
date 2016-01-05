#!/usr/bin/env python3
from game import Game, MAX_THROWS
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

    def test_board(self):
        board = Board()
        for player in Players:
            self.board_for_player(board, player)

    def test_game(self):
        game = Game()
        b = game.move_manager.board
        player = game.current
        for i in range(0, MAX_THROWS):
            self.assertEqual(player, game.current)
            self.assertEqual(game._execute_move(5), True)
        player = Players.next(player)
        self.assertEqual(player, game.current)
        self.assertEqual(game._execute_move(6), True)
        self.assertEqual(player, game.current)
        self.assertEqual(game._execute_move(1), True)
        player = Players.next(player)
        self.assertEqual(player, game.current)

    def test_player_base(self):
        game = Game()
        player = game.current
        self.assertEqual(game._execute_move(5), True)
        expected_move_stats = [1, 0, 0, 0]
        self.assertListEqual(game.players[player].move_stats, expected_move_stats)
        self.assertEqual(game._execute_move(6), True)
        expected_move_stats = [2, 0, 0, 0]
        self.assertListEqual(game.players[player].move_stats, expected_move_stats)
        self.assertEqual(game._execute_move(6), True)
        expected_move_stats = [3, 0, 0, 0]
        self.assertListEqual(game.players[player].move_stats, expected_move_stats)
        # set all but one pawn on field:
        for i in range(0, 5):
            self.assertEqual(game._execute_move(6), True)
        self.assertEqual(game._execute_move(1), True)
        num_pawns_at_home = len([True for p in range(0, PAWN_COUNT) if game.board.pawns[player][p].type is BoardFieldType.HOME])
        self.assertEqual(num_pawns_at_home, 1)
        expected_move_stats = [9, 0, 0, 0]
        self.assertListEqual(game.players[player].move_stats, expected_move_stats)
        # let all other players roll a 1
        for i in range(0, 9):
            self.assertEqual(game._execute_move(1), True)
        self.assertEqual(game.current, player)
        self.assertEqual(game._execute_move(6), True)
        expected_move_stats = [10, 0, 0, 0]
        self.assertListEqual(game.players[player].move_stats, expected_move_stats)
        self.assertEqual(game._execute_move(2), True)
        self.assertEqual(game.current, Players.next(player))
        expected_move_stats = [11, 0, 0, 0]
        self.assertListEqual(game.players[player].move_stats, expected_move_stats)
        # let all other players roll a 1
        for i in range(0, 9):
            self.assertEqual(game._execute_move(1), True)
        self.assertEqual(game.current, player)
        self.assertEqual(game._execute_move(3), True)
        expected_move_stats = [11, 0, 0, 1]
        self.assertListEqual(game.players[player].move_stats, expected_move_stats)

    def board_for_player(self, board, player):
        # [ ][ ][ ][ ]
        self.assertEqual(board._is_no_space_in_finish(player), True)
        self.assertEqual(board.is_finish_free_in_between(player, 0, 3), True)
        self.assertEqual(board.can_player_only_emerge(player), True)
        # [ ][ ][ ][X]
        board.move_pawn(player, 0, Field(type=BoardFieldType.FINISH, player=player, field_index=PAWN_COUNT-1))
        self.assertEqual(board._is_no_space_in_finish(player), True)
        self.assertEqual(board.is_finish_free_in_between(player, 0, 3), False)
        self.assertEqual(board.is_finish_free_in_between(player, 0, 2), True)
        self.assertEqual(board.is_finish_free_in_between(player, 0, 0), True)
        # [ ][ ][X][ ]
        board.move_pawn(player, 0, Field(type=BoardFieldType.FINISH, player=player, field_index=PAWN_COUNT-2))
        self.assertEqual(board._is_no_space_in_finish(player), False)
        self.assertEqual(board.is_finish_free_in_between(player, 0, 2), False)
        self.assertEqual(board.is_finish_free_in_between(player, 0, 1), True)
        self.assertEqual(board.is_finish_free_in_between(player, 3, 3), True)
        self.assertEqual(board.can_player_only_emerge(player), False)
        # [ ][ ][X][X]
        board.move_pawn(player, 1, Field(type=BoardFieldType.FINISH, player=player, field_index=PAWN_COUNT-1))
        self.assertEqual(board._is_no_space_in_finish(player), True)
        self.assertEqual(board.can_player_only_emerge(player), True)
        #  X [ ][ ][X][X]
        board.move_pawn(player, 2, Field(type=BoardFieldType.FIELD, player=len(Players),
                                         field_index=board._make_global_field_counter(player, BOARD_FIELD_COUNT-1)))
        self.assertEqual(board.can_player_only_emerge(player), False)
        # [X][ ][X][X]
        board.move_pawn(player, 2, Field(type=BoardFieldType.FINISH, player=player, field_index=PAWN_COUNT-4))
        self.assertEqual(board._is_no_space_in_finish(player), False)
        # [X][X][X][X]
        board.move_pawn(player, 3, Field(type=BoardFieldType.FINISH, player=player, field_index=PAWN_COUNT-3))
        self.assertEqual(board._is_no_space_in_finish(player), True)
        self.assertEqual(board.has_player_finished(player), True)

    def valid_moves_finish_for_player(self, board, move_manager, player):
        # set board
        target = Field(type=BoardFieldType.FINISH, player=player, field_index=0)
        board.move_pawn(player, 0, target)

        moves = move_manager.get_valid_moves(player, 1)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=1,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=1))
        self.assertNotEqual(moves, [], "No valid moves found")
        self.assertEqual(moves[0], expected_move)
        moves = move_manager.get_valid_moves(player, 3)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=3,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=3))
        self.assertEqual(moves[0], expected_move)
        moves = move_manager.get_valid_moves(player, 4)
        self.assertEqual(moves, [])
        moves = move_manager.get_valid_moves(player, 5)
        self.assertEqual(moves, [])

        # set board
        target = Field(type=BoardFieldType.FINISH, player=player, field_index=2)
        board.move_pawn(player, 1, target)

        moves = move_manager.get_valid_moves(player, 2)
        self.assertEqual(moves, [])
        moves = move_manager.get_valid_moves(player, 1)
        self.assertEqual(len(moves), 2)
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
        self.assertEqual(len(moves), 2)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=1,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=0))
        self.assertIn(expected_move, moves)
        expected_move = Move(pawn_id=1, move_type=MoveType.NORMAL, number_of_points=1,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=3))
        self.assertIn(expected_move, moves)
        moves = move_manager.get_valid_moves(player, 2)
        self.assertEqual(len(moves), 1)
        expected_move = Move(pawn_id=0, move_type=MoveType.NORMAL, number_of_points=2,
                             to_field=Field(type=BoardFieldType.FINISH, player=player, field_index=1))
        self.assertIn(expected_move, moves)
        moves = move_manager.get_valid_moves(player, 3)
        self.assertEqual(moves, [])
        moves = move_manager.get_valid_moves(player, 4)
        self.assertEqual(moves, [])


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3

from collections import namedtuple

from common_definitions import BoardFieldType, BOARD_FIELD_COUNT,\
                               PAWN_COUNT, Players, MAX_DICE_NUMBER_OF_POINTS

"""
Field definition: (BoardFieldType | Player | Index)
"""
Field = namedtuple('Field', ['type', 'player', 'index'])

class BoardFieldDesc:
    def __init__(self, player):
        assert 0 <= player <= len(Players)
        # init with given player
        self.pawn = player

    def is_occupied(self):
        return self.pawn is not len(Players)

    def set_empty(self):
        self.pawn = len(Players)


class Board:
    def __init__(self):
        # playing fields
        self._fields = {}

        for player in range(len(Players)):
            for index in range(PAWN_COUNT):
                self._fields[(BoardFieldType.FINISH, player, index)] = BoardFieldDesc(len(Players))
                self._fields[(BoardFieldType.HOME, player, index)] = BoardFieldDesc(player)

        for index in range(BOARD_FIELD_COUNT):
            self._fields[(BoardFieldType.FIELD, len(Players), index)] = BoardFieldDesc(len(Players))

        # pawns
        self.pawns = []

        # set all pawns to their respective home fields
        for player in Players:
            pawns = []
            for i in range(PAWN_COUNT):
                pawns.append(Field(BoardFieldType.HOME, player, i))
            self.pawns.append(pawns)

    def get_next_field(self, player, from_field, number_of_points):
        if from_field[0] is BoardFieldType.HOME:
            if number_of_points is not MAX_DICE_NUMBER_OF_POINTS:
                return False
            return self._get_player_start_field(player)

        elif from_field[0] is BoardFieldType.FINISH:
            target_field = from_field[2] + number_of_points
            if target_field > (PAWN_COUNT - 1):
                return False
            return Field(BoardFieldType.FINISH, player, target_field)

        elif from_field[0] is BoardFieldType.FIELD:
            player_field_counter = Board._make_player_field_counter(player, from_field[2])
            target = player_field_counter + number_of_points
            if target < BOARD_FIELD_COUNT:
                return Field(BoardFieldType.FIELD,
                             len(Players),
                             Board._make_global_field_counter(player, target))

            return self.get_next_field(player,
                                       (BoardFieldType.FINISH, player, 0),
                                       target - BOARD_FIELD_COUNT)

        assert False

    def get_board_field_desc(self, field):
        """ Getter for _field array
        :param field:
        :return:
        """
        return self._fields[field]

    @staticmethod
    def _get_player_start_field(player):
        return Field(BoardFieldType.FIELD, len(Players), player * BOARD_FIELD_COUNT / len(Players))

    @staticmethod
    def _make_player_field_counter(player, global_field_counter):
        assert 0 <= global_field_counter < BOARD_FIELD_COUNT
        return (global_field_counter + BOARD_FIELD_COUNT - player * BOARD_FIELD_COUNT / len(Players)) \
            % BOARD_FIELD_COUNT

    @staticmethod
    def _make_global_field_counter(player, player_field_counter):
        assert 0 <= player_field_counter < BOARD_FIELD_COUNT
        return (player_field_counter + player * BOARD_FIELD_COUNT / len(Players)) % BOARD_FIELD_COUNT

    def move_pawn(self, player, pawn_id, to_field):

        assert 0 <= pawn_id < PAWN_COUNT
        assert to_field in self._fields

        # empty current field
        self._fields[self.pawns[player][pawn_id]].set_empty()

        # set pawn
        self.pawns[player][pawn_id] = to_field

        # fill new field
        self._fields[to_field].pawn = player


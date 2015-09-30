#!/usr/bin/env python3

from common_definitions import BoardFieldType, BOARD_FIELD_COUNT,\
                               PAWN_COUNT, Players, MAX_DICE_NUMBER_OF_POINTS


class BoardField:
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
                self._fields[(BoardFieldType.FINISH, player, index)] = BoardField(len(Players))
                self._fields[(BoardFieldType.HOME, player, index)] = BoardField(player)

        for index in range(BOARD_FIELD_COUNT):
            self._fields[(BoardFieldType.FIELD, len(Players), index)] = BoardField(len(Players))

        # pawns
        self.pawns = []

        # set all pawns to their respective home fields
        for player in Players:
            pawns = []
            for i in range(PAWN_COUNT):
                pawns.append((BoardFieldType.HOME, player, i))
            self.pawns.append(pawns)

    def get_next_field(self, player, from_field, dice_dots):
        if from_field[0] is BoardFieldType.HOME:
            if dice_dots is not MAX_DICE_NUMBER_OF_POINTS:
                return False
            return self._get_player_start_field(player)

        elif from_field[0] is BoardFieldType.FINISH:
            target_field = from_field[1] + dice_dots
            if target_field > (PAWN_COUNT - 1):
                return False
            return BoardFieldType.FINISH, target_field

        elif from_field[0] is BoardFieldType.FIELD:
            player_field_counter = Board._make_player_field_counter(player, from_field[1])
            target = player_field_counter + dice_dots
            if target < BOARD_FIELD_COUNT:
                return BoardFieldType.FIELD, Board._make_global_field_counter(player, target)

            return self.get_next_field(player,
                                       (BoardFieldType.FINISH, 0),
                                       target - BOARD_FIELD_COUNT)

        assert False

    @staticmethod
    def _get_player_start_field(player):
        return BoardFieldType.FIELD, len(Players), player * BOARD_FIELD_COUNT / len(Players)

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


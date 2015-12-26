#!/usr/bin/env python3

from collections import namedtuple

from common_definitions import BoardFieldType, BOARD_FIELD_COUNT,\
                               PAWN_COUNT, Players, MAX_DICE_NUMBER_OF_POINTS

"""
Field definition: (BoardFieldType | Player | Index)
"""
Field = namedtuple('Field', ['type', 'player', 'field_index'])


class BoardFieldDesc:
    def __init__(self, player, pawn_id):
        assert 0 <= player <= len(Players)
        assert 0 <= pawn_id < PAWN_COUNT
        # init with given player and pawn_id
        self.player = player
        self.pawn_id = pawn_id

    def is_occupied(self):
        return self.player is not len(Players)

    def set_empty(self):
        self.player = len(Players)
        self.pawn_id = 0


class Board:
    def __init__(self):
        # playing fields
        self._fields = {}

        for player in range(len(Players)):
            for index in range(PAWN_COUNT):
                self._fields[(BoardFieldType.FINISH, player, index)] = BoardFieldDesc(len(Players), 0)
                self._fields[(BoardFieldType.HOME, player, index)] = BoardFieldDesc(player, index)

        for index in range(BOARD_FIELD_COUNT):
            self._fields[(BoardFieldType.FIELD, len(Players), index)] = BoardFieldDesc(len(Players), 0)

        # pawns
        self.pawns = []

        # set all pawns to their respective home fields
        for player in Players:
            pawns = []
            for i in range(PAWN_COUNT):
                pawns.append(Field(BoardFieldType.HOME, player, i))
            self.pawns.append(pawns)

    def move_pawn(self, player, pawn_id, to_field):

        assert 0 <= pawn_id < PAWN_COUNT
        assert to_field in self._fields
        assert not self._fields[to_field].is_occupied()

        # swap from and to field occupation
        self._fields[to_field], self._fields[self.pawns[player][pawn_id]] =\
            self._fields[self.pawns[player][pawn_id]], self._fields[to_field]

        # set pawn
        self.pawns[player][pawn_id] = to_field

    def send_home(self, on_field):
        board_field_desc = self._fields[on_field]
        # there needs to be a pawn!
        assert board_field_desc.is_occupied()

        # set pawn own its 'own' home field
        to_field = Field(BoardFieldType.HOME, board_field_desc.player, board_field_desc.pawn_id)

        self.move_pawn(board_field_desc.player, board_field_desc.pawn_id, to_field)

    def get_next_field(self, player, pawn, number_of_points):
        assert player in Players
        assert 0 <= pawn < PAWN_COUNT

        from_field = self.pawns[player][pawn]
        return self.propagate_field(player, from_field, number_of_points)

    def propagate_field(self, player, from_field, number_of_points):

        if from_field[0] is BoardFieldType.HOME:
            if number_of_points is not MAX_DICE_NUMBER_OF_POINTS:
                return False
            return self._get_player_start_field(player)

        elif from_field[0] is BoardFieldType.FINISH:
            target_field_index = from_field.field_index + number_of_points
            if target_field_index > (PAWN_COUNT - 1):
                return False

            # cannot jump over pawn on finish fields
            if not self.is_finish_free_in_between(player, from_field.field_index, target_field_index):
                return False

            return Field(BoardFieldType.FINISH, player, target_field_index)

        elif from_field[0] is BoardFieldType.FIELD:
            player_field_counter = Board._make_player_field_counter(player, from_field[2])
            target = player_field_counter + number_of_points
            if target < BOARD_FIELD_COUNT:
                return Field(BoardFieldType.FIELD,
                             len(Players),
                             Board._make_global_field_counter(player, target))

            return self.propagate_field(player,
                                        Field(BoardFieldType.FINISH, player, 0),
                                        target - BOARD_FIELD_COUNT)

        assert False

    def get_target_field_desc(self, player, pawn, number_of_points):
        """
        Wrap method get_next_field using pawn array
        :param player:
        :param pawn:
        :param number_of_points:
        :return: BoardFieldDesc of target field
        """
        assert player in Players
        assert 0 <= pawn < PAWN_COUNT
        return self._fields[self.propagate_field(player,
                                                 self.pawns[player][pawn],
                                                 number_of_points)]
        pass

    def get_board_field_desc(self, field):
        """ Getter for _field array
        :param field:
        :return:
        """
        return self._fields[field]

    def is_finish_free_in_between(self, player, index_first_need_free, index_last_need_free):
        assert(0 <= index_first_need_free < 4)
        assert(0 <= index_last_need_free < 4)

        for i in range(int(index_first_need_free + 1), int(index_last_need_free + 1)):
            if self._fields[(BoardFieldType.FINISH, player, i)].is_occupied():
                return False

        return True

    def get_pawn_progress_rating(self, player, pawn_id):

        field = self.pawns[player][pawn_id]

        if field.type == BoardFieldType.HOME:
            return -1

        if field.type == BoardFieldType.FINISH:
            return BOARD_FIELD_COUNT + field.field_index

        return Board._make_player_field_counter(player, field.field_index)

    @staticmethod
    def is_player_start_field(player, field):
        if field.type is not BoardFieldType.FIELD:
            return False

        assert 0 <= field.field_index < BOARD_FIELD_COUNT

        if Board._make_player_field_counter(player, field.field_index) == 0:
            return True

        return False

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

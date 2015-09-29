# Board

from common_definitions import BoardFieldType, BoardFieldCount, PlayerCount, PawnCount, Players


class BoardField:

    def __init__(self):
        # init with empty
        self.pawn = PlayerCount

    def is_occupied(self):
        return self.pawn is not PlayerCount


class Board:
    def __init__(self):
        # playing fields
        self.fields = [BoardField()] * BoardFieldCount
        self.finish = [[[BoardField()] * PawnCount] * PlayerCount]
        # pawns
        self.pawns = []
        for player in Players:
            pawns = []
            for i in range(PawnCount):
                pawns.append((BoardFieldType.HOME, i))
            self.pawns.append(pawns)


    def move_pawn(self):
        print("blubb")

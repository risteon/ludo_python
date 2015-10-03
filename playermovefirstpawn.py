# Player

from playerbase import PlayerBase, Players


class PlayerMoveFirstPawn(PlayerBase):

    def get_desc(self):
        """"Return description string"""""
        return "Always moves the pawn which is furthest from the start"

    def choose_move(self, moves):
        # todo: Fix choosing!

        # return pawn id
        return moves[0][0]

    def notify_cannot_move(self):
        print("I'm so unlucky!")

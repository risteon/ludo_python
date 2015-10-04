# Player

from playerbase import PlayerBase, Players


class PlayerMoveFirstPawn(PlayerBase):

    def get_desc(self):
        """"Return description string"""""
        return "Always moves the pawn which is furthest from the start"

    def choose_move(self, moves):
        if not moves:
            print("I'm so unlucky!")
            return False

        # todo: Fix choosing!

        # return move
        return moves[0]

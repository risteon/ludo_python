# Player

from operator import itemgetter
from playerbase import PlayerBase, Players


class PlayerMoveFirstPawn(PlayerBase):

    def get_desc(self):
        """"Return description string"""""
        return "Always moves the pawn which is furthest from the start"

    def choose_move(self, moves):
        if not moves:
            return False

        if len(moves) > 1:
            progress_list = [(move, self.board.get_pawn_progress_rating(self.player, move.pawn_id))
                             for move in moves]

            priority = sorted(progress_list, key=itemgetter(1), reverse=True)

            # return move
            return priority[0][0]

        return moves[0]

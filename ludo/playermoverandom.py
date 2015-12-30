# Player

from playerbase import PlayerBase, Players
from random import randint


class PlayerMoveRandom(PlayerBase):

    def get_desc(self):
        """"Return description string"""""
        return "Chooses a random pawn to move"

    def _choose_move_impl(self, moves):
        if not moves:
            return None

        return moves[randint(0, len(moves)-1)]

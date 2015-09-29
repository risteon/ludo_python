#!python3

import threading

from BoardDrawer import BoardDrawer
from BoardDrawer import BoardFieldType
from BoardDrawer import Players


class Game:
    def __init__(self):
        # Thread for tk mainloop, this runs until the program gets exited
        self.tk_thread = threading.Thread(target=self._tk_mainloop)
        self.tk_thread.start()

    def test_pawn_movement(self):
        self.board_drawer.move_player(4, BoardFieldType.FIELD, Players.black, 0)
        self.board_drawer.move_player(5, BoardFieldType.FIELD, Players.black, 1)

    def _tk_mainloop(self):
        # print board on tk canvas
        self.board_drawer = BoardDrawer()
        # call mainloop()
        self.board_drawer.show_board()
        # delete tkinter canvas explicitly in THIS thread
        del self.board_drawer


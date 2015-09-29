#!python3

import threading

from board import Board

from boarddrawer import BoardDrawer

from common_definitions import BoardFieldType
from common_definitions import Players


class Game:
    def __init__(self):
        self.board = Board()

        self.event_ready = threading.Event()
        # Look to serialize canvas drawings
        self.lock = threading.Lock()
        # Thread for tk mainloop, this runs until the program gets exited
        self.tk_thread = threading.Thread(target=self._tk_mainloop)
        self.tk_thread.start()

        # Wait for completion of canvas initialization
        self.event_ready.wait()

    def test_pawn_movement(self):
        # Create tasks
        task1 = {'type': "move", 'data': (Players.black, 0, BoardFieldType.FIELD, 4)}
        task2 = {'type': "move", 'data': (Players.black, 2, BoardFieldType.FIELD, 32)}
        task3 = {'type': "move", 'data': (Players.yellow, 3, BoardFieldType.FINISH, 2)}

        # submit tasks
        self.board_drawer.job_queue.put_nowait(task1)
        self.board_drawer.job_queue.put_nowait(task2)
        self.board_drawer.job_queue.put_nowait(task3)

    def _tk_mainloop(self):
        # print board on tk canvas
        self.board_drawer = BoardDrawer()
        # set ready event for main thread to continue initialization
        self.event_ready.set()
        # call mainloop()
        self.board_drawer.show_board()
        # delete tkinter canvas explicitly in THIS thread
        del self.board_drawer

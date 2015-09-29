#!python3

import threading

from board import Board
from player import Player
from die import Die

from boarddrawer import BoardDrawer

from common_definitions import BoardFieldType, PawnCount
from common_definitions import Players


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(p) for p in Players]
        self.current = Players.black
        self.die = Die()

        self.event_ready = threading.Event()
        # Look to serialize canvas drawings
        self.lock = threading.Lock()
        # Thread for tk mainloop, this runs until the program gets exited
        self.tk_thread = threading.Thread(target=self._tk_mainloop)
        self.tk_thread.start()

        # Wait for completion of canvas initialization
        self.event_ready.wait()

    def next_move(self):
        print("It's", self.current, "move")
        while True:
            number = self.die.roll()
            self.players[self.current].move(number)
            if number is not 6:
                break
            print(self.current, "rolls again!")

        self.current = Players.next(self.current)

    def test_pawn_movement(self):
        # Create tasks
        task1 = {'type': "move", 'data': (Players.black, 0, BoardFieldType.FIELD, 4)}
        task2 = {'type': "move", 'data': (Players.black, 2, BoardFieldType.FIELD, 32)}
        task3 = {'type': "move", 'data': (Players.yellow, 3, BoardFieldType.FINISH, 2)}

        # submit tasks
        self.board_drawer.job_queue.put_nowait(task1)
        self.board_drawer.job_queue.put_nowait(task2)
        self.board_drawer.job_queue.put_nowait(task3)

    def update_canvas(self):
        tasks = []
        # iterate over every pawn
        for player in Players:
            for pawn in range(PawnCount):
                tasks.append({'type': "move",
                              'data': (player, pawn, self.board.pawns[player][pawn][0],
                                       self.board.pawns[player][pawn][1])})

        # update every pawn on canvas
        list(map(self.board_drawer.job_queue.put_nowait, tasks))

    def _tk_mainloop(self):
        # print board on tk canvas
        self.board_drawer = BoardDrawer()
        # set ready event for main thread to continue initialization
        self.event_ready.set()
        # call mainloop()
        self.board_drawer.show_board()
        # delete tkinter canvas explicitly in THIS thread
        del self.board_drawer

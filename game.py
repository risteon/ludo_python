#!/usr/bin/env python3

import threading

from board import Board
from playermovefirstpawn import PlayerMoveFirstPawn
from die import Die

from boarddrawer import BoardDrawer

from move_manager import MoveManager

from common_definitions import BoardFieldType, PAWN_COUNT
from common_definitions import Players


class Game:
    def __init__(self):

        self.board = Board()
        self.move_manager = MoveManager(self.board)

        self.players = [PlayerMoveFirstPawn(p, self.board) for p in Players]
        self.current = Players.black
        self.die = Die()

        self.event_ready = threading.Event()
        self.event_finished = threading.Event()
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

    def update_canvas(self):

        tasks = []
        # iterate over every pawn
        for player in Players:
            for pawn in range(PAWN_COUNT):
                tasks.append({'type': "move",
                              'data': (player, pawn, self.board.pawns[player][pawn][0],
                                       self.board.pawns[player][pawn][2])})

        # update every pawn on canvas
        list(map(self.board_drawer.job_queue.put_nowait, tasks))

    def _tk_mainloop(self):
        # print board on tk canvas
        self.board_drawer = BoardDrawer()
        # set ready event for main thread to continue initialization
        self.event_ready.set()
        # call mainloop()
        self.board_drawer.show_board()
        self.event_finished.wait()
        # delete tkinter canvas explicitly in THIS thread
        del self.board_drawer

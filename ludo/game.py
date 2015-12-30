#!/usr/bin/env python3

import threading

from board import Board
from playermovefirstpawn import PlayerMoveFirstPawn
from die import Die

from boarddrawer import BoardDrawer

from move_manager import MoveManager

from common_definitions import BoardFieldType, PAWN_COUNT, MAX_DICE_NUMBER_OF_POINTS
from common_definitions import Players

MAX_THROWS = 3


class Game:
    def __init__(self):

        self.board = Board()
        self.move_manager = MoveManager(self.board)

        self.players = [PlayerMoveFirstPawn(p, self.board) for p in Players]
        self.current = Players.black
        self.die = Die()
        self._retry_counter = 0

        # save finishers
        self.finishers = []

        self.event_ready = threading.Event()
        self.event_finished = threading.Event()
        # Look to serialize canvas drawings
        self.lock = threading.Lock()
        # Thread for tk mainloop, this runs until the program gets exited
        self.tk_thread = threading.Thread(target=self._tk_mainloop)

    def start_tk_visualization(self):
        self.tk_thread.start()
        # Wait for completion of canvas initialization
        self.event_ready.wait()

    def next_move(self):
        # while True:
        #    number = self.die.roll()
        #    self.players[self.current].move(number)
        #    if number is not 6:
        #        break
        #    print(self.current, "rolls again!")

        number = self.die.roll()
        return self._execute_move(number)

    def _execute_move(self, number):
        moves = self.move_manager.get_valid_moves(self.current, number)

        if not self._let_player_execute_move(moves):
            return False

        # roll again when having max number of points
        if number == MAX_DICE_NUMBER_OF_POINTS:
            return True

        if self._retry_counter == 0:
            self._go_to_next_player()
        return True

    def _let_player_execute_move(self, moves):
        move = self.players[self.current].choose_move(moves)

        if move is not None:
            self._retry_counter = 0
            self.move_manager.perform_move(self.current, move)
            if self.move_manager.check_if_finished(self.current):
                assert self.current not in self.finishers
                self.finishers.append(self.current)
                if len(self.finishers) == len(Players):
                    return False

        else:
            if (self.move_manager.board.can_player_only_emerge(self.current) and
                    self._retry_counter < MAX_THROWS-1):
                self._retry_counter += 1
            else:
                self._retry_counter = 0

        return True

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

    def _go_to_next_player(self):
        assert len(self.finishers) < len(Players)
        while True:
            self.current = Players.next(self.current)
            if self.current not in self.finishers:
                break

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

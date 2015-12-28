#!/usr/bin/env python3

import threading

from board import Board
from playermovefirstpawn import PlayerMoveFirstPawn
from die import Die

from boarddrawer import BoardDrawer

from move_manager import MoveManager

from common_definitions import BoardFieldType, PAWN_COUNT, MAX_DICE_NUMBER_OF_POINTS
from common_definitions import Players

MAX_RETRY = 3


class Game:
    def __init__(self):

        self.board = Board()
        self.move_manager = MoveManager(self.board)

        self.players = [PlayerMoveFirstPawn(p, self.board) for p in Players]
        self.current = Players.black
        self.die = Die()
        self.retry_counter = 0

        # save finishers
        self.finishers = []

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
        # while True:
        #    number = self.die.roll()
        #    self.players[self.current].move(number)
        #    if number is not 6:
        #        break
        #    print(self.current, "rolls again!")

        number = self.die.roll()
        moves = self.move_manager.get_valid_moves(self.current, number)
        move = self.players[self.current].choose_move(moves)

        if moves:
            self.retry_counter = 0
            self.move_manager.perform_move(self.current, move)
            if not self.move_manager.check_if_finished(self.current):
                print(self.current, "has rolled a", number, "and moved pawn", move.pawn_id, "- type:", move.move_type,
                      "valid moves:")
            else:
                assert self.current not in self.finishers
                self.finishers.append(self.current)
                print(self.current, "has finished:", len(self.finishers))
                if len(self.finishers) == len(Players):
                    return False

            # roll again when having max number of points
            if number == MAX_DICE_NUMBER_OF_POINTS:
                print("Roll again!")
                return True
        else:
            if (self.move_manager.board.can_player_only_emerge(self.current) and
                    self.retry_counter < MAX_RETRY):
                self.retry_counter += 1
                return True
            else:
                self.retry_counter = 0
                print(self.current, "has rolled a", number, "and cannot move any pawn")

        self._go_to_next_player()
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

        print("Turn:", self.current)

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

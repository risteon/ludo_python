from tkinter import *
import queue

from common_definitions import BoardFieldType
from common_definitions import Players


class BoardDrawer:
    # DIMENSIONS
    GRID_PIXEL_SIZE = 50
    GRID_PIXEL_MARGIN = 5
    GRID_SIZE = 11
    CANVAS_WIDTH = GRID_PIXEL_SIZE * GRID_SIZE
    CANVAS_HEIGHT = GRID_PIXEL_SIZE * GRID_SIZE

    PLAYER_DEFINITIONS = (
        ("#000000", (0, 0), (5, 1), (0, 1)),
        ("#EED016", (0, 9), (1, 5), (1, 0)),
        ("#00FF00", (9, 9), (5, 9), (0, -1)),
        ("#FF0000", (9, 0), (9, 5), (-1, 0))
    )

    PLAYER_START_FIELDS = (0, 0), (0, 1), (1, 0), (1, 1)

    def __init__(self):
        """ Create canvas

        <longer description>
        """
        self.pawns = []
        self.job_queue = queue.Queue()

        self.master = Tk()
        self.master.title("Ludo")
        self.w = Canvas(self.master,
                        width=BoardDrawer.CANVAS_WIDTH,
                        height=BoardDrawer.CANVAS_HEIGHT)
        self.w.pack()

        # Draw board outline
        self.draw_board()

    def update_canvas(self):
        """ can't create custom event for tkinter's main loop,
        so use this timed event loop as alternate solution
        to process update jobs from main game thread
        """
        try:
            while True:
                if not self._process_update_task(self.job_queue.get_nowait()):
                    print("invalid canvas update task!")
                    # is more error handling necessary?
                    # assert False

        except queue.Empty:
            # insert 'update job' into tkinter main loop after given time
            self.master.after(100, self.update_canvas)

    def _process_update_task(self, task):
        if task['type'] == 'move':
            self.move_player(*task['data'])
            return True

        return False

    def draw_board(self):
        # Draw standard playing fields as circles
        for field_number in range(40):
            coord = BoardDrawer._get_grid_coordinates(
                BoardFieldType.FIELD,
                field_number
            )
            self._draw_fields_board(coord, fill="#999999")

        # Draw player home fields
        self._draw_fields_home()

        # Draw player finish fields
        self._draw_fields_finish()

        # Create player pawns on home fields
        self._create_pawns_initial()

    def move_player(self, player, pawn_id, field_type, field_number):
        # change coordinates of existing canvas object
        coords = BoardDrawer._get_grid_coordinates(field_type, field_number, player)
        coords_pixel = BoardDrawer._get_grid_pixel_coordinates(coords)

        self.w.coords(self.pawns[player][pawn_id], coords_pixel[0]+6, coords_pixel[1]+6,
                      coords_pixel[0] + 34, coords_pixel[1] + 34)

    def _draw_fields_home(self):
        for i in range(4):
            for color in Players:
                grid_coord = BoardDrawer._get_grid_coordinates(
                    BoardFieldType.HOME, i, color
                )
                self._draw_fields_board(grid_coord,
                                        fill=BoardDrawer.PLAYER_DEFINITIONS[color][0])

    def _draw_fields_finish(self):
        for i in range(4):
            for color in Players:
                grid_coord = BoardDrawer._get_grid_coordinates(
                    BoardFieldType.FINISH, i, color
                )
                self._draw_fields_board(grid_coord,
                                        fill=BoardDrawer.PLAYER_DEFINITIONS[color][0])

    def _draw_fields_board(self, grid_coordinates, **oval_options):
        pixel_lower = self._get_grid_pixel_coordinates(grid_coordinates)
        return self.w.create_oval(pixel_lower[0], pixel_lower[1],
                                  pixel_lower[0] + 40, pixel_lower[1] + 40,
                                  oval_options)

    def _draw_board_player(self, grid_coordinates, player_color):
        pixel_lower = self._get_grid_pixel_coordinates(grid_coordinates)
        return self.w.create_oval(pixel_lower[0]+6, pixel_lower[1]+6,
                                  pixel_lower[0] + 34, pixel_lower[1] + 34,
                                  fill=player_color, outline="white", width=5.0)

    def _create_pawns_initial(self):
        for color in Players:
            pawns_color = []
            for i in range(4):
                coord = BoardDrawer._get_grid_coordinates(BoardFieldType.HOME, i, color)
                pawns_color.append(self._draw_board_player(
                    coord,
                    BoardDrawer.PLAYER_DEFINITIONS[color][0])
                )

            self.pawns.append(pawns_color)

    @staticmethod
    def tuple_add(xs, ys):
        return tuple(x + y for x, y in zip(xs, ys))

    @staticmethod
    def tuple_multiply(xs, f):
        return tuple(x * f for x in xs)

    def show_board(self):
        # user update canvas loop
        self.update_canvas()
        # tkinter main event loop
        self.master.mainloop()

    @staticmethod
    def _get_grid_coordinates(field_type,
                              field_number,
                              player_color=Players.black):
        if field_type == BoardFieldType.FIELD:
            return BoardDrawer._calculate_field_grid_coordinates(field_number)
        elif field_type == BoardFieldType.FINISH:
            assert 0 <= field_number < 4
            return BoardDrawer.tuple_add(
                BoardDrawer.PLAYER_DEFINITIONS[player_color][2],
                BoardDrawer.tuple_multiply(
                    BoardDrawer.PLAYER_DEFINITIONS[player_color][3],
                    field_number
                )
            )
        elif field_type == BoardFieldType.HOME:
            assert 0 <= field_number < 4
            return BoardDrawer.tuple_add(
                BoardDrawer.PLAYER_DEFINITIONS[player_color][1],
                BoardDrawer.PLAYER_START_FIELDS[field_number]
            )

        assert False

    @staticmethod
    def _calculate_field_grid_coordinates(field_number):

        # Check Range
        assert 0 <= field_number < 40, \
            "field_number out of range (0-39)"

        if field_number < 5:
            return 4, field_number
        elif field_number < 9:
            return 8 - field_number, 4
        elif field_number == 9:
            return 0, 5
        elif field_number < 15:
            return field_number - 10, 6
        elif field_number < 19:
            return 4, field_number - 8
        elif field_number == 19:
            return 5, 10
        elif field_number < 25:
            return 6, 30 - field_number
        elif field_number < 29:
            return field_number - 18, 6
        elif field_number == 29:
            return 10, 5
        elif field_number < 35:
            return 40 - field_number, 4
        elif field_number < 39:
            return 6, 38 - field_number

        return 5, 0

    @staticmethod
    def _get_grid_pixel_coordinates(coordinates):

        return (coordinates[0] * BoardDrawer.GRID_PIXEL_SIZE +
                BoardDrawer.GRID_PIXEL_MARGIN,
                coordinates[1] * BoardDrawer.GRID_PIXEL_SIZE +
                BoardDrawer.GRID_PIXEL_MARGIN)

from tkinter import *
from enum import Enum, unique


class BoardDrawer:

    # DIMENSIONS
    GRID_PIXEL_SIZE = 50
    GRID_PIXEL_MARGIN = 5
    GRID_SIZE = 11
    CANVAS_WIDTH = GRID_PIXEL_SIZE*GRID_SIZE
    CANVAS_HEIGHT = GRID_PIXEL_SIZE*GRID_SIZE

    # Colors
    @unique
    class Colors(Enum):
        black = 0
        yellow = 1
        green = 2
        red = 3

    def __init__(self):
        """ Create canvas

        <longer description>
        """
        self.master = Tk()
        self.canvas = Canvas(self.master,
                             width=BoardDrawer.CANVAS_WIDTH,
                             height=BoardDrawer.CANVAS_HEIGHT)
        self.canvas.pack()

        # Draw board outline
        self.draw_board()

    def draw_board(self):

        # Draw standard playing fields as circles
        for field_number in range(40):
            coord = self.calculate_field_grid_coordinates(field_number)
            pixel_lower = self.get_grid_pixel_coordinates(coord)
            self.canvas.create_oval(pixel_lower[0], pixel_lower[1],
                                    pixel_lower[0] + 40, pixel_lower[1] + 40)

        # Draw player home fields in colors

    def show_board(self):
        self.master.mainloop()

    @staticmethod
    def calculate_field_grid_coordinates(field_number):

        # Check Range
        assert 0 <= field_number < 40, \
               "field_number out of range (0-39)"

        if field_number < 5:
            return 4, field_number
        elif field_number < 9:
            return 8-field_number, 4
        elif field_number == 9:
            return 0, 5
        elif field_number < 15:
            return field_number - 10, 6
        elif field_number < 19:
            return 4, field_number - 8
        elif field_number == 19:
            return 5, 10
        elif field_number < 25:
            return 6, 30-field_number
        elif field_number < 29:
            return field_number-18, 6
        elif field_number == 29:
            return 10, 5
        elif field_number < 35:
            return 40-field_number, 4
        elif field_number < 39:
            return 6, 38-field_number
        
        return 5, 0

    @staticmethod
    def get_grid_pixel_coordinates(coordinates):

        return (coordinates[0]*BoardDrawer.GRID_PIXEL_SIZE +
                BoardDrawer.GRID_PIXEL_MARGIN,
                coordinates[1]*BoardDrawer.GRID_PIXEL_SIZE +
                BoardDrawer.GRID_PIXEL_MARGIN)

